---
name: "platform-infrastructure"
description: "Produce a Platform & Infrastructure Improvement Pack (shared capabilities plan, reliability/performance/privacy targets, scaling triggers, analytics + discoverability decisions, execution roadmap). Use for platform engineering, infrastructure planning, scalability, reliability, and architecture foundations."
---

# Platform & Infrastructure

## Scope

**Covers**
- Platform engineering / “paved roads”: shared capabilities that multiple product teams reuse
- Infrastructure quality attributes: reliability, performance, privacy/safety, operability, cost
- Scalability planning: capacity limits, leading indicators, “doomsday clock” triggers, sequencing
- Instrumentation strategy: server-side event tracking, data quality, observability gaps
- Discoverability architecture for web platforms (optional): sitemap + internal linking

**When to use**
- “Create a platform infrastructure plan to increase feature velocity without repeating work.”
- “Turn reliability/performance/privacy goals into concrete SLOs and an execution roadmap.”
- “We’re approaching scaling limits—define triggers and the next infra projects.”
- “Our analytics is messy—design a server-side tracking plan and event contract.”
- “For a large web property, define sitemap + internal-linking requirements for crawlability.”

**When NOT to use**
- You are handling an active incident or outage (use incident response/runbooks first).
- You only need a single localized perf fix or refactor (just do the work).
- You need product strategy/positioning for a platform-as-product (use `platform-strategy`).
- You need a full feature spec or UX flows (use `writing-specs-designs` / `writing-prds`).
- SEO/content strategy is the primary workstream (use `content-marketing`).

## Inputs

**Minimum required**
- System boundary (services/apps) + primary users/customers
- Current pains (pick 1–3): reliability, performance, cost, privacy/security/compliance, developer velocity, data quality/analytics, SEO/discoverability
- Current architecture constraints (data stores, runtime, deployment model, key dependencies)
- Scale + trajectory (rough): current usage + expected growth + known upcoming spikes
- Constraints: deadlines, staffing/capacity, risk tolerance, compliance/privacy requirements

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If details remain missing, proceed with explicit assumptions and provide 2–3 options.
- If asked to change production systems or run commands, require explicit confirmation and include rollback guidance.

## Outputs (deliverables)

Produce a **Platform & Infrastructure Improvement Pack** in Markdown (in-chat; or as files if requested), in this order:

1) **Context snapshot** (scope, constraints, assumptions, stakeholders, success definition)
2) **Shared capabilities inventory + platformization plan** (what to standardize, why, and how)
3) **Quality attributes spec** (reliability/perf/privacy/safety targets; proposed SLOs/SLIs)
4) **Scaling “doomsday clock” + capacity plan** (limits, triggers, lead time, projects)
5) **Instrumentation plan** (observability gaps + server-side analytics event contract)
6) **Discoverability plan (optional)** for web platforms (sitemap + internal linking requirements)
7) **Execution roadmap** (sequencing, milestones, owners, dependencies, comms)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + define “what decision will this enable?”
- **Inputs:** Context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm scope boundaries, top pains, and time horizon. Write a 1–2 sentence decision statement (e.g., “We will standardize X and commit to SLO Y by date Z.”).
- **Outputs:** Context snapshot (draft).
- **Checks:** A stakeholder can answer: “What will we do differently after reading this?”

### 2) Find repeatable product capabilities worth platformizing
- **Inputs:** Recent roadmap/initiatives; architecture overview; pain points.
- **Actions:** Inventory repeated “feature components” (e.g., export, filtering, permissions, audit logs, notifications). Identify 3–7 candidates for shared infrastructure. Define what becomes the platform contract vs what remains product-specific.
- **Outputs:** Shared capabilities inventory + platformization plan (draft).
- **Checks:** Each candidate has: (a) at least 2 consumers, (b) a clear API/contract idea, (c) a migration/rollout approach.

### 3) Define quality attributes and targets (make “invisible work” explicit)
- **Inputs:** Reliability/perf/privacy needs; customer expectations; compliance constraints.
- **Actions:** Write the quality attributes spec. Propose SLOs/SLIs for reliability and performance; document privacy/safety requirements (data residency, encryption, access controls, retention).
- **Outputs:** Quality attributes spec (draft).
- **Checks:** Targets are measurable and owned (even if initial numbers are estimates + confidence).

### 4) Build the scaling “doomsday clock”
- **Inputs:** Current bottlenecks/limits; growth expectations; lead times for major changes.
- **Actions:** Identify top 3–10 capacity limits (DB size/IOPS, queue depth, cache hit rate, deploy throughput, rate limits). Define thresholds that trigger scaling projects early enough (lead time-aware).
- **Outputs:** Doomsday clock table + capacity plan (draft).
- **Checks:** Each limit has a metric, an alert threshold, a lead time estimate, and a named mitigation project.

### 5) Decide instrumentation: observability + server-side analytics
- **Inputs:** Current logging/metrics/tracing; current analytics tracking approach.
- **Actions:** Specify observability gaps (must-have dashboards/alerts) and define an event contract for server-side analytics (names, properties, identity strategy, delivery guarantees, QA checks).
- **Outputs:** Instrumentation plan (draft).
- **Checks:** Event definitions are consistent across clients; key events are captured server-side; data-quality checks exist.

### 6) (Optional) Discoverability architecture for web platforms
- **Inputs:** If applicable: site/app information architecture; SEO importance; crawl constraints.
- **Actions:** Define sitemap requirements (categorization, pagination, freshness) and internal-linking rules (“related content”, indexability controls, canonicalization).
- **Outputs:** Discoverability plan (draft) or “Not applicable” decision.
- **Checks:** A crawler can reach all indexable pages via links/sitemaps; “noindex”/canonicals are intentional.

### 7) Turn decisions into a sequenced execution roadmap
- **Inputs:** Draft deliverables; constraints; dependencies; capacity.
- **Actions:** Prioritize initiatives using impact × risk × effort × lead time. Create milestones, owners, and rollout plans (including deprecation/decommission for old paths).
- **Outputs:** Execution roadmap (draft).
- **Checks:** Roadmap has a first executable milestone, explicit dependencies, and measurable acceptance criteria.

### 8) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Tighten unclear contracts, add missing measures, and always include **Risks / Open questions / Next steps**.
- **Outputs:** Final Platform & Infrastructure Improvement Pack.
- **Checks:** A team can execute without extra meetings; unknowns are explicit and owned.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (shared capabilities):** “Use `platform-infrastructure` for a B2B analytics app where every team keeps rebuilding export, filtering, and permissions. Output a platformization plan + roadmap + SLO targets.”

**Example 2 (scaling readiness):** “We expect 5× traffic in 6 months. Define a doomsday clock for Postgres limits, propose scaling projects, and set reliability/performance SLOs. Also standardize server-side analytics.”

**Boundary example:** “We’re mid-incident and pages are down—tell us what to do right now.”  
Response: out of scope; recommend incident response first, then use this skill post-incident to create the scaling plan and reliability roadmap.

