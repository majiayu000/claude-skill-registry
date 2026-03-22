---
name: lp-onboarding-audit
description: Audit an app's onboarding flow against the "Onboarding Done Right" checklist. Customizes the generic checklist for the app's purpose and audience, then audits actual code using lp-do-fact-find's Outcome A process. Produces an analysis-ready brief.
operating_mode: EXECUTE
---

# Onboarding Audit

Audit an app's onboarding experience against the universal "Onboarding Done Right" checklist (sections A–I). Customizes the checklist for the app's business context, audits actual code, and produces a fact-find brief that feeds into `/lp-do-analysis` before planning.

## When to Use

- **DO (`/lp-do-fact-find`)**: When a startup loop card targets onboarding improvement
- **L2→L3 readiness**: When a business is launching and onboarding is a critical activation lever
- **Standalone**: Operator invokes `/lp-onboarding-audit <BIZ>` at any time to audit an existing onboarding flow
- **Post-launch**: Periodic re-audit to check regression or measure improvement

## Operating Mode

**READ + CUSTOMIZE + AUDIT + REPORT**

**Allowed:**
- Read generic checklist from `.claude/skills/_shared/onboarding-done-right-checklist.md`
- Read business strategy plans, brand language docs, businesses.json
- Read onboarding component code, routes, layouts, analytics, test files
- Trace flow logic and data contracts
- Run read-only commands (grep, find, file listing)
- Create/update fact-find brief at `docs/plans/<app>-onboarding-audit-fact-find.md`
- Create/update Business OS card and stage doc via agent API

**Not Allowed:**
- Code changes or refactors (use `/lp-do-build` after planning)
- Running tests (audit is static analysis + code reading)
- User research or live user testing (audit is code-only)
- Marking items Pass without citing evidence

## Inputs

| Source | Path | Required |
|--------|------|----------|
| Business unit code | `<BIZ>` (e.g., `BRIK`, `HEAD`, `PET`) | Yes |
| Strategy plan | `docs/business-os/strategy/<BIZ>/plan.user.md` | Yes |
| Business registry | `docs/business-os/strategy/businesses.json` | Yes |
| Generic checklist | `.claude/skills/_shared/onboarding-done-right-checklist.md` | Yes |
| Brand language | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | No — enhances customization |
| App name | `<app>` argument (e.g., `prime`) | No — if BIZ has multiple apps |
| Scope limit | `--scope A,B,E` argument | No — audit specific sections only |

## Workflow

### Step 1: Resolve Business Context

**Goal:** Understand the business, app type, audience, and brand before customizing the checklist.

1. Read `businesses.json` to map BIZ → app list and theme
2. Read strategy plan for: business model, target audience, app purpose, maturity stage
3. Read brand language doc (if exists) for: audience definition, personality, device context
4. If user specified an app, audit that one; otherwise audit all apps for that business
5. **Classify app type** as one of:
   - Free content app / Free guest companion / Paid app / Freemium
   - Enterprise/B2B / Admin/internal tool / Booking/commerce / Social/community
6. Document the classification — it drives N/A decisions in Step 2

**Outputs for brief:**
- Business Unit, App name(s), App type classification
- Target audience summary, Device context, Business model

### Step 2: Customize the Checklist

**Goal:** Make the generic checklist specific to this app's purpose.

1. Read `.claude/skills/_shared/onboarding-done-right-checklist.md`
2. For each section A–I:
   - **Check applicability** using the "App Type N/A Guidance" table
   - If N/A: document WHY (e.g., "Section F (Paywall) → N/A: Prime is a free guest companion app")
   - If applicable: write 1–2 sentences translating generic items into this app's context
3. Examples of app-specific interpretation:
   - Section A (Value-first) for Prime: "Guest sees their personalized arrival plan within 2 screens of starting onboarding"
   - Section B (Friction) for Prime: "Guest profile capture must justify every field — ETA is critical, room preferences are deferrable"
   - Section G (Analytics) for a pre-L2 app: "Likely missing entirely — flag as a prerequisite gap"

