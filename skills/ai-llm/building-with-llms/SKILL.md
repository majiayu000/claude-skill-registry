---
name: "building-with-llms"
description: "Produce an LLM Build Pack (prompt+tool contract, data/eval plan, architecture+safety, launch checklist). Use for building with LLMs, GPT/Claude apps, prompt engineering, RAG, and tool-using agents."
---

# Building with LLMs

## Scope

**Covers**
- Building and shipping LLM-powered features/apps (assistant, copilot, light agent workflows)
- Prompt + tool contract design (instructions, schemas, examples, guardrails)
- Data quality + evaluation (test sets, rubrics, red teaming, iteration loop)
- Production readiness (latency/cost budgets, logging, fallbacks, safety/security checks)
- Using coding agents (Codex/Claude Code) to accelerate engineering safely

**When to use**
- “Turn this LLM feature idea into a build plan with prompts, evals, and launch checks.”
- “We need a system prompt + tool definitions + output schema for our LLM workflow.”
- “Our LLM is flaky—design an eval plan and iteration loop to stabilize quality.”
- “Design a RAG/tool-using agent approach with safety and monitoring.”
- “We want to use an AI coding agent to implement this—set constraints and review gates.”

**When NOT to use**
- You need product/portfolio strategy and positioning (use `ai-product-strategy`).
- You need a full PRD/spec set for cross-functional alignment (use `writing-prds` / `writing-specs-designs`).
- You need primary user research (use `conducting-user-interviews` / `usability-testing`).
- You are doing model training/research, infra architecture, or bespoke model tuning (delegate to ML/eng; this skill assumes API models).
- You only want “which model/provider should we pick?” (treat as an input; if it dominates, do a separate evaluation doc).

## Inputs

**Minimum required**
- Use case + target user + what “good” looks like (success metrics + failure modes)
- The LLM’s job: generate text, transform data, classify, extract, plan, or take actions via tools
- Constraints: privacy/compliance, data sensitivity, latency, cost, reliability, supported regions
- Integration surface: UI/workflow, downstream systems/APIs/tools, and any required output schema

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If details remain missing, proceed with explicit assumptions and provide 2–3 options (prompting vs RAG vs tool use; autonomy level).
- If asked to write code or run commands, request confirmation and use least privilege (no secrets; avoid destructive changes).

## Outputs (deliverables)

Produce an **LLM Build Pack** (in chat; or as files if requested), in this order:

1) **Feature brief** (goal, users, non-goals, constraints, success + guardrails)
2) **System design sketch** (pattern + architecture, context strategy, budgets, failure handling)
3) **Prompt + tool contract** (system prompt, tool schemas, output schema, examples, refusal/guardrails)
4) **Data + evaluation plan** (test set, rubrics, automated checks, red-team suite, acceptance thresholds)
5) **Build + iteration plan** (prototype slice, instrumentation, debugging loop, how to use coding agents safely)
6) **Launch + monitoring plan** (logging, dashboards/alerts, fallback/rollback, incident playbook hooks)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Frame the job, boundary, and “good”
- **Inputs:** Use case, target user, constraints.
- **Actions:** Write a crisp job statement (“The LLM must…”) + 3–5 non-goals. Define success metrics and guardrails (quality, safety, cost, latency).
- **Outputs:** Draft **Feature brief**.
- **Checks:** A stakeholder can restate what the LLM does and does not do, and how success is measured.

### 2) Choose the minimum viable autonomy pattern
- **Inputs:** Workflow + risk tolerance.
- **Actions:** Decide assistant vs copilot vs agent-like tool use. Identify “human control points” (review/approve moments) and what the model is never allowed to do.
- **Outputs:** Autonomy decisions captured in **Feature brief**.
- **Checks:** Any action-taking behavior has explicit permissions, confirmations, and an undo/rollback story.

### 3) Design the context strategy (prompting → RAG → tools)
- **Inputs:** Data sources, integration points, constraints.
- **Actions:** Decide how the model gets reliable context: instruction hierarchy, retrieval strategy, tool calls, structured inputs. Define the “source of truth” and how conflicts are handled.
- **Outputs:** Draft **System design sketch**.
- **Checks:** You can explain (a) what data is used, (b) where it comes from, (c) how freshness/authority is enforced.

### 4) Draft the prompt + tool contract (make the system legible)
- **Inputs:** Job statement + context strategy + output schema needs.
- **Actions:** Write the system prompt, tool descriptions, and output schema. Add examples and explicit DO/DO NOT rules. Include safe failure behavior (ask clarifying questions, abstain, cite sources).
- **Outputs:** **Prompt + tool contract**.
- **Checks:** A reviewer can predict behavior for 5–10 representative inputs; contract includes at least 3 hard constraints and examples.

### 5) Build the eval set + rubric (debug like software)
- **Inputs:** Expected behaviors + failure modes + edge cases.
- **Actions:** Create a test set covering normal cases, tricky cases, and red-team cases. Define a scoring rubric and acceptance thresholds. Add automated checks where possible (schema validity, citation presence, forbidden content).
- **Outputs:** **Data + evaluation plan**.
- **Checks:** You can run the same prompts repeatedly and measure improvement/regression; evals cover the top failure modes.

### 6) Prototype a thin slice, using coding agents safely
- **Inputs:** System sketch + prompt contract + eval plan.
- **Actions:** Implement the smallest end-to-end slice. Use coding agents for “lower hanging fruit” tasks, but keep tight constraints: small diffs, tests, code review, no secret handling.
- **Outputs:** **Build + iteration plan** (and optionally a prototype plan/checklist).
- **Checks:** You can explain what the agent changed, why, and how it was validated (tests, evals, manual review).

### 7) Production readiness: budgets, monitoring, and failure handling
- **Inputs:** Prototype learnings + constraints.
- **Actions:** Define cost/latency budgets, fallbacks, rate limits, logging fields, and alert thresholds. Address prompt injection/tool misuse risks; add safeguards and review processes.
- **Outputs:** **Launch + monitoring plan**.
- **Checks:** There is a clear path to detect regressions, cap cost, and safely degrade when the model misbehaves.

### 8) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Tighten unclear contracts, add missing tests, and always include **Risks / Open questions / Next steps**.
- **Outputs:** Final **LLM Build Pack**.
- **Checks:** A team can execute the plan without a meeting; unknowns are explicit and owned.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (RAG copilot):** “Use `building-with-llms` to plan a support-response copilot that drafts replies using our internal KB. Constraints: no PII leakage; must cite sources; p95 latency < 3s; cost < $0.10/ticket.”  
Expected: LLM Build Pack with prompt/tool contract, eval set (including privacy red-team cases), and monitoring/rollback plan.

**Example 2 (tool-using workflow):** “Use `building-with-llms` to design an LLM workflow that turns meeting notes into action items and Jira tickets (human review required). Output must be valid JSON.”  
Expected: output schema + tool contract + eval plan for structured extraction + guardrails against over-creation.

**Boundary example:** “Fine-tune/train a new LLM from scratch.”  
Response: out of scope; propose an API-model approach and highlight what ML/infra work is required if training is truly needed.

