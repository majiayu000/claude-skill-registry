---
name: ydata-profiling
version: 1.0.0
description: Automated data quality reports with comprehensive variable analysis, missing value detection, correlations, and HTML report generation - formerly pandas-profiling
author: workspace-hub
category: data-analysis
capabilities:
  - Automated data quality reports
  - Variable type inference and analysis
  - Missing value detection and patterns
  - Correlation analysis (Pearson, Spearman, Kendall, Phik)
  - Duplicate row detection
  - HTML report generation
  - Large dataset handling with minimal mode
  - Comparison reports between datasets
  - Time series analysis
tools:
  - ydata-profiling
  - pandas
  - numpy
  - scipy
  - matplotlib
tags: [ydata-profiling, pandas-profiling, data-quality, eda, profiling, missing-values, correlations, html-report, data-analysis]
platforms: [python]
related_skills:
  - autoviz
  - pandas-data-processing
  - polars
  - great-tables
  - streamlit
---

# YData Profiling Data Quality Skill

Master YData Profiling (formerly pandas-profiling) for automated data quality reports with comprehensive variable analysis, missing value patterns, correlation detection, and publication-ready HTML reports.

## When to Use This Skill

### USE YData Profiling when:
- **Data quality assessment** - Evaluating dataset health and completeness
- **Initial data exploration** - Understanding a new dataset quickly
- **Missing value analysis** - Detecting patterns in missing data
- **Variable analysis** - Understanding distributions and characteristics
- **Data documentation** - Creating shareable data quality reports
- **Dataset comparison** - Comparing training vs test data, or before/after
- **Stakeholder reporting** - Generating professional HTML reports
- **Data validation** - Checking data before ML model training

### DON'T USE YData Profiling when:
- **Real-time analysis** - Need streaming data profiling
- **Custom visualizations** - Specific chart requirements
- **Interactive dashboards** - Use Streamlit or Dash instead
- **Very large datasets** - Over 10M rows (use sampling or minimal mode)
- **Production pipelines** - Need lightweight validation (use Great Expectations)

## Prerequisites

```bash
# Basic installation
pip install ydata-profiling

# With all optional dependencies
pip install 'ydata-profiling[all]'

# Using uv (recommended)
uv pip install ydata-profiling pandas numpy

# Jupyter notebook support
pip install ydata-profiling ipywidgets notebook

# Verify installation
python -c "from ydata_profiling import ProfileReport; print('YData Profiling ready!')"
```

## Core Capabilities

### 1. Basic Profile Report Generation

**Simplest Usage:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

# Load data
df = pd.read_csv("data.csv")

# Generate profile report
profile = ProfileReport(df, title="Data Quality Report")

# Save to HTML file
profile.to_file("report.html")

# Display in Jupyter notebook
profile.to_notebook_iframe()
```

**With Configuration:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("sales_data.csv")

# Customized profile report
profile = ProfileReport(
    df,
    title="Sales Data Quality Report",
    explorative=True,  # Enable all analyses
    dark_mode=False,
    orange_mode=False,
    config_file=None,  # Or path to custom config
    lazy=True  # Defer computation
)

# Access specific sections
print(profile.description_set)  # Variable descriptions
print(profile.get_description())  # Full description

# Save report
profile.to_file("sales_report.html")
```

**From DataFrame with Sample Data:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample dataset
np.random.seed(42)
n = 5000

df = pd.DataFrame({
    "customer_id": range(1, n + 1),
    "name": [f"Customer_{i}" for i in range(n)],
    "age": np.random.normal(40, 15, n).astype(int),
    "income": np.random.exponential(50000, n),
    "category": np.random.choice(["A", "B", "C", "D"], n, p=[0.4, 0.3, 0.2, 0.1]),
    "registration_date": [
        datetime(2020, 1, 1) + timedelta(days=int(d))
        for d in np.random.uniform(0, 1825, n)
    ],
    "is_active": np.random.choice([True, False], n, p=[0.8, 0.2]),
    "score": np.random.uniform(0, 100, n),
    "email": [f"customer_{i}@example.com" for i in range(n)]
})

