---
name: land
description: Use when the user wants knowledge delivered to an audience — slides, a deck, a diagram, an explainer for others, teaching or talk material — or shares existing content that isn't getting through.
---

# Land

Deliver information the way minds absorb it. Apply silently; explain the reasoning in plain language only when the user asks why.

## Before designing

Ask only what's missing, then confirm a 3–5 line brief (audience / goal / structure / hook) before generating:

1. **Audience** — sets language, analogies, assumed prior knowledge.
2. **The one thing** — if they keep a single memory, action, or feeling, what is it? Everything serves it.

Open with a hook that creates a curiosity gap ("You think X — actually Y"), never a topic title.

## Principles

- **One cognitive unit at a time.** One idea per slide, section, or screen. Split rather than crowd.
- **Visuals carry the information.** Acceptance test: delete every word — the meaning must survive. Text is a label, not the explanation. Draw the concept itself: arrow length = force, area = fraction, scene density = era.
- **Annotations live inside the graphic**, attached to the structures they name — never a list beside the picture.
- **Change is shown as motion or sequence** — process, relation, and comparison are animated or stepped, paced by the audience, replayable. Nothing autoplays.

## Knowledge type → representation

| The content is... | Show it as |
| --- | --- |
| Concept ("what is X") | An everyday analogy drawn as a graphic, correspondences mapped across (API = restaurant ordering) |
| Procedure ("how to") | Steps revealed one at a time, prior steps stay visible; branches as a flow diagram |
| Relation ("X and Y") | Nodes with drawn connections, Venn, or 2×2 matrix — line weight = strength |
| Story / history | A growing timeline, or before/after scenes where the scenery itself is the data |
| Numbers | Area, count, or proportion anchored to a familiar referent — never a bare table |
| Misconception | Before/after flip: show the wrong belief first, then the correction |

## Defaults — the user's call, not yours

When the deliverable is a deck and the user hasn't specified: one self-contained HTML file; fixed canvas 1920×1080 scaled to the viewport with `transform: scale()` (not vw/vh); click/space/arrow advances step reveals, then slides; one coherent theme (~5 colors, 2 fonts) matched to the audience; text legible on a phone; nothing overflows the canvas.

## Never

- Bullet-point lists as the design — every list becomes a layout, diagram, or step reveal.
- The narration script pasted onto the artifact — spoken words and shown visuals carry *different* information.
- Decorative icons or illustrations beside text — if deleting the graphic loses nothing, it failed the acceptance test.
- Dark-gradient-plus-white-text "AI deck" aesthetic.
- Infinite loops or `setInterval` animation bugs.
