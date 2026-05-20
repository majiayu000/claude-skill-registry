---
name: d3js-data-visualization
description: Create interactive, custom data visualizations using d3.js — including charts, graphs, network diagrams, and geographic maps. Use when you need fine-grained control over visual elements, transitions, or interactions beyond what standard charting libraries offer, in any JavaScript environment (vanilla JS, React, Vue, Svelte, etc.).
---

# D3.js Data Visualization

Build sophisticated, interactive data visualizations using d3.js (Data-Driven Documents). D3 binds data to DOM elements and applies data-driven transformations to produce publication-quality, fully customizable visuals.

## When to Use This Skill

- Custom charts requiring unique visual encodings or layouts
- Interactive visualizations with pan, zoom, or brush behaviors
- Network/graph visualizations (force-directed, tree, hierarchy, chord diagrams)
- Geographic visualizations with custom projections
- Smooth, choreographed transitions and animations
- Novel chart types not available in standard libraries (Recharts, Chart.js, etc.)
- Fine-grained SVG styling and accessibility control

**Consider alternatives for:**
- 3D visualizations → use Three.js
- Simple standard charts with minimal customization → use Chart.js or Recharts

## Required Tools / Libraries

No backend required. Runs entirely in the browser or Node.js (with jsdom/canvas).

```bash
# Install via npm
npm install d3

# Or use CDN in HTML
<script src="https://d3js.org/d3.v7.min.js"></script>
```

## Core Workflow

### 1. Set Up D3

```javascript
import * as d3 from 'd3';
```

### 2. Standard Chart Structure

Every d3 visualization follows this pattern:

```javascript
function drawChart(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove(); // clear previous render

  const width = 800, height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Define scales
  const xScale = d3.scaleLinear().domain([0, d3.max(data, d => d.x)]).range([0, innerWidth]);
  const yScale = d3.scaleLinear().domain([0, d3.max(data, d => d.y)]).range([innerHeight, 0]);

  // Axes
  g.append("g").attr("transform", `translate(0,${innerHeight})`).call(d3.axisBottom(xScale));
  g.append("g").call(d3.axisLeft(yScale));

  // Data elements
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
}
```

## Common Chart Patterns

### Bar Chart

```javascript
const xScale = d3.scaleBand().domain(data.map(d => d.category)).range([0, innerWidth]).padding(0.1);
const yScale = d3.scaleLinear().domain([0, d3.max(data, d => d.value)]).range([innerHeight, 0]);

g.selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", d => xScale(d.category))
  .attr("y", d => yScale(d.value))
  .attr("width", xScale.bandwidth())
  .attr("height", d => innerHeight - yScale(d.value))
  .attr("fill", "steelblue");
```

### Line Chart

```javascript
const line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.value))
  .curve(d3.curveMonotoneX);

g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "steelblue")
  .attr("stroke-width", 2)
  .attr("d", line);
```

### Scatter Plot

```javascript
g.selectAll("circle")
  .data(data)
  .join("circle")
  .attr("cx", d => xScale(d.x))
  .attr("cy", d => yScale(d.y))
  .attr("r", d => sizeScale(d.size))
  .attr("fill", d => colorScale(d.category))
  .attr("opacity", 0.7);
```

### Pie / Donut Chart

```javascript
const pie = d3.pie().value(d => d.value).sort(null);
const arc = d3.arc().innerRadius(0).outerRadius(Math.min(width, height) / 2 - 20);
const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

const g = svg.append("g").attr("transform", `translate(${width / 2},${height / 2})`);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => colorScale(i))
  .attr("stroke", "white")
  .attr("stroke-width", 2);
```

### Force-Directed Network Graph

```javascript
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id).distance(100))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2));

const link = g.selectAll("line").data(links).join("line").attr("stroke", "#999");
const node = g.selectAll("circle").data(nodes).join("circle")
  .attr("r", 8).attr("fill", "steelblue")
  .call(d3.drag()
    .on("start", (e) => { if (!e.active) simulation.alphaTarget(0.3).restart(); e.subject.fx = e.subject.x; e.subject.fy = e.subject.y; })
    .on("drag",  (e) => { e.subject.fx = e.x; e.subject.fy = e.y; })
    .on("end",   (e) => { if (!e.active) simulation.alphaTarget(0); e.subject.fx = null; e.subject.fy = null; }));

simulation.on("tick", () => {
  link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("cx", d => d.x).attr("cy", d => d.y);
});
```

