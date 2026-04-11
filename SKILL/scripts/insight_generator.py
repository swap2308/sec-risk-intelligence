import pandas as pd
import numpy as np

def generate_insights(features, rule_score, drivers, validation, anomaly_signal):
    insights = {}

    latest = features.iloc[-1]
    # -----------------------------
    # M-Score (Earnings Manipulation Risk)
    # -----------------------------
    m_score = (
        0.9 * latest.get("dsri", 0) +
        0.5 * latest.get("gmi", 0) +
        0.7 * latest.get("sgi", 0) +
        1.2 * latest.get("tata", 0)
    )
    
    m_score_risk = (
        "High Manipulation Risk 🔴" if m_score > 2.5 else
        "Moderate Manipulation Risk 🟡" if m_score > 1.5 else
        "Low Manipulation Risk 🟢"
    )
    # -----------------------------
    # Financial Summary
    # -----------------------------
    insights["financial_summary"] = {
        "revenue": float(latest.get("revenue", 0)),
        "net_income": float(latest.get("net_income", 0)),
        "profit_margin": float(latest.get("profit_margin", 0)),
        "debt_to_equity": float(latest.get("debt_to_equity", 0))
    }

    # -----------------------------
    # Risk Summary
    # -----------------------------
    insights["risk_summary"] = {
        "risk_score": rule_score,
        "risk_level": (
            "High Risk 🔴" if rule_score >= 70 else
            "Medium Risk 🟡" if rule_score >= 40 else
            "Low Risk 🟢"
        ),
        "confidence_score": validation["confidence_score"]
    }
    # -----------------------------
    # M-Score Insight
    # -----------------------------
    insights["m_score"] = {
        "value": float(m_score),
        "risk_level": m_score_risk
    }

    # -----------------------------
    # Key Drivers
    # -----------------------------
    insights["key_drivers"] = drivers

    # -----------------------------
    # Anomaly Insight
    # -----------------------------
    if anomaly_signal["is_anomaly"]:
        insights["anomaly"] = "Unusual financial pattern detected"
    else:
        insights["anomaly"] = "No significant anomalies detected"

    # -----------------------------
    # Business Interpretation
    # -----------------------------
    interpretation = []

    if latest.get("profit_margin", 0) < 0:
        interpretation.append("Company is operating at a loss")

    if latest.get("debt_to_equity", 0) > 2:
        interpretation.append("Company is highly leveraged")

    if latest.get("revenue_growth", 0) < 0:
        interpretation.append("Revenue is declining")
    if m_score > 2.5:
        interpretation.append("Potential earnings manipulation risk detected")
    elif m_score > 1.5:
        interpretation.append("Some indicators of earnings quality concerns")

    if not interpretation:
        interpretation.append("Company shows stable financial performance")

    insights["interpretation"] = interpretation

    # -----------------------------
    # Recommendations
    # -----------------------------
    recommendations = []

    if rule_score >= 70:
        recommendations.append("Review financial stability before investment")
    elif rule_score >= 40:
        recommendations.append("Monitor key financial metrics closely")
    else:
        recommendations.append("Company appears financially stable")

    insights["recommendations"] = recommendations

    return insights
