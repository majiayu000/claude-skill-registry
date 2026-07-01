---
name: repeated-component-alignment
description: Any component rendered many times — cards, list rows, table cells, nav items, tiles, KPI widgets, feed entries — is a fixed slot model, not a free-form box. The same slots appear in the same place in every instance and stay aligned across siblings even when text and values vary in length. Reserve space for optional slots, pin anchor elements (CTA, price, value), clamp overflowing text, and give the full value back via title/tooltip. Use when building or reviewing any repeated component whose content length differs between instances.
metadata:
  priority: 8
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.vue"
    - "**/*.svelte"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "card"
      - "list item"
      - "repeated component"
      - "equal height"
      - "same place"
      - "aligned"
      - "read more"
      - "truncate"
      - "ellipsis"
      - "line clamp"
      - "different lengths"
      - "tile"
retrieval:
  aliases:
    - repeated component consistency
    - slot model
    - equal height cards
    - aligned list items
    - card alignment
    - truncate text
    - line clamp
    - ellipsis
    - read more link position
  intents:
    - keep elements in the same place across repeated components
    - make cards or list items the same height
    - align CTAs and values across instances
    - handle long and short text in a repeated component
    - truncate overflowing text but keep it readable
  examples:
    - my cards look different because the descriptions have different lengths
    - keep the read more link in the same place on every card
    - the badge pushes the title down on some items
    - align the prices across all the tiles
    - truncate long titles but keep them readable
---

# Repeated Component Alignment

When a component is rendered many times — a card grid, a list, a table, a nav menu, a row of KPI tiles, a feed — it stops being a single box and becomes a **pattern**. The value of a pattern is rhythm: the eye learns the layout once and scans the same slot across every instance (the title row, the price row, the action row). Variable content length breaks that rhythm unless the component is built to absorb it.

The principle is general. A **card** is the most common case, but the same rule governs list rows, table cells, nav items, tiles, comment entries, dashboard widgets, search results — anything repeated. Treat each as a **fixed slot model**, not a free-form container.

The goal: **content of any length, instances that look identical.** This is partly content production (write to a target length) and partly layout engineering (build slots that tolerate the variance). This skill covers the layout half and where the two meet.

---

## The Slot Model

Name the slots once and treat them as a contract every instance honours. A product card, as a worked example:

```
┌──────────────────────┐
│ [media]              │  ← fixed aspect ratio
│                      │
├──────────────────────┤
│ ● Badge              │  ← optional slot, space reserved
│ Title                │  ← clamp to N lines
│ Subtitle / meta      │
│                      │
│ Description text…    │  ← flexible slot, grows
│                      │
├──────────────────────┤
│ €19.99      Read more│  ← anchor, pinned to bottom
└──────────────────────┘
```

The same three rules apply to a **list row** (avatar · name · meta · status pinned right), a **KPI tile** (label · big number · trend pinned bottom), or a **search result** (title · url · snippet clamped):

- **Every slot has a fixed position**, whether or not it has content in a given instance.
- **One slot absorbs the variance** (usually the description/snippet). All others are fixed or clamped.
- **Anchor elements are pinned** — the primary action or value (CTA, price, status, trend) sits at the same position in every instance regardless of how much content is above or beside it.

---

## Aligning the Anchor

The single most common defect: text of different lengths makes the anchor element (a "Read more" link, a price, a status chip) float to a different position in each instance. Fix it by letting the flexible slot grow and pushing the anchor to a fixed edge.

**Vertical layout (cards, tiles) — pin the footer to the bottom:**

```css
.item {
  display: flex;
  flex-direction: column;
  height: 100%;            /* fill the grid/flex track */
}

.item__media {
  aspect-ratio: 4 / 3;     /* never let media height vary */
  object-fit: cover;
}

.item__description {
  flex: 1;                 /* the flexible slot absorbs the slack */
}

.item__footer {
  margin-top: auto;        /* pin the anchor (price + CTA) to the bottom */
}
```