# Add some missing values
df.loc[np.random.choice(n, 200), "income"] = np.nan
df.loc[np.random.choice(n, 150), "age"] = np.nan

# Generate report
profile = ProfileReport(df, title="Customer Data Profile")
profile.to_file("customer_profile.html")
```

### 2. Variable Analysis

**Understanding Variable Types:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np

# Dataset with various variable types
df = pd.DataFrame({
    # Numeric variables
    "integer_col": np.random.randint(1, 100, 1000),
    "float_col": np.random.randn(1000) * 100,

    # Categorical variables
    "category_high_card": [f"cat_{i}" for i in np.random.randint(1, 100, 1000)],
    "category_low_card": np.random.choice(["A", "B", "C"], 1000),

    # Boolean
    "boolean_col": np.random.choice([True, False], 1000),

    # Date/Time
    "date_col": pd.date_range("2020-01-01", periods=1000, freq="H"),

    # Text
    "text_col": ["Sample text " * np.random.randint(1, 10) for _ in range(1000)],

    # URL
    "url_col": [f"https://example.com/page/{i}" for i in range(1000)],

    # Constant
    "constant_col": ["constant"] * 1000,

    # Unique
    "unique_col": range(1000)
})

profile = ProfileReport(
    df,
    title="Variable Types Analysis",
    explorative=True
)

# The report will automatically detect:
# - Numeric: integer_col, float_col
# - Categorical: category_high_card, category_low_card
# - Boolean: boolean_col
# - DateTime: date_col
# - Text: text_col
# - URL: url_col
# - Constant: constant_col
# - Unique: unique_col (potentially ID column)

profile.to_file("variable_types_report.html")
```

**Detailed Variable Statistics:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "revenue": np.random.exponential(1000, 5000),
    "quantity": np.random.randint(1, 100, 5000),
    "discount": np.random.uniform(0, 0.5, 5000),
    "category": np.random.choice(["Electronics", "Clothing", "Food"], 5000)
})

profile = ProfileReport(df, title="Sales Variables Analysis")

# Access variable-level statistics programmatically
description = profile.get_description()

# Numeric variable statistics
for var_name, var_data in description.variables.items():
    print(f"\n{var_name}:")
    print(f"  Type: {var_data['type']}")
    if "mean" in var_data:
        print(f"  Mean: {var_data['mean']:.2f}")
        print(f"  Std: {var_data['std']:.2f}")
        print(f"  Min: {var_data['min']:.2f}")
        print(f"  Max: {var_data['max']:.2f}")
```

### 3. Missing Value Analysis

**Detecting Missing Patterns:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np

# Create dataset with various missing patterns
np.random.seed(42)
n = 5000

df = pd.DataFrame({
    "complete": np.random.randn(n),  # No missing

    "random_missing": np.where(
        np.random.random(n) < 0.1,
        np.nan,
        np.random.randn(n)
    ),

    "conditional_missing": np.where(
        np.random.randn(n) > 1.5,
        np.nan,
        np.random.randn(n)
    ),

    "block_missing": np.concatenate([
        np.random.randn(4000),
        np.full(1000, np.nan)
    ]),

    "highly_missing": np.where(
        np.random.random(n) < 0.7,
        np.nan,
        np.random.randn(n)
    )
})

# Profile with missing value analysis
profile = ProfileReport(
    df,
    title="Missing Value Analysis",
    missing_diagrams={
        "bar": True,
        "matrix": True,
        "heatmap": True
    }
)

profile.to_file("missing_analysis.html")

# Programmatic access to missing info
description = profile.get_description()
print("\nMissing Value Summary:")
for var_name, var_data in description.variables.items():
    missing_count = var_data.get("n_missing", 0)
    missing_pct = var_data.get("p_missing", 0) * 100
    print(f"  {var_name}: {missing_count} ({missing_pct:.1f}%)")
```

**Missing Value Configuration:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("data_with_missing.csv")

