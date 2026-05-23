---
name: elevation-and-depth
description: Elevation — subtle shadows and layering — communicates visual hierarchy by lifting elements above the surface. Combined with border-radius, it creates the tactile quality of cards, modals, and interactive surfaces. Use when designing cards, dropdowns, modals, tooltips, or any floating UI element.
metadata:
  priority: 6
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "**/tokens/**"
    - "**/theme/**"
    - "tailwind.config.*"
    - "design-system/**"
    - "components/**"
  promptSignals:
    phrases:
      - "shadow"
      - "elevation"
      - "card"
      - "border radius"
      - "depth"
      - "floating"
      - "modal"
      - "dropdown"
retrieval:
  aliases:
    - elevation
    - box shadow
    - card design
    - depth hierarchy
    - border radius
    - floating elements
  intents:
    - make a card stand out
    - design elevation system
    - set up shadow tokens
    - make hierarchy feel physical
    - style a modal or dropdown
  examples:
    - make this card feel elevated
    - set up a shadow scale for the design system
    - what border radius should cards use
---

# Elevation and Depth

Elevation uses shadow and layering to communicate that an element sits above the base surface — giving UI a sense of physical depth. Combined with border-radius, it creates the tactile quality that makes cards graspable, modals clearly floating, and dropdowns feel like they've appeared on top of content.

## The Elevation Scale

Define a small set of elevation levels as tokens. Each level maps to a specific UI role.

| Level | Token | Shadow | Role |
|---|---|---|---|
| 0 | `--shadow-none` | none | Flat surface, inline elements |
| 1 | `--shadow-xs` | `0 1px 2px rgba(0,0,0,0.06)` | Subtle card, table row hover |
| 2 | `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.10), 0 1px 2px rgba(0,0,0,0.06)` | Card, input focus ring area |
| 3 | `--shadow-md` | `0 4px 6px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.06)` | Dropdown, popover |
| 4 | `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.05)` | Modal, dialog, side drawer |
| 5 | `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.08), 0 8px 10px rgba(0,0,0,0.04)` | Command palette, full-screen overlay |

Keep shadows subtle. Dark, heavy shadows feel dated and visually aggressive. Light, diffuse shadows feel modern and material.

### The "Shadow + Border" Rule
A subtle shadow on a white surface can sometimes "wash out," making the edge of a card feel fuzzy or indistinct.
- **Rule:** For elevated white cards or sections, pair the shadow with a **1px border** that is slightly darker (1.5x to 2x) than the shadow's core tone (e.g., a medium grey like `#E2E8F0` or `grey-200`).
- **Effect:** The border defines the physical boundary of the card, while the shadow provides the depth. Together, they make the component "pop" with much higher clarity than using either alone.

### Subtle Gradients for Depth
Gradients can be used to bring "liveliness" to an interface and reinforce the sense of elevation.
- **The Lighting Metaphor:** A subtle linear gradient (top-to-bottom) that is slightly lighter at the top mimics natural overhead lighting. This makes a surface feel more physical and elevated than a flat fill.
- **The 5% Rule:** Keep the gradient extremely subtle. A change in lightness of only 2–5% between the top and bottom is usually enough. If the user can easily see where the gradient starts and ends, it is likely too heavy.
- **Usage:** Apply to primary buttons, hero cards, and header sections to improve visual hierarchy and brand personality.

## Pairing Elevation with Border-Radius

Border-radius and shadow work together to define the character of a surface. The combination signals the element's role and the product's visual tone.

| Surface | Shadow | Border-Radius | Tone |
|---|---|---|---|
| Inline chip / tag | none | `--radius-full` (pill) | Flat, lightweight |
| Card | `--shadow-sm` | `--radius-md` (8–12px) | Graspable, contained |
| Dropdown / popover | `--shadow-md` | `--radius-md` (8px) | Floating, contextual |
| Modal / dialog | `--shadow-lg` | `--radius-lg` (12–16px) | Prominent, focused |
| Toast / notification | `--shadow-md` | `--radius-md` | Ephemeral, above content |
| Button | none or `--shadow-xs` | **consistent across all buttons** — see below |

## Border-Radius Consistency Rule

**Button border-radius must not vary within a product.** All buttons — primary, secondary, destructive, ghost — use the same radius token. Varying radius between button types breaks visual consistency and implies a semantic difference that does not exist.

```css
/* Correct: one radius for all buttons */
.btn { border-radius: var(--radius-button); }

/* Wrong: different radii for different button variants */
.btn-primary { border-radius: 8px; }
.btn-secondary { border-radius: 4px; }  /* ← breaks consistency */
```

The button radius token is a brand decision — set it once, apply it everywhere.

## Text Shadow for Contrast and Separation

`text-shadow` can lift text off a background without changing colours — useful when contrast is marginal or text sits on a photograph, gradient, or complex background.

The effect must be imperceptible as a shadow. If the user notices the shadow, it is too strong.

```css
/* On images or complex backgrounds */
.hero-title {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
}

/* Very subtle separation from a near-matching background */
.label-on-tinted-surface {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
}

/* White text on light background — use a dark shadow, not white */
.inverted-text {
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.30);
}
```

**Rules:**
- Opacity: stay below `0.30` — above that it reads as a design choice rather than a refinement
- Blur: `2–4px` maximum — higher values make text feel dirty
- Offset: `0 1px` or `0 0` — directional offsets above 2px look like retro Web 2.0
- Never use `text-shadow` to compensate for a contrast failure — fix the colour first. Use it only when colours are already close to passing and a nudge is needed, or when text sits on unpredictable imagery

## Dark Mode Shadows

Shadows are less visible on dark backgrounds. On dark surfaces, compensate with:
- Slightly higher opacity on shadow values
- Adding a subtle border (`1px solid rgba(255,255,255,0.08)`) to define card edges
- Increasing the elevation level by one step for the same perceived depth

## Review Checklist

- [ ] Is there a defined elevation scale as design tokens (not one-off shadow values per component)?
- [ ] Does each elevated element use the correct level for its role (card ≠ modal)?
- [ ] Are shadows light and diffuse, avoiding heavy black (#000) defaults?
- [ ] For white cards on light backgrounds, is the shadow paired with a 1px border for better definition?
- [ ] Is border-radius consistent across all button variants?
- [ ] Do shadows feel subtle and diffuse rather than heavy and dark?
- [ ] On dark surfaces, are card/panel edges visible through border or adjusted shadow?
- [ ] Is elevation used to communicate layering — not just decoration?
- [ ] If gradients are used, are they subtle (2–5% lightness change) and used to reinforce the lighting/elevation metaphor?

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Different border-radius on primary vs secondary buttons | Implies semantic difference that doesn't exist | Single `--radius-button` token for all buttons |
| Heavy `box-shadow: 0 8px 16px rgba(0,0,0,0.4)` | Feels dated and visually aggressive | Use low-opacity, multi-layer diffuse shadows |
| Shadow on every element regardless of role | Elevation loses meaning when everything is elevated | Reserve shadow for genuinely floating elements |
| Flat cards with no elevation on a white background | Card edge disappears into the page | Use `--shadow-sm` or a `1px` border to define the card boundary |
