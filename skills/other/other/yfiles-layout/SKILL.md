---
name: yfiles-layout
description: Applies automatic layout algorithms (HierarchicalLayout, OrganicLayout, TreeLayout, CircularLayout, OrthogonalLayout, RadialLayout) to arrange graph elements. Use when organizing graphs, applying layouts, or when user mentions "hierarchical", "organic", "tree", "circular", "orthogonal", "radial", "arrange nodes", or "apply layout".
---

# Apply Automatic Layouts

Executes layout algorithms to automatically arrange graph elements.

## Quick Start

```typescript
import { HierarchicalLayout, LayoutExecutor } from '@yfiles/yfiles'

await new LayoutExecutor({
  graphComponent,
  layout: new HierarchicalLayout(),
  animationDuration: '0.5s'
}).start()
```

## Before Applying

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_search_by_description(query="layout algorithm")
yfiles:yfiles_get_symbol_details(name="HierarchicalLayout")
yfiles:yfiles_get_symbol_details(name="LayoutExecutor")
```

## Choosing a Layout

Quick decision guide:

- **Tree (no cycles)?** → TreeLayout
- **Directed/hierarchical?** → HierarchicalLayout
- **Undirected network?** → OrganicLayout
- **Center focus?** → RadialLayout
- **Orthogonal routing?** → OrthogonalLayout
- **Circular/cyclic?** → CircularLayout

## Common Layouts

See [algorithms.md](algorithms.md) for:
- HierarchicalLayout (flowcharts, org charts)
- OrganicLayout (social networks)
- TreeLayout (file trees, decision trees)
- CircularLayout (cycles)
- OrthogonalLayout (technical diagrams)
- RadialLayout (star topologies)

## Advanced Configuration

See [configuration.md](configuration.md) for:
- LayoutData (constraints, hints)
- Sequential layouts
- Partial layouts
- Incremental layouts
- Fixed nodes

## Complete Examples

See [examples.md](examples.md) for working code.

## LayoutExecutor Options

```typescript
new LayoutExecutor({
  graphComponent,        // Required
  layout,               // Required: ILayoutAlgorithm
  layoutData,           // Optional: Layout-specific data
  animationDuration: '1s',
  animateViewport: true,
  easedAnimation: true
})
```

## After Layout

Layout is applied and animated. Viewport adjusts automatically if `animateViewport: true`.

## MCP Tools

- `yfiles:yfiles_search_documentation(query="layout algorithms")` - Overview
- `yfiles:yfiles_get_symbol_details(name="LayoutExecutor")` - Executor API
- `yfiles:yfiles_search_by_description(query="hierarchical layout")` - Specific algorithms
