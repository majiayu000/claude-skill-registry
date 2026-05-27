---
name: colormaps-styling
description: Master color management and visual styling with Colorcet. Use this skill when selecting appropriate colormaps, creating accessible and colorblind-friendly visualizations, applying consistent themes, or customizing plot aesthetics with perceptually uniform color palettes.
version: 2025-01-07
compatibility: Requires colorcet >= 3.1.0, holoviews >= 1.18.0, panel >= 1.3.0, bokeh >= 3.0.0
---

# Colormaps & Styling Skill

## Overview

Master color management and visual styling with Colorcet and theme customization. Select appropriate colormaps, create accessible visualizations, and apply consistent application styling.

### What is Colorcet?

Colorcet provides perceptually uniform colormaps designed for scientific visualization:

- **Perceptually uniform**: Changes in data correspond to proportional visual changes
- **Colorblind-friendly**: Palettes designed for accessibility
- **Purpose-built**: Specific colormaps for different data types
- **HoloViz integration**: Seamless use across HoloViews, Panel, and Bokeh

## Quick Start

### Installation

```bash
pip install colorcet
```

### Basic Usage

```python
import colorcet as cc
from colorcet import cm
import holoviews as hv

hv.extension('bokeh')

# Use a colormap
data.hvplot.scatter('x', 'y', c='value', cmap=cm['cet_goertzel'])
```

## Core Concepts

### 1. Colormap Categories

**Sequential**: Single hue, increasing intensity
```python
# Blues, greens, reds, grays
data.hvplot('x', 'y', c='value', cmap=cm['cet_blues'])
```

**Diverging**: Two hues from center point
```python
# Emphasize positive/negative
data.hvplot('x', 'y', c='value', cmap=cm['cet_coolwarm'])
```

**Categorical**: Distinct colors for categories
```python
# Qualitative data
data.hvplot('x', 'y', c='category', cmap=cc.palette['tab10'])
```

**Cyclic**: Wraps around for angular data
```python
# Angles, directions, phases
data.hvplot('x', 'y', c='angle', cmap=cm['cet_cyclic_c1'])
```

**See**: [Colormap Reference](../../references/colormaps/colormap-reference.md) for complete catalog

### 2. Accessibility

**Colorblind-safe palettes**:
```python
# Deuteranopia (red-green)
cmap=cm['cet_d4']

# Protanopia (red-green)
cmap=cm['cet_p3']

# Tritanopia (blue-yellow)
cmap=cm['cet_t10']

# Grayscale-safe
cmap=cm['cet_gray_r']
```

**See**: [Accessibility Guide](../../references/colormaps/accessibility.md) for comprehensive guidelines

### 3. Colormap Selection Guide

| Data Type | Recommended Colormap | Example |
|-----------|---------------------|---------|
| Single channel (positive) | `cet_blues`, `cet_gray_r` | Temperature, density |
| Diverging (±) | `cet_coolwarm`, `cet_bwy` | Correlation, anomalies |
| Categorical | `tab10`, `tab20` | Categories, labels |
| Angular | `cet_cyclic_c1` | Wind direction, phase |
| Full spectrum | `cet_goertzel` | General purpose |

### 4. HoloViews Styling

```python
import holoviews as hv

# Apply colormap
scatter = hv.Scatter(data, 'x', 'y', vdims=['value']).opts(
    color=hv.dim('value').norm(),
    cmap=cm['cet_goertzel'],
    colorbar=True,
    width=600,
    height=400
)

# Style options
scatter.opts(
    size=5,
    alpha=0.7,
    tools=['hover'],
    title='My Plot'
)
```

**See**: [HoloViews Styling](../../references/colormaps/holoviews-styling.md) for advanced customization

### 5. Panel Themes

```python
import panel as pn

# Apply theme
pn.extension(design='material')

# Custom theme
pn.config.theme = 'dark'

# Accent color
template = pn.template.FastListTemplate(
    title='My App',
    accent='#00aa41'
)
```

**See**: [Panel Themes](../../references/colormaps/panel-themes.md) for theme customization

## Common Patterns

### Pattern 1: Heatmap with Diverging Colormap

```python
import holoviews as hv
from colorcet import cm

heatmap = hv.HeatMap(data, ['x', 'y'], 'value').opts(
    cmap=cm['cet_coolwarm'],
    colorbar=True,
    width=600,
    height=400,
    tools=['hover']
)
```

### Pattern 2: Categorical Color Assignment

```python
import panel as pn
from colorcet import palette

categories = ['A', 'B', 'C', 'D']
colors = palette['tab10'][:len(categories)]

color_map = dict(zip(categories, colors))
plot = data.hvplot('x', 'y', c='category', cmap=color_map)
```

### Pattern 3: Consistent App Styling

```python
import panel as pn

# Set global theme
pn.extension(design='material')

# Custom CSS
pn.config.raw_css.append("""
.card {
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
""")

# Accent color throughout
accent = '#00aa41'
template = pn.template.FastListTemplate(
    title='My Dashboard',
    accent=accent
)
```

### Pattern 4: Responsive Colorbar

```python
from holoviews import opts

plot = data.hvplot.scatter('x', 'y', c='value', cmap=cm['cet_blues']).opts(
    colorbar=True,
    colorbar_opts={
        'title': 'Value',
        'width': 10,
        'ticker': {'desired_num_ticks': 5}
    }
)
```

### Pattern 5: Colorblind-Safe Visualization

```python
from colorcet import cm

# Use colorblind-safe diverging palette
plot = data.hvplot('x', 'y', c='value', cmap=cm['cet_d4']).opts(
    title='Colorblind-Safe Visualization',
    width=600,
    height=400
)

# Alternative: Use patterns/hatching
plot.opts(hatch_pattern='/')
```

