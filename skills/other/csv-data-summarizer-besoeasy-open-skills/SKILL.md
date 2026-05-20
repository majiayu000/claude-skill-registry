---
name: csv-data-summarizer
description: Analyzes CSV files and automatically generates comprehensive summaries with statistical insights, data quality checks, and visualizations using Python and pandas. No questions asked — just upload a CSV and get a full analysis immediately.
---

# CSV Data Summarizer

This skill analyzes any CSV file and delivers a complete statistical summary with visualizations in one shot. It adapts intelligently to the type of data it finds — sales, customer, financial, operational, survey, or generic tabular data.

## When to Use This Skill

- User uploads or references a CSV file
- Asking to summarize, analyze, or visualize tabular data
- Requesting insights from a dataset
- Wanting to understand data structure and quality

## Behavior Rule

**Do not ask the user what they want. Immediately run the full analysis.**

When a CSV is provided, skip questions like "What would you like me to do?" and go straight to the analysis.

## Required Tools / Libraries

```bash
pip install pandas matplotlib seaborn
```

## How It Works

The skill inspects the data first, then automatically determines which analyses are relevant:

| Data type | Focus areas |
|-----------|-------------|
| Sales / e-commerce | Time-series trends, revenue, product performance |
| Customer data | Distributions, segmentation, geographic patterns |
| Financial | Trend analysis, statistics, correlations |
| Operational | Time-series, performance metrics, distributions |
| Survey | Frequency analysis, cross-tabulations |
| Generic | Adapts based on column types found |

Visualizations are only created when they make sense:
- Time-series plots → only if date/timestamp columns exist
- Correlation heatmaps → only if multiple numeric columns exist
- Category distributions → only if categorical columns exist
- Histograms → for numeric distributions when relevant

