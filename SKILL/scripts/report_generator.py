import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os


# -----------------------------
# Create Charts
# -----------------------------
def create_charts(df):
    os.makedirs("outputs", exist_ok=True)

    # Revenue trend
    plt.figure()
    df.sort_values('ddate')['revenue'].plot(title="Revenue Trend")
    plt.xlabel("Time")
    plt.ylabel("Revenue")
    plt.savefig("outputs/revenue.png")
    plt.close()

    # Net income trend
    plt.figure()
    df.sort_values('ddate')['net_income'].plot(title="Net Income Trend")
    plt.savefig("outputs/net_income.png")
    plt.close()


# -----------------------------
# Generate HTML Report
# -----------------------------
def generate_report(df, insights, validation, output_path="outputs/report.html"):

    latest = df.iloc[-1]

    html = f"""
    <html>
    <head>
        <title>Financial Risk Report</title>
        <style>
            body {{ font-family: Arial; margin: 40px; background: #f4f6f8; }}
            h1, h2 {{ color: #2c3e50; }}
            .card {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}
        </style>
    </head>

    <body>

    <h1>📊 Financial Risk Intelligence Report</h1>
    <p><b>Generated:</b> {datetime.now()}</p>

    <!-- Executive Summary -->
    <div class="card">
        <h2>Executive Summary</h2>
        <p>Risk Score: {insights['risk_score']}</p>
        <p>Risk Level: {insights['risk_level']}</p>
        <p>Confidence: {validation['confidence_score']}%</p>
    </div>

    <!-- Methodology -->
    <div class="card">
        <h2>Methodology</h2>
        <ul>
            <li>Feature engineering (growth, margin, leverage)</li>
            <li>Rule-based risk scoring</li>
            <li>Isolation Forest anomaly detection</li>
            <li>Model validation using agreement and stability</li>
        </ul>
    </div>

    <!-- Data Quality -->
    <div class="card">
        <h2>Data Quality Summary</h2>
        <p>Total Records: {len(df)}</p>
        <p>Columns: {list(df.columns)}</p>
    </div>

    <!-- Results -->
    <div class="card">
        <h2>Results</h2>
        <img src="revenue.png" width="600"/>
        <img src="net_income.png" width="600"/>
    </div>

    <!-- Validation -->
    <div class="card">
        <h2>Validation Metrics</h2>
        <p>Model Agreement: {validation['agreement']['agreement']}</p>
        <p>Stability Score: {validation['stability']['stability_score']}</p>
        <p>Anomaly Strength: {validation['anomaly_strength']}</p>
    </div>

    <!-- Interpretation -->
    <div class="card">
        <h2>Business Interpretation</h2>
        <ul>
            {"".join([f"<li>{i}</li>" for i in insights['interpretation']])}
        </ul>
    </div>

    <!-- Recommendations -->
    <div class="card">
        <h2>Recommendations</h2>
        <ul>
            {"".join([f"<li>{r}</li>" for r in insights['recommendations']])}
        </ul>
    </div>

    <!-- Limitations -->
    <div class="card">
        <h2>Limitations</h2>
        <ul>
            <li>Based only on financial data</li>
            <li>No market or sentiment data</li>
            <li>Indicative, not predictive</li>
        </ul>
    </div>

    </body>
    </html>
    """

    with open(output_path, "w") as f:
        f.write(html)

    return output_path

