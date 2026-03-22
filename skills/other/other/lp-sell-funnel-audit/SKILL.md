---
name: lp-sell-funnel-audit
description: Audit a live sales funnel with rendered browser evidence, not DOM inference alone. Verifies mobile and fullscreen booking paths, captures screenshots, critiques stale reviews against the live site, writes a dated sales audit artifact, and updates SELL-08 activation evidence.
operating_mode: AUDIT
related_skills: meta-user-test, lp-channels, startup-loop, tools-ui-breakpoint-sweep
---

# Sell Funnel Audit

Audit a live sales funnel end to end using rendered browser evidence.

This skill exists to prevent a specific failure mode: making high-severity claims from DOM trees, affordance listings, or raw HTML that do not match what users actually see after render.

## When to Use

- A user asks for a sales funnel audit, booking funnel critique, or conversion-path review.
- A prior audit or external review needs verification against the live site.
- SELL-08 activation readiness needs current funnel evidence before paid spend.
- A business has changed booking UX, pricing presentation, room cards, deal routing, or Octorate handoff behavior.

## Relationship to Other Skills

- `meta-user-test`: broad site QA and crawl coverage. Use it for full-site health audits.
- `lp-sell-funnel-audit`: narrow conversion-path audit focused on revenue-critical routes and handoffs.
- `tools-ui-breakpoint-sweep`: responsive defect sweep for selected routes. Use it when layout breakage is the main concern.
- `startup-loop`: consumes this audit as SELL-08 activation evidence.

## Inputs

| Input | Required | Notes |
|---|---|---|
| `--business <BIZ>` | Yes | Example: `BRIK` |
| Primary site URL | Yes | Example: `https://hostel-positano.com/en` |
| Prior review text or artifact | No | If provided, critique it claim-by-claim against live evidence |
| Route scope | No | Default: homepage, deals, dated book page, Octorate handoff |
| Viewport scope | No | Default: `mobile, fullscreen` only |

Default viewport scope for this skill is:
- `mobile`: iPhone-class width with touch enabled
- `fullscreen`: desktop viewport around `1440x900`

Do not add tablet or intermediate breakpoints unless the user requests them.

## Non-Negotiable Rendered Evidence Gate

Before recording any finding above `Low`, complete all of the following:

1. Capture rendered screenshots for each audited surface in both required viewports.
2. Exercise the flow with real navigation and clicks/taps where possible.
3. Confirm that the rendered state matches the claimed issue.

Rules:

- DOM text, affordance trees, HTML source, and network payloads are **supporting evidence only**.
- If a claim is based only on DOM/HTML and not on rendered state, label it `Hypothesis - needs rendered verification`.
- Do not call something `Critical` or `High` until the rendered state is confirmed.
- If rendered evidence contradicts an earlier claim, the rendered evidence wins.
- Wait for the rendered state to settle after hydration, redirects, and primary image/content load before judging the screen.
- Claims about visible prices, sticky CTAs, above-the-fold actions, rate-plan clarity, deal carry-through, or booking-engine summaries always require rendered confirmation.

## Required Audit Scope

Unless the user narrows scope, audit these surfaces:

1. Homepage primary booking entry points
2. Deals or promo page CTA path
3. Dated booking page with room cards and rate-plan controls
4. Booking engine handoff page (for example Octorate)

For each surface, verify:
- visible price state
- CTA labeling and hierarchy
- trust signals
- date/guest persistence
- mobile above-the-fold behavior
- handoff clarity and brand continuity

## Workflow

### 0) Write QA Inventory

Before opening the browser, list:
- the user questions to answer,
- the conversion claims you expect to make,
- the concrete surfaces and actions to verify,
- at least 2 off-happy-path checks.

Minimum off-happy-path checks:
- direct load of a dated booking URL
- click-through from deals/promo path to booking path

### 1) Capture Rendered Evidence First

Open the live site in both required viewports and capture:
- homepage top state
- booking-surface top state
- at least one room-card state
- booking-engine handoff top state

If a prior review is being critiqued, do this step before judging any of its claims.

### 2) Map The Live Funnel

Build the current funnel map from observed behavior:

`Ingress -> intermediate route(s) -> dated booking state -> room/rate selection -> handoff`

Use exact URLs where relevant.

### 3) Validate Or Reject Prior Claims

If a prior review exists, classify each major claim as one of:
- `Validated`
- `Partially valid`
- `Invalid on live site`
- `Stale / superseded`
- `Unverified`

Do not just summarize. Record the specific mismatch between the old claim and the current rendered evidence.

### 4) Write Current Findings

Focus on present-tense issues only.

Use this severity model:
- `Critical`: trust or transaction integrity failure on the core booking path
- `High`: likely conversion blocker or strong trust break with workaround
- `Medium`: material friction or clarity issue
- `Low`: polish or minor messaging issue

### 5) Decide SELL-08 Activation Readiness

The audit must end with one explicit activation decision:
- `Pass`
- `Blocked`

`Blocked` if any unresolved `Critical` or `High` finding exists on the core path in either required viewport.

### 6) Persist The Artifact Into The Sales Loop

Write the audit to:

`docs/business-os/strategy/<BIZ>/sales/YYYY-MM-DD-<business-lower>-sales-funnel-rendered-audit.user.md`

Persist screenshots to:

`docs/business-os/strategy/<BIZ>/sales/artifacts/YYYY-MM-DD-<business-lower>-sales-funnel-rendered-audit/`

If the business already has a standing-registry sales funnel artifact entry, update its path to the new audit so the latest evidence is discoverable by the sales loop.

## Output Contract

### Frontmatter (required)

```yaml
---
Type: Sales-Funnel-Audit
Status: Active
Business: <BIZ>
Date: <YYYY-MM-DD>
Viewport-Scope: mobile, fullscreen
Rendered-Evidence: required
Primary-URL: <https://...>
Activation-Decision: Pass | Blocked
Activation-Blockers-High: <int>
Activation-Blockers-Critical: <int>
Review-trigger: Before SELL-08 paid activation or after any booking funnel / booking-engine change.
---
```

### Body Sections (required order)

1. `# <Title>`
2. `## Scope and evidence`
3. `## Executive verdict`
4. `## Live funnel map`
5. `## Prior review validation`
6. `## Current findings`
7. `## Activation readiness decision`
8. `## Evidence log`
9. `## Next actions`

## Quality Bar

- Every `High` or `Critical` finding has at least one screenshot link.
- Mobile and fullscreen are both covered.
- The audit distinguishes stale claims from current issues.
- The activation decision is explicit and backed by current evidence.
- The artifact is written into the business sales namespace, not left in chat only.
