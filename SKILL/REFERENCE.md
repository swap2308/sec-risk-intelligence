# REFERENCE.md 
-— Financial Risk Intelligence Domain Knowledge

---

# 1. Financial Feature Definitions

## 1.1 Revenue Growth

**Formula:**
Revenue Growth = (Current Revenue - Previous Revenue) / Previous Revenue

**Business Meaning:**
Measures company expansion. Sustained negative growth signals declining demand or competitive pressure.

---

## 1.2 Profit Margin

**Formula:**
Profit Margin = Net Income / Revenue

**Business Meaning:**
Indicates operational efficiency. Low or negative margins suggest cost pressure or weak pricing power.

---

## 1.3 Debt-to-Equity Ratio

**Formula:**
Debt-to-Equity = Total Debt / Shareholder Equity

**Business Meaning:**
Measures leverage. High values indicate financial risk due to debt burden.

---

## 1.4 Asset Coverage Ratio

**Formula:**
Asset Coverage = Assets / Debt

**Business Meaning:**
Indicates ability to cover liabilities with assets. Low values suggest solvency risk.

---

## 1.5 Operating Cash Flow Ratio

**Formula:**
Operating Cash Flow Ratio = Operating Cash Flow / Revenue

**Business Meaning:**
Reflects real cash generation. Negative values indicate potential liquidity issues.

---

## 1.6 Revenue Volatility

**Formula:**
Standard deviation of revenue growth over recent periods

**Business Meaning:**
High volatility indicates unstable business performance.

---

## 1.7 Revenue Trend

**Formula:**
Rolling average of recent revenue growth

**Business Meaning:**
Captures direction of business momentum (growth vs decline).

---

# 2. Risk Scoring Framework

## Risk Levels

| Score Range | Risk Level  |
| ----------- | ----------- |
| 0–39        | Low Risk    |
| 40–69       | Medium Risk |
| 70–100      | High Risk   |

---

## Risk Drivers

### Profitability Risk

* Profit margin < 0 → Severe risk
* Profit margin < 5% → Moderate risk

---

### Growth Risk

* Revenue growth < 0 → Negative trend
* Revenue growth < -10% → Severe decline

---

### Leverage Risk

* Debt-to-equity > 2 → High risk
* Debt-to-equity > 3 → Critical risk

---

### Cash Flow Risk

* Negative operating cash flow → High risk
* Low cash flow ratio (<5%) → Weak sustainability

---

### Balance Sheet Risk

* Equity ≤ 0 → Critical financial distress

---

### Stability Risk

* High volatility (>0.3) → Unstable performance
* Negative trend → Deterioration signal

---

# 3. Anomaly Detection Framework

## Method

Isolation Forest algorithm

---

## Interpretation

| Output | Meaning                             |
| ------ | ----------------------------------- |
| -1     | Anomaly (unusual financial pattern) |
| 1      | Normal                              |

---

## Business Meaning

Anomalies may indicate:

* Sudden revenue spikes/drops
* Accounting irregularities
* Structural business change

---

# 4. Multi-Model Comparison Framework

The system uses two analytical approaches:

1. Rule-Based Risk Scoring  
2. Isolation Forest Anomaly Detection  


## 4.1 Model Agreement

Compare:

* Rule-based risk score
* Anomaly detection result

---

## 4.2 Stability

Measured using revenue volatility

* Low volatility → stable business
* High volatility → uncertain performance

---

## 4.3 Confidence Score

Factors:

* Data sufficiency
* Model agreement
* Stability
* Anomaly strength

---
## Decision Logic

- If both models indicate high risk → Confirmed risk  
- If only rule model indicates risk → Financial risk  
- If only anomaly model indicates risk → Hidden or emerging risk  
- If neither → Stable  

The final decision is based on combined interpretation of both models.

# 5. Interpretation Framework

## Low Risk

* Stable revenue growth
* Healthy margins
* Controlled leverage

---

## Medium Risk

* Moderate leverage
* Weak margins
* Inconsistent growth

---

## High Risk

* Negative profitability
* High debt burden
* Declining revenue
* Negative equity

---

# 6. Recommendation Templates

## Low Risk

* Maintain current strategy
* Monitor trends periodically

---

## Medium Risk

* Improve margins
* Reduce leverage
* Monitor financial signals closely

---

## High Risk

* Investigate financial distress
* Reduce debt exposure
* Improve liquidity
* Consider restructuring

---

# 7. Industry Benchmarks (General)

| Metric          | Healthy Range |
| --------------- | ------------- |
| Profit Margin   | >10%          |
| Revenue Growth  | >5%           |
| Debt-to-Equity  | <1            |
| Cash Flow Ratio | >10%          |

---

# 8. Assumptions & Limitations

* Based on structured financial data only
* Does not include market sentiment or macro factors
* Risk score is indicative, not predictive
* Industry-specific variations are not fully captured

---
