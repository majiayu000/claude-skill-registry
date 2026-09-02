---
name: design
description: 'Use when starting UI work, defining palettes or design tokens, or fixing AI-generic, vibe-coded, or default-framework UI. Also handles TUI, CLI, and desktop surfaces when the runtime is named. Not for persisted design systems; use design-consultation. Not for live-URL audits; use web-design-review. No irreversible changes.'
---

# Design

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Starting UI work, defining palettes or design tokens, or correcting AI-generic, vibe-coded, or default-framework design. |
| Authority | Reversible local: creates or revises local UI direction, token, and implementation artifacts appropriate to the chosen runtime. Roll back by reverting the touched files. |
| Side effect | Local write to UI direction, token, and implementation artifacts only. No VCS, credential, paid, published, deployed, or remote mutation. |
| Done | One defensible direction is implemented consistently across palette, typography, spacing, density, and motion; runtime and cross-surface checks pass without AI-generic or compensatory overkill tells. |

## Inputs

- The surface being designed (landing, dashboard, settings, docs, one-screen tool, TUI, CLI, desktop app). Required.
- The runtime or framework in use (vanilla CSS/HTML, React/Tailwind/shadcn, Bubble Tea/Ratatui/Textual, clap/cobra/cmdliner/typer, Tauri/Slint/egui/Iced, Qt/QML). Required before implementation.
- Primary user and density target. Required for framing; state assumptions if not supplied.
- Existing project context (PRD, brand brief, design tokens, component library). Optional; load when present.

## Procedure

Direction precedes tokens; tokens precede code. The picked direction is the contract. Restraint is the default; reach for decoration only when a named surface goal demands it. Balance, not maximalism, not minimalism.

1. **Frame the surface.** Identify register first: **brand** (marketing, landing, campaign, long-form, portfolio; design IS the product) or **product** (app UI, admin, dashboard, tool; design SERVES the product). Detection rule, first match wins: (a) cue in the task ("landing page" / "campaign hero" → brand; "dashboard" / "settings panel" → product); (b) surface in focus or route segment (`/marketing/*` vs `/app/*`); (c) register field in project context. Then capture surface, primary user, density target, and motion budget in ms. Write one sentence of physical scene (who, where, ambient light, mood) that forces the dark/light decision; category names alone do not force the answer. **Done when:** register is named, the four framing fields are captured, and the dark/light sentence is written.

2. **Diverge: 3-4 directions in parallel with forced contrast.** Dispatch one exploration per direction with a constraint that forces contrast (post-minimalism vs neo-brutalism vs Material 3 vs Fluent, or named taste anchors pulling in opposite directions). Reject converged outputs; re-dispatch with sharpened constraints if two directions read alike. Diversity techniques: verbalized sampling, actor-critic per candidate, persona injection, temperature, most-unlikely reframing, anti-pattern catalog. **Done when:** 3-4 directions are produced and no two read alike under a headline-swap test.

3. **Return a fixed shape per direction.** Each direction states: name (one or two words), 1-2 taste anchors (Linear / Stripe / Things 3 / Rosé Pine / Are.na; name the references), OKLCH palette stub (4-6 swatches, never the default Tailwind ramp), type pair (display + text, named families), spacing scale subset committed (e.g. 4/8/16/24/48), motion budget in ms with one easing curve. **Done when:** every direction carries all six fields with no defaults borrowed from a framework ramp.

4. **Pick via per-axis single-select.** Each axis (direction, density, motion budget, type pair) is its own single-select question; the recommended option carries `(Recommended)` and is placed first. Ticking `(Recommended)` is accepting the default. Never use multiSelect for axis-with-default override semantics: it collapses N independent decisions into one ambiguous checklist. Reserve multiSelect for additive picks only. **Done when:** one option is selected per axis and the picked direction is named.

