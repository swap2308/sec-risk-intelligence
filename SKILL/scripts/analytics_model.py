"""
analytics_model.py

Performs:
1. Feature engineering
2. Anomaly detection (Isolation Forest)
3. Risk scoring (rule-based v2)
4. Model validation & comparison

Input:
    CSV file with financial data

Output:
    outputs/model_output.json
"""

import pandas as pd
import numpy as np
import json
import argparse
import os
import sys

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# -----------------------------
# Feature Engineering
# -----------------------------
def compute_features(df):
    df = df.sort_values(['cik', 'ddate'])

    # Lag
    df['prev_revenue'] = df.groupby('cik')['revenue'].shift(1)

    # Growth
    df['revenue_growth'] = (df['revenue'] - df['prev_revenue']) / (df['prev_revenue'] + 1e-6)

    # Profitability
    df['profit_margin'] = df['net_income'] / (df['revenue'] + 1e-6)

    # Leverage
    df['debt_to_equity'] = df['debt'] / (df['equity'] + 1e-6)

    # Liquidity
    df['cash_flow_ratio'] = df['cash_flow'] / (df['revenue'] + 1e-6)

    # Solvency
    df['liability_ratio'] = df['liabilities'] / (df['assets'] + 1e-6)

    # Volatility
    df['revenue_volatility'] = df.groupby('cik')['revenue'].pct_change().rolling(3).std().reset_index(level=0, drop=True)

    # Trend
    df['revenue_trend'] = df.groupby('cik')['revenue'].pct_change().rolling(3).mean().reset_index(level=0, drop=True)

    return df


# -----------------------------
# Anomaly Detection
# -----------------------------
def detect_anomalies(df):
    features = [
        'revenue', 'net_income', 'debt', 'equity',
        'cash_flow', 'assets', 'liabilities',
        'profit_margin', 'debt_to_equity', 'revenue_growth'
    ]

    features = [col for col in features if col in df.columns]

    X = df[features].replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(n_estimators=150, contamination=0.1, random_state=42)

    df['anomaly_flag'] = model.fit_predict(X_scaled)
    df['anomaly_score'] = model.decision_function(X_scaled)

    return df


# -----------------------------
# Risk Model (v2)
# -----------------------------
def compute_risk_score(df):
    df = df.sort_values('ddate')

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    risk = 0
    drivers = []

    # Profitability
    pm = latest['profit_margin']
    if pm < 0:
        risk += 30
        drivers.append("Negative profitability")
    elif pm < 0.05:
        risk += 15
        drivers.append("Low margin")

    # Growth
    growth = latest['revenue_growth']
    if growth < -0.1:
        risk += 30
        drivers.append("Sharp revenue decline")
    elif growth < 0:
        risk += 20
        drivers.append("Declining revenue")

    # Leverage
    dte = latest['debt_to_equity']
    if dte > 3:
        risk += 30
        drivers.append("Very high leverage")
    elif dte > 2:
        risk += 20
        drivers.append("High leverage")

    # Cash Flow
    if latest['cash_flow'] < 0:
        risk += 25
        drivers.append("Negative cash flow")

    # Solvency
    if latest['liabilities'] > latest['assets']:
        risk += 25
        drivers.append("Liabilities exceed assets")

    # Volatility
    if latest.get('revenue_volatility', 0) > 0.3:
        risk += 10
        drivers.append("High volatility")

    # Anomaly
    if latest['anomaly_flag'] == -1:
        risk += 20
        drivers.append("Anomalous pattern")

    return min(risk, 100), drivers


# -----------------------------
# Model Validation
# -----------------------------
def validate_models(df, risk_score):
    latest = df.iloc[-1]

    anomaly_flag = 1 if latest['anomaly_flag'] == -1 else 0
    anomaly_score = latest['anomaly_score']

    # Risk band
    if risk_score >= 70:
        rule_band = "high"
    elif risk_score >= 40:
        rule_band = "medium"
    else:
        rule_band = "low"

    anomaly_band = "high" if anomaly_flag else "low"

    agreement = (rule_band == anomaly_band)

    volatility = df['revenue'].pct_change().std()
    stability = max(0, 1 - volatility)

    strength = max(0, -anomaly_score)

    confidence = round((
        0.3 * min(1, len(df)/5) +
        0.3 * (1 if agreement else 0.5) +
        0.2 * stability +
        0.2 * (1 - strength)
    ) * 100, 2)

    return {
        "agreement": agreement,
        "stability_score": float(stability),
        "anomaly_strength": float(strength),
        "confidence_score": confidence
    }


# -----------------------------
# Main Execution
# -----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", required=True)
    parser.add_argument("--output", default="outputs/model_output.json")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input_data)

        # Feature Engineering
        df = compute_features(df)

        # Anomaly Detection
        df = detect_anomalies(df)

        # Risk Model
        risk_score, drivers = compute_risk_score(df)

        # Validation
        validation = validate_models(df, risk_score)

        # Output formatting
        risk_level = (
            "High" if risk_score >= 70 else
            "Medium" if risk_score >= 40 else
            "Low"
        )

        latest = df.iloc[-1]

        output = {
            "company": str(latest.get("name", "Unknown")),
            "cik": int(latest["cik"]),
            "risk_score": int(risk_score),
            "risk_level": risk_level,
            "drivers": drivers,
            "anomaly": {
                "is_anomaly": int(latest['anomaly_flag'] == -1),
                "anomaly_score": float(latest['anomaly_score'])
            },
            "validation": validation
        }

        os.makedirs("outputs", exist_ok=True)

        with open(args.output, "w") as f:
            json.dump(output, f, indent=4)

        print(json.dumps(output, indent=2))

    except Exception as e:
        error = {"status": "error", "message": str(e)}
        print(json.dumps(error))
        sys.exit(1)


if __name__ == "__main__":
    main()