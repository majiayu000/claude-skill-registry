---
name: plotting-fundamentals
description: Master quick plotting and interactive visualization with hvPlot. Use this skill when creating basic plots (line, scatter, bar, histogram, box), visualizing pandas DataFrames with minimal code, adding interactivity and hover tools, composing multiple plots in layouts, or generating publication-quality visualizations rapidly.
version: 2025-01-07
compatibility: Requires hvplot >= 0.9.0, holoviews >= 1.18.0, pandas >= 1.0.0, numpy >= 1.15.0, bokeh >= 3.0.0
---

# Plotting Fundamentals Skill

## Overview

Master quick plotting and interactive visualization with hvPlot and HoloViews basics. This skill covers essential techniques for creating publication-quality plots with minimal code.

## Dependencies

- hvplot >= 0.9.0
- holoviews >= 1.18.0
- pandas >= 1.0.0
- numpy >= 1.15.0
- bokeh >= 3.0.0

## Core Capabilities

### 1. hvPlot Quick Plotting

hvPlot provides an intuitive, pandas-like API for rapid visualization:

```python
import hvplot.pandas
import pandas as pd
import numpy as np

# Create sample data
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100),
    'sales': np.cumsum(np.random.randn(100)) + 100,
    'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
})

# Simple line plot
df.hvplot.line(x='date', y='sales', title='Sales Over Time')

# Grouped plot
df.hvplot.line(x='date', y='sales', by='region', subplots=True)

# Scatter with size and color
df.hvplot.scatter(x='sales', y='date', c='region', size=50)
```

### 2. Common Plot Types

```python
# Bar plot
df.hvplot.bar(x='region', y='sales', rot=45)

# Histogram
df['sales'].hvplot.hist(bins=30, title='Sales Distribution')

# Box plot
df.hvplot.box(y='sales', by='region')

# Area plot
df.hvplot.area(x='date', y='sales')

# KDE (Kernel Density Estimation)
df['sales'].hvplot.kde()

# Hexbin (for large datasets)
df.hvplot.hexbin(x='sales', y='date', gridsize=20)
```

### 3. Customization Options

```python
# Apply consistent styling
plot = df.hvplot.line(
    x='date',
    y='sales',
    title='Sales Trend',
    xlabel='Date',
    ylabel='Sales ($)',
    color='#2E86DE',
    line_width=2,
    height=400,
    width=700,
    responsive=True,
    legend='top_left'
)

# Color mapping
df.hvplot.scatter(
    x='sales',
    y='date',
    c='sales',
    cmap='viridis',
    s=100
)

# Multiple series
df.hvplot.line(
    x='date',
    y=['sales'],
    title='Performance Metrics'
)
```

### 4. Interactive Features

```python
# Hover information
df.hvplot.scatter(
    x='sales',
    y='date',
    hover_cols=['region'],
    tools=['hover', 'pan', 'wheel_zoom']
)

# Selection and linked views
import holoviews as hv
scatter = df.hvplot.scatter(x='sales', y='date')
scatter.opts(tools=['box_select'])

# Responsive sizing
plot = df.hvplot.line(
    x='date',
    y='sales',
    responsive=True,
    height=400
)
```

### 5. Geographic Plotting with hvPlot

```python
import geopandas as gpd

# Quick geographic plot
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gdf.hvplot(
    c='pop_est',
    cmap='viridis',
    geo=True,
    frame_width=600
)

# City points on map
cities = gpd.GeoDataFrame({
    'name': ['City A', 'City B'],
    'geometry': [Point(0, 0), Point(1, 1)],
    'population': [1000000, 500000]
})
cities.hvplot(
    geo=True,
    c='population',
    size='population',
    cmap='plasma'
)
```

## HoloViews Fundamentals

### 1. Basic Element Types

```python
import holoviews as hv
from holoviews import opts

# Curve
curve = hv.Curve(df, 'date', 'sales')

# Scatter
scatter = hv.Scatter(df, 'sales', 'date')

# Histogram
hist = hv.Histogram(df['sales'].values)

# Image (heatmap)
image = hv.Image(data)

# Bars
bars = hv.Bars(df, 'region', 'sales')

# Text annotations
text = hv.Text(0.5, 0.5, 'Hello HoloViews')
```

### 2. Styling and Options

```python
# Using .opts() method
plot = hv.Curve(df, 'date', 'sales').opts(
    title='Sales Trend',
    xlabel='Date',
    ylabel='Sales',
    color='#2E86DE',
    line_width=2,
    height=400,
    width=700
)

# Using opts object
opts_obj = opts.Curve(
    title='Sales',
    color='navy',
    line_width=2
)
plot = hv.Curve(df, 'date', 'sales').opts(opts_obj)
```

