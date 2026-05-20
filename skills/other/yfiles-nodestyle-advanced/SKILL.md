---
name: yfiles-nodestyle-advanced
description: Implements advanced node style features including viewport culling (isVisible), custom bounds (getBounds), and group node styles. Optimizes rendering performance and handles hierarchical visualization. Use when implementing viewport culling, custom bounds, group nodes, or when user mentions "isVisible", "getBounds", "group node", "viewport culling", or "rendering optimization".
---

# Advanced Node Style Features

Implement viewport culling, custom bounds, and group node styles.

## Quick Start

```typescript
export class AdvancedNodeStyle extends NodeStyleBase {
  protected isVisible(
    context: ICanvasContext,
    rectangle: Rect,
    node: INode
  ): boolean {
    // Only render if node intersects viewport
    return node.layout.toRect().intersects(rectangle)
  }

  protected getBounds(context: ICanvasContext, node: INode): Rect {
    // Return actual rendering bounds (including badges, etc.)
    return node.layout.toRect().getEnlarged(10)
  }
}
```

## Before Implementing

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_get_symbol_details(name="NodeStyleBase")
yfiles:yfiles_list_members(name="NodeStyleBase")
yfiles:yfiles_search_documentation(query="group node style")
yfiles:yfiles_get_symbol_details(name="INode")
```

## Core Concepts

- **isVisible()**: Viewport culling for performance
- **getBounds()**: Actual rendering bounds
- **Group nodes**: Hierarchical container nodes
- **Folding**: Collapsible groups

## When to Implement

- **isVisible()**: Custom shapes extending beyond layout
- **getBounds()**: Rendering beyond layout bounds (badges, shadows)
- **Group styles**: Hierarchical graph visualization

**Note**: When implementing yFiles interfaces, always use `BaseClass()` wrapper instead of TypeScript `implements`. The `@yfiles/eslint-plugin` rule `@yfiles/fix-implements-using-baseclass` enforces this pattern.

## Code Examples

See [examples.md](examples.md) for:
- Viewport culling optimization
- Custom bounds with badges
- Group node styles
- Folder tab rendering

## Reference

See [reference.md](reference.md) for:
- isVisible() optimization strategies
- getBounds() calculation patterns
- Group node API
- Performance considerations

## Related Skills

- `/yfiles-nodestyle-basic` - Start here
- `/yfiles-nodestyle-configure` - Configuration
- `/yfiles-nodestyle-interaction` - Hit testing

## MCP Tools

- `yfiles:yfiles_get_symbol_details(name="INode")` - Node API
- `yfiles:yfiles_search_by_description(query="group node")` - Group nodes
- `yfiles:yfiles_search_documentation(query="folding")` - Collapsible groups
