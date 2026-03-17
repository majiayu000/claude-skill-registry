---
name: layerchart-svelte5
# prettier-ignore
description: LayerChart Svelte 5 patterns. Use for chart components with tooltip snippets, Chart context access, and all Svelte 5 snippet patterns for tooltips, gradients, highlights, and axes.
---

# LayerChart Svelte 5

Docs: **next.layerchart.com** (NOT layerchart.com - that's Svelte 4)

## Install

```bash
npm i layerchart@next d3-scale
```

**CRITICAL**: Use `@next` tag. Stable (1.x) is Svelte 4 only.

## Quick Start

```svelte
<Chart {data} x="date" y="value" tooltip={{ mode: 'bisect-x' }}>
	<Svg><Area class="fill-primary/20" /><Highlight points /></Svg>
	<Tooltip.Root>{#snippet children({ data })}{data.value}{/snippet}</Tooltip.Root>
</Chart>
```

## Core Patterns

- **Tooltip**: `{#snippet children({ data })}` - NOT `let:data`
- **Chart context**: `{#snippet children({ context })}`
- **Gradient**: `{#snippet children({ gradient })}`
- **Enable tooltip**: `tooltip={{ mode: 'band' | 'bisect-x' }}`
- **Type data**: `{#snippet children({ data }: { data: MyType })}`

## Tooltip Modes

| Mode         | Use Case               |
| ------------ | ---------------------- |
| `band`       | Bar charts (scaleBand) |
| `bisect-x`   | Time-series area/line  |
| `quadtree-x` | Area (nearest x)       |
| `quadtree`   | Scatter plots          |

## References

- [full-patterns.md](references/full-patterns.md) - Area, Bar, Pie,
  Calendar
- [tooltip-modes.md](references/tooltip-modes.md) - All modes
- [graph-patterns.md](references/graph-patterns.md) - ForceGraph,
  zoom/pan
