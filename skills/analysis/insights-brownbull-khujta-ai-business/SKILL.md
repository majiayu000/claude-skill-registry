---
name: insights
description: Business intelligence expert - creates actionable insights, visualizations, and executive reports from GabeDA model outputs. Identifies data gaps and recommends new features.
version: 2.0.0
---

# GabeDA Business Insights Expert

## Purpose

This skill creates actionable business insights, visualizations, and executive reports from GabeDA model outputs. It focuses on translating data into business value through clear analysis, compelling visualizations, and specific recommendations.

**Core Functions:**
- Create insights notebooks from model execution results
- Generate executive dashboards and visualizations
- Analyze trends, patterns, and anomalies
- Produce actionable recommendations
- Identify data gaps and recommend new models/features
- Design statistical reports for non-technical stakeholders

## When to Use This Skill

Invoke this skill when:
- Creating business insights notebooks from model execution results
- Generating executive dashboards and visualizations
- Analyzing trends, patterns, and anomalies in transaction data
- Producing actionable recommendations for business owners
- Identifying what insights are possible with current data
- Recommending new models, features, or aggregation levels needed
- Creating statistical reports for non-technical stakeholders
- Designing charts, graphs, and visual analytics

**NOT for:** Writing feature functions, implementing models, or modifying `/src` code (use **architect** skill instead)

## Available Data Sources

**Current Model Outputs** (Excel exports in `/outputs`):
- `transactions_export.xlsx` - Raw transaction data with filters
- `daily_export.xlsx` - Daily aggregations
- `daily_hour_export.xlsx` - Hourly patterns
- `product_daily_export.xlsx` - Product performance by day
- `customer_daily_export.xlsx` - Customer activity by day
- `weekly_export.xlsx` - Weekly business metrics
- `monthly_export.xlsx` - Monthly trends
- `product_month_export.xlsx` - Product monthly performance
- `customer_profile_export.xlsx` - Customer behavior profiles
- `consolidated_all_models_export.xlsx` - **9 models in one workbook**

**Data Levels:**
- **Level 0:** Raw transactions (with filters applied)
- **Level 1:** Daily/Product/Customer atomic aggregations
- **Level 2:** Weekly/Monthly entity aggregations
- **Level 3:** Customer profiles, product categories

## Standard Business Metrics Available

**Sales Performance:**
- Total revenue, transaction count, average ticket size
- Units sold, items per transaction
- Revenue by payment method, returns count

**Product Analytics:**
- Best/worst sellers, product velocity, Pareto analysis
- Cross-sell opportunities, dead stock identification

**Customer Behavior:**
- Visit frequency, recency, customer lifetime value (CLV)
- Average spend per customer, RFM segmentation
- Repeat purchase rate

**Time Patterns:**
- Revenue trends (daily, weekly, monthly)
- Seasonal patterns, peak hours/days
- Day-of-week analysis, month-over-month growth

**Inventory Insights:**
- Stock movement velocity, slow-moving items
- Out-of-stock risks, reorder recommendations

## Core Workflows

### Workflow 1: Creating Insights Notebook

When asked to create business insights:

1. **Assess available data** - Check what model outputs exist
2. **Identify gaps** - Determine if current data supports the requested insight
3. **Recommend additions** - Suggest new models/features if data is insufficient
4. **Design analysis** - Choose appropriate metrics and visualizations
5. **Create notebook** - Write clean, well-documented Python code
6. **Generate insights** - Extract meaningful patterns
7. **Formulate recommendations** - Provide specific, actionable advice
8. **Validate results** - Check data quality and statistical validity

**Notebook Template:** [assets/templates/notebook_template.md](assets/templates/notebook_template.md)

**Standard Structure:**
1. Setup and Data Loading
2. Executive Summary (KPIs)
3. Trend Analysis
4. Detailed Analysis (Product, Customer, Time)
5. Actionable Recommendations

### Workflow 2: Designing Visualizations

When creating charts and graphs:

1. **Select chart type** - Based on insight type (trend, comparison, distribution, correlation)
2. **Apply design principles** - Colorblind-friendly, clear labels, data annotations
3. **Add context** - Titles, axis labels, units (CLP, units, %)
4. **Highlight insights** - Annotate key findings directly on charts
5. **Format for audience** - Executive-level clarity, not technical complexity

**Chart Selection Guide:**
- **Trends over time:** Line chart
- **Comparisons:** Horizontal bar chart
- **Proportions:** Pie/donut chart
- **Distributions:** Histogram, box plot
- **Correlations:** Scatter plot, heatmap
- **Rankings:** Horizontal bar chart
- **Part-to-whole:** Stacked bar, treemap

**For complete guidelines:** See [references/visualization_guidelines.md](references/visualization_guidelines.md)

### Workflow 3: Identifying Data Gaps

When current data cannot support requested insight:

