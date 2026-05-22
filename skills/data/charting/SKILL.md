---
name: charting
description: Select the right Python charting library (seaborn, matplotlib, graphviz) and produce publication-quality static visualizations. Use when creating charts, plots, graphs, diagrams, heatmaps, visualizations from data, or when choosing between matplotlib/seaborn/graphviz. Also triggers for network diagrams, flowcharts, dependency trees, state machines, and entity-relationship diagrams. For interactive browser-rendered charts or uploaded data exploration, defer to charting-vega-lite instead.
metadata:
  version: 0.1.0
---

# Charting: Python Static Visualizations

Select the optimal Python charting library and produce clean, publication-quality output.

## Library Selection Framework

Choose the library based on what the visualization represents, not habit.

### Seaborn — DEFAULT for statistical/analytical charts

Seaborn wraps matplotlib with better defaults, tighter pandas integration, and fewer lines of code. Reach for seaborn first when the data lives in a DataFrame and the goal is analytical.

**Use for:** distributions (histograms, KDEs, violin plots, ECDFs), categorical comparisons (box plots, swarm plots, strip plots, bar plots), correlation (heatmaps, pair plots, regression plots), grouped/faceted views (`FacetGrid`, `catplot`, `relplot`).

**Why:** Automatic axis labeling from column names, coherent color palettes, built-in aggregation with confidence intervals, and `hue`/`col`/`row` faceting with minimal code.

**Practical rule:** If the code would call `plt.bar()`, `plt.hist()`, `plt.scatter()`, or build a heatmap with `plt.imshow()` — use the seaborn equivalent instead. It will look better with less effort.

### Matplotlib — fine-grained control and non-standard layouts

Drop to raw matplotlib only when seaborn doesn't support the chart type or when pixel-level layout control is required.

**Use for:** custom multi-panel figures mixing chart types, unusual annotations (arrows, shaded regions, custom legends), non-standard axes (polar, broken axes, insets), animations, image overlays, or any layout where the default seaborn API is insufficient.

**Combine with seaborn:** Seaborn plots return matplotlib `Axes` objects. Apply matplotlib customization on top of seaborn output rather than rebuilding from scratch.

### Graphviz — graph/network structures

Graphviz operates in a fundamentally different domain: nodes and edges, not x/y data.

**Use for:** dependency trees, flowcharts, state machines, org charts, entity-relationship diagrams, DAGs, call graphs, any directed or undirected graph structure.

**Python interface:** Use the `graphviz` Python package (installed). Create `graphviz.Digraph()` or `graphviz.Graph()`, add nodes/edges, render to PNG/SVG/PDF.

```python
import graphviz
g = graphviz.Digraph(format='png')
g.node('A', 'Start')
g.node('B', 'Process')
g.edge('A', 'B')
g.render('/home/claude/output', cleanup=True)
```

**Layout engines:** `dot` (hierarchical, default), `neato` (spring model), `fdp` (force-directed), `circo` (circular), `twopi` (radial). Set via `g.engine = 'neato'`.

### Vega-Lite — interactive browser charts

When the user wants interactive, browser-rendered visualizations (tooltips, zoom, selection, filtering) or uploads data for exploratory charting, defer to the `charting-vega-lite` skill. That skill handles React artifact generation with inline data islands.

**Decision shortcut:** Static image file → this skill. Interactive artifact → charting-vega-lite.

## Quick Reference: Chart Type → Library

| Need | Library | Function |
|---|---|---|
| Histogram / KDE | seaborn | `sns.histplot()`, `sns.kdeplot()` |
| Box / Violin / Swarm | seaborn | `sns.boxplot()`, `sns.violinplot()` |
| Bar (categorical) | seaborn | `sns.barplot()`, `sns.countplot()` |
| Correlation heatmap | seaborn | `sns.heatmap()` |
| Scatter + regression | seaborn | `sns.scatterplot()`, `sns.regplot()` |
| Pair plot (multi-var) | seaborn | `sns.pairplot()` |
| Faceted grid | seaborn | `sns.FacetGrid`, `catplot`, `relplot` |
| Time series line | seaborn | `sns.lineplot()` (handles CI bands) |
| Custom multi-panel | matplotlib | `fig, axes = plt.subplots()` |
| Polar / radar | matplotlib | `projection='polar'` |
| Annotated diagrams | matplotlib | `ax.annotate()`, arrows, patches |
| Dependency tree | graphviz | `Digraph` |
| Flowchart / FSM | graphviz | `Digraph` with shape attrs |
| ER diagram | graphviz | `Graph` with record shapes |
| Network graph | graphviz | `Graph` with layout engine |

## Production Defaults

Apply these defaults to produce clean output without per-chart fiddling.

### Seaborn Setup
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
```

Style options: `whitegrid` (default, good for most), `white` (cleaner for publications), `darkgrid` (data-dense plots), `ticks` (minimal).

### Figure Sizing and DPI
```python
fig, ax = plt.subplots(figsize=(10, 6))
# Or for seaborn figure-level functions:
g = sns.catplot(..., height=6, aspect=1.5)

# Save at publication quality
plt.savefig('/home/claude/chart.png', dpi=150, bbox_inches='tight', facecolor='white')
```

Use `dpi=150` for screen/web output, `dpi=300` for print. Always use `bbox_inches='tight'` to avoid clipped labels.

### Color Guidance
- Categorical: `"muted"`, `"Set2"`, `"tab10"` — distinct, accessible
- Sequential: `"viridis"`, `"YlOrRd"`, `"Blues"` — ordered magnitude
- Diverging: `"RdBu"`, `"coolwarm"` — centered on zero/midpoint
- Avoid: `"jet"`, `"rainbow"` — perceptually non-uniform, colorblind-hostile

### Common Refinements
```python
# Rotate x-labels if overlapping
plt.xticks(rotation=45, ha='right')

# Remove top/right spines for cleaner look
sns.despine()

# Thousands separator for large numbers
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
```

## Output Workflow

1. Create chart in `/home/claude/`
2. Save as PNG (default) or SVG (if user needs vector)
3. Copy to `/mnt/user-data/outputs/`
4. Present via `present_files`

Always `plt.close()` after saving to free memory.