**Outputs for brief:**
- Customized checklist with N/A reasoning and app-specific interpretation per section

### Step 3: Audit Actual Onboarding Code

**Goal:** Scan the codebase using lp-do-fact-find's evidence audit methodology.

1. **Locate onboarding entry points:**
   - Search for: `onboard*`, `welcome*`, `setup*`, `guided*`, `activation*` in component names and routes
   - Common paths: `apps/<app>/src/components/onboarding/`, `apps/<app>/src/app/onboarding/`
   - Read layout files, flow components, step components

2. **Trace flow logic:**
   - Number of steps, conditional branching, skip/exit paths
   - Data collected at each step (fields, schemas)
   - Where data is persisted (API calls, local storage, state)

3. **Scan analytics instrumentation:**
   - Search for `track`, `record`, `analytics`, `event`, `log` in onboarding components
   - Check: per-step events, completion event, drop-off tracking, error logging
   - Note any analytics SDK setup (Mixpanel, Amplitude, PostHog, etc.)

4. **Check accessibility:**
   - Grep for `aria-`, `tabIndex`, `role=`, `focus()`, `label`, `sr-only`
   - Check touch target sizes in styles
   - Look for focus management between steps

5. **Check error handling:**
   - Network failure states, retry logic, validation UX
   - Loading states (skeleton loaders vs spinners vs nothing)
   - Timeout handling, session expiry during onboarding

6. **Review test coverage:**
   - Locate test files for onboarding components
   - Note what's covered vs gaps
   - Check for integration/E2E tests of the full flow

**If no onboarding flow is found:** STOP. Report that the app has no onboarding and recommend building one. Do not fabricate audit results.

**Outputs for brief:**
- Component inventory (all onboarding-related file paths)
- Flow map (steps → data → persistence → analytics)
- Test coverage summary

### Step 4: Score Each Section

**Goal:** Produce a Pass/Fail/Partial/N/A verdict for each checklist item with evidence.

**Scoring rules:**
- **Pass:** Implemented and meets practice — cite component path + line number
- **Fail:** Missing, broken, or anti-pattern — explain what's wrong
- **Partial:** Implemented with gaps — specify what's missing
- **N/A:** Not applicable — reasoning from Step 2

**Section-level verdict:**
- >80% of applicable items Pass → **Section passes**
- >50% of applicable items Fail → **Section fails** (requires immediate attention)
- 50–80% Pass → **Section needs improvement**

**Must-have risk items** (from the scoring rubric):
- Aha moment not reached quickly → automatic risk flag
- Sign-up before value when not required → automatic risk flag
- No onboarding funnel analytics → automatic risk flag
- No paywall test strategy for paid apps → automatic risk flag

### Step 5: Produce Fact-Find Brief

**Goal:** Write an analysis-ready brief using `lp-do-fact-find` Outcome A format.

**Output path:**
```
docs/plans/<app>-onboarding-audit-fact-find.md
```

**Frontmatter (required):**
```yaml
---
Type: Fact-Find
Outcome: Planning
Status: <Ready-for-analysis | Needs-input>
Domain: UI
Workstream: Engineering
Created: <YYYY-MM-DD>
Last-updated: <YYYY-MM-DD>
Feature-Slug: <app>-onboarding-audit
Deliverable-Type: <code-change | multi-deliverable>
Execution-Track: <code | mixed>
Primary-Execution-Skill: lp-do-build
Supporting-Skills: lp-design-system
Related-Analysis: docs/plans/<app>-onboarding-audit-analysis.md
Business-OS-Integration: on
Business-Unit: <BIZ>
---
```

**Brief sections (in order):**

1. **Scope** — Summary, goals, non-goals, constraints
2. **App Context** — Business unit, app type, audience, device, business model
3. **Evidence Audit** — Component inventory, flow map, data contracts, analytics coverage, test landscape
4. **Customized Checklist** — Section-by-section scores with per-item evidence:
   ```
   ### Section A: Value-first flow
   **App-specific interpretation:** <1-2 sentences>
   **Verdict:** Pass | Fail | Needs-Improvement | N/A

   - [x] A.1 Core promise is benefit-led — **Pass** — `GuestProfileStep.tsx:15` shows "Help us prepare your perfect stay"
   - [ ] A.2 Aha moment designed — **Fail** — No meaningful result shown; flow ends at generic "Welcome" screen
   ...
   ```
