---
name: surface-separation
description: A surface is set apart from its background by exactly one means — a border, an elevation, or a fill. Combining all three reads as noise. Opacity is a state signal, not a tinting tool; layering translucency over translucency makes contrast unpredictable and impossible to verify. Use when designing cards, panels, list rows, toolbars, or any container that needs to read as distinct from what sits behind it.
metadata:
  priority: 7
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
      - "card"
      - "panel"
      - "surface"
      - "border"
      - "opacity"
      - "transparent"
      - "container"
      - "too busy"
retrieval:
  aliases:
    - surface separation
    - card boundaries
    - opacity misuse
    - transparent layers
    - visual noise
    - container styling
  intents:
    - make a card read as distinct
    - stop the UI looking busy
    - decide between border and shadow
    - use transparency correctly
    - fix unpredictable contrast
  examples:
    - this panel looks noisy, what do I remove
    - should this card have a border or a shadow
    - can I use opacity to lighten this colour
    - why does my contrast check fail on this overlay
---

# Surface Separation

A surface — a card, a panel, a toolbar, a row — needs to read as distinct from whatever sits behind it. There are exactly three ways to achieve that, and the mistake is almost always using more than one at full strength rather than choosing badly between them.

## Pick One Strategy Per Surface

| Strategy | Mechanism | Reads as | Best for |
|---|---|---|---|
| **Border** | 1px line at the boundary | Precise, drawn, documentary | Dense UI, tables, forms, anything where the edge itself carries meaning |
| **Elevation** | Shadow implying height | Floating, temporary, above | Modals, dropdowns, popovers, drag states |
| **Fill** | Contrasting background tone | Grouped, embedded, part of the page | Sections, sidebars, alternating rows, inline callouts |

Each answers a different question. A border says *where the surface ends*. An elevation says *how far above the page it sits*. A fill says *what it belongs to*. Choose based on which question the user actually has.

**The rule:** never combine all three on the same surface. A card that carries a visible border, a drop shadow, and a background tone distinct from the page is stating its boundary three times. Nothing is emphasised because everything is. This is the most common single cause of a UI that someone describes as "busy" or "heavy" without being able to point at why.

### The Legitimate Pair

Border and elevation together are correct in one specific case: a light surface on a light page, where a subtle shadow alone washes out and the edge goes fuzzy. Here the border defines the boundary and the shadow supplies the depth — they do different jobs. See [[elevation-and-depth]] for the shadow scale and the border tone that pairs with it.

What keeps this to two signals is that the surface fill stays at or near the page tone. The moment you also push the background a clear step away, the edge is being stated a third time.

### Nesting

A surface inside a surface should change strategy, not intensify the same one. A bordered card containing bordered rows produces a grid of lines with no hierarchy. Use a fill shift for the inner rows, or drop the inner borders and rely on spacing — see [[gestalt-ui-organisation]] for when proximity alone is enough to group.

Depth of nesting is the real constraint. Past two levels of visible separation, no strategy reads clearly. Flatten the structure instead.

## Opacity Is a State, Not a Tint

Opacity communicates that an element is **temporarily not fully available**: disabled, loading, pending, dragging. That is its entire job in a UI.

```css
.btn:disabled     { opacity: 0.4; }
.card.is-loading  { opacity: 0.7; }
.row.is-dragging  { opacity: 0.5; }
```

Reserving it for this makes it legible. When opacity appears for any other reason, the signal stops meaning anything.

### Never Tint With Transparency

Reaching for `rgba(brand, 0.1)` or `opacity: 0.6` to produce a lighter shade of a colour is the anti-pattern. Define the tint as a real token instead:

```css
/* Wrong — the rendered colour depends on whatever is behind it */
.badge { background: rgba(37, 99, 235, 0.12); }

/* Right — a resolved token with a known value */
.badge { background: var(--color-brand-50); }
```

Three things break with the transparent version:

1. **The colour is not knowable.** It resolves against whatever sits behind it, which changes with the parent, the theme, and the scroll position. Two instances of the same component render as different colours.
2. **Contrast cannot be verified.** WCAG ratios are computed between two concrete colours. A translucent layer has no concrete colour until it composites, so no automated check can confirm the text on it is readable — and it will pass in one context and fail in another.
3. **The design system loses the value.** A tint that exists only as an alpha multiplier is not a token. It cannot be referenced, exported, versioned, or swapped per theme.

Derive tints algorithmically from the brand colour and store them as tokens — [[algorithmic-color-palette]] covers deriving a full ramp from one or two source colours.

### Translucency on Translucency

The failure compounds when a translucent element sits on another translucent element. Each layer multiplies against the last, so the final rendered colour depends on the whole chain beneath it — and nobody knows that chain while authoring the component.

**Never set `opacity` on an element whose `background-color` already carries an alpha channel.** If both appear on the same component, one of them is doing the wrong job: either the background should be an opaque token, or the opacity should be a state and the background should not be translucent.

Glass and frosted effects are the deliberate exception, because unpredictable background is the point. They come with a cost: the text on them needs its own opaque backing, or a contrast guarantee that holds against the worst-case backdrop. Do not let a glass surface carry body copy without one.

### Disabled Is the Exception That Proves It

Disabled elements are exempt from WCAG contrast minimums, which is exactly why low opacity is correct there and nowhere else — it is the one place where deliberately unreadable is the intended message. Opacity alone is still not enough to communicate disabled: pair it with `cursor: not-allowed` and a non-interactive state. [[button-states]] has the full state matrix.

## Checklist

- [ ] Does each surface use one separation strategy, or a border/elevation pair with a page-tone fill?
- [ ] Is any surface carrying a border, a shadow, and a distinct fill at once?
- [ ] Does nested separation change strategy rather than repeat it, and stop at two levels?
- [ ] Is every `opacity` value in the codebase attached to a state — disabled, loading, dragging?
- [ ] Are all tints real tokens rather than alpha multipliers?
- [ ] Does any component set `opacity` on top of an already-translucent background?
- [ ] Does text on a glass surface have an opaque backing or a worst-case contrast guarantee?
