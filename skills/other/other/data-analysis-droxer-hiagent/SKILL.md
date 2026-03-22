---
name: data-analysis
description: Structured data analysis with statistical rigor, automated EDA, and publication-quality visualizations. Use when the user asks to analyze data, analyze a dataset, create charts, visualize data, compute statistics, or work with CSV and spreadsheet files.
license: MIT
sandbox-template: data_science
allowed-tools: code_run code_interpret file_read file_write file_list file_edit user_message
---

# Data Analysis Methodology

Prioritize correctness over speed — a wrong insight is worse than no insight.

## Step 1: Data Ingestion

Uploaded files are located at `/home/user/uploads/`. Always list that directory first to discover available files:

```python
import os
for f in os.listdir('/home/user/uploads/'):
    print(f)
```

**Tool selection:** Use `code_run` as the primary execution tool — it is universally supported across all sandbox providers. Use `code_interpret` only when you need rich output capture (e.g., inline dataframes, rendered plots); note that `code_interpret` may not be available in all environments.

Examine the raw file (first 20-30 lines) to understand format, delimiter, encoding, headers, and obvious quality issues before loading.

Load by file type — always specify dtypes for known columns and parse_dates for date columns:

| Extension | Loader |
|---|---|
| `.csv` | `pd.read_csv('/home/user/uploads/file.csv', parse_dates=[...])` |
| `.tsv` | `pd.read_csv('/home/user/uploads/file.tsv', sep='\t', parse_dates=[...])` |
| `.xlsx` / `.xls` | `pd.read_excel('/home/user/uploads/file.xlsx', engine='openpyxl')` |
| `.json` | `pd.read_json('/home/user/uploads/file.json')` |
| `.parquet` | `pd.read_parquet('/home/user/uploads/file.parquet')` |

## Step 2: Mandatory EDA

Run this diagnostic block on every dataset before any analysis:

```python
print(f"Shape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"\nNumeric summary:\n{df.describe()}")

for col in df.select_dtypes(include='object').columns:
    n_unique = df[col].nunique()
    print(f"\n{col}: {n_unique} unique values")
    if n_unique <= 20:
        print(df[col].value_counts())
```

**Do not skip this step.** Report findings before proceeding to analysis.

After completing EDA, send a progress update via `user_message` summarizing the dataset shape, quality issues found, and your planned analysis approach.

## Step 3: Data Cleaning Decision Framework

- **Missing values**: Report percentage. Drop rows only if <5% missing. Otherwise, impute (median for skewed numeric, mode for categorical) and flag it.
- **Duplicates**: Drop exact duplicates. For near-duplicates, ask the user.
- **Outliers**: Detect with IQR method (1.5×IQR). Report them but do NOT remove unless the user asks — outliers can be real data.
- **Type coercion**: Convert string numbers to numeric, parse dates, encode categoricals.

## Step 4: Analysis Technique Selection

Match technique to the question type:

| Question Type | Technique |
|---|---|
| "How much / how many" | Aggregation (groupby + sum/mean/count) |
| "Is there a relationship" | Correlation (Pearson for linear, Spearman for monotonic) |
| "Is there a difference" | Statistical test (t-test for 2 groups, ANOVA for 3+) |
| "What predicts X" | Regression (linear for continuous, logistic for binary) |
| "How has X changed" | Time series (resample, rolling average, trend decomposition) |
| "What are the groups" | Clustering (k-means) or segmentation (quantile splits) |

**Always report effect sizes and confidence intervals, not just p-values.**

After selecting your analysis technique, send a progress update via `user_message` describing which technique you chose and why, before running the full analysis.

## Step 5: Visualization Selection

Choose chart types by data shape:

| Data | Chart |
|---|---|
| Distribution of one numeric variable | Histogram or KDE plot |
| Comparison across categories | Bar chart (horizontal if >5 categories) |
| Relationship between two numeric variables | Scatter plot |
| Trend over time | Line chart |
| Part-of-whole | Stacked bar (NOT pie chart) |
| Correlation matrix | Heatmap |

Sandbox-specific rules:
- Use `matplotlib.use('Agg')` — there is no display
- Always call `plt.close()` after saving to free memory
- Save plots to `/home/user/output/` at 150 dpi — create the directory first: `os.makedirs('/home/user/output/', exist_ok=True)`
- When using `code_run`, pass saved file paths via the `output_files` parameter so artifacts are tracked. When using `code_interpret`, rich outputs (plots, dataframes) are auto-captured — but for file-based outputs (saved PNGs), prefer `code_run` with `output_files`
- Use colorblind-friendly palettes (`tab10`, `Set2`)

## Step 6: Report Structure

```
**Dataset Overview**: [rows × columns, date range if applicable]

**Key Findings**:
1. [Quantified finding — "Revenue increased 23% QoQ"]
2. [Finding with statistical backing — "Correlation r=0.82, p<0.001"]

**Data Quality Notes**: [Cleaning applied, missing data, caveats]

**Methodology**: [Tests/techniques used and why]
```

**Never say "X causes Y" from observational data alone.**
