---
name: yfiles-nodestyle-interaction
description: Implements custom hit testing and edge cropping for node styles by overriding isHit and getOutline methods. Handles accurate click detection for custom shapes and proper edge connections. Use when implementing hit testing, custom click areas, edge cropping, or when user mentions "isHit", "hit testing", "getOutline", "edge cropping", or "edge connection points".
---

# Node Style Interaction

Implement custom hit testing and edge cropping for accurate user interaction.

## Quick Start

```typescript
export class InteractiveNodeStyle extends NodeStyleBase {
  protected isHit(
    context: IInputModeContext,
    location: Point,
    node: INode
  ): boolean {
    // Check if click is within node bounds
    return node.layout.toRect().contains(location, context.hitTestRadius)
  }

  protected getOutline(node: INode): GeneralPath | null {
    // Return path for edge cropping
    const { x, y, width, height } = node.layout
    const path = new GeneralPath()
    path.appendRectangle(new Rect(x, y, width, height), false)
    return path
  }
}
```

## Before Implementing

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_get_symbol_details(name="NodeStyleBase")
yfiles:yfiles_list_members(name="NodeStyleBase")
yfiles:yfiles_search_by_description(query="hit testing")
yfiles:yfiles_get_symbol_details(name="GeneralPath")
```

## Core Concepts

- **isHit()**: Determines if point hits the node
- **getOutline()**: Defines shape for edge cropping
- **hitTestRadius**: Tolerance area around edges
- **GeneralPath**: Defines arbitrary shapes

## When to Implement

- **isHit()**: When node shape isn't rectangular
- **getOutline()**: When edges should crop at custom shape boundary

**Note**: When implementing yFiles interfaces, always use `BaseClass()` wrapper instead of TypeScript `implements`. The `@yfiles/eslint-plugin` rule `@yfiles/fix-implements-using-baseclass` enforces this pattern.

## Code Examples

See [examples.md](examples.md) for:
- Basic hit testing for custom shapes
- Hit testing with exclusion areas
- getOutline for edge cropping
- Complex shape outlines
- Circular and elliptical hit testing

## Reference

See [reference.md](reference.md) for:
- isHit() method signature and parameters
- getOutline() implementation patterns
- GeneralPath API
- Geometric utilities

## Related Skills

- `/yfiles-nodestyle-basic` - Basic rendering
- `/yfiles-nodestyle-configure` - Configuration
- `/yfiles-nodestyle-advanced` - Performance and group nodes

## MCP Tools

- `yfiles:yfiles_get_symbol_details(name="GeneralPath")` - Path construction API
- `yfiles:yfiles_get_symbol_details(name="GeometryUtilities")` - Geometry helpers
- `yfiles:yfiles_search_by_description(query="hit testing")` - Documentation
