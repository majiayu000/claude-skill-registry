---
name: variant-consistency-checker
description: "[Design System] Validate UI component usage against design system specifications. Use when (1) checking component variants/sizes are valid, (2) verifying required props are present, (3) detecting deprecated component usage, (4) finding disallowed prop combinations, (5) user asks to 'check component usage', 'validate variants', 'audit design system compliance', or 'find component inconsistencies'."
---

# Variant Consistency Checker

Validate UI component usage against design system specifications.

## Quick Start

```bash
python3 scripts/check_variants.py --spec components-spec.yml --source src/
```

## Issue Types

| Type | Description |
|------|-------------|
| `unknown-variant` | Variant not in spec |
| `unknown-size` | Size not in spec |
| `missing-prop` | Required prop absent |
| `deprecated` | Using deprecated component |
| `disallowed-combination` | Invalid prop combination |
| `unknown-component` | Component not in spec |
| `unknown-prop` | Prop not defined (strict mode) |

## Detection Examples

### React/JSX
```jsx
// Issues detected:
<Button variant="outline" size="xl" />
//       ↑ unknown-variant  ↑ unknown-size

<Button variant="primary" />
//       ↑ missing-prop: children
```