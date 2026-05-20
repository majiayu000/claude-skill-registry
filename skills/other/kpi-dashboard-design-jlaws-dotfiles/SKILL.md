---
name: kpi-dashboard-design
description: Design effective KPI dashboards with metrics selection, visualization best practices, and real-time monitoring patterns. Use when building business dashboards, selecting metrics, or designing data visualization layouts.
---

# KPI Dashboard Design

## KPI Framework

| Level | Focus | Update Frequency | Audience |
|-------|-------|------------------|----------|
| **Strategic** | Long-term goals | Monthly/Quarterly | Executives |
| **Tactical** | Department goals | Weekly/Monthly | Managers |
| **Operational** | Day-to-day | Real-time/Daily | Teams |

## Dashboard Hierarchy

```
Executive Summary (1 page): 4-6 headline KPIs, trend indicators, key alerts
Department Views: Sales, Marketing, Operations, Finance dashboards
Detailed Drilldowns: Individual metrics, root cause analysis
```

## Common KPIs by Department

```yaml
Sales:
  Revenue: MRR, ARR, ARPU, Revenue Growth Rate
  Pipeline: Pipeline Value, Win Rate, Deal Size, Sales Cycle Length

Marketing:
  Acquisition: CPA, CAC, Lead Volume, MQLs
  ROI: Marketing ROI, Channel Attribution, CAC Payback Period

Product:
  Usage: DAU/MAU, Session Duration, Feature Adoption, Stickiness
  Quality: NPS, CSAT, Bug Count, Time to Resolution
  Growth: User Growth Rate, Activation Rate, Retention Rate, Churn Rate

Finance:
  Profitability: Gross Margin, Net Profit Margin, EBITDA
  Liquidity: Current Ratio, Cash Flow, Working Capital
  Efficiency: Revenue per Employee, Operating Expense Ratio
```

## Layout: SaaS Metrics Dashboard

```
┌──────────────────────┬──────────────────────────────────────┐
│  MRR: $125,000 ▲8%   │  MRR GROWTH TREND                    │
│  ARR: $1,500,000 ▲15% │  [line chart]                        │
├──────────────────────┼──────────────────────────────────────┤
│  UNIT ECONOMICS      │  COHORT RETENTION                    │
│  CAC: $450           │  M1: 85% | M3: 80% | M6: 72%       │
│  LTV: $2,700         │                                      │
│  LTV/CAC: 6.0x       │                                      │
│  Payback: 4 months   │                                      │
├──────────────────────┴──────────────────────────────────────┤
│  CHURN: Gross 4.2% | Net 1.8% | Logo 3.1% | Expansion 2.4% │
└─────────────────────────────────────────────────────────────┘
```

## SQL: Key Calculations

```sql
-- Monthly Recurring Revenue (MRR)
WITH mrr_calculation AS (
    SELECT DATE_TRUNC('month', billing_date) AS month,
        SUM(CASE subscription_interval
            WHEN 'monthly' THEN amount
            WHEN 'yearly' THEN amount / 12
            WHEN 'quarterly' THEN amount / 3
        END) AS mrr
    FROM subscriptions WHERE status = 'active'
    GROUP BY DATE_TRUNC('month', billing_date)
)
SELECT month, mrr,
    LAG(mrr) OVER (ORDER BY month) AS prev_mrr,
    (mrr - LAG(mrr) OVER (ORDER BY month)) / LAG(mrr) OVER (ORDER BY month) * 100 AS growth_pct
FROM mrr_calculation;

-- Cohort Retention
WITH cohorts AS (
    SELECT user_id, DATE_TRUNC('month', created_at) AS cohort_month FROM users
),
activity AS (
    SELECT user_id, DATE_TRUNC('month', event_date) AS activity_month
    FROM user_events WHERE event_type = 'active_session'
)
SELECT c.cohort_month,
    EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month)) AS months_since_signup,
    COUNT(DISTINCT a.user_id)::FLOAT / COUNT(DISTINCT c.user_id) * 100 AS retention_rate
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id AND a.activity_month >= c.cohort_month
GROUP BY c.cohort_month, EXTRACT(MONTH FROM age(a.activity_month, c.cohort_month));
```

## Python Dashboard (Streamlit)

```python
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="KPI Dashboard", layout="wide")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Revenue", "$2.4M", "▲ 12.5%")
with col2: st.metric("Customers", "12,450", "▲ 15.2%")
with col3: st.metric("NPS Score", "72", "▲ 5.0")
with col4: st.metric("Churn Rate", "4.2%", "▼ 0.8%")

# Charts
col1, col2 = st.columns(2)
with col1:
    fig = px.line(revenue_data, x='Month', y='Revenue', line_shape='spline', markers=True)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.pie(product_data, values='Revenue', names='Product', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Cohort Heatmap
import plotly.graph_objects as go
fig = go.Figure(data=go.Heatmap(
    z=cohort_data.iloc[:, 1:].values, x=['M0','M1','M2','M3','M4'],
    y=cohort_data['Cohort'], colorscale='Blues',
    text=cohort_data.iloc[:, 1:].values, texttemplate='%{text}%',
))
st.plotly_chart(fig, use_container_width=True)
```