### Heatmap

```javascript
// data: [{ row, column, value }, ...]
const rows = [...new Set(data.map(d => d.row))];
const cols = [...new Set(data.map(d => d.column))];

const xScale = d3.scaleBand().domain(cols).range([0, innerWidth]).padding(0.01);
const yScale = d3.scaleBand().domain(rows).range([0, innerHeight]).padding(0.01);
const colorScale = d3.scaleSequential(d3.interpolateYlOrRd).domain([0, d3.max(data, d => d.value)]);

g.selectAll("rect")
  .data(data)
  .join("rect")
  .attr("x", d => xScale(d.column))
  .attr("y", d => yScale(d.row))
  .attr("width", xScale.bandwidth())
  .attr("height", yScale.bandwidth())
  .attr("fill", d => colorScale(d.value));
```

## Interactivity

### Tooltips

```javascript
const tooltip = d3.select("body").append("div")
  .style("position", "absolute")
  .style("visibility", "hidden")
  .style("background", "white")
  .style("border", "1px solid #ddd")
  .style("padding", "10px")
  .style("border-radius", "4px")
  .style("pointer-events", "none");

elements
  .on("mouseover", (event, d) => tooltip.style("visibility", "visible").html(`<strong>${d.label}</strong><br/>Value: ${d.value}`))
  .on("mousemove", (event)    => tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px"))
  .on("mouseout",  ()         => tooltip.style("visibility", "hidden"));
```

### Zoom and Pan

```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => g.attr("transform", event.transform));

svg.call(zoom);
```

### Transitions & Animations

```javascript
// Basic
circles.transition().duration(750).attr("r", 10);

// Staggered
circles.transition().delay((d, i) => i * 50).duration(500).attr("cy", d => yScale(d.value));

// Custom easing
circles.transition().duration(1000).ease(d3.easeBounceOut).attr("r", 10);
```

## Responsive Sizing

```javascript
function setupResponsiveChart(containerId, data) {
  const container = document.getElementById(containerId);
  const svg = d3.select(`#${containerId}`).append('svg');

  const updateChart = () => {
    const { width, height } = container.getBoundingClientRect();
    svg.attr('width', width).attr('height', height);
    drawChart(data, svg, width, height);
  };

  updateChart();
  window.addEventListener('resize', updateChart);
  return () => window.removeEventListener('resize', updateChart);
}
```

## Scale Reference

| Scale | Use case |
|-------|----------|
| `d3.scaleLinear()` | Continuous numeric data |
| `d3.scaleLog()` | Exponential/logarithmic data |
| `d3.scaleTime()` | Date/time axes |
| `d3.scaleBand()` | Bar chart categories |
| `d3.scaleOrdinal()` | Categorical colors |
| `d3.scaleSequential()` | Single-hue color gradients |
| `d3.scaleDiverging()` | Diverging color scales |

## Best Practices

- Always validate data: filter nulls and NaN before binding
- Clear previous render with `svg.selectAll("*").remove()` before redrawing
- Use `.join()` (enter/update/exit in one call) instead of separate selections
- Add ARIA labels (`role="img"`, `aria-label`) for accessibility
- For >1000 elements, consider Canvas rendering instead of SVG
- Debounce resize handlers to avoid excessive redraws
- Define color palettes upfront for visual consistency

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Axes not appearing | Check for NaN in scale domain; verify group transform |
| Transitions not working | Call `.transition()` before attribute changes |
| Responsive sizing broken | Use `ResizeObserver` or update SVG `width`/`height` on resize |
| Performance issues | Switch to Canvas, debounce resize, use `.join()` |

## Related Skills

- `generate-asset-price-chart` — OHLC candlestick chart generation
- `trading-indicators-from-price-data` — Compute indicators to feed into charts
- `free-geocoding-and-maps` — Geographic data for map visualizations