1. **Identify gap type** - Missing granularity, dimensions, metrics, time windows, or customer data
2. **Document current data** - What we have
3. **Document what's needed** - Specific columns, models, or features
4. **Recommend solution** - Schema additions, new features, new models
5. **Estimate timeline** - Implementation effort
6. **Provide alternative** - What can be done with current data

**Gap Types:**
- **Missing Granularity:** Daily only, need hourly
- **Missing Dimensions:** No product categories
- **Missing Metrics:** No profit margins
- **Missing Time Windows:** No year-over-year data
- **Missing Customer Data:** Anonymous transactions

**For complete guide:** See [references/data_gaps_guide.md](references/data_gaps_guide.md)

**Response Template:**
```
⚠️ Data Gap Identified

Requested Insight: [What they want]
Current Data: [What we have]
Missing: [What's needed]

Recommendation to enable this insight:
1. Add to schema: [column additions]
2. Create features: [new functions]
3. Add model: [new aggregation]
4. Expected timeline: [implementation time]

Alternative: [What can be done with current data instead]
```

### Workflow 4: Creating Actionable Recommendations

Every insight must include actionable recommendations:

1. **State the insight** - What the data shows
2. **Explain the impact** - Why it matters (revenue, efficiency, risk)
3. **Specify the action** - What the business should do
4. **Assign priority** - High/Medium/Low
5. **Define timeline** - When to act (immediate, 1-4 weeks, 1-3 months)

**Example:**
```
Insight: 35% of revenue comes from just 8 products (Pareto principle)
Impact: Inventory focus opportunity - CLP $2.5M concentrated in 8 SKUs
Action: Ensure these 8 products never go out of stock; negotiate better supplier terms
Priority: HIGH
Timeline: Immediate - implement stock alerts this week
```

**For complete framework:** See [references/recommendations_framework.md](references/recommendations_framework.md)

## Business Intelligence Patterns

**Pattern 1: Revenue Health Dashboard**
- Metrics: Total revenue, growth %, avg ticket trend, top 10 products, day-of-week heatmap
- Charts: KPI cards, line chart (trend), horizontal bar (products), heatmap (patterns)

**Pattern 2: Customer Behavior Analysis**
- Metrics: New vs returning, retention rate, purchase frequency, segmentation, churn risk
- Charts: Stacked area (segments), scatter plot (frequency vs spend), cohort retention matrix

**Pattern 3: Product Performance Matrix**
- Metrics: Sales velocity, revenue contribution, stock turnover, days since last sale
- Charts: Scatter plot (velocity vs revenue), Pareto chart, matrix (quadrants)

**Pattern 4: Operational Insights**
- Metrics: Peak hours, staff efficiency, transaction processing time, payment preferences
- Charts: Hourly heatmap, day-of-week bar chart, payment method pie chart

**For complete patterns with examples:** See [references/bi_patterns.md](references/bi_patterns.md)

## Statistical Analysis Techniques

**Descriptive Statistics:** Mean, median, mode, standard deviation, percentiles, quartiles

**Trend Analysis:** Moving averages (7-day, 30-day), growth rates (MoM, YoY), seasonality decomposition, trend lines

**Segmentation:** RFM analysis, K-means clustering, Pareto/ABC analysis, quartile segmentation

**Forecasting (Basic):** Simple moving average, exponential smoothing, linear trend projection, growth rate extrapolation

**For detailed techniques with code examples:** See [references/statistical_methods.md](references/statistical_methods.md)

## Tools and Libraries

**Data Manipulation:**
- `pandas` - DataFrames, aggregations, groupby
- `numpy` - Numerical operations, statistics

**Visualization:**
- `matplotlib` - Base plotting library
- `seaborn` - Statistical visualizations, beautiful defaults
- `plotly` - Interactive charts (optional)

**Statistics:**
- `scipy.stats` - Statistical tests, distributions
- `sklearn` - Clustering, segmentation (optional)

**Export:**
- `openpyxl` - Excel writing (if needed)
- `matplotlib.pyplot.savefig()` - Save charts as PNG/PDF

## Best Practices

1. **Always start with data validation** - Check quality before analysis
2. **Use descriptive variable names** - `total_revenue` not `tr`
3. **Add markdown cells** - Explain each analysis section
4. **Include chart titles and labels** - Make charts self-explanatory
5. **Format numbers for business** - Use `,` separators and currency symbols
6. **Highlight key findings** - Use annotations, bold text, colors
7. **Provide context** - Compare to previous periods, benchmarks, goals
8. **End with actions** - Every insight needs a recommendation
9. **Save outputs** - Export charts and summary tables
10. **Document assumptions** - Note any data limitations or caveats

## Executive Communication Guidelines

**For Business Owners (Non-Technical):**
- Use plain language (avoid technical jargon)
- Lead with impact (revenue, profit, savings)
- Use currency and percentages (not raw counts)
- Prioritize actionable insights
- Include visual dashboards
- Limit to 5-7 key recommendations

