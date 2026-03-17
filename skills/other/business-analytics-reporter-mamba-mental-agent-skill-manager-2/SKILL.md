---
name: business-analytics-reporter
description: This skill should be used when analyzing business sales and revenue data from CSV files to identify weak areas, generate statistical insights, and provide strategic improvement recommendations. Use when the user requests a business performance report, asks to analyze sales data, wants to identify areas of weakness, or needs recommendations on business improvement strategies.
---

# Business Analytics Reporter

## Overview

Generate comprehensive business performance reports that analyze sales and revenue data, identify areas where the business is lacking, interpret what the statistics indicate, and provide actionable improvement strategies. The skill uses data-driven analysis to detect weak areas and recommends specific strategies backed by business frameworks.

## When to Use This Skill

Invoke this skill when users request:
- "Analyze my business data and tell me where we're lacking"
- "Generate a report on what areas need improvement"
- "What do these sales numbers tell us about our business performance?"
- "Create a business analysis report with improvement strategies"
- "Identify weak areas in our revenue data"
- "What strategies should we use to improve our business metrics?"

The skill expects CSV files containing business data (sales, revenue, transactions) with columns like dates, amounts, categories, or products.

## Core Workflow

### Step 1: Data Loading and Exploration

Start by understanding the data structure and what the user wants to analyze.

**Ask clarifying questions if needed:**
- What specific metrics or areas should the analysis focus on?
- Are there particular time periods or categories of interest?
- Should the report include visualizations or focus on written analysis?

**Load and explore the data:**
```python
import pandas as pd

# Load the CSV file
df = pd.read_csv('business_data.csv')

# Display basic information
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(df.head())
```

### Step 2: Run Automated Analysis

Use the bundled analysis script to generate comprehensive insights:

```bash
python scripts/analyze_business_data.py path/to/business_data.csv output_report.json
```

The script will:
1. Automatically detect data structure (revenue columns, date columns, categories)
2. Calculate statistical metrics (mean, median, growth rates, volatility)
3. Identify trends and patterns
4. Detect weak areas and underperforming segments
5. Generate improvement strategies based on findings
6. Output a structured JSON report

**Output structure:**
```json
{
  "metadata": {...},
  "findings": {
    "basic_statistics": {...},
    "trend_analysis": {...},
    "category_analysis": {...},
    "variability": {...}
  },
  "weak_areas": [...],
  "improvement_strategies": [...]
}
```

### Step 3: Interpret the Analysis Results

Read the generated JSON report and interpret the findings for the user in plain language.

**Focus on:**
1. **Current State**: What the data shows about business performance
2. **Weak Areas**: Specific problems identified with severity levels
3. **Root Causes**: Why these issues exist (use business frameworks from references/)
4. **Impact**: What these weaknesses mean for the business

**Example interpretation:**
```
Based on the analysis of your sales data from January to December 2024:

Current State:
- Total revenue: $1.2M with average monthly revenue of $100K
- Average growth rate: -3.5% indicating declining performance
- Revenue stability: High volatility (CV: 58%) suggesting inconsistent performance

Weak Areas Identified:
1. Revenue Growth (High Severity): Negative average growth rate of -3.5%
2. Performance Consistency (Medium Severity): 45% of periods show declining performance
3. Category Performance (Medium Severity): 4 underperforming categories identified
```

### Step 4: Generate Detailed Recommendations

Consult the business frameworks reference to provide strategic recommendations:

**Load business frameworks for context:**
Refer to `references/business_frameworks.md` for:
- Revenue growth strategies (market penetration, product development, etc.)
- Operational excellence frameworks
- Customer-centric strategies
- Pricing strategy frameworks
- Common weak area solutions

**Structure recommendations as:**

For each identified weak area, provide:
1. **Strategic Initiative Name**: Clear, actionable program name
2. **Objective**: What this strategy aims to achieve
3. **Key Actions**: 3-5 specific, prioritized steps
4. **Expected Impact**: High/Medium/Low
5. **Timeline**: Realistic implementation timeframe
6. **Success Metrics**: How to measure improvement

**Example recommendation:**
```
Strategy: Revenue Acceleration Program
Area: Revenue Growth
Objective: Reverse negative growth trend and achieve 10%+ monthly growth

Key Actions:
1. Implement aggressive customer acquisition campaigns
2. Review and optimize pricing strategy
3. Launch upselling and cross-selling initiatives
4. Expand into new market segments or geographies
5. Accelerate product development and innovation

Expected Impact: High
Timeline: 3-6 months
Success Metrics: Monthly revenue growth rate, new customer acquisition, ARPU increase
```

### Step 5: Create Visualizations (Optional)

If requested, create interactive visualizations using Plotly to illustrate findings:

**Consult visualization guide:**
Refer to `references/visualization_guide.md` for:
- Recommended chart types for different analyses
- Code examples for creating charts
- Best practices for business dashboards

**Common visualizations to create:**
1. **Revenue Trend Chart**: Line chart showing revenue over time with growth rate overlay
2. **Category Performance**: Bar chart sorted by revenue contribution
3. **Volatility Analysis**: Box plot or standard deviation visualization
4. **Weak Areas Heatmap**: Visual representation of severity and impact

**Example code for revenue trend:**
```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add revenue line
fig.add_trace(
    go.Scatter(x=df['date'], y=df['revenue'], name="Revenue",
               line=dict(color='blue', width=3)),
    secondary_y=False
)

# Add growth rate line
fig.add_trace(
    go.Scatter(x=df['date'], y=df['growth_rate'], name="Growth Rate",
               line=dict(color='green', dash='dash')),
    secondary_y=True
)

fig.update_layout(title_text="Revenue Performance & Growth Rate")
fig.show()
```

