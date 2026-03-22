---
name: echarts
description: >-
  Create interactive data visualizations with Apache ECharts. Use when a user asks to build charts, dashboards, or data-driven graphics using ECharts in React, Vue, or vanilla JavaScript applications.
license: Apache-2.0
compatibility: "No special requirements"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["charts", "interactive", "canvas", "dashboard", "analytics"]
---
# ECharts — Enterprise Data Visualization

## Overview

You are an expert in Apache ECharts, the powerful charting library for complex data visualizations. You help developers create interactive dashboards with line, bar, pie, scatter, heatmap, tree, sankey, geographic, and custom chart types with animations, themes, and large dataset support (Canvas + WebGL rendering for millions of data points).

## Instructions

### React Integration

```tsx
// Using echarts-for-react wrapper
import ReactECharts from "echarts-for-react";

function SalesChart({ data }) {
  const option = {
    title: { text: "Monthly Sales", left: "center" },
    tooltip: {
      trigger: "axis",
      formatter: (params) => {
        return params.map(p => `${p.seriesName}: $${p.value.toLocaleString()}`).join("<br/>");
      },
    },
    legend: { bottom: 0, data: ["Revenue", "Costs", "Profit"] },
    xAxis: { type: "category", data: data.map(d => d.month) },
    yAxis: { type: "value", axisLabel: { formatter: "${value}" } },
    series: [
      { name: "Revenue", type: "bar", data: data.map(d => d.revenue), color: "#4f46e5" },
      { name: "Costs", type: "bar", data: data.map(d => d.costs), color: "#ef4444" },
      { name: "Profit", type: "line", data: data.map(d => d.profit), color: "#22c55e",
        smooth: true, areaStyle: { opacity: 0.1 } },
    ],
    toolbox: {
      feature: {
        saveAsImage: {},                  // Download as PNG
        dataZoom: {},                     // Zoom into data
        restore: {},                      // Reset view
      },
    },
    dataZoom: [{ type: "slider", start: 0, end: 100 }],  // Timeline scrubber
  };

  return <ReactECharts option={option} style={{ height: 500 }} />;
}

// Pie chart with drill-down
function CategoryBreakdown({ data }) {
  const option = {
    tooltip: { trigger: "item", formatter: "{b}: {c} ({d}%)" },
    series: [{
      type: "pie",
      radius: ["40%", "70%"],             // Donut chart
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: "#fff", borderWidth: 2 },
      label: { show: true, formatter: "{b}\n{d}%" },
      emphasis: { label: { fontSize: 16, fontWeight: "bold" } },
      data: data.map(d => ({ value: d.count, name: d.category })),
    }],
  };
  return <ReactECharts option={option} style={{ height: 400 }} />;
}

// Real-time streaming chart
function LiveMetrics() {
  const chartRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      const chart = chartRef.current?.getEchartsInstance();
      if (!chart) return;
      // Append new data point, remove oldest
      chart.setOption({
        series: [{ data: [...currentData, newPoint].slice(-60) }],
      });
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return <ReactECharts ref={chartRef} option={baseOption} />;
}
```

### Advanced Charts

```typescript
// Sankey diagram (flow visualization)
const sankeyOption = {
  series: [{
    type: "sankey",
    data: [
      { name: "Organic" }, { name: "Paid" }, { name: "Referral" },
      { name: "Signup" }, { name: "Activation" }, { name: "Paid User" },
    ],
    links: [
      { source: "Organic", target: "Signup", value: 5000 },
      { source: "Paid", target: "Signup", value: 3000 },
      { source: "Referral", target: "Signup", value: 2000 },
      { source: "Signup", target: "Activation", value: 6000 },
      { source: "Signup", target: "Churned", value: 4000 },
      { source: "Activation", target: "Paid User", value: 3500 },
    ],
  }],
};

// Heatmap (calendar-style, like GitHub contributions)
const calendarHeatmap = {
  visualMap: { min: 0, max: 100, type: "piecewise", orient: "horizontal", left: "center" },
  calendar: { range: "2026", cellSize: ["auto", 15] },
  series: [{
    type: "heatmap",
    coordinateSystem: "calendar",
    data: dailyData.map(d => [d.date, d.commits]),
  }],
};
```

## Installation

```bash
npm install echarts echarts-for-react    # React
npm install echarts                       # Vanilla JS
```

## Examples

**Example 1: User asks to set up echarts**

User: "Help me set up echarts for my project"

The agent should:
1. Check system requirements and prerequisites
2. Install or configure echarts
3. Set up initial project structure
4. Verify the setup works correctly

**Example 2: User asks to build a feature with echarts**

User: "Create a dashboard using echarts"

The agent should:
1. Scaffold the component or configuration
2. Connect to the appropriate data source
3. Implement the requested feature
4. Test and validate the output

## Guidelines

1. **echarts-for-react for React** — Use the wrapper for lifecycle management; pass `option` as prop, not imperative API calls
2. **Canvas for large data** — ECharts uses Canvas by default; it handles 100K+ points smoothly; switch to WebGL for millions
3. **Toolbox for interaction** — Enable `saveAsImage`, `dataZoom`, `restore` in the toolbox; users expect to zoom and download
4. **Responsive resize** — ECharts auto-resizes with the container; wrap in a div with CSS width/height
5. **Theme system** — Use ECharts themes for consistent styling across charts; create custom themes at https://echarts.apache.org/en/theme-builder.html
6. **Lazy rendering** — Use `lazyUpdate={true}` in React for performance; prevents unnecessary re-renders
7. **Dataset for shared data** — Use ECharts `dataset` component when multiple series share the same data source
8. **Server-side rendering** — Use `echarts-node-export` for generating chart images server-side (reports, emails)
