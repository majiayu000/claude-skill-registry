---
name: "ai-evals"
description: "Create an AI Evals Pack (eval PRD, test set, rubric, judge plan, results + iteration loop). Use for LLM evaluation, benchmarks, rubrics, error analysis/open coding, and ship/no-ship quality gates for AI features."
---

# AI Evals

## Scope

**Covers**
- Designing evaluation (“evals”) for LLM/AI features as an execution contract: what “good” means and how it’s measured
- Converting failures into a **golden test set** + **error taxonomy** + **rubric**
- Choosing a judging approach (human, LLM-as-judge, automated checks) and a repeatable harness/runbook
- Producing decision-ready results and an iteration loop (every bug becomes a new test)

**When to use**
- “Design evals for this LLM feature so we can ship with confidence.”
- “Create a rubric + golden set + benchmark for our AI assistant/copilot.”
- “We’re seeing flaky quality—do error analysis and turn it into a repeatable eval.”
- “Compare prompts/models safely with a clear acceptance threshold.”

**When NOT to use**
- You need to decide *what to build* (use `problem-definition`, `building-with-llms`, or `ai-product-strategy`).
- You’re primarily doing traditional non-LLM software testing (use your standard eng QA/unit/integration tests).
- You want model training research or infra design (this skill assumes API/model usage; delegate to ML/infra).
- You only want vendor/model selection with no defined task + data (use `evaluating-new-technology` first, then come back with a concrete use case).

## Inputs

**Minimum required**
- System under test (SUT): what the AI does, for whom, in what workflow (inputs → outputs)
- The decision the eval must support (ship/no-ship, compare options, regression gate)
- What “good” means: 3–10 target behaviors + top failure modes
- Constraints: privacy/compliance, safety policy, languages, cost/latency budgets, timeline

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If details remain missing, proceed with explicit assumptions and provide 2–3 viable options (judge type, scoring scheme, dataset size).
- If asked to run code or generate datasets from sensitive sources, request confirmation and apply least privilege (no secrets; redact/anonymize).

## Outputs (deliverables)

Produce an **AI Evals Pack** (in chat; or as files if requested), in this order:

1) **Eval PRD** (evaluation requirements): decision, scope, target behaviors, success metrics, acceptance thresholds  
2) **Test set spec + initial golden set**: schema, coverage plan, and a starter set of cases (tagged by scenario/risk)  
3) **Error taxonomy** (from error analysis + open coding): failure modes, severity, examples  
4) **Rubric + judging guide**: dimensions, scoring scale, definitions, examples, tie-breakers  
5) **Judge + harness plan**: human vs LLM-as-judge vs automated checks, prompts/instructions, calibration, runbook, cost/time estimate  
6) **Reporting + iteration loop**: baseline results format, regression policy, how new bugs become new tests  
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Define the decision and write the Eval PRD
- **Inputs:** SUT description, stakeholders, decision to support.
- **Actions:** Define the decision (ship/no-ship, compare A vs B), scope/non-goals, target behaviors, acceptance thresholds, and what must never happen.
- **Outputs:** Draft **Eval PRD** (template in [references/TEMPLATES.md](references/TEMPLATES.md)).
- **Checks:** A stakeholder can restate what is being measured, why, and what “pass” means.

### 2) Draft the golden set structure + coverage plan
- **Inputs:** User workflows, edge cases, safety risks, data availability.
- **Actions:** Specify the test case schema, tagging, and coverage targets (happy paths, tricky paths, adversarial/safety, long-tail). Create an initial starter set (small but high-signal).
- **Outputs:** **Test set spec + initial golden set**.
- **Checks:** Every target behavior has at least 2 test cases; high-severity risks are explicitly represented.

### 3) Run error analysis and open coding to build a taxonomy
- **Inputs:** Known failures, logs, stakeholder anecdotes, initial golden set.
- **Actions:** Review failures, label them with open coding, consolidate into a taxonomy, and assign severity/impact. Identify likely root causes (prompting, missing context, tool misuse, formatting, policy).
- **Outputs:** **Error taxonomy** + “top failure modes” list.
- **Checks:** Taxonomy is mutually understandable by PM/eng; each category has 1–2 concrete examples.

### 4) Convert taxonomy → rubric + scoring rules
- **Inputs:** Taxonomy, target behaviors, output formats.
- **Actions:** Define scoring dimensions and scales; write clear judge instructions and tie-breakers; add examples and disallowed behaviors. Decide absolute scoring vs pairwise comparisons.
- **Outputs:** **Rubric + judging guide**.
- **Checks:** Two independent judges would likely score the same case similarly (instructions are specific, not vibes).

### 5) Choose the judging approach + harness/runbook
- **Inputs:** Constraints (time/cost), required reliability, privacy/safety constraints.
- **Actions:** Pick judge type(s): human, LLM-as-judge, automated checks. Define calibration (gold examples, inter-rater checks), sampling, and how results are stored. Write a runbook with estimated runtime/cost.
- **Outputs:** **Judge + harness plan**.
- **Checks:** The plan is repeatable (versioned prompts/models, deterministic settings where possible, clear data handling).

### 6) Define reporting, thresholds, and the iteration loop
- **Inputs:** Stakeholder needs, release cadence.
- **Actions:** Specify report format (overall + per-tag metrics), regression rules, and what changes require re-running evals. Define the iteration loop: every discovered failure becomes a new test + taxonomy update.
- **Outputs:** **Reporting + iteration loop**.
- **Checks:** A reader can make a decision from the report without additional meetings; regressions are detectable.

### 7) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Fix missing coverage, vague rubric language, or non-repeatable harness steps. Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final **AI Evals Pack**.
- **Checks:** The eval definition functions as a product requirement: clear, testable, and actionable.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (answer quality + safety):** “Use `ai-evals` to design evals for a customer-support reply drafting assistant. Constraints: no PII leakage, must cite KB articles, and must refuse unsafe requests. Output: AI Evals Pack.”

**Example 2 (structured extraction):** “Use `ai-evals` to create a rubric + golden set for an LLM that extracts invoice fields to JSON. Constraints: must always return valid JSON; prioritize recall for `amount` and `due_date`. Output: AI Evals Pack.”

**Boundary example:** “We don’t know what the AI feature should do yet—just ‘add AI’ and pick a model.”  
Response: out of scope; first define the job/spec and success metrics (use `problem-definition` or `building-with-llms`), then return to `ai-evals` with a concrete SUT.

