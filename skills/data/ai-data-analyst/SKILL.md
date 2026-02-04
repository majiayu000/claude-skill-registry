---
name: ai-data-analyst
description: Perform comprehensive data analysis, statistical modeling, and data visualization by writing and executing self-contained Python scripts. Use when you need to analyze datasets, perform statistical tests, create visualizations, or build predictive models with reproducible, code-based workflows.
---

# Skill: AI data analyst

## Purpose

Perform comprehensive data analysis, statistical modeling, and data visualization by writing and executing self-contained Python scripts. Generate publication-quality charts, statistical reports, and actionable insights from data files or databases.

## When to use this skill

- You need to **analyze datasets** to understand patterns, trends, or relationships.
- You want to perform **statistical tests** or build predictive models.
- You need **data visualizations** (charts, graphs, dashboards) to communicate findings.
- You're doing **exploratory data analysis** (EDA) to understand data structure and quality.
- You need to **clean, transform, or merge** datasets for analysis.
- You want **reproducible analysis** with documented methodology and code.
- You are performing **Convex Backend Engineering** (schema design, query optimization, log analysis).

## Key capabilities

Unlike point-solution data analysis tools:

- **Convex Engineering Integration**: Native support for Convex MCP tools (`mcp_convex`) and CLI.
- **Full Python ecosystem**: Access to pandas, numpy, scikit-learn, statsmodels, matplotlib, seaborn, plotly, and more.
- **Runs locally**: Your data stays on your machine; no uploads to third-party services.
- **Reproducible**: All analysis is code-based and version controllable.
- **Customizable**: Extend with any Python library or custom analysis logic.
- **Publication-quality output**: Generate professional charts and reports.
- **Statistical rigor**: Access to comprehensive statistical and ML libraries.

## Inputs

- **Data sources**: CSV files, Excel files, JSON, Parquet, or database connections.
- **Analysis goals**: Questions to answer or hypotheses to test.
- **Variables of interest**: Specific columns, metrics, or dimensions to focus on.
- **Output preferences**: Chart types, report format, statistical tests needed.
- **Context**: Business domain, data dictionary, or known data quality issues.

## Out of scope

- Real-time streaming data analysis (use appropriate streaming tools).
- Extremely large datasets requiring distributed computing (use Spark/Dask instead).
- Production ML model deployment (use ML ops tools and infrastructure).
- Live dashboarding (use BI tools like Tableau/Looker for operational dashboards).

## Conventions and best practices

### Python environment

- Use **virtual environments** to isolate dependencies.
- Install only necessary packages for the specific analysis.
- Document all dependencies in `requirements.txt` or `environment.yml`.

### Code structure

- Write **self-contained scripts** that can be re-run by others.
- Use **clear variable names** and add comments for complex logic.
- **Separate concerns**: data loading, cleaning, analysis, visualization.
- Save **intermediate results** to files when analysis is multi-stage.

### Data handling

- **Never modify source data files** – work on copies or in-memory dataframes.
- **Document data transformations** clearly in code comments.
- **Handle missing values** explicitly and document approach.
- **Validate data quality** before analysis (check for nulls, outliers, duplicates).

### Visualization best practices

- Choose **appropriate chart types** for the data and question.
- Use **clear labels, titles, and legends** on all charts.
- Apply **appropriate color schemes** (colorblind-friendly when possible).
- Include **sample sizes and confidence intervals** where relevant.
- Save visualizations in **high-resolution formats** (PNG 300 DPI, SVG for vector graphics).

### Statistical analysis

- **State assumptions** for statistical tests clearly.
- **Check assumptions** before applying tests (normality, homoscedasticity, etc.).
- **Report effect sizes** not just p-values.
- **Use appropriate corrections** for multiple comparisons.
- **Explain practical significance** in addition to statistical significance.

## Required behavior

1. **Understand the question**: Clarify what insights or decisions the analysis should support.
2. **Explore the data**: Check structure, types, missing values, distributions, outliers.
3. **Clean and prepare**: Handle missing data, outliers, and transformations appropriately.
4. **Analyze systematically**: Apply appropriate statistical methods or ML techniques.
5. **Visualize effectively**: Create clear, informative charts that answer the question.
6. **Generate insights**: Translate statistical findings into actionable business insights.
7. **Document thoroughly**: Explain methodology, assumptions, limitations, and conclusions.
8. **Make reproducible**: Ensure others can re-run the analysis and get the same results.

