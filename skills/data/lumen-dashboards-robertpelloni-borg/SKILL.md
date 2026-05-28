---
name: lumen-dashboards
description: Master declarative, no-code data dashboards with Lumen YAML specifications. Use this skill when building standard data exploration dashboards, connecting multiple data sources (files, databases, APIs), creating interactive filters and cross-filtering, designing responsive layouts with indicators and charts, or enabling rapid dashboard prototyping without writing code.
version: 2025-01-07
compatibility: Requires lumen >= 0.10.0, panel >= 1.3.0, holoviews >= 1.18.0, param >= 2.0.0. Supports PostgreSQL, DuckDB, SQLite, CSV, Parquet, Excel, and REST API data sources.
---

# Lumen Dashboards Skill

## Overview

Lumen is a declarative framework for creating data dashboards through YAML specifications. Build interactive data exploration dashboards without writing code - just configuration.

### What is Lumen?

Lumen provides a declarative approach to building data dashboards:

- **No-code dashboards**: Define everything in YAML
- **Data pipelines**: Sources → Transforms → Views
- **Interactive exploration**: Built-in filters and cross-filtering
- **Component library**: Reusable sources, transforms, views
- **Live updates**: Auto-reload and real-time data

### Lumen vs Panel vs Lumen AI

| Feature | Lumen Dashboards | Panel | Lumen AI |
|---------|------------------|-------|----------|
| **Approach** | Declarative YAML | Imperative Python | Conversational |
| **Code Required** | No | Yes | No |
| **Use Case** | Fixed dashboards | Custom apps | Ad-hoc exploration |
| **Flexibility** | Medium | High | High |
| **Development Speed** | Very fast | Medium | Very fast |

**Use Lumen when**:
- Building standard data exploration dashboards
- Working with non-programmers
- Want rapid prototyping with configuration
- Need reproducible dashboard specifications

**Use Panel when**:
- Need fine-grained control over components
- Building custom application logic
- Creating novel interactions

**Use Lumen AI when**:
- Users need ad-hoc exploration
- Questions vary unpredictably
- Enabling self-service analytics

## Quick Start

### Installation

```bash
pip install lumen
```

### Your First Dashboard

**File: `dashboard.yaml`**

```yaml
sources:
  data:
    type: file
    tables:
      penguins: https://datasets.holoviz.org/penguins/v1/penguins.csv

pipelines:
  main:
    source: data
    table: penguins

    filters:
      - type: widget
        field: species

layouts:
  - title: Penguin Explorer
    views:
      - type: hvplot
        pipeline: main
        kind: scatter
        x: bill_length_mm
        y: bill_depth_mm
        by: species
        title: Bill Dimensions
```

**Launch:**
```bash
lumen serve dashboard.yaml --show
```

## Core Concepts

### 1. Sources

Data sources provide tables for your dashboard.

**Supported sources**:
- **File**: CSV, Parquet, Excel, JSON
- **Database**: PostgreSQL, DuckDB, SQLite
- **REST API**: JSON endpoints
- **Intake**: Data catalogs

**Quick example**:
```yaml
sources:
  mydata:
    type: file
    tables:
      sales: ./data/sales.csv
```

**See**: [Data Sources Reference](../../references/lumen-dashboards/sources.md) for comprehensive source configuration.

### 2. Pipelines

Pipelines define data flows: Source → Filters → Transforms → Views

**Basic pipeline**:
```yaml
pipelines:
  sales_pipeline:
    source: mydata
    table: sales

    filters:
      - type: widget
        field: region

    transforms:
      - type: aggregate
        by: ['category']
        aggregate:
          total_sales: {revenue: sum}
```

**Components**:
- **Filters**: Interactive widgets for user input
- **Transforms**: Data manipulation (filter, aggregate, sort, SQL)
- **Views**: Visualizations and tables

### 3. Filters

Add interactive controls:

