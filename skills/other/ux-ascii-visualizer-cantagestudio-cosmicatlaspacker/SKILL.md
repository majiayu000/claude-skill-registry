---
name: ux-ascii-visualizer
description: "[UI/UX] Visualizes UI screen structures and components as ASCII art. Represents wireframes, layouts, and UI components as text-based diagrams. Use when requesting 'ASCII wireframe', 'screen structure visualization', or 'UI layout drawing'."
---

# UX ASCII Visualizer

A skill that visualizes UI screen structures and components as ASCII art.

## When to Use

- Visualizing screen layouts as text
- Quick wireframe sketching
- Documenting UI component structures
- Creating visual materials for design reviews

## Box Drawing Character Set

### Basic Box (Single Line)
```
┌───┬───┐    ╭───────╮
│   │   │    │ round │
├───┼───┤    ╰───────╯
│   │   │
└───┴───┘
```

### Emphasis Box (Double Line)
```
╔═══╦═══╗
║   ║   ║
╠═══╬═══╣
║   ║   ║
╚═══╩═══╝
```

## UI Component Symbols

### Buttons
```
[Primary Button]     ← Primary button
[[Strong Action]]    ← Emphasized button
( Cancel )           ← Cancel/secondary button
[+] [−] [×] [↻]      ← Icon buttons
```

### Selection Controls
```
(●) Selected         ← Radio (selected)
(○) Unselected       ← Radio (unselected)
[✓] Checked          ← Checkbox (selected)
[ ] Unchecked        ← Checkbox (unselected)
```

### List & Tree
```
▶ Collapsed Item     ← Collapsed item
▼ Expanded Item      ← Expanded item
  ├─ Child 1
  ├─ Child 2
  └─ Child 3
```

## Layout Patterns

### 3-Column Layout (Archon Style)
```
┌──────────┬────────────────┬──────────────────┐
│ Sidebar  │  List Panel    │  Detail Panel    │
│          │                │                  │
│ ▼ Group1 │ ┌────────────┐ │ ┌──────────────┐ │
│   Item1  │ │ List Item 1│ │ │   Content    │ │
│   Item2  │ ├────────────┤ │ └──────────────┘ │
│          │ │ List Item 2│ │                  │
│ ▼ Group2 │ └────────────┘ │ [Save] [Cancel]  │
└──────────┴────────────────┴──────────────────┘
```

## Constraints

- Width should not exceed 80 characters (terminal compatibility)
- Consider CJK characters occupy 2 spaces for alignment
- Split complex screens into multiple diagrams