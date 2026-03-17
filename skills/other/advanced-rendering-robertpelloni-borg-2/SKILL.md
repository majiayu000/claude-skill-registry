---
name: advanced-rendering
description: Master high-performance rendering for large datasets with Datashader. Use this skill when working with datasets exceeding 100M+ points, optimizing visualization performance, or implementing efficient rendering strategies with rasterization and colormapping techniques.
version: 2025-01-07
compatibility: Requires datashader >= 0.15.0, colorcet >= 3.1.0, holoviews >= 1.18.0, pandas >= 1.0.0, numpy >= 1.15.0
---

# Advanced Rendering Skill

## Overview

Master high-performance rendering for large datasets with Datashader and optimization techniques. This skill covers handling 100M+ point datasets, performance tuning, and efficient visualization strategies.

## Dependencies

- datashader >= 0.15.0
- colorcet >= 3.1.0
- holoviews >= 1.18.0
- pandas >= 1.0.0
- numpy >= 1.15.0

## Core Capabilities

### 1. Datashader Fundamentals

Datashader is designed for rasterizing large datasets:

```python
import datashader as ds
from datashader.mpl_ext import _colorize
import holoviews as hv

# Load large dataset (can handle 100M+ points)
df = pd.read_csv('large_dataset.csv')  # Millions or billions of rows

# Create datashader canvas
canvas = ds.Canvas(plot_width=800, plot_height=600)

# Rasterize aggregation
agg = canvas.points(df, 'x', 'y')

# Convert to image
img = agg.to_array(True)
```

### 2. Efficient Point Rendering

```python
from holoviews.operation.datashader import datashade, aggregate, shade

# Quick datashading with HoloViews
scatter = hv.Scatter(df, 'x', 'y')
shaded = datashade(scatter)

# With custom aggregation
agg = aggregate(scatter, width=800, height=600)
colored = shade(agg, cmap='viridis')

# Control rasterization
from holoviews.operation import rasterize

rasterized = rasterize(
    scatter,
    aggregator=ds.count(),
    pixel_ratio=2,
    upsample_method='interp'
)
```

### 3. Color Mapping and Aggregation

```python
import datashader as ds
from colorcet import cm

# Count aggregation (heatmap)
canvas = ds.Canvas()
agg = canvas.points(df, 'x', 'y', agg=ds.count())

# Weighted aggregation
agg = canvas.points(df, 'x', 'y', agg=ds.sum('value'))

# Mean aggregation
agg = canvas.points(df, 'x', 'y', agg=ds.mean('value'))

# Custom colormapping
import datashader.transfer_functions as tf

shaded = tf.shade(agg, cmap=cm['viridis'])
shaded_with_spread = tf.spread(shaded, px=2)
```

### 4. Image Compositing

```python
# Combine multiple datasets
canvas = ds.Canvas(x_range=(0, 100), y_range=(0, 100))

agg1 = canvas.points(df1, 'x', 'y')
agg2 = canvas.points(df2, 'x', 'y')

# Shade separately
shaded1 = tf.shade(agg1, cmap=cm['reds'])
shaded2 = tf.shade(agg2, cmap=cm['blues'])

# Composite
import datashader.transfer_functions as tf
composite = tf.composite(shaded1, shaded2)
```

### 5. Interactive Datashader with HoloViews

```python
from holoviews.operation.datashader import datashade
from holoviews import streams

# Interactive scatter with zooming
def create_datashaded_plot(data):
    scatter = hv.Scatter(data, 'x', 'y')
    return datashade(scatter, cmap='viridis')

# Add interaction
range_stream = streams.RangeXY()
interactive_plot = hv.DynamicMap(
    create_datashaded_plot,
    streams=[range_stream]
)
```

### 6. Time Series Data Streaming