# Detailed missing value analysis
profile = ProfileReport(
    df,
    title="Missing Value Deep Dive",
    missing_diagrams={
        "bar": True,     # Bar chart of missing values per variable
        "matrix": True,  # Nullity matrix (pattern visualization)
        "heatmap": True  # Nullity correlation heatmap
    },
    # Treat certain values as missing
    vars={
        "num": {
            "low_categorical_threshold": 0
        }
    }
)

profile.to_file("missing_deep_dive.html")
```

### 4. Correlation Analysis

**Multiple Correlation Methods:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np

# Create correlated dataset
np.random.seed(42)
n = 2000

x1 = np.random.randn(n)
x2 = np.random.randn(n)

df = pd.DataFrame({
    "x1": x1,
    "x2": x2,
    "y_strong": x1 * 2 + np.random.randn(n) * 0.5,  # Strong correlation
    "y_moderate": x1 + np.random.randn(n) * 2,      # Moderate correlation
    "y_weak": x1 * 0.5 + np.random.randn(n) * 3,    # Weak correlation
    "y_negative": -x1 + np.random.randn(n) * 0.5,   # Negative correlation
    "y_nonlinear": x1 ** 2 + np.random.randn(n),    # Non-linear relationship
    "y_independent": np.random.randn(n),            # No correlation
    "category": np.random.choice(["A", "B", "C"], n)  # Categorical
})

# Profile with all correlation methods
profile = ProfileReport(
    df,
    title="Correlation Analysis",
    correlations={
        "pearson": {"calculate": True, "warn_high_correlations": 0.9},
        "spearman": {"calculate": True, "warn_high_correlations": 0.9},
        "kendall": {"calculate": True, "warn_high_correlations": 0.9},
        "phi_k": {"calculate": True, "warn_high_correlations": 0.9},
        "cramers": {"calculate": True, "warn_high_correlations": 0.9}
    }
)

profile.to_file("correlation_analysis.html")
```

**Correlation Thresholds:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("features.csv")

# Custom correlation thresholds
profile = ProfileReport(
    df,
    title="Feature Correlation Report",
    correlations={
        "pearson": {
            "calculate": True,
            "warn_high_correlations": 0.8,  # Warn above this
            "threshold": 0.3  # Minimum to display
        },
        "spearman": {
            "calculate": True,
            "warn_high_correlations": 0.8
        }
    }
)

profile.to_file("feature_correlations.html")
```

### 5. Large Dataset Handling

**Minimal Mode for Speed:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np

# Large dataset
large_df = pd.DataFrame({
    f"col_{i}": np.random.randn(1000000)
    for i in range(50)
})
large_df["category"] = np.random.choice(["A", "B", "C"], 1000000)

print(f"Dataset size: {large_df.shape}")

# Minimal mode - fast but less detailed
profile = ProfileReport(
    large_df,
    title="Large Dataset Profile",
    minimal=True  # Enables minimal mode
)

profile.to_file("large_dataset_minimal.html")
```

**Sampling for Large Datasets:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np

def profile_large_dataset(
    df: pd.DataFrame,
    sample_size: int = 100000,
    title: str = "Sampled Profile"
) -> ProfileReport:
    """
    Profile large dataset using sampling.

    Args:
        df: Input DataFrame
        sample_size: Number of rows to sample
        title: Report title

    Returns:
        ProfileReport object
    """
    if len(df) > sample_size:
        df_sampled = df.sample(n=sample_size, random_state=42)
        print(f"Sampled {sample_size} rows from {len(df)}")
    else:
        df_sampled = df
        print(f"Using full dataset: {len(df)} rows")

    return ProfileReport(
        df_sampled,
        title=f"{title} (n={len(df_sampled):,})",
        minimal=len(df_sampled) > 50000  # Auto minimal for large samples
    )

