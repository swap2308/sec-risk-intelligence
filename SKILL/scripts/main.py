from data_validation import run_validation
from analytics_model import (
    compute_features,
    prepare_m_score_features,   
    detect_anomalies,
    compute_risk_score         
)
from model_validation import validate_models
from insight_generation import generate_insights
from report_generator import create_charts, generate_report


def main():
    # -----------------------------
    # Load Data
    # -----------------------------
    df = pd.read_csv("data/financial_table.csv")
    df['ddate'] = pd.to_datetime(df['ddate'])

    # -----------------------------
    # Stage 1: Validation
    # -----------------------------
    run_validation(df)

    # -----------------------------
    # Stage 2: Feature Engineering
    # -----------------------------
    df_features = compute_features(df)

    # -----------------------------
    # Stage 2.1: M-Score Features  
    # -----------------------------
    df_features = prepare_m_score_features(df_features)

    # -----------------------------
    # Stage 3: Anomaly Detection
    # -----------------------------
    df_anomaly = detect_anomalies(df_features, df_features)

    latest = df_anomaly.iloc[-1]

    anomaly_signal = {
        "is_anomaly": int(latest['anomaly_flag'] == -1),
        "anomaly_score": float(latest['anomaly_score'])
    }

    # -----------------------------
    # Stage 4: Risk Scoring (includes M-score)
    # -----------------------------
    score, drivers = compute_risk_score(df_anomaly)

    # -----------------------------
    # Stage 5: Model Validation
    # -----------------------------
    validation = validate_models(df_anomaly, score)

    # -----------------------------
    # Stage 6: Insight Generation
    # -----------------------------
    insights = generate_insights(
        df_anomaly,
        score,
        drivers,
        validation,
        anomaly_signal
    )

    # Optional: add identifiers for report
    latest = df_anomaly.iloc[-1]
    insights["company"] = str(latest.get("name", "Unknown"))
    insights["cik"] = int(latest.get("cik", 0))
    insights["risk_score"] = score
    insights["risk_level"] = (
        "High" if score >= 70 else
        "Medium" if score >= 40 else
        "Low"
    )

    # -----------------------------
    # Stage 7: Report Generation
    # -----------------------------
    create_charts(df_anomaly)
    generate_report(df_anomaly, insights, validation)


if __name__ == "__main__":
    main()
    
