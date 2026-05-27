---
name: dembrandt
description: >
  Orchestrator for the full dembrandt UX pipeline. Routes a UI/UX task through six ordered stages —
  brand foundation → design tokens → layout → components → UX polish → accessibility gate — loading
  the right sub-skill at each stage. Use when the task spans multiple design concerns: "design review",
  "build UI", "audit interface", "from brand to UI". For single-concern tasks (e.g. "review my colour
  palette") go directly to the relevant sub-skill instead.
metadata:
  priority: 10
  authors:
    - name: VictorGjn
      url: https://github.com/VictorGjn
      note: original concept and pipeline design
  docs:
    - "https://dembrandt.com"
    - "https://www.npmjs.com/package/dembrandt"
  promptSignals:
    phrases:
      - "design review"
      - "build ui"
      - "audit interface"
      - "from brand to ui"
      - "full ux review"
      - "ui audit"
      - "review my ui"
      - "review this interface"
      - "design audit"
      - "ux audit"
retrieval:
  aliases:
    - dembrandt pipeline
    - full ux pipeline
    - ui design orchestrator
    - end-to-end design review
  intents:
    - run a full UX review across multiple design concerns
    - orchestrate brand-to-UI design pipeline
    - audit an interface end to end
    - run all design checks in order
  examples:
    - review my checkout flow
    - audit this interface
    - do a full design review
    - build a UI from scratch following best practices
    - run the dembrandt pipeline on this product
---

# dembrandt — UX Pipeline Orchestrator

> Concept by [@VictorGjn](https://github.com/VictorGjn).

Routes multi-concern UI/UX tasks through six ordered stages. Each stage loads sub-skills on demand — only what the task actually needs.

**When to use this skill vs a sub-skill directly:**

- Multi-concern task ("design review", "audit interface", "build UI") → use this orchestrator
- Single-concern task ("check my colour palette", "review button states") → go directly to the sub-skill
- Brand-to-token-to-spec pipeline with a URL or DESIGN.md → use `generate-ui-from-brand` instead

---

## Pipeline

### Stage 1 — Brand Foundation

Establish the visual language before making any token decisions.

Sub-skills (load as needed):
- `brand-visual-language` — shape language, icon style, typography tone
- `algorithmic-color-palette` — derive states and brand-tinted greys from brand colours
- `color-mode-and-theme` — light vs dark vs combined, when to offer a theme selector

**Gate:** Brand tone and colour system agreed before proceeding.

---

### Stage 2 — Design Tokens & Scales

Pin the numeric system so all components share a common foundation.

Sub-skills (load as needed):
- `modular-scale-typography` — ratio-based type scales, minimum sizes, context-aware usage
- `elevation-and-depth` — shadow scale, border-radius, card and modal patterns
- `button-states` — six states: rest, hover, active, focus, disabled, loading
- `component-family-consistency` — buttons, inputs, pills: shared radius, colour, height
- `status-colors-and-errors` — minimal semantic colours, error recovery, prevention

**Gate:** Tokens defined and consistent across component family.

---

### Stage 3 — Layout & Structure

Apply layout decisions to the specific product context.

Sub-skills (load as needed):
- `gestalt-ui-organisation` — group related controls: proximity, similarity, common region
- `visual-emphasis-and-hierarchy` — one CTA per view, colour and size as emphasis
- `information-architecture` — naming, mental models, data UI, confirm dialogs
- `ui-context-and-scope` — hierarchy, breadcrumbs, colour regions, scope communication
- `responsive-paradigms` — mobile/tablet/desktop: nav, sections, sticky behaviour
- `ui-density` — match density to platform and user type
- `sticky-and-fixed-elements` — headers, bottom toolbars, z-index tokens
- `scroll-areas` — avoid inner scroll, one axis only, user-controlled

**Gate:** Layout is coherent across breakpoints and user contexts.

---

### Stage 4 — Components & Interaction

Review component patterns and interactive states.

Sub-skills (load as needed):
- `real-world-metaphors` — cards, carousels, drawers: when to use and how
- `form-design` — helper text, placeholder, validation, submit state
- `data-display-and-selection` — grid/list/table, large hit areas, mass actions
- `global-toolbar-controls` — currency, language, locale: placement and typography
- `notifications-and-recovery` — toasts, banners, retry, undo — always a path forward

**Gate:** All interactive states handled; no dead ends.

---

### Stage 5 — UX Polish

Apply UX principles and motion to sharpen perceived quality.

Sub-skills (load as needed):
- `nielsen-usability-heuristics` — 10 usability principles with review checklists
- `user-flows-and-guided-paths` — wizards, purchase flows, onboarding sequences
- `micro-interactions` — animated icons, toggles, reveals, celebrations
- `loading-states-and-perceived-performance` — spinners, skeleton screens, staggered entry
- `motion-and-storytelling` — Disney principles and cinematic language in UI

**Gate:** Flow is legible end-to-end; perceived performance is acceptable.

---

### Stage 6 — Accessibility & Technical Gate

Hard ship gate. Do not skip or defer.

Sub-skills (load as needed):
- `wcag-accessibility` — WCAG 2.2 AA / EN 301 549: contrast, keyboard, ARIA
- `semantic-html-and-seo` — HTML5, alt texts, Open Graph, progressive enhancement
- `performance-and-web-vitals` — Lighthouse audit, LCP, CLS, INP, images, fonts, JS loading

**Gate:** Passes WCAG 2.2 AA. Required by EU Accessibility Act (EAA) for products launched after June 2025.

---

## Relationship to `generate-ui-from-brand`

`generate-ui-from-brand` is a token-extraction pipeline: URL or DESIGN.md → tokens → UI spec. It overlaps stages 1–2 of this orchestrator. Use it when you have a brand source and need a concrete spec. Use this orchestrator when you are reviewing or building across the full stack of UX concerns without a specific brand-extraction starting point.
