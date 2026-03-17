---
name: echarts
description: Knowledge about pyecharts chart creation, HTML report generation, and visualization best practices
---

# ECharts Skill

## Technology Stack

- **pyecharts**: Python wrapper for Apache ECharts
- **Apache ECharts**: JavaScript charting library
- **Output**: Self-contained HTML with embedded JS

## Chart Types Reference

### Bar Charts
```python
from pyecharts.charts import Bar
from pyecharts import options as opts

chart = Bar()
chart.add_xaxis(labels)
chart.add_yaxis("Series Name", values)
chart.set_global_opts(
    title_opts=opts.TitleOpts(title="Chart Title"),
    tooltip_opts=opts.TooltipOpts(trigger="axis"),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
)
```

### Line Charts
```python
from pyecharts.charts import Line

chart = Line()
chart.add_xaxis(dates)
chart.add_yaxis("Actual", values, is_smooth=True)
chart.add_yaxis("7-Day MA", moving_avg_7, is_smooth=True, linestyle_opts=opts.LineStyleOpts(type_="dashed"))
```

### Pie Charts
```python
from pyecharts.charts import Pie

chart = Pie()
chart.add("", list(zip(labels, values)))
chart.set_global_opts(legend_opts=opts.LegendOpts(orient="vertical", pos_left="left"))
```

### Heatmaps
```python
from pyecharts.charts import HeatMap

chart = HeatMap()
chart.add_xaxis(x_labels)
chart.add_yaxis("", y_labels, value=[[x, y, val], ...])
chart.set_global_opts(
    visualmap_opts=opts.VisualMapOpts(min_=0, max_=max_val),
)
```

### Scatter Plots (for anomalies)
```python
from pyecharts.charts import Scatter

chart = Scatter()
chart.add_xaxis(dates)
chart.add_yaxis("Cost", costs, symbol_size=10)
# Add anomaly markers with different color/size
```

## Critical: Browser Compatibility

**Always convert to lists for JavaScript:**
```python
# CORRECT
chart.add_xaxis(df['column'].tolist())
chart.add_yaxis("Label", df['values'].tolist())

# WRONG - causes rendering issues
chart.add_xaxis(df['column'].values)  # numpy array
chart.add_xaxis(df['column'])  # pandas Series
```

## Theme Options

Available themes in pyecharts:
- `macarons` (default) - Colorful, professional
- `shine` - Bright colors
- `roma` - Muted, elegant
- `vintage` - Retro feel
- `dark` - Dark background
- `light` - Light, minimal

Usage:
```python
from pyecharts.globals import ThemeType
chart = Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
```

## HTML Report Structure

```python
def generate_html_report(self, output_path: str, top_n: int = 10) -> str:
    # Create all charts
    charts = [
        self.create_cost_by_service_chart(top_n),
        self.create_cost_by_account_chart(),
        # ... more charts
    ]

    # Combine into page
    page = Page(layout=Page.SimplePageLayout)
    for chart in charts:
        page.add(chart)

    # Render to file
    page.render(output_path)
    return output_path
```

## Formatting Numbers

```python
# Currency formatting in tooltips
tooltip_opts=opts.TooltipOpts(
    trigger="axis",
    formatter="{b}: ${c:,.2f}"
)

# Axis label formatting
yaxis_opts=opts.AxisOpts(
    axislabel_opts=opts.LabelOpts(formatter="${value:,.0f}")
)
```

## Common Issues & Solutions

### Empty Charts
1. Check browser console for JS errors
2. Verify `.tolist()` on all data
3. Hard refresh (Ctrl+Shift+R)
4. Check data exists in HTML source

### Chart Too Small
```python
init_opts=opts.InitOpts(width="100%", height="400px")
```

### Labels Overlapping
```python
xaxis_opts=opts.AxisOpts(
    axislabel_opts=opts.LabelOpts(rotate=45, interval=0)
)
```

### Legend Too Long
```python
legend_opts=opts.LegendOpts(
    type_="scroll",
    orient="horizontal",
    pos_bottom="0%"
)
```

## Testing Visualizations

```bash
# Test chart creation
uv run pytest tests/test_visualizer.py -v

# Regenerate example report
uv run pytest tests/test_examples.py -v -s

# View in browser
open examples/example_report.html
```
