---
name: scroll-areas
description: Scroll areas inside a layout should be avoided wherever possible. When unavoidable, allow only one scroll axis at a time and always keep the user in control. Use when designing layouts, data tables, panels, or any component that might introduce an inner scroll container.
metadata:
  priority: 7
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
      - "scroll"
      - "overflow"
      - "scrollable"
      - "inner scroll"
      - "fixed height"
      - "overflow-y"
      - "overflow-x"
retrieval:
  aliases:
    - scroll areas
    - inner scroll
    - overflow scroll
    - nested scroll
    - scrollable container
  intents:
    - avoid scroll inside scroll
    - design a scrollable list
    - handle overflow content
    - layout with constrained height
  examples:
    - should this panel scroll independently
    - how do I handle a long list inside a fixed layout
    - avoid scroll inside scroll
---

# Scroll Areas

## Avoid Scroll Areas by Default

Scroll containers inside a layout — panels, drawers, tables, modals with inner overflow — create friction. Users must discover that a region scrolls, manage multiple independent scroll positions simultaneously, and context-switch between scroll areas on the same screen.

**Default: let the page scroll.** A single page-level scroll is universally understood and requires no discovery. Before introducing an inner scroll area, ask whether the layout can be restructured so the page itself handles the overflow.

Alternatives to inner scroll:
- Pagination or load-more for long lists
- Collapsible sections (accordion) for long detail panels
- A separate page or route for content that would otherwise fill a scroll area
- Progressive disclosure — show less by default, expand on demand

## When a Scroll Area Is Justified

Some layouts genuinely require inner scroll:

- **Fixed-height sidebars** with navigation trees longer than the viewport
- **Data tables** where the header must remain visible while rows scroll
- **Chat or log panels** where the stream is continuous and the surrounding layout is fixed
- **Code editors or terminal panes** embedded in a larger application shell

In these cases, proceed — but apply the constraints below.

## One Axis Only

Never create a scroll container that scrolls on both axes simultaneously. Two-axis scroll is disorienting, hard to control precisely, and nearly unusable on touch devices.

```css
/* One axis: vertical */
overflow-y: auto;
overflow-x: hidden;

/* One axis: horizontal (e.g. wide table) */
overflow-x: auto;
overflow-y: hidden;

/* Never */
overflow: auto; /* allows both axes */
```

If content requires both axes — e.g. a wide table inside a constrained panel — restructure the layout so the table's horizontal scroll is the only scroll in the view, with the page itself not scrolling at that point.

## Always User-Controlled

Scroll must never happen automatically without user intent. Specifically:

- **No auto-scrolling** that moves the viewport without the user initiating it
- **No scroll hijacking** — do not intercept the native scroll event to animate or pace it artificially
- **Scroll-to on load** is acceptable only when restoring a previous scroll position (e.g. returning to a list after navigating away)
- **Scroll-to for errors or anchors** is acceptable as a response to a user action (submitting a form with errors, clicking a table-of-contents link)

Exception: chat and log panels may auto-scroll to the bottom on new content, but only if the user is already at the bottom. If the user has scrolled up to read, do not force them back down — show a "new messages" indicator instead.

## Scroll Affordance

Users must be able to tell a region is scrollable before they attempt to scroll it.

- Clip content visually at the edge — a partially visible item signals "there is more"
- Use a subtle scrollbar (not `scrollbar-width: none`) so the track is visible
- On touch, a partial item at the edge is the primary affordance — ensure the container does not have `overflow: hidden` on the trailing edge

## Review Checklist

- [ ] Is every inner scroll area genuinely necessary, or can the layout be restructured to use page scroll?
- [ ] Does every scroll container scroll on one axis only?
- [ ] Is `overflow: auto` (two-axis) avoided on all scroll containers?
- [ ] Is scroll always user-initiated — no hijacking, no forced auto-scroll?
- [ ] Is the scrollable region visually apparent (partial content, visible scrollbar)?
- [ ] On touch devices, is scroll smooth and native (`-webkit-overflow-scrolling: touch` or equivalent)?