# Usage
# large_df = pd.read_parquet("huge_dataset.parquet")
# profile = profile_large_dataset(large_df, sample_size=50000)
# profile.to_file("sampled_profile.html")
```

**Explorative vs Minimal Configuration:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("data.csv")

# EXPLORATIVE MODE - Full analysis (slower)
profile_full = ProfileReport(
    df,
    title="Full Explorative Report",
    explorative=True,  # Enable all analyses
    correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": True},
        "phi_k": {"calculate": True}
    },
    missing_diagrams={
        "bar": True,
        "matrix": True,
        "heatmap": True
    },
    interactions={
        "continuous": True  # Scatter plots for numeric pairs
    }
)

# MINIMAL MODE - Quick overview (faster)
profile_minimal = ProfileReport(
    df,
    title="Minimal Quick Report",
    minimal=True,  # Disable expensive computations
    correlations=None,  # Skip correlations
    missing_diagrams={"bar": False, "matrix": False, "heatmap": False},
    interactions={"continuous": False}
)
```

### 6. Comparison Reports

**Comparing Two Datasets:**
```python
from ydata_profiling import ProfileReport, compare
import pandas as pd
import numpy as np

# Create two related datasets
np.random.seed(42)

# Training data
df_train = pd.DataFrame({
    "feature_1": np.random.randn(5000),
    "feature_2": np.random.exponential(100, 5000),
    "feature_3": np.random.choice(["A", "B", "C"], 5000),
    "target": np.random.randint(0, 2, 5000)
})

# Test data (slightly different distribution)
df_test = pd.DataFrame({
    "feature_1": np.random.randn(2000) * 1.2,  # Different variance
    "feature_2": np.random.exponential(120, 2000),  # Different mean
    "feature_3": np.random.choice(["A", "B", "C", "D"], 2000),  # New category
    "target": np.random.randint(0, 2, 2000)
})

# Generate individual profiles
profile_train = ProfileReport(df_train, title="Training Data")
profile_test = ProfileReport(df_test, title="Test Data")

# Compare profiles
comparison = compare([profile_train, profile_test])

# Save comparison report
comparison.to_file("train_test_comparison.html")
```

**Before/After Comparison:**
```python
from ydata_profiling import ProfileReport, compare
import pandas as pd
import numpy as np

# Original data
df_before = pd.DataFrame({
    "value": np.concatenate([
        np.random.randn(900),
        np.array([100, -50, 200, 150, -100])  # Outliers
    ]),
    "category": np.random.choice(["A", "B", "C"], 905),
    "score": np.random.uniform(0, 100, 905)
})

# Add missing values
df_before.loc[np.random.choice(905, 50), "value"] = np.nan

# Cleaned data (after preprocessing)
df_after = df_before.copy()

# Remove outliers
Q1 = df_after["value"].quantile(0.25)
Q3 = df_after["value"].quantile(0.75)
IQR = Q3 - Q1
df_after = df_after[
    (df_after["value"] >= Q1 - 1.5 * IQR) &
    (df_after["value"] <= Q3 + 1.5 * IQR)
]

# Fill missing values
df_after["value"] = df_after["value"].fillna(df_after["value"].median())

# Compare before and after
profile_before = ProfileReport(df_before, title="Before Cleaning")
profile_after = ProfileReport(df_after, title="After Cleaning")

comparison = compare([profile_before, profile_after])
comparison.to_file("cleaning_comparison.html")
```

### 7. HTML Report Customization

**Custom Report Configuration:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("data.csv")

# Customized report
profile = ProfileReport(
    df,
    title="Custom Styled Report",
    dataset={
        "description": "This is a sample dataset for analysis",
        "creator": "Data Team",
        "copyright_holder": "Company Inc.",
        "copyright_year": "2025",
        "url": "https://company.com/data"
    },
    variables={
        "descriptions": {
            "revenue": "Total revenue in USD",
            "units": "Number of units sold",
            "category": "Product category"
        }
    },
    html={
        "style": {
            "full_width": True
        },
        "navbar_show": True,
        "minify_html": True
    },
    progress_bar=True
)

profile.to_file("custom_report.html")
```

**Report Sections Control:**
```python
from ydata_profiling import ProfileReport
import pandas as pd

df = pd.read_csv("data.csv")

