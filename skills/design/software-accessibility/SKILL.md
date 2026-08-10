---
name: software-accessibility
description: "Implements accessibility fixes in code. Use when remediating semantic HTML, ARIA, focus, keyboard support, or screen-reader behavior."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Accessibility Engineering

Use this skill to implement accessibility in code: semantic HTML, ARIA only where necessary, keyboard support, focus management, screen-reader compatibility, and baseline automation in CI.

This skill owns engineering implementation. It does not own design-side WCAG interpretation or formal accessibility-test programs.

## Quick Reference

| Need | Default | Notes |
|------|---------|-------|
| fix component semantics | semantic HTML first | add ARIA only when HTML is insufficient |
| keyboard support | tab order, visible focus, correct key handling | test manually every time |
| screen reader verification | VoiceOver plus NVDA minimum | use two readers when possible |
| automated coverage | axe-core plus Lighthouse or Pa11y | automation catches markup-level issues, not the full experience |
| modal or composite widget | APG-aligned pattern | do not invent custom keyboard behavior |
| compliance prep | WCAG 2.2 AA minimum, then local regulation check | verify current legal posture before final claims |
| WCAG 2.2 checklist, axe-core/Pa11y snippets, EU Accessibility Act | [references/wcag-2-2-checklist.md](references/wcag-2-2-checklist.md) | includes June 2025 EAA applicability decision |
| run axe-core in CI | [scripts/run_axe.sh](scripts/run_axe.sh) | exits non-zero on violations |

## When to Use This Skill

Use this skill when the main work is:

- remediating semantic HTML, labels, roles, and landmarks
- fixing keyboard access, focus management, or SPA route focus behavior
- implementing APG-style component patterns
- improving screen-reader announcements and dynamic content handling
- adding accessibility engineering checks to CI

Route elsewhere when the main work is:

| Need | Use Instead |
|------|-------------|
| design-side accessibility and interaction design | [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md) |
| accessibility test automation program or formal audit flow | [../qa-testing-accessibility/SKILL.md](../qa-testing-accessibility/SKILL.md) |
| usability research with disabled users | [../software-ux-research/SKILL.md](../software-ux-research/SKILL.md) |
| frontend stack setup and general UI build work | [../software-frontend/SKILL.md](../software-frontend/SKILL.md) |
| platform-specific mobile accessibility behavior | [../software-mobile/SKILL.md](../software-mobile/SKILL.md) |

## Defaults

- semantic HTML before ARIA
- visible focus always on
- keyboard support for every interactive element
- screen-reader checks before calling the fix complete
- automation as baseline, not proof of full accessibility
- current standards and regulatory deadlines are volatile and must be verified before final compliance advice

## Workflow

1. Identify the affected flow, component, and assistive-technology risk.
2. Replace incorrect custom markup with semantic HTML where possible.
3. Add the minimum ARIA state and relationship attributes required for the pattern.
4. Verify keyboard interaction and focus behavior.
5. Verify screen-reader announcements and dynamic updates.
6. Add or update automated checks to prevent regression.

## ASCII Flow

```text
Accessibility request
  -> Identify affected flow and assistive-technology risk
  -> Prefer native semantic HTML or platform control
  -> Add only required ARIA, labels, state, and relationships
  -> Verify keyboard, focus, and screen-reader behavior
  -> Add automated regression checks
  -> Report remaining manual or compliance risk
```

## Implementation Rules

### Semantic HTML First

Default order:

1. native element
2. minimal ARIA enhancement
3. fully custom widget only when no native pattern exists

Common mistakes to avoid:

- `div` or `span` used as buttons
- focusable elements hidden from assistive tech
- redundant or conflicting `aria-label`
- missing state attributes such as `aria-expanded`
- stripping semantics from interactive elements

### Keyboard and Focus

Every interactive surface must support:

- logical tab order
- visible focus indicator
- escape and arrow-key behavior where the pattern requires it
- focus trap and focus restoration for dialogs
- route-change focus management in SPAs

### Screen Reader Verification

Minimum verification set:

