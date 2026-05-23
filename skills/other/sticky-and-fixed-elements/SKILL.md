---
name: sticky-and-fixed-elements
description: "Sticky and fixed positioning keeps critical UI persistent as the user scrolls — headers at the top, toolbars at the bottom on mobile. Use deliberately: too many fixed layers create visual noise and reduce content area. Use when designing navigation headers, bottom toolbars, floating action buttons, or table column headers."
metadata:
  priority: 6
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
  promptSignals:
    phrases:
      - "sticky"
      - "fixed"
      - "position: fixed"
      - "position: sticky"
      - "toolbar"
      - "bottom bar"
      - "floating"
      - "persistent header"
retrieval:
  aliases:
    - sticky header
    - fixed toolbar
    - bottom navigation
    - floating action button
    - sticky table header
    - persistent UI
  intents:
    - keep header visible on scroll
    - design a bottom toolbar
    - add a floating action button
    - make table headers sticky
    - decide between sticky and fixed
  examples:
    - should the header be sticky or fixed
    - design a bottom toolbar for mobile
    - keep this toolbar visible while scrolling
---

# Sticky and Fixed Elements

## position: fixed vs position: sticky

| Property | Behaviour | Use for |
|---|---|---|
| `position: fixed` | Removed from document flow. Always stays at the same viewport position regardless of scroll or parent. | Global navigation header, bottom toolbar, floating action button |
| `position: sticky` | Stays in document flow until it hits its scroll threshold, then locks in place. Returns to flow when parent scrolls past. | Table column headers, section headings in a long list, in-page toolbars within a scroll container |

**Prefer `sticky` over `fixed`** when the element belongs to a specific section or scroll context. Fixed elements sit above everything and affect the entire viewport — use them only for truly global UI.

## Top — Navigation Header

The global navigation header is the most common fixed element. It should:

- Remain visible at all times so the user can always navigate away
- Be as thin as possible to maximise content area — 48–64px is a common range
- Have a background and shadow so content scrolling beneath it does not bleed through
- On scroll, a subtle shadow (`--shadow-sm`) signals that content is behind it

```css
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height);
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
  z-index: var(--z-header);
}
```

Compensate for the fixed header with matching top padding on the page body:
```css
body { padding-top: var(--header-height); }
```

## Bottom — Toolbar on Mobile

On mobile, the bottom of the screen is the most reachable area with one thumb. A persistent bottom toolbar is the natural home for:

- Primary navigation (bottom tab bar — iOS and Android convention)
- Contextual actions for the current view (edit, share, delete)
- A floating action button (FAB) for the single most important action

Bottom toolbars should:
- Respect the safe area inset on devices with a home indicator: `padding-bottom: env(safe-area-inset-bottom)`
- Be visually separated from content (background fill, top border, or shadow)
- Contain 3–5 items maximum — more than 5 should move to a menu or a different pattern
- Use icons with labels for navigation tabs, or icons alone for contextual toolbars (with tooltips)

On desktop, bottom toolbars are uncommon. Status bars, editor toolbars, and command palettes are the desktop equivalent — these are typically `position: fixed` at the bottom or `position: sticky` within their scroll container.

## Sticky Table Headers

For data tables inside a scroll container, sticky column headers prevent the user from losing track of what each column means.

```css
thead th {
  position: sticky;
  top: 0;
  background: var(--color-surface);
  z-index: 1;
}
```

If the table also has a sticky first column (for row identifiers), the top-left cell needs both `top: 0` and `left: 0`, and a higher `z-index` to sit above both the header row and the sticky column.

## Stacking and Z-index

Sticky and fixed elements create stacking context. Define z-index as named tokens, not arbitrary numbers:

```css
--z-base:       0;
--z-dropdown:   100;
--z-sticky:     200;
--z-header:     300;
--z-modal:      400;
--z-toast:      500;
```

Every fixed or sticky element must declare its z-index explicitly using a token. Avoid ad-hoc values like `z-index: 9999` — they signal an unmanaged stacking context and will eventually conflict.

## How Many Fixed Layers Is Too Many

Each fixed layer removes space from the content area and adds visual complexity. A page should rarely need more than:

- 1 fixed header (top)
- 1 fixed toolbar or bottom nav (bottom, mobile)
- 1 floating action button or contextual overlay

A fixed header + fixed bottom toolbar + floating button + sticky sidebar + sticky table header all simultaneously is too many layers. Consolidate where possible.

## Review Checklist

- [ ] Is `sticky` used for section-scoped elements and `fixed` only for truly global UI?
- [ ] Does the fixed header compensate for its height with body padding?
- [ ] Does the bottom toolbar respect `env(safe-area-inset-bottom)` on mobile?
- [ ] Are all z-index values defined as named tokens, not arbitrary numbers?
- [ ] Is the total number of simultaneous fixed layers minimal — header + one bottom element maximum in most cases?
- [ ] Does content scrolling behind a fixed element not visually bleed through (background + shadow on the fixed element)?
