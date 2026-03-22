---
name: tools-ui-breakpoint-sweep
description: Open the app at user-specified viewport widths and systematically detect responsive layout failures (overflow/bleed, clipping, misalignment, broken reflow). Produces a screenshot-backed issue log with repro steps and fix hypotheses.
operating_mode: AUDIT
trigger_conditions: responsive layout, breakpoint QA, overflow, reflow failures, mobile layout, viewport testing, horizontal scroll
related_skills: tools-ui-contrast-sweep, lp-design-qa, lp-launch-qa, lp-do-build
---

# UI Breakpoint Sweep

Run a deterministic responsive QA sweep across explicit viewport widths and routes. Detect containment, reflow, and overlay failures with screenshot-backed evidence.

This is a QA/diagnostic skill, not a redesign exercise.

## Relationship to Other Skills

- `lp-design-qa`: static code audit of responsive intent and token usage; no browser rendering or screenshot evidence.
- `tools-ui-breakpoint-sweep`: live rendered behavior across explicit breakpoints with screenshot-backed defects.
- `meta-user-test`: broad crawl/site-health audit; use it when you need full-site coverage beyond selected routes.
- `lp-launch-qa`: pre-launch gate; consume this sweep as responsive evidence for conversion/performance readiness.
- `lp-do-build`: execute fixes after this sweep report is approved.

## Required First Question

If widths are not already provided, ask exactly:

`Which breakpoint widths (in px) should I test?`
`Example: 320, 375, 430, 768, 1024, 1280`

Do not start the sweep until widths are confirmed.

## Inputs

| Input | Required | Notes |
|------|----------|-------|
| Breakpoints (px) | Yes | Comma-separated widths, e.g. `320,375,430,768,1024,1280` |
| App entry URL | Yes | Local or deployed URL |
| Routes/screens to cover | No (recommended) | If absent, discover primary navigation routes plus at least one dense page |
| Auth scope or test account | No | If login is required and no credentials exist, run no-auth scope and document the gap |
| Theme/mode/locale | No | e.g. light/dark, locale, long-text stress mode |

If the operator only provides widths, proceed with sensible defaults for optional inputs and explicitly document assumptions.

## Defaults (only when operator does not specify)

- Breakpoints: `320, 375, 390, 414, 480, 600, 768, 820, 1024, 1280, 1440`
- Viewport height: `900`
- Routes:
  1. app entry route
  2. primary same-origin navigation targets discovered from visible navigation links
  3. at least one dense route (forms/tables/modals/drawers/filters)
- Theme/locale: app default

If app URL is missing, ask: `What URL should I sweep?`

## Operating Mode

**AUDIT + REPORT (read-only against product code)**

**Allowed:**
- Open app in browser automation and set viewport widths
- Navigate routes and interact with menu/modal/drawer/accordion/dropdown states
- Capture full-page and focused screenshots
- Write report artifact and screenshot files

**Not allowed:**
- Code or CSS changes unless explicitly requested after reporting
- Subjective redesign commentary without reproducible defects
- Marking issues without evidence

## Output Contract

Write one report artifact plus linked screenshots:

- Report: `docs/audits/breakpoint-sweeps/YYYY-MM-DD-<slug>/breakpoint-sweep-report.md`
- Screenshots: `docs/audits/breakpoint-sweeps/YYYY-MM-DD-<slug>/screenshots/`

Use `.claude/skills/tools-web-breakpoint/modules/report-template.md` for required report structure.

Every issue must include: breakpoint, route, repro steps, expected vs actual, severity, and screenshot link(s).

## Workflow

### 0) Write QA Inventory (Required Gate)

Before any browser is opened, write a QA inventory. **Do not start the sweep until this inventory is complete.**

Build the inventory from three sources:

1. **User requirements** — what was explicitly requested or described as the test scope.
2. **Features being tested** — every meaningful user-facing control, mode switch, or interactive behaviour visible on the routes under test.
3. **Claims to sign off** — every user-visible claim you intend to make in the final report.

For each item, note the intended functional check and the visual state where the claim must be verified.

