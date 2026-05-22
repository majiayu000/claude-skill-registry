---
name: "ai-product-strategy"
description: "Create an AI Product Strategy Pack (thesis, prioritized use cases, system plan, eval + learning plan, agentic safety plan, roadmap). Use for AI product strategy, LLM/agent strategy, AI roadmap, AI-first product direction."
---

# AI Product Strategy

## Scope

**Covers**
- Defining an executable product strategy for an AI/LLM/agent product or AI feature portfolio
- Translating AI uncertainty (non-determinism, emergent risks) into an empirical plan with evals + instrumentation
- Choosing product form factor (assistant vs copilot vs agent), autonomy boundaries, and a safety/security posture
- Producing a strategy pack leaders and teams can use to align and execute

**When to use**
- “Define our AI product strategy / LLM strategy / agent strategy.”
- “Prioritize AI use cases and turn them into an AI roadmap.”
- “We’re adding AI to an existing product—what should we build and how do we measure it?”
- “We want to ship an agent; define autonomy, security, and rollout.”

**When NOT to use**
- You need a long-term product/company vision (use `defining-product-vision` first).
- You need deep competitor research, battlecards, or win/loss (use `competitive-analysis`).
- You need a feature-level PRD/spec/design doc (use `writing-prds` / `writing-specs-designs` after strategy).
- You’re doing model architecture research, training, or infra-level technical design (delegate to ML/eng).
- You don’t yet have a clear problem/ICP hypothesis (use `problem-definition` / `conducting-user-interviews`).

## Inputs

**Minimum required**
- Product context (what exists today) + target customer/user + their job/pain
- Strategy horizon (default: 3–12 months) + constraints (budget, latency, policy/legal, data access, platform)
- Intended AI surface and scope: assistant / copilot / agent; where it lives in the workflow
- Success metrics (1–3) and guardrails (2–5), including safety/trust, cost, and latency

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If details remain missing, proceed with clearly labeled assumptions and provide 2–3 options (use-case focus, autonomy level, build/buy).

## Outputs (deliverables)

Produce an **AI Product Strategy Pack** in Markdown (in-chat; or as files if requested), in this order:

1) **Context snapshot** (decision, users, constraints, why now)
2) **Strategy thesis** (value prop, why-now, differentiation, non-goals)
3) **Use-case portfolio** (prioritized opportunities with feasibility + risk)
4) **Autonomy policy** (assistant→copilot→agent boundaries + human control points)
5) **System plan** (build/buy, data plan, eval plan, cost/latency budgets)
6) **Empirical learning plan** (experiments, instrumentation, iteration cadence)
7) **Roadmap** (phases, milestones, exit criteria, owners)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Frame the decision and boundaries
- **Inputs:** User request + constraints.
- **Actions:** Define the decision to make, strategy horizon, and audience. Decide whether this is for a single feature, a product line, or a platform capability. Write 3–5 explicit non-goals.
- **Outputs:** Draft **Context snapshot** + **scope boundaries**.
- **Checks:** You can state “We are deciding X by date Y for audience Z,” and list what’s explicitly out of scope.

### 2) Map the user workflow and role shift
- **Inputs:** Target user + current workflow.
- **Actions:** Map the workflow steps where AI changes the user’s job. Note “human control points” (where a user must review/approve). Identify failure modes that matter (hallucination, privacy, action mistakes).
- **Outputs:** Workflow notes + role-shift bullets (in thesis or appendix).
- **Checks:** Value is tied to a real workflow step (not generic “AI magic”).

### 3) Build a use-case portfolio and prioritize bets
- **Inputs:** Workflow map + constraints + risk appetite.
- **Actions:** List 6–12 candidate use cases. Score value vs feasibility vs risk. Select the top 1–3 bets and 1 “explore later” bet.
- **Outputs:** **Use-case portfolio** table + recommendation.
- **Checks:** Each selected bet has a clear user, measurable outcome, and known “must-not-do” constraints.

### 4) Define differentiation + “why us / why now”
- **Inputs:** Top bets + assets + market context.
- **Actions:** Draft the strategy thesis: value prop, why-now, and defensible differentiation (data, distribution, workflow integration, UX, trust). Write key assumptions and how you’ll test them.
- **Outputs:** **Strategy thesis** (copy/paste from template).
- **Checks:** Differentiation is not “we use AI”; it names compounding advantages or unique assets.

### 5) Choose form factor and autonomy policy (assistant → copilot → agent)
- **Inputs:** Bets + constraints + safety requirements.
- **Actions:** Decide the minimal autonomy needed for utility. Specify what the system can do, what it can suggest, and what it must never do. Define permission prompts, approvals, logging, and rollback for any action-taking behavior.
- **Outputs:** **Autonomy policy** table.
- **Checks:** Every action capability has explicit permissions + auditability + rollback.

### 6) Draft the system plan (build/buy, data, evals, budgets)
- **Inputs:** Autonomy policy + constraints + data access.
- **Actions:** Choose a strategy-level technical approach (e.g., RAG, tool use, fine-tuning) and a data plan. Define eval strategy (offline + online), quality targets, and cost/latency budgets.
- **Outputs:** **System plan**.
- **Checks:** There’s a plausible path to meet quality + safety + cost + latency with measurable evals.

### 7) Make it empirical (experiments + instrumentation + iteration)
- **Inputs:** Thesis + system plan + assumptions.
- **Actions:** Design experiments/prototypes and a “watch/listen” plan post-launch. Define instrumentation (events/logs), review cadence, and an iteration loop for both utility and risk.
- **Outputs:** **Empirical learning plan**.
- **Checks:** Every major assumption has a test + metric + owner + timebox.

### 8) Roadmap + quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Create a phased roadmap with milestones, exit criteria, and owners. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Always add **Risks / Open questions / Next steps**.
- **Outputs:** Final **AI Product Strategy Pack**.
- **Checks:** A stakeholder can act on the pack without a meeting; trade-offs and unknowns are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (AI-first product):** “Use `ai-product-strategy` to define strategy for an AI coding assistant for mid-market engineering teams. Constraints: ship a beta in 8 weeks; must not leak proprietary code; budget capped at $X/month.”  
Expected: strategy thesis + prioritized use cases + autonomy policy + system/eval plan + roadmap.

**Example 2 (AI feature portfolio):** “Use `ai-product-strategy` to prioritize AI opportunities for a customer support platform. Decide copilot vs agent, include safety posture, and propose a 2-quarter roadmap.”  
Expected: use-case portfolio with 1–3 bets, a clear agency-control policy, empirical plan, and phased roadmap with exit criteria.

**Boundary example:** “Pick the best LLM provider.”  
Response: treat “provider choice” as an input to the system plan; ask for constraints (data, cost, latency, privacy, regions). If the broader product decision is unclear, run this full strategy workflow first.

