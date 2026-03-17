---
name: csv-analyzer
description: Comprehensive CSV data analysis and visualization tool. Use this skill when analyzing CSV files, generating data summaries, creating visualizations from data, detecting outliers, finding correlations, assessing data quality, or creating data reports. Triggers on CSV analysis, data exploration, data visualization, data profiling, statistical analysis, or data quality assessment requests.
---

# CSV Analyzer

## Overview

Comprehensive CSV data analysis and visualization engine. Run the script, then use this guide to interpret results and provide insights to users.

## Quick Start

```bash
cd ~/.claude/skills/csv-analyzer/scripts
export $(grep -v '^#' /path/to/project/.env | xargs 2>/dev/null)
python3 analyze_csv.py /path/to/data.csv
```

## Chart Selection Decision Tree

**IMPORTANT**: Choose charts based on what the user needs to understand:

```
What is the user trying to understand?
│
├── "What does my data look like?" (Overview)
│   └── Run with defaults → overview_dashboard.png
│
├── "Is my data clean?" (Quality)
│   └── Check: quality_score, missing_values, duplicates
│   └── Show: missing_values.png if problems exist
│
├── "What's the distribution?" (Single Variable)
│   ├── Numeric → numeric_distributions.png (histogram + KDE)
│   ├── Categorical → categorical_distributions.png (bar chart)
│   └── Time-based → time_series.png
│
├── "Are there outliers?" (Anomalies)
│   └── box_plots.png → points beyond whiskers are outliers
│
├── "How are variables related?" (Relationships)
│   ├── 2 numeric vars → correlation_heatmap.png
│   ├── 2-6 numeric vars → pairplot.png (scatter matrix)
│   ├── Numeric vs Categorical → violin_plot.png
│   └── All numeric → correlation_heatmap.png
│
└── "Can I predict X from Y?" (Predictive)
    └── correlation_heatmap.png → |r| > 0.5 suggests predictive power
```

## How to Interpret Results (For Claude)

### Quality Score Interpretation

| Score | Grade | What to Tell User |
|-------|-------|-------------------|
| 90-100 | A | "Your data is excellent quality - ready for analysis" |
| 80-89 | B | "Good quality data with minor issues worth noting" |
| 70-79 | C | "Moderate quality - address missing values before critical analysis" |
| 60-69 | D | "Significant quality issues - recommend data cleaning first" |
| <60 | F | "Critical issues - data needs substantial cleaning" |

### Correlation Interpretation

| \|r\| Value | Strength | What to Say |
|-------------|----------|-------------|
| 0.9 - 1.0 | Very Strong | "X and Y are very strongly related - almost deterministic" |
| 0.7 - 0.9 | Strong | "X and Y have a strong relationship - X could help predict Y" |
| 0.5 - 0.7 | Moderate | "X and Y are moderately correlated - some predictive value" |
| 0.3 - 0.5 | Weak | "X and Y have a weak relationship - limited predictive power" |
| 0.0 - 0.3 | Negligible | "X and Y appear unrelated" |

**Sign matters:**
- Positive: "As X increases, Y tends to increase"
- Negative: "As X increases, Y tends to decrease"

### Skewness Interpretation

| Skewness | Distribution Shape | Recommendation |
|----------|-------------------|----------------|
| < -1 | Heavy left tail | "Most values are high, with some very low outliers" |
| -1 to -0.5 | Mild left skew | "Slightly more low outliers than high" |
| -0.5 to 0.5 | Symmetric | "Nicely balanced distribution - good for most analyses" |
| 0.5 to 1 | Mild right skew | "Slightly more high outliers than low" |
| > 1 | Heavy right tail | "Most values are low, with some very high outliers. Consider log transform for modeling." |

### Outlier Assessment

When reporting outliers:
- **Few outliers (<1%)**: "A few extreme values that may warrant investigation"
- **Moderate outliers (1-5%)**: "Notable outliers - check if they're errors or genuine extremes"
- **Many outliers (>5%)**: "High outlier rate suggests either data issues or a non-normal distribution"

## Insight Generation Framework

After running analysis, provide insights in this order:

### 1. Data Overview (Always)
```
"Your dataset has [rows] records and [cols] columns:
- [n] numeric columns: [list top 3]
- [n] categorical columns: [list top 3]
- Data quality score: [score]/100 ([grade])"
```

### 2. Key Findings (Pick most relevant)

**If quality issues exist:**
```
"I noticed some data quality concerns:
- [X]% missing values in [column] - [recommend: drop/impute/investigate]
- [N] duplicate rows detected - [recommend: keep first/remove all/investigate]"
```

