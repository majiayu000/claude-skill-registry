# Example: PM Sprint From Sales Request To PRD

## Scenario

Sales is pushing a feature request that sounds important, but the scope is still muddy. You want the PM Sprint to turn the request into a first-slice PRD direction instead of a wishlist.

## Prompt

```text
Take this from idea to PRD with the full PM sprint: enterprise prospects keep asking for approval workflows before changes go live. We need to know whether this is a real product gap, what the first version should be, and how to frame success without building a giant admin suite.
```

## Example Output Excerpt

```text
Sprint Summary

1. Discover
- The signal is credible if approval workflow requests cluster around regulated buyers, admin-owned products, or change-risk concerns.
- Evidence required before scoping: lost-deal count tied to approval requirements, top 3 approval use cases, and whether current workarounds happen outside the product.
- Risk to avoid: treating "enterprise requested it" as sufficient proof without separating compliance need from buyer preference.

2. Position
- Primary user: workspace admins responsible for operational control, not everyday end users.
- Core job: prevent risky changes from going live without forcing the team into offline review rituals.
- Product promise: controlled release confidence, not a full governance platform.

3. Prioritize
- Best first slice: one approval gate on publish for high-risk changes, with named approver, approve/reject action, and audit trail.
- Explicit exclusions: multi-step approval chains, conditional routing, SLA escalations, policy builder, and cross-workspace governance.
- Why this slice wins: it solves the strongest trust objection without opening a broad admin-suite surface area.

4. Specify
- PRD scope: publish gate for selected asset types, approval request state, approver notification, approval history, and event instrumentation.
- Out of scope: draft collaboration overhaul, custom roles redesign, and non-publish approvals.
- Key dependency: clear definition of "high-risk change" so the gate does not trigger on trivial edits.

5. Validate
- Hypothesis: a narrow publish-approval flow increases enterprise buyer confidence and reduces manual review workarounds.
- Validation plan: 5 admin interviews on workflow fit, prototype review with 2 recent deals, and implementation sizing before broader commitment.
- Kill signal: if most prospects actually need policy automation or multi-step governance, this first slice is too thin to win.

6. Measure
- Primary metric: share of target enterprise evaluations where approval-gap objection is removed.
- Product metric: publish actions using approval gate per eligible workspace.
- Guardrail: median publish delay should not create broad workflow friction for non-admin teams.
```

## Why This Matters

This example shows the PM Sprint doing the hard PM work: proving the demand signal, narrowing the scope aggressively, and preserving a clean first slice instead of collapsing into "enterprise features."

## Reuse

Reuse this pattern when you need to:

- turn sales pressure into evidence-backed product framing
- protect the team from broad governance or admin-suite sprawl
- produce a PRD-ready first version with explicit exclusions, validation plan, and guardrails