## Required artifacts

- **Analysis script(s)**: Well-documented Python code performing the analysis.
- **Visualizations**: Charts saved as high-quality image files (PNG/SVG).
- **Analysis report**: Markdown or text document summarizing:
  - Research question and methodology
  - Data description and quality assessment
  - Key findings with supporting statistics
  - Visualizations with interpretations
  - Limitations and caveats
  - Recommendations or next steps
- **Requirements file**: `requirements.txt` with all dependencies.
- **Sample data** (if appropriate and non-sensitive): Small sample for reproducibility.

## Implementation checklist

### 1. Data exploration and preparation

- [ ] Load data and inspect structure (shape, columns, types)
- [ ] Check for missing values, duplicates, outliers
- [ ] Generate summary statistics (mean, median, std, min, max)
- [ ] Visualize distributions of key variables
- [ ] Document data quality issues found

### 2. Data cleaning and transformation

- [ ] Handle missing values (impute, drop, or flag)
- [ ] Address outliers if needed (cap, transform, or document)
- [ ] Create derived variables if needed
- [ ] Normalize or scale variables for modeling
- [ ] Split data if doing train/test analysis

### 3. Analysis execution

- [ ] Choose appropriate analytical methods
- [ ] Check statistical assumptions
- [ ] Execute analysis with proper parameters
- [ ] Calculate confidence intervals and effect sizes
- [ ] Perform sensitivity analyses if appropriate

### 4. Visualization

- [ ] Create exploratory visualizations
- [ ] Generate publication-quality final charts
- [ ] Ensure all charts have clear labels and titles
- [ ] Use appropriate color schemes and styling
- [ ] Save in high-resolution formats

### 5. Reporting

- [ ] Write clear summary of methods used
- [ ] Present key findings with supporting evidence
- [ ] Explain practical significance of results
- [ ] Document limitations and assumptions
- [ ] Provide actionable recommendations

### 6. Reproducibility

- [ ] Test that script runs from clean environment
- [ ] Document all dependencies
- [ ] Add comments explaining non-obvious code
- [ ] Include instructions for running analysis

## Convex Engineering Workflow

When working with Convex (backend, database, schemas), you **MUST** follow this specialized workflow:

### 1. Protocols & Rules

- **READ FIRST**: Always read `resources/convex_rules.md` before writing any Convex code.
  - Command: `view_file(AbsolutePath=".../resources/convex_rules.md")`
- **MCP Integration**: Use `mcp_convex` tools to inspect CURRENT state before proposing changes.
  - `mcp_convex_tables`: Check table schemas.
  - `mcp_convex_functionSpec`: Check existing functions.
  - `mcp_convex_logs`: Analyze recent failures.

### 2. Implementation & fix

- **CLI First**: Use `bunx convex` for all operations.
  - DO NOT use generic SQL or other DB commands.
  - Example: `bunx convex run serena/actions:doSomething`
- **Log Analysis**:
  - When debugging, pull logs via `bunx convex logs --prod --failure` OR `mcp_convex_logs`.
  - Analyze stack traces using Python scripts if text analysis is insufficient.

### 3. Code Generation

- **Schema**: Define in `convex/schema.ts` using `defineSchema` and `defineTable`.
- **Functions**: Use `query`, `mutation`, `action` from `_generated/server`.
- **Validation**: Ensure `args` and `returns` validators (e.g., `v.string()`, `v.id()`) are strictly typed.

## Verification

Run the following to verify the analysis:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run analysis script
python analysis.py

# Check outputs generated
ls -lh outputs/
```

The skill is complete when:

- Analysis script runs without errors from clean environment.
- All required visualizations are generated in high quality.
- Report clearly explains methodology, findings, and limitations.
- Results are interpretable and actionable.
- Code is well-documented and reproducible.

## Common analysis patterns

### Exploratory Data Analysis (EDA)

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and inspect data
df = pd.read_csv('data.csv')
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Visualize distributions
df.hist(figsize=(12, 10), bins=30)
plt.tight_layout()
plt.savefig('distributions.png', dpi=300)

# Check correlations
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.savefig('correlations.png', dpi=300)
```