```python
# Efficient streaming plot for time series
from holoviews.operation.datashader import rasterize
from holoviews import streams

def create_timeseries_plot(df_window):
    curve = hv.Curve(df_window, 'timestamp', 'value')
    return curve

# Rasterize for efficiency
rasterized = rasterize(
    hv.Curve(df, 'timestamp', 'value'),
    aggregator=ds.mean('value'),
    width=1000,
    height=400
)
```

## Performance Optimization Strategies

### 1. Memory Optimization

```python
# Use data types efficiently
df = pd.read_csv(
    'large_file.csv',
    dtype={
        'x': 'float32',
        'y': 'float32',
        'value': 'float32',
        'category': 'category'
    }
)

# Chunk processing for extremely large files
chunk_size = 1_000_000
aggregations = []

for chunk in pd.read_csv('huge.csv', chunksize=chunk_size):
    canvas = ds.Canvas()
    agg = canvas.points(chunk, 'x', 'y')
    aggregations.append(agg)

# Combine results
combined_agg = aggregations[0]
for agg in aggregations[1:]:
    combined_agg = combined_agg + agg
```

### 2. Resolution and Pixel Ratio

```python
# Adjust canvas resolution based on data density
def auto_canvas(df, target_pixels=500000):
    data_points = len(df)
    aspect_ratio = (df['x'].max() - df['x'].min()) / (df['y'].max() - df['y'].min())

    pixels = int(np.sqrt(target_pixels / aspect_ratio))
    height = pixels
    width = int(pixels * aspect_ratio)

    return ds.Canvas(
        plot_width=width,
        plot_height=height,
        x_range=(df['x'].min(), df['x'].max()),
        y_range=(df['y'].min(), df['y'].max())
    )

canvas = auto_canvas(df)
agg = canvas.points(df, 'x', 'y')
```

### 3. Aggregation Selection

```python
# Choose appropriate aggregation for your data
canvas = ds.Canvas()

# For counting: count()
agg_count = canvas.points(df, 'x', 'y', agg=ds.count())

# For averages: mean()
agg_mean = canvas.points(df, 'x', 'y', agg=ds.mean('value'))

# For sums: sum()
agg_sum = canvas.points(df, 'x', 'y', agg=ds.sum('value'))

# For max/min
agg_max = canvas.points(df, 'x', 'y', agg=ds.max('value'))

# For percentiles
agg_p95 = canvas.points(df, 'x', 'y', agg=ds.count_cat('category'))
```

## Colormapping with Colorcet

### 1. Perceptually Uniform Colormaps

```python
from colorcet import cm, cmap_d
import datashader.transfer_functions as tf

# Use perceptually uniform colormaps
canvas = ds.Canvas()
agg = canvas.points(df, 'x', 'y', agg=ds.count())

# Gray scale
shaded_gray = tf.shade(agg, cmap=cm['gray'])

# Perceptual colormaps
shaded_viridis = tf.shade(agg, cmap=cm['viridis'])
shaded_turbo = tf.shade(agg, cmap=cm['turbo'])

# Category colormaps
shaded_color = tf.shade(agg, cmap=cm['cet_c5'])
```

### 2. Custom Color Normalization

```python
# Logarithmic normalization
from datashader.transfer_functions import Log

canvas = ds.Canvas()
agg = canvas.points(df, 'x', 'y', agg=ds.sum('value'))

# Log transform for better visualization
shaded = tf.shade(agg, norm='log', cmap=cm['viridis'])

# Power law normalization
shaded_power = tf.shade(agg, norm=ds.transfer_functions.eq_hist, cmap=cm['plasma'])
```

### 3. Multi-Band Compositing

```python
# Separate visualization of multiple datasets
canvas = ds.Canvas()

agg_red = canvas.points(df_red, 'x', 'y')
agg_green = canvas.points(df_green, 'x', 'y')
agg_blue = canvas.points(df_blue, 'x', 'y')

# Stack as RGB
from datashader.colors import rgb
result = rgb(agg_red, agg_green, agg_blue)
```

