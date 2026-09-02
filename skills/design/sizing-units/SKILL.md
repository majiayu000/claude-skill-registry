---
name: sizing-units
description: Which CSS unit a value should be written in. rem for anything a text-size preference must move — type, control heights, padding around text. px only for what must not move — hairlines, borders, shadow offsets. Relative units for layout widths. Use when defining spacing and sizing tokens, choosing between px and rem, setting control heights, writing media queries, or fixing a layout that breaks when the user enlarges text.
metadata:
  priority: 5
  pathPatterns:
    - "design-system/**"
    - "ui/**"
    - "**/tokens*"
    - "**/*.css"
    - "**/tailwind.config.*"
    - "components/**"
    - "src/components/**"
  promptSignals:
    phrases:
      - "rem"
      - "px"
      - "em"
      - "spacing scale"
      - "sizing tokens"
      - "root font size"
      - "text zoom"
      - "which unit"
retrieval:
  aliases:
    - px vs rem
    - css units
    - spacing units
    - sizing tokens
    - root font size
    - text scaling
  intents:
    - decide between px and rem for spacing
    - define a spacing scale
    - fix a layout that breaks when text is enlarged
    - choose units for media queries
    - set control heights that survive text scaling
  examples:
    - should spacing be in rem or px
    - our buttons clip when the user enlarges text
    - what unit for border radius and shadows
    - should media queries use px or em
---

# Sizing Units

## The Question the Unit Answers

A unit is not a formatting preference. It is a declaration of what happens to a value when the user enlarges text.

- `rem` — this value belongs to the text and must grow with it.
- `px` — this value belongs to the screen and must stay put.
- `%`, `fr`, `ch`, `clamp()`, `min()` — this value belongs to the available space.

Pick the unit by answering that question, not by picking a house style and applying it everywhere. Both absolutist positions — all-rem and all-px — produce defects, and they are different defects.

## Zoom Is Not the Font-Size Setting

The common argument for px everywhere is that browsers already have full-page zoom, so the root font size can be ignored. They are separate controls serving separate people.

- **Full-page zoom** magnifies everything, layout included. It buys larger text at the cost of horizontal scrolling and fewer items per screen.
- **The browser's default font size** enlarges text and leaves the layout alone. This is what a user with low vision sets once, years ago, and never touches again. They will not switch to zoom because your product ignored it.

A product that hard-codes every dimension in px answers the first user and silently refuses the second. WCAG 2.2 SC 1.4.4 (Resize Text) requires text to reach 200% without loss of content or function, and SC 1.4.10 (Reflow) requires the page to survive it in a single column. See [[wcag-accessibility]].

## Use rem For

**Typography.** Every font size and line height. See [[modular-scale-typography]].

**Padding around text.** A button's inner padding in px means large text presses against its edges. In rem the breathing room scales with the words it surrounds.

**Control heights.** A 40px control holding 24px text is broken. Write the height token in rem and it stays a control-shaped control at every text size. See [[component-family-consistency]].

**Measure.** `max-width` on a text column: `65ch` or a rem value, never px.

**Gaps between text-bearing blocks.** Stack spacing in a form or an article is part of the reading rhythm.

## Use px For

**Hairlines and borders.** `1px` is one device pixel by intent. In rem it becomes `1.25px` at a larger root size and renders as a blurry smear.

**Shadow offsets and blur.** Elevation is a screen-space effect. See [[elevation-and-depth]].

**Small icons inside controls** where the icon is a fixed glyph rather than text.

**Sub-pixel corrections** — the `-1px` that makes two borders overlap instead of doubling.

## Use Relative Units For

Layout widths and gaps. This is where the "lock it in px so it stays stable" instinct goes wrong: a px-locked container is not stable, it is brittle. The text inside it still grows, and a fixed box is exactly what makes growing text clip.

```css
/* Brittle — the box cannot absorb anything */
.card   { width: 320px; height: 180px; }
.sidebar { width: 280px; }

/* Resilient */
.card    { max-width: 20rem; min-height: 11.25rem; }
.sidebar { width: clamp(16rem, 22%, 22rem); }
```

**`min-height`, never `height`,** on anything containing text. A fixed height cannot grow; a minimum height holds the shape at rest and yields when it must.

## Media Queries

Use `em` in media queries. Media-query `rem` and `em` both resolve against the browser's default font size, ignoring any `html { font-size }` you set — so `em` is the honest spelling, and both respect the user's preference where a px breakpoint does not. A user with a large default font size gets the layout their effective text size warrants, not the one their device width claims.

```css
@media (min-width: 48em) { /* ~768px at default settings */ }
```

## Do Not Reset the Root

```css
html { font-size: 62.5%; } /* Do not do this */
```

The 62.5% trick exists to make rem arithmetic easy — `1.6rem` for 16px. It buys you mental arithmetic and pays for it by overriding the user's stated preference by default. Keep the root at the browser default and let the tooling do the division.

## Review Checklist

- [ ] Is every font size, line height, and text-adjacent padding in rem?
- [ ] Are borders, hairlines, and shadow offsets in px?
- [ ] Does any element containing text use `height` rather than `min-height`?
- [ ] Are container widths relative (`%`, `fr`, `clamp()`, `max-width`) rather than fixed px?
- [ ] Are media-query breakpoints in `em`?
- [ ] Is `html { font-size }` left at the browser default?
- [ ] At a 200% browser font-size setting, does every control still contain its label, with no clipping and no horizontal page scroll?
