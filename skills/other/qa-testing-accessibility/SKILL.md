---
name: qa-testing-accessibility
description: "Builds accessibility testing workflows for WCAG 2.2 audits and CI gates. Use when adding axe-core or Lighthouse checks, calibrating gate policy, or planning screen-reader testing."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# QA Testing (Accessibility)

Accessibility testing automation, CI gating, and audit methodology for web and mobile. Use this skill to decide what to automate, what requires manual testing, and how to build a sustainable accessibility quality gate.

Key distinction: `software-ui-ux-design` covers accessible *design*. This skill covers accessible *testing* — tooling, CI gates, screen reader protocols, and conformance evidence.

## Quick Start

1. Add axe-core to existing component or E2E tests to catch common detectable issues early.
2. Establish a baseline before enabling blocking gates on legacy codebases.
3. Set a team-defined CI policy: a common starter is block on critical/serious, warn on moderate, but tune it per product risk and remediation maturity.
4. Plan manual audit for what automation cannot judge reliably: context, usability, cognitive load, and assistive-technology behavior.
5. Run screen-reader verification on critical user flows before release.

## Workflow

1. Gather the target surfaces, WCAG scope, and platform constraints.
2. Cover what automation can reliably detect first.
3. Add manual keyboard and screen-reader checks for critical journeys.
4. Turn findings into CI gates, remediation work, and verification evidence.

## Inputs to Gather

- Target WCAG level: AA (default) or AAA (specific requirements)
- Platforms: web, iOS, Android, or combination
- Assistive technology requirements: screen readers, switch access, voice control
- Existing accessibility tooling and baseline violation count
- Regulatory requirements: ADA Title II (US state/local government — WCAG 2.1 AA technical standard, extended compliance dates), Section 508 (US federal ICT — WCAG 2.0 AA baseline), EN 301 549 (current: V3.2.1/WCAG 2.1; V4.1.1/WCAG 2.2 AA expected ~Oct 2026), European Accessibility Act (EAA) — see `## Regulatory Landscape` for corrected dates and scope; do not assume any single deadline applies to a private US business
- Critical user flows that must be accessible
- Design system or component library status (tested vs untested)

## WCAG 2.2 Automation Boundary

Automation covers only a subset of WCAG 2.2. The exact share varies by product, framework, and tool rule set, so do not treat any percentage as a conformance rule.

| Coverage Type | Examples |
|---------------|----------|
| Reliably automatable | Color contrast, missing alt attributes, missing form labels, heading hierarchy, landmark structure, duplicate IDs, many ARIA validity checks |
| Candidate detection + human verification | Alt-text quality, keyboard usability, touch target adequacy, focus order, live-region behavior |
| Manual only | Cognitive load, reading level, error-prevention UX, consistent navigation, timing adjustments, motion preferences, full screen-reader usability, reflow at high zoom |

See [references/wcag-automation-matrix.md](references/wcag-automation-matrix.md) for criterion-level planning.

## Tool Comparison

| Tool | Best For | False Positive Rate | CI Ready |
|------|----------|---------------------|----------|
| axe-core | Default recommendation — broad rule coverage and mature integrations | Low | Yes |
| Lighthouse | Broader audits (performance + accessibility), good for CI | Low-Medium | Yes |
| Pa11y | CLI-focused CI pipelines | Low | Yes |
| WAVE | Manual browser-based review | N/A | No |
| IBM Equal Access | Additional rule coverage beyond axe | Low | Yes |
| Android Accessibility Scanner | Android native app audits | Low | Partial |
| Xcode Accessibility Inspector | iOS native app audits | Low | Partial |

## Conformance Boundary

- Automated scans and severity labels do not establish WCAG conformance by themselves.
- WCAG conformance claims require combined evidence: automated findings, manual review, and assistive-technology testing on the relevant user journeys.
- Tool severity levels are implementation guidance, not legal or standards-grade conformance verdicts.

## Accessibility Overlays: Do Not Recommend

"Accessibility overlay" or "widget" products (a single JS snippet injected to auto-remediate a
site — e.g. AccessiBe, UserWay, and similar tools) are not a substitute for code-level
remediation and materially increase legal exposure rather than reducing it:

- UsableNet's mid-2025 lawsuit report found 22.6% of H1 2025 US web-accessibility lawsuit
  filings targeted sites that had an overlay installed — overlay presence is increasingly cited
  in complaints as evidence the defendant knew about accessibility obligations but chose the
  cheapest option instead of remediating.
- The FTC fined AccessiBe $1,000,000 (final order approved April 2025) for false, misleading,
  or unsubstantiated advertising claims about WCAG/ADA compliance, and barred the company from
  making compliance claims without evidence.
- Overlays frequently intercept keyboard and focus behavior in ways that conflict with the
  user's own assistive technology, and cannot fix missing semantics, bad reading order, or
  incorrect ARIA in the underlying markup — they layer a script on top of the defect.
- If an existing product already has an overlay installed, treat it as an open risk item in the
  audit, not as a completed accessibility control. Recommend code-level remediation and removal
  of the overlay as part of the plan, not alongside it.

## Prioritizing Fixes: User Impact, Not Violation Count

Violation *count* is a weak signal for triage. Prioritize remediation by:

1. **Whether the barrier is absolute or has a workaround.** A missing form label on the only
   checkout submit button blocks the task completely; a redundant ARIA role on a footer icon is
   an inconvenience. Fix the blocker first even if it is one finding against fifty minor ones
   elsewhere.
2. **Centrality of the flow.** Sign-in, checkout, account recovery, and any flow a user cannot
   route around outrank rarely-visited settings or marketing pages.
3. **Breadth of affected users and devices.** A defect in a shared design-system component (see
   below) or a core layout template affects every page that uses it — fix it once, upstream.

A page with 200 minor violations is lower priority than a page with two critical violations on
a primary conversion path — do not let dashboards that sort by raw count drive the backlog.

## Design-System Leverage

Fixing an accessibility defect once in a shared component (Button, Modal, Form Field, Tabs,
Combobox primitives) remediates every page and flow that uses it — this has far higher ROI than
page-by-page fixes and is usually the highest-leverage first move in a new remediation program.
When starting an accessibility program: audit the design system's core interactive components
first, fix and test them against the ARIA APG pattern for that component type, then re-scan
pages — a large share of page-level findings usually collapse once the shared components are
correct. Component-level automated tests (Storybook a11y addon, `jest-axe`) catch regressions in
these primitives before they propagate back out to every consuming page.

## Web Testing Patterns

- **Component tests**: axe-core via `@axe-core/playwright`, `cypress-axe`, or Storybook `a11y` addon.
- **E2E tests**: inject `@axe-core/playwright` into page-level assertions after navigation.
- **Lighthouse CI**: run `lhci autorun` with accessibility category thresholds.
- **SPA considerations**: re-scan after route changes and dynamic content loads.

See [references/automated-auditing.md](references/automated-auditing.md) for integration code and configuration.

## Mobile Testing Patterns

- **iOS**: Accessibility Inspector for static audits, XCUITest `accessibilityIdentifier` assertions, VoiceOver manual protocol.
- **Android**: Accessibility Scanner for static audits, Espresso `AccessibilityChecks.enable()`, TalkBack manual protocol.

See [references/mobile-accessibility.md](references/mobile-accessibility.md) for detailed workflows.

## CI Integration

| Stage | What to Run | Gate |
|-------|-------------|------|
| PR (component) | axe-core on changed components | Use team policy; common starter is block critical/serious |
| PR (E2E) | axe-core on smoke flows | Use team policy; common starter is block critical/serious |
| Staging deploy | Full-page Lighthouse + axe scan | Common starter: block critical, warn serious/moderate |
| Release | Manual audit of critical flows + screen reader verification | Sign-off required |

Baseline management: for existing codebases, snapshot current violations and gate only on *new* regressions. See [references/ci-accessibility-gates.md](references/ci-accessibility-gates.md).

## Three Tiers of Testing: Automated, Manual Expert, Real AT Users

Each tier catches defects the others miss — none is a substitute for the others on a
compliance-relevant or high-traffic critical flow:

