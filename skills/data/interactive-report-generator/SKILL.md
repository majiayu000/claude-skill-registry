---
name: interactive-report-generator
description: Generate interactive HTML reports with Plotly visualizations from data analysis results. Supports dashboards, charts, and professional styling.
version: 1.0.0
category: workspace-hub
type: skill
trigger: manual
auto_execute: false
capabilities:
  - plotly_visualization
  - html_report_generation
  - dashboard_creation
  - csv_data_integration
  - responsive_design
tools:
  - Write
  - Read
  - Bash
related_skills:
  - data-validation-reporter
  - yaml-workflow-executor
---

# Interactive Report Generator

> Create professional, interactive HTML reports with Plotly visualizations.

## Quick Start

```bash
# Generate report from data
/interactive-report-generator --data results.csv --output report.html

# Create dashboard
/interactive-report-generator --type dashboard --config dashboard.yaml

# Generate from analysis results
/interactive-report-generator --source analysis_output/
```

## When to Use

**USE when:**
- Creating analysis reports
- Generating data visualizations
- Building dashboards
- Presenting results to stakeholders

**DON'T USE when:**
- Static images are required
- PDF export is primary format
- Real-time streaming data

## Prerequisites

- Python 3.9+
- plotly>=5.15.0
- pandas>=2.0.0
- Data in CSV/DataFrame format

## Overview

Generates interactive HTML reports compliant with workspace-hub HTML_REPORTING_STANDARDS.md:

1. **Interactive plots only** - No static matplotlib
2. **CSV data import** - Relative paths
3. **Responsive design** - Works on all devices
4. **Professional styling** - Consistent theming
5. **Export options** - PNG, SVG from plots

## Core Templates

### 1. Basic Report Template

```python
"""
ABOUTME: Interactive HTML report generator
ABOUTME: Creates Plotly-based reports from analysis data
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


def generate_report(
    data: pd.DataFrame,
    output_path: Path,
    title: str = "Analysis Report",
    config: Optional[Dict[str, Any]] = None
) -> Path:
    """
    Generate interactive HTML report from data.

    Args:
        data: DataFrame with analysis results
        output_path: Path to save HTML report
        title: Report title
        config: Optional configuration dictionary

    Returns:
        Path to generated report
    """
    config = config or {}

    # Create HTML structure
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        .report-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .report-header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .report-header .metadata {{
            opacity: 0.9;
            font-size: 0.9em;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .card .label {{
            font-size: 0.85em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .plot-container {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .plot-container h2 {{
            margin-bottom: 20px;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: #666;
            font-size: 0.85em;
        }}
        @media (max-width: 768px) {{
            .report-header h1 {{
                font-size: 1.8em;
            }}
            .card .value {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-header">
        <h1>{title}</h1>
        <div class="metadata">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
            Records: {len(data):,}
        </div>
    </div>

    <div class="container">
        <!-- Summary Cards -->
        <div class="summary-cards" id="summary-cards">
            <!-- Generated by JavaScript -->
        </div>

        <!-- Plots -->
        <div id="plots-container">
            <!-- Generated dynamically -->
        </div>
    </div>

    <div class="footer">
        Generated with Interactive Report Generator | workspace-hub
    </div>
</body>
</html>
"""

    # Write HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content)

    return output_path


def create_time_series_plot(
    data: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = "Time Series"
) -> go.Figure:
    """
    Create interactive time series plot.

    Args:
        data: DataFrame with time series data
        x_col: Column for x-axis (typically datetime)
        y_cols: Columns for y-axis values
        title: Plot title

    Returns:
        Plotly Figure object
    """
    fig = go.Figure()

    for col in y_cols:
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[col],
            mode='lines+markers',
            name=col,
            hovertemplate='%{x}<br>%{y:.2f}<extra></extra>'
        ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title="Value",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )

    return fig


def create_distribution_plot(
    data: pd.DataFrame,
    column: str,
    title: str = "Distribution"
) -> go.Figure:
    """
    Create interactive histogram/distribution plot.

    Args:
        data: DataFrame with data
        column: Column to plot distribution
        title: Plot title

    Returns:
        Plotly Figure object
    """
    fig = px.histogram(
        data,
        x=column,
        title=title,
        template='plotly_white',
        nbins=50
    )

    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count",
        height=400
    )

    return fig


def create_correlation_heatmap(
    data: pd.DataFrame,
    columns: Optional[List[str]] = None,
    title: str = "Correlation Matrix"
) -> go.Figure:
    """
    Create interactive correlation heatmap.

    Args:
        data: DataFrame with numeric data
        columns: Optional list of columns to include
        title: Plot title

    Returns:
        Plotly Figure object
    """
    if columns:
        corr_data = data[columns].corr()
    else:
        corr_data = data.select_dtypes(include='number').corr()

    fig = px.imshow(
        corr_data,
        title=title,
        template='plotly_white',
        color_continuous_scale='RdBu_r',
        zmin=-1,
        zmax=1
    )

    fig.update_layout(height=500)

    return fig


def create_dashboard(
    data: pd.DataFrame,
    output_path: Path,
    config: Dict[str, Any]
) -> Path:
    """
    Create multi-panel dashboard.

    Args:
        data: DataFrame with analysis data
        output_path: Path to save dashboard HTML
        config: Dashboard configuration

    Returns:
        Path to generated dashboard
    """
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Time Series",
            "Distribution",
            "Scatter Plot",
            "Summary Statistics"
        ),
        specs=[
            [{"type": "scatter"}, {"type": "histogram"}],
            [{"type": "scatter"}, {"type": "table"}]
        ]
    )

    # Add plots based on config
    numeric_cols = data.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) >= 2:
        # Time series or line plot
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[numeric_cols[0]],
                mode='lines',
                name=numeric_cols[0]
            ),
            row=1, col=1
        )

        # Distribution
        fig.add_trace(
            go.Histogram(x=data[numeric_cols[0]], name="Distribution"),
            row=1, col=2
        )

        # Scatter
        fig.add_trace(
            go.Scatter(
                x=data[numeric_cols[0]],
                y=data[numeric_cols[1]],
                mode='markers',
                name="Correlation"
            ),
            row=2, col=1
        )

    # Summary statistics table
    stats = data.describe().reset_index()
    fig.add_trace(
        go.Table(
            header=dict(values=list(stats.columns)),
            cells=dict(values=[stats[col].round(2) for col in stats.columns])
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Analysis Dashboard"
    )

    # Save
    fig.write_html(output_path, include_plotlyjs='cdn')

    return output_path
```

