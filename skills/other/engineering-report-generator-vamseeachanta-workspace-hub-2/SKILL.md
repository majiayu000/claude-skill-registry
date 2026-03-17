---
name: engineering-report-generator
description: Generate engineering analysis reports with interactive Plotly visualizations, standard report sections, and HTML export. Use for creating dashboards, analysis summaries, and technical documentation with charts.
version: 1.1.0
category: development
related_skills:
  - data-pipeline-processor
  - yaml-workflow-executor
  - parallel-file-processor
---

# Engineering Report Generator

> Version: 1.1.0
> Category: Development
> Last Updated: 2026-01-02

Generate professional engineering analysis reports with interactive visualizations using Plotly and responsive HTML export.

## Quick Start

```python
import plotly.express as px
import pandas as pd
from pathlib import Path
from datetime import datetime

# Load data
df = pd.read_csv("../data/processed/results.csv")

# Create visualization
fig = px.line(df, x="date", y="value", title="Analysis Results")

# Generate HTML report
html = f"""<!DOCTYPE html>
<html>
<head><title>Engineering Report</title></head>
<body>
<h1>Analysis Report - {datetime.now().strftime('%Y-%m-%d')}</h1>
{fig.to_html(full_html=False, include_plotlyjs="cdn")}
</body>
</html>"""

Path("../reports/analysis.html").write_text(html)
print("Report generated: reports/analysis.html")
```

## When to Use

- Creating analysis reports with charts and visualizations
- Building interactive dashboards from CSV/data sources
- Generating technical documentation with plots
- Producing client-deliverable HTML reports
- Summarizing engineering calculations with graphics

## Report Structure

### Standard Sections

1. **Header** - Title, date, project info, version
2. **Executive Summary** - Key findings and metrics at a glance
3. **Methodology** - Analysis approach and assumptions
4. **Results** - Data tables and interactive visualizations
5. **Discussion** - Interpretation of results
6. **Conclusions** - Summary and recommendations
7. **Appendix** - Supporting data, references

## Implementation Pattern

### Basic Report Generation

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path
from datetime import datetime

def generate_report(
    data_path: str,
    output_path: str,
    title: str,
    sections: dict
) -> str:
    """
    Generate HTML report with interactive visualizations.

    Args:
        data_path: Path to CSV data file (relative)
        output_path: Output HTML file path
        title: Report title
        sections: Dict of section content

    Returns:
        Path to generated report
    """
    # Load data
    df = pd.read_csv(data_path)

    # Create figures
    figures = create_visualizations(df, sections.get('charts', []))

    # Build HTML
    html = build_html_report(title, sections, figures)

    # Save
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)

    return output_path
```

### Visualization Patterns

```python
def create_visualizations(df: pd.DataFrame, chart_configs: list) -> list:
    """Create Plotly figures from configuration."""
    figures = []

    for config in chart_configs:
        chart_type = config.get('type', 'line')

        if chart_type == 'line':
            fig = px.line(
                df,
                x=config['x'],
                y=config['y'],
                color=config.get('color'),
                title=config.get('title', '')
            )
        elif chart_type == 'scatter':
            fig = px.scatter(
                df,
                x=config['x'],
                y=config['y'],
                color=config.get('color'),
                size=config.get('size'),
                title=config.get('title', '')
            )
        elif chart_type == 'bar':
            fig = px.bar(
                df,
                x=config['x'],
                y=config['y'],
                color=config.get('color'),
                title=config.get('title', '')
            )
        elif chart_type == 'heatmap':
            fig = px.imshow(
                df.pivot(
                    index=config['y'],
                    columns=config['x'],
                    values=config['values']
                ),
                title=config.get('title', '')
            )
        elif chart_type == 'polar':
            fig = px.line_polar(
                df,
                r=config['r'],
                theta=config['theta'],
                title=config.get('title', '')
            )

        # Apply standard styling
        fig.update_layout(
            template='plotly_white',
            font=dict(size=12),
            margin=dict(l=50, r=50, t=50, b=50)
        )

        figures.append(fig)

    return figures
