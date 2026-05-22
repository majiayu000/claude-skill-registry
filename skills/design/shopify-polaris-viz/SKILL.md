---
name: shopify-polaris-viz
description: Guide for creating data visualizations in Shopify Apps using the Polaris Viz library. Use this skill when building charts, graphs, dashboards, or any data visualization components that need to integrate with the Shopify Admin aesthetic. Covers BarChart, LineChart, DonutChart, SparkLineChart, and theming.
---

# Shopify Polaris Viz

Polaris Viz is Shopify's data visualization component library for React. It provides accessible, themeable chart components that match the Shopify Admin visual style.

> **Note**: This library was archived in June 2025. While still functional, Shopify recommends reaching out to support for migration assistance if building new features.

## Installation

```bash
npm install @shopify/polaris-viz
# Required peer dependencies
npm install @shopify/polaris @shopify/polaris-tokens
```

## Setup

Wrap your application with `PolarisVizProvider`:

```jsx
import { PolarisVizProvider } from '@shopify/polaris-viz';
import '@shopify/polaris-viz/build/esm/styles.css';

function App() {
  return (
    <PolarisVizProvider>
      {/* Your app */}
    </PolarisVizProvider>
  );
}
```

## Core Design Principles

1. **One Question Per Chart**: Each visualization should answer a single, specific question
2. **Accuracy First**: Faithfully represent the original dataset
3. **Accessibility**: Support screen readers, color-blind users, and multiple data formats
4. **Consistency**: Use Polaris themes for visual harmony with Shopify Admin

## Available Chart Components

| Component | Use Case | Max Data Points |
|-----------|----------|-----------------|
| `BarChart` | Comparing discrete categories | ~6 categories |
| `SimpleBarChart` | Simple horizontal bars | ~6 categories |
| `LineChart` | Trends over time | 30+ points |
| `SparkLineChart` | Compact inline trends | Any |
| `DonutChart` | Part-to-whole relationships | ~6 segments |
| `StackedAreaChart` | Cumulative trends | 30+ points |
| `FunnelChart` | Conversion funnels | ~6 stages |

## Quick Examples

### Bar Chart

```jsx
import { BarChart } from '@shopify/polaris-viz';

const data = [
  {
    name: 'Sales',
    data: [
      { key: 'Monday', value: 150 },
      { key: 'Tuesday', value: 200 },
      { key: 'Wednesday', value: 175 },
    ],
  },
];

<BarChart data={data} />
```

### Line Chart

```jsx
import { LineChart } from '@shopify/polaris-viz';

const data = [
  {
    name: 'Orders',
    data: [
      { key: 'Jan', value: 100 },
      { key: 'Feb', value: 150 },
      { key: 'Mar', value: 200 },
    ],
  },
];

<LineChart data={data} />
```

### Donut Chart

```jsx
import { DonutChart } from '@shopify/polaris-viz';

const data = [
  { name: 'Direct', data: [{ key: 'Direct', value: 200 }] },
  { name: 'Social', data: [{ key: 'Social', value: 150 }] },
  { name: 'Email', data: [{ key: 'Email', value: 100 }] },
];

<DonutChart data={data} />
```

### Spark Line (Inline Trend)

```jsx
import { SparkLineChart } from '@shopify/polaris-viz';

const data = [
  {
    data: [
      { key: 0, value: 100 },
      { key: 1, value: 150 },
      { key: 2, value: 120 },
      { key: 3, value: 180 },
    ],
  },
];

<SparkLineChart data={data} />
```

## Data Structure

All charts use a consistent `DataSeries` format:

```typescript
interface DataPoint {
  key: string | number;  // X-axis value or category
  value: number | null;  // Y-axis value (null for gaps)
}

interface DataSeries {
  name: string;           // Series label
  data: DataPoint[];      // Array of data points
  color?: string;         // Optional color override
  isComparison?: boolean; // Mark as comparison data (renders grey)
}
```

## Theming

Use the `theme` prop to switch between themes:

```jsx
// Use built-in themes
<BarChart data={data} theme="Light" />
<BarChart data={data} theme="Dark" />

// Or define custom themes in provider
<PolarisVizProvider
  themes={{
    MyBrand: {
      chartContainer: { backgroundColor: '#f9f9f9' },
      seriesColors: { upToEight: ['#5c6ac4', '#47c1bf'] },
    },
  }}
>
  <BarChart data={data} theme="MyBrand" />
</PolarisVizProvider>
```

## Color Guidelines

- **Single series**: Use one consistent color
- **Comparison to past**: Current = purple, Historical = grey
- **Multiple series**: Use contrasting colors (max 4 lines recommended)
- **Positive/Negative**: Green = positive, Red = negative

## Accessibility Requirements

1. **Color contrast**: Ensure sufficient contrast between elements
2. **Screen readers**: Charts render with ARIA attributes
3. **Text alternatives**: Provide data tables as alternative format
4. **No color-only meaning**: Use patterns or labels alongside color

## Common Props

Most chart components accept these props:

| Prop | Type | Description |
|------|------|-------------|
| `data` | `DataSeries[]` | Chart data |
| `theme` | `string` | Theme name |
| `isAnimated` | `boolean` | Enable/disable animations |
| `showLegend` | `boolean` | Show legend |
| `xAxisOptions` | `object` | X-axis configuration |
| `yAxisOptions` | `object` | Y-axis configuration |
| `emptyStateText` | `string` | Text when no data |

## Axis Label Formatting

Follow Shopify's formatting standards:

- **Times**: 12-hour lowercase (12am, 6pm)
- **Days**: Three letters (Sun, Mon)
- **Months**: Three letters (Feb, Mar)
- **Dates**: "10 Apr" format
- **Numbers**: Use "k" for thousands, max 3 digits + decimal + letter

## Anti-Patterns to Avoid

- **DO NOT** exceed 6 categories in bar/donut charts - use tables instead
- **DO NOT** use more than 4 lines in a line chart
- **DO NOT** rely on color alone to convey meaning
- **DO NOT** use edge-to-edge axis lines - keep them within data range
- **DO NOT** mix Polaris Viz with other chart libraries in the same app

## References

- [Chart Components](./references/chart-components.md) - Detailed props and examples for each chart type
- [Theming Guide](./references/theming.md) - Custom theme configuration
- [Data Structures](./references/data-structures.md) - Complete TypeScript interfaces

## External Resources

- [GitHub Repository](https://github.com/Shopify/polaris-viz) (archived)
- [Storybook Documentation](https://polaris-viz.shopify.dev/)
- [Polaris Data Visualization Guidelines](https://polaris-react.shopify.com/design/data-visualizations)
