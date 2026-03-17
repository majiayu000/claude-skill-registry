---
name: yfiles-nodestyle-configure
description: Creates configurable and data-driven custom node styles using constructor parameters, node.tag data binding, and text rendering with TextRenderSupport. Use when making styles configurable, binding node data to visuals, rendering text in nodes, or when user mentions "configurable style", "node.tag", "data binding", "TextRenderSupport", or "text rendering".
---

# Configurable Custom Node Styles

Make custom node styles configurable and data-driven.

## Quick Start

```typescript
export class ConfigurableNodeStyle extends NodeStyleBase {
  constructor(public fillColor: string = '#0b7189') {
    super()
  }

  protected createVisual(context: IRenderContext, node: INode): SvgVisual {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
    const { x, y, width, height } = node.layout

    rect.setAttribute('fill', node.tag?.color ?? this.fillColor)
    // ... set other attributes

    return new SvgVisual(rect)
  }
}
```

## Before Configuring

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_get_symbol_details(name="TextRenderSupport")
yfiles:yfiles_search_documentation(query="node tag data binding")
yfiles:yfiles_search_by_description(query="text rendering")
```

## Core Concepts

- **Constructor params**: Class-level configuration
- **node.tag**: Per-node data binding
- **TextRenderSupport**: Proper text rendering with font, wrapping
- **Conditional rendering**: Different visuals based on data

## Configuration Strategies

1. **Constructor params** - Style-level defaults
2. **node.tag** - Per-node customization
3. **Combination** - tag overrides constructor params

## Code Examples

See [examples.md](examples.md) for:
- Constructor-based configuration
- Data binding from node.tag
- Text rendering with TextRenderSupport
- Conditional styling
- Combined configuration

## Reference

See [reference.md](reference.md) for:
- Constructor patterns
- node.tag structure recommendations
- TextRenderSupport API
- Font and text wrapping options

## Related Skills

- `/yfiles-nodestyle-basic` - Learn basic rendering first
- `/yfiles-nodestyle-interaction` - Add hit testing next
- `/yfiles-nodestyle-advanced` - Advanced features

## MCP Tools

- `yfiles:yfiles_get_symbol_details(name="TextRenderSupport")` - Text rendering API
- `yfiles:yfiles_get_symbol_details(name="Font")` - Font configuration
- `yfiles:yfiles_search_by_description(query="text wrapping")` - Wrapping options
