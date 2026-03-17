---
name: d3-viz
description: Create interactive data visualizations using D3.js. Use this when creating charts, graphs, network diagrams, geographic visualizations, or custom SVG-based data visualization.
allowed-tools: Read, Glob, Grep, Edit, Write
license: MIT
metadata:
  author: chrisvoncsefalvay
  version: "1.0"
---

# D3.js Visualization

D3.js를 사용한 인터랙티브 데이터 시각화 가이드입니다.

## When to Use D3.js

**적합한 경우:**
- 커스텀 차트 (표준 라이브러리에 없는)
- 인터랙티브 탐색 (pan, zoom, brush)
- 네트워크/그래프 시각화
- 지리 시각화 (커스텀 projection)
- 애니메이션 transition
- 출판 품질 그래픽

**대안 고려:**
- 3D 시각화 → Three.js
- 간단한 차트 → Chart.js, Recharts

## Setup

```javascript
// npm
import * as d3 from 'd3';

// CDN
<script src="https://d3js.org/d3.v7.min.js"></script>
```

## Core Workflow

```javascript
function drawVisualization(data) {
  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove(); // Clear previous

  // 1. Dimensions
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // 2. Main group with margins
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // 3. Scales
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);

  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);

  // 4. Axes
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));

  g.append("g")
    .call(d3.axisLeft(yScale));

  // 5. Data binding
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
}
```

## Common Patterns

### Bar Chart
```javascript
const xScale = d3.scaleBand()
  .domain(data.map(d => d.category))
  .range([0, innerWidth])
  .padding(0.1);

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

### Pie Chart
```javascript
const pie = d3.pie().value(d => d.value);
const arc = d3.arc()
  .innerRadius(0)
  .outerRadius(Math.min(width, height) / 2 - 20);

g.selectAll("path")
  .data(pie(data))
  .join("path")
  .attr("d", arc)
  .attr("fill", (d, i) => d3.schemeCategory10[i]);
```

## Interactivity

### Tooltips
```javascript
const tooltip = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("visibility", "hidden");

circles
  .on("mouseover", (event, d) => {
    tooltip.style("visibility", "visible")
      .html(`Value: ${d.value}`);
  })
  .on("mousemove", (event) => {
    tooltip
      .style("top", (event.pageY - 10) + "px")
      .style("left", (event.pageX + 10) + "px");
  })
  .on("mouseout", () => {
    tooltip.style("visibility", "hidden");
  });
```

### Zoom & Pan
```javascript
const zoom = d3.zoom()
  .scaleExtent([0.5, 10])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom);
```

## Transitions

```javascript
// Basic
circles.transition()
  .duration(750)
  .attr("r", 10);

// Staggered
circles.transition()
  .delay((d, i) => i * 50)
  .duration(500)
  .attr("cy", d => yScale(d.value));
```

## Scales Reference

| Scale Type | Use Case |
|------------|----------|
| `scaleLinear` | 연속 수치 |
| `scaleLog` | 지수 데이터 |
| `scaleTime` | 시간/날짜 |
| `scaleBand` | Bar chart 카테고리 |
| `scaleOrdinal` | 색상 매핑 |
| `scaleSequential` | 연속 색상 |

## Color Schemes

```javascript
// Categorical
d3.schemeCategory10  // 10 colors
d3.schemeTableau10   // Tableau 10

// Sequential
d3.interpolateBlues
d3.interpolateYlOrRd

// Diverging
d3.interpolateRdBu
```

## Best Practices

1. **Data Validation**: null/NaN 체크
2. **Responsive**: ResizeObserver 사용
3. **Performance**: 1000+ 요소 시 Canvas 고려
4. **Accessibility**: ARIA labels 추가
5. **Clean Up**: 이전 렌더링 제거
