---
name: pipeline-forecasting
description: Forecast categories, weighted pipeline calculations, deal scoring models, and forecast accuracy metrics.
allowed-tools: []
---

# Pipeline Forecasting

B2B sales forecasting frameworks and deal scoring models.

## Forecast Categories

| Category | Definition | Weight |
|----------|------------|--------|
| **Commit** | Will close this period | 90% |
| **Best Case** | High probability, some risk | 70% |
| **Pipeline** | Working, outcome uncertain | 30% |
| **Upside** | Long shot, possible | 10% |

## Weighted Pipeline

```
Weighted Pipeline = Σ (Deal Value × Stage Probability × Confidence)

Example:
$100K deal in Proposal (40%) with High confidence (1.1x)
= $100K × 0.4 × 1.1 = $44K weighted
```

## Forecast Accuracy Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Forecast Accuracy | Actual / Forecast | 90-110% |
| Commit Accuracy | Commit Closed / Commit Forecast | >85% |
| Best Case Accuracy | BC Closed / BC Forecast | >60% |
| Pipeline Accuracy | Pipeline Closed / Pipeline Forecast | >25% |

## Weekly Forecast Review Template

```
FORECAST REVIEW: [Date]

Commit: $[X] ([Y] deals)
- [Deal 1]: $X - [Status/Risk]
- [Deal 2]: $X - [Status/Risk]

Best Case: $[X] ([Y] deals)
- [Deal 1]: $X - [What needs to happen]

Pipeline: $[X] ([Y] deals)
- At risk: [List]
- Upside: [List]

Total Weighted: $[X]
vs. Target: $[X]
Gap: $[X]

Actions This Week:
1. [Specific action on deal]
2. [Specific action on deal]
```

## Deal Scoring Model

### Score Components

| Factor | Weight | Scoring |
|--------|--------|---------|
| **ICP Fit** | 20% | 3=Perfect, 2=Good, 1=Marginal, 0=Off |
| **Champion** | 25% | 3=Active, 2=Supportive, 1=Identified, 0=None |
| **Authority** | 20% | 3=Buyer engaged, 2=Identified, 1=Unknown, 0=Blocked |
| **Need** | 15% | 3=Urgent, 2=Important, 1=Nice-to-have, 0=None |
| **Timeline** | 10% | 3=This quarter, 2=Next quarter, 1=This year, 0=None |
| **Competition** | 10% | 3=None/weak, 2=Incumbent, 1=Strong, 0=Losing |

### Score Interpretation

- **85-100%**: High confidence commit
- **70-84%**: Best case
- **50-69%**: Standard pipeline
- **<50%**: At risk, qualify harder