# Control which sections appear
profile = ProfileReport(
    df,
    title="Selective Report",
    samples={
        "head": 10,  # Show first 10 rows
        "tail": 10   # Show last 10 rows
    },
    duplicates={
        "head": 10  # Show first 10 duplicate rows
    },
    correlations={
        "pearson": {"calculate": True},
        "spearman": {"calculate": False},  # Skip Spearman
        "kendall": {"calculate": False},   # Skip Kendall
        "phi_k": {"calculate": False}      # Skip Phi-K
    },
    missing_diagrams={
        "bar": True,
        "matrix": False,  # Skip matrix
        "heatmap": False  # Skip heatmap
    }
)

profile.to_file("selective_report.html")
```

**Export Options:**
```python
from ydata_profiling import ProfileReport
import pandas as pd
import json

df = pd.read_csv("data.csv")
profile = ProfileReport(df, title="Export Demo")

# Export to HTML
profile.to_file("report.html")

# Export to JSON
profile.to_file("report.json")

# Get JSON as string
json_output = profile.to_json()

# Get as dictionary
description_dict = profile.get_description()

# Save widgets for notebook
profile.to_widgets()
```

## Complete Examples

### Example 1: Data Quality Pipeline

```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np
from datetime import datetime
import os
import json

def data_quality_pipeline(
    df: pd.DataFrame,
    output_dir: str,
    dataset_name: str = "dataset",
    target_column: str = None
) -> dict:
    """
    Complete data quality assessment pipeline.

    Args:
        df: Input DataFrame
        output_dir: Output directory for reports
        dataset_name: Name for the dataset
        target_column: Target variable (optional)

    Returns:
        Dictionary with quality metrics
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting data quality assessment for: {dataset_name}")
    print(f"Dataset shape: {df.shape}")

    # Generate profile report
    profile = ProfileReport(
        df,
        title=f"Data Quality Report: {dataset_name}",
        explorative=True,
        correlations={
            "pearson": {"calculate": True, "warn_high_correlations": 0.9},
            "spearman": {"calculate": True},
            "phi_k": {"calculate": True}
        },
        missing_diagrams={
            "bar": True,
            "matrix": True,
            "heatmap": True
        }
    )

    # Save HTML report
    html_path = os.path.join(output_dir, f"{dataset_name}_report.html")
    profile.to_file(html_path)

    # Extract quality metrics
    description = profile.get_description()

    # Calculate quality scores
    quality_metrics = {
        "dataset_name": dataset_name,
        "timestamp": datetime.now().isoformat(),
        "rows": len(df),
        "columns": len(df.columns),
        "memory_mb": df.memory_usage(deep=True).sum() / 1024**2
    }

    # Missing value analysis
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    quality_metrics["completeness_score"] = (1 - missing_cells / total_cells) * 100

    # Variable analysis
    variable_summary = []
    for var_name, var_data in description.variables.items():
        var_info = {
            "name": var_name,
            "type": str(var_data.get("type", "unknown")),
            "missing_count": var_data.get("n_missing", 0),
            "missing_pct": var_data.get("p_missing", 0) * 100,
            "unique_count": var_data.get("n_distinct", 0)
        }

        if "mean" in var_data:
            var_info["mean"] = var_data["mean"]
            var_info["std"] = var_data["std"]

        variable_summary.append(var_info)

    quality_metrics["variables"] = variable_summary

    # Duplicate analysis
    duplicate_rows = df.duplicated().sum()
    quality_metrics["duplicate_rows"] = duplicate_rows
    quality_metrics["uniqueness_score"] = (1 - duplicate_rows / len(df)) * 100

    # Constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    quality_metrics["constant_columns"] = constant_cols

    # High cardinality columns
    high_card_threshold = 0.9
    high_card_cols = [
        col for col in df.columns
        if df[col].nunique() / len(df) > high_card_threshold
    ]
    quality_metrics["high_cardinality_columns"] = high_card_cols

    # Overall quality score
    quality_score = (
        quality_metrics["completeness_score"] * 0.4 +
        quality_metrics["uniqueness_score"] * 0.3 +
        (100 - len(constant_cols) / len(df.columns) * 100) * 0.3
    )
    quality_metrics["overall_quality_score"] = quality_score

    # Save metrics as JSON
    metrics_path = os.path.join(output_dir, f"{dataset_name}_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(quality_metrics, f, indent=2, default=str)

    print(f"\nQuality Assessment Complete:")
    print(f"  Completeness Score: {quality_metrics['completeness_score']:.1f}%")
    print(f"  Uniqueness Score: {quality_metrics['uniqueness_score']:.1f}%")
    print(f"  Overall Quality Score: {quality_metrics['overall_quality_score']:.1f}%")
    print(f"\nReports saved to: {output_dir}")

    return quality_metrics

# Usage example
def generate_sample_data():
    """Generate sample data for testing."""
    np.random.seed(42)
    n = 10000

    df = pd.DataFrame({
        "customer_id": range(1, n + 1),
        "revenue": np.random.exponential(500, n),
        "quantity": np.random.randint(1, 50, n),
        "category": np.random.choice(["Electronics", "Clothing", "Food"], n),
        "region": np.random.choice(["North", "South", "East", "West"], n),
        "date": pd.date_range("2024-01-01", periods=n, freq="H"),
        "score": np.random.uniform(0, 100, n)
    })

    # Add some issues
    df.loc[np.random.choice(n, 500), "revenue"] = np.nan
    df.loc[np.random.choice(n, 300), "score"] = np.nan

    # Add duplicates
    df = pd.concat([df, df.sample(200)], ignore_index=True)

    return df

# sample_df = generate_sample_data()
# metrics = data_quality_pipeline(sample_df, "quality_output", "sales_data")
```

### Example 2: ML Dataset Profiling

```python
from ydata_profiling import ProfileReport, compare
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def ml_dataset_profiling(
    X: pd.DataFrame,
    y: pd.Series,
    output_dir: str,
    test_size: float = 0.2
) -> dict:
    """
    Profile ML dataset with train/test comparison.

    Args:
        X: Feature DataFrame
        y: Target Series
        output_dir: Output directory
        test_size: Test set proportion

    Returns:
        Profiling results
    """
    os.makedirs(output_dir, exist_ok=True)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # Combine features and target
    df_train = X_train.copy()
    df_train["target"] = y_train.values

    df_test = X_test.copy()
    df_test["target"] = y_test.values

    print(f"Training set: {df_train.shape}")
    print(f"Test set: {df_test.shape}")

    # Generate individual profiles
    print("\nProfiling training set...")
    profile_train = ProfileReport(
        df_train,
        title="Training Set Profile",
        explorative=True
    )
    profile_train.to_file(os.path.join(output_dir, "train_profile.html"))

    print("Profiling test set...")
    profile_test = ProfileReport(
        df_test,
        title="Test Set Profile",
        explorative=True
    )
    profile_test.to_file(os.path.join(output_dir, "test_profile.html"))

    # Generate comparison report
    print("Generating comparison report...")
    comparison = compare([profile_train, profile_test])
    comparison.to_file(os.path.join(output_dir, "train_test_comparison.html"))

    # Check for data drift
    drift_metrics = {}
    numeric_cols = X.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        train_mean = df_train[col].mean()
        test_mean = df_test[col].mean()
        train_std = df_train[col].std()

        # Calculate drift as standardized difference
        drift = abs(train_mean - test_mean) / train_std if train_std > 0 else 0
        drift_metrics[col] = {
            "train_mean": train_mean,
            "test_mean": test_mean,
            "drift_score": drift
        }

    # Identify significant drift
    significant_drift = [
        col for col, metrics in drift_metrics.items()
        if metrics["drift_score"] > 0.5
    ]

    if significant_drift:
        print(f"\nWarning: Significant drift detected in: {significant_drift}")

    return {
        "train_profile": profile_train,
        "test_profile": profile_test,
        "comparison": comparison,
        "drift_metrics": drift_metrics,
        "significant_drift": significant_drift,
        "output_dir": output_dir
    }

# Generate sample ML dataset
def create_ml_dataset(n_samples=10000):
    """Create sample ML dataset."""
    np.random.seed(42)

    X = pd.DataFrame({
        "feature_1": np.random.randn(n_samples),
        "feature_2": np.random.exponential(10, n_samples),
        "feature_3": np.random.uniform(0, 100, n_samples),
        "feature_4": np.random.randn(n_samples) * 5,
        "category": np.random.choice(["A", "B", "C"], n_samples)
    })

    # Target based on features
    y = (X["feature_1"] + X["feature_2"] / 10 > 1).astype(int)
    y = pd.Series(y, name="target")

    return X, y

# X, y = create_ml_dataset(10000)
# results = ml_dataset_profiling(X, y, "ml_profiling_output")
```

### Example 3: Time Series Data Profiling

```python
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def profile_time_series(
    df: pd.DataFrame,
    date_column: str,
    value_columns: list,
    output_dir: str
) -> dict:
    """
    Profile time series data with temporal analysis.

    Args:
        df: Time series DataFrame
        date_column: Date/time column name
        value_columns: List of value columns to analyze
        output_dir: Output directory

    Returns:
        Profiling results
    """
    os.makedirs(output_dir, exist_ok=True)

    # Ensure datetime type
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])

    # Sort by date
    df = df.sort_values(date_column)

    # Add temporal features
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month
    df["day_of_week"] = df[date_column].dt.dayofweek
    df["hour"] = df[date_column].dt.hour
    df["is_weekend"] = df["day_of_week"].isin([5, 6])

    # Generate main profile
    profile = ProfileReport(
        df,
        title="Time Series Data Profile",
        tsmode=True,  # Enable time series mode
        sortby=date_column,
        explorative=True
    )

    profile.to_file(os.path.join(output_dir, "time_series_profile.html"))

    # Analyze temporal patterns
    temporal_analysis = {}

    for col in value_columns:
        # Monthly statistics
        monthly = df.groupby("month")[col].agg(["mean", "std", "min", "max"])
        temporal_analysis[f"{col}_monthly"] = monthly.to_dict()

        # Day of week statistics
        dow = df.groupby("day_of_week")[col].agg(["mean", "std"])
        temporal_analysis[f"{col}_day_of_week"] = dow.to_dict()

    # Profile by time period
    # Most recent period
    recent_cutoff = df[date_column].max() - timedelta(days=30)
    df_recent = df[df[date_column] >= recent_cutoff]

    if len(df_recent) > 100:
        profile_recent = ProfileReport(
            df_recent,
            title="Recent 30 Days Profile",
            minimal=True
        )
        profile_recent.to_file(os.path.join(output_dir, "recent_30d_profile.html"))

    print(f"Time series profiling complete!")
    print(f"Date range: {df[date_column].min()} to {df[date_column].max()}")
    print(f"Total records: {len(df):,}")

    return {
        "main_profile": profile,
        "temporal_analysis": temporal_analysis,
        "output_dir": output_dir
    }

# Generate sample time series
def create_time_series_data():
    """Create sample time series data."""
    np.random.seed(42)

    # Generate hourly data for 1 year
    dates = pd.date_range("2024-01-01", "2024-12-31", freq="H")
    n = len(dates)

    # Trend + seasonality + noise
    trend = np.linspace(100, 150, n)
    daily_seasonality = 20 * np.sin(2 * np.pi * np.arange(n) / 24)
    weekly_seasonality = 10 * np.sin(2 * np.pi * np.arange(n) / (24 * 7))
    noise = np.random.randn(n) * 5

    return pd.DataFrame({
        "timestamp": dates,
        "value": trend + daily_seasonality + weekly_seasonality + noise,
        "volume": np.random.exponential(1000, n),
        "category": np.random.choice(["A", "B", "C"], n)
    })

# ts_df = create_time_series_data()
# results = profile_time_series(
#     ts_df,
#     date_column="timestamp",
#     value_columns=["value", "volume"],
#     output_dir="time_series_output"
# )
```

## Integration Examples

### YData Profiling with Streamlit

```python
import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(page_title="Data Profiler", layout="wide")
st.title("Interactive Data Profiler")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head(100))

    # Profile options
    with st.sidebar:
        st.header("Profile Options")
        minimal = st.checkbox("Minimal Mode", value=False)
        explorative = st.checkbox("Explorative Mode", value=True)

    if st.button("Generate Profile"):
        with st.spinner("Generating report..."):
            profile = ProfileReport(
                df,
                title="Data Profile",
                minimal=minimal,
                explorative=explorative
            )

            st_profile_report(profile)
```

### YData Profiling with Polars

```python
from ydata_profiling import ProfileReport
import polars as pl
import pandas as pd

def profile_polars_df(
    lf: pl.LazyFrame,
    title: str = "Polars Data Profile",
    **kwargs
) -> ProfileReport:
    """
    Profile Polars LazyFrame using YData Profiling.

    Args:
        lf: Polars LazyFrame
        title: Report title
        **kwargs: Additional ProfileReport arguments

    Returns:
        ProfileReport object
    """
    # Collect and convert to pandas
    df_polars = lf.collect()
    df_pandas = df_polars.to_pandas()

    return ProfileReport(df_pandas, title=title, **kwargs)

# Usage
# lf = pl.scan_parquet("data.parquet")
# profile = profile_polars_df(lf, title="Polars Data Profile")
# profile.to_file("profile.html")
```

## Best Practices

### 1. Use Minimal Mode for Large Datasets

```python
# GOOD: Minimal mode for large data
profile = ProfileReport(large_df, minimal=True)

# AVOID: Full explorative on large data
# profile = ProfileReport(large_df, explorative=True)  # Slow!
```

### 2. Sample for Initial Exploration

```python
# GOOD: Sample first, then full profile
sample = df.sample(n=10000, random_state=42)
profile = ProfileReport(sample, title="Sample Profile")

# If interesting, profile full data
# profile_full = ProfileReport(df, minimal=True)
```

### 3. Customize for Your Needs

```python
# GOOD: Disable unnecessary computations
profile = ProfileReport(
    df,
    correlations={"pearson": {"calculate": True}},  # Only Pearson
    missing_diagrams={"bar": True, "matrix": False, "heatmap": False}
)
```

### 4. Use Lazy Evaluation

```python
# GOOD: Lazy profile, compute when needed
profile = ProfileReport(df, lazy=True)
# ... do other work ...
profile.to_file("report.html")  # Computes here
```

## Troubleshooting

### Common Issues

**Issue: Memory error with large dataset**
```python
# Solution 1: Use minimal mode
profile = ProfileReport(df, minimal=True)

# Solution 2: Sample data
profile = ProfileReport(df.sample(50000))
```

**Issue: Slow report generation**
```python
# Solution: Disable expensive computations
profile = ProfileReport(
    df,
    correlations=None,
    interactions={"continuous": False},
    missing_diagrams={"matrix": False, "heatmap": False}
)
```

**Issue: Report too large**
```python
# Solution: Limit samples shown
profile = ProfileReport(
    df,
    samples={"head": 5, "tail": 5},
    duplicates={"head": 5}
)
```

**Issue: DateTime not recognized**
```python
# Solution: Convert explicitly
df["date_col"] = pd.to_datetime(df["date_col"])
profile = ProfileReport(df)
```

## Version History

- **1.0.0** (2026-01-17): Initial release
  - Basic profile report generation
  - Variable analysis and type detection
  - Missing value analysis patterns
  - Correlation methods (Pearson, Spearman, Kendall, Phi-K)
  - Large dataset handling (minimal mode, sampling)
  - Comparison reports for datasets
  - HTML report customization
  - Time series profiling
  - Complete pipeline examples
  - Integration with Streamlit and Polars
  - Best practices and troubleshooting

## Resources

- **Official Documentation**: https://docs.profiling.ydata.ai/
- **GitHub**: https://github.com/ydataai/ydata-profiling
- **PyPI**: https://pypi.org/project/ydata-profiling/
- **Migration from pandas-profiling**: https://docs.profiling.ydata.ai/latest/migration/

---

**Generate comprehensive data quality reports automatically with YData Profiling!**
