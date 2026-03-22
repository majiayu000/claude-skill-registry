---
name: create-metrics-framework
description: Define a North Star metric, input metrics, and guardrail metrics when the user asks to create a metrics framework, define KPIs, or set up measurement
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[product area or business goal to build metrics around]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: metrics, measurement, kpi
---

# Create Metrics Framework

## Overview

Build a metrics framework combining the North Star Framework (Amplitude), AARRR Pirate Metrics, and HEART Framework (Google). Defines one North Star metric, the input metrics that drive it, and guardrail metrics that prevent gaming. Gives the team a shared definition of success.

## Workflow

1. **Read product context** -- Scan `.chalk/docs/product/` for the product profile, PRDs with success metrics, JTBD docs, and any existing metrics definitions. Understand what the product does and who it serves before defining metrics.

2. **Parse scope** -- Extract from `$ARGUMENTS` the product area or business goal. If unspecified, build a company-level metrics framework using the product profile.

3. **Determine the next file number** -- Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

4. **Define the North Star metric** -- Identify the single metric that best captures the core value the product delivers to users. It must be: measurable, actionable by the team, a leading indicator of revenue, and reflective of user value (not just business extraction).

5. **Map input metrics** -- Identify 3-5 input metrics that drive the North Star. Use the AARRR framework as a lens: Acquisition (how users find you), Activation (first value moment), Retention (users come back), Revenue (users pay), Referral (users bring others). Not all stages need a metric -- pick the ones that matter most.

6. **Apply the HEART framework** -- For key user journeys, consider: Happiness (satisfaction), Engagement (usage depth), Adoption (new feature uptake), Retention (continued use), Task success (completion rate). Use this to fill gaps the AARRR lens missed.

7. **Set guardrail metrics** -- Define 2-3 metrics that must NOT degrade while optimizing the North Star. These prevent gaming (e.g., optimizing signups by removing friction could degrade activation quality).

8. **Write the file** -- Save to `.chalk/docs/product/<n>_metrics_framework.md`.

9. **Confirm** -- Share the file path and highlight which metrics likely need instrumentation work before they can be measured.

## Output

- **File**: `.chalk/docs/product/<n>_metrics_framework.md`
- **Format**: Plain markdown with North Star definition, input metrics table, and guardrail metrics
- **First line**: `# Metrics Framework: <Product Area>`

## Anti-patterns

- **Vanity metrics as North Star** -- Page views, total signups, or app downloads do not reflect user value. The North Star must measure value delivered, not volume collected.
- **Too many metrics** -- If everything is a key metric, nothing is. One North Star, 3-5 inputs, 2-3 guardrails. That is the budget.
- **No guardrails** -- Without guardrails, teams will optimize the North Star at the expense of something important. Always define what must not break.
- **Unmeasurable metrics** -- Every metric must be instrumentable with current or near-term tooling. If you cannot measure it, it is not a metric -- it is a wish.
- **Lagging-only indicators** -- Revenue and churn are important but slow to move. Include leading indicators (activation rate, feature adoption) that predict future outcomes.
