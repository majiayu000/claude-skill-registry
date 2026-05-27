---
name: conductor-motion
description: "Generate hand-crafted web animation patterns as self-contained HTML: typewriter/rotator effects, progress bar simulations, file review state machines, staggered reveals, terminal status displays, Lottie orchestration, scroll-driven sequences. Behavioral animations that simulate live software. Triggers on typewriter effect, progress animation, stagger reveal, terminal animation, data simulation, product demo animation, loading sequence, conductor motion."
argument-hint: "[--mode typewriter|progress|file-review|stagger-reveal|terminal|lottie-compose|full-page|catalog] [--pacing slow|medium|fast] [content args]"
---

# Conductor Motion

Generate the mid-layer animation patterns that make product marketing sites feel alive — typewriter simulations, progress bar choreography, staggered content reveals, Lottie sequencing, and scroll-driven animation compositions. These patterns simulate live software through animation alone.

Deconstructed from [ConductorAI.com](https://www.conductorai.com/) (Webflow, GSAP 3.15, Lottie, vanilla JS).

## Quick Start

```bash
# Typewriter hero with word cycling
python3 scripts/conductor_motion_generator.py --mode typewriter \
  --base-text "Accelerating" \
  --words "complex approvals,investigations,e-discovery,FOIA review" \
  --output typewriter.html

# Progress bar simulation
python3 scripts/conductor_motion_generator.py --mode progress \
  --title "search initialization" --doc-count 1324 \
  --rows "QUERY_RECEIVED,INPUT,ELECTRONIC SIGNATURE,JURISDICTION" \
  --output progress.html

# File review state machine
python3 scripts/conductor_motion_generator.py --mode file-review \
  --files "Report_Q4.xlsx,Contract_Draft.pdf,Audit_Log.csv" \
  --output file-review.html

# Full landing page with all patterns
python3 scripts/conductor_motion_generator.py --mode full-page \
  --output landing.html

# Effects catalog (all modes demonstrated)
python3 scripts/conductor_motion_generator.py --mode catalog --output catalog.html
```

Or let Claude generate directly from the templates and references.

## Motion Interview

When invoked without `--mode`, the skill runs a brief motion interview:

1. **Content type** — What are you animating? (hero section, product demo, status dashboard, landing page)
2. **Pacing** — What tempo? (slow/deliberate, medium/professional, fast/urgent)
3. **Patterns** — Which effects? (typewriter, progress, file-review, stagger, terminal, lottie, or all)
4. **Color scheme** — Dark or light background?
5. **Design tokens** — Use existing `DESIGN.md` / `.design-context.md`, or defaults?

Output: `.motion-context.md` consumed by generation phase.

If `.design-context.md` exists with MOTION_INTENSITY dial set, skip the pacing question and derive from that value:
- MOTION_INTENSITY 1-3 → slow
- MOTION_INTENSITY 4-6 → medium
- MOTION_INTENSITY 7-10 → fast

## Modes

| Mode | Template | Patterns Composed |
|------|----------|-------------------|
| `typewriter` | `assets/templates/typewriter.html` | Hero rotator + type-on + blinking cursor |
| `progress` | `assets/templates/progress.html` | Progress bar + counter + dot-leaders + processing dots + staggered rows |
| `file-review` | `assets/templates/file-review.html` | File list + state machine (unreviewed→processing→reviewed) + status indicators |
| `stagger-reveal` | `assets/templates/stagger-reveal.html` | Hero cascade + section reveals + IntersectionObserver scroll triggers |
| `terminal` | `assets/templates/terminal.html` | Timestamps + status typing + search result counters + progress sync |
| `lottie-compose` | `assets/templates/lottie-compose.html` | Lottie player + responsive variants + scroll-synced playback |
| `full-page` | `assets/templates/full-page.html` | All patterns composed into a coherent landing section |
| `catalog` | `assets/templates/catalog.html` | Visual reference with live demos of each pattern |

## Color System

All effects read from `--cm-*` CSS custom properties. Override at `:root` to re-theme. Default: dark scheme with `#4F7BF7` brand accent. Light scheme swaps bg/text polarity.

Full token reference (dark, light, easing, timing): `references/design-tokens.md`

## Composition Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `--pacing` | `slow \| medium \| fast` | `medium` | Speed multiplier: slow=1.5x duration, fast=0.6x |
| `--stagger` | `100–400` | `200` | Milliseconds between sequential reveals |
| `--typing-speed` | `20–80` | `45` | Base ms per character typed |
| `--typing-variance` | `0–40` | `18` | Random variance added to typing speed |
| `--easing` | `cubic \| quart \| linear` | `cubic` | Primary easing: easeOutCubic, easeOutQuart, or linear |
| `--progress-duration` | `2000–10000` | `6000` | Total progress animation ms |
| `--hold-duration` | `500–3000` | `1100` | Ms to hold typed word before deleting |
| `--color-scheme` | `dark \| light` | `dark` | Background/foreground polarity |
| `--font` | font name | `Geist` | Primary font (loaded via Google Fonts CDN) |
| `--accent` | hex color | `#4F7BF7` | Override `--cm-brand` |
| `--lottie-cdn` | `boolean` | `false` | Include Lottie player CDN (lottie-compose mode only) |

### Content Parameters (per mode)

**typewriter**: `--base-text`, `--words` (comma-separated), `--cursor` (char, default `|`), `--loop` (boolean)
**progress**: `--title`, `--doc-count`, `--rows` (comma-separated labels), `--start-percent` (default 5)
**file-review**: `--files` (comma-separated filenames with extensions), `--review-speed` (ms per file)
**stagger-reveal**: `--items` (comma-separated selectors or text blocks), `--direction` (up|down|left|right)
**terminal**: `--status-items` (comma-separated), `--result-count`, `--result-label`, `--timestamps` (boolean)
**lottie-compose**: `--lottie-src` (URL to .json), `--lottie-loop`, `--lottie-autoplay`, `--responsive` (boolean)

## Architecture

```
                     ┌──────────────────────┐
                     │   .design-context.md  │ ← from /shape (optional)
                     │   DESIGN.md tokens    │ ← from /design-md (optional)
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │   Motion Interview    │ ← asks pacing, patterns, content
                     │  (skip if --mode set) │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │  .motion-context.md   │ ← pacing, patterns, content data
                     └──────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                  ▼
     ┌────────────┐   ┌────────────┐    ┌────────────────┐
     │  Template   │   │   Token    │    │    Content     │
     │  Selection  │   │ Application│    │   Injection    │
     │ (mode→html) │   │ (--cm-*)   │    │ (user data)    │
     └──────┬─────┘   └─────┬──────┘    └───────┬────────┘
            │                │                    │
            └────────────────┼────────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │  Single-file HTML    │
                  │  (inline CSS + JS)   │
                  │  CDN: fonts only     │
                  │  (+ Lottie if needed)│
                  └──────────────────────┘
```

## Animation Engine Internals

Easing functions, timing constants per mode, and pacing multiplier tables: `references/design-tokens.md`

Key: `easeOutCubic` (`t => 1 - Math.pow(1-t, 3)`) is the default. Pacing multiplier scales all durations — slow=1.5×, medium=1.0×, fast=0.6×. Stagger delays scale at 0.8× the multiplier.

## Gotchas (What Claude Gets Wrong Without This Skill)

1. **Reaches for GSAP or Framer Motion.** These patterns are vanilla JS — no framework needed. GSAP adds 30KB for effects achievable with `requestAnimationFrame` and CSS transitions.
2. **Uses `transition: all` for reveals.** Triggers layout on every property. Explicitly list `opacity` and `transform` only.
3. **Forgets `prefers-reduced-motion`.** Every single effect must show its final state immediately under reduced motion. Claude skips this ~60% of the time.
4. **Uses `Date.now()` in animation loops.** Not monotonic, drifts on clock sync. Must use `performance.now()`.
5. **Hardcodes colors instead of CSS custom properties.** Makes re-theming impossible. All colors must go through `--cm-*` tokens.
6. **Leaves `will-change` on permanently.** Reserves GPU memory for the life of the element. Add before animation, remove after.
7. **Generates typing effects without a cursor.** The blinking cursor is what sells the illusion of a human typing. Without it, it looks like a broken render.
8. **Animates `width` for progress bars via JS.** CSS `transition: width` on the fill element handles this. JS should only set the target percentage.
9. **Puts stagger delays in JS `setTimeout` chains.** Use CSS `transition-delay: calc(N * var(--cm-stagger))` so pacing changes propagate from one token.
10. **Builds file review UI with `innerHTML`.** XSS vector when filenames come from user input. Use `textContent` + DOM construction.

## Implementation Rules

1. **Vanilla only.** No React, Vue, Svelte, Angular. Plain HTML + CSS + JS. These are marketing page embeds — a framework adds 30-100KB for effects that need <2KB of JS.
2. **Single-file output.** Everything in one HTML file. CDN imports for fonts only (+ Lottie when needed). Single-file means drag-and-drop into any CMS or Webflow embed block.
3. **`requestAnimationFrame` only.** Never `setInterval` for visual animation loops. `setInterval` permitted only for non-visual state cycling (e.g., "PROCESSING..." dot count).
4. **`performance.now()` for timing.** Never `Date.now()` in animation tick functions.
5. **`prefers-reduced-motion` required.** Every animated effect shows its final state immediately when reduced motion is preferred. No motion, no transitions.
6. **Visibility API integration.** Pause all animation loops when `document.hidden === true`. Resume on visibility change.
7. **`will-change` lifecycle.** Add `will-change: opacity, transform` before animation starts, remove after completion. Never leave it permanent.
8. **`--cm-*` tokens everywhere.** Never hardcode colors, timing, or typography — always reference custom properties.
9. **Guard double-initialization.** Every init function checks `dataset.{name}Init === "true"` before proceeding. Without this, hot-reload in dev tools or Webflow's live preview runs init twice, doubling all animations.
10. **Viewport meta required.** `<meta name="viewport" content="width=device-width, initial-scale=1">`. Without it, mobile browsers zoom to 980px default, breaking all clamp() sizing.
11. **Touch and resize handlers.** Responsive recalculation on `resize` (debounced 80ms). Touch-friendly interaction targets.
12. **Accessible by default.** `aria-hidden="true"` on decorative elements (cursors, spinners). `role="progressbar"` with `aria-valuenow` on progress bars. All content readable without JS.
13. **Font: Geist + Geist Mono.** Via Google Fonts CDN. `-webkit-font-smoothing: antialiased`. Geist's monospace numerals and tight letter-spacing match the ConductorAI source. The mono variant is essential for terminal displays and dot-leader alignment.

## Anti-Patterns

- Never use `transition: all` — explicitly list each property and duration
- Never animate `width`, `height`, `top`, `left`, `margin`, `padding` — use `transform` and `opacity` only
- Never hardcode stagger delays in ms — use CSS custom property `--cm-stagger` multiplied by index
- Never omit `prefers-reduced-motion` — every effect needs it, no exceptions
- Never animate off-screen elements — guard with IntersectionObserver or page-load class toggle
- Never use `Date.now()` in rAF loops — `performance.now()` is monotonic and sub-ms accurate
- Never leave `will-change` on permanently — it reserves GPU memory; add before, remove after
- Never assume typing text is single-line — handle `white-space: nowrap` on the typing container, not the parent
- Never use pure white `#FFFFFF` as text in dark mode — use `--cm-text` (`#E8ECF4`) for less eye strain
- Never play Lottie animations eagerly on mobile if they're below the fold — use IntersectionObserver
- Never create typing effects without cursor — the cursor sells the illusion
- Never hardcode file extensions in the file-review pattern — parse from filename

See `references/anti-patterns.md` for expanded explanations with code examples.

## Generator Script

```bash
python3 scripts/conductor_motion_generator.py \
  --mode typewriter|progress|file-review|stagger-reveal|terminal|lottie-compose|full-page|catalog \
  --pacing slow|medium|fast \
  --stagger 200 \
  --typing-speed 45 \
  --easing cubic \
  --color-scheme dark|light \
  --accent "#4F7BF7" \
  --output output.html
```

Mode-specific content flags documented under Composition Parameters.

## Validation

```bash
python3 scripts/validate_conductor_motion.py output.html
```

Checks: viewport meta, `--cm-*` properties, no framework imports, `requestAnimationFrame` present, `prefers-reduced-motion` media query, `performance.now()` in animation code, font-smoothing, `aria-hidden` on cursors, `document.hidden` visibility check, no `transition: all`, no `setInterval` for animation (warning for any `setInterval`), no layout-triggering property animation.

## References

Load on-demand when implementing specific patterns:

| Reference | Covers |
|-----------|--------|
| `references/design-tokens.md` | Full `--cm-*` token system: dark/light schemes, easing functions, timing constants per mode, pacing multiplier |
| `references/typewriter-patterns.md` | Hero rotator + type-on variants, timing constants, cursor styles, visibility API, word cycling state machine |
| `references/progress-simulation-patterns.md` | Progress bar, easeOutCubic tick, counters, dot-leaders, staggered rows, processing dots |
| `references/stagger-reveal-patterns.md` | Hero cascade, section reveals, IntersectionObserver, scroll-triggered, double-rAF technique |
| `references/file-review-patterns.md` | State machine (unreviewed→processing→reviewed), template cloning, status indicators, SVG icons |
| `references/terminal-display-patterns.md` | Status typing, timestamps, dot-leaders, search result counters, progress sync |
| `references/lottie-orchestration.md` | Lottie player setup, responsive variants, scroll-synced playback, data attributes |
| `references/scroll-driven-animations.md` | CSS animation-timeline, GSAP ScrollTrigger fallback, IntersectionObserver patterns |
| `references/anti-patterns.md` | Banned patterns with wrong/right code examples and rationale |
| `references/advanced-compositions.md` | Workflow graphs, multi-agent review, reviewer sidebar, search input sim, comparison bars, dot-matrix numbers, corner brackets |

## Cross-Skill Relationships

- **grainient**: Grainient owns CSS surface effects (shadows, aurora, glass, ticker, hover-zoom). Conductor-motion owns behavioral animations (typing, progress, state machines, stagger sequences). Rule: if it simulates software behavior, it's conductor-motion; if it's a visual treatment, it's grainient.
- **minoan-frontend-design**: Creative direction and text-animation-catalog provide timing specs that conductor-motion implements as generators. MOTION_INTENSITY dial from `.design-context.md` drives pacing selection.
- **design-polish**: Conductor-motion output must pass design-polish's motion checks (150–300ms state changes, ease-out-quart, transform+opacity only).
- **design-audit**: Output must pass accessibility checks (reduced-motion, aria attributes, contrast).
- **threejs-particle-canvas**: Boundary at "2D behavioral vs 3D visual." Loading spinners with parametric curves → threejs-particle-canvas. Progress bar simulations → conductor-motion.
- **rocaille-shader**: No overlap. Shaders are visual treatments, not behavioral simulations.
- **shape**: Upstream. Produces `.design-context.md` that conductor-motion consumes for pacing and token context.

## Attribution

Patterns deconstructed from [ConductorAI.com](https://www.conductorai.com/) (Webflow, May 2026). Technologies: GSAP 3.15 + ScrollTrigger, Lottie (lottie-web), Finsweet Attributes, vanilla JavaScript. Typography: Geist + Geist Mono via Google Fonts.