```yaml
filters:
  # Dropdown select
  - type: widget
    field: category

  # Multi-select
  - type: widget
    field: region
    multiple: true

  # Date range
  - type: widget
    field: date
    widget: date_range_slider

  # Numeric slider
  - type: param
    parameter: min_revenue
    widget_type: FloatSlider
    start: 0
    end: 100000
```

### 4. Transforms

Process data in pipelines:

**Common transforms**:
- `columns`: Select specific columns
- `query`: Filter rows with pandas query
- `aggregate`: Group and aggregate
- `sort`: Sort data
- `sql`: Custom SQL queries

**Example**:
```yaml
transforms:
  - type: columns
    columns: ['date', 'region', 'revenue']

  - type: query
    query: "revenue > 1000"

  - type: aggregate
    by: ['region']
    aggregate:
      total: {revenue: sum}
      avg: {revenue: mean}
```

**See**: [Data Transforms Reference](../../references/lumen-dashboards/transforms.md) for all transform types.

### 5. Views

Visualize data:

**View types**:
- `hvplot`: Interactive plots (line, scatter, bar, etc.)
- `table`: Data tables
- `indicator`: KPI metrics
- `vega`: Vega-Lite specifications
- `altair`: Altair charts
- `plotly`: Plotly charts

**Example**:
```yaml
views:
  - type: hvplot
    pipeline: main
    kind: line
    x: date
    y: revenue
    by: category

  - type: indicator
    pipeline: main
    field: total_revenue
    title: Total Sales
    format: '${value:,.0f}'
```

**See**: [Views Reference](../../references/lumen-dashboards/views.md) for all view types and options.

### 6. Layouts

Arrange views on the page:

```yaml
layouts:
  - title: Overview
    layout: [[0, 1, 2], [3], [4, 5]]  # Grid positions
    views:
      - type: indicator
        # View 0 config...

      - type: indicator
        # View 1 config...

      - type: hvplot
        # View 2 config...
```

**Layout types**:
- **Grid**: `[[0, 1], [2, 3]]`
- **Tabs**: Multiple layouts become tabs
- **Responsive**: Adapts to screen size

**See**: [Layouts Reference](../../references/lumen-dashboards/layouts.md) for advanced layout patterns.

## Common Patterns

### Pattern 1: KPI Dashboard

```yaml
sources:
  metrics:
    type: file
    tables:
      data: ./metrics.csv

pipelines:
  kpis:
    source: metrics
    table: data
    transforms:
      - type: aggregate
        aggregate:
          total_revenue: {revenue: sum}
          total_orders: {orders: sum}
          avg_order_value: {revenue: mean}

layouts:
  - title: KPIs
    layout: [[0, 1, 2]]
    views:
      - type: indicator
        pipeline: kpis
        field: total_revenue
        format: '${value:,.0f}'

      - type: indicator
        pipeline: kpis
        field: total_orders
        format: '{value:,.0f}'

      - type: indicator
        pipeline: kpis
        field: avg_order_value
        format: '${value:.2f}'
```

### Pattern 2: Filtered Exploration

```yaml
pipelines:
  explorer:
    source: mydata
    table: sales

    filters:
      - type: widget
        field: region
        label: Region

      - type: widget
        field: category
        label: Category
        multiple: true

      - type: widget
        field: date
        widget: date_range_slider

    views:
      - type: hvplot
        kind: scatter
        x: price
        y: quantity
        by: category

      - type: table
        page_size: 20
```

### Pattern 3: Multi-Source Dashboard

```yaml
sources:
  sales_db:
    type: postgres
    connection_string: postgresql://localhost/sales
    tables: [orders, customers]

  inventory_file:
    type: file
    tables:
      stock: ./inventory.csv

pipelines:
  sales_pipeline:
    source: sales_db
    table: orders

  inventory_pipeline:
    source: inventory_file
    table: stock
```

### Pattern 4: Cross-Filtering