5. **Derive tokens from the picked direction.** Color, type, space, radius, shadow, motion: each a token, each referenced, not hardcoded. Pick the color strategy before picking colors: **Restrained** (tinted neutrals plus one accent at ≤10% surface coverage; product default), **Committed** (one saturated color carries 30-60% of the surface; brand default for identity pages), **Full palette** (3-4 named roles, each deliberate; brand campaigns, product data viz), **Drenched** (the surface IS the color; brand heroes, campaign pages). The ≤10% accent cap applies only to Restrained. Express tokens in the runtime's native token system: CSS custom properties for web, theme or design-token objects for React, style structs for TUI and desktop, palette constants for CLI. Tokens precede component code; component code references tokens. **Done when:** the six token families are expressed in the runtime's native system and referenced, not hardcoded.

6. **Implement against the runtime.** Apply the cross-surface invariants regardless of runtime. Audit the result against the anti-slop charter. **Done when:** implementation references the committed tokens and the audit flags no Side A or Side B tell and no invariant violation.

Cross-surface invariants (apply on every runtime):

- Color as input, never as default: custom OKLCH palette derived from the picked direction; never the default Tailwind, Material, or Bootstrap ramp.
- Spacing scale is 4/8/12/16/24/32/48/64. Pick a subset matching the density target; commit and stick. A new value mid-build is a smell.
- At most two type families: display plus text. A third is a smell unless the direction explicitly demands it (e.g. a mono accent for code).
- Motion is budgeted in milliseconds. One easing curve per surface. `transition: all` is forbidden. Name the properties (`transition: opacity 120ms ease, transform 120ms ease`) so layout and paint do not animate together.
- Semantic structure precedes class names: `<nav>` / `<main>` / `<article>` first; utility classes second. Class soup over weak structure is slop.

Anti-slop charter (audit both sides):

Side A: slop tells (the AI-generic look):

- Purple-blue or purple-pink gradient: RLHF over-aligns to this; betrays self-generated palette.
- Inter alone as the type system: default of every template; no commitment, no contrast.
- Centered hero plus 3-column feature grid: the landing-page silhouette; reads as preset.
- Glassmorphism on every surface: translucence loses meaning when nothing is opaque.
- `rounded-lg` uniform on every element: radius without hierarchy is decoration, not signal.
- `shadow-md` uniform across the surface: elevation that conveys nothing.
- `transition: all`: animates layout, color, and transform together; jank guaranteed.
- `font-family: system-ui`: abdicates the type decision; reads as "did not pick".
- Default Tailwind palette (slate-500 / blue-500): the costume of "I used the framework defaults".
- Colored card borders to assert structure: borders are not the right tool for hierarchy.
- Emoji icons in production UI: accessibility hostile; locale-fragile; reads as draft.

Side B: overkill compensation (slop's louder cousin):

- Sprites on every empty pixel: decoration substituting for missing information density.
- Gradient on every section background: every section "important" means none are.
- Animation on every element entrance: motion budget is a budget; spend it once.
- Multi-paradigm mash (neo-brutalism shadow on a glass card on a Material 3 button): paradigm conflict reads as confusion, not eclecticism.
- Decorative noise compensating for a thin idea: when the surface earns its weight, restraint amplifies it.

## Failure and recovery
- Converged directions: if two or more directions read alike, do not pick from a thin field. Re-dispatch with sharpened, opposing constraints until contrast is real.
- Missing runtime: if the runtime is not identified before step 5, stop and ask; do not implement against an assumed runtime.
- Token drift mid-build: a new spacing value, third type family, or hardcoded color appearing mid-build is a smell. Revert to the committed token set; do not patch around it.
- Audit failure: if the result triggers any Side A or Side B tell, or violates a cross-surface invariant, the done predicate does not hold. Fix the tell at its source; do not compensate with more decoration.
- Partial result: never present an unaudited or half-implemented direction as done. State which steps are complete and which remain.

## Output
One picked direction plus a committed token set (color, type, space, radius, shadow, motion) in the runtime's native token system and implementation artifacts that reference those tokens, ordered frame → direction → tokens → implementation, passing the anti-slop charter and cross-surface invariants.
