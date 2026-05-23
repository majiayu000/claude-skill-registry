---
name: "shipping-products"
description: "Plan and execute a product launch/release with speed and safety. Produces a Shipping & Launch Pack (release brief, rollout/rollback plan, product quality list, comms + enablement, monitoring plan, post-launch review). Use for ship, launch, release, deploy, go live."
---

# Shipping Products

## Scope

**Covers**
- Turning “we need to ship” into a concrete **release plan** with owners, dates, and a rollout strategy
- Building a **Shipping & Launch Pack** that makes the release decision-ready (Go/No-go)
- Shipping in **small, frequent increments** to improve both speed and stability
- Defining a reusable **Product Quality List (PQL)** and iterating it based on escapes
- Planning **measurement, monitoring, rollback**, and **post-launch learning**

**When to use**
- “We’re launching / releasing / deploying / going live—make a plan and ship.”
- “Create a go/no-go checklist and rollout plan for this release.”
- “We need to ship faster without breaking trust—set up small-batch shipping.”
- “Write release notes + comms + enablement for an upcoming launch.”

**When NOT to use**
- You don’t yet agree on the problem or target user (use `problem-definition`)
- You need to right-size scope to hit a date/appetite (use `scoping-cutting`)
- You need a decision-ready PRD (use `writing-prds`) or build-ready spec/design doc (use `writing-specs-designs`)
- You’re setting long-term strategy/vision (use `defining-product-vision`) or choosing among initiatives (use `prioritizing-roadmap`)

## Inputs

**Minimum required**
- What you’re shipping (feature/change), target users, and where it will be available (platforms, regions, plans)
- Desired ship date/timebox + constraints (compliance, privacy, brand, uptime windows)
- Success metric(s) + guardrails (trust/safety, performance, reliability, support load)
- Rollout context (flags? staged rollout? beta? migration?) + key dependencies
- Stakeholders + DRI (who decides go/no-go) + who is on point during the launch

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and list **Open questions** that would change the ship decision.

## Outputs (deliverables)

Produce a **Shipping & Launch Pack** in Markdown (in-chat; or as files if the user requests):

1) **Release brief** (what/why now/who/when; DRI; scope + non-goals)
2) **Rollout plan** (phases, eligibility, flags, sequencing, kill switch, rollback)
3) **Quality plan (PQL)** (tests/acceptance, “must be true”, known risks, sign-offs)
4) **Measurement + monitoring plan** (success metrics, dashboards, alerts, owner)
5) **Comms + enablement plan** (internal/external messaging, docs, support readiness)
6) **Launch day runbook** (timeline, checkpoints, go/no-go criteria, escalation)
7) **Post-launch review plan** (what we’ll learn, retro prompts, follow-ups)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + define “what does shipped mean?”
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the change, target users, ship date, DRI, constraints, and what “live” means (where/for whom).
- **Outputs:** Release brief (draft).
- **Checks:** You can state the release in one sentence: “We will ship <what> to <who> by <when> via <rollout>.”

### 2) Choose the ship strategy (small batches by default)
- **Inputs:** Release brief; constraints; dependency map.
- **Actions:** Decide: internal → beta → GA (or phased rollout), flag strategy, and how to keep changes small. Identify the smallest safe increments.
- **Outputs:** Rollout plan (draft) + incremental release slices.
- **Checks:** Each increment has a clear user-visible outcome and a rollback path.

### 3) Run the “maximally accelerated” forcing function
- **Inputs:** Rollout plan (draft); slice list; blockers.
- **Actions:** Ask: “If we had to ship tomorrow, what would we do?” Use this to identify critical path vs non-essential work. Convert into a realistic plan.
- **Outputs:** Critical path list + cut/defer list + open questions.
- **Checks:** Every blocker is categorized: remove, work around, accept risk, or change scope.

### 4) Define the Product Quality List (PQL) + acceptance bar
- **Inputs:** Known risks; guardrails; product surface area.
- **Actions:** Create/extend a PQL (tests, UX states, security/privacy, reliability, performance). Explicitly list “must be true” to ship.
- **Outputs:** Quality plan (PQL) + go/no-go criteria (draft).
- **Checks:** PQL items are measurable/verifiable, not vibes; owners are assigned.

### 5) Measurement, monitoring, rollback
- **Inputs:** Success metrics/guardrails; rollout plan.
- **Actions:** Define dashboards/queries, alert thresholds, and on-call/escalation. Write the rollback and “stop-the-line” triggers.
- **Outputs:** Monitoring plan + rollback plan + launch runbook skeleton.
- **Checks:** If the metric moves the wrong way, you know who acts, how fast, and what they do.

### 6) Comms + enablement (internal first)
- **Inputs:** Release brief; target audiences; launch tier (minor/major).
- **Actions:** Draft internal announcement, release notes, help docs updates, sales/support enablement, and external messaging (if any).
- **Outputs:** Comms + enablement plan.
- **Checks:** Every audience has: what changed, why it matters, what to do next, where to get help.

### 7) Go/No-go + launch execution
- **Inputs:** Full pack draft; PQL; checklists.
- **Actions:** Run a go/no-go review, finalize the runbook timeline, confirm roles, and ensure dependencies are ready.
- **Outputs:** Final Shipping & Launch Pack (ready to execute).
- **Checks:** [references/CHECKLISTS.md](references/CHECKLISTS.md) passes with no open “stop-ship” items.

### 8) Post-launch review + iterate the system
- **Inputs:** Launch outcomes; incident notes; feedback.
- **Actions:** Run a short retro, capture learnings, update the PQL based on escapes, and define next iteration(s).
- **Outputs:** Post-launch review notes + PQL updates + next steps.
- **Checks:** At least 1 process improvement is identified and owners/dates are assigned.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS release):** “We’re launching role-based access control for admins next month. Create a Shipping & Launch Pack with a staged rollout, go/no-go criteria, and support enablement.”  
Expected: a phased rollout with clear eligibility, a PQL including permission edge cases, and a launch runbook + comms plan.

**Example 2 (Consumer app iteration):** “Ship ‘saved searches’ to 10% of users behind a flag next week; define monitoring and rollback triggers.”  
Expected: a small-batch rollout plan, dashboards/alerts tied to guardrails, and explicit stop-the-line thresholds.

**Boundary example:** “Decide what we should build this quarter.”  
Response: use `prioritizing-roadmap` (and/or `defining-product-vision`) first; then apply this skill to the chosen initiative’s release.

