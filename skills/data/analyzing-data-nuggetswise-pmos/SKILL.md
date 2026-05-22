---
name: analyzing-data
description: Use when you have CSV/Excel data files and need PM insights (retention, funnel, segmentation) via Python analysis.
---

# Analyzing Data

## Overview

A protocol for Python-based data analysis that prevents hallucination by requiring explicit column understanding, separating metrics from implications, and labeling all hypotheses.

## When to Use

- User provides CSV, Excel, or structured data files
- User asks for "analysis", "insights", "metrics", "trends", or "charts"
- Data exists in `data/` or `inputs/` folder
- User wants to understand product performance

## Core Pattern

**Step 1: Exploratory Data Analysis (EDA)**

Write and execute a Python script to produce:

```python
import pandas as pd

# Load data
df = pd.read_csv('inputs/data/filename.csv')  # or pd.read_excel()

# Basic info
print("=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS & TYPES ===")
print(df.dtypes)

print("\n=== FIRST 5 ROWS ===")
print(df.head())

print("\n=== SUMMARY STATS ===")
print(df.describe(include='all'))

print("\n=== MISSING DATA ===")
print(df.isnull().sum() / len(df) * 100)
```

**Step 2: Data Dictionary**

Create a data dictionary table:

| Column | Type | Example Values | Meaning |
|--------|------|----------------|---------|
| [col] | [dtype] | [2-3 examples] | [Explicit/Unknown] |

**Rules:**
- Mark meaning as "Unknown" if not explicitly documented
- Do NOT infer column meanings from names alone
- Ask user to clarify unknown columns before proceeding

**Step 3: Analysis Plan**

Only propose analyses where:
- Required columns have known meanings
- User has confirmed the business context
- The analysis directly answers user's question

**Step 4: Execution & Visualization**

```python
import matplotlib.pyplot as plt

# Example: Time series
df['date'] = pd.to_datetime(df['date_column'])
daily = df.groupby('date').size()
daily.plot(figsize=(10,5), title='Daily Counts')
plt.savefig('outputs/insights/analysis_output.png')
print("Chart saved to outputs/insights/analysis_output.png")
```

**Step 5: Generate Output**

Write to `outputs/insights/data-analysis-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: analyzing-data
sources:
  - inputs/data/filename.csv (modified: YYYY-MM-DD)
downstream: []
---

# Data Analysis: [Dataset Name]

## Dataset Overview
| Attribute | Value |
|-----------|-------|
| Rows | N |
| Columns | N |
| Date range | [if applicable] |

## Data Dictionary
| Column | Type | Example Values | Meaning |
|--------|------|----------------|---------|
| ... | ... | ... | Explicit/Unknown |

## Key Metrics
| Metric | Value | Source |
|--------|-------|--------|
| [Metric name] | [Number] | [Code output] |

## Findings
1. **[Finding]** — Evidence: [code output]

## Hypotheses (require validation)
1. **[Hypothesis]** — Based on: [observation]

## Visualizations
- [Chart description]: outputs/insights/[filename].png

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Metric] | Evidence | [Python output] |
| [Trend interpretation] | Hypothesis | [Based on metric X] |
```

**Step 6: Copy to History & Update Tracker**

- Copy to `history/analyzing-data/data-analysis-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Action | Command |
|--------|---------|
| Load CSV | `pd.read_csv('inputs/data/file.csv')` |
| Load Excel | `pd.read_excel('inputs/data/file.xlsx')` |
| Save chart | `plt.savefig('outputs/insights/output.png')` |
| Check nulls | `df.isnull().sum()` |

## Common Mistakes

- **Assuming column meanings:** "user_id probably means..." → Ask user to confirm
- **Stating implications as facts:** "Users are churning because..." → Label as hypothesis
- **Using sample data for conclusions:** "Based on 10 rows..." → Ensure representative data
- **Ignoring missing data:** 50% nulls in key column → Report this prominently
- **No data dictionary:** Jumping to analysis → Always document columns first

## Verification Checklist

- [ ] Data dictionary created with all columns
- [ ] Unknown meanings explicitly marked
- [ ] User confirmed column semantics before analysis
- [ ] Metrics separated from hypotheses
- [ ] Missing data reported
- [ ] Charts saved to outputs/insights/
- [ ] All code executed successfully
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Metric] | Evidence | [Python output] |
| [Trend interpretation] | Hypothesis | [Based on metric X] |
| [Column meaning] | Evidence/Unknown | [User confirmed / Not stated] |
