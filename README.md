#  SEC Financial Risk Intelligence Agent

##  Overview

The **SEC Financial Risk Intelligence Agent** is an end-to-end analytics system that evaluates company financial health using structured financial data.
It applies feature engineering, anomaly detection, rule-based scoring, and model validation to generate explainable risk insights and a professional report.

This project follows a **deterministic analytics pipeline** and is designed as an LLM-compatible skill.

---

##  Objective

To analyze company financial data and:

* Detect financial risk
* Identify anomalies
* Evaluate stability and trends
* Generate explainable insights
* Produce a professional report

---

##  Project Structure

```plaintext
sec-risk-intelligence/
│
├── data/
│   └── financial_table.csv
│
├── scripts/
│   ├── data_validation.py
│   ├── analytics_model.py
│   ├── insight_generation.py
│   ├── report_generator.py
│   ├── main.py
│
├── outputs/
│   ├── validation.json
│   ├── model_output.json
│   ├── report.html
│   ├── revenue.png
│   └── net_income.png
│
├── SKILL.md
├── REFERENCE.md
└── README.md
```

---

## 📊 Dataset

The dataset contains financial information derived from SEC filings.

### Required Columns

* cik
* ddate
* revenue
* net_income
* assets
* liabilities
* debt
* equity
* cash_flow
* name

---

##  Analytics Pipeline

The system follows a structured 6-stage workflow:

### 1. Data Validation & Profiling

* Checks schema, nulls, duplicates, data types
* Outputs: `validation.json`

---

### 2. Feature Engineering

Computed features:

* Revenue growth
* Profit margin
* Debt-to-equity
* Cash flow ratio
* Liability ratio
* Revenue volatility
* Revenue trend

---

### 3. Modelling

#### Model 1: Rule-Based Risk Scoring

Evaluates:

* Profitability
* Growth
* Leverage
* Liquidity
* Solvency

#### Model 2: Anomaly Detection

* Isolation Forest
* Detects unusual financial patterns

---

### 4. Model Validation

Compares models using:

* Model agreement
* Stability (volatility-based)
* Anomaly strength

---

### 5. Insight Generation

Produces:

* Risk explanation
* Business interpretation
* Key drivers
* Recommendations

---

### 6. Report Generation

Generates a professional HTML report including:

* Executive summary
* Methodology
* Data quality
* Results with charts
* Validation metrics
* Business interpretation
* Recommendations
* Limitations

---

##  Outputs

| File                | Description           |
| ------------------- | --------------------- |
| `validation.json`   | Data quality report   |
| `model_output.json` | Risk analysis results |
| `report.html`       | Final business report |

---

##  How to Run

### Run Full Pipeline

```bash
python scripts/main.py \
  --input-data data/financial_table.csv \
  --output-report outputs/report.html
```

---

### Run Individual Stages

#### Data Validation

```bash
python scripts/data_validation.py \
  --input-data data/financial_table.csv \
  --output outputs/validation.json
```

#### Analytics Model

```bash
python scripts/analytics_model.py \
  --input-data data/financial_table.csv \
  --output outputs/model_output.json
```

#### Report Generation

```bash
python scripts/report_generator.py \
  --input-data data/financial_table.csv \
  --model-output outputs/model_output.json \
  --output outputs/report.html
```

---

##  Sample Output

### Risk Summary

* Risk Score: 62
* Risk Level: Medium

### Key Drivers

* Low profit margin
* Moderate leverage
* Weak revenue growth

---

##  Key Features

* Deterministic analytics pipeline
* Multi-model comparison
* Explainable risk scoring
* Structured JSON outputs
* Professional HTML reporting
* Modular script design

---

##  Limitations

* Based only on financial data
* No market or sentiment data
* Industry variations not modeled
* Risk score is indicative, not predictive

---

##  Future Enhancements

* NLP analysis of SEC filings (MD&A)
* Market data integration
* Peer benchmarking
* Forecasting models

---

##  Conclusion

This project demonstrates a **production-style analytics workflow** combining financial modeling, anomaly detection, and explainable AI to generate actionable business insights.

---
