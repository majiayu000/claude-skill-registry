---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: report-generator
description: "Generate professional data reports with charts, tables, and visualizations"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: presentation
tags:
  - report
  - generator
  - data
  - visualization
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
    - create_docx
    - create_xlsx
    - create_chart
    - create_pptx

# Skill Capabilities
capabilities:
  - report_generation
  - data_visualization

# Language Support
languages:
  - en
  - zh
---

# Report Generator Skill

## Overview

This skill enables automatic generation of professional data reports. Create dashboards, KPI summaries, and analytical reports with charts, tables, and insights from your data.

## How to Use

1. Provide data (CSV, Excel, JSON, or describe it)
2. Specify the type of report needed
3. I'll generate a formatted report with visualizations

**Example prompts:**
- "Generate a sales report from this data"
- "Create a monthly KPI dashboard"
- "Build an executive summary with charts"
- "Produce a data analysis report"

## Domain Knowledge

### Report Components

```python
# Report structure
report = {
    'title': 'Monthly Sales Report',
    'period': 'January 2024',
    'sections': [
        'executive_summary',
        'kpi_dashboard',
        'detailed_analysis',
        'charts',
        'recommendations'
    ]
}
```

### Using Python for Reports

```python
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(data, output_path):
    # Load data
    df = pd.read_csv(data)
    
    # Calculate KPIs
    total_revenue = df['revenue'].sum()
    avg_order = df['revenue'].mean()
    growth = df['revenue'].pct_change().mean()
    
    # Create charts
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    df.plot(kind='bar', ax=axes[0,0], title='Revenue by Month')
    df.plot(kind='line', ax=axes[0,1], title='Trend')
    plt.savefig('charts.png')
    
    # Generate PDF
    # ... PDF generation code
    
    return output_path
```

### HTML Report Template

```python
def generate_html_report(data, title):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            .kpi {{ display: flex; gap: 20px; }}
            .kpi-card {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
            .metric {{ font-size: 2em; font-weight: bold; color: #2563eb; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="kpi">
            <div class="kpi-card">
                <div class="metric">${data['revenue']:,.0f}</div>
                <div>Total Revenue</div>
            </div>
            <div class="kpi-card">
                <div class="metric">{data['growth']:.1%}</div>
                <div>Growth Rate</div>
            </div>
        </div>
        <!-- More content -->
    </body>
    </html>
    '''
    return html
```

## Example: Sales Report

```python
import pandas as pd
import matplotlib.pyplot as plt

def create_sales_report(csv_path, output_path):
    # Read data
    df = pd.read_csv(csv_path)
    
    # Calculate metrics
    metrics = {
        'total_revenue': df['amount'].sum(),
        'total_orders': len(df),
        'avg_order': df['amount'].mean(),
        'top_product': df.groupby('product')['amount'].sum().idxmax()
    }
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Revenue by product
    df.groupby('product')['amount'].sum().plot(
        kind='bar', ax=axes[0,0], title='Revenue by Product'
    )
    
    # Monthly trend
    df.groupby('month')['amount'].sum().plot(
        kind='line', ax=axes[0,1], title='Monthly Revenue'
    )
    
    plt.tight_layout()
    plt.savefig(output_path.replace('.html', '_charts.png'))
    
    # Generate HTML report
    html = generate_html_report(metrics, 'Sales Report')
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    return output_path

create_sales_report('sales_data.csv', 'sales_report.html')
```

## Resources

- [Matplotlib](https://matplotlib.org/)
- [Plotly](https://plotly.com/)
- [ReportLab](https://www.reportlab.com/)