```yaml
pipelines:
  main:
    source: data
    table: sales

    filters:
      - type: widget
        field: region

layouts:
  - title: Analysis
    views:
      # Clicking bar filters other views
      - type: hvplot
        pipeline: main
        kind: bar
        x: category
        y: revenue
        selection_group: category_filter

      # Responds to selection above
      - type: hvplot
        pipeline: main
        kind: scatter
        x: price
        y: quantity
        selection_group: category_filter
```

### Pattern 5: SQL Transform

```yaml
transforms:
  - type: sql
    query: |
      SELECT
        region,
        category,
        SUM(revenue) as total_revenue,
        COUNT(*) as order_count,
        AVG(revenue) as avg_order_value
      FROM table
      WHERE date >= '2024-01-01'
      GROUP BY region, category
      HAVING total_revenue > 10000
      ORDER BY total_revenue DESC
```

## Python API

While Lumen is designed for YAML, you can also use Python:

```python
from lumen.sources import FileSource
from lumen.pipeline import Pipeline
from lumen.views import hvPlotView
from lumen.dashboard import Dashboard
import panel as pn

# Create source
source = FileSource(tables={'sales': './data/sales.csv'})

# Create pipeline
pipeline = Pipeline(source=source, table='sales')

# Create view
view = hvPlotView(
    pipeline=pipeline,
    kind='scatter',
    x='price',
    y='quantity'
)

# Create dashboard
dashboard = Dashboard(
    pipelines={'main': pipeline},
    layouts=[view]
)

# Serve
dashboard.servable()
```

**See**: [Python API Reference](../../references/lumen-dashboards/python-api.md) for detailed API usage.

## Configuration

### Global Config

```yaml
config:
  title: My Dashboard
  theme: dark  # or 'default', 'material'
  sizing_mode: stretch_width
  logo: ./logo.png
  favicon: ./favicon.ico
  layout: column  # or 'grid', 'tabs'
```

### Themes

```yaml
config:
  theme: material
  theme_json:
    palette:
      primary: '#00aa41'
      secondary: '#616161'
```

### Authentication

```bash
# Serve with auth
lumen serve dashboard.yaml \
  --oauth-provider=generic \
  --oauth-key=${OAUTH_KEY} \
  --oauth-secret=${OAUTH_SECRET}
```

## Deployment

### Development

```bash
# Local with auto-reload
lumen serve dashboard.yaml --autoreload --show

# Specific port
lumen serve dashboard.yaml --port 5007
```

### Production

```bash
# Production server
panel serve dashboard.yaml \
  --port 80 \
  --num-procs 4 \
  --allow-websocket-origin=analytics.company.com
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY dashboard.yaml data/ ./
CMD ["lumen", "serve", "dashboard.yaml", "--port", "5006", "--address", "0.0.0.0"]
```

**See**: [Deployment Guide](../../references/lumen-dashboards/deployment.md) for production deployment best practices.

## Best Practices

### 1. Source Organization

```yaml
# ✅ Good: Descriptive names
sources:
  sales_database:
    type: postgres
    tables: [orders, customers]

  inventory_files:
    type: file
    tables:
      stock: ./inventory.csv

# ❌ Bad: Generic names
sources:
  db1:
    type: postgres
  file1:
    type: file
```

### 2. Pipeline Reusability

```yaml
# Define reusable pipelines
pipelines:
  base_sales:
    source: data
    table: sales
    filters:
      - type: widget
        field: region

  summary_sales:
    pipeline: base_sales  # Extends base_sales
    transforms:
      - type: aggregate
        by: ['category']
        aggregate:
          total: {revenue: sum}
```

### 3. Performance

```yaml
# Limit data size for large tables
sources:
  bigdata:
    type: postgres
    tables:
      events: "SELECT * FROM events WHERE date >= '2024-01-01' LIMIT 100000"
```

### 4. User Experience

```yaml
# Provide clear labels and formatting
filters:
  - type: widget
    field: region
    label: "Sales Region"  # Clear label

views:
  - type: indicator
    field: revenue
    title: "Total Revenue"
    format: '${value:,.0f}'  # Formatted display
```

