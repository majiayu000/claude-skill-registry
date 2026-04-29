---
name: design
description: 'Set visual and interaction direction for any UI surface — web, React, TUI, CLI, desktop (Tauri/Slint/egui/Iced), Qt, or design-system tokens — before any UI code. Direction-first: generates 3-4 radically distinct directions in parallel via verbalized sampling, picks one via per-axis single-select, then derives palette, typography, spacing, and motion budget from the pick. Loads when the user asks for UI work, a palette / theme / tokens, mentions a design system, or when output looks AI-generic, vibe-coded, sloppy, or default Tailwind / shadcn / Bootstrap. Enforces a two-sided anti-slop charter: forbids purple gradients, `transition: all`, system-ui, default Tailwind palette, gradients on buttons — AND overkill compensation (sprites, gradients on every section, animation on every element).'
---

Direction first, tokens second, code last. Restraint is the default posture; ONE intentional moment per surface earns the lift.

## Posture

Direction precedes tokens; tokens precede code. The picked direction is the contract — palette, type, spacing, motion all derive from it, not the other way around. Restraint is the default; reach for decoration only when a named surface goal demands it. Posture rests on `references/soul.md` (design philosophy) — load when the user asks "why this look" or when the model is tempted to add decoration to compensate for a thin idea.

**Balance, not maximalism.** ODIN's "don't hold back" (borrowed from the `<design>` block above) means conviction, not volume. The two failure modes catalogued in the anti-slop charter below are reciprocals — AI-generic timidity (Side A) and decorative overkill (Side B) both come from the same fear of commitment. Balance simplicity and verbosity per surface; restraint as the default, the one intentional moment as the lift, neither timid nor loud.

## ODIN `<design>` block — LOAD-BEARING

Quoted verbatim from `output-styles/odin.md` lines 254–262.

```
<design>
Modern, elegant UI/UX. Don't hold back.

**Tokens:** MUST use design system tokens, not hardcoded values.
**Density:** 2-3x denser. Spacing: 4/8/12/16/24/32/48/64px. Medium-high density default. Ask preference when ambiguous.
**Paradigms:** Post-minimalism [default] | Neo-brutalism | Glassmorphism | Material 3 | Fluent. Avoid naive minimalism.
**Forbidden:** Purple-blue/purple-pink | `transition: all` | `font-family: system-ui` | Pure purple/red/blue/green | Self-generated palettes | Gradients (unless explicitly requested, NEVER on buttons/titles)
**Gate:** Design excellence >= 95%
</design>
```

## Register × paradigm matrix — pointer

Brand register opens neo-brutalism / glassmorphism / M3 Expressive with Committed / Full palette / Drenched color strategies; product register defaults to Restrained + post-minimalism / Fluent 2. Full matrix in `references/paradigms.md §0`.

## Anti-slop charter — LOAD-BEARING

Two-sided ban-list. Each row: ban — WHY in one line. Depth in `references/anti-slop.md`.

**Side A — slop tells (the AI-generic look):**

- Purple-blue or purple-pink gradient — RLHF over-aligns to this; betrays self-generated palette.
- Inter alone as the type system — default of every Vercel template; no commitment, no contrast.
- Centered hero plus 3-column feature grid — the shadcn landing-page silhouette; reads as preset.
- Glassmorphism on every surface — translucence loses meaning when nothing is opaque.
- `rounded-lg` uniform on every element — radius without hierarchy is decoration, not signal.
- `shadow-md` uniform across the surface — elevation that conveys nothing.
- `transition: all` — animates layout, color, and transform together; jank guaranteed.
- `font-family: system-ui` — abdicates the type decision; reads as "did not pick".
- Default Tailwind palette (slate-500 / blue-500) — the costume of "I used the framework defaults".
- Colored card borders to assert structure — borders are not the right tool for hierarchy.
- Emoji icons in production UI — accessibility hostile; locale-fragile; reads as draft.

