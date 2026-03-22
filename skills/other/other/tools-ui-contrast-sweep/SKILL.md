---
name: tools-ui-contrast-sweep
description: At user-specified breakpoints, audit the UI for contrast failures (text/background, icons, controls, focus indicators) and visual-uniformity drift (inconsistent tokens, typography, spacing, component variants). Produces screenshot-backed findings with WCAG-aligned thresholds and fix hypotheses.
operating_mode: AUDIT
trigger_conditions: accessibility, color contrast, WCAG, pre-launch QA, visual uniformity, dark mode audit, focus indicators
related_skills: tools-ui-breakpoint-sweep, lp-design-qa, lp-do-build
---

# Contrast + Uniformity Sweep

Audit rendered UI across explicit breakpoints and theme modes to find legibility and visual-system consistency failures.

This skill is diagnostic only: identify, evidence, classify, and propose fix direction. Do not redesign or patch code during the sweep unless explicitly requested.

## Relationship to Other Skills

- `tools-web-breakpoint`: responsive containment/reflow failures across breakpoints. Use together when contrast failures appear only after responsive stacking.
- `lp-design-qa`: static code/token/a11y audit without runtime screenshots. Use to trace root causes for repeated uniformity drift.
- `meta-user-test`: broad site-wide health audit. Use when route coverage should be sitemap-driven rather than operator-selected.
- `lp-do-build`: implement fixes after this report is approved.

## Required First Prompt

If missing from operator input, ask exactly:

`Which breakpoint widths (px) and which theme modes (light/dark/brand themes) should I test for contrast + uniformity?`

Then collect required surfaces:

`Which UI surfaces should be in scope (header/nav, primary CTAs, forms, modals, tables, marketing pages)?`

## Inputs

| Input | Required | Notes |
|------|----------|-------|
| Breakpoints (px) | Yes | e.g. `320, 375, 430, 768, 1024, 1280` |
| Theme modes | Yes | light/dark/brand themes |
| Target surfaces | Yes | scope-critical areas to audit |
| Standard | No (recommended) | default `WCAG 2.x AA`; operator may request AAA |
| Token references | No | `tokens.ts`, CSS vars, Tailwind/token docs |

If operator gives only breakpoints:
- default to `WCAG 2.x AA`
- run light mode first
- record assumptions explicitly in the report

## Standards and Thresholds

Use these defaults unless operator requests otherwise.

### WCAG AA defaults

- Normal text (`<18pt` and `<14pt bold`): `>= 4.5:1`
- Large text (`>=18pt` or `>=14pt bold`): `>= 3.0:1`
- Non-text essential UI (icons, borders, controls): `>= 3.0:1`
- Focus indicators: `>= 3.0:1` against adjacent colors and visibly discernible

### If operator requests AAA

- Normal text: `>= 7.0:1`
- Large text: `>= 4.5:1`
- Non-text/focus checks remain at WCAG non-text contrast criteria (`>= 3.0:1`)

### Sampling requirement for complex backgrounds

For gradients/images/translucent overlays/blurred surfaces, sample multiple points and report:
- worst-case ratio (required)
- average ratio (recommended)

## Repo Context to Load

Before auditing, load the visual-system baseline:

- `docs/design-system-handbook.md`
- `docs/typography-and-color.md`
- `packages/themes/<theme>/src/tokens.ts` (or `packages/themes/base/src/tokens.ts`)
- `packages/design-system/src/utils/style/overflowContainment.ts`

For token drift triage, run static scans in affected app paths (examples):

- non-token colors: `rg -n "#[0-9a-fA-F]{3,8}|rgb\\(|hsl\\(" apps packages`
- default Tailwind palette drift: `rg -n "\\b(bg|text|border)-(red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50|100|200|300|400|500|600|700|800|900)\\b" apps packages`
- arbitrary sizing/spacing drift (triage only): `rg -n "\\[[0-9.]+(px|rem|em|vh|vw|%)\\]" apps packages`

## Workflow

### 1) Intake and Matrix Setup

1. Confirm breakpoints, modes, surfaces, and standard (AA/AAA).
2. Resolve route list from operator surfaces (or infer best-effort routes and mark assumptions).
3. Set stable viewport height (default `900`).
4. Prepare artifact folder and screenshot naming convention.
5. **Detect JS theme toggle** — scan page source for `localStorage` + `data-theme` (or equivalent cookie/class-based toggle). If found, expand the test matrix (see step 2a below).

### 2) Breakpoint Sweep Execution

For each breakpoint `W` and each mode:
1. Set viewport to `W x 900`.
2. Visit each target route/surface.
3. Capture baseline screenshot.
4. Run contrast checks and uniformity checks.
5. Trigger interaction states where feasible:
   - hover / active
   - disabled
   - `focus-visible` via keyboard tab flow
   - modal/drawer/popover open states
   - form error states (if low-friction to trigger)

### 2a) Split-State Testing (mandatory when JS theme toggle detected)

A JS toggle (localStorage, cookie, or `data-theme` attribute) and `prefers-color-scheme` are independent systems. They can disagree — e.g. OS in light mode but toggle previously set to dark. CSS variables controlled only by `@media(prefers-color-scheme)` are invisible to the toggle, causing broken mixed states that `emulateMedia` alone can never reproduce.

**Always test all four combinations when a toggle exists:**

| `emulateMedia` | localStorage/toggle | Scenario label |
|---|---|---|
| light | light | `media-light/toggle-light` (clean) |
| dark | dark | `media-dark/toggle-dark` (clean) |
| **light** | **dark** | `media-light/toggle-dark` ← most common user-facing breakage |
| **dark** | **light** | `media-dark/toggle-light` |

