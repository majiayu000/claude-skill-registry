---
name: "working-backwards"
description: "Create an Amazon-style PR/FAQ (future press release + FAQ) plus a backcasting launch plan to align on customer value, scope, and GTM readiness. Use for working backwards, PRFAQ / PR-FAQ, future press release, backcasting, launch plan."
---

# Working Backwards (PR/FAQ + Backcasting)

## Scope

**Covers**
- Turning a product idea into a customer-centric **future press release + FAQ (PR/FAQ)**
- Creating 2–3 divergent PR options to avoid solution lock-in
- Backcasting a launch: a concrete **GTM + operational “machinery” plan** from target date back to today
- Surfacing stakeholders, dependencies, constraints, and risks early

**When to use**
- “Write a PR/FAQ for…”
- “Working backwards from the customer…”
- “Create a future press release / press release from the future”
- “Backcast a launch plan / working backwards timeline”
- “We need alignment on what we’re building before writing a PRD”

**When NOT to use**
- You don’t yet understand the problem and need discovery framing (use `problem-definition`)
- You already have narrative alignment and need detailed requirements (use `writing-prds`)
- You need a build-ready engineering/design spec (use `writing-specs-designs`)
- You’re prioritizing among many initiatives (use `prioritizing-roadmap`)
- You only need marketing copy for an already-built product (this skill is for product decision-making)

## Inputs

**Minimum required**
- Product/context + target customer/user segment
- Problem statement (or symptoms) + why now
- Candidate solution idea(s) (can be vague; options are welcome)
- Constraints: timeline/launch target, platform, policy/legal, dependencies
- Success metrics (1–3) + guardrails (2–5)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers remain missing, proceed with clearly labeled assumptions and provide 2–3 options (PR variants, scope, rollout).

## Outputs (deliverables)

Produce a **Working Backwards Pack** in Markdown (in-chat; or as files if the user requests):

1) **Context snapshot**
2) **PR options:** 2–3 divergent future press releases (1 page each)
3) **Selected PR:** refined future press release
4) **FAQ:** customer + internal (business/ops/technical/legal) FAQs
5) **Backcasting plan:** milestones to launch (owners, dates, dependencies)
6) **Stakeholder + “machinery” plan:** approvals, comms, rollout, support readiness
7) **Success metrics + guardrails** (+ instrumentation notes)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** user request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the decision (invest vs not, choose approach), audience, and target launch date/timebox. Capture constraints + stakeholders.
- **Outputs:** Context snapshot.
- **Checks:** You can state the decision and time horizon in one sentence.

### 2) Write the problem paragraph (before any solution)
- **Inputs:** customer segment + evidence; why now.
- **Actions:** Draft “Problem today” in customer language. List top pains and current alternatives/workarounds.
- **Outputs:** Problem paragraph + alternatives bullets.
- **Checks:** Describes pain without specifying implementation; avoids “we want to build X” framing.

### 3) Draft 2–3 divergent future press releases (options)
- **Inputs:** problem paragraph; constraints.
- **Actions:** Create Option A/B/C PRs with different solution shapes. Keep them 1 page each.
- **Outputs:** 2–3 PR drafts.
- **Checks:** Options are meaningfully different; each promises clear customer value; no internal jargon.

### 4) Select the best option and refine to a single PR
- **Inputs:** PR options; decision criteria; stakeholder feedback (if available).
- **Actions:** Pick a winner (or hybrid) and refine the PR for clarity, boundaries, and a concrete “how it works”.
- **Outputs:** Selected PR.
- **Checks:** A stakeholder can restate the benefit and “why now” in one sentence; “who it’s for / not for” is explicit.

### 5) Write the FAQ (customer + internal)
- **Inputs:** selected PR; constraints; dependencies.
- **Actions:** Draft FAQs in sections: customer, business, technical/ops, legal/compliance. Include out-of-scope, risks, and measurement.
- **Outputs:** FAQ section.
- **Checks:** Top objections are answered; open questions are explicitly labeled; no “we’ll figure it out later” hand-waving.

### 6) Backcast: build the launch and “machinery” plan
- **Inputs:** target launch tier/date; FAQ dependencies.
- **Actions:** Create a milestone plan working backward (design, eng, data, legal, docs, support, comms). Define launch tiers and rollback.
- **Outputs:** Backcasting plan + launch tiers/rollback plan.
- **Checks:** Each milestone has an owner + success criteria; major dependencies have a plan.

### 7) Stress-test: pre-mortem + metrics + guardrails
- **Inputs:** PR/FAQ + backcasting plan.
- **Actions:** Run a pre-mortem. List failure modes (trust/safety/quality/cost). Define success metrics + guardrails + instrumentation needs.
- **Outputs:** Risks + metrics/guardrails + validation notes.
- **Checks:** Each major risk has a mitigation/monitor; metrics are computable and owned.

### 8) Quality gate + finalize pack
- **Inputs:** full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Ensure final section includes risks/open questions/next steps.
- **Outputs:** Final Working Backwards Pack.
- **Checks:** Pack is decision-ready and shareable async (no meeting required).

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS):** “Write a PR/FAQ and backcasting plan for ‘Role-based dashboards’ for enterprise admins, with a beta in 8 weeks.”  
Expected: 2–3 PR options, selected PR/FAQ, and a milestone plan covering security review, instrumentation, docs/support.

**Example 2 (Consumer):** “Work backwards for ‘Saved routes’ in a navigation app; propose two alternative product concepts and pick one.”  
Expected: divergent PRs that surface trade-offs, clear metrics (repeat usage, retention), and guardrails (privacy, battery, safety).

**Boundary example:** “Write a PR/FAQ for ‘use AI’ (no user problem).”  
Response: ask intake questions, redirect to `problem-definition` if needed, and do not pretend to have customer clarity.