### Step 6: Generate Final Report

Compile findings into a comprehensive report format.

**Option A: Generate HTML Report**

Use the report template from `assets/report_template.html`:

```python
# Read the template
with open('assets/report_template.html', 'r') as f:
    template = f.read()

# Load analysis results
with open('output_report.json', 'r') as f:
    analysis = json.load(f)

# Populate the template with actual data
# Replace placeholders with real values from analysis
# Add Plotly charts as JavaScript
# Save as final HTML report

with open('business_report.html', 'w') as f:
    f.write(populated_template)
```

The HTML template includes:
- Executive summary with key metrics
- Interactive charts for trends and categories
- Styled weak area cards with severity indicators
- Strategic recommendations with action items
- Professional styling and print-ready format

**Option B: Generate Markdown Report**

Create a structured markdown document:

```markdown
# Business Performance Analysis Report

**Generated:** [Date]
**Data Period:** [Period]

## Executive Summary

[Brief overview of findings]

## Key Metrics

- Total Revenue: $X
- Average Growth Rate: X%
- Revenue Stability: [Assessment]
- Weak Areas Identified: X

## Performance Trends

[Insert chart or describe trends]

## Areas of Weakness

### 1. [Weak Area Name] (Severity)
**Finding:** [Description]
**Impact:** [Business impact]

### 2. [Next weak area...]

## Strategic Recommendations

### Strategy 1: [Name]
**Objective:** [Goal]
**Actions:**
- [Action 1]
- [Action 2]
...

**Expected Impact:** High/Medium/Low
**Timeline:** X months
```

## Key Analysis Metrics

The analysis script calculates the following metrics automatically:

### Growth Analysis
- **Average Growth Rate**: Period-over-period revenue change percentage
- **Declining Period Count**: Number of periods with negative growth
- **Trend Direction**: Overall trajectory (growing, declining, stable)

### Stability Analysis
- **Coefficient of Variation (CV)**: Measures revenue volatility
  - CV < 25%: Stable performance
  - CV 25-50%: Moderate volatility
  - CV > 50%: High volatility (flag as weak area)

### Category Performance
- **Revenue Contribution**: Percentage breakdown by category
- **Underperforming Categories**: Bottom 25% by average performance
- **Top/Bottom Performers**: Best and worst performing categories

### Statistical Indicators
- Mean, Median, Standard Deviation for all numeric columns
- Min/Max values and ranges
- Total aggregates

## Business Frameworks Reference

When generating recommendations, leverage the frameworks documented in `references/business_frameworks.md`:

1. **Revenue Growth Strategies**: Market penetration, product development, market development, diversification
2. **Operational Excellence**: Process optimization, resource allocation, quality management
3. **Customer-Centric Strategies**: Retention programs, CLV optimization, segmentation
4. **Pricing Strategies**: Value-based, dynamic, competitive pricing
5. **Data-Driven Decision Making**: Analytics maturity model, KPI frameworks

Match identified weak areas with appropriate strategic frameworks to provide contextually relevant recommendations.

## Tips for Effective Reports

1. **Start with the Big Picture**: Lead with overall performance and key findings
2. **Prioritize by Severity**: Focus on high-severity issues first
3. **Be Specific**: Provide concrete numbers and percentages, not vague assessments
4. **Action-Oriented**: Every weak area should have actionable recommendations
5. **Context Matters**: Consider industry benchmarks and business context
6. **Visual Communication**: Use charts to make trends immediately clear
7. **Executive-Friendly**: Structure for quick scanning with clear headers and summaries

## Common Weak Areas and Detection

The analysis automatically detects these common business problems:

| Weak Area | Detection Criteria | Typical Root Causes |
|-----------|-------------------|---------------------|
| Revenue Growth | Negative average growth rate | Market saturation, increased competition, poor positioning |
| Performance Consistency | >40% declining periods | Lack of recurring revenue, seasonal dependency |
| Revenue Stability | CV > 50% | Customer concentration, volatile demand |
| Category Performance | Categories in bottom 25% | Poor product-market fit, pricing issues, low awareness |

## Example Usage

**User request:** "Analyze my Q4 sales data and tell me where we're weak and how to improve"

**Workflow:**
1. Load the CSV: `df = pd.read_csv('q4_sales.csv')`
2. Run analysis: `python scripts/analyze_business_data.py q4_sales.csv q4_report.json`
3. Read results: `with open('q4_report.json') as f: report = json.load(f)`
4. Interpret findings for the user in natural language
5. Create visualizations using Plotly (refer to `references/visualization_guide.md`)
6. Generate HTML report using `assets/report_template.html`
7. Provide strategic recommendations using `references/business_frameworks.md`

**Expected output:**
- Clear explanation of current business performance
- 3-5 identified weak areas with severity levels
- 4-6 strategic initiatives with specific action plans
- Interactive visualizations (if requested)
- Professional HTML or markdown report

## Resources

### scripts/
- `analyze_business_data.py`: Automated analysis engine that detects data structure, calculates metrics, identifies weak areas, and generates improvement strategies

### references/
- `business_frameworks.md`: Comprehensive guide to business strategy frameworks, common weak areas, and solution templates
- `visualization_guide.md`: Chart type recommendations, Plotly code examples, and dashboard design best practices

### assets/
- `report_template.html`: Professional HTML template with interactive visualizations, styled cards for weak areas and strategies, and print-ready formatting
