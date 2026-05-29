---
name: ascii-diagrams
description: Create and fix ASCII diagrams, tables, wireframes, box-drawings. Use when message contains Unicode box characters (┌┐└┘│─), user asks to create/fix text visualization, align borders, or fix broken ASCII art. Triggers on "поправ діаграму", "fix diagram", "create table", "вирівняй", "align boxes".
---

# ASCII Diagrams & Text Visualization

Create and repair pixel-perfect monospace diagrams, tables, and wireframes.

## Core Principle

> **Every character counts.** In monospace, misaligned borders break visual structure instantly.

## Validation Script

Always validate diagrams before committing:

```bash
python scripts/validate_boxes.py <file.md>        # Check for issues
python scripts/validate_boxes.py <file.md> --fix  # Auto-fix width issues
```

## Quick Reference: Box Drawing Characters

```
Corners:  ┌ ┐ └ ┘  (light)     ╔ ╗ ╚ ╝  (double)
Lines:    ─ │      (light)     ═ ║      (double)
T-joins:  ┬ ┴ ├ ┤  (light)     ╦ ╩ ╠ ╣  (double)
Cross:    ┼        (light)     ╬        (double)
Rounded:  ╭ ╮ ╰ ╯  (rounded corners)
```

## Creating Tables

### Standard Table Pattern

```
┌─────────────┬────────────┬───────┐
│ Column 1    │ Column 2   │ Col 3 │
├─────────────┼────────────┼───────┤
│ Value here  │ Another    │ 123   │
│ More data   │ Content    │ 456   │
└─────────────┴────────────┴───────┘
```

**Construction rules:**
1. Count characters in widest cell per column
2. Add 1 space padding on each side (cell width + 2)
3. Draw top border: `┌` + `─` × width + `┬` between columns + `┐`
4. Draw header row with `│` separators
5. Draw separator: `├` + `─` × width + `┼` between columns + `┤`
6. Draw data rows
7. Draw bottom: `└` + `─` × width + `┴` between columns + `┘`

### Markdown-Compatible Table

When ASCII boxes render poorly, use pipe tables:

```markdown
| Status      | Count | Action   |
|-------------|-------|----------|
| Connected   | 42    | None     |
| Pending     | 7     | Review   |
```

## Creating Wireframes

### Modal/Dialog Pattern

```
╭────────────────────────────────────────╮
│  Modal Title                        ✕  │
├────────────────────────────────────────┤
│                                        │
│  Content area with description         │
│  text that explains the action.        │
│                                        │
│  ┌──────────────────────────────────┐  │
│  │ Input field                      │  │
│  └──────────────────────────────────┘  │
│                                        │
│               [Cancel]  [Confirm]      │
│                                        │
╰────────────────────────────────────────╯
```

### Card Pattern

```
┌──────────────────────────────────┐
│ ◉ Card Title             [···]  │
├──────────────────────────────────┤
│                                  │
│  Card content goes here with    │
│  multiple lines of text.        │
│                                  │
│  ● Status: Active               │
│  ○ Priority: Medium             │
│                                  │
└──────────────────────────────────┘
```

### Layout Grid

```
┌────────────────────────────────────────────────┐
│                    Header                      │
├────────────┬───────────────────────────────────┤
│            │                                   │
│  Sidebar   │         Main Content              │
│            │                                   │
│  ○ Nav 1   │   ┌──────────┐  ┌──────────┐     │
│  ● Nav 2   │   │  Card 1  │  │  Card 2  │     │
│  ○ Nav 3   │   └──────────┘  └──────────┘     │
│            │                                   │
├────────────┴───────────────────────────────────┤
│                    Footer                      │
└────────────────────────────────────────────────┘
```

## Creating Flow Diagrams

### Horizontal Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Start  │────▶│ Process │────▶│   End   │
└─────────┘     └─────────┘     └─────────┘
```

### Vertical Flow with Branching

```
          ┌─────────┐
          │  Input  │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │ Decide  │
          └────┬────┘
               │
         ┌─────┴─────┐
         ▼           ▼
   ┌─────────┐ ┌─────────┐
   │   Yes   │ │   No    │
   └────┬────┘ └────┬────┘
        │           │
        └─────┬─────┘
              ▼
          ┌─────────┐
          │ Output  │
          └─────────┘
```

### Architecture Diagram

```
┌───────────────────────────────────────────────┐
│                  Frontend                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  React   │  │  Zustand │  │  Query   │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼───────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │ HTTP/WS
                      ▼