| Tier | Who | Catches | Misses |
|------|-----|---------|--------|
| Automated | CI (axe-core, Lighthouse, jsx-a11y) | Structural/programmatic defects reliably, at zero marginal cost per run | Anything requiring judgment about meaning, sufficiency, or usability |
| Manual expert | Sighted engineer/QA running keyboard + screen-reader protocol | Flow-level defects, focus management, ARIA correctness in context | Real-world friction — expert testers know the workarounds a first-time AT user does not |
| Real AT users | Actual disabled users, their own devices/AT/versions/speed | Highest-fidelity signal — muscle-memory shortcuts, unfamiliar error recovery, device-specific quirks | Nothing structural, but is the slowest and highest-cost tier to run |

Judgment: automated scanning plus an in-house expert running a checklist is necessary but not
sufficient for confidence on a critical or regulated flow. Before a compliance-relevant release
(EAA, ADA Title II, VPAT/ACR sign-off) or a redesign of a core flow, get at least one round of
testing with actual assistive-technology users — recruit through accessibility user-research
panels, disability employee resource groups, or existing screen-reader-using customers, and
budget to compensate them as paid research participants, not as a favor. (Unverified as of
2026-07-11: specific vendor names and pricing for AT-user testing panels change; verify current
options before committing budget.)

## Screen Reader Testing Protocol

Test critical flows with at least one screen reader per target platform:

| Platform | Screen Reader | When |
|----------|---------------|------|
| macOS/iOS | VoiceOver | Default for Apple targets |
| Windows | NVDA (free) or JAWS | Default for Windows web |
| Android | TalkBack | Default for Android targets |

What to verify: landmark announcements, heading navigation, form label association, error announcements, dynamic content updates (live regions), modal/dialog focus management, custom widget interaction.

