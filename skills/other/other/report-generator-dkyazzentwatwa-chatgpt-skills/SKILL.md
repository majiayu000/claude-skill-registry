---
name: report-generator
description: Generate professional PDF/HTML reports with charts, tables, and narrative from data. Supports templates, branding, and automated report generation.
---

# Report Generator

Create professional, data-driven reports with charts, tables, and narrative text. Perfect for business reports, analytics dashboards, status updates, and automated reporting pipelines.

## Quick Start

```python
from scripts.report_gen import ReportGenerator

# Create a simple report
report = ReportGenerator("Monthly Sales Report")
report.add_text("This report summarizes sales performance for Q4 2024.")
report.add_table(sales_data, title="Sales by Region")
report.add_chart(sales_data, chart_type="bar", title="Revenue by Month")
report.add_text("Key findings: Revenue increased 25% quarter-over-quarter.")
report.generate().save("sales_report.pdf")

# From template
report = ReportGenerator.from_template("executive_summary")
report.set_data(data_dict)
report.generate().save("exec_summary.pdf")
```

## Features

- **Multiple Output Formats**: PDF, HTML
- **Rich Content**: Text, tables, charts, images, headers
- **Chart Types**: Bar, line, pie, scatter, area, heatmap
- **Table Formatting**: Auto-styling, conditional formatting
- **Templates**: Pre-built report templates
- **Branding**: Logo, colors, fonts, headers/footers
- **Sections**: Table of contents, page numbers, appendices
- **Data Integration**: CSV, DataFrame, dict inputs

## API Reference

### Initialization

```python
# New report
report = ReportGenerator("Report Title")
report = ReportGenerator("Report Title", subtitle="Q4 2024 Analysis")

# From template
report = ReportGenerator.from_template("quarterly_review")

# With config
report = ReportGenerator("Title", config={
    "page_size": "letter",
    "orientation": "portrait",
    "margins": {"top": 1, "bottom": 1, "left": 0.75, "right": 0.75}
})
```

### Report Metadata

```python
# Title and subtitle
report.set_title("Annual Report 2024")
report.set_subtitle("Financial Performance Analysis")

# Author and date
report.set_author("Analytics Team")
report.set_date("December 2024")
report.set_date_auto()  # Use today

# Organization
report.set_organization("Acme Corporation")
report.set_logo("logo.png")
```

### Adding Content

#### Text Content

```python
# Simple paragraph
report.add_text("This is a paragraph of analysis text.")

# Styled text
report.add_text("Important finding!", style="highlight")
report.add_text("Key metric: 42%", style="metric")

# Headers
report.add_heading("Executive Summary", level=1)
report.add_heading("Revenue Analysis", level=2)
report.add_heading("By Region", level=3)

# Bullet points
report.add_bullets([
    "Revenue increased 25% YoY",
    "Customer acquisition up 15%",
    "Churn rate decreased to 3%"
])

# Numbered list
report.add_numbered_list([
    "Expand to European markets",
    "Launch mobile application",
    "Implement AI-driven analytics"
])
```

#### Tables

```python
# From DataFrame
import pandas as pd
df = pd.DataFrame({
    'Region': ['North', 'South', 'East', 'West'],
    'Revenue': [100000, 85000, 92000, 78000],
    'Growth': ['12%', '8%', '15%', '5%']
})
report.add_table(df, title="Regional Performance")

# From dict/list
data = [
    {'Product': 'A', 'Sales': 1000, 'Profit': 200},
    {'Product': 'B', 'Sales': 1500, 'Profit': 350}
]
report.add_table(data, title="Product Summary")

# With styling
report.add_table(df, title="Sales Data",
    highlight_max=['Revenue'],       # Highlight max values
    highlight_min=['Growth'],        # Highlight min values
    currency_cols=['Revenue'],       # Format as currency
    percent_cols=['Growth'],         # Format as percent
    align={'Region': 'left', 'Revenue': 'right'}
)
```

#### Charts

```python
# Bar chart
report.add_chart(
    data=df,
    chart_type="bar",
    x="Region",
    y="Revenue",
    title="Revenue by Region"
)

# Line chart
report.add_chart(
    data=time_series_df,
    chart_type="line",
    x="Month",
    y=["Sales", "Forecast"],
    title="Sales Trend"
)

# Pie chart
report.add_chart(
    data=category_df,
    chart_type="pie",
    values="Amount",
    labels="Category",
    title="Budget Allocation"
)

# Chart options
report.add_chart(
    data=df,
    chart_type="bar",
    x="Region",
    y="Revenue",
    title="Revenue Analysis",
    color="#3498db",
    width=6,           # inches
    height=4,
    show_values=True,
    show_legend=True
)
```

#### Images

```python
# Add image
report.add_image("screenshot.png", caption="Dashboard View")
report.add_image("diagram.png", width=5, caption="Architecture Diagram")
```

#### Special Elements

```python
# Page break
report.add_page_break()

# Horizontal line
report.add_divider()

# Spacer
report.add_spacer(height=0.5)  # inches

# Callout box
report.add_callout(
    "Key Insight: Customer retention improved 20% after implementing the new onboarding flow.",
    style="info"  # info, warning, success, error
)

# Quote
report.add_quote(
    "Data is the new oil.",
    attribution="Clive Humby"
)
```