┌───────────────────────────────────────────────┐
│                  Backend                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ FastAPI  │──│ Services │──│  Models  │    │
│  └──────────┘  └────┬─────┘  └────┬─────┘    │
└─────────────────────┼─────────────┼───────────┘
                      │             │
        ┌─────────────┴─────────────┘
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Postgres│   │  NATS   │   │  Redis  │
   └─────────┘   └─────────┘   └─────────┘
```

## Special Elements

### Icons & Indicators

```
Status:     ● active   ○ inactive   ◐ partial
Checkbox:   ☑ checked  ☐ unchecked  ☒ disabled
Arrows:     → ← ↑ ↓    ▶ ◀ ▲ ▼      ➜ ➤
Progress:   ▓▓▓▓▓░░░░░ (50%)
Stars:      ★★★☆☆ (3/5)
Bullets:    • ◦ ‣ ⁃
```

### Button Representations

```
Standard:  [Button]    [  OK  ]   [Cancel]
Primary:   【Submit】   ⟦ Action ⟧
Rounded:   ( Click )   (  Go  )
```

## Fixing Broken Diagrams

### CRITICAL: Always Diagnose First

**Before manually fixing, run this diagnostic:**

```bash
python3 << 'EOF'
diagram = """
PASTE_DIAGRAM_HERE
"""
print("Line-by-line analysis:\n")
for i, line in enumerate(diagram.strip().split('\n'), 1):
    has_broken = '�' in line or '\ufffd' in line
    marker = '⚠️  BROKEN CHAR' if has_broken else ''
    print(f"{i:2d}: len={len(line):3d} {marker}")
    if has_broken:
        # Find position of broken chars
        for j, c in enumerate(line):
            if c == '�' or ord(c) == 0xFFFD:
                print(f"    Position {j}: replacement character (corrupted Unicode)")
EOF
```

**Common diagnostic findings:**

| Finding | Cause | Fix |
|---------|-------|-----|
| `len` varies by 1-2 | Missing/extra spaces | Pad to max length |
| `⚠️ BROKEN CHAR` | Corrupted Unicode (copy/paste issue) | Replace `�` with `─` |
| Very different lengths | Nested box misalignment | Realign inner boxes |

### Diagnostic Checklist

1. **Count border lengths** - top `─` count must equal bottom
2. **Check vertical alignment** - all `│` must be in same column
3. **Verify corner usage** - `┌┐` top, `└┘` bottom, never mixed
4. **Match cell widths** - every row same total width
5. **Consistent spacing** - same padding in all cells
6. **No broken chars** - search for `�` (U+FFFD replacement character)

### Common Issues & Fixes

**Issue: Jagged right edge**
```
❌ BROKEN                     ✅ FIXED
┌───────────────────┐        ┌───────────────────┐
│ Short          │           │ Short             │
│ Much longer text│           │ Much longer text  │
└──────────────────┘          └───────────────────┘
```
Fix: Pad shorter lines with spaces to match longest line.

**Issue: Mismatched borders**
```
❌ BROKEN                     ✅ FIXED
┌───────────────────┐        ┌───────────────────┐
│ Content          |         │ Content           │
└──────────────────-┘         └───────────────────┘
```
Fix: Use consistent box characters (`│` not `|`, `─` not `-`).

**Issue: Wrong corner characters**
```
❌ BROKEN                     ✅ FIXED
+-------------------+        ┌───────────────────┐
| Content           |        │ Content           │
+-------------------+        └───────────────────┘
```
Fix: Replace ASCII `+` `-` `|` with proper box drawing characters.

## Validation Checklist

Before committing any ASCII diagram:

```
□ All horizontal borders same length
□ All vertical bars aligned in columns
□ Corners use correct characters (┌┐└┘)
□ Content properly padded with spaces
□ No mixed ASCII/Unicode border chars
□ Renders correctly in monospace font
□ Width fits target display (80-120 chars typical)
□ Run: python scripts/validate_boxes.py <file>
```

## Width Guidelines

| Context        | Max Width | Notes                      |
|----------------|-----------|----------------------------|
| Markdown docs  | 80 chars  | Traditional terminal width |
| Code comments  | 72 chars  | Leaves room for indent     |
| Wide displays  | 120 chars | Modern monitors            |
| GitHub README  | 100 chars | Optimal for web rendering  |

## Pro Tips

1. **Draft in stages** - Draw outer box first, then inner structure
2. **Use placeholders** - Mark widths with `XXX` then replace
3. **Copy working patterns** - Start from examples above
4. **Validate always** - Run `validate_boxes.py` before saving
5. **Consider alternatives** - Sometimes Mermaid/PlantUML better for complex diagrams
