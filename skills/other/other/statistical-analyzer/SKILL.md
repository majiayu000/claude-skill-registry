---
name: statistical-analyzer
description: Perform statistical hypothesis testing, regression analysis, ANOVA, and t-tests with plain-English interpretations and visualizations.
---

# Statistical Analyzer

Guided statistical analysis with hypothesis testing, regression, ANOVA, and plain-English results.

## Features

- **Hypothesis Testing**: t-tests, chi-square, proportion tests
- **Regression Analysis**: Linear, polynomial, multiple regression
- **ANOVA**: One-way, two-way ANOVA with post-hoc tests
- **Distribution Analysis**: Normality tests, Q-Q plots
- **Correlation Analysis**: Pearson, Spearman with significance
- **Plain-English Results**: Interpret statistical outputs
- **Visualizations**: Regression plots, residual analysis, box plots
- **Report Generation**: PDF/HTML reports with interpretations

## Quick Start

```python
from statistical_analyzer import StatisticalAnalyzer

analyzer = StatisticalAnalyzer()

# T-test
analyzer.load_data(df, group_col='treatment', value_col='score')
results = analyzer.t_test(group1='control', group2='experimental')
print(results['interpretation'])

# Regression
analyzer.load_data(df)
results = analyzer.linear_regression(x='age', y='income')
print(f"R²: {results['r_squared']}")
analyzer.plot_regression('regression.png')
```

## CLI Usage

```bash
# T-test
python statistical_analyzer.py --data data.csv --test t-test --group treatment --value score --output results.html

# ANOVA
python statistical_analyzer.py --data data.csv --test anova --group category --value score --output results.pdf

# Regression
python statistical_analyzer.py --data data.csv --test regression --x age --y income --output report.pdf

# Correlation matrix
python statistical_analyzer.py --data data.csv --test correlation --output correlation.png
```

## API Reference

### StatisticalAnalyzer Class

```python
class StatisticalAnalyzer:
    def __init__(self)

    # Data Loading
    def load_data(self, data, **kwargs) -> 'StatisticalAnalyzer'
    def load_csv(self, filepath, **kwargs) -> 'StatisticalAnalyzer'

    # Hypothesis Tests
    def t_test(self, group1, group2, paired=False, alternative='two-sided') -> Dict
    def one_sample_t_test(self, column, expected_mean, alternative='two-sided') -> Dict
    def anova(self, groups, value_col) -> Dict
    def chi_square(self, observed, expected=None) -> Dict
    def proportion_test(self, successes, total, expected_prop=0.5) -> Dict

    # Regression
    def linear_regression(self, x, y) -> Dict
    def polynomial_regression(self, x, y, degree=2) -> Dict
    def multiple_regression(self, predictors: List[str], target: str) -> Dict

    # Correlation
    def correlation(self, method='pearson') -> pd.DataFrame  # Correlation matrix
    def correlation_test(self, var1, var2, method='pearson') -> Dict

    # Distribution Tests
    def normality_test(self, column, method='shapiro') -> Dict
    def qq_plot(self, column, output=None) -> str

    # Visualization
    def plot_regression(self, output, x=None, y=None) -> str
    def plot_residuals(self, output) -> str
    def plot_distribution(self, column, output) -> str
    def plot_boxplot(self, groups, value_col, output) -> str

    # Reporting
    def generate_report(self, output, format='pdf') -> str
    def summary(self) -> str
```

## Tests

### T-Test

Compare means between two groups:

```python
analyzer.load_csv('data.csv')

# Independent samples
results = analyzer.t_test(
    group1='control',
    group2='treatment',
    paired=False
)

# Results
print(results)
# {
#     'statistic': -2.45,
#     'p_value': 0.018,
#     'mean_diff': -5.2,
#     'ci': (-9.5, -0.9),
#     'interpretation': 'The difference is statistically significant (p=0.018)...'
# }

# Paired samples (before/after)
results = analyzer.t_test(
    group1='before',
    group2='after',
    paired=True
)
```