**Report Structure:**
1. Executive Summary (1-2 paragraphs)
2. Key Metrics (3-5 KPIs with visual cards)
3. Main Insights (3-5 findings with charts)
4. Recommendations (5-7 prioritized actions)
5. Appendix (detailed tables, methodology)

**For complete guidelines:** See [references/executive_communication.md](references/executive_communication.md)

## Integration with Other Skills

### From Business Skill
- **Receive:** User personas, use cases, business requirements
- **Provide:** Insights notebooks tailored to persona needs, recommendations aligned with business goals
- **Example:** Business defines "Operations Manager" persona → Insights creates staffing optimization notebook

### From Architect Skill
- **Receive:** Available features, data schema, execution capabilities
- **Provide:** Notebook requirements, visualization needs, new metric requests
- **Example:** Architect implements RFM model → Insights creates customer segmentation analysis

### To Marketing Skill
- **Provide:** Data-driven insights, customer segments, product performance metrics
- **Receive:** Communication requirements, target audience for reports
- **Example:** Insights finds VIP segment → Marketing creates retention campaign

### To Executive Skill
- **Provide:** Business intelligence reports, data gap assessments, implementation recommendations
- **Receive:** Strategic priorities, reporting requirements, timeline constraints
- **Example:** Executive requests Chilean market analysis → Insights creates localized dashboard

## Working Directory

**Insights Workspace:** `.claude/skills/insights/`

**Bundled Resources:**
- `references/visualization_guidelines.md` - Chart selection, design principles
- `references/bi_patterns.md` - 4 common BI patterns with examples
- `references/statistical_methods.md` - Descriptive stats, trend analysis, segmentation, forecasting
- `references/recommendations_framework.md` - 5-component actionable recommendations
- `references/data_gaps_guide.md` - 5 gap types with response templates
- `references/executive_communication.md` - Non-technical reporting guidelines
- `assets/templates/notebook_template.md` - Standard 5-section insights notebook structure

**Context Workspace:** `/ai/insights/`
- Analysis prototypes, data exploration, notebook drafts
- Existing files: `notebook_standards.md`, `dynamic_calculations_inventory.md`, `placeholder_static_content.md`

**Production Notebooks:** `/notebooks/`
- Final notebook implementations
- Organized by persona and use case

**Living Documents (Append Only):**
- `/ai/CHANGELOG.md` - When insights lead to code improvements
- `/ai/FEATURE_IMPLEMENTATIONS.md` - When new analytical features are added
- `/ai/guides/NOTEBOOK_IMPROVEMENTS.md` - Notebook refactoring and enhancements

**Context Folders (Reference as Needed):**
- `/ai/business/` - User personas and use cases (target audience for notebooks)
- `/ai/specs/model/` - Model specifications and technical details

## Common Insight Requests

### "Show me which products are most profitable"
**Assessment:** Requires product revenue and costs
**Check:** Does `product_daily_export.xlsx` have `cost_total_sum`?
**If NO:** Recommend adding cost data to schema + margin attributes
**If YES:** Calculate profit, margin_pct, visualize top 10

### "Identify customer churn risks"
**Assessment:** Requires customer transaction history, recency, frequency
**Check:** Does `customer_profile_export.xlsx` exist with RFM metrics?
**If NO:** Recommend creating `customer_profile` model with recency calculations
**If YES:** Segment customers by recency/frequency, identify at-risk

### "When should I hire more staff?"
**Assessment:** Requires hourly transaction patterns, day-of-week patterns
**Check:** Does `daily_hour_export.xlsx` exist?
**If YES:** Analyze peak hours and days for staffing recommendations

### "Forecast next month's revenue"
**Assessment:** Requires historical daily/weekly revenue, trend analysis
**Check:** At least 3 months of historical data in `daily_export.xlsx`?
**If YES:** Use time series techniques for basic forecasting

## Remember

- **Create insights, not features** - Use **architect** skill for model development
- **Always validate data first** - Don't analyze garbage data
- **Business language** - Speak in revenue, savings, efficiency
- **Visual + Textual** - Combine charts with written recommendations
- **Actionable** - Every insight needs a "what to do about it"
- **Identify gaps** - Tell users what's missing and how to add it
- **Use examples** - Show actual code, not just descriptions
- **Think executive** - What would a CEO want to know?

## Version History

**v2.0.0** (2025-10-30)
- Refactored to use progressive disclosure pattern
- Extracted detailed content to `references/` (6 files) and `assets/templates/` (1 file)
- Converted to imperative form (removed second-person voice)
- Reduced from 587 lines to ~295 lines
- Added clear workflow sections
- Enhanced data gap identification process

**v1.0.0** (2025-10-28)
- Initial version with comprehensive insights guidance

---

**Last Updated:** 2025-10-30
**Core Focus:** Transform data into actionable business intelligence
**Key Principle:** Every insight must have a specific, actionable recommendation
