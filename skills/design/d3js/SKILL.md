---
name: d3js
version: 1.0.0
description: Create custom, highly interactive data visualizations with D3.js (Data-Driven Documents)
author: workspace-hub
category: data-visualization
tags: [charts, d3, svg, interactive, custom-viz]
platforms: [web, javascript]
---

# D3.js Data Visualization Skill

Create powerful, custom data visualizations using D3.js for complete control over SVG elements, transitions, and data binding.

## When to Use This Skill

Use D3.js when you need:
- **Complete customization** - Every aspect of the visualization controlled
- **Complex interactions** - Advanced user interactions and transitions
- **Unique visualizations** - Bespoke charts not available in other libraries
- **Data-driven DOM manipulation** - Direct binding of data to DOM elements
- **Custom animations** - Sophisticated transitions and effects

**Avoid when:**
- Simple charts with default styling are sufficient (use Chart.js)
- Quick implementation is priority (use Plotly or Chart.js)
- Team lacks JavaScript expertise

## Core Capabilities

### 1. Data Binding
```javascript
// Select and bind data to elements
d3.select('#chart')
  .selectAll('circle')
  .data(dataset)
  .enter()
  .append('circle')
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y))
  .attr('r', d => d.radius)
  .style('fill', d => colorScale(d.category));
```

### 2. Scales and Axes
```javascript
// Create scales for positioning
const xScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.x)])
  .range([0, width]);

const yScale = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.y)])
  .range([height, 0]);

// Create axes
const xAxis = d3.axisBottom(xScale);
const yAxis = d3.axisLeft(yScale);

svg.append('g')
  .attr('transform', `translate(0, ${height})`)
  .call(xAxis);

svg.append('g')
  .call(yAxis);
```

### 3. Transitions and Animations
```javascript
// Smooth transitions
d3.selectAll('circle')
  .transition()
  .duration(1000)
  .attr('r', d => d.newRadius)
  .style('fill', 'steelblue');
```

### 4. Interactive Elements
```javascript
// Add interactivity
const tooltip = d3.select('body')
  .append('div')
  .attr('class', 'tooltip')
  .style('opacity', 0);

circles
  .on('mouseover', function(event, d) {
    tooltip.transition()
      .duration(200)
      .style('opacity', .9);
    tooltip.html(`Value: ${d.value}`)
      .style('left', (event.pageX + 10) + 'px')
      .style('top', (event.pageY - 28) + 'px');
  })
  .on('mouseout', function(d) {
    tooltip.transition()
      .duration(500)
      .style('opacity', 0);
  });
```

## Complete Examples

### Example 1: Interactive Bar Chart
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    .bar { fill: steelblue; cursor: pointer; }
    .bar:hover { fill: orange; }
    .tooltip {
      position: absolute;
      padding: 10px;
      background: rgba(0,0,0,0.8);
      color: white;
      border-radius: 5px;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div id="chart"></div>
  <script>
    // Data
    const data = [
      { category: 'A', value: 30 },
      { category: 'B', value: 80 },
      { category: 'C', value: 45 },
      { category: 'D', value: 60 },
      { category: 'E', value: 20 }
    ];

    // Dimensions
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select('#chart')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleBand()
      .domain(data.map(d => d.category))
      .range([0, width])
      .padding(0.1);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .range([height, 0]);

    // Axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale));

    svg.append('g')
      .call(d3.axisLeft(yScale));

    // Tooltip
    const tooltip = d3.select('body')
      .append('div')
      .attr('class', 'tooltip')
      .style('opacity', 0);

    // Bars
    svg.selectAll('.bar')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', d => xScale(d.category))
      .attr('y', d => yScale(d.value))
      .attr('width', xScale.bandwidth())
      .attr('height', d => height - yScale(d.value))
      .on('mouseover', function(event, d) {
        d3.select(this).style('fill', 'orange');
        tooltip.transition().duration(200).style('opacity', .9);
        tooltip.html(`${d.category}: ${d.value}`)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 28) + 'px');
      })
      .on('mouseout', function(d) {
        d3.select(this).style('fill', 'steelblue');
        tooltip.transition().duration(500).style('opacity', 0);
      });
  </script>
</body>
</html>
```

### Example 2: Animated Line Chart with CSV Data
```javascript
// Load and visualize CSV data
d3.csv('../data/timeseries.csv').then(data => {
  // Parse dates and values
  const parseDate = d3.timeParse('%Y-%m-%d');
  data.forEach(d => {
    d.date = parseDate(d.date);
    d.value = +d.value;
  });

  // Scales
  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, width]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([height, 0]);

  // Line generator
  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);

  // Draw line with animation
  const path = svg.append('path')
    .datum(data)
    .attr('class', 'line')
    .attr('d', line)
    .style('fill', 'none')
    .style('stroke', 'steelblue')
    .style('stroke-width', 2);

  // Animate path
  const totalLength = path.node().getTotalLength();
  path
    .attr('stroke-dasharray', totalLength + ' ' + totalLength)
    .attr('stroke-dashoffset', totalLength)
    .transition()
    .duration(2000)
    .ease(d3.easeLinear)
    .attr('stroke-dashoffset', 0);

  // Add dots
  svg.selectAll('.dot')
    .data(data)
    .enter()
    .append('circle')
    .attr('class', 'dot')
    .attr('cx', d => xScale(d.date))
    .attr('cy', d => yScale(d.value))
    .attr('r', 0)
    .style('fill', 'steelblue')
    .transition()
    .delay((d, i) => i * 50)
    .duration(500)
    .attr('r', 4);
});
```

### Example 3: Force-Directed Network Graph
```javascript
// Network data
const nodes = [
  { id: 'A', group: 1 },
  { id: 'B', group: 1 },
  { id: 'C', group: 2 },
  { id: 'D', group: 2 },
  { id: 'E', group: 3 }
];

