---
name: "writing-north-star-metrics"
description: "Define or refresh a product North Star metric + driver tree and produce a shareable North Star Metric Pack (narrative, metric spec, inputs, guardrails, rollout)."
---

# Writing North Star Metrics

## Scope

**Covers**
- Defining or refreshing a product/company North Star and North Star Metric
- Translating a qualitative value model into measurable, decision-useful metrics
- Creating a simple driver tree: leading input/proxy metrics + guardrails
- Producing a “North Star Metric Pack” teams can use as a decision tie-breaker

**When to use**
- “We need one metric that defines success.”
- “Teams are optimizing different KPIs.”
- “We’re setting quarterly OKRs and need leading indicators.”
- “We’re launching a new strategy and need a metric that aligns decisions.”

**When NOT to use**
- You only need OKRs for an already-agreed North Star
- You need a full analytics taxonomy/event tracking plan from scratch
- Stakeholders haven’t aligned on the customer value model / mission at all (do product vision/strategy first)
- You’re choosing a single experiment metric for a one-off test

## Inputs

**Minimum required**
- Product/company + primary customer segment
- The “value moment” (what the customer gets when things go well)
- Business model + strategic goal (growth, activation, retention, margin, trust, etc.)
- Time horizon (next quarter vs next year)
- Measurement constraints (what you can measure today; data latency; known gaps)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If still missing, proceed with clearly labeled assumptions and provide 2–3 options.

## Outputs (deliverables)

Produce a **North Star Metric Pack** in Markdown (in-chat; or as files if the user requests):

1) **North Star Narrative** (value model, tie-breaker, scope)
2) **Candidate metrics** (3–5) + **selection rationale** (evaluation table)
3) **Chosen North Star Metric spec** (definition, formula, window, segmentation, owner, data source)
4) **Driver tree** (leading input/proxy metrics + guardrails)
5) **Validation & rollout plan** (instrumentation checks, dashboard cadence, decision rules)
6) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + constraints
- **Inputs:** User context; use [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm product, customer, value moment, horizon, constraints, stakeholders.
- **Outputs:** 5–10 bullet “Context snapshot”.
- **Checks:** You can explain the customer value in one sentence.

### 2) Define the qualitative North Star (before numbers)
- **Inputs:** Context snapshot.
- **Actions:** Write a North Star statement and value model from the customer’s perspective.
- **Outputs:** Draft **North Star Narrative** (template in [references/TEMPLATES.md](references/TEMPLATES.md)).
- **Checks:** Narrative can act as a decision tie-breaker (“if we do X, does it move the North Star?”).

### 3) Generate 3–5 candidate North Star metrics (customer POV)
- **Inputs:** North Star Narrative + value moment.
- **Actions:** Propose metrics that measure delivered customer value (not internal activity). Include at least one “friction/absence of pain” option when relevant.
- **Outputs:** Candidate list with definitions.
- **Checks:** Each candidate is measurable, understandable, and not trivially gameable.

### 4) Stress-test and pick the North Star metric
- **Inputs:** Candidate metrics.
- **Actions:** Evaluate with [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md). Explicitly test:
  - Leading vs lagging (avoid “retention as the only goal”; pair lagging outcomes with controllable inputs)
  - Controllability within a quarter (proxy/input metrics you can move)
  - Ecosystem impact (what breaks if you optimize this?)
- **Outputs:** Selection table + chosen metric + why others lost.
- **Checks:** A cross-functional leader could agree/disagree based on definitions and evidence.

### 5) Write the metric spec (make it unambiguous)
- **Inputs:** Chosen metric.
- **Actions:** Define formula, unit, window, inclusion rules, segmentation, owner, source, latency, and example calculation.
- **Outputs:** **North Star Metric Spec**.
- **Checks:** Two analysts would compute the same number.

### 6) Build the driver tree (inputs + guardrails)
- **Inputs:** Metric spec + product levers.
- **Actions:** Decompose into 3–7 drivers; identify leading input/proxy metrics you can move in weeks/months; add guardrails to prevent gaming/harm.
- **Outputs:** Driver tree table + guardrails list.
- **Checks:** Every driver has at least 1 realistic lever (initiative/experiment) and 1 measurement.

### 7) Define validation + rollout
- **Inputs:** Driver tree + constraints.
- **Actions:** Plan validation (sanity checks, correlation to outcomes) and operationalization (dashboards, cadence, owners, decision rules).
- **Outputs:** **Validation & Rollout Plan**.
- **Checks:** Plan includes “who does what, when” and works with current instrumentation.

### 8) Quality gate + finalize pack
- **Inputs:** All drafts.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final **North Star Metric Pack**.
- **Checks:** Pack is shareable as-is; key decisions and caveats are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS):** “Define a North Star metric for a team collaboration tool.”  
Expected: a pack that chooses a customer-value metric (e.g., weekly active teams completing the core value moment), plus a driver tree (activation → collaboration depth) and guardrails.

**Example 2 (Marketplace):** “Refresh North Star metric for a local services marketplace.”  
Expected: a pack that measures delivered value (e.g., successful jobs completed with quality), plus input metrics for supply/demand balance and quality guardrails.

**Boundary example:** “Our North Star should be retention.”  
Response: keep retention as an outcome/validation metric, and propose controllable input/proxy metrics (time-to-first-value, weekly value moments, repeat value delivery) as the operating focus.

