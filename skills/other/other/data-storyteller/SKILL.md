---
name: data-storyteller
description: Transform CSV/Excel data into narrative reports with auto-generated insights, visualizations, and PDF export. Auto-detects patterns and creates plain-English summaries.
---

# Data Storyteller

Automatically transform raw data into compelling, insight-rich reports. Upload any CSV or Excel file and get back a complete analysis with visualizations, statistical summaries, and narrative explanations - all without writing code.

## Core Workflow

### 1. Load and Analyze Data

```python
from scripts.data_storyteller import DataStoryteller

# Initialize with your data file
storyteller = DataStoryteller("your_data.csv")

# Or from a pandas DataFrame
import pandas as pd
df = pd.read_csv("your_data.csv")
storyteller = DataStoryteller(df)
```

### 2. Generate Full Report

```python
# Generate comprehensive report
report = storyteller.generate_report()

# Access components
print(report['summary'])           # Executive summary
print(report['insights'])          # Key findings
print(report['statistics'])        # Statistical analysis
print(report['visualizations'])    # Generated chart info
```

### 3. Export Options

```python
# Export to PDF
storyteller.export_pdf("analysis_report.pdf")

# Export to HTML (interactive charts)
storyteller.export_html("analysis_report.html")

# Export charts only
storyteller.export_charts("charts/", format="png")
```

## Quick Start Examples

### Basic Analysis
```python
from scripts.data_storyteller import DataStoryteller

# One-liner full analysis
DataStoryteller("sales_data.csv").generate_report().export_pdf("report.pdf")
```

### Custom Analysis
```python
storyteller = DataStoryteller("data.csv")

# Focus on specific columns
storyteller.analyze_columns(['revenue', 'customers', 'date'])

# Set analysis parameters
report = storyteller.generate_report(
    include_correlations=True,
    include_outliers=True,
    include_trends=True,
    time_column='date',
    chart_style='business'
)
```

## Features

### Auto-Detection
- **Column Types**: Numeric, categorical, datetime, text, boolean
- **Data Quality**: Missing values, duplicates, outliers
- **Relationships**: Correlations, dependencies, groupings
- **Time Series**: Trends, seasonality, anomalies

### Generated Visualizations
| Data Type | Charts Generated |
|-----------|-----------------|
| Numeric | Histogram, box plot, trend line |
| Categorical | Bar chart, pie chart, frequency table |
| Time Series | Line chart, decomposition, forecast |
| Correlations | Heatmap, scatter matrix |
| Comparisons | Grouped bar, stacked area |

### Narrative Insights
The storyteller generates plain-English insights including:
- Executive summary of key findings
- Notable patterns and anomalies
- Statistical significance notes
- Actionable recommendations
- Data quality warnings

## Output Sections

### 1. Executive Summary
High-level overview of the dataset and key findings in 2-3 paragraphs.

### 2. Data Profile
- Row/column counts
- Memory usage
- Missing value analysis
- Duplicate detection
- Data type distribution

### 3. Statistical Analysis
For each numeric column:
- Central tendency (mean, median, mode)
- Dispersion (std dev, IQR, range)
- Distribution shape (skewness, kurtosis)
- Outlier count

### 4. Categorical Analysis
For each categorical column:
- Unique values count
- Top/bottom categories
- Frequency distribution
- Category balance assessment

### 5. Correlation Analysis
- Correlation matrix with significance
- Strongest relationships highlighted
- Multicollinearity warnings

### 6. Time-Based Analysis
If datetime column detected:
- Trend direction and strength
- Seasonality patterns
- Year-over-year comparisons
- Growth rate calculations

### 7. Visualizations
Auto-generated charts saved to report:
- Distribution plots
- Trend charts
- Comparison charts
- Correlation heatmaps

### 8. Recommendations
Data-driven suggestions:
- Columns needing attention
- Potential data quality fixes
- Analysis suggestions
- Business implications

## Chart Styles

```python
# Available styles
styles = ['business', 'scientific', 'minimal', 'dark', 'colorful']

storyteller.generate_report(chart_style='business')
```

## Configuration

```python
storyteller = DataStoryteller(df)

# Configure analysis
storyteller.config.update({
    'max_categories': 20,       # Max categories to show
    'outlier_method': 'iqr',    # 'iqr', 'zscore', 'isolation'
    'correlation_threshold': 0.5,
    'significance_level': 0.05,
    'date_format': 'auto',      # Or specify like '%Y-%m-%d'
    'language': 'en',           # Narrative language
})
```

## Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| CSV | .csv | Auto-detect delimiter |
| Excel | .xlsx, .xls | Multi-sheet support |
| JSON | .json | Records or columnar |
| Parquet | .parquet | For large datasets |
| TSV | .tsv | Tab-separated |

## Example Output

### Sample Executive Summary
> "This dataset contains 10,847 records across 15 columns, covering sales transactions from January 2023 to December 2024. Revenue shows a strong upward trend (+23% YoY) with clear seasonal peaks in Q4. The top 3 product categories account for 67% of total revenue. Notable finding: Customer acquisition cost has increased 15% while retention rate dropped 8%, suggesting potential profitability concerns worth investigating."

### Sample Insight
> "Strong correlation detected between marketing_spend and new_customers (r=0.78, p<0.001). However, this relationship weakens significantly after $50K monthly spend, suggesting diminishing returns beyond this threshold."

## Best Practices

1. **Clean data first**: Remove obvious errors before analysis
2. **Name columns clearly**: Helps auto-detection and narratives
3. **Include dates**: Enables time-series analysis
4. **Provide context**: Tell the storyteller what the data represents

## Limitations

- Maximum recommended: 1M rows, 100 columns
- Complex nested data may need flattening
- Images/binary data not supported
- PDF export requires reportlab package

## Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
reportlab>=4.0.0
openpyxl>=3.1.0
```