- landmarks and heading structure
- form labels and error association
- role and state announcement for controls
- live-region behavior for dynamic feedback
- meaningful alt text and decorative-image hiding

Minimum matrix:

- VoiceOver on Apple platforms
- NVDA on Windows

### Automation and CI

| Layer | Tool | Catches |
|-------|------|---------|
| Authoring | `eslint-plugin-jsx-a11y` (React) or `axe-linter` | Missing labels, wrong roles, bad ARIA usage |
| Component tests | `@axe-core/react` or `jest-axe` | Markup-level violations per component |
| E2E / integration | axe-core via Playwright or Cypress | Page-level violations in rendered state |
| CI gate | Lighthouse or Pa11y | Score regression and critical issues |

Automation does not replace keyboard walkthroughs, screen-reader validation, or judgment on content order, announcement quality, and alt-text quality.

Automated tools detect a real but bounded slice of issues: Deque's 2021 audit-data study found axe-core-class rule checking fully covered about 57% of WCAG issues found in expert audits (verify current figure before quoting; see [references/wcag-2-2-checklist.md](references/wcag-2-2-checklist.md)). Treat "green" automated results as a floor, not a compliance conclusion — a page can pass every automated rule and still fail for real screen-reader users on announcement quality, reading order, and interaction logic that no rule engine parses.

### When Automation Is Enough vs When a Human Must Check

| Signal type | Automatable | Requires a human pass |
|---|---|---|
| Missing `alt`, label, or landmark | Yes — rule-detectable | — |
| Contrast ratio below threshold | Yes — rule-detectable | — |
| `role`/state attribute present but semantically wrong for context | Partial — flags presence, not correctness | Yes — judgment on whether the role fits the interaction |
| Reading order matches visual order | No | Yes — screen-reader walkthrough |
| Live-region announcement is timely and not noisy | No | Yes — screen-reader walkthrough |
| Focus lands somewhere sensible after a route change or async update | No | Yes — keyboard + screen-reader walkthrough |
| Alt text is accurate and non-redundant (not just present) | No | Yes — content review |
| Keyboard operability of a composite widget (arrow keys, Home/End, typeahead) | No | Yes — manual keyboard pass |

Never report an automated scan result (axe-core, Lighthouse, WAVE, Pa11y) as "accessible" or "WCAG conformant" on its own — report it as "N automated violations resolved; manual keyboard and screen-reader verification pending/complete."

## Remediation Prioritization

When a scan or audit returns more issues than can be fixed at once, rank by user impact, not by rule-engine severity label alone:

1. **Blocks a core task entirely** (cannot submit a form, cannot open a required dialog, cannot complete checkout) — fix first regardless of how many instances exist.
2. **Affects a high-traffic or legally sensitive flow** (auth, checkout, account settings, any flow named in a demand letter or audit finding) — fix next.
3. **Widespread pattern-level defect** (e.g., every icon button sitewide is unlabeled) — fix once at the component/design-system level; this clears more violations per hour of engineering time than any single-page fix.
4. **Isolated, low-traffic instances** — batch these; do not let them block a release on their own merits.

Effort-vs-impact check before committing to a large remediation plan: a single shared-component fix (e.g., the button, input, or modal primitive) frequently resolves dozens of scattered violations at once — audit the design system before auditing every page.

## Accessibility Overlay Warning

Do not recommend, and flag if found, third-party "accessibility overlay" or "widget" scripts (icon-based toolbars that claim to auto-remediate a site via injected JavaScript) as a compliance solution. As of 2026-07-11:

