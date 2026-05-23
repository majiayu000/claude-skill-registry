---
name: component-family-consistency
description: Buttons, inputs, pills, badges, calendars, and other interactive components form a visual family — they share the same border-radius, colour logic, shadow scale, border style, and spacing rhythm. Inconsistency between them breaks the sense of a coherent product. Use when building or reviewing a component library, design system, or any set of UI components.
metadata:
  priority: 8
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/tokens/**"
    - "**/theme/**"
    - "design-system/**"
    - "tailwind.config.*"
  promptSignals:
    phrases:
      - "component library"
      - "design system"
      - "button"
      - "input"
      - "form"
      - "badge"
      - "pill"
      - "consistent components"
      - "component family"
retrieval:
  aliases:
    - component family
    - design system consistency
    - component tokens
    - visual consistency
    - form components
    - ui components
  intents:
    - make components look consistent
    - build a component library
    - review design system consistency
    - align button and input styles
    - create visual cohesion
  examples:
    - my buttons and inputs look like they are from different products
    - make all form components consistent
    - review this component library for visual consistency
---

# Component Family Consistency

Every interactive component in a product — buttons, inputs, selects, checkboxes, radio buttons, pills, badges, tags, calendars, date pickers, sliders, toggles — belongs to the same visual family. They share a common design DNA. A user should be able to look at any component and feel that it belongs to the same product as every other component.

When components are designed in isolation without shared tokens, the product feels assembled from parts rather than built as a whole.

## The Shared DNA

Define these tokens once. Every component inherits from them.

### Border-Radius
All interactive components use the same base radius token. Variations are derived, not invented.

```css
--radius-base:    8px;   /* buttons, inputs, selects */
--radius-sm:      4px;   /* checkboxes, small badges */
--radius-lg:      12px;  /* cards, modals, large panels */
--radius-full:    9999px; /* pills, tags, avatar chips */
```

A button and an input on the same form must have the same radius. A pill is always `--radius-full`. A badge is `--radius-sm` or `--radius-full` depending on brand tone — but consistent across all badges.

### Border Style

Borders across all form components and containers should use a highly restricted set of tokens.

**The 2-Step Rule:** Limit border widths to at most two options (e.g., `1px` and `4px`, or `1px` and `8px`). Do not use an incremental scale like `1px, 2px, 3px, 4px...`. A limited choice makes the hierarchy clear and the product feel intentional.

```css
--border-width-thin:   1px;   /* Default for inputs, cards, dividers */
--border-width-thick:  4px;   /* Featured items, bold accents, active indicators */

--border-color:        var(--color-border);
--border-color-focus:  var(--color-primary);
--border-color-error:  var(--color-error);
```

An input border and a select border are identical at rest. Focus state uses `--border-color-focus` everywhere. Error state uses `--border-color-error` everywhere.

### Spacing and Height
Components at the same visual scale share height and internal padding.

```css
/* Default (md) size */
--component-height-md:    40px;
--component-padding-x-md: 12px;
--component-padding-y-md: 8px;

/* Small */
--component-height-sm:    32px;
--component-padding-x-sm: 8px;
--component-padding-y-sm: 6px;

/* Large */
--component-height-lg:    48px;
--component-padding-x-lg: 16px;
--component-padding-y-lg: 10px;
```

A button and an input placed next to each other must be the same height. This is not cosmetic — mismatched heights break form layouts and signal disorder.

### Shadow
Interactive components use a consistent shadow logic:

- At rest: no shadow, or `--shadow-xs` for floating components (select dropdown trigger)
- On focus: focus ring via `outline`, not `box-shadow` (unless using `box-shadow` as the focus ring consistently)
- Elevated (dropdowns, popovers opening from components): `--shadow-md`

### Colour Logic
The same colour roles apply uniformly across all components:

| State | Colour token |
|---|---|
| Rest border | `--color-border` |
| Focus border / ring | `--color-primary` |
| Error border | `--color-error` |
| Disabled | `--color-text-secondary` at reduced opacity |
| Selected / active fill | `--color-primary` |
| Hover background | `--color-primary` at 8–12% opacity |

## Component Family Members

| Component | Shares radius | Shares height | Shares border | Shares colour logic |
|---|---|---|---|---|
| Button | ✓ | ✓ | — (filled) | ✓ |
| Input / textarea | ✓ | ✓ | ✓ | ✓ |
| Select | ✓ | ✓ | ✓ | ✓ |
| Checkbox | `--radius-sm` | — | ✓ | ✓ |
| Radio | `--radius-full` | — | ✓ | ✓ |
| Toggle / switch | `--radius-full` | ✓ | — | ✓ |
| Pill / tag | `--radius-full` | ✓ | ✓ optional | ✓ |
| Badge | `--radius-sm` or `--radius-full` | — | — | ✓ |
| Date picker / calendar | `--radius-base` | ✓ | ✓ | ✓ |
| Slider | `--radius-full` (track + thumb) | — | — | ✓ |
| Search input | ✓ | ✓ | ✓ | ✓ |
| Combobox | ✓ | ✓ | ✓ | ✓ |

## Gradients in Components

If the brand uses gradients, apply them consistently:

- A gradient on a primary button should use the same gradient angle and stops as gradient usage elsewhere in the product
- Hover state: slightly shift the gradient lightness, not the hue
- Do not use gradients on some button variants and flat colour on others — pick one approach per variant and apply it universally

## Review Checklist

- [ ] Do buttons and inputs on the same form share the same height?
- [ ] Do all bordered components use at most two border-width options (e.g., 1px and 4px)?
- [ ] Does focus state look identical across all focusable components?
- [ ] Does error state look identical across all components that can have errors?
- [ ] Are all radius values derived from the same base token — not set independently per component?
- [ ] Do pills and tags use `--radius-full` consistently?
- [ ] Is gradient usage (if any) consistent across all button variants?
- [ ] Could a new component be added to the library using only existing tokens?
