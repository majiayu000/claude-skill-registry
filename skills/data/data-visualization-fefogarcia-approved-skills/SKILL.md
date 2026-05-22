---
name: data-visualization
description: Create production-quality data visualizations including charts, dashboards, and infographics. Use when the user asks to visualize data, create charts, build dashboards, make infographics, plot statistics, or transform datasets into visual representations. Supports React/Recharts artifacts, static images (PNG/PDF via Python), and interactive HTML. Triggers include "visualize this data", "create a chart", "build a dashboard", "make a graph", "plot this", "infographic", or any request to represent data visually.
---

# Data Visualization

Create clear, purposeful visualizations that communicate data effectively.

## Decision Framework

### 1. Choose Output Format

| Format | Best For | Implementation |
|--------|----------|----------------|
| **React Artifact** | Interactive dashboards, real-time exploration, web delivery | Recharts + Tailwind |
| **HTML Artifact** | Standalone interactive charts, shareable files | Chart.js or D3 |
| **Python → PNG/PDF** | Print-ready graphics, reports, presentations | Matplotlib/Seaborn |
| **Python → Interactive** | Notebooks, exploratory analysis | Plotly |

### 2. Choose Chart Type

**Comparison** (values across categories):
- Bar chart: Few categories, discrete comparison
- Grouped bar: Multiple series comparison
- Lollipop: Cleaner alternative to bars

**Trend** (change over time):
- Line chart: Continuous data, multiple series
- Area chart: Emphasize magnitude/cumulative
- Sparkline: Compact trend indicator

**Distribution** (data spread):
- Histogram: Frequency distribution
- Box plot: Quartiles and outliers
- Violin: Distribution shape

**Composition** (parts of whole):
- Pie/Donut: 2-5 categories max, percentages
- Stacked bar: Composition over categories
- Treemap: Hierarchical composition

**Relationship** (correlation):
- Scatter plot: Two variables correlation
- Bubble chart: Three variables
- Heatmap: Matrix relationships

**Geospatial**:
- Choropleth: Regional data
- Point map: Location-based values

## Implementation Patterns

### React Artifact (Recharts)

```jsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', value: 400 },
  { month: 'Feb', value: 300 },
];

export default function Chart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="month" tick={{ fill: '#666' }} />
        <YAxis tick={{ fill: '#666' }} />
        <Tooltip />
        <Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Python Static Export

```python
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

ax.plot(x, y, color='#2563eb', linewidth=2)
ax.set_title('Title', fontsize=14, fontweight='600', pad=20)
ax.set_xlabel('X Label', fontsize=11)
ax.set_ylabel('Y Label', fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('chart.png', bbox_inches='tight', facecolor='white')
```

### HTML Artifact (Chart.js)

```html
<canvas id="chart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
new Chart(document.getElementById('chart'), {
  type: 'bar',
  data: {
    labels: ['A', 'B', 'C'],
    datasets: [{ data: [10, 20, 30], backgroundColor: '#2563eb' }]
  },
  options: { responsive: true, plugins: { legend: { display: false } } }
});
</script>
```

## Design Principles

### Color
- **Sequential**: Single hue gradient for ordered data (light→dark)
- **Diverging**: Two hues for data with meaningful center (blue←white→red)
- **Categorical**: Distinct hues for unordered categories (max 7-8)
- Colorblind-safe: avoid red/green pairs

### Typography
- Title: 14-16px, semibold
- Axis labels: 11-12px, regular
- Annotations: 10-11px
- Sans-serif for clarity (Inter, system-ui)

### Layout
- Data-ink ratio: maximize information, minimize decoration
- White space: generous margins
- Alignment: left-align text, right-align numbers
- Grid: subtle, low contrast

### Accessibility
- Minimum contrast ratio 4.5:1
- Don't rely on color alone—use patterns, labels
- Alt text for static images
- Keyboard navigation for interactive

## Anti-Patterns

- 3D charts (distort perception)
- Pie charts with >5 slices
- Dual Y-axes (misleading)
- Truncated axes (exaggerate)
- Rainbow color scales
- Excessive gridlines

## Dashboard Composition

1. **Hierarchy**: Lead with the key metric
2. **Flow**: Left-to-right, top-to-bottom
3. **Grouping**: Related charts in proximity
4. **Consistency**: Same color encoding throughout
5. **Filtering**: Global filters affect all charts

## Data Preparation Checklist

- [ ] Handle missing values
- [ ] Check for outliers
- [ ] Normalize if comparing scales
- [ ] Sort meaningfully
- [ ] Aggregate appropriately
- [ ] Round display values (2-3 digits)

## Resources

See `references/` for detailed guidance:
- **color-palettes.md**: Curated color schemes for different data types
- **chart-selection.md**: Extended decision tree for complex cases