Add **at least 2 exploratory / off-happy-path scenarios** — interactions not on the scripted path that could expose fragile behaviour (e.g. resizing the viewport mid-interaction, rapidly toggling a drawer, submitting an empty form, tabbing through all focusable controls).

The inventory is the shared coverage list for both the Functional QA Pass and the Visual QA Pass. Copy it into the report's `## QA Inventory` section.

### 1) Intake and Sweep Plan

1. Confirm breakpoint list and URL.
2. Resolve route list:
   - Use operator-provided routes when available.
   - Otherwise discover primary navigation routes and add at least one dense route.
3. Record assumptions (auth, theme, locale, unavailable routes).
4. Prepare artifact directory and screenshot naming convention.

### 2) Execute Breakpoint Matrix

For each width `W`:

1. Set viewport to `W x 900`.
   - **For mobile breakpoints (W ≤ 480px):** also configure the browser context with `isMobile: true` and `hasTouch: true` to enable realistic touch-event simulation and mobile user-agent behaviour. These flags must be set in the browser context options, not only via viewport size.
2. For each target route, run the **Functional QA Pass** first, then the **Visual QA Pass**.

#### Functional QA Pass

Use real user controls for all checks — keyboard, mouse click, touch events (at W ≤ 480px). Browser `evaluate()` calls may inspect or stage state but **do not count as functional signoff input**.

- Navigate and wait for ready state (`network idle` or app-ready selector).
- Run overflow/reflow checks (see §4 Detection Heuristics).
- Trigger interactive states using real input:
  - mobile nav/hamburger — open and close via tap/click
  - one modal/drawer/popover — open, interact, verify close control is reachable, close
  - one accordion/dropdown — cycle through states: open → closed → open
  - key forms/tables/cards — attempt the primary action or submission
- For reversible controls or stateful toggles in the QA inventory: test the full cycle (initial state → changed state → returned to initial).
- Work through every item in the QA inventory. If a new control or state is discovered, add it to the inventory before continuing.

#### Visual QA Pass

Run this as a separate, explicit pass after the Functional QA Pass is complete.

- Capture baseline full-page screenshot.
- Inspect the initial viewport before scrolling — confirm the core content and primary CTA are clearly visible without clipping.
- Inspect all required visible regions (nav, hero/content area, primary CTA, modals/drawers in settled state, footer).
- Inspect at least one in-transition state (drawer opening, modal appearing) when motion is part of the experience.
- Judge aesthetic quality as well as correctness — the UI should feel intentional and coherent at this breakpoint.
- Capture focused screenshot(s) for any detected issue, in addition to the full-page baseline.

### 3) Failure Taxonomy

Assess each route+width against:

- **A. Viewport overflow (page-level)**
  - Unexpected horizontal scroll
  - Visible elements extending beyond viewport bounds
- **B. Parent/container overflow (component-level)**
  - Child bleed beyond parent bounds
  - Unintentional clipping from `overflow: hidden|clip`
  - Text truncation that destroys meaning
- **C. Reflow correctness**
  - Columns failing to stack
  - Fixed widths blocking responsive behavior
  - Wrapping that makes controls unusable
  - Misalignment/overlap jitter
- **D. Fixed layers/overlays**
  - Sticky header/footer obscures content
  - Modal/drawer exceeds viewport with no usable internal scroll
  - Off-screen drawer or unreachable close controls
- **E. Density/long-content stress**
  - Long titles/translations/numbers/tags pushing controls off-screen or collapsing hierarchy

### 4) Detection Heuristics (practical pass/fail rules)

Flag an issue if any condition is true:

- `documentElement.scrollWidth > documentElement.clientWidth + 2` (unexpected horizontal scroll)
- Visible element has `rect.right > viewportWidth + 4` or `rect.left < -4`
- Parent with `overflow: hidden|clip` partially hides meaningful child content without intentional truncation behavior
- Critical controls (primary CTA, submit, nav close, modal close) are clipped/off-screen or require horizontal scrolling
- Sticky/fixed layers overlap first actionable content and prevent normal interaction
- Modal/drawer cannot be fully navigated or closed on the current viewport

**Per-region viewport fit check (required before signoff):**

