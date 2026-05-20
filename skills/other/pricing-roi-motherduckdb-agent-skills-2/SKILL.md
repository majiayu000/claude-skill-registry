---
name: pricing-roi
description: Explain MotherDuck pricing and ROI tradeoffs. Use when an economic_buyer, technical_owner, or analytics_lead is asking about spend, budget guardrails, workload cost drivers, plan fit, or whether MotherDuck is worth adopting.
license: MIT
---

# Pricing and ROI

Use this skill when the user is asking whether MotherDuck is financially sensible for their workload, team, or project. This is a workflow skill focused on cost framing, not implementation detail.

## Source Of Truth

- Always verify current numbers, plan limits, and feature entitlements against the live public pricing page before answering.
- If the MotherDuck MCP `ask_docs_question` feature is available, use it first for pricing-related documentation lookups.
- Use the live pricing, Hypertenancy, and Trust & Security pages for exact commercial framing.

## Default Posture

- Do not hardcode pricing numbers unless you have verified them in the current turn.
- Separate storage, compute, and operational complexity in every answer.
- Map workload shape to cost shape before comparing vendors or plans.
- Treat many pricing questions as risk, predictability, or procurement questions rather than purely technical ones.

## Workflow

1. Identify the workload shape, team size, and comparison baseline.
2. Determine whether the real concern is raw spend, predictability, procurement, or operational overhead.
3. Map the workload to MotherDuck cost buckets and plan posture.
4. Frame ROI in terms of systems replaced, complexity removed, and faster delivery.
5. Call out what still needs live pricing-page or sales confirmation.

## Open Next

- `references/PRICING_ROI_PLAYBOOK.md` for workload-to-cost mapping, publicly safe talking points, ROI framing, and what not to promise

## Related Skills

- `connect` when the pricing discussion depends on connection-path choices
- `security-governance` when compliance, residency, or commercial controls affect ROI
- `build-cfa-app` and `build-dashboard` when the economics depend on the application architecture
