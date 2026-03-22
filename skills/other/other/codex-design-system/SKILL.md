---
name: codex-design-system
description: Modern design vocabulary with palettes, typography, layouts, animations, and composition principles. Prevents generic output and injects professional-grade aesthetics.
load_priority: on-demand
---

## TL;DR
Load before any UI/frontend task. This skill brings 30 palettes, 21 free font pairings, 20 layout patterns, 15 micro-interactions, composition rules, current trends, and developer-UI anti-pattern fixes. Anti-generic rules: no default blue, no plain white card stacks, no bootstrap look.

## Activation
1. Activate when task involves UI, frontend, styling, component work, or landing-page creation.
2. Activate on `$design` or "make it look premium/modern/creative".
3. Auto-load when `frontend-specialist` agent is active.

## Anti-Generic Rules (HARD)
- NEVER use default blue (`#007bff`, `#2196F3`, `#3B82F6`) or default purple (`#6C63FF`, `#7C3AED`) unless the chosen palette in `references/palettes.md` explicitly uses it.
- NEVER ship plain white cards with `border-radius: 8px` and `box-shadow: 0 2px 4px rgba(0,0,0,0.1)`.
- NEVER use system fonts or unnamed "sans-serif"; specify exact font families and fallbacks.
- NEVER build a fully symmetrical layout without hierarchy through size, spacing, color, or motion.
- ALWAYS choose a palette from `references/palettes.md` before writing UI code.
- ALWAYS choose a font pair from `references/typography.md`.
- ALWAYS apply at least one composition principle from `references/composition.md`.
- ALWAYS add at least two micro-interactions from `references/micro-interactions.md`.

## Design Decision Flow
1. Decide the mood: premium, bold, calm, editorial, playful, technical, or luxury.
2. Pick one palette from `references/palettes.md`.
3. Pick one font pair from `references/typography.md`.
4. Pick one or two layout patterns from `references/patterns.md`.
5. Pick two or three micro-interactions from `references/micro-interactions.md`.
6. Check `references/anti-patterns.md` before finalizing.
7. Then write UI code with explicit values for color, type, spacing, radius, and shadow.

## Reference Files
- `references/palettes.md` — 30 curated palettes with exact hex tokens, mood, app fit, and contrast ratios.
- `references/typography.md` — 21 free font pairings with imports, weights, style tags, and fallback stacks.
- `references/patterns.md` — 20 layout patterns with structure, responsive CSS, and usage boundaries.
- `references/micro-interactions.md` — 15 production-ready motion patterns with CSS or JS code.
- `references/composition.md` — Visual hierarchy, spacing, grids, storytelling flow, and emphasis rules.
- `references/trends.md` — Current design trends for 2025-2026 with code signatures and fit guidance.
- `references/anti-patterns.md` — 15 developer-UI mistakes with wrong/right code and violated principles.
