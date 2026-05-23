---
name: financial-data-visualization
model: standard
description: Patterns for building dark-themed financial charts and data visualizations. Covers chart theming, color scales for gains/losses, and real-time data display. Use when building trading dashboards or financial analytics. Triggers on chart theme, data visualization, financial chart, dark theme, gains losses, trading UI.
---

# Financial Data Visualization

Build dark-themed financial charts and visualizations that are readable, beautiful, and consistent with modern trading UIs.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install financial-data-visualization
```


---

## When to Use

- Building trading dashboards with charts
- Displaying portfolio performance
- Showing price history and trends
- Any financial data visualization

---

## Pattern 1: Chart Color Palette

```typescript
// lib/chart-theme.ts
export const chartColors = {
  // Gains/Losses
  positive: 'hsl(154 80% 60%)',    // Green
  negative: 'hsl(346 80% 62%)',    // Red
  neutral: 'hsl(216 90% 68%)',     // Blue
  
  // Backgrounds
  background: 'hsl(222 47% 11%)',
  surface: 'hsl(222 47% 15%)',
  grid: 'hsl(222 47% 20%)',
  
  // Text
  textPrimary: 'hsl(210 40% 98%)',
  textSecondary: 'hsl(215 20% 65%)',
  textMuted: 'hsl(215 20% 45%)',
  
  // Data series
  series: [
    'hsl(200 90% 65%)',  // Cyan
    'hsl(280 90% 65%)',  // Purple
    'hsl(45 90% 65%)',   // Gold
    'hsl(160 90% 65%)',  // Teal
    'hsl(320 90% 65%)',  // Pink
  ],
};
```

---

## Pattern 2: Recharts Theme Config

```tsx
// components/charts/chart-config.ts
import { chartColors } from '@/lib/chart-theme';

export const chartConfig = {
  // Axis styling
  axisStyle: {
    stroke: chartColors.textMuted,
    fontSize: 11,
    fontFamily: 'var(--font-mono)',
  },
  
  // Grid styling
  gridStyle: {
    stroke: chartColors.grid,
    strokeDasharray: '3 3',
  },
  
  // Tooltip styling
  tooltipStyle: {
    backgroundColor: chartColors.surface,
    border: `1px solid ${chartColors.grid}`,
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
  },
};

// Custom tooltip component
export function ChartTooltip({ active, payload, label }: any) {
  if (!active || !payload) return null;

  return (
    <div
      className="rounded-lg border bg-popover px-3 py-2 shadow-lg"
      style={chartConfig.tooltipStyle}
    >
      <p className="text-xs text-muted-foreground mb-1">{label}</p>
      {payload.map((entry: any, index: number) => (
        <p
          key={index}
          className="text-sm font-mono tabular-nums"
          style={{ color: entry.color }}
        >
          {entry.name}: {formatCurrency(entry.value)}
        </p>
      ))}
    </div>
  );
}
```

---

## Pattern 3: Price Chart Component

```tsx
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

interface PriceChartProps {
  data: { time: string; price: number }[];
  isPositive?: boolean;
}