- The FTC's April 2025 final order against accessiBe (Decision and Order, April 21, 2025) found the vendor's marketing claims — that its widget made a site "compliant with 30% of WCAG's requirements immediately" and the rest "within 48 hours" via AI — to be deceptive, and fined the company $1,000,000. This is directly citable precedent against overlay-as-compliance claims (verify current status at ftc.gov before citing as ongoing).
- Overlays cannot fix the defects that dominate real WCAG violations: missing or wrong semantic HTML, broken heading hierarchy, incorrect ARIA in source, missing form labels, keyboard traps, and focus-management bugs. These require source-code changes, not a JavaScript layer bolted on top.
- Independent industry consensus (the Overlay Fact Sheet, signed by hundreds of accessibility practitioners and disabled users) documents overlays sometimes actively breaking existing assistive-technology behavior that worked before the overlay was added.
- Overlay-bearing sites are disproportionately named in ADA-related demand letters and lawsuits (industry litigation trackers report overlays present on a substantial share of sued sites) — an overlay is not legal cover and can increase exposure.
- If a client already has an overlay installed: do not treat it as a baseline to build on top of. Recommend fixing the underlying markup and removing or downgrading the overlay to a genuinely optional enhancement (e.g., text resize, contrast toggle) rather than a claimed compliance layer.

## Common Patterns

Use APG-aligned implementations. Do not invent new interaction models when a known pattern exists.

| Widget | Required keyboard behavior | ARIA pattern |
|--------|---------------------------|--------------|
| Tabs | Arrow keys switch tabs; Tab moves into panel | `role="tablist"`, `role="tab"`, `aria-selected` |
| Dialog | Tab/Shift+Tab cycles inside; Escape closes | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| Combobox | Arrow keys navigate listbox; Enter selects; Escape closes | `role="combobox"`, `aria-expanded`, `aria-controls` |
| Accordion | Enter/Space toggle panels; optional arrow-key navigation | `role="button"`, `aria-expanded`, `aria-controls` |
| Menu | Arrow keys navigate items; Escape closes; Tab exits | `role="menu"`, `role="menuitem"`, `aria-haspopup` |
| Tree view | Arrow keys navigate; Enter activates; Space selects | `role="tree"`, `role="treeitem"`, `aria-expanded` |

## Known Traps

- Route transitions in SPAs that never move focus to the new page heading or landmark.
- Dialogs that trap focus while open but fail to restore focus to the triggering control on close.
- Toasts and validation messages that update visually but never announce through a correctly scoped live region.
- Screen-reader-hidden containers that still contain focusable descendants.
- Composite widgets that handle arrow keys but forget Home/End, Escape, typeahead, or disabled-item semantics required by the pattern.
- Mobile-only testing that misses desktop screen-reader and keyboard failures.

## Common Anti-Patterns

- Placeholder text used as the only label.
- Click handlers on non-interactive elements without full keyboard and semantic remediation.
- Positive `tabindex` used to force order instead of fixing DOM order.
- `aria-label` added on top of already-correct visible labels, creating redundant or conflicting names.
- `aria-hidden="true"` applied to visible interactive content.
- Custom selects, comboboxes, or menus built from scratch when a native control or established APG pattern would work.

## AI-Generated Accessibility Risks

Pay extra attention to AI-produced code that shows:

- div soup
- broken or invented ARIA
- missing form labels
- skipped heading hierarchy
- low-contrast styling
- missing or broken focus states
- incomplete keyboard handlers

## Verification Gate

Do not call the work complete until all of these are checked:

- [ ] Keyboard walkthrough passes for the affected flow (Tab, Shift+Tab, Enter, Escape, arrow keys as required)
- [ ] Visible focus indicator present in all interactive states (never removed with `outline: none` alone)
- [ ] Screen-reader output checked on VoiceOver (macOS/iOS) and NVDA (Windows) — two readers minimum
- [ ] Zero critical or serious axe-core violations remain; any suppressed violation has an explicit justification comment
- [ ] Heading order is sequential with no skipped levels; landmark structure matches intended page regions
- [ ] All form inputs have visible labels bound via `for`/`id` or `aria-labelledby`; errors use `aria-describedby`
- [ ] Dynamic content updates announced via correctly scoped `aria-live` region
- [ ] Any WCAG or legal-compliance claim is verified against W3C/WAI or official regulatory sources, not memory

## EU Accessibility Act (June 2025)

