---
name: "platform-strategy"
description: "Create a Platform Strategy Pack (platform-as-product charter, interface map, lifecycle stage, ecosystem/moat model, governance, metrics, roadmap). Use for platform strategy, developer platforms, APIs, AI platforms, and ecosystems."
---

# Platform Strategy

## Scope

**Covers**
- Internal platforms (paved roads, shared infrastructure/services) treated as products
- External/hybrid platforms (APIs, extensions, partners) and ecosystem strategy
- Platform lifecycle strategy (when to open vs when to close for control/monetization)
- Platform surface-area design (interfaces, abstractions, governance) to reduce cognitive load for product teams
- AI platform defensibility (context repositories + integrated “toolkit” experiences) when relevant

**When to use**
- “Create a platform strategy for our developer platform / API.”
- “Turn our internal platform into a product with clear users, metrics, and roadmap.”
- “We want to open our platform to third parties—define incentives, governance, and a rollout.”
- “We’re building an AI platform—what’s the defensible system beyond a single feature?”

**When NOT to use**
- You don’t have a clear problem/job-to-be-done yet (use `problem-definition` first).
- You primarily need a product/company strategy and portfolio plan (use `ai-product-strategy`).
- You’re selecting a vendor/tool rather than defining a platform strategy (use `evaluating-new-technology`).
- You need an implementation design/architecture doc (use `writing-specs-designs` after this).

## Inputs

**Minimum required**
- Platform type: internal / external / hybrid (and who “the platform owner” is)
- Primary users/consumers (e.g., developers, data scientists, partners) and their top jobs-to-be-done
- Current state: what exists today (surfaces, APIs, services, docs), and what’s broken/painful
- Business intent: why now, desired outcomes (speed, reliability, revenue, ecosystem leverage), time horizon
- Constraints: security/privacy/compliance, SLOs, regions, budgets, resourcing, dependencies
- Decision context: who decides, what decisions are on the table (open/close, pricing, governance), target date

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If still missing, proceed with explicit assumptions and present 2–3 strategy options (e.g., internal-only vs partner beta vs public API).
- Do not request secrets or credentials. Require explicit confirmation for any production changes or external outreach.

## Outputs (deliverables)

Produce a **Platform Strategy Pack** (in chat; or as files if requested), in this order:

1) **Platform Product Charter** (users, jobs, non-goals, assumptions, outcomes)
2) **Platform Surface & Interface Map** (capabilities, owners, APIs/SDKs, “paved road” defaults, boundaries)
3) **Lifecycle Stage & Open/Close Strategy** (stage diagnosis, stage-appropriate moves, transition risks)
4) **Moat & Ecosystem Model** (compounding loops, incentives, seeding plan, investment gates)
5) **Governance & Policy Plan** (what’s open/closed, SLAs, deprecation, partner rules, pricing/packaging if relevant)
6) **Metrics & Operating Model** (platform-as-product operating cadence, intake, support, adoption + productivity metrics)
7) **12‑month Roadmap** (milestones, bets, sequencing, dependencies)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Define the platform as a product (users + jobs + outcomes)
- **Inputs:** Platform context, primary user groups, current pain.
- **Actions:** Write the platform’s “user promise” and top 3–5 jobs-to-be-done. Add 3–5 non-goals. Choose 2–4 outcome metrics (prefer developer productivity metrics like cycle time).
- **Outputs:** Draft **Platform Product Charter**.
- **Checks:** You can describe value without naming internal components (“We reduce X minutes of toil per deploy”).

### 2) Diagnose the platform lifecycle stage (and what decisions are truly on the table)
- **Inputs:** Market/organization conditions, competitive context (if external), timeline.
- **Actions:** Determine the most likely stage (Step 0→3) and list evidence. Clarify the “open vs close” decision(s) you must make now (not someday).
- **Outputs:** **Lifecycle Stage & Open/Close Strategy** (draft).
- **Checks:** The stage is justified with evidence, not aspiration (“we should be a platform”).

