---
name: building-tour-cards
description: Guidelines for the Tour Card UI, the primary item in the tour grid. Use when building the tour browsing interface.
---

# Tour Card UI Component

## When to use this skill
- Building the travel catalog.
- Implementing "Featured Tours" on the homepage.

## Design Specs
- **Image**: Aspect ratio 4:3, rounded corners.
- **Content**:
    - Right: Rating (Star icon + number).
    - Top: Title (Bold, 1.1rem).
    - Subtitle: Location (Muted text + pin icon).
    - Bottom: Price (Prominent, e.g., "$299/person").
- **Hover**: Subtle lift/shadow effect.

## Instructions
- **Accessibility**: Use semantic tags (`article`, `h3`).
- **Performance**: Use `next/image` for optimized tour images.