## Troubleshooting

### Dashboard Won't Load

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('dashboard.yaml'))"

# Run with debug logging
lumen serve dashboard.yaml --log-level=debug
```

### Data Not Showing

- Verify data source path/connection
- Check table names match YAML config
- Ensure columns referenced exist in data

### Performance Issues

- Limit query results (use SQL WHERE clauses)
- Reduce number of rows displayed
- Use aggregation before visualization

**See**: [Troubleshooting Guide](../../references/lumen-dashboards/troubleshooting.md) for common issues.

## Progressive Learning Path

### Level 1: Basics
1. Create simple file-based dashboard
2. Add filters
3. Create basic views

**Resources**:
- Quick Start (this doc)
- [Data Sources Reference](../../references/lumen-dashboards/sources.md)

### Level 2: Transforms
1. Filter and aggregate data
2. Use SQL transforms
3. Chain multiple transforms

**Resources**:
- [Data Transforms Reference](../../references/lumen-dashboards/transforms.md)

### Level 3: Advanced Layouts
1. Multi-page dashboards
2. Cross-filtering
3. Custom themes

**Resources**:
- [Layouts Reference](../../references/lumen-dashboards/layouts.md)
- [Views Reference](../../references/lumen-dashboards/views.md)

### Level 4: Production
1. Database integration
2. Authentication
3. Deployment

**Resources**:
- [Deployment Guide](../../references/lumen-dashboards/deployment.md)

## Additional Resources

### Documentation
- **[Data Sources Reference](../../references/lumen-dashboards/sources.md)** - All source types and configuration
- **[Data Transforms Reference](../../references/lumen-dashboards/transforms.md)** - Complete transform reference
- **[Views Reference](../../references/lumen-dashboards/views.md)** - All visualization types
- **[Layouts Reference](../../references/lumen-dashboards/layouts.md)** - Layout patterns and organization
- **[Python API Reference](../../references/lumen-dashboards/python-api.md)** - Programmatic dashboard creation
- **[Deployment Guide](../../references/lumen-dashboards/deployment.md)** - Production deployment
- **[Examples](../../references/lumen-dashboards/examples.md)** - Complete dashboard examples
- **[Troubleshooting Guide](../../references/lumen-dashboards/troubleshooting.md)** - Common issues

### External Links
- [Lumen Documentation](https://lumen.holoviz.org/)
- [Lumen Gallery](https://lumen.holoviz.org/gallery/)
- [GitHub Repository](https://github.com/holoviz/lumen)
- [Community Discourse](https://discourse.holoviz.org)

## Use Cases

### Business Intelligence
- Executive dashboards
- Sales analytics
- Financial reporting
- Operational metrics

### Data Exploration
- Dataset overview
- Interactive filtering
- Drill-down analysis
- Comparative views

### Real-Time Monitoring
- Live data feeds
- Alert dashboards
- System metrics
- Performance tracking

### Reporting
- Scheduled reports
- Standardized views
- Shareable dashboards
- Embedded analytics

## Summary

Lumen enables rapid dashboard development through declarative YAML specifications.

**Strengths**:
- No Python code required
- Fast development cycle
- Reproducible specifications
- Built-in interactivity
- Standard dashboard patterns

**Ideal for**:
- Fixed dashboard layouts
- Standard data patterns
- Non-programmer dashboard creators
- Rapid prototyping

**Consider alternatives when**:
- Need custom application logic → [Panel Dashboards](../panel-dashboards/SKILL.md)
- Need ad-hoc exploration → [Lumen AI](../lumen-ai/SKILL.md)
- Building novel interactions → [Panel Dashboards](../panel-dashboards/SKILL.md)

## Related Skills

- **[Lumen AI](../lumen-ai/SKILL.md)** - Conversational data exploration
- **[Panel Dashboards](../panel-dashboards/SKILL.md)** - Custom Python dashboards
- **[Plotting Fundamentals](../plotting-fundamentals/SKILL.md)** - Quick plotting with hvPlot