**How to inject localStorage state in Playwright:**
```js
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => localStorage.setItem('sl-theme', 'dark')); // or whatever key
await page.reload({ waitUntil: 'load' });
// confirm: await page.evaluate(() => document.documentElement.getAttribute('data-theme'))
```

**What to check in split states:**
- CSS custom properties that appear in `@media(prefers-color-scheme)` but NOT in `html[data-theme]` — these will hold stale values in the mismatched state
- Text colour vars (`--text`, `--text-muted`) that come from `data-theme` paired against background/surface vars that come from `@media` only (or vice versa)
- Any component that hardcodes `color:#fff` or `color:#000` while its background var is theme-switched

**Flag as S1** if any split state produces unreadable text. The root cause is always: CSS variables split across two theming systems that don't fully overlap.

**Recommended fix pattern:** Make `html[data-theme="dark/light"]` the single authoritative source for ALL CSS vars. Keep `@media(prefers-color-scheme)` only as a FOUC fallback (it fires before JS runs). Since `html[data-theme]` has higher specificity than `:root` inside `@media`, it will always win once JS sets it.

### 3) Contrast Checks (priority order)

Audit:
- primary text blocks (body/headings/captions/helper text)
- interactive text (links, button labels, nav items)
- form affordances (placeholder, borders, error/success text)
- icons and badges (especially icon-only controls)
- focus rings/outlines during keyboard navigation
- overlay scenarios (scrims, translucency, image cards, gradients)

Flag contrast findings when:
- measured ratio is below threshold
- normal state is borderline and fails on hover/focus/disabled/error
- worst-case sample on gradient/image fails
- placeholder substitutes label with low contrast
- focus indicator exists but is visually indistinct

Evidence required per contrast finding:
- breakpoint + mode + route
- element label/selector/component best-effort
- state (`default|hover|focus|disabled|error|active`)
- measured ratio(s) with threshold (worst-case mandatory)
- screenshot with element clearly visible

### 4) Uniformity Checks (priority order)

Audit:
- color/token compliance and repeated non-token drift
- component consistency (buttons/links/inputs across routes)
- typography consistency (size/weight/line-height hierarchy)
- spacing/radius/shadow rhythm consistency
- dark-mode parity for hierarchy/affordances

Flag uniformity findings when:
- same component family differs materially in computed styles
- repeated non-token colors or inconsistent opacity values appear
- disabled/focus states differ across equivalent components
- same semantic meaning uses conflicting visual treatments
- hierarchy weakens (e.g., heading visually weaker than body)

Evidence required per uniformity finding:
- breakpoint + mode + route
- component family (best effort)
- exact observed difference (what differs and where)
- screenshot pair (`reference` vs `drift`)
- likely cause hypothesis (token bypass/local override/missing variant)

### 5) Severity Model

- **S1 Blocker**: text/controls not reliably readable; critical actions obscured; focus effectively invisible for keyboard users
- **S2 Major**: widespread AA/AAA failures on key UI or system inconsistency harming trust/comprehension
- **S3 Minor**: localized drift/cosmetic inconsistency without material task failure

### 6) Responsive-vs-Palette Attribution Rule

If a contrast failure appears only at specific breakpoints due to layout/image stacking, classify as responsive root cause (with contrast impact), not pure palette failure. Cross-reference `tools-web-breakpoint` for follow-up.

### 7) Output Artifacts

Write report + screenshots:

- Report: `docs/audits/contrast-sweeps/YYYY-MM-DD-<slug>/contrast-uniformity-report.md`
- Screenshots: `docs/audits/contrast-sweeps/YYYY-MM-DD-<slug>/screenshots/`

Optional machine-readable artifacts (recommended for regression tracking):

- `docs/audits/contrast-sweeps/YYYY-MM-DD-<slug>/contrast-findings.json`
- `docs/audits/contrast-sweeps/YYYY-MM-DD-<slug>/uniformity-findings.json`

Use `.claude/skills/tools-ui-contrast-sweep/modules/report-template.md` for required structure.

### 8) Completion Message

Return:
- breakpoints and modes tested
- surfaces/routes covered
- issue totals by severity
- report path + JSON artifact paths (if produced)
- assumptions and uncovered scope gaps

If no issues are found, state exactly:

`No contrast or visual-uniformity failures detected across the tested breakpoint/mode matrix.`

- If issues were found and fixed via `/lp-do-build`: **re-run this sweep** to confirm findings are resolved before routing to `tools-refactor`.
- If the page has a JS theme toggle: re-run must include all four split-state combinations, not just clean `emulateMedia` states. A fix that only passes clean states may still fail in the mismatched case.

## Guardrails

- Do not propose color changes that break brand intent without noting tradeoffs.
- Prefer token-level/component-variant fixes over per-page overrides.
- Validate `focus-visible` states explicitly via keyboard path.
- Avoid reporting micro-differences unless they affect readability, interaction, or hierarchy.

## Integration

- **Upstream:** `lp-design-qa` (optional trigger — contrast-sweep is often invoked after lp-design-qa flags color or accessibility concerns); `lp-do-build` (direct invocation for pre-launch QA pass).
- **Downstream:** `tools-refactor` (contrast and token findings feed the refactor entry criteria); `lp-do-build` (issues returned as structured findings for fix tasks).
- **Loop position:** S9B secondary skill, required before S9B→SIGNALS advance (`GATE-UI-SWEEP-01`). Also runs alongside `tools-ui-breakpoint-sweep` at S9C for ongoing quality passes.
- **S9B advance requirement:** When running this sweep for S9B→SIGNALS advance, the operator must manually set `Business: <BIZ>` in the report frontmatter (the template includes a placeholder — replace it with the actual business identifier). All application routes must be covered; `Routes-Tested: 0` will block the advance gate. Both light and dark modes must be tested. All S1 blockers must be resolved before advancing.
