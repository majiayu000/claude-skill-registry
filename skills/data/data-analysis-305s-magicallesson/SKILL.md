---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: data-analysis
description: "Analyze spreadsheet data, generate insights, create visualizations, and build reports from Excel/CSV data."
version: "1.0.0"
author: claude-office-skills
license: MIT

# Categorization
category: finance
tags:
  - data
  - analysis
  - spreadsheet
  - excel
  - visualization
  - insights
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# MCP Tools Integration
mcp:
  server: office-mcp
  tools:
    - read_xlsx
    - analyze_spreadsheet
    - create_chart
    - pivot_table
  optional_tools:
    - create_xlsx
    - xlsx_to_json

# Skill Capabilities
capabilities:
  - data_analysis
  - statistical_analysis
  - visualization
  - trend_detection
  - reporting

# Input/Output Specification
input:
  required:
    - type: file
      formats: [xlsx, csv, xls]
      description: The spreadsheet data to analyze
  optional:
    - type: text
      name: analysis_goal
      description: Specific questions or analysis goals
    - type: text
      name: output_format
      description: Preferred output format (report, chart, summary)

output:
  primary:
    type: report
    format: markdown
    sections:
      - data_overview
      - key_insights
      - visualizations
      - recommendations

# Language Support
languages:
  - en
  - zh

# Related Skills
related_skills:
  - excel-automation
  - report-generator
  - xlsx-manipulation
---

# Data Analysis Assistant

Analyze data in spreadsheets, uncover insights, and create compelling visualizations.

## Overview

This skill helps you:
- Understand and explore your data
- Perform statistical analysis
- Generate insights and recommendations
- Create charts and visualizations
- Write formulas and queries

## How to Use

### Getting Started
1. Share your spreadsheet or data file
2. Describe what you want to analyze
3. Get insights, formulas, or visualizations

### Analysis Types

**Exploratory Analysis**
```
"What patterns do you see in this data?"
"Give me an overview of this dataset"
"What are the key statistics?"
```

**Specific Questions**
```
"What was the total revenue by region?"
"Which products had the highest growth?"
"Is there a correlation between X and Y?"
```

**Visualization Requests**
```
"Create a chart showing sales trends"
"Make a comparison chart of Q1 vs Q2"
"Show the distribution of customer ages"
```

## Output Formats

### Data Overview
```markdown
## Dataset Overview

**Rows**: 1,234
**Columns**: 15
**Date Range**: Jan 2025 - Dec 2025

### Column Summary
| Column | Type | Non-null | Unique | Sample Values |
|--------|------|----------|--------|---------------|
| date | Date | 100% | 365 | 2025-01-01 |
| revenue | Number | 98% | 890 | $1,234.56 |
| region | Text | 100% | 5 | North, South |

### Data Quality Issues
- [X] rows have missing values in [column]
- [Y] potential duplicates detected
```

### Statistical Analysis
```markdown
## Statistical Summary

### [Metric Name]
- **Mean**: X
- **Median**: Y
- **Std Dev**: Z
- **Min/Max**: A / B

### Key Findings
1. [Finding with statistical support]
2. [Finding with statistical support]

### Recommendations
- [Action based on analysis]
```

### Insight Report
```markdown
## Analysis Report: [Topic]

### Executive Summary
[2-3 sentence overview of key findings]

### Key Metrics
| Metric | Value | Change |
|--------|-------|--------|
| Total Revenue | $X | +Y% |
| Avg Order Value | $Z | -W% |

### Trends
1. **[Trend 1]**: [Description with data]
2. **[Trend 2]**: [Description with data]

### Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]
```

## Common Analysis Workflows

### Sales Analysis
```
1. "Show total sales by month"
2. "Which products are top performers?"
3. "What's the customer segment breakdown?"
4. "Compare this year vs last year"
5. "Forecast next quarter based on trends"
```

### Customer Analysis
```
1. "What's the customer distribution by segment?"
2. "Calculate customer lifetime value"
3. "Which customers are at risk of churning?"
4. "What's the acquisition cost vs LTV ratio?"
```

### Financial Analysis
```
1. "Calculate profit margins by product"
2. "What's the expense breakdown?"
3. "Show cash flow trends"
4. "Compare budget vs actual"
```

## Formula Generation

### Request Formulas
```
"Write a formula to calculate year-over-year growth"
"Create a VLOOKUP to match customer data"
"Make a dynamic sum based on criteria"
```

### Formula Output
```markdown
## Formula: [Purpose]

### Excel/Google Sheets
```excel
=SUMIFS(Sales[Amount], Sales[Region], "North", Sales[Date], ">="&DATE(2025,1,1))
```

### Explanation
- `SUMIFS`: Sums values meeting multiple criteria
- First argument: Column to sum
- Subsequent pairs: Criteria column + criteria value

### Usage
Place in cell [X] where you want the result.
```

## Visualization Recommendations

### Choose the Right Chart
| Data Type | Best Chart |
|-----------|------------|
| Trends over time | Line chart |
| Part of whole | Pie/Donut chart |
| Comparison | Bar chart |
| Distribution | Histogram |
| Correlation | Scatter plot |
| Geographic | Map chart |

### Chart Specifications
```markdown
## Recommended Chart: [Type]

**Data Series**:
- X-axis: [Column] (e.g., Date)
- Y-axis: [Column] (e.g., Revenue)
- Series: [Column] (e.g., Region)

**Formatting**:
- Title: "[Descriptive title]"
- Colors: Use consistent color scheme
- Labels: Show values on data points

**Chart Description**:
[What this chart shows and why it's useful]
```

## Advanced Analysis

### Pivot Table Design
```markdown
## Pivot Table: [Purpose]

**Rows**: [Field 1], [Field 2]
**Columns**: [Field 3]
**Values**: SUM of [Field 4], AVG of [Field 5]
**Filters**: [Field 6]

Expected Output:
| Region | Q1 | Q2 | Q3 | Q4 | Total |
|--------|----|----|----|----|-------|
| North | $X | $X | $X | $X | $X |
| South | $X | $X | $X | $X | $X |
```

### Cohort Analysis
```markdown
## Cohort Analysis

**Cohort Definition**: Customers grouped by [first purchase month]
**Metric**: [Retention rate / Revenue / etc.]
**Time Period**: [12 months]

| Cohort | M0 | M1 | M2 | M3 | ... |
|--------|-----|-----|-----|-----|-----|
| Jan 25 | 100%| 45% | 32% | 28% | ... |
| Feb 25 | 100%| 48% | 35% | 30% | ... |
```

## Best Practices

### For Better Analysis
1. **Clean data first**: Handle missing values, duplicates
2. **Define metrics clearly**: What exactly are you measuring?
3. **Consider context**: Industry benchmarks, seasonality
4. **Validate findings**: Cross-check with other data sources

### For Better Visualizations
1. **Keep it simple**: One main message per chart
2. **Label clearly**: Title, axes, legend
3. **Use appropriate scale**: Don't truncate misleadingly
4. **Consider colorblind users**: Use patterns or distinct colors

## Limitations

- Cannot directly execute code on your data
- Large datasets may need sampling
- Complex statistical models need specialized tools
- Real-time data requires live connections
- Cannot guarantee 100% accuracy on OCR'd data
