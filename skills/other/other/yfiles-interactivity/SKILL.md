---
name: yfiles-interactivity
description: Adds user interactivity to yFiles applications including tooltips, context menus, click handlers, graph search, overview component, hover effects, and selection events. Enables rich interactive diagram experiences. Use when implementing tooltips, context menus, search functionality, overview navigation, click events, hover effects, or when user mentions "tooltip", "context menu", "search", "overview", "click handler", "selection changed", "hover", or "interactive features".
---

# User Interactivity

Add interactive features like tooltips, context menus, search, and navigation to yFiles applications.

## Quick Start

```typescript
// Tooltips
inputMode.addEventListener('query-item-tool-tip', (evt) => {
  evt.toolTip = createTooltipContent(evt.item)
  evt.handled = true
})

// Context menu
inputMode.addEventListener('populate-item-context-menu', (evt) => {
  evt.contextMenu = [
    { label: 'Delete', action: () => inputMode.deleteSelection() }
  ]
})

// Overview
const overview = new GraphOverviewComponent('overviewDiv', graphComponent)

// Search with highlighting
graphComponent.highlights.clear()
graph.nodes.forEach(node => {
  if (matches(node, searchText)) {
    graphComponent.highlights.add(node)
  }
})
```

## Before Implementing

**Always query yFiles MCP for current API:**

```
yfiles:yfiles_get_symbol_details(name="GraphEditorInputMode")
yfiles:yfiles_list_members(name="GraphEditorInputMode", includeInherited=true)
yfiles:yfiles_get_symbol_details(name="GraphOverviewComponent")
yfiles:yfiles_search_documentation(query="tooltips context menu")
```

## Core Concepts

- **Tooltips**: query-item-tool-tip event, ToolTipInputMode configuration
- **Context Menus**: populate-item-context-menu event, contextMenu array
- **Click Events**: item-clicked, item-double-clicked, item-right-clicked
- **Graph Search**: Highlights manager, custom matching logic
- **Overview**: GraphOverviewComponent for navigation
- **Selection Events**: selection.item-added, selection.item-removed, current-item-changed

**Note**: Always use `addEventListener` (yFiles 3.0) instead of `addListener` (yFiles 2.6). The `@yfiles/eslint-plugin` rule `@yfiles/replace-legacy-event-listeners` enforces this and auto-fixes legacy patterns.

## When to Implement

- **Tooltips**: Show additional information on hover
- **Context Menus**: Provide contextual actions via right-click
- **Click Events**: React to user clicks on graph items
- **Graph Search**: Enable finding and highlighting nodes/edges
- **Overview**: Navigate large graphs with minimap
- **Selection Events**: React to selection changes for details panels

## Code Examples

See [examples.md](examples.md) for:
- Tooltip setup with HTML content
- Context menu with conditional items
- Graph search with highlighting
- Overview component integration
- Click event handlers
- Selection change listeners

## Reference

See [reference.md](reference.md) for:
- Event parameters and signatures
- ToolTipInputMode configuration options
- Context menu item format
- GraphOverviewComponent API
- Highlight manager usage
- Selection API

## Related Skills

- `/yfiles-init` - Initial setup
- `/yfiles-graphbuilder` - Build graphs from data
- `/yfiles-nodestyle-basic` - Custom visuals for highlighting

## MCP Tools

- `yfiles:yfiles_get_symbol_details(name="GraphEditorInputMode")` - Input mode API
- `yfiles:yfiles_get_symbol_details(name="GraphOverviewComponent")` - Overview component
- `yfiles:yfiles_search_documentation(query="tooltips")` - Documentation
- `yfiles:yfiles_search_by_description(query="search highlight")` - Find related APIs
