---
name: layerchart-svelte5
# prettier-ignore
description: LayerChart Svelte 5 patterns. Use for chart components with tooltip snippets, Chart context access, and all Svelte 5 snippet patterns for tooltips, gradients, highlights, and axes.
---

# LayerChart Svelte 5

Use **next.layerchart.com** docs (NOT layerchart.com - that's Svelte
4).

## Quick Start

```svelte
<Chart {data} x="date" y="value" tooltip={{ mode: 'bisect-x' }}>
	<Svg>
		<Axis placement="left" grid rule />
		<Area
			class="fill-primary/20"
			line={{ class: 'stroke-primary' }}
		/>
		<Highlight points lines />
	</Svg>
	<Tooltip.Root>
		{#snippet children({ data })}
			<Tooltip.Header>{data.date}</Tooltip.Header>
			<Tooltip.Item label="Value" value={data.value} />
		{/snippet}
	</Tooltip.Root>
</Chart>
```

## Core Patterns

- **Tooltip**: `{#snippet children({ data })}` - NOT `let:data`
- **Chart context**: `{#snippet children({ context })}`
- **Gradient**: `{#snippet children({ gradient })}`
- **Must enable**:
  `tooltip={{ mode: 'band' | 'bisect-x' | 'quadtree' }}`

## Tooltip Modes

| Mode         | Use Case               |
| ------------ | ---------------------- |
| `band`       | Bar charts (scaleBand) |
| `bisect-x`   | Time-series area/line  |
| `quadtree-x` | Area (nearest x)       |
| `quadtree`   | Scatter plots          |

## Type the Snippet

```svelte
{#snippet children({ data }: { data: MyDataType })}
```

## References

- [references/full-patterns.md](references/full-patterns.md) - All
  patterns
- [references/tooltip-modes.md](references/tooltip-modes.md) - Mode
  details
- Clone:
  `git clone --branch next https://github.com/techniq/layerchart.git`