The EAA (Directive 2019/882) entered enforcement on 28 June 2025. Scope covers B2C digital services: e-commerce order flows, online banking and financial portals, transport ticketing, e-books and reader apps, and audiovisual media player controls. Member-state market surveillance authorities are live; non-compliance exposes organizations to enforcement and disability-rights litigation. The technical standard is EN 301 549 v3.2.1, which references WCAG 2.1 AA as the web-content baseline; target WCAG 2.2 AA for new builds. See [references/wcag-2.2-and-3.0-watchlist.md](references/wcag-2.2-and-3.0-watchlist.md) for full detail.

## Scenarios

Recipes keyed to symptoms or remediation moments. Each lists the shortest path to resolution.

### S1 — Form audit: missing labels, error association, focus order

1. Run axe-core on the form page; collect all label, error, and focus violations.
2. Replace `placeholder`-only fields with visible `<label for="id">` elements.
3. Associate each error message with its input via `aria-describedby`.
4. Verify tab order matches visual reading order; fix DOM order rather than `tabindex`.
5. Re-run axe-core; confirm zero critical/serious label and error violations remain.
6. Do a keyboard walkthrough end-to-end: Tab, Shift+Tab, Enter, and Escape paths.

### S2 — Modal trap: inert/keyboard escape/focus return

1. Confirm the dialog opens and focus is sent to the first focusable element inside it.
2. Add `inert` attribute to all sibling roots outside the dialog on open; remove on close.
3. Verify Tab and Shift+Tab cycle only inside the dialog.
4. Verify Escape closes the dialog and returns focus to the triggering control.
5. Test with VoiceOver and NVDA; confirm modal role and accessible name are announced.

### S3 — Color contrast remediation in design tokens

1. Extract all foreground/background token pairs from the design system.
2. Run each pair through a WCAG 2.2 contrast checker; flag pairs below 4.5:1 (3:1 for large text).
3. Propose adjusted token values that pass AA; confirm with the design team.
4. Update the token file and regenerate CSS; run Lighthouse in CI to catch regressions.
5. Verify interactive focus indicators meet 3:1 against adjacent colors (WCAG 2.2 SC 1.4.11).

### S4 — RSC navigation focus loss in Next.js 15

1. Reproduce: navigate between routes and observe focus drops to `<body>` on page transition.
2. Add a skip-link at the top of the layout that targets `#main-content`.
3. After each RSC navigation, programmatically focus the `<h1>` or the `#main-content` landmark.
4. Use a `useEffect` on the route segment to move focus after hydration settles.
5. Verify with VoiceOver Safari and NVDA Chrome that route change is announced and focus lands correctly.
6. Add an axe-core E2E assertion on the landing heading to catch regression.

### S5 — Reduced-motion fallback for animation library

1. Audit all animation calls; identify those lacking a `prefers-reduced-motion` branch.
2. Add `@media (prefers-reduced-motion: reduce)` CSS overrides or check the media query in JS.
3. Replace motion-heavy transitions with instant or fade-only alternatives under reduced-motion.
4. Verify with OS reduced-motion enabled on macOS and Windows; confirm no vestibular-triggering motion.
5. Add a CI check (Playwright with `reducedMotion: 'reduce'` context) to prevent regression.

## Navigation

**Adjacent skills**

- [../software-ui-ux-design/SKILL.md](../software-ui-ux-design/SKILL.md)
- [../qa-testing-accessibility/SKILL.md](../qa-testing-accessibility/SKILL.md)
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md)
- [../software-mobile/SKILL.md](../software-mobile/SKILL.md)
- [../software-localisation/SKILL.md](../software-localisation/SKILL.md)
- [../qa-testing-playwright/SKILL.md](../qa-testing-playwright/SKILL.md)

**Sources**

- [data/sources.json](data/sources.json)

## Regulatory Traps

