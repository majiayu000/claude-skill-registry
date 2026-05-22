---
name: tremor-design-system
description: Build dashboards, analytics interfaces, and data-rich UIs using the Tremor design system (React + Tailwind CSS + Recharts). Use when the user asks to create dashboard components, KPI cards, charts, data tables, analytics pages, monitoring interfaces, or any data visualization UI that should use Tremor. Triggers include mentions of "Tremor", "tremor.so", "@tremor/react", requests for dashboard UIs with charts and tables, or when the user's project already uses Tremor components. Supports both Tremor Raw (copy-and-paste, tremor.so) and Tremor NPM (@tremor/react) versions. Do NOT use for general frontend work unrelated to dashboards or data visualization, or when the user explicitly requests a different component library.
---

# Tremor Design System

Build production-grade dashboards and analytics interfaces using Tremor's React component library.

## Version Detection

Tremor has two distribution models. Detect which the user's project uses before writing code:

1. **Tremor Raw** (tremor.so) — Copy-and-paste components into `src/components/`
   - Imports: `import { AreaChart } from "@/components/AreaChart"`
   - Requires: Tailwind CSS v4+, Radix UI, Recharts
   - Styling: Standard Tailwind utility classes

2. **Tremor NPM** (npm.tremor.so) — NPM package `@tremor/react`
   - Imports: `import { AreaChart, Card } from "@tremor/react"`
   - Requires: Tailwind CSS v3.4+, Headless UI, Remix Icons
   - Styling: Tremor-specific tokens (`text-tremor-content`, `dark:text-dark-tremor-content`)

**If unclear**, ask the user. Default to Tremor Raw for new projects, as it is the actively developed version (acquired by Vercel in Jan 2025).

## Workflow

1. **Determine version** — Check imports, `package.json`, or ask
2. **Identify pattern** — See [references/dashboard-patterns.md](references/dashboard-patterns.md) for common layouts (KPI rows, chart sections, filtered tables, full dashboards)
3. **Select components** — See [references/component-catalog.md](references/component-catalog.md) for the full component API
4. **Compose** — Assemble using the patterns below
5. **Style** — Apply Tailwind utilities consistent with the detected version

## Key Principles

- **Card is the atom**: Almost every dashboard section wraps in `<Card>`. KPIs, charts, tables, and forms all sit inside cards.
- **Grid layout**: Use Tailwind grid (`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6`) for responsive dashboard layouts. Never hardcode widths.
- **Data shape convention**: All chart components expect an array of objects. The `index` prop selects the x-axis key; `categories` selects the data series.
- **valueFormatter**: Always provide a `valueFormatter` for charts displaying currency, percentages, or units. Use `Intl.NumberFormat` for numbers.
- **Dark mode**: All components support dark mode. For Tremor Raw, use standard `dark:` prefixes. For NPM, use `dark-tremor-*` tokens.
- **"use client"**: Chart components use browser APIs (Recharts). In Next.js App Router, mark pages or components containing charts with `"use client"`.

## Common Data Shape

```ts
// All charts expect this pattern
const chartdata = [
  { date: "Jan 23", Revenue: 2890, Costs: 2338 },
  { date: "Feb 23", Revenue: 2756, Costs: 2103 },
  // ...
]

// index="date" → x-axis
// categories={["Revenue", "Costs"]} → data series
```

## Quick Reference: Chart Selection

| Use Case | Component |
|----------|-----------|
| Trends over time | `AreaChart` or `LineChart` |
| Category comparison | `BarChart` |
| Part-of-whole | `DonutChart` |
| Rankings | `BarList` |
| Budget/threshold | `CategoryBar` |
| Combined metrics | `ComboChart` (bar + line) |
| Inline sparkline | `SparkAreaChart`, `SparkLineChart`, `SparkBarChart` |
| Progress toward goal | `ProgressBar`, `ProgressCircle` |
| Uptime/status history | `Tracker` |

## Formatting Conventions

- Use `Intl.NumberFormat("us")` for US number formatting
- Currency: `(n) => \`$${Intl.NumberFormat("us").format(n)}\``
- Percentage: `(n) => \`${n}%\``
- Compact: `(n) => \`${Intl.NumberFormat("us", { notation: "compact" }).format(n)}\``

## References

- **Full component API and props**: [references/component-catalog.md](references/component-catalog.md)
- **Dashboard composition patterns**: [references/dashboard-patterns.md](references/dashboard-patterns.md)
