---
name: layout-spacing-checker
description: "[Design System] Validate margin/padding/gap values against spacing scale and grid rules. Use when (1) checking if spacing values follow the design system scale, (2) finding off-scale or inconsistent spacing, (3) auditing layout consistency across components, (4) user asks to 'check spacing', 'validate layout', 'audit margins/padding', or 'find off-scale values'."
---

# Layout & Spacing Scale Checker

Validate spacing values against a defined scale and find inconsistencies.

## Quick Start

```bash
python3 scripts/check_spacing.py --scale spacing.yml --source src/
```

## Issue Types

| Type | Severity | Description |
|------|----------|-------------|
| `off-scale` | warning | Value not in spacing scale |
| `inconsistent` | info | Different spacing for similar components |
| `zero-spacing` | info | Potentially missing spacing |
| `excessive` | warning | Unusually large spacing value |

## Detection Examples

### CSS/SCSS
```css
/* off-scale: 17px not in scale */
.card { padding: 17px; }
/* Suggested: 16px (md) or 20px */
```

### SwiftUI
```swift
// off-scale: 15 not in scale
.padding(15)
// Suggested: .padding(16) or spacing token .md
```