For each critical region — navigation bar, primary CTA, modal or drawer close button, and form submit button — run `getBoundingClientRect()` and verify:
- `rect.right ≤ viewportWidth` and `rect.left ≥ 0` (no horizontal bleed)
- `rect.bottom ≤ viewportHeight` (visible without scroll, for above-the-fold regions)

Document-level scroll metrics alone (`scrollWidth > clientWidth`) are not sufficient. Internal panes, fixed-height shells, and hidden-overflow containers can clip required UI while page-level scroll checks still pass.

Noise-control rules (do not over-report):

- Ignore <=2px overflow caused by rounding/subpixel rendering.
- Do not flag intentional horizontal containers (`overflow-x-auto`) when content remains reachable and semantics stay clear.
- Ignore hidden/off-canvas elements not intended to be visible and not intercepting interaction.

### 5) Severity Model

- **S1 Blocker**: core action impossible (submit, checkout, navigation, close modal)
- **S2 Major**: primary content/control impaired or misleading; workaround exists but UX is materially degraded
- **S3 Minor**: cosmetic/alignment issue with preserved usability

### 5.5) Exploratory Pass

After the scripted breakpoint matrix is complete, perform an unscripted exploratory pass on each route before writing the report.

- Allow ~30–90 seconds of free-form interaction: resize the viewport mid-session, navigate via keyboard only, tap in unexpected areas, attempt edge-case inputs (empty forms, long strings, rapid toggling).
- If a new control, state, or failure mode is discovered: add it to the QA inventory and include it in the report.
- The exploratory pass is not scored separately — findings feed into the main Issues list with the same severity model (§5).

### 6) Report and Evidence

For each issue, include:

- Breakpoint width
- Route/screen
- Component or section (best effort)
- Repro steps
- Expected vs actual
- Severity (`S1|S2|S3`)
- Screenshot links (full-page + focused when needed)
- Fix hypothesis (likely CSS cause + quick direction)

Typical fix directions to mention when applicable:

- missing `min-w-0` on flex/grid children
- incorrect `overflow` containment on component shells
- hard-coded widths replacing responsive constraints (`w-full`, `max-w-*`)
- missing wrap rules (`flex-wrap`, text wrap/word-break)
- overlay sizing/scroll fixes (`max-h-[dvh]`, internal scroll region)
- use shared design-system containment helpers where relevant (`overflowContainmentClass(...)` in `packages/design-system/src/utils/style/overflowContainment.ts`)

### 7) Completion Message

Return:

- breakpoints tested
- routes tested
- issue totals by severity
- path to `breakpoint-sweep-report.md`
- explicit assumptions and uncovered scope gaps
- **Negative confirmation** — for each defect class, state whether it was checked and not found:
  - A. Viewport overflow (unexpected horizontal scroll at page level)
  - B. Container overflow (component-level clipping or bleed beyond parent bounds)
  - C. Reflow correctness (columns not stacking, fixed widths, wrapping failures, alignment jitter)
  - D. Fixed layers / overlays (sticky headers obscuring content, unreachable modal/drawer close)
  - E. Density / long-content stress (long text, dense tables, or tag lists pushing controls off-screen)

If no issues are found, explicitly state:

`No responsive layout failures detected across tested breakpoint/route matrix. Defect classes A–E all checked; no failures found.`
- If issues were found and fixed via `/lp-do-build`: **re-run this sweep** to confirm findings are resolved before routing to `tools-refactor`.

## Integration

- **Upstream:** `lp-design-qa` (optional trigger — breakpoint-sweep is invoked after lp-design-qa flags responsive or layout concerns); `lp-do-build` (direct invocation for pre-launch QA pass).
- **Downstream:** `tools-refactor` (layout and overflow findings feed the refactor entry criteria); `lp-do-build` (issues returned as structured findings for fix tasks).
- **Loop position:** S9C (Parallel Sweep) — runs alongside `tools-ui-contrast-sweep` after UI build and static QA, before refactor.
- **Note:** `lp-responsive-qa` (under construction, see `docs/plans/lp-responsive-qa-skill/`) is a complementary rendered-screenshot skill for browser-based responsive validation. It will sit between `lp-do-build` and `lp-design-qa` once shipped. `tools-ui-breakpoint-sweep` remains the static layout audit tool.