### Sections and Structure

```python
# Start a new section
report.start_section("Financial Analysis")

# Add content to section
report.add_text("...")
report.add_table(...)

# End section
report.end_section()

# Table of contents (auto-generated)
report.enable_toc()

# Appendix
report.start_appendix()
report.add_heading("Raw Data", level=2)
report.add_table(raw_data)
```

### Branding and Styling

```python
# Logo and organization
report.set_logo("logo.png", width=150)
report.set_organization("Acme Corp")

# Colors
report.set_colors(
    primary="#1e40af",      # Headers, accents
    secondary="#6b7280",    # Secondary text
    background="#ffffff"    # Background
)

# Fonts
report.set_fonts(
    heading="Helvetica-Bold",
    body="Helvetica"
)

# Header and footer
report.set_header("Confidential - Internal Use Only")
report.set_footer("Page {page} of {total}")

# Watermark
report.set_watermark("DRAFT")
```

### Templates

```python
# Available templates
report = ReportGenerator.from_template("executive_summary")
report = ReportGenerator.from_template("quarterly_review")
report = ReportGenerator.from_template("project_status")
report = ReportGenerator.from_template("analytics_dashboard")

# Template with data
report = ReportGenerator.from_template("monthly_metrics")
report.set_data({
    "period": "December 2024",
    "revenue": 1500000,
    "growth": 0.15,
    "customers": 5000,
    "charts": {"revenue_trend": trend_df}
})
report.generate()
```

### Generation and Export

```python
# Generate report
report.generate()

# Save as PDF
report.save("report.pdf")

# Save as HTML
report.save("report.html")

# Get bytes
pdf_bytes = report.to_bytes()
html_string = report.to_html()
```

## Templates

### Executive Summary
- Title page
- Key metrics highlights
- Summary bullets
- Charts section
- Recommendations

### Quarterly Review
- Performance overview
- Financial metrics
- Comparison to previous quarter
- Goals progress
- Next quarter outlook

### Project Status
- Project overview
- Timeline/milestones
- Risks and issues
- Team updates
- Next steps

### Analytics Dashboard
- KPI cards
- Multiple charts
- Trend analysis
- Data tables
- Insights

## CLI Usage

```bash
# Generate from JSON config
python report_gen.py --config report_config.json --output report.pdf

# With template
python report_gen.py --template executive_summary --data data.json --output summary.pdf

# Quick report from CSV
python report_gen.py --csv data.csv --title "Data Report" --output report.pdf
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--config` | Report configuration JSON | - |
| `--template` | Template name | - |
| `--data` | Data JSON file | - |
| `--csv` | CSV data file | - |
| `--title` | Report title | `Report` |
| `--output` | Output file path | `report.pdf` |
| `--format` | Output format (pdf/html) | `pdf` |

## Examples

### Sales Report

```python
report = ReportGenerator("Q4 Sales Report")
report.set_subtitle("October - December 2024")
report.set_organization("Sales Department")
report.set_logo("company_logo.png")

report.add_heading("Executive Summary", level=1)
report.add_text(
    "Q4 2024 showed strong performance across all regions, "
    "with total revenue reaching $4.2M, a 23% increase over Q3."
)

report.add_callout(
    "Total Revenue: $4.2M (+23% QoQ)",
    style="success"
)

report.add_heading("Regional Performance", level=2)
report.add_chart(regional_data, "bar", x="Region", y="Revenue",
                 title="Revenue by Region")
report.add_table(regional_data, title="Detailed Metrics")

report.add_heading("Trends", level=2)
report.add_chart(monthly_data, "line", x="Month", y="Revenue",
                 title="Monthly Revenue Trend")

report.add_heading("Recommendations", level=1)
report.add_bullets([
    "Increase investment in high-growth East region",
    "Address declining West region performance",
    "Launch Q1 promotional campaign"
])

report.generate().save("q4_sales_report.pdf")
```

### Analytics Dashboard

```python
report = ReportGenerator("Marketing Analytics")
report.set_date_auto()

# KPI Summary
report.add_heading("Key Metrics", level=1)
kpis = [
    ["Visitors", "125,000", "+15%"],
    ["Conversions", "3,750", "+22%"],
    ["Revenue", "$187,500", "+18%"],
    ["CAC", "$45", "-8%"]
]
report.add_table(kpis, headers=["Metric", "Value", "Change"])

# Traffic Sources
report.add_heading("Traffic Sources", level=2)
report.add_chart(traffic_df, "pie", values="Sessions", labels="Source",
                 title="Traffic Distribution")

# Conversion Funnel
report.add_heading("Conversion Funnel", level=2)
report.add_chart(funnel_df, "bar", x="Stage", y="Users",
                 title="Funnel Analysis", horizontal=True)

# Trend Analysis
report.add_heading("Trends", level=2)
report.add_chart(daily_df, "line", x="Date", y=["Visitors", "Conversions"],
                 title="Daily Performance")

report.generate().save("marketing_dashboard.pdf")
```

## Dependencies

```
reportlab>=4.0.0
Pillow>=10.0.0
pandas>=2.0.0
matplotlib>=3.7.0
```

## Limitations

- Charts rendered as static images in PDF
- Complex layouts may need manual adjustment
- Large datasets may impact performance
- HTML output has basic styling (no interactive charts)