### 2. Report Generator Class

```python
"""
ABOUTME: Full-featured report generator class
ABOUTME: Supports multiple plot types and configurations
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class InteractiveReportGenerator:
    """Generate interactive HTML reports with Plotly."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize report generator.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.plots: List[go.Figure] = []
        self.summary_stats: Dict[str, Any] = {}

        # Default styling
        self.theme = self.config.get('theme', {
            'primary_color': '#667eea',
            'secondary_color': '#764ba2',
            'background': '#f5f5f5',
            'card_bg': '#ffffff',
            'text_color': '#333333'
        })

    def add_data(self, data: pd.DataFrame, name: str = "data"):
        """Add data source to report."""
        self.data = data
        self.data_name = name
        self._calculate_summary()

    def _calculate_summary(self):
        """Calculate summary statistics."""
        if hasattr(self, 'data'):
            self.summary_stats = {
                'total_records': len(self.data),
                'columns': len(self.data.columns),
                'numeric_cols': len(self.data.select_dtypes(include='number').columns),
                'missing_values': self.data.isnull().sum().sum()
            }

    def add_time_series(
        self,
        x_col: str,
        y_cols: List[str],
        title: str = "Time Series Analysis"
    ):
        """Add time series plot."""
        fig = go.Figure()

        for col in y_cols:
            fig.add_trace(go.Scatter(
                x=self.data[x_col],
                y=self.data[col],
                mode='lines+markers',
                name=col
            ))

        fig.update_layout(
            title=title,
            template='plotly_white',
            height=500
        )

        self.plots.append(('time_series', fig, title))

    def add_bar_chart(
        self,
        x_col: str,
        y_col: str,
        title: str = "Bar Chart"
    ):
        """Add bar chart."""
        fig = px.bar(
            self.data,
            x=x_col,
            y=y_col,
            title=title,
            template='plotly_white'
        )

        self.plots.append(('bar', fig, title))

    def add_scatter_plot(
        self,
        x_col: str,
        y_col: str,
        color_col: Optional[str] = None,
        title: str = "Scatter Plot"
    ):
        """Add scatter plot."""
        fig = px.scatter(
            self.data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            template='plotly_white'
        )

        self.plots.append(('scatter', fig, title))

    def add_histogram(
        self,
        column: str,
        title: str = "Distribution"
    ):
        """Add histogram."""
        fig = px.histogram(
            self.data,
            x=column,
            title=title,
            template='plotly_white'
        )

        self.plots.append(('histogram', fig, title))

    def add_heatmap(
        self,
        columns: Optional[List[str]] = None,
        title: str = "Correlation Heatmap"
    ):
        """Add correlation heatmap."""
        if columns:
            corr = self.data[columns].corr()
        else:
            corr = self.data.select_dtypes(include='number').corr()

        fig = px.imshow(
            corr,
            title=title,
            template='plotly_white',
            color_continuous_scale='RdBu_r'
        )

        self.plots.append(('heatmap', fig, title))

    def generate(
        self,
        output_path: Path,
        title: str = "Analysis Report"
    ) -> Path:
        """
        Generate the HTML report.

        Args:
            output_path: Path to save report
            title: Report title

        Returns:
            Path to generated report
        """
        # Build HTML
        html_parts = [self._generate_header(title)]
        html_parts.append(self._generate_summary_cards())

        for plot_type, fig, plot_title in self.plots:
            html_parts.append(self._wrap_plot(fig, plot_title))

        html_parts.append(self._generate_footer())

        # Combine and save
        html_content = self._get_html_template(
            title,
            '\n'.join(html_parts)
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content)

        return output_path

    def _get_html_template(self, title: str, body: str) -> str:
        """Get complete HTML template."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        {self._get_styles()}
    </style>
</head>
<body>
    {body}
</body>
</html>"""

    def _get_styles(self) -> str:
        """Get CSS styles."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }
        .card { background: white; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
        .card-value { font-size: 2.5em; font-weight: bold; color: #667eea; }
        .card-label { color: #666; text-transform: uppercase; font-size: 0.85em; }
        .plot-section { background: white; border-radius: 12px; padding: 25px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .footer { text-align: center; padding: 30px; color: #666; }
        """

    def _generate_header(self, title: str) -> str:
        """Generate header HTML."""
        return f"""
        <div class="header">
            <h1>{title}</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        <div class="container">
        """

    def _generate_summary_cards(self) -> str:
        """Generate summary cards HTML."""
        cards = ""
        for key, value in self.summary_stats.items():
            label = key.replace('_', ' ').title()
            cards += f"""
            <div class="card">
                <div class="card-value">{value:,}</div>
                <div class="card-label">{label}</div>
            </div>
            """

        return f'<div class="cards">{cards}</div>'

    def _wrap_plot(self, fig: go.Figure, title: str) -> str:
        """Wrap plot in HTML container."""
        plot_html = fig.to_html(full_html=False, include_plotlyjs=False)
        return f"""
        <div class="plot-section">
            <h2>{title}</h2>
            {plot_html}
        </div>
        """

    def _generate_footer(self) -> str:
        """Generate footer HTML."""
        return """
        </div>
        <div class="footer">
            Generated with Interactive Report Generator | workspace-hub
        </div>
        """
```