export function PriceChart({ data, isPositive = true }: PriceChartProps) {
  const color = isPositive ? chartColors.positive : chartColors.negative;
  
  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity={0.3} />
            <stop offset="100%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        
        <XAxis
          dataKey="time"
          axisLine={false}
          tickLine={false}
          tick={{ ...chartConfig.axisStyle }}
        />
        
        <YAxis
          domain={['auto', 'auto']}
          axisLine={false}
          tickLine={false}
          tick={{ ...chartConfig.axisStyle }}
          tickFormatter={(value) => formatCompact(value)}
        />
        
        <Tooltip content={<ChartTooltip />} />
        
        <Area
          type="monotone"
          dataKey="price"
          stroke={color}
          strokeWidth={2}
          fill="url(#priceGradient)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

---

## Pattern 4: Candlestick Colors

```typescript
export const candlestickColors = {
  up: {
    fill: 'hsl(154 80% 60%)',
    stroke: 'hsl(154 80% 50%)',
  },
  down: {
    fill: 'hsl(346 80% 62%)',
    stroke: 'hsl(346 80% 52%)',
  },
  wick: 'hsl(215 20% 45%)',
};

// Usage with lightweight-charts or similar
const candlestickSeries = chart.addCandlestickSeries({
  upColor: candlestickColors.up.fill,
  downColor: candlestickColors.down.fill,
  borderUpColor: candlestickColors.up.stroke,
  borderDownColor: candlestickColors.down.stroke,
  wickUpColor: candlestickColors.wick,
  wickDownColor: candlestickColors.wick,
});
```

---

## Pattern 5: Percentage Bar

```tsx
interface PercentageBarProps {
  value: number;  // -100 to 100
  showLabel?: boolean;
}

export function PercentageBar({ value, showLabel = true }: PercentageBarProps) {
  const isPositive = value >= 0;
  const absValue = Math.min(Math.abs(value), 100);

  return (
    <div className="flex items-center gap-2">
      {/* Negative side */}
      <div className="flex-1 flex justify-end">
        {!isPositive && (
          <div
            className="h-2 rounded-l bg-destructive"
            style={{ width: `${absValue}%` }}
          />
        )}
      </div>
      
      {/* Center divider */}
      <div className="w-px h-4 bg-border" />
      
      {/* Positive side */}
      <div className="flex-1">
        {isPositive && (
          <div
            className="h-2 rounded-r bg-success"
            style={{ width: `${absValue}%` }}
          />
        )}
      </div>
      
      {showLabel && (
        <span
          className={cn(
            'text-xs font-mono tabular-nums w-12 text-right',
            isPositive ? 'text-success' : 'text-destructive'
          )}
        >
          {formatPercentage(value)}
        </span>
      )}
    </div>
  );
}
```

---

## Pattern 6: Mini Sparkline

```tsx
interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
}

export function Sparkline({ data, width = 80, height = 24 }: SparklineProps) {
  const first = data[0];
  const last = data[data.length - 1];
  const isPositive = last >= first;
  const color = isPositive ? chartColors.positive : chartColors.negative;

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data
    .map((value, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((value - min) / range) * height;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg width={width} height={height} className="overflow-visible">
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
```

---

## Pattern 7: Chart Legend

```tsx
interface LegendItem {
  label: string;
  color: string;
  value?: string;
}

export function ChartLegend({ items }: { items: LegendItem[] }) {
  return (
    <div className="flex flex-wrap gap-4">
      {items.map((item) => (
        <div key={item.label} className="flex items-center gap-2">
          <div
            className="size-3 rounded-full"
            style={{ backgroundColor: item.color }}
          />
          <span className="text-xs text-muted-foreground">{item.label}</span>
          {item.value && (
            <span className="text-xs font-mono">{item.value}</span>
          )}
        </div>
      ))}
    </div>
  );
}
```

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/design-system-creation/](../../meta/design-system-creation/) — Complete design system workflow
- [animated-financial-display](../animated-financial-display/) — Number animations and value flash effects
- [dual-stream-architecture](../../realtime/dual-stream-architecture/) — Real-time data streaming patterns

---

## NEVER Do

- **Use light theme colors** — Ensure sufficient contrast on dark backgrounds
- **Use red/green without considering colorblind users** — Add shapes or patterns
- **Skip grid lines** — They help read values
- **Use thick strokes** — 1-2px is optimal for data lines
- **Animate charts on every data point** — Reserve animation for initial load

---

## Quick Reference

```tsx
// Color assignment
const color = value >= 0 ? chartColors.positive : chartColors.negative;

// Gradient definition
<linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stopColor={color} stopOpacity={0.3} />
  <stop offset="100%" stopColor={color} stopOpacity={0} />
</linearGradient>

// Axis styling
<XAxis tick={{ fill: chartColors.textMuted, fontSize: 11 }} />

// Tooltip styling
<Tooltip contentStyle={{ background: chartColors.surface }} />
```