### 3) Map surface area and define boundaries (reduce decision complexity)
- **Inputs:** Existing services/APIs, teams, dependency graph, common failures.
- **Actions:** Inventory platform capabilities; define what becomes a paved road vs optional. Specify boundaries: what platform owns vs domain teams own. Draft interface contracts (APIs/SDKs/events) and “default decisions” the platform makes for others.
- **Outputs:** **Platform Surface & Interface Map**.
- **Checks:** A domain team can build without re-deciding foundational choices (auth, logging, deployment, guardrails).

### 4) Identify the moat and the compounding loop(s)
- **Inputs:** Unique assets, distribution, data/context advantages, ecosystem participants.
- **Actions:** Propose 1–3 moat hypotheses and at least one compounding loop (“if this works, it accelerates”). Define incentives for each participant and a small seeding plan. Define “investment gates” (signals that justify more spend).
- **Outputs:** **Moat & Ecosystem Model**.
- **Checks:** The loop has measurable leading indicators (activation, retained developers, successful integrations).

### 5) Decide what to open, how to govern it, and how to protect the core
- **Inputs:** Stage, risks, support capacity, security/compliance requirements.
- **Actions:** Specify what’s open now vs later, plus governance: access control, quotas, review processes, partner rules, SLAs, deprecation/backwards compatibility, and (if relevant) pricing/packaging. Include an “abuse/quality” plan (observability, enforcement).
- **Outputs:** **Governance & Policy Plan**.
- **Checks:** “Open” surfaces have a sustainability plan (support, docs, incident response, versioning).

### 6) (If AI platform) Build defensibility as a system, not a feature
- **Inputs:** AI use cases, context sources, data sensitivity, required integrations.
- **Actions:** Design a “Swiss‑army toolkit” system: shared context repository + multiple experiences (autocomplete, chat, agent workflows) with consistent policies. Define permissions, audit logs, eval/monitoring, and human-in-the-loop points.
- **Outputs:** AI section inside **Platform Product Charter** + **Governance & Policy Plan** updates.
- **Checks:** The plan improves outcomes while containing risk (least privilege, auditable access, measurable quality).

### 7) Define metrics + operating model (platform-as-product)
- **Inputs:** Target outcomes, resourcing constraints, stakeholder map.
- **Actions:** Define a metric stack (north-star + input metrics) and an operating cadence (intake, prioritization, roadmap reviews, documentation, support/on-call, feedback loops). Ensure a PM/owner exists for internal platforms.
- **Outputs:** **Metrics & Operating Model**.
- **Checks:** Metrics tie to user outcomes (not vanity counts like “# of services migrated” alone).

### 8) Sequence the roadmap and quality-gate the pack
- **Inputs:** All draft artifacts.
- **Actions:** Create a 12‑month roadmap with 3 horizons (Now / Next / Later). Add dependencies, resourcing, and rollback/exit paths. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final **Platform Strategy Pack**.
- **Checks:** A stakeholder can make a decision (owner, date, next actions) and understand trade-offs.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (internal platform):** “Use `platform-strategy` to create a platform strategy for an internal ML platform used by 40 engineers. Goal: cut model deployment cycle time from 2 weeks to 2 days. Constraints: PII present; SOC2; 2 platform engineers; 6‑month horizon.”  
Expected: platform-as-product charter + paved-road interfaces + productivity metrics + governance for AI data.

**Example 2 (external ecosystem):** “Use `platform-strategy` to define an API platform strategy for opening our analytics product to partners. We want 20 high-quality integrations in 12 months without breaking core reliability.”  
Expected: stage diagnosis + open/close decisions + incentives + governance/versioning + roadmap.

**Boundary example:** “We should become a platform like Apple—make us a platform strategy.”  
Response: out of scope without specific users/jobs and a plausible compounding loop; ask intake questions and/or start with `problem-definition`.

