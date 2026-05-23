---
name: "writing-prds"
description: "Write a clear, decision-ready PRD (and optionally a PR/FAQ, AI eval spec, and prompt set) for cross-functional alignment."
---

# Writing PRDs

## Scope

**Covers**
- Turning a product idea into a **decision-ready PRD** with unambiguous scope, requirements, and success metrics
- Optionally producing a **PR/FAQ** (press release + FAQ) to force customer-centric narrative first
- For AI features: adding a **Prompt Set** + **Eval Spec** so “requirements” are testable and continuously checkable

**When to use**
- “Write a PRD / product spec / requirements doc for this feature.”
- “Turn these messy notes into a PRD we can align on.”
- “Create a PR/FAQ and then a PRD.”
- “This is an AI feature; I need evals + prompts to define behavior.”

**When NOT to use**
- You’re still choosing *what strategy/market to pursue* (do product vision / strategy first)
- You need discovery from scratch (research plan, problem validation) more than requirements
- You need a detailed engineering design doc (APIs, schemas, low-level architecture)
- You’re prioritizing among many initiatives (do roadmap prioritization first)

## Inputs

**Minimum required**
- Product + target user/customer segment
- Problem statement + why now (what changed, what’s broken, or what opportunity exists)
- Goal(s) + non-goal(s) + key constraints (timeline, policy/legal, platform, dependencies)
- Success metric(s) + 2–5 guardrails (quality, safety, cost, latency, trust)

**If it’s an AI feature (additionally)**
- What the model/system should do vs must never do (policy + safety)
- Concrete examples of desired and undesired outputs
- How correctness will be evaluated (offline tests, human review, online metrics)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers are still missing, proceed with clearly labeled assumptions and provide 2–3 options (scope, metric, rollout).

## Outputs (deliverables)

Produce a **PRD Pack** in Markdown (in-chat; or as files if the user requests):

1) **Context snapshot** (what decision we’re making, constraints, stakeholders)
2) **Artifact selection** (PR/FAQ vs PRD vs AI add-ons)
3) **PR/FAQ** (optional) — customer narrative + FAQs
4) **PRD** — goals/non-goals, requirements (R1…Rn), UX flows, metrics, rollout
5) **AI Prompt Set** (if AI) — versioned prompts + examples + guardrails
6) **AI Eval Spec** (if AI) — acceptance tests + judge prompts + pass/fail criteria
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Decide the artifact set (don’t over-document)
- **Inputs:** User request + constraints.
- **Actions:** Choose: PR/FAQ only, PRD only, PR/FAQ → PRD, or PRD + AI add-ons (Prompt Set + Eval Spec).
- **Outputs:** Artifact selection + rationale.
- **Checks:** The artifacts match the decision being made and the audience.

### 2) Intake + clarify decision and success
- **Inputs:** [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Ask up to 5 questions; confirm decision owner, timeline, constraints, and success metrics/guardrails.
- **Outputs:** Context snapshot.
- **Checks:** You can state “what we’re deciding” and “how we’ll measure success” in 1–2 sentences.

### 3) Write the customer narrative first (PR/FAQ or PRD narrative)
- **Inputs:** Context snapshot.
- **Actions:** Draft a customer-centric narrative (problem → solution → why now). If using PR/FAQ, draft the press release headline/summary and top FAQs.
- **Outputs:** Narrative section (and PR/FAQ if selected).
- **Checks:** A stakeholder can restate the customer benefit and urgency without jargon.

### 4) Lock scope boundaries (goals, non-goals, out of scope)
- **Inputs:** Narrative + constraints.
- **Actions:** Define goals, non-goals, and explicit exclusions; call out dependencies and assumptions.
- **Outputs:** Scope section(s) in the PRD.
- **Checks:** “What we are NOT doing” is as clear as what we are doing.

### 5) Convert scope into testable requirements (R1…Rn)
- **Inputs:** Goals + user journeys.
- **Actions:** Write numbered requirements with acceptance criteria, edge cases, and non-functional needs (privacy, latency, reliability). Mark “must/should/could”.
- **Outputs:** Requirements table/list.
- **Checks:** An engineer or QA can turn requirements into test cases without asking you to interpret intent.

### 6) Define UX flows + instrumentation plan
- **Inputs:** Requirements + current product surfaces/events.
- **Actions:** Describe key user flows/states; specify success metrics, guardrails, and event/data needs (what to log, where, who owns).
- **Outputs:** UX/flows section + metrics & instrumentation section.
- **Checks:** Every goal has at least one measurable metric and a realistic data source.

### 7) If AI feature: ship prompts + evals as “living requirements”
- **Inputs:** Requirements + examples.
- **Actions:** Create a versioned Prompt Set and an Eval Spec (judge prompts + test set + pass thresholds). Include red-team/failure modes.
- **Outputs:** Prompt Set + Eval Spec drafts.
- **Checks:** The eval suite can fail when behavior regresses and pass when requirements are met.

### 8) Quality gate + finalize for circulation
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final PRD Pack (shareable as-is).
- **Checks:** Decisions, owners, metrics, and open questions are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS feature):** “Write a PR/FAQ + PRD for ‘Saved views’ in our analytics dashboard for admins.”  
Expected: PR/FAQ narrative, a scoped PRD with R1…Rn, metrics/guardrails, and a rollout plan.

**Example 2 (AI feature):** “Write a PRD + Prompt Set + Eval Spec for an ‘AI email reply’ assistant with brand tone constraints.”  
Expected: requirements that include safety/brand constraints, a prompt set with examples, and an eval spec with judge prompts + pass/fail thresholds.

**Boundary example:** “Write a PRD for ‘make onboarding better’ (no product context).”  
Response: ask the minimum intake questions; if context remains missing, produce 2–3 scoped options + assumptions and recommend discovery before committing to requirements.

