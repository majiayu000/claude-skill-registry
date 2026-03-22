---
name: d3
description: >-
  Assists with building custom interactive data visualizations using D3.js. Use when creating
  charts, graphs, maps, force layouts, or hierarchical diagrams that require fine-grained
  control beyond what charting libraries provide. Trigger words: d3, data visualization,
  chart, svg, scales, force graph, treemap, choropleth.
license: Apache-2.0
compatibility: "No special requirements"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: design
  tags: ["d3", "data-visualization", "charts", "svg", "interactive"]
---

# D3.js

## Overview

D3.js is a low-level JavaScript library for building custom, interactive data visualizations by binding data to DOM elements. It provides scales, axes, shape generators, geographic projections, force simulations, and hierarchical layouts, giving developers full control over the visual output while integrating with React through computed scales and layouts.

## Instructions

- When binding data, use `.data(dataset).join("element")` (D3 v6+) for the enter/update/exit pattern, setting attributes and styles from bound data via accessor functions.
- When creating scales, choose the appropriate type (`scaleLinear` for continuous, `scaleBand` for categorical bars, `scaleTime` for dates, `scaleOrdinal` for color mapping) and always set domain from the data using `d3.extent()`.
- When building axes, create them with `d3.axisBottom(scale)` or `d3.axisLeft(scale)`, configure ticks and format labels with `d3.format()`, and regenerate on resize.
- When creating chart types, use shape generators (`d3.line()`, `d3.area()`, `d3.arc()`, `d3.pie()`, `d3.stack()`) and layout functions (`d3.treemap()`, `d3.forceSimulation()`, `d3.geoPath()`) for complex visualizations.
- When adding interactivity, use transitions (`.transition().duration(750)`) for smooth data updates, tooltips on hover, and brushing/zooming for exploration.
- When integrating with React, use D3 for math (scales, layouts, data transforms) and React for DOM rendering, computing values in `useMemo` and using `useEffect` with refs for D3-driven animations.

## Examples

### Example 1: Build a real-time dashboard with multiple chart types

**User request:** "Create a dashboard with line charts, bar charts, and a pie chart from API data"

**Actions:**
1. Set up shared scales with `d3.scaleTime()` for the x-axis and `d3.scaleLinear()` for the y-axis
2. Build a line chart using `d3.line()` with smooth curve interpolation and area fill
3. Build a grouped bar chart using `d3.scaleBand()` with staggered enter transitions
4. Build a donut chart using `d3.pie()` and `d3.arc()` with hover tooltips

**Output:** A responsive dashboard with animated charts that update smoothly when data changes.

### Example 2: Create a force-directed network graph

**User request:** "Visualize relationships between entities as an interactive network graph"

**Actions:**
1. Set up `d3.forceSimulation()` with `forceManyBody`, `forceLink`, and `forceCenter`
2. Render nodes as circles with `d3.scaleOrdinal()` coloring by category
3. Add drag interaction with `d3.drag()` to reposition nodes
4. Implement zoom and pan with `d3.zoom()` and tooltips on hover

**Output:** An interactive force-directed graph with draggable nodes, color-coded categories, and zoom navigation.

## Guidelines

- Use D3 for scales, layouts, and data processing; let React handle DOM rendering in React apps.
- Use `.join()` instead of manual enter/update/exit for simpler, cleaner data binding.
- Always set scale domains from data (`d3.extent()`) rather than hardcoding ranges.
- Use `d3.format()` for axis labels and tooltips: `",.0f"` for thousands, `"$.2f"` for currency.
- Add transitions of 750ms with `easeCubicInOut` for smooth data update animations.
- Make visualizations responsive by recalculating scales on `ResizeObserver` callbacks.
- Add `aria-label` to SVG elements and meaningful `<title>` tags for accessibility.
