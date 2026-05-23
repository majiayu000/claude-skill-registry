---
name: "product-led-sales"
description: "Create a Product-Led Sales Motion Pack (PQL/PQA definition, usage-signal spec + routing/SLA, sales outreach playbook, instrumentation plan, and pilot/scale plan). Use for product-led sales, sales-assist, PLG-to-sales handoffs, and converting self-serve usage into sales opportunities. Category: Sales & GTM."
---

# Product-Led Sales

## Scope

**Covers**
- Designing a **product-led sales (PLS)** motion: converting self-serve usage into a sales opportunity that can close larger contracts
- Defining **product-qualified** entities (PQL/PQA), signals, thresholds, scoring, and routing rules
- Designing the sales handoff workflow (alerts, SLAs, dispositions) and a Product↔Sales feedback loop
- Creating a usage-triggered outreach kit (helpful, compliant, not “creepy”)
- Planning instrumentation, reporting, and a pilot-to-scale rollout

**When to use**
- “We’re PLG/self-serve, but we want to add sales without breaking the low-touch funnel.”
- “Define PQLs/PQAs and the product signals that should trigger outreach.”
- “Create a product-led sales playbook for sales to act on usage signals.”
- “Sales says MQLs are low quality—build a product-qualified pipeline instead.”
- “Design a PLS pilot (routing + SLAs + measurement) before scaling.”

**When NOT to use**
- You don’t have meaningful activation or self-serve usage yet (fix onboarding/activation first)
- You want a purely enterprise, relationship-led motion with minimal product usage signals (use `enterprise-sales`)
- You need ICP/positioning or pricing/packaging from scratch (do that first, then return)
- You want spammy outreach, deception, or dark patterns (not supported)
- You need legal/privacy/security advice or production data/CRM implementation (coordinate with qualified experts)

## Inputs

**Minimum required**
- Product + model: freemium/trial, typical onboarding path, who uses vs who buys
- ICP/segments: target roles + company types + ACV bands (and which segment is in scope for PLS)
- Objective: conversion to paid, expansion, ACV lift, pipeline creation (pick 1 primary)
- Current funnel baseline: activation rate, trial-to-paid, expansion rate (even rough)
- Usage data reality: what events/attributes exist, and whether you can map users → accounts
- Sales capacity + workflow: SDR/AE/CS roles, SLAs, and where activity is logged (CRM)
- Constraints: regions/compliance, “don’t use these signals,” messaging tone/brand rules

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns in **Assumptions & unknowns** plus a short **Validation plan**.

## Outputs (deliverables)

Produce a **Product-Led Sales Motion Pack** in Markdown (in-chat; or as files if requested):

1) **Context + goal snapshot** (segment, objective, success metrics, constraints)
2) **PLS funnel + ownership map** (stages, intervention points, RACI, SLAs)
3) **PQL/PQA definition + signal spec** (signals table, thresholds/scoring, false-positive controls)
4) **Routing + workflow spec** (alerts, assignment rules, CRM fields, dispositions, feedback loop)
5) **Usage-triggered outreach kit** (email templates + call opener + follow-up rules)
6) **Instrumentation + reporting plan** (tracking plan, dashboards, leading indicators)
7) **Pilot + scale plan** (timeline, experiment design, rollout guardrails)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Intake + readiness gate (PLS is a layer, not a substitute)
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the primary objective and target segment(s). Run a readiness gate: do you have activation/usage depth + identity/account mapping to create reliable signals? Capture constraints (sales capacity, SLA expectations, privacy/compliance).
- **Outputs:** Context snapshot + readiness verdict (Ready / Needs prerequisites) + assumptions/unknowns.
- **Checks:** Objective is measurable; segment is explicit; prerequisites and constraints are documented.

