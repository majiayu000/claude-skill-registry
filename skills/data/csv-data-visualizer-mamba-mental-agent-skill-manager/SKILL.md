---
name: csv-data-visualizer
description: This skill should be used when working with CSV files to create interactive data visualizations, generate statistical plots, analyze data distributions, create dashboards, or perform automatic data profiling. It provides comprehensive tools for exploratory data analysis using Plotly for interactive visualizations.
---

# CSV Data Visualizer

## Overview

This skill enables comprehensive data visualization and analysis for CSV files. It provides three main capabilities: (1) creating individual interactive visualizations using Plotly, (2) automatic data profiling with statistical summaries, and (3) generating multi-plot dashboards. The skill is optimized for exploratory data analysis, statistical reporting, and creating presentation-ready visualizations.

## When to Use This Skill

Invoke this skill when users request:
- "Visualize this CSV data"
- "Create a histogram/scatter plot/box plot from this data"
- "Show me the distribution of [column]"
- "Generate a dashboard for this dataset"
- "Profile this CSV file" or "Analyze this data"
- "Create a correlation heatmap"
- "Show trends over time"
- "Compare [variable] across [categories]"

## Core Capabilities

### 1. Individual Visualizations

Create specific chart types for detailed analysis using the `visualize_csv.py` script.

**Available Chart Types:**

**Statistical Plots:**
```bash
# Histogram - distribution of numeric data
python3 scripts/visualize_csv.py data.csv --histogram column_name --bins 30

# Box plot - show quartiles and outliers
python3 scripts/visualize_csv.py data.csv --boxplot column_name

# Box plot grouped by category
python3 scripts/visualize_csv.py data.csv --boxplot salary --group-by department

# Violin plot - distribution with probability density
python3 scripts/visualize_csv.py data.csv --violin column_name --group-by category
```

**Relationship Analysis:**
```bash
# Scatter plot with automatic trend line
python3 scripts/visualize_csv.py data.csv --scatter height weight

# Scatter plot with color and size encoding
python3 scripts/visualize_csv.py data.csv --scatter x y --color category --size value

# Correlation heatmap for all numeric columns
python3 scripts/visualize_csv.py data.csv --correlation
```

**Time Series:**
```bash
# Line chart for single variable
python3 scripts/visualize_csv.py data.csv --line date sales

# Multiple variables on same chart
python3 scripts/visualize_csv.py data.csv --line date "sales,revenue,profit"
```

**Categorical Data:**
```bash
# Bar chart (counts categories automatically)
python3 scripts/visualize_csv.py data.csv --bar category

# Pie chart for composition
python3 scripts/visualize_csv.py data.csv --pie region
```

**Output Formats:**
Specify output file with desired format extension:
```bash
# Interactive HTML (default)
python3 scripts/visualize_csv.py data.csv --histogram age -o output.html

# Static image formats
python3 scripts/visualize_csv.py data.csv --scatter x y -o plot.png
python3 scripts/visualize_csv.py data.csv --correlation -o heatmap.pdf
python3 scripts/visualize_csv.py data.csv --bar category -o chart.svg
```

### 2. Automatic Data Profiling

Generate comprehensive data quality and statistical reports using the `data_profile.py` script.

**Text Report (default):**
```bash
python3 scripts/data_profile.py data.csv
```

**HTML Report:**
```bash
python3 scripts/data_profile.py data.csv -f html -o report.html
```

**JSON Report:**
```bash
python3 scripts/data_profile.py data.csv -f json -o profile.json
```

**What the Profiler Provides:**
- File information (size, dimensions)
- Dataset overview (shape, memory usage, duplicates)
- Column-by-column analysis (types, missing data, unique values)
- Missing data patterns and completeness
- Statistical summary for numeric columns (mean, std, quartiles, skewness, kurtosis)
- Categorical column analysis (frequency counts, most/least common values)
- Data quality checks (high missing data, duplicate rows, constant columns, high cardinality)

**When to Use Profiling:**
Always recommend running data profiling BEFORE creating visualizations when:
- User is unfamiliar with the dataset
- Data quality is unknown
- Need to identify appropriate visualization types
- Exploring a new dataset for the first time

### 3. Multi-Plot Dashboards

Create comprehensive dashboards with multiple visualizations using the `create_dashboard.py` script.

**Automatic Dashboard:**
Analyzes data types and automatically creates appropriate visualizations:
```bash
python3 scripts/create_dashboard.py data.csv
```

Custom output location:
```bash
python3 scripts/create_dashboard.py data.csv -o my_dashboard.html
```

Control number of plots:
```bash
python3 scripts/create_dashboard.py data.csv --max-plots 9
```

