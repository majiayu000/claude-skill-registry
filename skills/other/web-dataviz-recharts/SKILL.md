---
name: web-dataviz-recharts
description: Recharts composable chart components - LineChart, BarChart, AreaChart, PieChart, ComposedChart, responsive sizing, custom tooltips, animations
---

# Recharts Patterns

> **Quick Guide:** Recharts wraps D3 in composable React components for declarative charting. Each chart is composed from independent child components (`XAxis`, `YAxis`, `Tooltip`, `Legend`, `CartesianGrid`, data series). Use `ResponsiveContainer` or the `responsive` prop for adaptive sizing. Memoize `data` and callback props to avoid unnecessary recalculations. Custom tooltips use the `content` prop. In v3, `accessibilityLayer` defaults to `true`, and internal state is accessed via hooks, not cloned props.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap charts in `ResponsiveContainer` or set the `responsive` prop for adaptive sizing -- charts without responsive handling render at fixed dimensions)**

**(You MUST memoize data arrays and callback functions passed as props -- unstable references cause Recharts to recalculate all data points)**

**(You MUST provide explicit `width` and `height` to chart components when NOT using `ResponsiveContainer` -- charts render nothing without dimensions)**

**(You MUST use the `content` prop on `Tooltip` for custom tooltips -- return HTML elements, NOT SVG elements)**

</critical_requirements>

---

**Auto-detection:** Recharts, recharts, LineChart, BarChart, AreaChart, PieChart, ComposedChart, ScatterChart, RadarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Line, Bar, Area, Pie, Cell, LabelList, Brush, ReferenceLine, ReferenceArea, customized tooltip, chart data visualization

**When to use:**

- Building line, bar, area, pie, scatter, radar, or composed charts
- Creating responsive dashboards with multiple chart types
- Implementing custom tooltips, legends, or axis formatting
- Composing multiple data series in a single chart
- Adding reference lines, areas, or brushes for data exploration

**When NOT to use:**

- Highly custom, non-standard visualizations (use D3 directly)
- Canvas-based rendering for very large datasets (50K+ points) -- Recharts uses SVG
- 3D visualizations or globe/map projections

**Key patterns covered:**

- Chart composition with child components
- Responsive sizing (`ResponsiveContainer` vs `responsive` prop)
- Custom tooltips with typed props
- Multi-axis and multi-series charts
- ComposedChart for mixing chart types
- PieChart with custom labels and donut variants
- Animations and real-time data updates
- Performance optimization for large datasets

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Basic charts, responsive container, axes, tooltips, legends
- [examples/advanced.md](examples/advanced.md) - Composed charts, custom shapes, animations, real-time data, Brush
- [reference.md](reference.md) - Component quick reference, decision frameworks, prop cheat sheets

---

<philosophy>

## Philosophy

Recharts treats charts as **compositions of independent React components**. A `LineChart` is not a monolith -- it's an assembly of `XAxis`, `YAxis`, `Tooltip`, `Legend`, `CartesianGrid`, and one or more `Line` components. This composable architecture means you add features by adding child components, not by passing configuration objects.

**Core principles:**

1. **Composition over configuration** -- Add a `Tooltip` component to get tooltips, add `CartesianGrid` for grid lines. Remove them to remove the feature.
2. **Declarative data binding** -- Pass a `data` array to the chart, use `dataKey` on child components to bind to fields.
3. **SVG-based rendering** -- All output is SVG, enabling CSS styling and DOM inspection.
4. **Headless by default** -- Charts have minimal default styling. You control appearance through props and CSS.

**When to use Recharts:**

- Standard chart types (line, bar, area, pie, scatter, radar, funnel)
- Dashboards with multiple chart types sharing consistent patterns
- Projects that value a declarative, component-based API over imperative drawing

**When NOT to use:**

- Datasets exceeding ~50K data points (SVG performance degrades -- consider Canvas-based alternatives)
- Highly custom visualizations that don't map to standard chart types
- Animations requiring physics-based or gesture-driven interactions

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Chart Composition