### 2) Map the PLS funnel and decide where sales intervenes
- **Inputs:** Current PLG funnel, user journey, pricing/packaging, sales coverage model.
- **Actions:** Map stages from first value → sustained usage → qualification → sales assist → purchase/expansion → onboarding. Pick intervention points where a human can increase deal size or reduce time-to-value, and define guardrails to keep a low-touch path intact.
- **Outputs:** PLS funnel + intervention points + guardrails + ownership map (RACI).
- **Checks:** Low-touch conversion path remains viable; ownership is explicit at every stage.

### 3) Choose the qualified unit (PQL vs PQA) and write the definition
- **Inputs:** Buyer/user model, account structure, pricing driver (seats/usage).
- **Actions:** Decide the qualified unit:
  - **PQL** for user-led buying (a user’s intent/need)
  - **PQA** for account-led expansion (account adoption/coordination)
  Write a crisp definition: required signals + thresholds + exclusions.
- **Outputs:** PQL/PQA definition (inclusion/exclusion + examples).
- **Checks:** Definition is computable from data, not vibes; includes anti-gaming/false-positive controls.

### 4) Build the signal spec, scoring, and routing/SLA rules
- **Inputs:** Available events/properties, identity graph, sales capacity, CRM workflow.
- **Actions:** Create a signal catalog (activation/aha, depth, breadth, integrations, invites, admin actions, billing intent). Set thresholds and scoring, define routing (who gets alerted, when), and specify a triage/holdout path for ambiguous signals.
- **Outputs:** Signal spec table + scoring model + routing + SLA + disposition taxonomy.
- **Checks:** Signals map to intent and value potential; routing matches capacity; false positives are addressed.

### 5) Design the sales workflow and Product↔Sales feedback loop
- **Inputs:** Sales roles, CRM fields, enablement constraints.
- **Actions:** Define the operational workflow: alert delivery, assignment rules, what context reps see, required actions, logging, dispositions, and a weekly tuning loop with Product/RevOps to improve signals and messaging.
- **Outputs:** Workflow spec + RACI + weekly review agenda.
- **Checks:** Every alert has a next best action; outcomes are measurable and feed back into tuning.

### 6) Create the usage-triggered outreach kit (helpful, not creepy)
- **Inputs:** Use case narrative, common objections, signal context.
- **Actions:** Write email templates that reference helpful context (“noticed you’re setting up X”) without surveillance language. Provide variants for early vs high intent. Add a call opener + discovery prompts anchored to the user’s likely goal.
- **Outputs:** Outreach kit (emails + call opener + follow-up rules).
- **Checks:** One clear ask per message; tone is respectful/compliant; personalization uses only approved signals.

### 7) Pilot, measure, iterate, and scale
- **Inputs:** Draft pack; baseline metrics; pilot constraints.
- **Actions:** Propose a pilot (segment + duration + sample size), define success metrics and leading indicators (time-to-first-touch, meeting rate, conversion, expansion, retention). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Finalize with **Risks / Open questions / Next steps** and a rollout plan.
- **Outputs:** Final Product-Led Sales Motion Pack + pilot/measurement plan.
- **Checks:** Pilot is bounded; dashboards are specified; iteration cadence is scheduled and owned.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (trial → sales assist):**  
“Use `product-led-sales`. We’re a B2B analytics tool with a 14-day trial. We get lots of signups but low trial-to-paid. We have usage events and can map users to companies via email domain. Sales: 2 SDRs + 2 AEs. Output: a Product-Led Sales Motion Pack with a PQL definition, routing rules, outreach emails, and a 4-week pilot plan.”

**Example 2 (expansion via PQA):**  
“Use `product-led-sales`. We’re seat-based SaaS. Teams start self-serve at $20/seat but we want to land-and-expand into 100+ seat contracts. We can detect invites, admin setup, and integration activation. Output: a Motion Pack that defines PQAs, scoring, and a sales workflow + outreach kit for expansion.”

**Boundary example:**  
“Write a generic cold outbound sequence for any product and send it to 50,000 people.”  
Response: explain this skill is usage-signal-driven and must be targeted and compliant; request product + ICP + available signals and produce a small, testable sequence and pilot instead.
