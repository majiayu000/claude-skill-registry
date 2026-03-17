---
name: design-tokens-validator
description: "[Design System] Validate that code and styles use official design tokens instead of hard-coded values. Use when (1) reviewing CSS/SCSS/Tailwind/styled-components for hard-coded colors/spacing, (2) checking SwiftUI/UIKit for raw color/font values, (3) auditing Unity styles for magic numbers, (4) enforcing design system compliance, (5) user asks to 'check design tokens', 'validate tokens', 'find hard-coded values', or 'audit design system usage'."
---

# Design Tokens Validator

Scan source files for hard-coded design values and suggest official token replacements.

## Quick Start

```bash
python3 scripts/validate_tokens.py --tokens tokens.json --source src/
```

## Supported Token Categories

| Category | Example Token | Detects |
|----------|--------------|---------|
| Colors | `color.primary.500` | Hex (#FF0000), rgba(), hsl(), named colors |
| Typography | `font.size.md`, `font.weight.bold` | px/rem font sizes, numeric weights |
| Spacing | `spacing.4`, `spacing.lg` | px/rem padding/margin/gap values |
| Radius | `radius.md` | Border-radius values |
| Shadows | `shadow.lg` | Box-shadow definitions |

## Detection Examples

### CSS/SCSS
```css
/* Violation */
.card { color: #222222; padding: 17px; }

/* Correct */
.card { color: var(--color-text-primary); padding: var(--spacing-4); }
```

### SwiftUI
```swift
// Violation
Text("Hello").foregroundColor(Color(hex: "#222222"))

// Correct
Text("Hello").foregroundColor(.textPrimary)
```