**Side B — overkill compensation (slop's louder cousin):**

- Sprites on every empty pixel — decoration substituting for missing information density.
- Gradient on every section background — every section "important" means none are.
- Animation on every element entrance — motion budget is a budget; spend it once.
- Multi-paradigm mash (neo-brutalism shadow on a glass card on a Material 3 button) — paradigm conflict reads as confusion, not eclecticism.
- Decorative noise compensating for a thin idea — when the surface earns its weight, restraint amplifies it.

**Color strategy axis (commitment level).** Pick the strategy before picking colors. Each tier is deliberate, not a fallback.

- **Restrained** — tinted neutrals plus one accent at ≤10% surface coverage. Product default.
- **Committed** — one saturated color carries 30–60% of the surface. Brand default for identity-driven pages.
- **Full palette** — 3-4 named roles, each used deliberately. Brand campaigns; product data viz.
- **Drenched** — the surface IS the color. Brand heroes, campaign pages.

The "one accent ≤10%" cap applies only to **Restrained**. Committed / Full palette / Drenched exceed it on purpose; treat the cap as direction-conditional, not universal.

## Direction-first workflow

Six steps. Do not skip the divergence step.

1. **Frame the surface.** Capture: surface (landing / dashboard / settings / docs / one-screen tool), primary user, density target, motion budget in ms. **Then write one sentence of physical scene** (who, where, ambient light, mood) that FORCES the dark/light decision. Category names alone do not force the answer — "observability dashboard" fails; "SRE glancing at incident severity on a 27-inch monitor at 2am in a dim room" succeeds. Consult `references/soul.md` for the philosophical anchor — *why* this design must feel a certain way before deciding *how*. Surface answers before generating directions; designing on assumed callers wastes the parallel budget.

2. **Diverge: 3-4 directions in parallel via Verbalized Sampling.** Delegate the parallel-generation pattern from `odin:design-an-interface` — dispatch one Explore agent per direction with a constraint that *forces* contrast (post-minimalism vs neo-brutalism vs Material 3 vs Fluent, or named taste anchors that pull in opposite directions). Reject converged outputs; re-dispatch with sharpened constraints if two directions read alike.

3. **Per direction, return a fixed shape.** Each direction states: name (one or two words), 1-2 taste anchors (Linear / Stripe / Things 3 / Rosé Pine / Are.na — name the references), OKLCH palette stub (4-6 swatches, never the default Tailwind ramp), type pair (display + text, named families), spacing scale subset committed (e.g., 4/8/16/24/48), motion budget in ms with one easing curve.

4. **Pick via `odin:askme` exhaustive — per-axis single-select.** Each axis (direction, density, motion budget, type pair) is its own single-select question; the recommended option carries `(Recommended)` and is placed first. Ticking `(Recommended)` *is* accepting the default. Never use `multiSelect` for axis-with-default override semantics — that shape collapses N independent decisions into one ambiguous checklist; reserve `multiSelect` for additive picks only (feature toggles, optional sub-tasks).

5. **Derive DTCG-shaped tokens from the picked direction.** Color, type, space, radius, shadow, motion — each a token, each referenced not hardcoded. Tokens precede component code; component code references tokens.

6. **Route to the surface reference.** Pick the row in §6 that matches the runtime; load that reference for surface-specific patterns and pitfalls.

## Surface routing

| Runtime | Reference |
|---|---|
| Vanilla CSS / static HTML | `references/web.md` |
| React / Tailwind / shadcn | `references/react.md` |
| Bubble Tea / Ratatui / Textual | `references/tui.md` |
| clap / cobra / cmdliner / typer | `references/cli.md` |
| Tauri / Slint / egui / Iced | `references/desktop.md` |
| Qt / QML | `references/qt.md` |
| Cross-platform tokens | `references/design-systems.md` |
| Motion across runtimes (timing / easing / reduced motion) | `references/motion.md` |

## Cross-surface invariants

- **Color as input, never as default.** Custom OKLCH palette derived from the picked direction; never the default Tailwind, Material, or Bootstrap ramp.
- **Spacing scale is 4/8/12/16/24/32/48/64.** Pick a subset that matches density target; commit and stick. A new value mid-build is a smell.
- **At most two type families.** Display plus text. A third family is a smell unless the direction explicitly demands it (e.g., a mono accent for code).
- **Motion is budgeted in milliseconds.** One easing curve per surface. `transition: all` is forbidden — name the properties (`transition: opacity 120ms ease, transform 120ms ease`) so layout and paint do not animate together.
- **Semantic structure precedes class names.** `<nav>` / `<main>` / `<article>` first; utility classes second. Class soup over weak structure is slop.
- **Contrast: WCAG 2.1 AA is the legal floor.** APCA is a *design-input* tool only — it was REMOVED from WCAG 3 in July 2023 and never reinstated. Do not claim "WCAG 3 compliant via APCA"; that compliance does not exist. Verify AA with axe-core or the browser DevTools accessibility panel.

## Integration hooks

- `odin:askme` (exhaustive) — per-axis single-select for direction commitment; one tool call, ≤4 questions, `(Recommended)` first.
- `odin:design-an-interface` — the parallel-generation pattern lifted for direction divergence; same constraint-forced contrast, different artifact.
- `odin:plan` / `odin:proceed` / `odin:contexts` — orchestration when the design work spans multiple files or phases.
- `odin:write-a-skill` — when a downstream component skill is needed (e.g., a chart-component skill), author it with the same SKILL.md contract.

## Verification gate

1. ODIN design gate ≥95% per the `<design>` block above (tokens / density / paradigm / forbidden list).
2. Anti-slop checklist (§4 Side A AND Side B) returns zero violations.
3. Direction artifact recorded in commit body or PR description: name plus taste anchors plus one-line rationale.
4. Tokens referenced not hardcoded — `git grep` for raw hex, raw px values in component code; should be empty.
5. Cross-surface invariants honored — spacing subset committed, ≤2 type families, motion named-properties only.
6. Contrast verified via axe-core CLI or DevTools accessibility panel; WCAG 2.1 AA pass on every text surface.

## Anti-patterns

- "Be creative" / temperature-up — generates more slop, not better direction. VS structure or nothing.
- Single-shot palette generation — RLHF over-aligns to purple; the model's first guess is the slop.
- Skipping the direction commit and jumping to component code — components without a direction are coupling without contract.
- Mixing two paradigms on one surface — neo-brutalism shadow on a glass card reads as confusion.
- Ranking directions by implementation effort — short-term cost is the wrong axis; taste fit and depth are the right ones.

## Adjacent skills disambiguation

- `design-an-interface` — module / API contract shape; not visual direction. Lift its parallel-generation pattern, not its scope.
- `design-by-contract` — Eiffel-style pre/post conditions on functions; unrelated to UI.
- `web-design-skills:web-design-engineer` and `ui-ux-pro-max:ui-ux-pro-max` — installed but bloated and preset-heavy; `odin:design` chooses restraint and direction over presets.
