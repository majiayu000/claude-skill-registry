---
name: "evaluating-new-technology"
description: "Create a Technology Evaluation Pack (problem framing, options matrix, build vs buy, pilot plan, risk review, decision memo). Use for evaluating new tech, emerging technology, AI tools, vendor selection, and tech stack decisions."
---

# Evaluating New Technology

## Scope

**Covers**
- Evaluating a new tool/platform/vendor (including AI products) for adoption
- Emerging tech “should we use this?” decisions
- Build vs buy decisions and tech stack changes
- Running a proof-of-value pilot and capturing evidence
- First-pass risk review (security/privacy/compliance, vendor claims, operational readiness)

**When to use**
- “Evaluate this new AI tool/vendor for our team.”
- “Should we build this in-house or buy a vendor?”
- “We’re considering changing our analytics/experimentation stack—make a recommendation.”
- “Create a technology evaluation doc with a pilot plan, risks, and decision memo.”

**When NOT to use**
- You don’t have a real problem/job to solve yet (use `problem-definition` first).
- You need a full product strategy/roadmap (use `ai-product-strategy`).
- You’re designing how to build an LLM system (use `building-with-llms`).
- You need a formal security assessment / penetration testing (engage security; this skill produces a structured first pass).

## Inputs

**Minimum required**
- Candidate technology (what it is, vendor/build option, links if available)
- Problem/workflow to improve + who it’s for
- Current approach/stack and what’s not working
- Constraints: data sensitivity, privacy/compliance, budget, timeline, regions, deployment model (SaaS/on-prem)
- Decision context: who decides, adoption scope, risk tolerance

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If still missing, proceed with explicit assumptions and present 2–3 options (e.g., buy vs build vs defer).
- Do not request secrets. If asked to run tools, change production systems, or sign up for vendors, require explicit confirmation.

## Outputs (deliverables)

Produce a **Technology Evaluation Pack** (in chat; or as files if requested), in this order:

1) **Evaluation brief** (problem, stakeholders, decision, constraints, non-goals, assumptions)
2) **Options & criteria matrix** (status quo + alternatives, criteria, scoring, notes)
3) **Build vs buy analysis** (bandwidth/TCO, core competency, opportunity cost, lock-in)
4) **Pilot (proof-of-value) plan** (hypotheses, scope, metrics, timeline, exit criteria)
5) **Risk & guardrails review** (security/privacy/compliance, vendor claims, mitigations)
6) **Decision memo** (recommendation, rationale, trade-offs, adoption/rollback plan)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Start with the problem (avoid tool bias)
- **Inputs:** Candidate tech, target workflow/users, current pain.
- **Actions:** Write a one-sentence problem statement and “who feels it.” List 3–5 symptoms and 3–5 non-goals.
- **Outputs:** Draft **Evaluation brief** (problem + non-goals).
- **Checks:** You can explain the decision without naming the tool.

### 2) Define “good” and hard constraints
- **Inputs:** Success metrics, constraints, risk tolerance, decision deadline.
- **Actions:** Define success metrics (leading + lagging) and must-have constraints (privacy, compliance, security, uptime, latency/cost if relevant). Capture “deal breakers.”
- **Outputs:** **Evaluation brief** (success + constraints + deal breakers).
- **Checks:** A stakeholder can say what would make this a clear “yes” or “no.”

### 3) Map options and evaluation criteria (workflows → ROI)
- **Inputs:** Current stack, alternatives, stakeholders.
- **Actions:** List options: status quo, 1–3 vendors, build, hybrid. Define criteria anchored to workflows enabled and ROI (time saved, revenue impact, risk reduction), not feature checklists.
- **Outputs:** **Options & criteria matrix**.
- **Checks:** Every criterion is measurable or at least falsifiable in a pilot.

### 4) Fast reality check: integration + data fit
- **Inputs:** Architecture constraints, data sources, integration points.
- **Actions:** Identify required integrations (SSO, data pipelines, APIs, logs). Note migration complexity, data ownership, and export/exit path. For PLG/growth tools, sanity-check the stack layers (data hub → analytics → lifecycle).
- **Outputs:** Notes added to **Options & criteria matrix** (integration complexity + stack fit).
- **Checks:** You can describe the end-to-end data/control flow in 5–10 bullets.

### 5) Build vs buy with “bandwidth” as a first-class cost
- **Inputs:** Engineering capacity, core competencies, opportunity cost.
- **Actions:** Compare build vs buy using a bandwidth/TCO ledger (build time, maintenance, on-call, upgrades, vendor management). Prefer building only when it’s a core differentiator or the vendor market is immature/unacceptable.
- **Outputs:** **Build vs buy analysis**.
- **Checks:** The analysis includes opportunity cost and who would maintain the system 12 months from now.

### 6) Risk & guardrails review (be skeptical of “100% safe” claims)
- **Inputs:** Data sensitivity, threat model, vendor posture, deployment model.
- **Actions:** Identify key risks (security, privacy, compliance, reliability, lock-in). For AI vendors: treat “guardrails catch everything” claims as marketing; assume determined attackers exist and design defense-in-depth (permissions, logging, human approval points, eval/red-team).
- **Outputs:** **Risk & guardrails review**.
- **Checks:** Each top risk has an owner and a mitigation or a “blocker” label.

### 7) Plan a proof-of-value pilot (or document why you can skip it)
- **Inputs:** Criteria, risks, timeline, stakeholders.
- **Actions:** Define pilot hypotheses, scope, success metrics, test dataset, and evaluation method. Specify timeline, resourcing, and exit criteria (adopt / iterate / reject). Include rollback and data deletion requirements.
- **Outputs:** **Pilot plan**.
- **Checks:** A team can run the pilot without extra meetings; success/failure is unambiguous.

### 8) Decide, communicate, and quality-gate
- **Inputs:** Completed pack drafts.
- **Actions:** Write the **Decision memo** with recommendation, trade-offs, and adoption plan. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final **Technology Evaluation Pack**.
- **Checks:** Decision is actionable (owner, date, next actions) and reversible where possible.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (AI vendor):** “Use `evaluating-new-technology` to evaluate an AI ‘prompt guardrails’ vendor for our support agent. Constraints: SOC2 required, PII present, must support SSO, budget $50k/yr, decision in 3 weeks.”  
Expected: evaluation pack that treats guardrail claims skeptically and proposes defense-in-depth + a measurable pilot.

**Example 2 (analytics stack):** “Use `evaluating-new-technology` to choose between PostHog and Amplitude for our PLG product. Current stack: Segment + data warehouse; goal is faster iteration on onboarding and activation.”  
Expected: options matrix + pilot plan tied to workflows (experiments, funnels, lifecycle triggers) and migration effort.

**Boundary example:** “What’s the best new AI tool we should adopt?”  
Response: out of scope without a problem/workflow; ask intake questions and/or propose running `problem-definition` first.