- **EU Accessibility Act (EAA) enforcement began 28 June 2025**: Directive 2019/882 transposed into national law across EU member states; from this date consumer-facing digital products and services — including e-commerce websites, banking apps, e-books, transport booking, and streaming services — must conform or face enforcement action.
- **Conformity standard**: EN 301 549 is the harmonised EU standard for ICT accessibility, currently aligned with WCAG 2.1 AA — no harmonised EN 301 549 version yet incorporates WCAG 2.2 (European Commission guidance, 2025). Plan to WCAG 2.2 AA as a forward-looking target, but legal conformity under EAA is anchored to whichever EN 301 549 version is cited in the Official Journal at audit time. EN 301 549 also adds requirements beyond WCAG for non-web documents, native mobile apps, and ICT hardware — products must meet EN 301 549, not WCAG alone.
- **Scope — who is covered**: businesses with 10+ employees or annual turnover above EUR 2 million selling consumer-facing digital services into the EU are in scope; micro-enterprises (under 10 employees AND under EUR 2M turnover) are exempt from EAA but not from general non-discrimination law.
- **Documentation evidence required**: companies must produce an accessibility statement describing conformance level, known gaps, and a remediation timeline; a conformity assessment is required before placing a product on the market; retain both as evidence for national authority audits.
- **Member-state penalties vary**: enforcement is delegated to national competent authorities (e.g., Equality bodies, market surveillance authorities); fines and corrective orders differ by country — no single EU-wide fine cap; some member states (DE, FR) have established enforcement procedures with significant penalties.
- **Native mobile apps are in scope**: iOS and Android apps that fall under EAA product categories (e.g., banking, e-commerce, transport) must meet EN 301 549 Chapter 11 (mobile accessibility) — WCAG AA alone is insufficient for native apps.
- **Third-party components inherit risk**: if your product uses a third-party UI library or SDK that fails WCAG 2.2 AA, you as the product provider bear the compliance obligation — audit vendor components and request accessibility conformance reports (ACRs / VPATs).
- **WCAG 2.2 delta from 2.1**: new success criteria in 2.2 include 2.4.11 Focus Not Obscured, 2.4.12 Focus Not Obscured (Enhanced), 2.5.7 Dragging Movements, 2.5.8 Target Size (Minimum), 3.2.6 Consistent Help, 3.3.7 Redundant Entry, and 3.3.8 Accessible Authentication — audit existing products against these before 2.1-only remediation work is considered complete.
- **UK Equality Act / PSBAR**: UK public sector bodies remain under Public Sector Bodies Accessibility Regulations (PSBAR) 2018 (WCAG 2.1 AA); private sector digital services are covered by Equality Act 2010 reasonable adjustments — UK did not transpose EAA, so UK and EU obligations diverge post-Brexit.
- **US ADA Title II (state/local government)**: DOJ's 2024 final rule set WCAG 2.1 AA as the binding web/mobile-app technical standard. A DOJ Interim Final Rule effective 20 April 2026 (Federal Register 2026-07663) extended compliance dates by one year: entities serving a population of 50,000+ now have until 26 April 2027 (was 24 April 2026); entities under 50,000 population and special districts now have until 26 April 2028 (was 24 April 2027). The technical standard itself did not change — still WCAG 2.1 AA, not 2.2. Title II covers state/local government only; Title III (private business) has no DOJ technical-standard rule or fixed deadline — courts apply Title III to websites case by case, with WCAG 2.1/2.2 AA cited as the de facto standard in settlements. Do not imply a private-sector client has a Title-II-style deadline. For full engagement-level detail see [../qa-testing-accessibility/SKILL.md](../qa-testing-accessibility/SKILL.md), which owns the compliance-program view of this rule; this skill only needs the technical-standard fact (WCAG 2.1 AA) to avoid over- or under-building.
- **US Section 508**: federal ICT procurement baseline, incorporates WCAG 2.0 AA by reference via the 2017/2018 refresh (Section508.gov); many federal agencies target 2.1 or 2.2 AA in practice as forward-looking policy — verify the specific agency's current procurement language rather than assuming 2.0 AA is the ceiling.
- **Accessibility overlays are not a compliance strategy in any jurisdiction above** — see `## Accessibility Overlay Warning`. Regulators and courts increasingly treat overlay-only remediation as evidence of bad faith rather than good-faith effort.

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Verify current WCAG, EN 301 549, EAA, browser-support, and tool-maintenance claims before final advice.
- Prefer W3C, WAI, official tool docs, and government or regulator sources.
- If live verification is unavailable, mark standards and regulatory guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

