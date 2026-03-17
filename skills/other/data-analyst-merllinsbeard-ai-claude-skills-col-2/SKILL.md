---
name: data-analyst
description: This skill should be used when analyzing CSV datasets, handling missing values through intelligent imputation, and creating interactive dashboards to visualize data trends. Use this skill for tasks involving data quality assessment, automated missing value detection and filling, statistical analysis, and generating Plotly Dash dashboards for exploratory data analysis.
---

# Data Analyst

## Overview

This skill provides comprehensive capabilities for data analysis workflows on CSV datasets. It automatically analyzes missing value patterns, intelligently imputes missing data using appropriate statistical methods, and creates interactive Plotly Dash dashboards for visualizing trends and patterns. The skill combines automated missing value handling with rich interactive visualizations to support end-to-end exploratory data analysis.

## Core Capabilities

The data-analyst skill provides three main capabilities that can be used independently or as a complete workflow:

### 1. Missing Value Analysis
Automatically detect and analyze missing values in datasets, identifying patterns and suggesting optimal imputation strategies.

### 2. Intelligent Imputation
Apply sophisticated imputation methods tailored to each column's data type and distribution characteristics.

### 3. Interactive Dashboard Creation
Generate comprehensive Plotly Dash dashboards with multiple visualization types for trend analysis and exploration.

## Complete Workflow

When a user requests complete data analysis with missing value handling and visualization, follow this workflow:

### Step 1: Analyze Missing Values

Run the missing value analysis script to understand the data quality:

```bash
python3 scripts/analyze_missing_values.py <input_file.csv> <output_analysis.json>
```

**What this does**:
- Detects missing values in each column
- Identifies data types (numeric, categorical, temporal, etc.)
- Calculates missing value statistics
- Suggests appropriate imputation strategies per column
- Generates detailed JSON report and console output

**Review the output** to understand:
- Which columns have missing data
- The percentage of missing values
- The recommended imputation method for each column
- Why each method was recommended

### Step 2: Impute Missing Values

Apply automatic imputation based on the analysis:

```bash
python3 scripts/impute_missing_values.py <input_file.csv> <analysis.json> <output_imputed.csv>
```

**What this does**:
- Loads the analysis results (or performs analysis if not provided)
- Applies the optimal imputation method to each column:
  - **Mean**: For normally distributed numeric data
  - **Median**: For skewed numeric data
  - **Mode**: For categorical variables
  - **KNN**: For multivariate numeric data with correlations
  - **Forward fill**: For time series data
  - **Constant**: For high-cardinality text fields
- Handles edge cases (drops rows/columns when appropriate)
- Generates imputation report with before/after statistics
- Saves cleaned dataset

**The script automatically**:
- Drops columns with >70% missing values
- Drops rows where critical ID columns are missing
- Performs batch KNN imputation for correlated variables
- Creates detailed imputation log

### Step 3: Create Interactive Dashboard

Generate an interactive Plotly Dash dashboard:

```bash
python3 scripts/create_dashboard.py <imputed_file.csv> <output_dir> <port>
```

**Example**:
```bash
python3 scripts/create_dashboard.py data_imputed.csv ./visualizations 8050
```

**What this does**:
- Automatically detects column types (numeric, categorical, temporal)
- Creates comprehensive visualizations:
  - **Summary statistics table**: Descriptive stats for all numeric columns
  - **Time series plots**: Trend analysis if date/time columns exist
  - **Distribution plots**: Histograms for understanding data distributions
  - **Correlation heatmap**: Relationships between numeric variables
  - **Categorical analysis**: Bar charts for categorical variables
  - **Scatter plot matrix**: Pairwise relationships between variables
- Launches interactive Dash web server
- Optionally saves static HTML visualizations

**Access the dashboard** at `http://127.0.0.1:8050` (or specified port)

## Individual Use Cases

### Use Case A: Quick Missing Value Assessment

When the user wants to understand data quality without imputation:

```bash
python3 scripts/analyze_missing_values.py data.csv
```

Review the console output to understand missing value patterns and get recommendations.

### Use Case B: Imputation Only

When the user has a dataset with missing values and wants cleaned data:

```bash
python3 scripts/impute_missing_values.py data.csv
```

This performs analysis and imputation in one step, producing `data_imputed.csv`.

### Use Case C: Visualization Only

When the user has a clean dataset and wants interactive visualizations:

```bash
python3 scripts/create_dashboard.py clean_data.csv ./visualizations 8050
```

This creates a full dashboard without any preprocessing.

### Use Case D: Custom Imputation Strategy

When the user wants to review and adjust imputation strategies:

1. Run analysis first:
   ```bash
   python3 scripts/analyze_missing_values.py data.csv analysis.json
   ```

2. Review `analysis.json` and discuss strategies with the user

3. If needed, modify the imputation logic or parameters in the script