## Integration with Panel and HoloViews

```python
import panel as pn
from holoviews.operation.datashader import datashade

# Create interactive dashboard with datashader
class LargeDataViewer(param.Parameterized):
    cmap = param.Selector(default='viridis', objects=list(cm.keys()))
    show_spread = param.Boolean(default=False)

    def __init__(self, data):
        super().__init__()
        self.data = data

    @param.depends('cmap', 'show_spread')
    def plot(self):
        scatter = hv.Scatter(self.data, 'x', 'y')
        shaded = datashade(scatter, cmap=cm[self.cmap])

        if self.show_spread:
            shaded = tf.spread(shaded, px=2)

        return shaded

viewer = LargeDataViewer(large_df)

pn.extension('material')
app = pn.Column(
    pn.param.ParamMethod.from_param(viewer.param),
    viewer.plot
)
app.servable()
```

## Best Practices

### 1. Choose the Right Tool
```
< 10k points:        Use standard HoloViews/hvPlot
10k - 1M points:     Use rasterize() for dense plots
1M - 100M points:    Use Datashader
> 100M points:       Use Datashader with chunking
```

### 2. Appropriate Canvas Size
```python
# General rule: 400-1000 pixels on each axis
# Too small: loses detail
# Too large: slow rendering, memory waste

canvas = ds.Canvas(plot_width=800, plot_height=600)  # Good default
```

### 3. Normalize Large Value Ranges
```python
# When data has extreme outliers
canvas = ds.Canvas()
agg = canvas.points(df, 'x', 'y', agg=ds.mean('value'))

# Use appropriate normalization
shaded = tf.shade(agg, norm='log', cmap=cm['viridis'])
```

## Common Patterns

### Pattern 1: Progressive Disclosure
```python
def create_progressive_plot(df):
    # Start with aggregated view
    agg = canvas.points(df, 'x', 'y')
    return tf.shade(agg, cmap='viridis')

# User can zoom to see more detail
# Datashader automatically recalculates at new resolution
```

### Pattern 2: Categorical Visualization
```python
canvas = ds.Canvas()

# Aggregate by category
for category in df['category'].unique():
    subset = df[df['category'] == category]
    agg = canvas.points(subset, 'x', 'y', agg=ds.count())
    shaded = tf.shade(agg, cmap=cm[f'category_{category}'])
```

### Pattern 3: Time Series Aggregation
```python
def aggregate_time_series(df, time_bucket):
    df['time_bucket'] = pd.cut(df['timestamp'], bins=time_bucket)

    aggregated = df.groupby('time_bucket').agg({
        'x': 'mean',
        'y': 'mean',
        'value': 'sum'
    })

    return aggregated
```

## Common Use Cases

1. **Scatter Plot Analysis**: 100M+ point clouds
2. **Time Series Visualization**: High-frequency trading data
3. **Geospatial Heat Maps**: Global-scale location data
4. **Scientific Visualization**: Climate model outputs
5. **Network Analysis**: Large graph layouts
6. **Financial Analytics**: Tick-by-tick market data

## Troubleshooting

### Issue: Poor Color Differentiation
- Use perceptually uniform colormaps from colorcet
- Apply appropriate normalization (log, power law)
- Adjust canvas size for better resolution

### Issue: Memory Issues with Large Data
- Use chunk processing for files larger than RAM
- Reduce data type precision (float64 → float32)
- Aggregate before visualization
- Use categorical data type for strings

### Issue: Slow Performance
- Reduce canvas size (fewer pixels)
- Use simpler aggregation functions
- Enable GPU acceleration if available
- Profile with Python profilers to find bottlenecks

## Resources

- [Datashader Documentation](https://datashader.org)
- [Colorcet Documentation](https://colorcet.holoviz.org)
- [Datashader Examples](https://datashader.org/getting_started/index.html)
- [Large Data Visualization Guide](https://holoviews.org/user_guide/Large_Data.html)