Every Recharts chart follows the same composition pattern: a chart container wrapping axis, grid, data series, and overlay components.

```tsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const CHART_HEIGHT = 400;
const STROKE_WIDTH = 2;

<ResponsiveContainer width="100%" height={CHART_HEIGHT}>
  <LineChart data={data}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="month" />
    <YAxis />
    <Tooltip />
    <Legend />
    <Line
      type="monotone"
      dataKey="revenue"
      stroke="#8884d8"
      strokeWidth={STROKE_WIDTH}
    />
    <Line
      type="monotone"
      dataKey="expenses"
      stroke="#82ca9d"
      strokeWidth={STROKE_WIDTH}
    />
  </LineChart>
</ResponsiveContainer>;
```

**Why good:** Each child component is an independent feature -- remove `Tooltip` to remove tooltips, remove `CartesianGrid` to remove grid lines. Data binding is declarative via `dataKey`.

See [examples/core.md](examples/core.md) for full chart setup with TypeScript typing.

---

### Pattern 2: Responsive Sizing

Charts require explicit dimensions. Two approaches for responsive behavior:

#### ResponsiveContainer (recommended for most cases)

```tsx
const CHART_HEIGHT = 300;

<ResponsiveContainer width="100%" height={CHART_HEIGHT}>
  <BarChart data={data}>{/* ... */}</BarChart>
</ResponsiveContainer>;
```

#### `responsive` prop (v3+ -- simpler, CSS-based)

```tsx
<BarChart data={data} responsive>
  {/* chart uses standard CSS sizing from parent */}
</BarChart>
```

**When to use `ResponsiveContainer`:** When you need `debounce`, `aspect` ratio, `onResize` callback, or `minWidth`/`maxHeight` constraints.

**When to use `responsive` prop:** When standard CSS sizing from the parent element is sufficient and you want to avoid an extra wrapper.

**Gotcha:** `ResponsiveContainer` must have a parent with defined dimensions. If the parent has `height: 0` or is `display: none`, the chart will not render.

See [examples/core.md](examples/core.md) for responsive patterns and SSR considerations.

---

### Pattern 3: Custom Tooltips

Use the `content` prop on `Tooltip` to render a custom tooltip component. The component receives `active`, `payload`, and `label` props.

```tsx
import type { TooltipProps } from "recharts";
import type {
  ValueType,
  NameType,
} from "recharts/types/component/DefaultTooltipContent";

function CustomTooltip({
  active,
  payload,
  label,
}: TooltipProps<ValueType, NameType>) {
  if (!active || !payload?.length) return null;

  return (
    <div className="custom-tooltip">
      <p>{label}</p>
      {payload.map((entry) => (
        <p key={entry.name} style={{ color: entry.color }}>
          {entry.name}: {entry.value}
        </p>
      ))}
    </div>
  );
}

// Usage
<Tooltip content={<CustomTooltip />} />;
```

**Why good:** Full control over tooltip markup and styling, TypeScript types from Recharts, HTML elements (not SVG).

**Gotcha:** Custom tooltip `content` must return HTML elements, not SVG. Returning SVG causes rendering errors.

See [examples/core.md](examples/core.md) for formatted tooltips and passing extra props.

---

### Pattern 4: Axis Configuration

`XAxis` and `YAxis` accept `type`, `dataKey`, `tickFormatter`, `domain`, and `scale` for controlling axis behavior.

```tsx
const CURRENCY_FORMATTER = (value: number) => `$${value.toLocaleString()}`;
const DATE_FORMATTER = (value: string) => new Date(value).toLocaleDateString();

<XAxis
  dataKey="date"
  tickFormatter={DATE_FORMATTER}
  angle={-45}
  textAnchor="end"
  height={60}
/>
<YAxis
  tickFormatter={CURRENCY_FORMATTER}
  domain={[0, "dataMax + 1000"]}
  width={80}
/>
```

**Key props:**

