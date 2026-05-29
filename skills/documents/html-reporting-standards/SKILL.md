---
name: html-reporting-standards
version: "1.0.0"
category: _internal
description: "HTML Reporting Standards Skill"
---

# HTML Reporting Standards Skill

> Version: 1.0.0
> Category: Standards
> Triggers: Creating reports, visualizations, interactive charts

## Quick Reference

### MANDATORY: Interactive Plots Only

✅ **Allowed:** Plotly, Bokeh, Altair, D3.js
❌ **NOT Allowed:** Static matplotlib PNG/SVG exports

### Technology Selection

| Use Case | Recommended | Why |
|----------|------------|-----|
| General Analysis | Plotly | Easy, feature-rich, pandas integration |
| Statistical Viz | Altair | Grammar of graphics, declarative |
| Real-time Dashboards | Bokeh | Server capabilities, streaming |
| Custom Interactive | D3.js | Maximum flexibility |
| Time Series | Plotly | Excellent time series support |
| Large Datasets | Plotly (webGL) or Bokeh | Performance optimizations |

## Python Examples

### Plotly (Recommended)

```python
import plotly.express as px
import pandas as pd

# Load CSV with RELATIVE path
df = pd.read_csv('../data/processed/results.csv')

# Create interactive plot
fig = px.scatter(df, x='time', y='value',
                 color='category',
                 title='Interactive Results',
                 hover_data=['info'])

# Save as HTML
fig.write_html('../reports/analysis.html',
               include_plotlyjs='cdn',
               config={'responsive': True})
```

### Bokeh

```python
from bokeh.plotting import figure, output_file, save
import pandas as pd

df = pd.read_csv('../data/processed/results.csv')

p = figure(title='Interactive Dashboard')
p.circle(df['x'], df['y'], size=10, alpha=0.5)
p.sizing_mode = 'stretch_width'  # Responsive

output_file('../reports/dashboard.html')
save(p)
```

### Altair

```python
import altair as alt
import pandas as pd

df = pd.read_csv('../data/processed/results.csv')

chart = alt.Chart(df).mark_point().encode(
    x='time:T',
    y='value:Q',
    color='category:N',
    tooltip=['time', 'value', 'category']
).interactive()

chart.save('../reports/analysis.html')
```

## Report Structure

### Required HTML Sections

1. **Header**
   - Title, generation timestamp
   - Module/repository name
   - Author/generator info

2. **Summary Statistics**
   - Key metrics at glance
   - Record counts
   - Data quality indicators

3. **Interactive Visualizations**
   - Minimum 2-3 plots per report
   - Each plot MUST be interactive
   - Clear titles and labels

4. **Data Table (optional)**
   - Sortable/filterable
   - Show sample of data
   - Link to full CSV

5. **Footer**
   - Data source
   - Generation method
   - Contact info

### Responsive Design

Reports must work on:
- Desktop (1920px+)
- Laptop (1366px)
- Tablet (768px)
- Mobile (375px)

**Plotly responsive:**
```python
fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=40, b=20),
)
```

## CSV Data Handling

### MANDATORY: Relative Paths

```python
# ✅ CORRECT: Relative from report location
df = pd.read_csv('../data/processed/results.csv')

# ❌ WRONG: Absolute path
df = pd.read_csv('/mnt/github/workspace/data/results.csv')

# ❌ WRONG: Hardcoded path
df = pd.read_csv('C:/Users/user/data/results.csv')
```

### Path Resolution Helper

```python
from pathlib import Path

def get_data_path(filename, data_type='processed'):
    project_root = Path(__file__).parent.parent.parent
    return project_root / 'data' / data_type / filename

# Usage
df = pd.read_csv(get_data_path('analysis.csv'))
```

## Multi-Plot Dashboard

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Time Series', 'Distribution',
                   'Correlation', 'Summary')
)

# Add plots
fig.add_trace(go.Scatter(...), row=1, col=1)
fig.add_trace(go.Histogram(...), row=1, col=2)
fig.add_trace(go.Scatter(...), row=2, col=1)

fig.update_layout(height=800, showlegend=True)
fig.write_html('../reports/dashboard.html', include_plotlyjs='cdn')
```

## Best Practices

### Performance Optimization

**For large datasets (>10,000 points):**
```python
# Use WebGL rendering
fig = px.scatter(df, x='x', y='y', render_mode='webgl')

# Or sample for visualization
df_sample = df.sample(n=5000)
fig = px.scatter(df_sample, ...)
```

### Accessibility

- Descriptive titles and labels
- Sufficient color contrast
- Keyboard navigation
- Readable font size (≥12pt)

### Version Control

**Don't commit:** Generated HTML reports
**Do commit:** Report generation scripts, templates, CSV data

```gitignore
# .gitignore
reports/*.html
!reports/index.html
```

## Validation Checklist

- [ ] All plots are interactive (no static images)
- [ ] HTML report is generated
- [ ] CSV uses relative paths
- [ ] Report is responsive (tested mobile/desktop)
- [ ] Hover tooltips show data values
- [ ] Zoom/pan functionality works
- [ ] Legend is interactive
- [ ] Export options available
- [ ] Report loads in <3 seconds
- [ ] Works offline (embedded data or CDN fallback)

## Full Reference

See: @docs/modules/standards/HTML_REPORTING_STANDARDS.md

---

*Use this when creating reports, dashboards, or data visualizations.*