### 3. Composing Visualizations

```python
# Overlaying multiple plots
overlay = hv.Curve(df, 'date', 'sales') * hv.Scatter(df_subset, 'date', 'sales')

# Side-by-side layouts
layout = hv.Curve(df1, 'date', 'sales') + hv.Scatter(df2, 'date', 'value')

# Grid layouts
grid = (
    (hv.Curve(data1) + hv.Scatter(data2)) /
    (hv.Histogram(data3) + hv.Image(data4))
)

# Faceted views
faceted = hv.Curve(df, 'date', 'sales').facet('region')
```

### 4. Interactive Selection and Linking

```python
# Brush selection
curve_selectable = hv.Curve(df, 'date', 'sales').opts(
    tools=['box_select'],
    selection_fill_color='red',
    nonselection_fill_alpha=0.2
)

# Dynamic linking with streams
from holoviews import streams

# Hover information
hover = streams.Tap(source=scatter, transient=True)

@hv.transform
def get_info(data):
    if data.empty:
        return hv.Text(0, 0, 'Hover to select')
    return hv.Text(0, 0, f"Point: {data.iloc[0].values}")
```

## Best Practices

### 1. Data Preparation
- Always check data types before plotting
- Handle missing values explicitly
- Normalize columns for better visualization
- Use appropriate data ranges

### 2. Visual Design
- Choose colors for accessibility (colorblind-friendly palettes)
- Use title and axis labels
- Include legends for multiple series
- Maintain consistent styling across related plots

### 3. Performance
- Use datashader for datasets with >100k points
- Downsample or aggregate before plotting
- Use responsive=True for web dashboards
- Cache expensive plot computations

### 4. Code Organization
```python
# Create a plotting utility module
class PlotBuilder:
    COLORS = {'primary': '#2E86DE', 'secondary': '#A23B72'}
    DEFAULTS = {'height': 400, 'width': 700, 'responsive': True}

    @staticmethod
    def style_plot(plot, **kwargs):
        return plot.opts(**{**PlotBuilder.DEFAULTS, **kwargs})

# Usage
styled = PlotBuilder.style_plot(df.hvplot.line(x='date', y='sales'))
```

## Common Patterns

### Pattern 1: Dashboard with Multiple Plots
```python
def create_sales_dashboard(df):
    return hv.Column(
        df.hvplot.line(x='date', y='sales', title='Trend'),
        df.hvplot.bar(x='region', y='sales', title='By Region'),
        df['sales'].hvplot.hist(bins=20, title='Distribution')
    )
```

### Pattern 2: Conditional Visualization
```python
def plot_data(df, plot_type='line'):
    if plot_type == 'line':
        return df.hvplot.line(x='date', y='sales')
    elif plot_type == 'scatter':
        return df.hvplot.scatter(x='date', y='sales')
    else:
        return df.hvplot.bar(x='region', y='sales')
```

### Pattern 3: Multi-Series Plot with Legend
```python
def plot_multiple_metrics(df, metrics):
    plots = [df.hvplot.line(x='date', y=m, label=m) for m in metrics]
    return hv.Overlay(plots)
```

## Integration with Other HoloViz Tools

- **Panel**: Embed plots in dashboards
- **HoloViews**: Advanced composition and interactivity
- **Datashader**: Large dataset visualization
- **Param**: Dynamic plot updates based on parameters

## Common Use Cases

1. **Time Series Analysis**: Trends, anomalies, forecasting
2. **Comparative Analysis**: Category comparisons, rankings
3. **Distribution Analysis**: Histograms, KDEs, box plots
4. **Correlation Analysis**: Scatter plots, hexbins
5. **Geographic Analysis**: Maps, regional data
6. **Statistical Summaries**: Summary statistics with plots

## Troubleshooting

### Issue: Plot Won't Display
- Ensure `hvplot.pandas` or `hvplot.xarray` is imported
- Check data is not empty
- Verify x and y columns exist in dataframe

### Issue: Poor Performance with Large Data
- Use datashader for >100k points
- Implement aggregation or sampling
- Use hexbin or rasterization

### Issue: Unclear or Overlapping Labels
- Rotate x-axis labels with `rot=45`
- Use subplots with `by='column'`
- Adjust figure size with height/width

## Resources

- [hvPlot Documentation](https://hvplot.holoviz.org)
- [HoloViews Documentation](https://holoviews.org)
- [HoloViews Gallery](https://holoviews.org/reference/index.html)
- [Colorcet for Color Palettes](https://colorcet.holoviz.org)
