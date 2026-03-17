---
name: k-fenui
description: >
  Context for FenUI - the UI widget library for WoW addons. Covers
  frames, layouts, buttons, panels, and theming. Load this when
  building addon UI or working with FenUI widgets.
  Triggers: fenui, ui, widget, frame, layout, panel, button, tabs.
---

# FenUI Library

FenUI is a UI widget library for WoW addons - pre-built components with consistent styling and behavior.

## Design Philosophy

- **Composable**: Build complex UIs from simple widgets
- **Themeable**: Consistent look across all widgets
- **Declarative**: Describe what you want, not how to build it
- **Accessible**: Proper focus handling and keyboard navigation

## Widget Categories

| Category | Widgets | Purpose |
|----------|---------|---------|
| **Containers** | `Panel`, `Frame`, `Window` | Hold other widgets |
| **Layout** | `Layout`, `Grid`, `Stack` | Arrange children |
| **Input** | `Button`, `EditBox`, `Slider`, `Checkbox` | User interaction |
| **Display** | `Label`, `Icon`, `ProgressBar`, `Texture` | Show information |
| **Navigation** | `Tabs`, `ScrollFrame`, `Dropdown` | Navigate content |

## Usage Pattern

```lua
local FenUI = LibStub("FenUI")

-- Create a panel with children
local panel = FenUI.Panel:Create(parent, {
    width = 300,
    height = 200,
    title = "My Panel",
})

-- Add a button
local button = FenUI.Button:Create(panel, {
    text = "Click Me",
    onClick = function() print("Clicked!") end,
})
```

## Layout System

FenUI uses a declarative layout system:

```lua
local layout = FenUI.Layout:Create(parent, {
    direction = "vertical",  -- or "horizontal"
    spacing = 8,
    padding = { top = 10, bottom = 10, left = 10, right = 10 },
})

-- Children are automatically arranged
layout:AddChild(widget1)
layout:AddChild(widget2)
layout:AddChild(widget3)
```

## Common Widgets

### Panel

```lua
FenUI.Panel:Create(parent, {
    width = 300,
    height = 200,
    title = "Title",        -- Optional header
    closable = true,        -- Show close button
    movable = true,         -- Allow dragging
})
```

### Button

```lua
FenUI.Button:Create(parent, {
    text = "Click Me",
    width = 100,
    height = 24,
    onClick = function() end,
    onEnter = function() end,  -- Hover
    onLeave = function() end,
})
```

### Tabs

```lua
FenUI.Tabs:Create(parent, {
    tabs = {
        { id = "tab1", label = "First", content = frame1 },
        { id = "tab2", label = "Second", content = frame2 },
    },
    defaultTab = "tab1",
    onTabChanged = function(tabId) end,
})
```

### Grid

```lua
FenUI.Grid:Create(parent, {
    columns = 3,
    rowHeight = 30,
    columnWidth = 100,
    spacing = 4,
})
```

## Theming

FenUI supports theming via a theme table:

```lua
FenUI:SetTheme({
    colors = {
        background = { 0.1, 0.1, 0.1, 0.9 },
        text = { 1, 1, 1, 1 },
        accent = { 0.2, 0.6, 1, 1 },
    },
    fonts = {
        normal = "GameFontNormal",
        header = "GameFontNormalLarge",
    },
})
```

## Best Practices

1. **Use Layout** - Don't manually position widgets; use Layout containers
2. **Prefer FenUI widgets** - Don't create raw frames when a FenUI widget exists
3. **Keep View layer thin** - UI code should just display data from Bridge layer
4. **Test at different scales** - Check UI at various UI scale settings