## Usage Examples

### Example 1: Simple Report

```python
import pandas as pd
from pathlib import Path
from report_generator import InteractiveReportGenerator

# Load data
df = pd.read_csv('data/analysis_results.csv')

# Create report
report = InteractiveReportGenerator()
report.add_data(df)
report.add_time_series('date', ['value1', 'value2'])
report.add_histogram('value1')
report.add_heatmap()

# Generate
output = report.generate(
    Path('reports/analysis_report.html'),
    title='Analysis Results'
)
print(f"Report saved: {output}")
```

### Example 2: Dashboard Creation

```python
# Create dashboard with multiple views
report = InteractiveReportGenerator()
report.add_data(df)

# Add various plots
report.add_time_series('timestamp', ['metric_a', 'metric_b'])
report.add_scatter_plot('x_value', 'y_value', color_col='category')
report.add_bar_chart('category', 'total')
report.add_histogram('distribution_col')

# Generate dashboard
report.generate(
    Path('reports/dashboard.html'),
    title='Project Dashboard'
)
```

### Example 3: From CLI

```bash
# Generate report from command line
python -m report_generator \
    --data results.csv \
    --output report.html \
    --title "Analysis Results" \
    --plots time_series histogram heatmap
```

## Execution Checklist

**Data Preparation:**
- [ ] Data loaded as DataFrame
- [ ] Column names are clean
- [ ] Date columns parsed
- [ ] Missing values handled

**Report Creation:**
- [ ] Add data to generator
- [ ] Select appropriate plot types
- [ ] Configure titles and labels
- [ ] Generate HTML output

**Validation:**
- [ ] Open report in browser
- [ ] Verify interactivity works
- [ ] Check responsive design
- [ ] Test export options

## Best Practices

1. **Use descriptive titles** - Help users understand each visualization
2. **Limit plots per page** - 5-7 plots maximum for clarity
3. **Use consistent colors** - Match organizational branding
4. **Include summary stats** - Provide context for data
5. **Test on mobile** - Verify responsive design works

## Error Handling

### Missing Columns
```
Error: Column 'value' not found in data

Check:
1. Column names in DataFrame
2. Spelling and case sensitivity
3. Data was loaded correctly
```

### Empty Data
```
Error: No data to plot

Check:
1. DataFrame is not empty
2. Filters not too restrictive
3. Data loading succeeded
```

## Related Skills

- [data-validation-reporter](../data-validation-reporter/SKILL.md) - Data quality reports
- [yaml-workflow-executor](../yaml-workflow-executor/SKILL.md) - Configuration-driven reports

## References

- [Plotly Python Documentation](https://plotly.com/python/)
- [HTML Reporting Standards](../../../docs/modules/standards/HTML_REPORTING_STANDARDS.md)

---

## Version History

- **1.0.0** (2026-01-14): Initial release - Plotly-based interactive HTML report generator with dashboards, multiple plot types, and responsive design
