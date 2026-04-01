"""
report_generator.py  

Performs:
1. Chart generation (revenue, net income trends)
2. HTML report creation with embedded charts and validation metrics
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os


# ─────────────────────────────────────────────────────────────
# Charts
# ─────────────────────────────────────────────────────────────
def create_charts(df: pd.DataFrame, out_dir: str = "outputs") -> None:
    os.makedirs(out_dir, exist_ok=True)
    df = df.sort_values('ddate')

    for col, title, fname in [
        ('revenue',    'Revenue Trend',    'revenue.png'),
        ('net_income', 'Net Income Trend', 'net_income.png'),
    ]:
        if col not in df.columns:
            continue
        fig, ax = plt.subplots()
        ax.plot(df['ddate'], df[col], marker='o')
        ax.set_title(title)
        ax.set_xlabel('Date')
        ax.set_ylabel('USD')
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, fname))
        plt.close(fig)


# ─────────────────────────────────────────────────────────────
# HTML Report
# ─────────────────────────────────────────────────────────────
def generate_report(
    df: pd.DataFrame,
    insights: dict,
    validation: dict,
    output_path: str = "outputs/report.html",
) -> str:
    """
    FIX 6: All validation values accessed with single-level keys, matching
    the flat dict returned by validate_models():
        validation['agreement']        (bool)
        validation['stability_score']  (float)
        validation['anomaly_strength'] (float)
        validation['confidence_score'] (float)
        validation['decision']         (str)
    """
    create_charts(df, out_dir=os.path.dirname(output_path) or "outputs")

    # ── safe value helpers ──────────────────────────────────
    agreement_val  = validation.get('agreement', 'N/A')
    stability_val  = validation.get('stability_score', 'N/A')   # FIX 6
    strength_val   = validation.get('anomaly_strength', 'N/A')
    confidence_val = validation.get('confidence_score', 'N/A')
    decision_val   = validation.get('decision', 'N/A')

    interp_items = "".join(
        f"<li>{i}</li>" for i in insights.get('interpretation', [])
    )
    recom_items  = "".join(
        f"<li>{r}</li>" for r in insights.get('recommendations', [])
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Financial Risk Report</title>
  <style>
    body  {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f6f8; color: #222; }}
    h1,h2 {{ color: #2c3e50; }}
    .card {{
      background: white; padding: 20px; border-radius: 8px;
      margin-bottom: 20px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    table {{ border-collapse: collapse; width: 100%; }}
    th,td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
    th    {{ background: #eaf0fb; }}
    img   {{ max-width: 100%; height: auto; margin-top: 10px; }}
  </style>
</head>
<body>

<h1>📊 Financial Risk Intelligence Report</h1>
<p><b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

<!-- Executive Summary -->
<div class="card">
  <h2>Executive Summary</h2>
  <table>
    <tr><th>Company</th><td>{insights.get('company', 'N/A')}</td></tr>
    <tr><th>CIK</th><td>{insights.get('cik', 'N/A')}</td></tr>
    <tr><th>Risk Score</th><td>{insights.get('risk_score', 'N/A')} / 100</td></tr>
    <tr><th>Risk Level</th><td>{insights.get('risk_level', 'N/A')}</td></tr>
    <tr><th>Decision</th><td>{decision_val}</td></tr>
    <tr><th>Confidence</th><td>{confidence_val}%</td></tr>
  </table>
</div>

<!-- Methodology -->
<div class="card">
  <h2>Methodology</h2>
  <ul>
    <li>Feature engineering: revenue growth, profit margin, leverage, cash flow, solvency</li>
    <li>Beneish M-Score proxy indices (DSRI, GMI, SGI, TATA)</li>
    <li>Rule-based risk scoring with weighted driver penalties</li>
    <li>Isolation Forest anomaly detection (trained on full dataset)</li>
    <li>Multi-model validation: agreement, stability, anomaly strength</li>
  </ul>
</div>

<!-- Data Quality -->
<div class="card">
  <h2>Data Quality Summary</h2>
  <table>
    <tr><th>Records for company</th><td>{len(df)}</td></tr>
    <tr><th>Columns</th><td>{', '.join(df.columns.tolist())}</td></tr>
  </table>
</div>

<!-- Results / Charts -->
<div class="card">
  <h2>Financial Trends</h2>
  <img src="revenue.png"    alt="Revenue Trend"/>
  <img src="net_income.png" alt="Net Income Trend"/>
</div>

<!-- Validation Metrics  ← FIX 6: flat key access -->
<div class="card">
  <h2>Validation Metrics</h2>
  <table>
    <tr><th>Model Agreement</th><td>{agreement_val}</td></tr>
    <tr><th>Stability Score</th><td>{stability_val}</td></tr>
    <tr><th>Anomaly Strength</th><td>{strength_val}</td></tr>
    <tr><th>Confidence Score</th><td>{confidence_val}%</td></tr>
  </table>
</div>

<!-- Business Interpretation -->
<div class="card">
  <h2>Business Interpretation</h2>
  <ul>{interp_items}</ul>
</div>

<!-- Recommendations -->
<div class="card">
  <h2>Recommendations</h2>
  <ul>{recom_items}</ul>
</div>

<!-- Limitations -->
<div class="card">
  <h2>Limitations</h2>
  <ul>
    <li>Analysis is based solely on reported financial data</li>
    <li>No market, sentiment, or macroeconomic data is incorporated</li>
    <li>Risk score is indicative, not predictive</li>
    <li>Results depend on completeness and accuracy of input data</li>
  </ul>
</div>

</body>
</html>"""

    os.makedirs(os.path.dirname(output_path) or "outputs", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
