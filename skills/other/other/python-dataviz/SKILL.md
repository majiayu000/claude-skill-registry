---
name: python-dataviz
description: Professional data visualization using Python (matplotlib, seaborn, plotly). Create publication-quality static charts, statistical visualizations, and interactive plots. Use when generating charts/graphs/plots from data, creating infographics with data components, or producing scientific/statistical visualizations. Supports PNG/SVG (static) and HTML (interactive) export.
---

# Python Data Visualization

Create professional charts, graphs, and statistical visualizations using Python's leading libraries.

## Libraries & Use Cases

**matplotlib** - Static plots, publication-quality, full control
- Bar, line, scatter, pie, histogram, heatmap
- Multi-panel figures, subplots
- Custom styling, annotations
- Export: PNG, SVG, PDF

**seaborn** - Statistical visualizations, beautiful defaults
- Distribution plots (violin, box, kde, histogram)
- Categorical plots (bar, count, swarm, box)
- Relationship plots (scatter, line, regression)
- Matrix plots (heatmap, clustermap)
- Built on matplotlib, integrates seamlessly

**plotly** - Interactive charts, web-friendly
- Hover tooltips, zoom, pan
- 3D plots, animations
- Dashboards via Dash framework
- Export: HTML, PNG (requires kaleido)

## Quick Start

### Setup Environment

```bash
cd skills/python-dataviz
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### Create a Chart

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2, color='#667eea')
plt.title('Sine Wave', fontsize=16, fontweight='bold')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.grid(alpha=0.3)
plt.tight_layout()

# Export
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.savefig('output.svg', bbox_inches='tight')
```

## Chart Selection Guide

**Distribution/Statistical:**
- Histogram → `plt.hist()` or `sns.histplot()`
- Box plot → `sns.boxplot()`
- Violin plot → `sns.violinplot()`
- KDE → `sns.kdeplot()`

**Comparison:**
- Bar chart → `plt.bar()` or `sns.barplot()`
- Grouped bar → `sns.barplot(hue=...)`
- Horizontal bar → `plt.barh()` or `sns.barplot(orient='h')`

**Relationship:**
- Scatter → `plt.scatter()` or `sns.scatterplot()`
- Line → `plt.plot()` or `sns.lineplot()`
- Regression → `sns.regplot()` or `sns.lmplot()`

**Heatmaps:**
- Correlation matrix → `sns.heatmap(df.corr())`
- 2D data → `plt.imshow()` or `sns.heatmap()`

**Interactive:**
- Any plotly chart → `plotly.express` or `plotly.graph_objects`
- See references/plotly-examples.md

## Best Practices

### 1. Figure Size & DPI
```python
plt.figure(figsize=(10, 6))  # Width x Height in inches
plt.savefig('output.png', dpi=300)  # Publication: 300 dpi, Web: 72-150 dpi
```

### 2. Color Palettes
```python
# Seaborn palettes (works with matplotlib too)
import seaborn as sns
sns.set_palette("husl")  # Colorful
sns.set_palette("muted")  # Soft
sns.set_palette("deep")  # Bold

# Custom colors
colors = ['#667eea', '#764ba2', '#f6ad55', '#4299e1']
```

### 3. Styling
```python
# Use seaborn styles even for matplotlib
import seaborn as sns
sns.set_theme()  # Better defaults
sns.set_style("whitegrid")  # Options: whitegrid, darkgrid, white, dark, ticks

# Or matplotlib styles
plt.style.use('ggplot')  # Options: ggplot, seaborn, bmh, fivethirtyeight
```

### 4. Multiple Subplots
```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].plot(x, y1)
axes[0, 1].plot(x, y2)
# etc.
plt.tight_layout()  # Prevent label overlap
```

### 5. Export Formats
```python
# PNG for sharing/embedding (raster)
plt.savefig('chart.png', dpi=300, bbox_inches='tight', transparent=False)

# SVG for editing/scaling (vector)
plt.savefig('chart.svg', bbox_inches='tight')

# For plotly (interactive)
import plotly.express as px
fig = px.scatter(df, x='col1', y='col2')
fig.write_html('chart.html')
```

## Advanced Topics

See references/ for detailed guides:

- **Color theory & palettes**: references/colors.md
- **Statistical plots**: references/statistical.md
- **Plotly interactive charts**: references/plotly-examples.md
- **Multi-panel layouts**: references/layouts.md

## Example Scripts

See scripts/ for ready-to-use examples:

- `scripts/bar_chart.py` - Bar and grouped bar charts
- `scripts/line_chart.py` - Line plots with multiple series
- `scripts/scatter_plot.py` - Scatter plots with regression
- `scripts/heatmap.py` - Correlation heatmaps
- `scripts/distribution.py` - Histograms, KDE, violin plots
- `scripts/interactive.py` - Plotly interactive charts

## Common Patterns

### Data from CSV
```python
import pandas as pd
df = pd.read_csv('data.csv')

# Plot with pandas (uses matplotlib)
df.plot(x='date', y='value', kind='line', figsize=(10, 6))
plt.savefig('output.png', dpi=300)

# Or with seaborn for better styling
sns.lineplot(data=df, x='date', y='value')
plt.savefig('output.png', dpi=300)
```

### Dictionary Data
```python
data = {'Category A': 25, 'Category B': 40, 'Category C': 15}

# Matplotlib
plt.bar(data.keys(), data.values())
plt.savefig('output.png', dpi=300)

# Seaborn (convert to DataFrame)
import pandas as pd
df = pd.DataFrame(list(data.items()), columns=['Category', 'Value'])
sns.barplot(data=df, x='Category', y='Value')
plt.savefig('output.png', dpi=300)
```

### NumPy Arrays
```python
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y)
plt.savefig('output.png', dpi=300)
```

## Troubleshooting

**"No module named matplotlib"**
```bash
cd skills/python-dataviz
source .venv/bin/activate
pip install -r requirements.txt
```

**Blank output / "Figure is empty"**
- Check that `plt.savefig()` comes AFTER plotting commands
- Use `plt.show()` for interactive viewing during development

**Labels cut off**
```python
plt.tight_layout()  # Add before plt.savefig()
# Or
plt.savefig('output.png', bbox_inches='tight')
```

**Low resolution output**
```python
plt.savefig('output.png', dpi=300)  # Not 72 or 100
```

## Environment

The skill includes a venv with all dependencies. Always activate before use:

```bash
cd /home/matt/.openclaw/workspace/skills/python-dataviz
source .venv/bin/activate
```

Dependencies: matplotlib, seaborn, plotly, pandas, numpy, kaleido (for plotly static export)