**Custom Dashboard from Config:**
Create a JSON configuration file specifying exact plots:
```bash
python3 scripts/create_dashboard.py data.csv --config config.json
```

**Dashboard Config Format:**
```json
{
  "title": "Sales Analysis Dashboard",
  "plots": [
    {"type": "histogram", "column": "revenue"},
    {"type": "box", "column": "revenue", "group_by": "region"},
    {"type": "scatter", "column": "advertising", "group_by": "revenue"},
    {"type": "bar", "column": "product_category"},
    {"type": "correlation"}
  ]
}
```

**Dashboard Plot Types:**
- `histogram`: Distribution of numeric column
- `box`: Box plot, optionally grouped by category
- `scatter`: Relationship between two numeric columns
- `bar`: Count of categorical values
- `correlation`: Heatmap of numeric correlations

## Workflow Decision Tree

Use this decision tree to determine the appropriate approach:

```
User provides CSV file
│
├─ "Profile this data" / "Analyze this data" / Unfamiliar dataset
│  └─> Run data_profile.py first
│     Then offer visualization options based on findings
│
├─ "Create dashboard" / "Overview of the data" / Multiple visualizations needed
│  ├─ User knows exact plots wanted
│  │  └─> Create JSON config → run create_dashboard.py with config
│  └─ User wants automatic dashboard
│     └─> Run create_dashboard.py (auto mode)
│
└─ Specific visualization requested ("histogram", "scatter plot", etc.)
   └─> Use visualize_csv.py with appropriate flag
```

## Best Practices

### Starting Analysis
1. **Always profile first** for unfamiliar datasets: `python3 scripts/data_profile.py data.csv`
2. Review the profiling output to understand:
   - Column data types and ranges
   - Missing data patterns
   - Data quality issues
   - Statistical distributions

### Choosing Visualizations
Consult `references/visualization_guide.md` for detailed guidance. Quick reference:
- **Distribution**: Histogram, box plot, violin plot
- **Relationship**: Scatter plot, correlation heatmap
- **Time series**: Line chart
- **Categories**: Bar chart (preferred) or pie chart (use sparingly)
- **Comparison**: Box plot grouped by category

### Creating Dashboards
- **Automatic dashboard**: Good for initial exploration
- **Custom dashboard**: Better for presentations or specific analysis goals
- **Limit plots**: Keep to 6-9 plots maximum for readability
- **Logical grouping**: Group related visualizations together

### Output Considerations
- **HTML**: Best for interactive exploration (zoom, pan, hover tooltips)
- **PNG/PDF**: Best for reports and presentations
- **SVG**: Best for publications requiring vector graphics

## Dependencies

The scripts require these Python packages:
```bash
pip install pandas plotly numpy
```

For static image export (PNG, PDF, SVG), also install:
```bash
pip install kaleido
```

## Example Workflows

### Exploratory Data Analysis
```bash
# 1. Profile the data
python3 scripts/data_profile.py sales_data.csv -f html -o profile.html

# 2. Create automatic dashboard
python3 scripts/create_dashboard.py sales_data.csv -o dashboard.html

# 3. Dive deeper with specific plots
python3 scripts/visualize_csv.py sales_data.csv --scatter price sales --color region
python3 scripts/visualize_csv.py sales_data.csv --boxplot revenue --group-by product
```

### Report Generation
```bash
# Create specific visualizations for report
python3 scripts/visualize_csv.py data.csv --histogram age -o fig1_distribution.png
python3 scripts/visualize_csv.py data.csv --scatter income age -o fig2_correlation.png
python3 scripts/visualize_csv.py data.csv --bar category -o fig3_categories.png

# Generate data summary
python3 scripts/data_profile.py data.csv -f html -o data_summary.html
```

### Interactive Dashboard
```bash
# Create custom dashboard for presentation
# 1. First, create config.json with desired plots
# 2. Generate dashboard
python3 scripts/create_dashboard.py data.csv --config config.json -o presentation_dashboard.html
```

## Troubleshooting

**"Column not found" errors**:
- Run data profiling to see exact column names
- CSV columns are case-sensitive
- Check for leading/trailing spaces in column names

**Empty or incorrect visualizations**:
- Verify data types (numeric vs categorical)
- Check for missing data in plotted columns
- Ensure sufficient non-null values exist

**Script execution errors**:
- Verify dependencies are installed: `pip list | grep plotly`
- Check Python version: Python 3.6+ required
- For image export issues, install kaleido: `pip install kaleido`

## Resources

### scripts/
- `visualize_csv.py`: Main visualization script with all chart types
- `data_profile.py`: Automatic data profiling and quality analysis
- `create_dashboard.py`: Multi-plot dashboard generator

### references/
- `visualization_guide.md`: Comprehensive guide for choosing appropriate chart types, best practices, and common patterns