4. Run imputation:
   ```bash
   python3 scripts/impute_missing_values.py data.csv analysis.json data_imputed.csv
   ```

## Understanding Imputation Methods

The skill uses intelligent imputation strategies based on data characteristics. Key methods include:

- **Mean/Median**: For numeric data (mean for normal distributions, median for skewed)
- **Mode**: For categorical variables (most frequent value)
- **KNN (K-Nearest Neighbors)**: For multivariate numeric data where variables are correlated
- **Forward Fill**: For time series data (carry last observation forward)
- **Interpolation**: For smooth temporal trends
- **Constant Value**: For high-cardinality text fields (e.g., "Unknown")
- **Drop**: For columns with >70% missing or rows with missing IDs

For detailed information about when each method is appropriate, refer to `references/imputation_methods.md`.

## Dashboard Features

The interactive dashboard includes:

### Summary Statistics
- Count, mean, std, min, max, quartiles for all numeric columns
- Missing value counts and percentages
- Sortable table format

### Time Series Analysis
- Line plots with markers for temporal trends
- Multiple series support (up to 4 primary metrics)
- Hover details with exact values
- Unified hover mode for easy comparison

### Distribution Analysis
- Histograms for all numeric variables
- 30-bin default for granular distribution view
- Multi-panel layout for easy comparison

### Correlation Analysis
- Heatmap showing correlation coefficients
- Color-coded from -1 (negative) to +1 (positive)
- Annotated with exact correlation values
- Useful for identifying relationships

### Categorical Analysis
- Bar charts for categorical variables
- Top 10 categories shown (for high-cardinality variables)
- Frequency counts displayed

### Scatter Plot Matrix
- Pairwise scatter plots for numeric variables
- Limited to 5 variables for readability
- Lower triangle shown (avoiding redundancy)

## Setup and Dependencies

Before using the skill, ensure dependencies are installed:

```bash
pip install -r requirements.txt
```

Required packages:
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `scikit-learn` - KNN imputation
- `plotly` - Interactive visualizations
- `dash` - Web dashboard framework
- `dash-bootstrap-components` - Dashboard styling

## Best Practices

### For Analysis:
1. Always run analysis before imputation to understand data quality
2. Review suggested imputation methods - they're recommendations, not mandates
3. Pay attention to missing value percentages (>40% requires careful consideration)
4. Check data types match expectations (e.g., numeric IDs detected as numeric)

### For Imputation:
1. Save the original dataset before imputation
2. Review the imputation report to ensure methods make sense
3. Check imputed values are within reasonable ranges
4. Consider creating missing indicators for important variables
5. Document which imputation methods were used for reproducibility

### For Dashboards:
1. Use imputed/cleaned data for most accurate visualizations
2. Save static HTML plots if sharing with non-technical stakeholders
3. Use different ports if running multiple dashboards simultaneously
4. For large datasets (>100k rows), consider sampling for faster rendering

## Handling Edge Cases

### High Missing Rates (>50%)
The scripts automatically flag columns with >50% missing values. Options:
- Drop the column if not critical
- Create a missing indicator variable
- Investigate why data is missing (may be informative)

### Mixed Data Types
If a column contains mixed types (e.g., numbers and text):
- The script detects the primary type
- Consider cleaning the column before analysis
- Use constant imputation for mixed-type text columns

### Small Datasets
For datasets with <50 rows:
- Simple imputation (mean/median/mode) is more stable
- Avoid KNN (requires sufficient neighbors)
- Consider dropping rows instead of imputing

### Time Series Gaps
For time series with irregular timestamps:
- Use forward fill for short gaps
- Use interpolation for longer gaps with smooth trends
- Consider the sampling frequency when choosing methods

## Troubleshooting

### Script fails with "module not found"
Install dependencies: `pip install -r requirements.txt`

### Dashboard won't start (port in use)
Specify a different port: `python3 scripts/create_dashboard.py data.csv ./viz 8051`

### KNN imputation is slow
KNN is computationally intensive for large datasets. For >50k rows, consider:
- Using simpler methods (mean/median)
- Sampling the data first
- Using fewer columns in KNN

### Imputed values seem incorrect
- Review the analysis report - check detected data types
- Verify the column is being detected correctly (numeric vs categorical)
- Consider manual adjustment or different imputation method
- Check for outliers that may affect mean/median calculations

## Resources

### scripts/
- `analyze_missing_values.py` - Comprehensive missing value analysis with automatic strategy recommendation
- `impute_missing_values.py` - Intelligent imputation using multiple methods tailored to data characteristics
- `create_dashboard.py` - Interactive Plotly Dash dashboard generator with multiple visualization types

### references/
- `imputation_methods.md` - Detailed guide to missing value imputation strategies, decision frameworks, and best practices

### Other Files
- `requirements.txt` - Python dependencies for the skill