Market reality (WebAIM Screen Reader User Survey #10, fielded Dec 2023–Jan 2024, 1,539
respondents — the latest published edition; Survey #11 was in the field as of 2026-07-11 with
results not yet published): on desktop, JAWS (41%) and NVDA (38%) are the leading *primary*
screen readers, with NVDA the most-*commonly*-used overall (65.6%) ahead of JAWS (60.5%);
VoiceOver is used by 8.2% as primary desktop reader (up from 5.5% in 2021) but dominates mobile
(70.6% vs TalkBack's 34.6%). JAWS leads NVDA in North America specifically; NVDA leads
elsewhere. Test NVDA and JAWS both for enterprise/US-heavy audiences — do not treat NVDA alone
as sufficient Windows coverage.

See [references/screen-reader-testing.md](references/screen-reader-testing.md) for commands and checklists.

## Keyboard Navigation Testing

- Tab order matches visual/logical order
- Focus indicator is visible on all interactive elements
- Skip navigation link present and functional
- Modals trap focus correctly and return focus on close
- Custom components follow ARIA Authoring Practices Guide (APG) keyboard patterns

See [references/keyboard-navigation.md](references/keyboard-navigation.md) for verification steps.

## Quick Reference

| What to Test | Tool / Method | CI Stage | Automation |
|--------------|---------------|----------|------------|
| Color contrast | axe-core | PR gate | Full |
| Missing alt text | axe-core | PR gate | Full |
| Form labels | axe-core | PR gate | Full |
| Heading hierarchy | axe-core | PR gate | Full |
| ARIA validity | axe-core | PR gate | Full |
| Keyboard navigation | axe-core + manual | PR + release | Partial |
| Touch target size | axe-core + manual | PR + release | Partial |
| Screen reader flow | Manual (VoiceOver/NVDA/TalkBack) | Release | Manual |
| Cognitive load | Manual review | Release | Manual |
| Reflow at 400% zoom | Manual browser test | Release | Manual |

## Decision Tree

```text
Accessibility need:
├─ New project?
│   └─ axe-core in component tests + Lighthouse CI + design review
├─ Existing project with violations?
│   └─ Scan baseline → prioritize critical → gate new regressions
├─ Compliance requirement (ADA Title II / Section 508 / EN 301 549 / EAA)?
│   └─ Automated gates + manual audit + real-AT-user verification + VPAT/ACR documentation; see Regulatory Landscape for scope and dates
├─ Mobile app?
│   └─ Platform accessibility scanner + screen reader testing
├─ Design system / component library?
│   └─ Storybook axe addon + ARIA APG pattern review
└─ Pre-release?
    └─ Full automated scan + manual audit of critical flows
```

## Regulatory Landscape (2026)

**WCAG 2.2** has been a W3C Recommendation since 5 October 2023 (the 4.1.1 Parsing success
criterion was removed in the December 2024 update). It is the current normative baseline for
every regulation below — target WCAG 2.2 AA by default regardless of which regulation applies.

**WCAG 3.0 status:** still a W3C Working Draft (latest: March 2026; next draft expected
~September 2026). Candidate Recommendation is not expected before Q4 2027; W3C Recommendation
not before ~late 2028, with the AGWG co-chair targeting "towards the end of 2029." **WCAG 2.2 AA
is the operative compliance target for all work now.** WCAG 3.0 will not supersede 2.2
immediately on finalizing — both will coexist for years, and 3.0 uses an outcomes-based,
graded (Bronze/Silver/Gold) conformance model rather than 2.2's binary pass/fail. Track it; do
not gate against a draft.

**ADA Title II (US state/local government)** — do not cite the original 2024 dates without the
2026 extension:
- The DOJ's final rule (adopted 24 April 2024) set WCAG 2.1 Level AA as the binding technical
  standard for the web content and mobile apps of state and local government entities.
- Original compliance dates were 24 April 2026 (entities serving a population of 50,000+) and
  24 April 2027 (population under 50,000, or any special district government).
- A DOJ Interim Final Rule, effective 20 April 2026, **extended both dates by one year**:
  26 April 2027 for population 50,000+; 26 April 2028 for population under 50,000/special
  districts. Public comments on the extension closed 22 June 2026 — treat the new dates as
  current but not necessarily final, and re-check before citing them in a compliance plan.
- Scope is Title II only (state/local government). **Title III (private businesses/public
  accommodations) has no DOJ rule specifying a technical standard or deadline** — courts still
  apply Title III to websites case by case, and WCAG 2.1/2.2 AA is the de facto standard cited
  in settlements, but there is no promulgated federal regulation or fixed date for private
  companies. Do not tell a private-sector client they have an "ADA deadline" in the Title-II sense.

**Section 508 (US federal ICT)**: the binding technical standard is still **WCAG 2.0 Level AA**
(2017 refresh) — it has not been updated to reference WCAG 2.1 or 2.2. Recommend targeting
2.2 AA anyway as forward cover, but do not claim 2.2 is the current legal Section 508 baseline.

**EN 301 549 (EU harmonized ICT accessibility standard)**: current binding version is **V3.2.1**
(March 2021, WCAG 2.1 AA basis) — still normative for the EAA and the Web Accessibility
Directive. V4.1.1 (incorporating WCAG 2.2 AA) had a public-review draft (v4.1.0) released
November 2025; publication in the Official Journal of the EU is expected around **October
2026** (unverified as of 2026-07-11 — ETSI/EU publication timelines have slipped before; verify
before treating this as a hard date). Until V4.1.1 is formally adopted, audit against WCAG 2.2
AA now to avoid a re-audit gap later — the five criteria WCAG 2.2 added over 2.1 (2.4.11, 2.5.7,
2.5.8, 3.3.7, 3.3.8) will be required once V4.1.1 lands.

**EAA (European Accessibility Act)** timing — don't treat as a past deadline: enforcement has
been **active since 28 June 2025** for new and substantially-modified in-scope services
(enforcement is underway, not theoretical); **existing services have a transitional period to
28 June 2030**. Native mobile apps are in scope as software via EN 301 549. Treat EAA as an
ongoing obligation for any new or updated EU-market product — WCAG 2.1/2.2 AA + EN 301 549
conformance, plus an accessibility statement, throughout the transition, not a one-time
June-2025 gate.

## Do / Avoid

### Do

- Start with axe-core as the default cross-framework scanner
- Treat CI severity thresholds as team policy, not as a WCAG verdict
- Test with real assistive technology for critical flows, including sessions with actual
  disabled AT users before a compliance-relevant or core-flow release
- Fix shared design-system components first — highest leverage per hour spent
- Include accessibility in definition of done
- Use ARIA Authoring Practices Guide (APG) for custom component keyboard patterns
- Combine multiple automated tools for broader rule coverage
- Prioritize by user impact (blocker vs. workaround, flow centrality) over raw violation count

### Avoid

- Treating automated scanning as complete coverage or as proof of WCAG conformance
- Recommending or shipping an accessibility overlay/widget as a substitute for code-level
  remediation — it does not confer conformance and correlates with higher lawsuit rates
- Blocking all PRs on all existing violations (use baselines)
- Using only one automated tool without manual testing
- Testing accessibility only before release (shift left)
- Using ARIA when native HTML semantics work (`<button>` not `<div role="button">`)
- Relying on color alone to convey information
- Sorting remediation backlogs by violation count alone instead of user impact

## ASCII Flow

```text
Accessibility testing request
  -> Define surfaces, WCAG target, platforms, and critical user flows
  -> Add automated checks for detectable issues and establish baseline
  -> Tune CI policy by severity, risk, and remediation maturity
  -> Manually test keyboard, focus, screen reader, cognition, and mobile AT
  -> Record conformance evidence, exceptions, owners, and retest dates
  -> Keep accessibility gates in regular PR and release workflows
```

## Navigation

- `## Workflow`, `## WCAG 2.2 Automation Coverage`, and `## Decision Tree` for the baseline sequence
- `## Resources` and `## Templates` for deeper materials
- `## Related Skills` for cross-platform handoffs

## Resources

| Resource | Purpose |
|----------|---------|
| [references/automated-auditing.md](references/automated-auditing.md) | axe-core, Lighthouse, Pa11y integration and configuration |
| [references/screen-reader-testing.md](references/screen-reader-testing.md) | VoiceOver, NVDA, TalkBack testing protocols |
| [references/wcag-automation-matrix.md](references/wcag-automation-matrix.md) | WCAG 2.2 AA criteria mapped to automation coverage |
| [references/ci-accessibility-gates.md](references/ci-accessibility-gates.md) | CI gate design, baselines, and severity mapping |
| [references/cognitive-accessibility.md](references/cognitive-accessibility.md) | WCAG 2.2 cognitive criteria (3.3.7, 3.3.8, 2.4.11), reading-level checks, COGA guidance |
| [references/eslint-jsx-a11y-integration.md](references/eslint-jsx-a11y-integration.md) | eslint-plugin-jsx-a11y wiring, custom rule set, CI gate with --max-warnings=0 |
| [references/mobile-accessibility.md](references/mobile-accessibility.md) | iOS and Android accessibility testing patterns |
| [references/keyboard-navigation.md](references/keyboard-navigation.md) | Keyboard testing and ARIA APG patterns |
| [data/sources.json](data/sources.json) | Curated external sources |

## Scripts

| Script | Purpose |
|--------|---------|
| [scripts/generate-a11y-baseline.ts](scripts/generate-a11y-baseline.ts) | Playwright + axe-core baseline generator — run with `npx tsx scripts/generate-a11y-baseline.ts` |
| [scripts/README.md](scripts/README.md) | Setup and usage guide for all scripts |

## Templates

| Template | Purpose |
|----------|---------|
| [assets/template-accessibility-audit.md](assets/template-accessibility-audit.md) | Accessibility audit scope, findings, and remediation plan |
| [assets/template-accessibility-ci-config.md](assets/template-accessibility-ci-config.md) | Example CI configurations for axe-core and Lighthouse gates |
| [assets/template-screen-reader-checklist.md](assets/template-screen-reader-checklist.md) | Per-flow screen reader testing checklist |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [software-ui-ux-design](../software-ui-ux-design/SKILL.md) | Accessible design and WCAG 2.2 design patterns |
| [qa-testing-strategy](../qa-testing-strategy/SKILL.md) | Risk-based test strategy and coverage planning |
| [qa-testing-playwright](../qa-testing-playwright/SKILL.md) | E2E web testing with accessibility assertions |
| [qa-testing-android](../qa-testing-android/SKILL.md) | Android accessibility checks with Espresso |
| [qa-testing-ios](../qa-testing-ios/SKILL.md) | iOS accessibility testing with XCTest |
| [qa-testing-mobile](../qa-testing-mobile/SKILL.md) | Cross-platform mobile accessibility |
| [software-frontend](../software-frontend/SKILL.md) | Frontend development and semantic HTML |

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search or web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

