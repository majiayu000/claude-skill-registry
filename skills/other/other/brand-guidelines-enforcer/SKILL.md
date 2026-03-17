---
name: brand-guidelines-enforcer
description: "[Design System] Lightweight brand guidelines enforcement for UI copy and visual motifs. Use when (1) checking UI labels/buttons/error messages against brand tone, (2) validating color usage in specific contexts, (3) ensuring reserved components are used correctly, (4) user asks to 'check brand guidelines', 'validate brand compliance', 'review copy tone', or 'enforce design rules'."
---

# Brand Guidelines Enforcer

Lightweight enforcement of brand guidelines for UI copy and visual motifs.

## Quick Start

```bash
python3 scripts/enforce_brand.py --guidelines brand.yml --source src/
```

## Violation Types

| Type | Severity | Description |
|------|----------|-------------|
| `wrong-color-context` | warning | Color used outside allowed context |
| `tone-violation` | warning | Copy doesn't match brand voice |
| `reserved-component-misuse` | error | Reserved component in wrong screen |
| `prohibited-word` | error | Prohibited word/pattern found |
| `capitalization-error` | info | Wrong capitalization style |

## Detection Examples

### Tone Violations
```jsx
// Violation: unfriendly error message
<ErrorMessage>Error occurred: Invalid input</ErrorMessage>
// Suggested: "Something went wrong. Please check this field."

// Violation: generic CTA
<Button>Click here</Button>
// Suggested: "Get started" or "Continue"
```