For instances to be **equal height as siblings**, the container track must stretch them — CSS Grid and Flex do this by default (`align-items: stretch`). Then `height: 100%` makes each instance fill its track, and `margin-top: auto` aligns every footer.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-4);
  /* align-items: stretch is the default — do not override it */
}
```

**Horizontal layout (list rows, table cells) — pin the anchor to the right:**

```css
.row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.row__title {
  flex: 1;                 /* title absorbs the width variance */
  min-width: 0;            /* REQUIRED for the title to be allowed to shrink/ellipsis */
}
.row__status {
  margin-left: auto;       /* status pinned to the right edge */
}
```

Do **not** force equal size with a hard-coded `height` — the tallest natural instance sets the size, and content beyond it clips or overflows. Let the track stretch and pin the anchor.

---

## Reserve Space for Optional Slots

A slot that appears in some instances and not others — a badge, a discount label, a "verified" tick — shifts everything after it on the instances that have it, breaking alignment. Two fixes:

1. **Reserve the slot** — always render the container at a fixed size, empty when there is no content:

```css
.item__badge-row {
  min-height: 24px;        /* always occupies the row */
}
```

2. **Overlay the slot** — position it absolutely so it never participates in the flow:

```css
.item__badge {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
}
```

Reserve when the element is inline metadata; overlay when it is a marker on media (Sale, New). Either way, the slot after it must start at the same position in every instance.

---

## Clamp Overflowing Text — and Give the Full Value Back

When a slot must be fixed-size but its content varies, clamp it to a line count and signal the cut with an ellipsis. This keeps the geometry stable. **But truncation hides information — always make the full value recoverable.**

**Multi-line text — clamp to N lines:**

```css
.clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

**Single-line values (names, SKUs, paths) — ellipsis:**

```css
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;            /* needed inside a flex row to allow shrinking */
}
```

**Recover the full value.** A clamped or ellipsised string is a usability trap if the full text is unreachable. Provide it:

- **Native tooltip** for plain text: `<span title="Full value here">…</span>`. Zero cost, works everywhere, but hover-only (not touch) and unstyled.
- **Custom tooltip** when you need touch support, styling, or rich content.
- **Reveal in place** when the full content is the point — a "Read more" toggle that expands the instance or opens a detail view, rather than permanently hiding text the user needs.

> Only attach a tooltip when text is *actually* truncated — a `title` on a string that fits adds a redundant hover. Detect overflow (`scrollWidth > clientWidth`) and set `title` conditionally.

**The hierarchy of handling variable length:**

1. **Write to length** — the cleanest fix. Give content authors a target (e.g. titles ≤ 60 chars, snippets ≤ 120) so most values never need truncating. Layout tricks are a safety net, not the primary plan.
2. **Clamp + recover** — when authored length cannot be guaranteed (user-generated, third-party feeds, i18n expansion).
3. **Let one slot grow** — for the single slot allowed to vary, absorb the variance with flex rather than truncating, and pin everything after it.

---

## Internationalisation Note

Text expands when translated — German and Finnish commonly run 30–40% longer than English. A component that aligns perfectly in English can break in another locale. Design slots for the long case: clamp text, reserve optional slots, give flex rows `min-width: 0`, and never assume a label fits on one line because it does in the source language.

---

## Review Checklist

- [ ] Is the repeated component a defined slot model — every instance fills the same slots in the same order?
- [ ] Are sibling instances equal size via a stretched grid/flex track, not a hard-coded height?
- [ ] Is the anchor (CTA / price / status / value) pinned — `margin-top: auto` for columns, `margin-left: auto` for rows — so it aligns across instances?
- [ ] Does exactly one slot absorb length variance, with the rest fixed or clamped?
- [ ] Do optional slots (badge, label) reserve space or overlay, so they never shift the slots after them?
- [ ] Does media use a fixed `aspect-ratio` so its size never varies?
- [ ] Are multi-line slots clamped to a line count and single-line values ellipsised?
- [ ] Do flex rows that truncate have `min-width: 0` so the text is allowed to shrink?
- [ ] Is the full value recoverable (title/tooltip/reveal) wherever text is truncated?
- [ ] Is the tooltip applied only when the text actually overflows?
- [ ] Do content authors have target lengths, so truncation is a safety net rather than the norm?
- [ ] Have slots been checked against the longest-translating locale, not just the source language?
