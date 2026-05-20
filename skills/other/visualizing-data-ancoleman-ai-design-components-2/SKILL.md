---
name: visualizing-data
description: Builds dashboards, reports, and data-driven interfaces requiring charts, graphs, or visual analytics. Provides systematic framework for selecting appropriate visualizations based on data characteristics and analytical purpose. Includes 24+ visualization types organized by purpose (trends, comparisons, distributions, relationships, flows, hierarchies, geospatial), accessibility patterns (WCAG 2.1 AA compliance), colorblind-safe palettes, and performance optimization strategies. Use when creating visualizations, choosing chart types, displaying data graphically, or designing data interfaces.
---

# Data Visualization Component Library

Systematic guidance for selecting and implementing effective data visualizations, matching data characteristics with appropriate visualization types, ensuring clarity, accessibility, and impact.

## Overview

Data visualization transforms raw data into visual representations that reveal patterns, trends, and insights. This skill provides:

1. **Selection Framework**: Systematic decision trees from data type + purpose → chart type
2. **24+ Visualization Methods**: Organized by analytical purpose
3. **Accessibility Patterns**: WCAG 2.1 AA compliance, colorblind-safe palettes
4. **Performance Strategies**: Optimize for dataset size (<1000 to >100K points)
5. **Multi-Language Support**: JavaScript/TypeScript (primary), Python, Rust, Go

---

## Quick Start Workflow

### Step 1: Assess Data
```
What type? [categorical | continuous | temporal | spatial | hierarchical]
How many dimensions? [1D | 2D | multivariate]
How many points? [<100 | 100-1K | 1K-10K | >10K]
```

### Step 2: Determine Purpose
```
What story to tell? [comparison | trend | distribution | relationship | composition | flow | hierarchy | geographic]
```

### Step 3: Select Chart Type

**Quick Selection:**
- Compare 5-10 categories → Bar Chart
- Show sales over 12 months → Line Chart
- Display distribution of ages → Histogram or Violin Plot
- Explore correlation → Scatter Plot
- Show budget breakdown → Treemap or Stacked Bar

**Complete decision trees:** See `references/selection-matrix.md`

### Step 4: Implement

See language sections below for recommended libraries.

### Step 5: Apply Accessibility
- Add text alternative (aria-label)
- Ensure 3:1 color contrast minimum
- Use colorblind-safe palette
- Provide data table alternative

### Step 6: Optimize Performance
- <1000 points: Standard SVG rendering
- >1000 points: Sampling or Canvas rendering
- Very large: Server-side aggregation

---

## Purpose-First Selection

**Match analytical purpose to chart type:**

| Purpose | Chart Types |
|---------|-------------|
| **Compare values** | Bar Chart, Lollipop Chart |
| **Show trends** | Line Chart, Area Chart |
| **Reveal distributions** | Histogram, Violin Plot, Box Plot |
| **Explore relationships** | Scatter Plot, Bubble Chart |
| **Explain composition** | Treemap, Stacked Bar, Pie Chart (<6 slices) |
| **Visualize flow** | Sankey Diagram, Chord Diagram |
| **Display hierarchy** | Sunburst, Dendrogram, Treemap |
| **Show geographic** | Choropleth Map, Symbol Map |

---

## Visualization Catalog

### Tier 1: Fundamental Primitives
General audiences, straightforward data stories:
- **Bar Chart**: Compare categories
- **Line Chart**: Show trends over time
- **Scatter Plot**: Explore relationships
- **Pie Chart**: Part-to-whole (max 5-6 slices)
- **Area Chart**: Emphasize magnitude over time

### Tier 2: Purpose-Driven
Specific analytical insights:
- **Comparison**: Grouped Bar, Lollipop, Bullet Chart
- **Trend**: Stream Graph, Slope Graph, Sparklines
- **Distribution**: Violin Plot, Box Plot, Histogram
- **Relationship**: Bubble Chart, Hexbin Plot
- **Composition**: Treemap, Sunburst, Waterfall
- **Flow**: Sankey Diagram, Chord Diagram

### Tier 3: Advanced
Complex data, sophisticated audiences:
- **Multi-dimensional**: Parallel Coordinates, Radar Chart, Small Multiples
- **Temporal**: Gantt Chart, Calendar Heatmap, Candlestick
- **Network**: Force-Directed Graph, Adjacency Matrix

**Detailed descriptions:** See `references/chart-catalog.md`

---

## Accessibility Requirements (WCAG 2.1 AA)

### Text Alternatives
```html
<figure role="img" aria-label="Sales increased 15% from Q3 to Q4">
  <svg>...</svg>
</figure>
```

### Color Requirements
- Non-text UI elements: 3:1 minimum contrast
- Text: 4.5:1 minimum (or 3:1 for large text ≥24px)
- Don't rely on color alone - use patterns/textures + labels

### Colorblind-Safe Palettes

