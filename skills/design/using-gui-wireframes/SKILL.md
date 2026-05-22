---
name: using-gui-wireframes
description: Use when creating or editing UI mockups, screen layouts, or interface designs. Use INSTEAD of ASCII art for any visual UI representation.
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read
---

# Using GUI Wireframes

## Overview

**ALWAYS use mermaid wireframe syntax for UI mockups.** Never use ASCII art boxes, tables, or text representations for UI layouts.

## When to Use

Use wireframe syntax when:
- User asks for a "mockup", "wireframe", "UI design", or "screen layout"
- Visualizing app screens, forms, dashboards, or navigation flows
- Showing multi-screen user flows or journeys
- Any situation where you'd otherwise draw ASCII boxes for UI

**NEVER use ASCII art for UI.** Wireframe syntax renders as actual visual diagrams.

## Quick Syntax Reference

```
wireframe [viewport] [direction]
  [component] ["label"] [modifiers]
```

**Viewports:** `mobile` (375×600), `tablet` (768×1024), `desktop` (1200×800)

**Direction:** `LR` (horizontal screens), `TD` (vertical screens)

**Containers:**
| Component | Purpose |
|-----------|---------|
| `col` | Stack children vertically |
| `row` | Place children horizontally |
| `Card` | Bordered container |
| `screen "label"` | Separate viewport (for flows) |

**Components:**
| Component | Example |
|-----------|---------|
| `AppBar "title"` | Top navigation bar |
| `Title "text"` | Large heading |
| `Text "text"` | Body text |
| `Input "placeholder"` | Text field |
| `Button "label"` | Clickable button |
| `Checkbox "label"` | Checkbox |
| `Switch "label"` | Toggle |
| `Dropdown "label"` | Select menu |
| `Avatar` | User avatar |
| `Image` | Image placeholder |
| `spacer` | Flexible space |
| `divider` | Horizontal line |

**Modifiers:** `primary`, `secondary`, `danger`, `disabled`, `flex=N`, `width=N`, `height=N`, `padding=N`

## Critical Syntax Rules

1. **Indentation = hierarchy** - Use 2 spaces per level, no tabs
2. **Labels in quotes** - `Button "Submit"` not `Button Submit`
3. **Modifiers after label** - `Button "Save" primary` not `primary Button "Save"`
4. **Grid uses pipes** - `header "Col1 | Col2"` and `row "Val1 | Val2"`

## Common Patterns

**Mobile form:**
```
wireframe mobile
  col
    AppBar "Form Title"
    col padding=24
      Input "Field 1"
      Input "Field 2"
      spacer
      Button "Submit" primary
```

**Multi-screen flow:**
```
wireframe mobile LR
  screen "Login"
    col
      AppBar "Sign In"
      col padding=24
        Input "Email"
        Button "Login" primary
  screen "Home"
    col
      AppBar "Dashboard"
      Title "Welcome"
```

**Desktop sidebar layout:**
```
wireframe desktop
  col
    AppBar "App"
    row flex
      col width=200
        List "Nav 1"
        List "Nav 2"
      col flex
        Title "Content"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using ASCII boxes `[Button]` | Use `Button "label"` |
| Missing quotes on labels | `Title "Hello"` not `Title Hello` |
| Wrong indentation | Exactly 2 spaces per level |
| Tabs instead of spaces | Use spaces only |
| Modifier before label | `Button "X" primary` not `primary Button "X"` |

## Red Flags - You're Doing It Wrong

If you find yourself:
- Drawing `+----+` boxes → Use wireframe syntax
- Writing `| Button |` → Use `Button "label"`
- Making ASCII tables for UI → Use `Grid` with `header`/`row`
- Describing UI in prose → Create a wireframe diagram

**These all mean: Use wireframe syntax instead.**