**If strong correlations found:**
```
"Interesting relationships I found:
- [col1] and [col2] are strongly correlated (r=[value]) - [interpretation]
- This suggests [actionable insight]"
```

**If outliers detected:**
```
"I detected outliers in [columns]:
- [column]: [n] values beyond normal range ([min outlier] to [max outlier])
- These could be [data errors / genuine extremes / worth investigating]"
```

**If skewed distributions:**
```
"[Column] has a [right/left]-skewed distribution:
- Most values cluster around [median]
- But there are extreme values up to [max]
- For modeling, consider [log transform / robust methods]"
```

### 3. Recommendations (Based on findings)

| Finding | Recommendation |
|---------|----------------|
| Missing >20% in column | "Consider dropping this column or investigating why it's missing" |
| Missing <5% scattered | "Safe to impute with median (numeric) or mode (categorical)" |
| High correlation (>0.9) | "These columns may be redundant - consider keeping only one" |
| Many outliers | "Use robust statistics (median instead of mean) or investigate data collection" |
| Highly skewed | "Apply log transform before linear modeling" |
| Low quality score | "Prioritize data cleaning before analysis" |

## Multi-Chart Dashboard Requests

When user asks for a "dashboard" or "comprehensive view":

```bash
# Generate all visualizations
python3 analyze_csv.py data.csv --format html --max-charts 10
```

Then present charts in this order:
1. **overview_dashboard.png** - "Here's your data at a glance"
2. **correlation_heatmap.png** - "Key relationships between variables"
3. **numeric_distributions.png** - "How your numeric data is distributed"
4. **box_plots.png** - "Outlier analysis"
5. **categorical_distributions.png** - "Category breakdowns" (if applicable)

## Command Reference

### Basic Analysis
```bash
python3 analyze_csv.py data.csv
```

### Full Report with All Charts
```bash
python3 analyze_csv.py data.csv --format markdown --max-charts 10
```

### Quick Analysis (No Charts)
```bash
python3 analyze_csv.py data.csv --no-charts
```

### Large Files (>100MB)
```bash
python3 analyze_csv.py huge.csv --sample 50000
```

### Specific Date Columns
```bash
python3 analyze_csv.py data.csv --date-columns created_at updated_at
```

### JSON for Programmatic Use
```bash
python3 analyze_csv.py data.csv --format json --no-charts
```

### Custom Output Location
```bash
python3 analyze_csv.py data.csv --output-dir /path/to/project/.tmp/analysis
```

## Chart Descriptions (For Explaining to Users)

| Chart | When to Show | How to Describe |
|-------|--------------|-----------------|
| overview_dashboard.png | Always for first look | "Here's a bird's eye view of your data" |
| missing_values.png | If missing data exists | "This shows where your data has gaps" |
| numeric_distributions.png | When exploring distributions | "This shows how your numeric values are spread out" |
| box_plots.png | When checking for outliers | "The dots outside the boxes are potential outliers" |
| correlation_heatmap.png | When exploring relationships | "Darker colors = stronger relationships" |
| categorical_distributions.png | For category analysis | "This shows the breakdown of your categories" |
| time_series.png | For temporal data | "Here's how your data changes over time" |
| pairplot.png | For multivariate exploration | "Each cell shows how two variables relate" |
| violin_plot.png | Comparing groups | "This shows how distributions differ across groups" |

## Common User Questions → Actions

| User Says | Action |
|-----------|--------|
| "Analyze this CSV" | Run full analysis, show overview + key insights |
| "Is my data clean?" | Focus on quality_score, missing values, duplicates |
| "Find patterns" | Show correlation_heatmap, highlight strong correlations |
| "Are there outliers?" | Show box_plots, list outlier counts per column |
| "Compare X across Y" | Generate violin_plot for numeric X vs categorical Y |
| "Show me trends" | Generate time_series if datetime column exists |
| "Create a dashboard" | Generate all charts, present organized summary |
| "What should I clean?" | List columns with missing >5%, duplicates, outliers |

## Output Locations

Charts are saved to:
- Default: `~/.claude/skills/csv-analyzer/scripts/.tmp/csv_analysis/`
- Custom: Use `--output-dir /path/to/project/.tmp/analysis`

**Always copy charts to user's project .tmp for visibility:**
```bash
cp ~/.claude/skills/csv-analyzer/scripts/.tmp/csv_analysis/*.png /path/to/project/.tmp/csv_analysis/
```

## Cost

Free - runs entirely locally using pandas, matplotlib, seaborn, scipy.

## Dependencies

```bash
pip install pandas matplotlib seaborn scipy numpy
```
