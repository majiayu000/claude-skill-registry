---
name: text-animation
description: "Dependency-free kinetic typography: roll/slot text, reveals, typewriter, crossfade."
agent: typescript-frontend-engineer
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - text animation
    - kinetic typography
    - slot machine text
    - animated headline
    - rolling label
    - rolling counter
  pairs_with:
    - html-artifact
    - distinctive-frontend-design
  complexity: Medium
  category: frontend
---

# Text Animation Skill

## Overview

Animates text in HTML artifacts with zero runtime dependencies: per-character roll/slot transitions, split-letter reveals, typewriter, and crossfade swaps. Every pattern is vanilla JS + CSS, copied inline into the artifact and adapted to its content.

## Iron Rule: Zero npm

No npm packages, no CDN scripts, no build step, no external assets, ever. Every animation ships as inline `<style>` and `<script>` in the artifact itself. If a request seems to need a library (GSAP, anime.js, Framer Motion), use the reference patterns instead — they cover the same effect class.

## html-artifact Contract Compliance

Output embedded in an artifact must satisfy the html-artifact contract:

- Single self-contained `.html` file.
- All CSS inline in `<style>`, all JS inline in `<script>`.
- ≤500KB total file size.
- No CDN links, no external fonts, no remote assets.
- Respect `prefers-reduced-motion`: collapse durations to 0 when set.

## Workflow

1. **Classify the request.** Roll/slot transition between strings → `references/roll-text.md`. Entrance reveal, typewriter, or content swap → `references/text-animation-patterns.md`. Load only the matching reference.
2. **Copy the pattern inline.** Lift the CSS and JS from the reference into the artifact's `<style>`/`<script>`. Rename hooks to match the artifact's naming.
3. **Tune the knobs.** Duration, stagger, easing, direction — each reference documents its knobs. Match the artifact's motion language (see distinctive-frontend-design when active).
4. **Verify.** Open the file standalone; animation runs offline with no console errors.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| roll, slot, slot machine, retargeting label, rolling counter, string-to-string transition | `references/roll-text.md` | Complete roll-text demo plus extraction guide and knobs (duration, stagger, easing, direction) |
| reveal, entrance, typewriter, terminal effect, crossfade, swap text | `references/text-animation-patterns.md` | Split-letter reveal, typewriter, and crossfade swap snippets with usage notes |

## Error Handling

### Animation does not run when the page opens
Cause: transition start and end states applied in the same style flush; the browser batches them.
Solution: force a reflow (`void el.offsetHeight`) between setting the start state and the end state, as the reference patterns do.

### Characters jump width mid-animation
Cause: variable-width glyphs swapped without animating the cell width.
Solution: use the roll-text pattern's measured-width transition; it animates each cell from old-glyph width to new-glyph width.

## Reference Files

- `references/roll-text.md`: roll/slot pattern — standalone runnable demo, extraction guide, knob table
- `references/text-animation-patterns.md`: companion patterns — split-letter reveal, typewriter, crossfade swap
