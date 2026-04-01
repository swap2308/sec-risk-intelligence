from data_validation import run_validation
from analytics_model import compute_features, detect_anomalies, compute_risk
from model_validation import validate_models
from insight_generation import generate_insights
from report_generator import create_charts, generate_report

import pandas as pd


def main():
    df = pd.read_csv("data/financial_table.csv")

    # Stage 1: Validation
    run_validation(df)

    # Stage 2: Features
    df_features = compute_features(df)

    # Stage 3: Anomaly
    df_anomaly, _ = detect_anomalies(df_features)
    anomaly_signal = {
        "is_anomaly": int(df_anomaly.iloc[-1]['anomaly_flag'] == -1),
        "anomaly_score": float(df_anomaly.iloc[-1]['anomaly_score'])
    }

    # Stage 4: Risk
    score, drivers = compute_risk(df_anomaly)

    # Stage 5: Validation
    validation = validate_models(df_anomaly, score, anomaly_signal)

    # Stage 6: Insights
    insights = generate_insights(df_anomaly, score, drivers, validation, anomaly_signal)

    # Stage 7: Report
    create_charts(df_anomaly)
    generate_report(df_anomaly, insights, validation)


if __name__ == "__main__":
    main()

    