const links = [
  { source: 'A', target: 'B', value: 1 },
  { source: 'B', target: 'C', value: 2 },
  { source: 'C', target: 'D', value: 1 },
  { source: 'D', target: 'E', value: 3 },
  { source: 'E', target: 'A', value: 2 }
];

// Create force simulation
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d => d.id))
  .force('charge', d3.forceManyBody().strength(-200))
  .force('center', d3.forceCenter(width / 2, height / 2));

// Draw links
const link = svg.append('g')
  .selectAll('line')
  .data(links)
  .enter()
  .append('line')
  .style('stroke', '#999')
  .style('stroke-width', d => Math.sqrt(d.value));

// Draw nodes
const node = svg.append('g')
  .selectAll('circle')
  .data(nodes)
  .enter()
  .append('circle')
  .attr('r', 10)
  .style('fill', d => d3.schemeCategory10[d.group])
  .call(d3.drag()
    .on('start', dragstarted)
    .on('drag', dragged)
    .on('end', dragended));

// Add labels
const label = svg.append('g')
  .selectAll('text')
  .data(nodes)
  .enter()
  .append('text')
  .text(d => d.id)
  .style('font-size', '12px')
  .attr('dx', 12)
  .attr('dy', 4);

// Update positions on tick
simulation.on('tick', () => {
  link
    .attr('x1', d => d.source.x)
    .attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x)
    .attr('y2', d => d.target.y);

  node
    .attr('cx', d => d.x)
    .attr('cy', d => d.y);

  label
    .attr('x', d => d.x)
    .attr('y', d => d.y);
});

// Drag functions
function dragstarted(event, d) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(event, d) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragended(event, d) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
```

## Best Practices

### 1. Use Proper Margins Convention
```javascript
const margin = { top: 20, right: 20, bottom: 30, left: 40 };
const width = 960 - margin.left - margin.right;
const height = 500 - margin.top - margin.bottom;

const svg = d3.select('body').append('svg')
  .attr('width', width + margin.left + margin.right)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', `translate(${margin.left},${margin.top})`);
```

### 2. Use Method Chaining
```javascript
// Good - readable chaining
svg.selectAll('circle')
  .data(data)
  .enter()
  .append('circle')
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y))
  .attr('r', 5);
```

### 3. Separate Data from Presentation
```javascript
// Load data separately
d3.json('../data/data.json').then(data => {
  visualize(data);
});

function visualize(data) {
  // Visualization logic here
}
```

### 4. Use Responsive Design
```javascript
// Make chart responsive
function resize() {
  const container = d3.select('#chart').node();
  const width = container.getBoundingClientRect().width;

  xScale.range([0, width]);
  svg.attr('width', width);
  // Update chart elements
}

window.addEventListener('resize', resize);
```

## Common Patterns

### Update Pattern (Enter, Update, Exit)
```javascript
function update(data) {
  // Bind data
  const circles = svg.selectAll('circle')
    .data(data, d => d.id);

  // EXIT: Remove old elements
  circles.exit()
    .transition()
    .duration(500)
    .attr('r', 0)
    .remove();

  // UPDATE: Update existing elements
  circles
    .transition()
    .duration(500)
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y));

  // ENTER: Add new elements
  circles.enter()
    .append('circle')
    .attr('r', 0)
    .attr('cx', d => xScale(d.x))
    .attr('cy', d => yScale(d.y))
    .transition()
    .duration(500)
    .attr('r', 5);
}
```

### Brush and Zoom
```javascript
// Add zoom behavior
const zoom = d3.zoom()
  .scaleExtent([1, 10])
  .on('zoom', zoomed);

svg.call(zoom);

function zoomed(event) {
  const transform = event.transform;
  svg.attr('transform', transform);
}

// Add brush selection
const brush = d3.brush()
  .extent([[0, 0], [width, height]])
  .on('end', brushed);

svg.append('g')
  .attr('class', 'brush')
  .call(brush);

function brushed(event) {
  if (!event.selection) return;
  const [[x0, y0], [x1, y1]] = event.selection;
  // Handle selected region
}
```

## Installation & Setup

### CDN (Quick Start)
```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

### NPM (Production)
```bash
npm install d3
```

```javascript
import * as d3 from 'd3';
// Or import specific modules
import { select, scaleLinear, axisBottom } from 'd3';
```

## Performance Tips

1. **Minimize DOM operations** - Batch updates when possible
2. **Use canvas for large datasets** - Switch to canvas for >1000 points
3. **Throttle events** - Debounce mousemove/scroll events
4. **Optimize transitions** - Limit concurrent animations
5. **Use web workers** - Offload heavy computations

## Resources

- **Official Docs**: https://d3js.org/
- **Observable**: https://observablehq.com/@d3 (Interactive examples)
- **GitHub**: https://github.com/d3/d3
- **Gallery**: https://observablehq.com/@d3/gallery

## Integration with Other Tools

### With React
```javascript
import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

function D3Chart({ data }) {
  const svgRef = useRef();

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    // D3 code here
  }, [data]);

  return <svg ref={svgRef}></svg>;
}
```

### With CSV/JSON Data
```javascript
// Load from relative path
d3.csv('../data/data.csv').then(data => {
  // Process and visualize
});

d3.json('../data/data.json').then(data => {
  // Visualize JSON
});
```

---

**Use this skill when you need maximum control and customization in your data visualizations!**
