---
name: correlation-explorer
description: Find and visualize correlations between variables in datasets. Use for data exploration, feature selection, or identifying relationships between columns.
---

# Correlation Explorer

Analyze correlations between variables in CSV/Excel datasets.

## Features

- **Correlation Matrix**: Compute all pairwise correlations
- **Heatmap Visualization**: Color-coded correlation display
- **Significance Testing**: P-values for correlations
- **Multiple Methods**: Pearson, Spearman, Kendall
- **Strong Correlations**: Find highly correlated pairs
- **Target Analysis**: Correlations with specific variable

## Quick Start

```python
from correlation_explorer import CorrelationExplorer

explorer = CorrelationExplorer()

# Load and analyze
explorer.load_csv("sales_data.csv")
matrix = explorer.correlation_matrix()

# Find strong correlations
strong = explorer.find_strong_correlations(threshold=0.7)
print(strong)

# Generate heatmap
explorer.plot_heatmap("correlation_heatmap.png")
```

## CLI Usage

```bash
# Compute correlation matrix
python correlation_explorer.py --input data.csv --output correlations.csv

# Generate heatmap
python correlation_explorer.py --input data.csv --heatmap heatmap.png

# Find strong correlations
python correlation_explorer.py --input data.csv --strong --threshold 0.7

# Correlations with target variable
python correlation_explorer.py --input data.csv --target sales

# Use Spearman correlation
python correlation_explorer.py --input data.csv --method spearman

# Include p-values
python correlation_explorer.py --input data.csv --pvalues
```

## API Reference

### CorrelationExplorer Class

```python
class CorrelationExplorer:
    def __init__(self)

    # Data loading
    def load_csv(self, filepath: str, **kwargs) -> 'CorrelationExplorer'
    def load_dataframe(self, df: pd.DataFrame) -> 'CorrelationExplorer'

    # Analysis
    def correlation_matrix(self, method: str = "pearson") -> pd.DataFrame
    def correlation_with_pvalues(self, method: str = "pearson") -> tuple
    def correlate_with_target(self, target: str, method: str = "pearson") -> pd.Series

    # Discovery
    def find_strong_correlations(self, threshold: float = 0.7) -> list
    def find_weak_correlations(self, threshold: float = 0.3) -> list

    # Visualization
    def plot_heatmap(self, output: str, **kwargs) -> str
    def plot_scatter(self, var1: str, var2: str, output: str) -> str

    # Export
    def to_csv(self, output: str) -> str
    def to_json(self, output: str) -> str
```

## Correlation Methods

| Method | Best For |
|--------|----------|
| `pearson` | Linear relationships, normal data |
| `spearman` | Non-linear, ordinal data |
| `kendall` | Small samples, ordinal data |

```python
# Pearson (default) - parametric
matrix = explorer.correlation_matrix(method="pearson")

# Spearman - rank-based, non-parametric
matrix = explorer.correlation_matrix(method="spearman")

# Kendall - robust to outliers
matrix = explorer.correlation_matrix(method="kendall")
```

## Output Format

### Correlation Matrix
```python
           sales  marketing  customers
sales      1.000      0.854      0.723
marketing  0.854      1.000      0.612
customers  0.723      0.612      1.000
```

### Strong Correlations
```python
[
    {"var1": "sales", "var2": "marketing", "correlation": 0.854, "abs_corr": 0.854},
    {"var1": "sales", "var2": "customers", "correlation": 0.723, "abs_corr": 0.723}
]
```

### With P-Values
```python
{
    "correlations": DataFrame,
    "pvalues": DataFrame,
    "significant": [...],  # p < 0.05
}
```

## Example Workflows

### Feature Selection
```python
explorer = CorrelationExplorer()
explorer.load_csv("features.csv")

# Find features correlated with target
target_corr = explorer.correlate_with_target("target")
important_features = target_corr[abs(target_corr) > 0.3].index.tolist()
print(f"Important features: {important_features}")

# Find multicollinear features (to potentially drop)
strong = explorer.find_strong_correlations(threshold=0.9)
print("Highly correlated pairs (consider dropping one):")
for pair in strong:
    print(f"  {pair['var1']} <-> {pair['var2']}: {pair['correlation']:.3f}")
```

### Sales Analysis
```python
explorer = CorrelationExplorer()
explorer.load_csv("sales_data.csv")

# What drives sales?
sales_corr = explorer.correlate_with_target("revenue")
print("Factors correlated with revenue:")
for var, corr in sales_corr.sort_values(ascending=False).items():
    if var != "revenue":
        print(f"  {var}: {corr:.3f}")

# Visualize
explorer.plot_heatmap("sales_correlations.png")
```

### Data Exploration
```python
explorer = CorrelationExplorer()
explorer.load_csv("dataset.csv")

# Get full picture
corr, pvals = explorer.correlation_with_pvalues()

# Find all significant correlations
significant = []
for i in range(len(corr.columns)):
    for j in range(i+1, len(corr.columns)):
        if pvals.iloc[i, j] < 0.05:
            significant.append({
                'var1': corr.columns[i],
                'var2': corr.columns[j],
                'r': corr.iloc[i, j],
                'p': pvals.iloc[i, j]
            })
```

## Heatmap Options

```python
explorer.plot_heatmap(
    output="heatmap.png",
    cmap="coolwarm",      # Color scheme
    annot=True,           # Show values
    figsize=(12, 10),     # Figure size
    vmin=-1, vmax=1,      # Color scale
    title="Correlation Matrix"
)
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
- scipy>=1.10.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
