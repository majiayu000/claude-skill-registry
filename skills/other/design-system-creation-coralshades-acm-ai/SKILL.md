---
name: design-system-creation
description: >
  Build comprehensive design systems with components, patterns, and guidelines.
  Enable consistent design, faster development, and better collaboration across
  teams.
---

# Design System Creation

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Reference Guides](#reference-guides)
- [Best Practices](#best-practices)

## Overview

A design system is a structured set of components, guidelines, and principles that ensure consistency, accelerate development, and improve product quality.

## When to Use

- Multiple product interfaces or teams
- Scaling design consistency
- Reducing redundant component development
- Improving design-to-dev handoff
- Creating shared language across teams
- Building reusable components
- Documenting design standards

## Quick Start

Minimal working example:

```yaml
Design System Structure:

Foundation Layer:
  Typography:
    - Typefaces (Roboto, Inter)
    - Font sizes (scale: 12, 14, 16, 20, 28, 36, 48)
    - Font weights (Regular, Medium, Bold)
    - Line heights and letter spacing

Colors:
  - Primary brand color (#2196F3)
  - Secondary colors
  - Neutral palette (grays)
  - Semantic colors (success, error, warning)
  - Dark mode variants

Spacing:
  - Base unit: 4px
  - Scale: 4, 8, 12, 16, 24, 32, 48, 64px
  - Apply consistently across UI

Shadows & Elevation:
  - Elevation 0 (flat)
  - Elevation 1, 2, 4, 8, 16 (increasing depth)
  - Used for modals, cards, overlays
// ... (see reference guides for full implementation)
```

## Reference Guides

Detailed implementations in the `references/` directory:

| Guide | Contents |
|---|---|
| [Design System Components](references/design-system-components.md) | Design System Components |
| [Component Documentation](references/component-documentation.md) | Component Documentation |
| [Design System Governance](references/design-system-governance.md) | Design System Governance |
| [Design System Documentation](references/design-system-documentation.md) | Design System Documentation |

## Best Practices

### ✅ DO

- Start with essential components
- Document every component thoroughly
- Include code examples
- Test components across browsers
- Include accessibility guidance
- Version the design system
- Have clear governance
- Communicate updates proactively
- Gather feedback from users
- Maintain incrementally

### ❌ DON'T

- Create too many components initially
- Skip documentation
- Ignore accessibility
- Make breaking changes without migration path
- Allow inconsistent implementations
- Ignore user feedback
- Let design system stagnate
- Create components without proven need
- Make components too prescriptive
- Ignore performance impact