## Core Function

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def summarize_csv(file_path):
    df = pd.read_csv(file_path)
    summary = []
    charts_created = []

    # --- Overview ---
    summary.append("=" * 60)
    summary.append("DATA OVERVIEW")
    summary.append("=" * 60)
    summary.append(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")
    summary.append(f"\nColumns: {', '.join(df.columns.tolist())}")

    summary.append("\nDATA TYPES:")
    for col, dtype in df.dtypes.items():
        summary.append(f"  • {col}: {dtype}")

    # --- Data quality ---
    missing = df.isnull().sum().sum()
    missing_pct = (missing / (df.shape[0] * df.shape[1])) * 100
    summary.append("\nDATA QUALITY:")
    if missing:
        summary.append(f"Missing values: {missing:,} ({missing_pct:.2f}% of total data)")
        for col in df.columns:
            col_missing = df[col].isnull().sum()
            if col_missing > 0:
                summary.append(f"  • {col}: {col_missing:,} ({(col_missing / len(df)) * 100:.1f}%)")
    else:
        summary.append("No missing values — dataset is complete.")

    # --- Numeric analysis ---
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        summary.append("\nNUMERICAL ANALYSIS:")
        summary.append(str(df[numeric_cols].describe()))

        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            summary.append("\nCORRELATIONS:")
            summary.append(str(corr_matrix))

            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True, linewidths=1)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plt.savefig('correlation_heatmap.png', dpi=150)
            plt.close()
            charts_created.append('correlation_heatmap.png')

    # --- Categorical analysis ---
    categorical_cols = [c for c in df.select_dtypes(include='object').columns if 'id' not in c.lower()]
    if categorical_cols:
        summary.append("\nCATEGORICAL ANALYSIS:")
        for col in categorical_cols[:5]:
            value_counts = df[col].value_counts()
            summary.append(f"\n{col}:")
            for val, count in value_counts.head(10).items():
                summary.append(f"  • {val}: {count:,} ({(count / len(df)) * 100:.1f}%)")

    # --- Time series analysis ---
    date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower()]
    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        date_range = df[date_col].max() - df[date_col].min()
        summary.append(f"\nTIME SERIES ANALYSIS:")
        summary.append(f"Date range: {df[date_col].min()} to {df[date_col].max()}")
        summary.append(f"Span: {date_range.days} days")

        if numeric_cols:
            fig, axes = plt.subplots(min(3, len(numeric_cols)), 1, figsize=(12, 4 * min(3, len(numeric_cols))))
            if len(numeric_cols) == 1:
                axes = [axes]
            for idx, num_col in enumerate(numeric_cols[:3]):
                ax = axes[idx]
                df.groupby(date_col)[num_col].mean().plot(ax=ax, linewidth=2)
                ax.set_title(f'{num_col} Over Time')
                ax.set_xlabel('Date')
                ax.set_ylabel(num_col)
                ax.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('time_series_analysis.png', dpi=150)
            plt.close()
            charts_created.append('time_series_analysis.png')

    # --- Distribution plots ---
    if numeric_cols:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        for idx, col in enumerate(numeric_cols[:4]):
            axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
            axes[idx].set_title(f'Distribution of {col}')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
            axes[idx].grid(True, alpha=0.3)
        for idx in range(len(numeric_cols[:4]), 4):
            axes[idx].set_visible(False)
        plt.tight_layout()
        plt.savefig('distributions.png', dpi=150)
        plt.close()
        charts_created.append('distributions.png')

    # --- Categorical distribution plots ---
    if categorical_cols:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        for idx, col in enumerate(categorical_cols[:4]):
            value_counts = df[col].value_counts().head(10)
            axes[idx].barh(range(len(value_counts)), value_counts.values)
            axes[idx].set_yticks(range(len(value_counts)))
            axes[idx].set_yticklabels(value_counts.index)
            axes[idx].set_title(f'Top Values in {col}')
            axes[idx].set_xlabel('Count')
            axes[idx].grid(True, alpha=0.3, axis='x')
        for idx in range(len(categorical_cols[:4]), 4):
            axes[idx].set_visible(False)
        plt.tight_layout()
        plt.savefig('categorical_distributions.png', dpi=150)
        plt.close()
        charts_created.append('categorical_distributions.png')

    if charts_created:
        summary.append("\nVISUALIZATIONS CREATED:")
        for chart in charts_created:
            summary.append(f"  ✓ {chart}")

    summary.append("\n" + "=" * 60)
    summary.append("ANALYSIS COMPLETE")
    summary.append("=" * 60)

    return "\n".join(summary)
```

## Usage

```
Here's sales_data.csv. Can you summarize this file?
```

```
Analyze this customer data CSV and show me trends.
```

```
What insights can you find in orders.csv?
```

## Example Output

```
============================================================
DATA OVERVIEW
============================================================
Rows: 5,000 | Columns: 8
Columns: order_id, date, product, category, quantity, price, region, customer_id

DATA TYPES:
  • order_id: int64
  • date: object
  • price: float64
  ...

DATA QUALITY:
Missing values: 100 (0.25% of total data)
  • price: 100 (2.0%)

NUMERICAL ANALYSIS:
         quantity        price
count    5000.000    4900.000
mean        3.200      58.200
std         1.800      12.400
...

TIME SERIES ANALYSIS:
Date range: 2023-01-01 to 2023-12-31
Span: 364 days

VISUALIZATIONS CREATED:
  ✓ time_series_analysis.png
  ✓ distributions.png
  ✓ categorical_distributions.png
  ✓ correlation_heatmap.png
============================================================
ANALYSIS COMPLETE
============================================================
```

## Notes

- Date columns are auto-detected if the column name contains `date` or `time`
- Columns with `id` in the name are excluded from categorical analysis
- All charts are saved as PNG files in the working directory
- Missing data is handled gracefully throughout

## Related Skills

- `json-and-csv-data-transformation` — Clean and reshape CSV data before analysis
- `database-query-and-export` — Export query results to CSV for analysis
- `d3js-data-visualization` — Build interactive browser-based charts from the same data
