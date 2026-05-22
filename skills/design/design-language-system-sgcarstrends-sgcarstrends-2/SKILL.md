---
name: design-language-system
description: Apply the professional Navy Blue colour scheme and design tokens. Use when styling components, charts, or ensuring colour consistency across the application.
allowed-tools: Read, Edit, Grep, Glob
---

# Design Language System Skill

This skill documents the professional colour scheme and design tokens for SG Cars Trends, optimised for automotive data visualisation (GitHub Issue #406).

## When to Use This Skill

- Styling new components with the brand colour palette
- Implementing chart colours for data visualisation
- Ensuring colour consistency across the application
- Migrating arbitrary hex colours to design tokens
- Reviewing colour usage in code reviews

## Colour Philosophy

**Never use arbitrary hex colours in components.** Always use:

1. CSS variables (`var(--chart-1)`, `var(--primary)`)
2. HeroUI semantic classes (`text-foreground`, `bg-primary`, `text-default-500`)
3. Tailwind colour classes mapped to CSS variables (`text-primary`, `bg-muted`)

## Brand Colour Palette

| Role | Colour | Hex | HSL | Usage |
|------|--------|-----|-----|-------|
| Primary | Navy Blue | `#191970` | `hsl(240, 63%, 27%)` | Headers, footers, primary buttons, key accents |
| Secondary | Slate Gray | `#708090` | `hsl(210, 13%, 50%)` | Card containers, borders, secondary buttons |
| Accent | Steel Blue | `#4A6AAE` | `hsl(220, 40%, 49%)` | Interactive elements, links, hover states |
| Foreground | Blue-Gray | `#2D3748` | `hsl(220, 15%, 20%)` | Body text, icons |
| Muted | Light Blue-Gray | `#F0F4F8` | `hsl(213, 32%, 95%)` | Backgrounds, subtle textures |
| Border | Light Slate | `#E2E8F0` | `hsl(214, 32%, 91%)` | Dividers, input borders |
| Success | Green | `#22C55E` | `hsl(142, 71%, 45%)` | Positive trends, success states |
| Destructive | Red | `#DC2626` | `hsl(0, 72%, 51%)` | Errors, negative trends, destructive actions |

## CSS Variables

### Core Semantic Variables

Defined in `apps/web/src/app/globals.css`:

```css
:root {
  /* Primary - Navy Blue */
  --primary: hsl(240 63% 27%); /* #191970 */
  --primary-foreground: hsl(0 0% 100%);

  /* Secondary - Slate Gray */
  --secondary: hsl(210 13% 50%); /* #708090 */
  --secondary-foreground: hsl(0 0% 100%);

  /* Foreground - Blue-Gray */
  --foreground: hsl(220 15% 20%);
  --background: hsl(0 0% 100%);

  /* Muted - Light Blue-Gray */
  --muted: hsl(213 32% 95%); /* #F0F4F8 */
  --muted-foreground: hsl(220 15% 20%);

  /* Accent - Steel Blue */
  --accent: hsl(220 40% 49%); /* #4A6AAE */
  --accent-foreground: hsl(0 0% 100%);

  /* Success - Green */
  --success: hsl(142 71% 45%); /* #22C55E */
  --success-foreground: hsl(0 0% 100%);

  /* Destructive - Red */
  --destructive: hsl(0 72% 51%); /* #DC2626 */
  --destructive-foreground: hsl(0 0% 100%);

  /* Border */
  --border: hsl(214 32% 91%); /* #E2E8F0 */
}
```

### Chart Colour Variables

Navy Blue gradient palette for data visualisation:

```css
:root {
  --chart-1: hsl(240 64% 27%);  /* Navy Blue - Primary/Top ranking */
  --chart-2: hsl(220 51% 37%);  /* Medium Blue - Second ranking */
  --chart-3: hsl(220 41% 49%);  /* Light Blue - Third ranking */
  --chart-4: hsl(210 14% 53%);  /* Slate Gray - Fourth ranking */
  --chart-5: hsl(215 23% 65%);  /* Light Slate - Fifth ranking */
  --chart-6: hsl(212 17% 76%);  /* Pale Slate - Sixth ranking */
}
```

## Usage Patterns

### Text Colours

```tsx
// ✅ Good - Use semantic classes
<span className="text-foreground">Primary body text</span>
<span className="text-default-600">Secondary text</span>
<span className="text-default-500">Muted/helper text</span>
<span className="text-muted-foreground">Captions, metadata</span>
<span className="text-primary">Brand emphasis</span>

// ❌ Bad - Hardcoded colours
<span className="text-[#2F4F4F]">Body text</span>
<span style={{ color: "#708090" }}>Helper text</span>
```

### Background Colours

```tsx
// ✅ Good - Use semantic classes
<div className="bg-primary text-primary-foreground">Primary action</div>
<div className="bg-default-100">Subtle background</div>
<div className="bg-default-200">Hover state</div>
<div className="bg-white">Card background</div>

// ❌ Bad - Hardcoded colours
<div className="bg-[#191970]">Navy background</div>
```

### Chart Colours

```tsx
// ✅ Good - Use CSS variables
<div style={{ backgroundColor: `var(--chart-${index + 1})` }} />
<div className="bg-[var(--chart-1)]" />

// For bar charts with multiple series
{data.map((item, i) => (
  <Bar
    key={item.name}
    style={{ fill: `var(--chart-${i + 1})` }}
  />
))}

// For single-highlight charts
<Bar
  className={isHighlighted ? "fill-[var(--chart-1)]" : "fill-default-200"}
/>

// ❌ Bad - Hardcoded hex colours
<div style={{ backgroundColor: "#191970" }} />
<Bar fill="#708090" />
```

### Interactive States

```tsx
// ✅ Good - Use semantic classes for states
<button className="bg-primary text-primary-foreground hover:bg-primary/90">
  Primary Button
</button>

<Link className="text-default-500 hover:bg-default-100">
  Navigation Item
</Link>

// Active/selected states
<Tab className={isActive ? "bg-primary text-primary-foreground" : "text-default-500"}>
  Tab Label
</Tab>

// ❌ Bad - Hardcoded state colours
<button className="bg-[#191970] hover:bg-[#14145A]">Button</button>
```

## Chart Implementation Guidelines

### Maximum Series Count

Limit charts to **6 series maximum** to match the available `--chart-1` through `--chart-6` variables:

```tsx
// ✅ Good - Within 6 series limit
{data.slice(0, 5).map((item, i) => (
  <Bar style={{ fill: `var(--chart-${i + 1})` }} />
))}

// No modulo needed when series count is controlled
colour: `var(--chart-${index + 1})`

// ❌ Bad - Modulo for unlimited series (indicates design problem)
colour: `var(--chart-${(index % 6) + 1})`
```

### Single-Highlight Pattern

For charts where one element is emphasised:

```tsx
// Latest year highlighted, others muted
{data.map((item, i, arr) => {
  const isLatest = i === arr.length - 1;
  return (
    <div
      className={isLatest ? "bg-[var(--chart-1)]" : "bg-default-200 hover:bg-default-300"}
    />
  );
})}
```

### Recharts Implementation

```tsx
import { Cell, Pie, PieChart } from "recharts";

// Use CSS variables for fill colours
<Pie data={chartData} dataKey="value">
  {chartData.map((entry, index) => (
    <Cell
      key={`cell-${entry.name}`}
      fill={entry.fill}  // fill comes from data with var(--chart-N)
    />
  ))}
</Pie>
```

### Data Preparation

```tsx
// Prepare chart data with CSS variable colours
const chartData = data.map((item, index) => ({
  name: item.name,
  value: item.count,
  fill: `var(--chart-${index + 1})`,
}));
```

## HeroUI Theme Integration

The colour system is integrated with HeroUI via `apps/web/src/app/hero.ts`:

```typescript
import { heroui } from "@heroui/react";

export default heroui({
  themes: {
    light: {
      colors: {
        primary: {
          DEFAULT: "#191970",  // Navy Blue
          foreground: "#FFFFFF",
        },
        secondary: {
          DEFAULT: "#708090",  // Slate Gray
          foreground: "#FFFFFF",
        },
        success: {
          DEFAULT: "#008B8B",  // Dark Cyan
          foreground: "#FFFFFF",
        },
        foreground: "#2F4F4F",  // Dark Slate Gray
        // ... default scale for grays
      },
    },
  },
});
```

### HeroUI Default Scale

Use the `default` scale for UI element states:

| Class | Usage |
|-------|-------|
| `bg-default-50` | Lightest background |
| `bg-default-100` | Subtle background, hover state base |
| `bg-default-200` | Muted elements, inactive bars |
| `bg-default-300` | Hover state for muted elements |
| `text-default-500` | Muted text, placeholders |
| `text-default-600` | Secondary text |
| `text-default-900` | Strong emphasis (H4 headings) |

## Migration Checklist

When migrating existing code to the design system:

- [ ] Replace hardcoded hex colours with CSS variables or semantic classes
- [ ] Remove colour constant arrays (e.g., `CHART_COLORS`, `MARKET_SHARE_COLOURS`)
- [ ] Use `var(--chart-N)` inline for chart colours
- [ ] Replace `text-gray-*` with `text-default-*`
- [ ] Replace `bg-gray-*` with `bg-default-*`
- [ ] Ensure chart series count is 6 or fewer
- [ ] Remove modulo operations if series count is controlled
- [ ] Use `text-foreground` instead of `text-gray-900` for body text

## Anti-Patterns

### Colour Constant Arrays

```tsx
// ❌ Bad - Don't create colour arrays
const CHART_COLORS = ["#191970", "#2E4A8E", "#4A6AAE", "#708090"];
// ...later
backgroundColor: CHART_COLORS[i % CHART_COLORS.length]

// ✅ Good - Use CSS variables inline
backgroundColor: `var(--chart-${i + 1})`
```

### Hardcoded Hex Values

```tsx
// ❌ Bad - Hardcoded hex
<div className="text-[#2F4F4F]">Text</div>
<div style={{ backgroundColor: "#191970" }}>Box</div>

// ✅ Good - Semantic tokens
<div className="text-foreground">Text</div>
<div className="bg-primary">Box</div>
```

### Arbitrary Gray Classes

```tsx
// ❌ Bad - Tailwind gray scale
<span className="text-gray-600">Helper text</span>
<div className="bg-gray-100">Background</div>

// ✅ Good - HeroUI default scale
<span className="text-default-600">Helper text</span>
<div className="bg-default-100">Background</div>
```

## Exceptions

### OpenGraph Images

OG images require inline styles and cannot use CSS variables:

```tsx
// apps/web/src/app/*/opengraph-image.tsx
// Inline hex colours are acceptable here
<div style={{ backgroundColor: "#191970" }}>
```

### Theme Configuration

The `hero.ts` theme config uses hex values to define the source of truth:

```typescript
// apps/web/src/app/hero.ts
primary: {
  DEFAULT: "#191970",  // This defines the --primary variable
}
```

## Related Files

- `apps/web/src/app/globals.css` - CSS variable definitions
- `apps/web/src/app/hero.ts` - HeroUI theme configuration
- `apps/web/CLAUDE.md` - Colour System section
- `packages/ui/src/styles/globals.css` - Shared UI package styles

## Accessibility (WCAG AA)

- Normal text: Minimum 4.5:1 contrast ratio
- Large text: Minimum 3:1 contrast ratio
- Interactive elements: Minimum 3:1 for focus indicators
- Colour alone must not convey information (use icons, text, patterns)

The Navy Blue primary (`#191970`) on white background meets WCAG AAA contrast requirements.
