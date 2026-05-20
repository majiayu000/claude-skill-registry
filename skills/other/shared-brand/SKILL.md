---
name: shared-brand
description: Brand identity, design tokens, and anti-pattern philosophy shared across all platforms.
---

## Purpose

Define brand identity once. Platform styleguides reference this for colors, typography philosophy, design direction, and anti-patterns — then add platform-specific details.

## Design direction

- **Aesthetic:** premium consumer with selective immersive moments
- **Tone:** confident, intentional, restrained
- **"Wow"** is used sparingly and purposefully

If a screen could belong to any generic product, it does not meet the bar.

## Brand colors

### Core palette

- `brand.orange` = #FF5E1A
- `neutral.white` = #FFFFFF
- `neutral.lightGray` = #DAD9D9
- `neutral.darkGray` = #282828
- `neutral.black` = #000000

### Usage rules

- Raw hex values must not appear in components or views
- All color usage must reference semantic tokens
- Contrast must meet WCAG 2.1 AA in both light and dark modes
- See platform styleguide references for token implementations

## Typography

**Banned as primary/sole font:**
Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Nunito, Source Sans, IBM Plex Sans

Typography must contribute voice, not just legibility. No single neutral sans-serif everywhere.

## Anti-patterns (avoid)

### Cards

- Don't wrap everything in cards
- Don't nest cards inside cards
- Prefer whitespace and scale over borders

### Effects

- No decorative animation — motion must communicate state or causality
- Glass is a material, not decoration — must convey depth or focus
- No overly neutral palettes — brand accent used decisively

### General

- Template layouts shipped unchanged do not meet the bar
- Perfect symmetry without intent
- Unchanged framework defaults (shadcn, PrimeNG, SwiftUI)