```

### HTML Template

```python
def build_html_report(title: str, sections: dict, figures: list) -> str:
    """Build complete HTML report."""

    # Convert figures to HTML
    chart_html = '\n'.join([
        f'<div class="chart-container">{fig.to_html(full_html=False, include_plotlyjs="cdn")}</div>'
        for fig in figures
    ])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --background-color: #f5f6fa;
            --card-background: #ffffff;
            --text-color: #2c3e50;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: var(--background-color);
            color: var(--text-color);
            line-height: 1.6;
        }}

        .report-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .report-header h1 {{
            margin: 0 0 10px 0;
            font-size: 2em;
        }}

        .section {{
            background: var(--card-background);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .section h2 {{
            color: var(--primary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 10px;
            margin-top: 0;
        }}

        .chart-container {{
            margin: 20px 0;
        }}

        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}

        .metric-card {{
            background: var(--background-color);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}

        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: var(--secondary-color);
        }}

        .metric-label {{
            font-size: 0.9em;
            color: #666;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}

        th {{
            background: var(--primary-color);
            color: white;
        }}

        @media (max-width: 768px) {{
            body {{ padding: 10px; }}
            .report-header {{ padding: 20px; }}
            .section {{ padding: 15px; }}
        }}
    </style>
</head>
<body>
    <div class="report-header">
        <h1>{title}</h1>
        <div class="report-meta">
            <span>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</span>
            {f'<span> | Project: {sections.get("project", "")}</span>' if sections.get("project") else ''}
        </div>
    </div>

    {f'<div class="section"><h2>Executive Summary</h2>{sections.get("summary", "")}</div>' if sections.get("summary") else ''}

    {f'<div class="section"><h2>Methodology</h2>{sections.get("methodology", "")}</div>' if sections.get("methodology") else ''}

    <div class="section">
        <h2>Results</h2>
        {chart_html}
        {sections.get("results", "")}
    </div>

    {f'<div class="section"><h2>Discussion</h2>{sections.get("discussion", "")}</div>' if sections.get("discussion") else ''}

    {f'<div class="section"><h2>Conclusions</h2>{sections.get("conclusions", "")}</div>' if sections.get("conclusions") else ''}

    {f'<div class="section"><h2>Appendix</h2>{sections.get("appendix", "")}</div>' if sections.get("appendix") else ''}

    <footer style="text-align: center; padding: 20px; color: #666; font-size: 0.9em;">
        Report generated using Engineering Report Generator
    </footer>
</body>
</html>'''

    return html
```

## Usage Examples

### Example 1: Production Analysis Report

```python
# Configuration
report_config = {
    'title': 'Monthly Production Analysis',
    'project': 'Field A Development',
    'summary': '''
        <div class="summary-grid">
            <div class="metric-card">
                <div class="metric-value">125,000</div>
                <div class="metric-label">Total Oil (bbl)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">98.5%</div>
                <div class="metric-label">Uptime</div>
            </div>
        </div>
    ''',
    'charts': [
        {'type': 'line', 'x': 'date', 'y': 'production', 'title': 'Daily Production'},
        {'type': 'bar', 'x': 'well', 'y': 'cumulative', 'title': 'Well Performance'}
    ]
}

# Generate
generate_report(
    data_path='../data/processed/production.csv',
    output_path='../reports/production_report.html',
    **report_config
)
```

### Example 2: Structural Analysis Report

```python
report_config = {
    'title': 'Structural Analysis Results',
    'methodology': '<p>Analysis performed per DNV-RP-C201 using finite element method.</p>',
    'charts': [
        {'type': 'heatmap', 'x': 'x_coord', 'y': 'y_coord', 'values': 'stress', 'title': 'Stress Distribution'},
        {'type': 'scatter', 'x': 'load', 'y': 'displacement', 'title': 'Load-Displacement Curve'}
    ],
    'conclusions': '<p>All structural elements satisfy design criteria with safety factor > 1.5</p>'
}
```

### Example 3: Multi-Panel Dashboard

```python
from plotly.subplots import make_subplots

def create_dashboard(df: pd.DataFrame, output_path: str):
    """Create multi-panel analysis dashboard."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Trend', 'Distribution', 'Comparison', 'Correlation')
    )

    # Add traces to each panel
    fig.add_trace(go.Scatter(x=df['date'], y=df['value'], mode='lines'), row=1, col=1)
    fig.add_trace(go.Histogram(x=df['value']), row=1, col=2)
    fig.add_trace(go.Bar(x=df['category'], y=df['count']), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['x'], y=df['y'], mode='markers'), row=2, col=2)

    fig.update_layout(height=800, title_text="Analysis Dashboard")
    fig.write_html(output_path)

    return output_path
```

## Best Practices

### Do

1. Use relative paths from report location for data
2. Include interactive plots only (Plotly, Bokeh, Altair)
3. Apply consistent color schemes across charts
4. Add clear axis labels and titles
5. Include hover data for detailed values
6. Make reports responsive (mobile-friendly)

### Don't

1. Export static matplotlib PNG/SVG images
2. Use absolute file paths
3. Create overly complex visualizations
4. Skip executive summaries
5. Ignore accessibility (color contrast)

### Data Input
- Use relative paths from report location
- CSV files with clear column headers
- Data pre-processed and validated

### HTML Output
- Self-contained files (CDN for Plotly)
- Responsive design (mobile-friendly)
- Print-friendly styling
- Accessible color contrast

### File Organization
```
project/
    data/
        raw/           # Original data
        processed/     # Analysis-ready CSV
    reports/
        analysis.html  # Generated reports
    scripts/
        generate_report.py
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` | Data file missing | Verify data path is correct |
| `KeyError` | Column not in DataFrame | Check column names match config |
| `ValueError` | Data type mismatch | Convert types before plotting |
| `Empty figure` | No data after filtering | Validate data before visualization |

### Error Template

```python
def safe_generate_report(data_path: str, output_path: str, config: dict) -> dict:
    """Generate report with error handling."""
    try:
        # Validate data exists
        if not Path(data_path).exists():
            return {'status': 'error', 'message': f'Data file not found: {data_path}'}

        # Load and validate
        df = pd.read_csv(data_path)
        if df.empty:
            return {'status': 'error', 'message': 'Data file is empty'}

        # Generate report
        output = generate_report(data_path, output_path, **config)
        return {'status': 'success', 'output': output}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

## Execution Checklist

- [ ] Data file exists and is not empty
- [ ] Column names match chart configuration
- [ ] Output directory exists or is created
- [ ] All charts have titles and labels
- [ ] Report includes executive summary
- [ ] Plotly CDN included for interactivity
- [ ] Responsive design tested on mobile
- [ ] Color contrast meets accessibility standards
- [ ] Report file size is reasonable (<10MB)

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Generation Time | <5s | Report creation speed |
| File Size | <10MB | HTML report size |
| Load Time | <3s | Browser render time |
| Chart Count | 1-10 | Optimal visualization count |
| Mobile Score | >90 | Lighthouse mobile score |

## Integration

### With YAML Workflow
```yaml
task: generate_report
input:
  data_path: data/processed/results.csv
output:
  report_path: reports/analysis.html
config:
  title: "Analysis Report"
  charts:
    - type: line
      x: time
      y: value
```

### With Data Pipeline
```python
# Pipeline output -> Report input
pipeline_results = process_data(raw_data)
pipeline_results.to_csv('data/processed/results.csv')

generate_report(
    data_path='data/processed/results.csv',
    output_path='reports/analysis.html',
    title='Pipeline Results'
)
```

## Related Skills

- [xlsx](../../document-handling/xlsx/SKILL.md) - Excel data handling
- [pdf](../../document-handling/pdf/SKILL.md) - PDF report generation
- [data-pipeline-processor](../data-pipeline-processor/SKILL.md) - Data preparation
- [yaml-workflow-executor](../yaml-workflow-executor/SKILL.md) - Workflow automation

---

## Version History

- **1.1.0** (2026-01-02): Upgraded to SKILL_TEMPLATE_v2 format with Quick Start, Error Handling, Metrics, Execution Checklist, additional examples
- **1.0.0** (2024-10-15): Initial release with Plotly visualizations, HTML templates, responsive design
