---
name: data-analysis
description: Analyze datasets to answer defined questions through statistical methods, trend identification, hypothesis testing, and correlation analysis. Use when the user needs evidence-backed findings or decisions from data; use exploratory-data-analysis instead for open-ended first-pass profiling before questions are defined.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Data Analysis

This skill enables an AI agent to perform rigorous statistical analysis on structured datasets. The agent loads data, computes descriptive and inferential statistics, identifies trends and correlations, tests hypotheses, and produces actionable insights. It supports CSV, Excel, Parquet, and JSON inputs and leverages pandas, scipy, and statsmodels for analysis.

## Workflow

1. **Load and profile the data.** Read the dataset into a pandas DataFrame and inspect its shape, column types, and memory usage. Display the first and last rows to confirm the data loaded correctly. Check for obvious structural issues such as shifted columns or encoding problems.

2. **Compute descriptive statistics.** Generate summary statistics for all numeric columns including mean, median, standard deviation, skewness, and kurtosis. For categorical columns, compute value counts and mode. This step establishes a baseline understanding of each variable's distribution.

3. **Identify trends and patterns.** Apply rolling averages, percentage changes, and seasonal decomposition to time-indexed data. For non-temporal data, use group-by aggregations and pivot tables to surface patterns across categories. Flag any monotonic trends or cyclical behavior.

4. **Perform correlation and hypothesis testing.** Calculate Pearson and Spearman correlation matrices to quantify relationships between variables. Conduct hypothesis tests (t-tests, chi-square, ANOVA) where appropriate to determine statistical significance. Report p-values and confidence intervals alongside effect sizes.

5. **Detect anomalies and outliers.** Use the IQR method and z-scores to identify data points that deviate significantly from the norm. Cross-reference outliers with domain context to determine whether they represent errors, rare events, or meaningful signals.

6. **Synthesize findings into a report.** Summarize the key insights in plain language, supported by specific numbers. Rank findings by business impact or statistical significance. Include limitations and caveats such as sample size constraints or confounding variables.

## Supported Technologies

- **pandas** — data loading, manipulation, and aggregation
- **scipy.stats** — hypothesis testing, statistical distributions
- **statsmodels** — time-series decomposition, regression analysis
- **numpy** — numerical computations

## Usage

Provide the agent with a file path to the dataset and a description of the analysis goals. Optionally specify which columns to focus on, the significance level for hypothesis tests (default alpha=0.05), and whether time-series methods should be applied.

## Examples

### Example 1: Sales CSV analysis with pandas

```python
import pandas as pd
from scipy import stats

# Load the dataset
df = pd.read_csv("sales_2024.csv", parse_dates=["order_date"])

# Descriptive statistics
print(df[["revenue", "units_sold", "discount"]].describe())
#          revenue  units_sold  discount
# count   8450.00     8450.00   8450.00
# mean     312.45       4.12      0.08
# std      189.73       2.87      0.05
# min       12.00       1.00      0.00
# max     2450.00      47.00      0.35

# Correlation analysis
corr = df[["revenue", "units_sold", "discount"]].corr(method="pearson")
print(corr)
#             revenue  units_sold  discount
# revenue       1.000       0.847    -0.213
# units_sold    0.847       1.000    -0.089
# discount     -0.213      -0.089     1.000

# Hypothesis test: do discounted orders produce higher revenue?
discounted = df[df["discount"] > 0]["revenue"]
full_price = df[df["discount"] == 0]["revenue"]
t_stat, p_value = stats.ttest_ind(discounted, full_price)
print(f"t={t_stat:.3f}, p={p_value:.4f}")
# t=-3.217, p=0.0013 — discounted orders have significantly lower revenue per order
```

### Example 2: Time-series analysis with seasonal decomposition

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# Load monthly revenue data
df = pd.read_csv("monthly_revenue.csv", parse_dates=["month"], index_col="month")

# Decompose into trend, seasonal, and residual components
result = seasonal_decompose(df["revenue"], model="additive", period=12)

print("Trend (last 6 months):")
print(result.trend.dropna().tail(6))
# 2024-07    48230.12
# 2024-08    49012.45
# 2024-09    49780.33
# 2024-10    50234.10
# 2024-11    51002.88
# 2024-12    51890.67

print("\nSeasonal peaks:")
seasonal = result.seasonal.groupby(result.seasonal.index.month).mean()
print(seasonal.nlargest(3))
# month
# 11    8923.40   (November — holiday pre-orders)
# 12    7654.20   (December — holiday sales)
# 3     3210.15   (March — spring promotions)

# The upward trend of ~$600/month suggests 14.5% annualized growth.
# Strong Q4 seasonality accounts for roughly 18% of total annual revenue.
```

## Best Practices

- Always inspect raw data before computing statistics — silent parsing errors (wrong delimiters, encoding issues) can invalidate every downstream result.
- Report effect sizes alongside p-values; statistical significance alone does not imply practical importance.
- Use non-parametric tests (Mann-Whitney, Kruskal-Wallis) when data distributions are heavily skewed or sample sizes are small.
- Segment analysis by meaningful categories (region, product line, customer tier) to avoid Simpson's paradox.
- Document assumptions explicitly — stationarity for time-series, normality for parametric tests, independence of observations.
- Validate surprising findings with a holdout sample or alternative methodology before presenting them as conclusions.

## Edge Cases

- **Missing values in key columns.** If more than 30% of a target column is null, warn the user that imputation may introduce significant bias. Offer to analyze the complete-case subset instead.
- **Extremely skewed distributions.** Log-transform or use median-based statistics when skewness exceeds |2.0| to avoid misleading mean values.
- **Multicollinearity.** When two predictors correlate above 0.9, flag this and recommend dropping one or using regularized models to avoid inflated coefficients.
- **Small sample sizes (n < 30).** Switch to exact tests or bootstrap methods and widen confidence intervals accordingly.
- **Mixed data types in a single column.** Coerce carefully and report how many values could not be converted, rather than silently dropping them.