**IBM Palette (Recommended):**
```
#648FFF (Blue), #785EF0 (Purple), #DC267F (Magenta),
#FE6100 (Orange), #FFB000 (Yellow)
```

**Avoid:** Red/Green combinations (8% of males have red-green colorblindness)

### Keyboard Navigation
- Tab through interactive elements
- Enter/Space to activate tooltips
- Arrow keys to navigate data points

**Complete accessibility guide:** See `references/accessibility.md`

---

## Performance by Data Volume

| Rows | Strategy | Implementation |
|------|----------|----------------|
| <1,000 | Direct rendering | Standard libraries (SVG) |
| 1K-10K | Sampling/aggregation | Downsample to ~500 points |
| 10K-100K | Canvas rendering | Switch from SVG to Canvas |
| >100K | Server-side aggregation | Backend processing |

---

## JavaScript/TypeScript Implementation

### Recharts (Business Dashboards)
Composable React components, declarative API, responsive by default.

```bash
npm install recharts
```

```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', sales: 4000 },
  { month: 'Feb', sales: 3000 },
  { month: 'Mar', sales: 5000 },
];

export function SalesChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="sales" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### D3.js (Custom Visualizations)
Maximum flexibility, industry standard, unlimited chart types.

```bash
npm install d3
```

### Plotly (Scientific/Interactive)
3D visualizations, statistical charts, interactive out-of-box.

```bash
npm install react-plotly.js plotly.js
```

**Detailed examples:** See `references/javascript/`

---

## Python Implementation

**Common Libraries:**
- **Plotly** - Interactive charts (same API as JavaScript)
- **Matplotlib** - Publication-quality static plots
- **Seaborn** - Statistical visualizations
- **Altair** - Declarative visualization grammar

**When building Python implementations:**
1. Follow universal patterns above
2. Use RESEARCH_GUIDE.md to research libraries
3. Add to `references/python/`

---

## Integration with Design Tokens

Reference the **design-tokens** skill for theming:

```css
--chart-color-primary
--chart-color-1 through --chart-color-10
--chart-axis-color
--chart-grid-color
--chart-tooltip-bg
```

```tsx
<Line stroke="var(--chart-color-primary)" />
```

Light/dark/high-contrast themes work automatically via design tokens.

---

## Common Mistakes to Avoid

1. **Chart-first thinking** - Choose based on data + purpose, not aesthetics
2. **Pie charts for >6 categories** - Use sorted bar chart instead
3. **Dual-axis charts** - Usually misleading, use small multiples
4. **3D when 2D sufficient** - Adds complexity, reduces clarity
5. **Rainbow color scales** - Not perceptually uniform, not colorblind-safe
6. **Truncated y-axis** - Indicate clearly or start at zero
7. **Too many colors** - Limit to 6-8 distinct categories
8. **Missing context** - Always label axes, include units

---

## Quick Decision Tree

```
START: What is your data?

Categorical (categories/groups)
  ├─ Compare values → Bar Chart
  ├─ Show composition → Treemap or Pie Chart (<6 slices)
  └─ Show flow → Sankey Diagram

Continuous (numbers)
  ├─ Single variable → Histogram, Violin Plot
  └─ Two variables → Scatter Plot

Temporal (time series)
  ├─ Single metric → Line Chart
  ├─ Multiple metrics → Small Multiples
  └─ Daily patterns → Calendar Heatmap

Hierarchical (nested)
  ├─ Proportions → Treemap
  └─ Show depth → Sunburst, Dendrogram

Geographic (locations)
  ├─ Regional aggregates → Choropleth Map
  └─ Point locations → Symbol Map
```

---

## References

**Selection Guides:**
- `references/chart-catalog.md` - All 24+ visualization types
- `references/selection-matrix.md` - Complete decision trees

**Technical Guides:**
- `references/accessibility.md` - WCAG 2.1 AA patterns
- `references/color-systems.md` - Colorblind-safe palettes
- `references/performance.md` - Optimization by data volume

**Language-Specific:**
- `references/javascript/` - React, D3.js, Plotly examples
- `references/python/` - Plotly, Matplotlib, Seaborn

**Assets:**
- `assets/color-palettes/` - Accessible color schemes
- `assets/example-datasets/` - Sample data for testing

---

## Examples

**Working code examples:**
- `examples/javascript/bar-chart.tsx`
- `examples/javascript/line-chart.tsx`
- `examples/javascript/scatter-plot.tsx`
- `examples/javascript/accessible-chart.tsx`

```bash
cd examples/javascript && npm install && npm start
```

---

## Validation

```bash
# Validate accessibility
scripts/validate_accessibility.py <chart-html>

# Test colorblind
# Use browser DevTools color vision deficiency emulator
```

---

**Progressive disclosure:** This SKILL.md provides overview and quick start. Detailed documentation, code examples, and language-specific implementations in `references/` and `examples/` directories.