- `type`: `"category"` (default for XAxis) or `"number"` (default for YAxis)
- `domain`: `[min, max]` -- accepts numbers, `"auto"`, `"dataMin"`, `"dataMax"`, or expressions like `"dataMax + 100"`
- `tickFormatter`: Function to format tick labels
- `scale`: `"auto"`, `"log"`, `"symlog"`, or custom D3 scale

See [examples/core.md](examples/core.md) for multi-axis, hidden axes, and label configuration.

---

### Pattern 5: PieChart and Donut Charts

PieChart uses the `Pie` component (not `PieChart` alone). Use `Cell` components for per-slice coloring. Set `innerRadius` for donut style.

```tsx
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];
const CHART_SIZE = 400;
const OUTER_RADIUS = 150;
const INNER_RADIUS = 80; // > 0 for donut

<PieChart width={CHART_SIZE} height={CHART_SIZE}>
  <Pie
    data={data}
    dataKey="value"
    nameKey="name"
    cx="50%"
    cy="50%"
    outerRadius={OUTER_RADIUS}
    innerRadius={INNER_RADIUS}
    label
  >
    {data.map((_, index) => (
      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
    ))}
  </Pie>
  <Tooltip />
  <Legend />
</PieChart>;
```

**Why good:** `Cell` components give per-slice control. `innerRadius > 0` creates donut chart. `label` prop enables sector labels.

See [examples/core.md](examples/core.md) for custom labels and nested pie charts.

---

### Pattern 6: ComposedChart

Mix different chart types (Line, Bar, Area) in a single chart using `ComposedChart`.

```tsx
import {
  ComposedChart,
  Line,
  Bar,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

<ComposedChart data={data}>
  <XAxis dataKey="month" />
  <YAxis yAxisId="left" />
  <YAxis yAxisId="right" orientation="right" />
  <Tooltip />
  <Legend />
  <Bar dataKey="sales" yAxisId="left" fill="#8884d8" />
  <Line type="monotone" dataKey="trend" yAxisId="right" stroke="#ff7300" />
  <Area
    type="monotone"
    dataKey="forecast"
    yAxisId="left"
    fill="#82ca9d"
    opacity={0.3}
  />
</ComposedChart>;
```

**Why good:** Dual Y-axes via `yAxisId`, different visual types in one chart. Use when data has different scales or units.

See [examples/advanced.md](examples/advanced.md) for full ComposedChart patterns.

---

### Pattern 7: Animations and Transitions

Recharts animates data changes by default. Control with `isAnimationActive`, `animationDuration`, and `animationEasing` on data series components.

```tsx
const ANIMATION_DURATION = 800;

<Line
  dataKey="value"
  isAnimationActive={true}
  animationDuration={ANIMATION_DURATION}
  animationEasing="ease-in-out"
  animationBegin={0}
/>;
```

**Disable animations** for real-time data or performance-critical scenarios:

```tsx
<Line dataKey="value" isAnimationActive={false} />
```

**Gotcha:** When animation is enabled, the entire chart redraws on every data update. For high-frequency updates (>1 update/second), disable animations and use the chart's `throttleDelay` prop.

See [examples/advanced.md](examples/advanced.md) for real-time data patterns.

---

### Pattern 8: Performance Optimization

For large datasets or frequent updates, apply these patterns:

```tsx
// 1. Memoize data to prevent recalculation
const chartData = useMemo(() => transformData(rawData), [rawData]);

// 2. Memoize callback props
const formatTick = useCallback((value: number) => `$${value}`, []);

// 3. Disable animation for frequent updates
<Line dataKey="value" isAnimationActive={false} />

// 4. Throttle mouse events on the chart
<LineChart data={chartData} throttleDelay={100}>
```

**Key strategies:**

- Memoize `data` arrays -- unstable references force full recalculation
- Memoize `dataKey` functions -- changes trigger point recalculation
- Disable animations for real-time or rapidly updating charts
- Use `throttleDelay` on chart components for mouse event throttling
- Aggregate data before rendering -- show 500 points instead of 50,000

