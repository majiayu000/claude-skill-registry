---
name: mui-x-charts
description: "MUI X Charts for data visualization in React applications. Line charts, bar charts, pie charts, customization, theming. Trigger: When creating data visualizations with MUI X Charts, implementing charts, or customizing chart appearance."
skills:
  - mui
  - react
  - typescript
  - humanizer
dependencies:
  "@mui/x-charts": ">=6.0.0 <8.0.0"
  react: ">=17.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# MUI X Charts Skill

## Overview

Guidance for implementing data visualizations using MUI X Charts in React applications.

## Objective

Enable developers to create accessible, responsive charts and graphs using MUI X Charts library.

---

## When to Use

Use this skill when:

- Creating data visualizations in MUI-based React apps
- Implementing line, bar, pie, or scatter charts
- Needing theme-aware charts that match MUI design
- Building responsive, interactive charts

Don't use this skill for:

- Complex visualizations (consider D3.js or Chart.js)
- Non-MUI projects (use other chart libraries)
- Real-time streaming data (limited support)

---

## Critical Patterns

### ✅ REQUIRED: Provide Axis Labels and Legends

```typescript
// ✅ CORRECT: Descriptive labels
<LineChart
  xAxis={[{ label: 'Month', data: months }]}
  yAxis={[{ label: 'Revenue ($)' }]}
  series={[{ data: revenue, label: 'Q1 2024' }]}
/>

// ❌ WRONG: No labels (inaccessible)
<LineChart
  xAxis={[{ data: months }]}
  series={[{ data: revenue }]}
/>
```

### ✅ REQUIRED: Use Responsive Sizing

```typescript
// ✅ CORRECT: Container-based sizing
<Box sx={{ width: '100%', height: 400 }}>
  <LineChart /* ... */ />
</Box>

// ❌ WRONG: Fixed pixel sizes
<LineChart width={800} height={400} />
```

### ✅ REQUIRED: Ensure Color Contrast

```typescript
// ✅ CORRECT: Use theme colors with good contrast
<LineChart
  series={[
    { data: data1, color: theme.palette.primary.main },
    { data: data2, color: theme.palette.secondary.main },
  ]}
/>
```

---

## Conventions

Refer to mui for:

- Theme integration
- Component patterns

Refer to react for:

- Component structure
- Hooks usage

### MUI X Charts Specific

- Choose appropriate chart type for data
- Implement responsive sizing
- Provide proper axis labels and legends
- Handle loading and error states
- Ensure color contrast for accessibility

---

## Decision Tree

**Time series data?** → Use `LineChart`.

**Categorical comparison?** → Use `BarChart`.

**Part-to-whole relationship?** → Use `PieChart`.

**Correlation between variables?** → Use `ScatterChart`.

**Multiple metrics?** → Use multiple series in same chart or compose multiple charts.

**Interactive tooltips?** → Enabled by default, customize with `tooltip` prop.

**Custom styling?** → Use `sx` prop or theme customization.

---

## Example

```typescript
import { LineChart } from '@mui/x-charts/LineChart';

<LineChart
  xAxis={[{ data: [1, 2, 3, 4, 5] }]}
  series={[
    { data: [2, 5, 3, 7, 4], label: 'Series A' }
  ]}
  width={500}
  height={300}
/>
```

---

## Edge Cases

**Empty data:** Handle gracefully with placeholder or message.

**Large datasets:** Consider data aggregation or sampling for performance.

**Dynamic data:** Use React state and update chart data reactively.

**Accessibility:** Provide alternative data representation (table) for screen readers.

**Print support:** Test chart rendering in print mode, may need CSS adjustments.

---

## References

- https://mui.com/x/react-charts/