## Best Practices

### 1. Match Colormap to Data Type

```python
# ✅ Good: Sequential for positive values
temp_plot = data.hvplot(c='temperature', cmap=cm['cet_fire'])

# ✅ Good: Diverging for centered data
correlation = data.hvplot(c='correlation', cmap=cm['cet_coolwarm'])

# ❌ Bad: Rainbow/jet colormap (not perceptually uniform)
bad_plot = data.hvplot(c='value', cmap='jet')  # Avoid!
```

### 2. Consider Accessibility

```python
# ✅ Good: Colorblind-safe
plot = data.hvplot(c='value', cmap=cm['cet_d4'])

# ✅ Good: Add patterns for print/grayscale
plot.opts(hatch_pattern='/')

# ✅ Good: Test in grayscale
plot.opts(cmap=cm['cet_gray_r'])
```

### 3. Consistent Styling

```python
# ✅ Good: Define color scheme once
COLORS = {
    'primary': '#00aa41',
    'secondary': '#616161',
    'accent': '#ff6f00'
}

# Use throughout application
pn.template.FastListTemplate(accent=COLORS['primary'])
```

### 4. Meaningful Labels

```python
# ✅ Good: Descriptive colorbar
plot.opts(
    colorbar=True,
    colorbar_opts={'title': 'Temperature (°C)'}
)

# ❌ Bad: No context
plot.opts(colorbar=True)
```

### 5. Performance with Large Data

```python
# For large datasets, limit colormap resolution
plot.opts(
    cmap=cm['cet_goertzel'],
    color_levels=256  # Reduce if performance issues
)
```

## Configuration

### Global Colormap Defaults

```python
import holoviews as hv
from colorcet import cm

# Set default colormap
hv.opts.defaults(
    hv.opts.Image(cmap=cm['cet_goertzel']),
    hv.opts.Scatter(cmap=cm['cet_blues'])
)
```

### Theme Configuration

```python
import panel as pn

# Material design
pn.extension(design='material')

# Dark mode
pn.config.theme = 'dark'

# Custom theme JSON
pn.config.theme_json = {
    'palette': {
        'primary': '#00aa41',
        'secondary': '#616161'
    }
}
```

## Troubleshooting

### Colormap Not Showing

```python
# Check if colormap imported
from colorcet import cm
print(cm['cet_goertzel'])  # Should print colormap

# Verify data range
print(data['value'].min(), data['value'].max())

# Explicit normalization
plot.opts(color=hv.dim('value').norm())
```

### Colors Look Wrong

- **Issue**: Perceptual non-uniformity
- **Solution**: Use Colorcet instead of matplotlib defaults

```python
# ❌ Avoid
cmap='jet', cmap='rainbow'

# ✅ Use
cmap=cm['cet_goertzel'], cmap=cm['cet_fire']
```

### Theme Not Applying

```python
# Ensure extension loaded with design
pn.extension(design='material')

# Check theme setting
print(pn.config.theme)  # 'default' or 'dark'

# Reload page after theme change
```

## Progressive Learning Path

### Level 1: Basics
1. Install Colorcet
2. Use basic colormaps
3. Apply to plots

**Resources**:
- Quick Start (this doc)
- [Colormap Reference](../../references/colormaps/colormap-reference.md)

### Level 2: Accessibility
1. Understand colormap categories
2. Choose appropriate maps
3. Test for colorblindness

**Resources**:
- [Accessibility Guide](../../references/colormaps/accessibility.md)

### Level 3: Advanced Styling
1. Customize HoloViews opts
2. Create custom themes
3. Consistent branding

**Resources**:
- [HoloViews Styling](../../references/colormaps/holoviews-styling.md)
- [Panel Themes](../../references/colormaps/panel-themes.md)

## Additional Resources

### Documentation
- **[Colormap Reference](../../references/colormaps/colormap-reference.md)** - Complete colormap catalog
- **[Accessibility Guide](../../references/colormaps/accessibility.md)** - Colorblind-friendly design
- **[HoloViews Styling](../../references/colormaps/holoviews-styling.md)** - Advanced customization
- **[Panel Themes](../../references/colormaps/panel-themes.md)** - Theme and branding

### External Links
- [Colorcet Documentation](https://colorcet.holoviz.org/)
- [Colorcet Gallery](https://colorcet.holoviz.org/user_guide/index.html)
- [Color Universal Design](https://jfly.uni-koeln.de/color/)
- [WCAG Color Contrast](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

## Use Cases

### Scientific Visualization
- Temperature maps
- Density plots
- Correlation matrices
- Geospatial data

### Data Dashboards
- KPI indicators
- Time series
- Category comparison
- Status displays

### Accessibility
- Colorblind-friendly visualizations
- Print-safe graphics
- High-contrast displays
- Grayscale compatibility

### Branding
- Corporate colors
- Consistent styling
- Custom themes
- Professional appearance

## Summary

Colorcet provides perceptually uniform, accessible colormaps for scientific visualization.

**Key principles**:
- Match colormap to data type
- Choose colorblind-safe palettes
- Use perceptually uniform maps
- Maintain consistent styling
- Test accessibility

**Ideal for**:
- Scientific visualizations
- Accessible dashboards
- Professional applications
- Print publications

**Colormap selection**:
- Sequential: Single channel data
- Diverging: Centered data (±)
- Categorical: Qualitative categories
- Cyclic: Angular/periodic data

## Related Skills

- **[Data Visualization](../data-visualization/SKILL.md)** - HoloViews visualization patterns
- **[Panel Dashboards](../panel-dashboards/SKILL.md)** - Dashboard styling and themes
- **[Plotting Fundamentals](../plotting-fundamentals/SKILL.md)** - Basic plotting with hvPlot
