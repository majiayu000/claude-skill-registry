---
name: outlier-detective
description: Detect anomalies and outliers in datasets using statistical and ML methods. Use for data cleaning, fraud detection, or quality control analysis.
---

# Outlier Detective

Detect anomalies and outliers in numeric data using multiple methods.

## Features

- **Statistical Methods**: Z-score, IQR, Modified Z-score
- **ML Methods**: Isolation Forest, LOF, DBSCAN
- **Visualization**: Box plots, scatter plots
- **Multi-Column**: Analyze multiple variables
- **Reports**: Detailed outlier reports
- **Flexible Thresholds**: Configurable sensitivity

## Quick Start

```python
from outlier_detective import OutlierDetective

detective = OutlierDetective()
detective.load_csv("sales_data.csv")

# Detect outliers in a column
outliers = detective.detect("revenue", method="iqr")
print(f"Found {len(outliers)} outliers")

# Get full report
report = detective.analyze("revenue")
print(report)
```

## CLI Usage

```bash
# Detect outliers using IQR method
python outlier_detective.py --input data.csv --column sales --method iqr

# Use Z-score with custom threshold
python outlier_detective.py --input data.csv --column price --method zscore --threshold 3

# Analyze all numeric columns
python outlier_detective.py --input data.csv --all

# Generate visualization
python outlier_detective.py --input data.csv --column revenue --plot boxplot.png

# Export outliers to CSV
python outlier_detective.py --input data.csv --column value --output outliers.csv

# Use Isolation Forest (ML)
python outlier_detective.py --input data.csv --method isolation_forest
```

## API Reference

### OutlierDetective Class

```python
class OutlierDetective:
    def __init__(self)

    # Data loading
    def load_csv(self, filepath: str, **kwargs) -> 'OutlierDetective'
    def load_dataframe(self, df: pd.DataFrame) -> 'OutlierDetective'

    # Detection (single column)
    def detect(self, column: str, method: str = "iqr", **kwargs) -> pd.DataFrame
    def analyze(self, column: str) -> dict

    # Detection (multi-column)
    def detect_multivariate(self, columns: list = None, method: str = "isolation_forest") -> pd.DataFrame
    def analyze_all(self) -> dict

    # Visualization
    def plot_boxplot(self, column: str, output: str) -> str
    def plot_scatter(self, col1: str, col2: str, output: str) -> str
    def plot_distribution(self, column: str, output: str) -> str

    # Export
    def get_outliers(self, column: str, method: str = "iqr") -> pd.DataFrame
    def get_clean_data(self, column: str, method: str = "iqr") -> pd.DataFrame
```

## Detection Methods

### Statistical Methods

#### IQR (Interquartile Range)
- Default and most robust method
- Outliers: values below Q1 - 1.5×IQR or above Q3 + 1.5×IQR
- Multiplier configurable (default: 1.5)

```python
outliers = detective.detect("price", method="iqr", multiplier=1.5)
```

#### Z-Score
- Based on standard deviations from mean
- Assumes normal distribution
- Threshold configurable (default: 3)

```python
outliers = detective.detect("price", method="zscore", threshold=3)
```

#### Modified Z-Score
- Uses median instead of mean
- More robust to existing outliers
- Based on MAD (Median Absolute Deviation)

```python
outliers = detective.detect("price", method="modified_zscore", threshold=3.5)
```

### ML Methods

#### Isolation Forest
- Ensemble method, good for high-dimensional data
- Contamination parameter sets expected outlier fraction

```python
outliers = detective.detect_multivariate(
    method="isolation_forest",
    contamination=0.1
)
```

#### Local Outlier Factor (LOF)
- Density-based method
- Compares local density to neighbors

```python
outliers = detective.detect_multivariate(
    method="lof",
    n_neighbors=20
)
```

## Output Format

### detect() Result
```python
# Returns DataFrame of outlier rows with additional columns:
#   - outlier_score: How extreme the value is
#   - outlier_reason: Description of why it's an outlier

   index  value  outlier_score  outlier_reason
0     15   5000          4.2    Above Q3 + 1.5×IQR
1     42  -1000         -3.8    Below Q1 - 1.5×IQR
```

### analyze() Result
```python
{
    "column": "revenue",
    "total_rows": 1000,
    "outlier_count": 23,
    "outlier_percent": 2.3,
    "methods": {
        "iqr": {"count": 23, "indices": [...]},
        "zscore": {"count": 18, "indices": [...]},
        "modified_zscore": {"count": 20, "indices": [...]}
    },
    "stats": {
        "mean": 5432.10,
        "median": 4890.00,
        "std": 1234.56,
        "min": -1000.00,
        "max": 15000.00,
        "q1": 3500.00,
        "q3": 6200.00,
        "iqr": 2700.00
    },
    "bounds": {
        "lower": -550.00,
        "upper": 10250.00
    }
}
```

## Example Workflows

### Data Cleaning Pipeline
```python
detective = OutlierDetective()
detective.load_csv("raw_data.csv")

# Analyze and visualize
report = detective.analyze("price")
print(f"Found {report['outlier_count']} outliers ({report['outlier_percent']:.1f}%)")

# Get clean data
clean_data = detective.get_clean_data("price", method="iqr")
clean_data.to_csv("clean_data.csv")
```

### Fraud Detection
```python
detective = OutlierDetective()
detective.load_csv("transactions.csv")

# Use multiple methods for consensus
iqr_outliers = set(detective.detect("amount", method="iqr").index)
zscore_outliers = set(detective.detect("amount", method="zscore").index)

# Transactions flagged by both methods
high_confidence = iqr_outliers & zscore_outliers
print(f"High-confidence anomalies: {len(high_confidence)}")
```

### Multi-Variable Analysis
```python
detective = OutlierDetective()
detective.load_csv("sensors.csv")

# Detect multivariate outliers
outliers = detective.detect_multivariate(
    columns=["temp", "pressure", "humidity"],
    method="isolation_forest",
    contamination=0.05
)
print(f"Anomalous readings: {len(outliers)}")
```

## Visualization Examples

```python
# Box plot with outliers highlighted
detective.plot_boxplot("revenue", "revenue_boxplot.png")

# Distribution with bounds
detective.plot_distribution("price", "price_dist.png")

# Scatter plot (2D outliers)
detective.plot_scatter("feature1", "feature2", "scatter.png")
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
- scipy>=1.10.0
- scikit-learn>=1.3.0
- matplotlib>=3.7.0
