---
name: yfiles-nodestyle-basic
description: Creates basic custom node styles by extending NodeStyleBase and implementing createVisual/updateVisual methods. Handles SVG rendering, visual caching, and performance optimization. Use when creating custom node visualizations, implementing custom shapes, or when user mentions "custom node style", "NodeStyleBase", "createVisual", "updateVisual", or "custom rendering".
---

# Basic Custom Node Styles

Create custom node visualizations using NodeStyleBase.

## Quick Start

```typescript
import { NodeStyleBase, SvgVisual, type IRenderContext, type INode } from '@yfiles/yfiles'

export class CustomNodeStyle extends NodeStyleBase {
  protected createVisual(context: IRenderContext, node: INode): SvgVisual {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
    const { x, y, width, height } = node.layout
    rect.setAttribute('x', String(x))
    rect.setAttribute('y', String(y))
    rect.setAttribute('width', String(width))
    rect.setAttribute('height', String(height))
    rect.setAttribute('fill', '#0b7189')
    return new SvgVisual(rect)
  }
}
```

## Before Creating

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_get_symbol_details(name="NodeStyleBase")
yfiles:yfiles_list_members(name="NodeStyleBase")
yfiles:yfiles_search_documentation(query="custom node style")
```

## Core Concepts

- **createVisual()**: Creates SVG visual (required)
- **updateVisual()**: Optimizes rerendering (highly recommended)
- **Caching**: Store render state in visual.tag for efficient updates
- **SvgVisual**: Wrapper for SVG elements

## Implementation Steps

1. Extend NodeStyleBase
2. Implement createVisual() to create SVG
3. Implement updateVisual() for performance
4. Use visual caching to avoid unnecessary DOM updates

**Note**: When implementing yFiles interfaces, always use `BaseClass()` wrapper instead of TypeScript `implements`. The `@yfiles/eslint-plugin` rule `@yfiles/fix-implements-using-baseclass` enforces this pattern.

## Code Examples

See [examples.md](examples.md) for:
- Basic rectangle style
- Custom shape with path
- Optimized style with updateVisual
- Caching patterns

## Reference

See [reference.md](reference.md) for:
- NodeStyleBase API details
- SVG manipulation patterns
- Performance best practices
- Visual caching strategies

## Related Skills

After mastering basics, explore:
- `/yfiles-nodestyle-configure` - Make styles configurable and data-driven
- `/yfiles-nodestyle-interaction` - Add hit testing and edge cropping
- `/yfiles-nodestyle-advanced` - Viewport culling and group nodes

## MCP Tools

- `yfiles:yfiles_get_symbol_details(name="NodeStyleBase")` - Base class API
- `yfiles:yfiles_get_symbol_details(name="SvgVisual")` - Visual wrapper
- `yfiles:yfiles_search_documentation(query="custom node style")` - Tutorials