### ANOVA

Compare means across multiple groups:

```python
results = analyzer.anova(
    groups=['control', 'treatment_a', 'treatment_b'],
    value_col='score'
)

# Results include post-hoc tests
print(results['interpretation'])
# "There is a statistically significant difference between groups (p<0.001).
#  Post-hoc tests show treatment_a differs from control (p=0.003)..."
```

### Regression Analysis

```python
# Simple linear regression
results = analyzer.linear_regression(x='hours_studied', y='exam_score')

print(f"R² = {results['r_squared']:.3f}")
print(f"Equation: y = {results['slope']:.2f}x + {results['intercept']:.2f}")
print(f"p-value: {results['p_value']:.4f}")

# Polynomial regression
results = analyzer.polynomial_regression(x='age', y='salary', degree=2)

# Multiple regression
results = analyzer.multiple_regression(
    predictors=['age', 'experience', 'education'],
    target='salary'
)
```

### Correlation Analysis

```python
# Full correlation matrix
corr_matrix = analyzer.correlation(method='pearson')
print(corr_matrix)

# Test specific correlation
results = analyzer.correlation_test('height', 'weight', method='pearson')
print(results['interpretation'])
# "There is a strong positive correlation (r=0.82, p<0.001)"
```

### Distribution Tests

```python
# Test normality
results = analyzer.normality_test('scores', method='shapiro')
# Returns: {'statistic': 0.98, 'p_value': 0.35,
#           'interpretation': 'Data appears normally distributed (p=0.35)'}

# Q-Q plot
analyzer.qq_plot('scores', output='qq_plot.png')
```

## Interpretation Guide

The analyzer provides plain-English interpretations:

### Significance Levels
- **p < 0.001**: "Highly significant"
- **p < 0.01**: "Very significant"
- **p < 0.05**: "Statistically significant"
- **p ≥ 0.05**: "Not statistically significant"

### Effect Sizes
- **Cohen's d**: Small (0.2), Medium (0.5), Large (0.8)
- **R²**: Weak (<0.3), Moderate (0.3-0.7), Strong (>0.7)
- **Correlation**: Weak (<0.3), Moderate (0.3-0.7), Strong (>0.7)

## Visualizations

### Regression Plot
```python
analyzer.linear_regression(x='age', y='income')
analyzer.plot_regression('regression.png')
# Creates scatter plot with regression line and confidence interval
```

### Residual Plot
```python
analyzer.plot_residuals('residuals.png')
# Checks regression assumptions (homoscedasticity)
```

### Box Plot
```python
analyzer.plot_boxplot(
    groups=['control', 'treatment_a', 'treatment_b'],
    value_col='score',
    output='boxplot.png'
)
```

### Distribution Plot
```python
analyzer.plot_distribution('scores', 'distribution.png')
# Histogram with normal curve overlay
```

## Reports

Generate comprehensive reports:

```python
analyzer.load_csv('data.csv')
analyzer.t_test(group1='control', group2='treatment')
analyzer.linear_regression(x='hours', y='score')

# PDF report with all analyses
analyzer.generate_report('analysis_report.pdf', format='pdf')

# HTML report
analyzer.generate_report('analysis_report.html', format='html')
```

Reports include:
- Summary statistics
- Test results with interpretations
- Visualizations
- Assumptions checks
- Recommendations

## Assumptions Checking

Automatic assumptions validation:

```python
# T-test checks:
# - Normality (Shapiro-Wilk)
# - Equal variances (Levene's test)
# Warnings if assumptions violated

# ANOVA checks:
# - Normality per group
# - Homogeneity of variances
# Suggests non-parametric alternatives

# Regression checks:
# - Linearity
# - Homoscedasticity
# - Normality of residuals
# - Independence (Durbin-Watson)
```

## Dependencies

- scipy>=1.10.0
- statsmodels>=0.14.0
- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
- reportlab>=4.0.0