See [examples/advanced.md](examples/advanced.md) for data sampling and throttling patterns.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Chart Type?

```
What relationship are you showing?
|
+-> Change over time?
|   +-> Continuous trend -> LineChart or AreaChart
|   +-> Discrete periods -> BarChart
|   +-> Both overlaid -> ComposedChart
|
+-> Part of a whole?
|   +-> Few categories (< 8) -> PieChart
|   +-> With center content -> PieChart (donut: innerRadius > 0)
|
+-> Correlation between variables?
|   +-> Two variables -> ScatterChart
|
+-> Multi-dimensional comparison?
|   +-> 3+ variables per item -> RadarChart
|
+-> Mixing types?
    +-> Bar + Line + Area -> ComposedChart
```

### Responsive Approach?

```
Need debounce, aspect ratio, onResize callback?
+-> YES -> ResponsiveContainer
+-> NO  -> responsive prop (v3+, simpler)
```

### When to Disable Animations?

- Data updates more than once per second
- Large datasets (1000+ points)
- Print or export scenarios
- Performance-sensitive dashboards with many charts

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Chart renders nothing** -- Missing `width`/`height` props and no `ResponsiveContainer`. Charts require explicit dimensions.
- **Unstable data reference** -- Passing `data={fetchedData.map(...)}` inline creates a new array every render, forcing full recalculation. Memoize with `useMemo`.
- **Custom tooltip returns SVG** -- The `content` prop on `Tooltip` must return HTML elements. SVG elements cause rendering errors.
- **`ResponsiveContainer` parent has no dimensions** -- If the parent has `height: 0`, the chart will not render. Ensure the parent has defined height.

**Medium Priority Issues:**

- **Missing `dataKey` on data series** -- `Line`, `Bar`, `Area`, and `Pie` require `dataKey` to bind to data fields. Without it, nothing renders.
- **`CartesianGrid` with non-default axis IDs** -- In v3, `CartesianGrid` requires `xAxisId`/`yAxisId` matching the axes. Mismatched IDs produce no grid lines.
- **Inline function as `dataKey`** -- Causes recalculation on every render. Memoize with `useCallback` or define outside the component.
- **PieChart without `Cell` components** -- All slices render in the same default color. Use `Cell` for per-slice coloring.

**Gotchas & Edge Cases:**

- `ResponsiveContainer` uses ResizeObserver -- may not fire on initial render in some SSR scenarios. Set `initialDimension` as a fallback.
- `XAxis type="category"` is the default -- for numeric axes, explicitly set `type="number"`.
- `domain` on YAxis resets when data changes unless you set `allowDataOverflow={true}`.
- Z-index in SVG follows render order, not CSS `z-index` -- place important elements later in JSX to render on top.
- `syncId` synchronizes tooltips and brushes across charts -- all charts with the same `syncId` share hover state.
- `Brush` component enables range selection but adds significant DOM elements. Avoid on dashboards with many charts.
- PieChart `label` prop can be `true` (default labels), an element, or a render function -- but complex labels may overlap on small slices. Use `LabelList` or a custom `label` function with collision detection.
- `animationBegin` defaults to 0 but animations stack -- multiple series animate simultaneously unless you stagger `animationBegin`.
- `accessibilityLayer` defaults to `true` in v3 -- keyboard controls and ARIA attributes are enabled automatically.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap charts in `ResponsiveContainer` or set the `responsive` prop for adaptive sizing -- charts without responsive handling render at fixed dimensions)**

**(You MUST memoize data arrays and callback functions passed as props -- unstable references cause Recharts to recalculate all data points)**

**(You MUST provide explicit `width` and `height` to chart components when NOT using `ResponsiveContainer` -- charts render nothing without dimensions)**

**(You MUST use the `content` prop on `Tooltip` for custom tooltips -- return HTML elements, NOT SVG elements)**

**Failure to follow these rules will cause charts to render nothing, performance degradation from unnecessary recalculations, and tooltip rendering errors.**

</critical_reminders>