### Time series analysis

```python
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load time series data
df = pd.read_csv('timeseries.csv', parse_dates=['date'])
df.set_index('date', inplace=True)

# Decompose time series
decomposition = seasonal_decompose(df['value'], model='additive', period=30)
fig = decomposition.plot()
fig.set_size_inches(12, 8)
plt.savefig('decomposition.png', dpi=300)

# Calculate rolling statistics
df['rolling_mean'] = df['value'].rolling(window=7).mean()
df['rolling_std'] = df['value'].rolling(window=7).std()

# Plot with trends
plt.figure(figsize=(12, 6))
plt.plot(df['value'], label='Original')
plt.plot(df['rolling_mean'], label='7-day Moving Avg', linewidth=2)
plt.fill_between(df.index,
                 df['rolling_mean'] - df['rolling_std'],
                 df['rolling_mean'] + df['rolling_std'],
                 alpha=0.3)
plt.legend()
plt.savefig('trends.png', dpi=300)
```

### Statistical hypothesis testing

```python
from scipy import stats
import numpy as np

# Compare two groups
group_a = df[df['group'] == 'A']['metric']
group_b = df[df['group'] == 'B']['metric']

# Check normality
_, p_norm_a = stats.shapiro(group_a)
_, p_norm_b = stats.shapiro(group_b)

# Choose appropriate test
if p_norm_a > 0.05 and p_norm_b > 0.05:
    # Parametric test (t-test)
    statistic, p_value = stats.ttest_ind(group_a, group_b)
    test_used = "Independent t-test"
else:
    # Non-parametric test (Mann-Whitney U)
    statistic, p_value = stats.mannwhitneyu(group_a, group_b)
    test_used = "Mann-Whitney U test"

# Calculate effect size (Cohen's d)
pooled_std = np.sqrt((group_a.std()**2 + group_b.std()**2) / 2)
cohens_d = (group_a.mean() - group_b.mean()) / pooled_std

print(f"Test used: {test_used}")
print(f"Test statistic: {statistic:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Effect size (Cohen's d): {cohens_d:.4f}")
```

### Predictive modeling

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Prepare data
X = df.drop('target', axis=1)
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

# Feature importance
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(importance['feature'][:10], importance['importance'][:10])
plt.xlabel('Feature Importance')
plt.title('Top 10 Most Important Features')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300)
```

## Recommended Python libraries

### Data manipulation

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **polars**: High-performance DataFrame library (alternative to pandas)

### Visualization

- **matplotlib**: Foundational plotting library
- **seaborn**: Statistical visualizations
- **plotly**: Interactive charts
- **altair**: Declarative statistical visualization

### Statistical analysis

- **scipy.stats**: Statistical functions and tests
- **statsmodels**: Statistical modeling
- **pingouin**: Statistical tests with clear output

### Machine learning

- **scikit-learn**: ML algorithms and tools
- **xgboost**: Gradient boosting
- **lightgbm**: Fast gradient boosting

### Time series

- **statsmodels.tsa**: Time series analysis
- **prophet**: Forecasting tool
- **pmdarima**: Auto ARIMA

### Specialized

- **networkx**: Network analysis
- **geopandas**: Geospatial data analysis
- **textblob** / **spacy**: Natural language processing

## Safety and escalation

- **Data privacy**: Never analyze or share data containing PII without proper authorization.
- **Statistical validity**: If sample sizes are too small for reliable inference, call this out explicitly.
- **Causal claims**: Avoid implying causation from correlational analysis; be explicit about limitations.
- **Model limitations**: Document when models may not generalize or when predictions should not be trusted.
- **Data quality**: If data quality issues could materially affect conclusions, flag this prominently.

## Integration with other skills

This skill can be combined with:

- **Internal data querying**: To fetch data from warehouses or databases for analysis.
- **Web app builder**: To create interactive dashboards displaying analysis results.
- **Internal tools**: To build analysis tools for non-technical stakeholders.
