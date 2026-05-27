---
name: d3js-visualizations
description: Create interactive data visualizations using D3.js for charts, graphs, maps, and custom visual analytics
---

# D3.js Visualizations Skill

Build interactive, web-based data visualizations using D3.js (Data-Driven Documents).

## When to Use
- Interactive charts and graphs
- Custom data visualizations
- Geographic maps
- Network diagrams
- Real-time dashboards

## Core Capabilities
- Bar, line, scatter, area charts
- Force-directed graphs
- Geographic maps (choropleth, bubble maps)
- Hierarchical data (treemaps, sunburst)
- Custom SVG visualizations
- Data transitions and animations
- Interactive tooltips and zoom

## Example: Bar Chart
```javascript
import * as d3 from 'd3';

const data = [30, 86, 168, 281, 303, 365];

const svg = d3.select('svg');
const width = 800;
const height = 400;

const x = d3.scaleBand()
  .domain(data.map((d, i) => i))
  .range([0, width])
  .padding(0.1);

const y = d3.scaleLinear()
  .domain([0, d3.max(data)])
  .range([height, 0]);

svg.selectAll('rect')
  .data(data)
  .join('rect')
  .attr('x', (d, i) => x(i))
  .attr('y', d => y(d))
  .attr('width', x.bandwidth())
  .attr('height', d => height - y(d))
  .attr('fill', 'steelblue');
```

## Best Practices
- Use responsive SVG viewBox
- Optimize for performance (large datasets)
- Add accessible labels
- Implement smooth transitions
- Handle edge cases

## Resources
- D3.js: https://d3js.org/
- Observable: https://observablehq.com/@d3
