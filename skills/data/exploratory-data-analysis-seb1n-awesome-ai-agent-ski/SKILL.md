---
name: exploratory-data-analysis
description: Perform systematic exploratory data analysis to understand dataset structure, distributions, relationships, and anomalies before modeling. Use when a dataset is new, its quality is unknown, or the user requests open-ended profiling; use data-analysis instead for a defined hypothesis or decision question.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Exploratory Data Analysis

This skill enables an AI agent to perform structured exploratory data analysis (EDA) on any tabular dataset. The agent systematically profiles the data's shape and types, examines distributions, computes correlations, detects outliers, and produces a summary of findings. EDA is the critical first step before any modeling or reporting — it reveals what the data actually contains versus what it is assumed to contain.

## Workflow

1. **Load and inspect basic structure.** Read the dataset and immediately report its shape (rows, columns), column names, data types, and memory footprint. Display the first 5 and last 5 rows to catch header issues, trailing garbage rows, or encoding artifacts. This takes under a second but prevents hours of downstream confusion.

2. **Assess data quality.** Count nulls per column as both absolute and percentage. Identify columns with zero variance (constant values), high cardinality categoricals (e.g., a "notes" field with unique values per row), and mixed-type columns. Build a concise quality scorecard: columns with >5% missing, columns with suspicious types, and duplicate row counts.

3. **Analyze distributions of individual variables.** For numeric columns, compute mean, median, standard deviation, skewness, and kurtosis. Plot histograms or KDE plots. For categorical columns, show value counts and proportions for the top 10 categories. Flag highly imbalanced distributions (e.g., a binary target where one class is under 5%).

4. **Explore relationships between variables.** Compute the full correlation matrix for numeric columns and visualize it as a heatmap. For categorical-vs-numeric relationships, use grouped box plots or violin plots. For categorical-vs-categorical, use contingency tables or mosaic plots. Highlight pairs with correlation above 0.7 or below -0.7.

5. **Detect outliers and anomalies.** Apply the IQR method to every numeric column and report the count and percentage of outlier values. Visualize outliers with box plots. Cross-reference outliers across columns — a row that is an outlier in multiple columns simultaneously often represents a data entry error or a genuinely unusual observation.

6. **Synthesize findings into an EDA report.** Write a structured summary covering: dataset overview, quality issues found, key distribution characteristics, notable correlations, outlier summary, and recommended next steps (e.g., columns to drop, transformations to apply, features likely to be predictive).

## Supported Technologies

- **pandas** — data loading and profiling
- **matplotlib / seaborn** — distribution and correlation visualizations
- **ydata-profiling** (formerly pandas-profiling) — automated EDA report generation
- **scipy.stats** — statistical tests for distribution analysis

## Usage

Provide the agent with the dataset file path. Optionally specify target columns of interest, maximum categories to display for categorical variables, and whether to generate an automated HTML report. The agent will return both visual outputs and a text summary of findings.

## Examples

### Example 1: Full EDA on a dataset

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("employee_attrition.csv")

# Step 1: Structure
print(f"Shape: {df.shape}")               # Shape: (1470, 35)
print(f"Dtypes:\n{df.dtypes.value_counts()}")
# int64      26
# object      9

# Step 2: Data quality
print(f"\nNull counts:\n{df.isnull().sum().loc[lambda x: x > 0]}")
# monthly_income    12
# years_at_company   8
print(f"Duplicates: {df.duplicated().sum()}")  # Duplicates: 3

# Step 3: Distributions
print(f"\nNumeric summary:\n{df[['age', 'monthly_income', 'years_at_company']].describe()}")
#        age  monthly_income  years_at_company
# mean  36.9         6502.93              7.01
# std    9.1         4707.96              6.13
# min   18.0         1009.00              0.00
# 50%   36.0         4919.00              5.00
# max   60.0        19999.00             40.00

print(f"\nAttrition distribution:\n{df['attrition'].value_counts(normalize=True)}")
# No     0.839
# Yes    0.161    <-- imbalanced target

# Step 4: Correlations
corr = df.select_dtypes(include="number").corr()
high_corr = corr.where(
    (corr.abs() > 0.7) & (corr != 1.0)
).stack().dropna()
print(f"\nHigh correlations:\n{high_corr}")
# monthly_income  job_level           0.95
# total_working_years  job_level      0.78
# years_at_company  years_in_role     0.76

# Step 5: Outlier summary
for col in ["monthly_income", "years_at_company"]:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
    print(f"{col}: {outliers} outliers ({outliers/len(df)*100:.1f}%)")
# monthly_income: 0 outliers (0.0%)
# years_at_company: 47 outliers (3.2%)

# Visualization: correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr, cmap="coolwarm", center=0, annot=False, square=True)
plt.title("Feature Correlation Matrix")
plt.tight_layout()
plt.savefig("eda_correlation_heatmap.png", dpi=150)
```

### Example 2: Automated EDA report generation

```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("employee_attrition.csv")

# Generate a comprehensive HTML report
profile = ProfileReport(
    df,
    title="Employee Attrition EDA Report",
    explorative=True,
    correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "phi_k": {"calculate": True}
    },
    missing_diagrams={
        "bar": True,
        "matrix": True,
        "heatmap": True
    }
)

profile.to_file("eda_report.html")
# Generates a full interactive report including:
# - Dataset overview (size, types, missing cells, duplicates)
# - Per-variable analysis (stats, histogram, common/extreme values)
# - Correlation matrices (Pearson, Spearman, Phi-K)
# - Missing value patterns (bar chart, matrix, nullity heatmap)
# - Sample rows and duplicate detection
print("Report saved to eda_report.html")
```

## Best Practices

- Run EDA before any feature engineering or modeling — assumptions about data quality are almost always wrong until verified.
- Visualize distributions, do not just read summary statistics; a bimodal distribution and a normal distribution can share the same mean and standard deviation.
- Check for data leakage during EDA — if a feature has perfect or near-perfect correlation with the target, it may contain future information.
- Always inspect the tail ends of distributions; the most interesting and problematic data often lives in the extremes.
- Document your EDA findings in a shareable format (HTML report or notebook) so that collaborators can review your reasoning.
- Re-run EDA after major cleaning steps to verify that transformations had the intended effect.

## Edge Cases

- **Datasets with hundreds of columns.** Skip per-column visualizations and focus on automated profiling with ydata-profiling. Use correlation thresholds to surface only the most interesting pairs.
- **Highly imbalanced target variable.** Flag this explicitly (e.g., "Only 2.3% positive class") and recommend stratified sampling or rebalancing techniques for downstream modeling.
- **All-null columns or zero-variance columns.** Drop them automatically during EDA and document them in the findings, as they contribute no analytical value.
- **String columns that are actually numeric.** Detect columns where >90% of values parse as numbers and recommend type coercion before proceeding with statistical analysis.
- **Datetime columns requiring timezone awareness.** Flag timezone-naive datetime columns when the dataset contains records from multiple regions to prevent silent aggregation errors.