5. **Findings Summary** — Sections passing / failing / needing improvement / N/A
6. **Risks** — Table with top risks, likelihood, impact, mitigation
7. **Recommended Fixes** — Prioritized as P0 (critical) / P1 (important) / P2 (polish), each with component path and expected impact
8. **Confidence Inputs** — Implementation, Approach, Impact, Delivery-Readiness, Testability scores (0–100) for `/lp-do-analysis`
9. **Suggested Task Seeds** — Non-binding task ideas for `/lp-do-analysis` and later `/lp-do-plan`
10. **Analysis Readiness** — Status + blocking items if any

### Step 6: Report Completion

**Completion message format:**

```
Onboarding audit complete for <app> (<BIZ>).

**Audit summary:**
- Sections audited: <N> | Passing: <N> | Failing: <N> | Needs improvement: <N> | N/A: <N>

**Must-have risk check:**
- Aha moment: <Pass | FAIL>
- Sign-up before value: <Pass | FAIL | N/A>
- Funnel analytics: <Pass | FAIL>
- Paywall test strategy: <Pass | FAIL | N/A>

**Top 3 risks:**
1. <Risk 1> (Severity: High | Medium | Low)
2. <Risk 2>
3. <Risk 3>

**Recommended fixes:** P0: <N> | P1: <N> | P2: <N>

**Brief:** `docs/plans/<app>-onboarding-audit-fact-find.md`
**Status:** Ready-for-analysis | Needs-input
**Next:** `/lp-do-analysis <app>-onboarding-audit`
```

## Quality Checks

- [ ] Business context resolved (strategy plan read, app type classified)
- [ ] Brand language read (if exists) for audience and voice context
- [ ] Checklist customized (N/A marked with reasoning, app-specific interpretation per section)
- [ ] All onboarding components found and read (not guessed)
- [ ] Every Pass/Fail cites component path + line number (no verdicts without evidence)
- [ ] Every N/A section has documented reasoning
- [ ] Must-have risk items checked (A: Aha, B: sign-up gate, G: analytics, F: paywall)
- [ ] At least one risk identified (no "everything is perfect" audits)
- [ ] Fact-find brief has all required lp-do-fact-find Outcome A sections
- [ ] Confidence inputs provided (5 dimensions, 0–100)
- [ ] Analysis readiness status set
- [ ] Brief saved at correct path with correct frontmatter

## Integration

- **Consumed by**: `/lp-do-analysis` (selects the right onboarding improvement approach before tasking)
- **Feeds into**: `/lp-do-plan` and then `/lp-do-build`
- **References**: `.claude/skills/_shared/onboarding-done-right-checklist.md` (generic checklist)
- **Loop position**: DO (`/lp-do-fact-find`) — specialized fact-find for onboarding audits
- **Trigger conditions**:
  - Card targets onboarding improvement
  - Business at L2→L3 transition (launch readiness)
  - Operator invokes manually at any time
- **Business OS sync**: Creates card + fact-find stage doc when `Business-Unit` is present

## Red Flags (Invalid Run)

1. **No onboarding found:** If the app has no discoverable onboarding flow, STOP and report. Do not fabricate results.
2. **Business context missing:** If strategy plan doesn't exist and context can't be inferred, STOP and ask user to provide it.
3. **Scoring without evidence:** Every Pass must cite a file path. If you can't find evidence, mark as Fail or Partial, never Pass.
4. **N/A without reasoning:** Every N/A must explain why. "Not applicable" alone is not acceptable.
5. **Zero risks identified:** Every audit must surface at least one risk. If everything genuinely passes, flag the must-have items as the minimum verification.

## Example Invocation

```
/lp-onboarding-audit BRIK
/lp-onboarding-audit BRIK prime
/lp-onboarding-audit BRIK prime --scope A,B,G
```
