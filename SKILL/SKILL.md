---
name:  SEC Financial Risk Intelligence with M-Score Integration
description: "Analyze company financial data to assess financial risk using feature engineering, anomaly detection, rule-based scoring, and multi-model validation. Produces structured outputs and a professional report."

---

#  SEC Financial Risk Intelligence with M-Score Integration

This skill evaluates **financial risk and potential earnings manipulation** of a company using structured financial data derived from SEC filings.

It combines:

- Deterministic financial ratio analysis  
- Beneish M-Score (fraud detection signals)  
- Machine learning (Isolation Forest anomaly detection)  
- Rule-based risk scoring  
- Model validation and confidence scoring  

The skill is designed to be **auditable, explainable, and production-ready**

---

# What the Skill Expects at Runtime

## 1. Dataset Input

The skill accepts a dataset file provided at runtime.

### Default Dataset (Fallback)

data/financial_table.csv

If no dataset is provided, the system uses the default dataset.

---

### Accepted Formats

* CSV
* Excel
* Parquet

---

### Required Columns

| Column      | Type   | Description         |
| ----------- | ------ | ------------------- |
| cik         | int    | Company identifier  |
| ddate       | date   | Reporting date      |
| revenue     | float  | Total revenue       |
| net_income  | float  | Net income          |
| assets      | float  | Total assets        |
| liabilities | float  | Total liabilities   |
| debt        | float  | Total debt          |
| equity      | float  | Shareholder equity  |
| cash_flow   | float  | Operating cash flow |
| receivables   | float  | receivables |
| cogs   | float  | cogs |
| name        | string | Company name        |

---

### Validation Rules

* `cik`, `ddate` must not be null
* Numeric columns must be valid floats
* `ddate` must be parseable
* Reject dataset if:

  * > 30% nulls in critical columns
  * Duplicate rows >10%

---

## 2. User Configuration Inputs

| Parameter       | Type | Default  | Description                      |
| --------------- | ---- | -------- | -------------------------------- |
| cik             | int  | required | Company to analyze               |
| lookback_period | int  | 3        | Number of periods used for trend |
| risk_threshold  | int  | 70       | High risk cutoff                 |

---

# Analytics Pipeline

---

## Stage 1: Data Validation & Profiling

### Script Execution

Run:

python scripts/data_validation.py 
--input-data data/financial_table.csv 
--output outputs/validation.json

---

### Steps

* Compute row count and column count
* Compute null percentage per column
* Detect duplicate rows
* Validate data types
* Detect outliers using IQR

---

### Output Format

{
"status": "success",
"row_count": int,
"column_count": int,
"null_percentage": dict,
"warnings": list,
"errors": list
}

---

## Stage 2: Data Preparation & Feature Engineering

### Script Execution

python scripts/analytics_model.py 
--input-data data/financial_table.csv 
--output outputs/model_output.json

---

### Computations

For each `cik`, sort data by `ddate`.

Compute:

* revenue_growth = (revenue_t − revenue_t-1) / revenue_t-1
* profit_margin = net_income / revenue
* debt_to_equity = debt / equity
* cash_flow_ratio = cash_flow / revenue
* liability_ratio = liabilities / assets
* revenue_volatility = std(revenue.pct_change() over last 3 periods)
* revenue_trend = mean(revenue.pct_change() over last 3 periods)

---

## Stage 3: Modelling & Analysis

### Models Used

Model 1: Rule-Based Risk Scoring
Model 2: Isolation Forest Anomaly Detection

---
Core Financial Features

| Feature | Formula |
|--------|--------|
| Revenue Growth | (Revenue - Prev Revenue) / Prev Revenue |
| Profit Margin | Net Income / Revenue |
| Debt-to-Equity | Debt / Equity |
| Cash Flow Ratio | Cash Flow / Revenue |
| Liability Ratio | Liabilities / Assets |

### Risk Model Logic

* Profit margin < 0 → +30 risk
* Profit margin < 5% → +15 risk
* Revenue growth < -10% → +30 risk
* Revenue growth < 0 → +20 risk
* Debt-to-equity > 3 → +30 risk
* Debt-to-equity > 2 → +20 risk
* Negative cash flow → +25 risk
* Liabilities > Assets → +25 risk
* High volatility (>0.3) → +10 risk
* Anomaly detected → +20 risk

---

### Model Output Format

{
"company": string,
"cik": int,
"risk_score": int,
"risk_level": string,
"drivers": list,
"anomaly": {
"is_anomaly": int,
"anomaly_score": float
},
"validation": {
"agreement": boolean,
"stability_score": float,
"anomaly_strength": float,
"confidence_score": float
}
}

---

## Stage 4: Model Validation

### Script Execution

python scripts/analytics_model.py 
--input-data data/financial_table.csv 
--output outputs/model_output.json

---

### Multi-Algorithm Comparison

Compare:

* Rule-Based Risk Model
* Isolation Forest

Metrics:

* Model Agreement = (risk_band == anomaly_band)
* Stability Score = 1 − volatility
* Anomaly Strength = − anomaly_score

---

### Validation Thresholds

* Risk Score: 0–39 Low, 40–69 Medium, 70–100 High
* Volatility: >0.3 indicates instability
* Anomaly score < -0.1 indicates strong anomaly

---

### Decision Logic

* Both high → Confirmed Risk
* Rule only → Financial Risk
* Anomaly only → Hidden Risk
* None → Stable

---

## Stage 5: Insight Generation & Interpretation

### Script Execution

python scripts/insight_generation.py

---

### Steps

1. Use computed outputs:

   * risk_score
   * drivers
   * anomaly signals
   * validation metrics

2. Consult REFERENCE.md:

   * Financial meaning of ratios
   * Risk thresholds
   * Business implications

3. Generate:

   * Financial summary
   * Risk explanation
   * Business interpretation

---

## Stage 6: Report Generation

### Script Execution

python scripts/report_generator.py 
--input-data data/financial_table.csv 
--model-output outputs/model_output.json 
--output outputs/report.html

---

## Visualisations

The report must include:

1. Revenue Trend Chart
2. Net Income Trend Chart
3. Debt-to-Equity Trend
4. Cash Flow Trend

---

## Report Structure

1. Executive Summary
2. Methodology
3. Data Quality Summary
4. Results (with charts)
5. Validation Metrics
6. Business Interpretation
7. Recommendations
8. Limitations

---

### Output

outputs/report.html

---

# End-to-End Execution

Run full pipeline:

python scripts/main.py 
--input-data data/financial_table.csv 
--output-report outputs/report.html

---

# Important Notes

1. This is not financial advice
2. Results depend on data quality
3. Risk score is indicative
4. Combines rule-based and anomaly models

---

# No Shortcuts

Each stage must:

* Execute independently
* Validate outputs
* Pass structured data forward

---

# Future Enhancements

* NLP (MD&A analysis)
* Market data integration
* Peer benchmarking
* Forecasting
