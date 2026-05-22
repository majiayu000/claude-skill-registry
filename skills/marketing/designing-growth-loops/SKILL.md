---
name: "designing-growth-loops"
description: "Design growth loops (viral/referral/acquisition loops, flywheels) and produce a Growth Loop Design Pack (loop map, loop scorecard, channel fit + paid-loop feasibility, experiment backlog, measurement plan). Use for growth teams creating new growth loops or innovating beyond incremental optimization."
---

# Designing Growth Loops

## Scope

**Covers**
- Turning a growth goal into a **loop-based growth model** (micro loops + macro loops)
- Designing and documenting loops: **viral/referral**, **content/UGC**, **SEO**, **partner/integration**, **sales-assisted**, and **paid acquisition loops**
- Choosing channels using a **Customer × Business × Medium** fit check
- Validating paid loops with **unit economics (LTV, CAC, payback)** gating
- Producing an actionable loop plan: loop map → scorecard → experiments → measurement

**When to use**
- “Design a growth loop / viral loop / referral loop”
- “Create a growth flywheel for <product>”
- “Map our micro + macro growth loops and prioritize which to build”
- “We need new growth loops (not just optimize ads/onboarding)”
- “Decide whether a paid acquisition loop is viable”

**When NOT to use**
- You haven’t clarified the ICP/problem or value proposition (use `problem-definition`).
- You’re still establishing PMF and need a PMF signal set (use `measuring-product-market-fit`).
- You only need an experiment list/prioritization, not loop design (use `prioritizing-roadmap`).
- You’re making a one-way-door launch decision (use `shipping-products` / `running-decision-processes`).

## Inputs

**Minimum required**
- Product + target user/ICP (and 1–2 key segments)
- Current stage (pre-PMF / early PMF / growth / mature) and current primary growth channel(s)
- The core value moment (what users do when they “get value”)
- A baseline snapshot of the growth system (best available): acquisition sources, conversion funnel, retention/engagement, referrals/sharing
- Constraints: budget, timebox, brand/safety, platform policy, legal/privacy, engineering capacity
- For paid loops: rough unit economics (LTV, gross margin, CAC/payback targets) or a proxy

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md), then proceed.
- If data is missing, proceed with explicit assumptions and label confidence.
- Do not request secrets or PII; prefer aggregated metrics or redacted excerpts.

## Outputs (deliverables)

Produce a **Growth Loop Design Pack** (Markdown in-chat; or as files if requested) containing:

1) **Context snapshot** (goal, ICP/segments, constraints, timebox)
2) **Loop inventory + baseline** (current loops and where the system currently gets growth)
3) **Loop map (qualitative model)** (micro loops + macro loop; how loops connect)
4) **Loop candidates + mechanism library** (platform/channel mechanisms; ethical/policy-compliant)
5) **Loop scorecard + selection** (top 1–2 loops to build/scale; optimize vs innovate recommendation)
6) **Measurement plan** (loop KPIs, leading indicators, required instrumentation)
7) **Experiment backlog + 30/60/90 plan** (tests, sequencing, dependencies, owners if known)
8) **Risks / Open questions / Next steps** (always included)

Templates and checklists:
- [references/TEMPLATES.md](references/TEMPLATES.md)
- [references/CHECKLISTS.md](references/CHECKLISTS.md)
- [references/RUBRIC.md](references/RUBRIC.md)
- Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + growth goal framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the growth goal (what metric, by when), the target segment(s), and constraints (budget, brand, platform rules, capacity). Decide whether the priority is **innovation** (new loop) vs **optimization** (existing loop).
- **Outputs:** Context snapshot + “decision this work informs.”
- **Checks:** A stakeholder can answer: “Which metric changes by when, and what will we do differently if it doesn’t?”

### 2) Baseline the current growth system (loops + funnel)
- **Inputs:** Current acquisition sources, funnel, retention, referral/share, unit economics (if any).
- **Actions:** Inventory existing loops (even if weak). Identify the **core value moment** and the “loop output” that could feed back (invites, content, word-of-mouth, spend, integrations).
- **Outputs:** Loop inventory + baseline table.
- **Checks:** Baseline includes at least one number for each: acquisition volume, activation rate, retention/engagement proxy.

### 3) Generate loop candidates (micro + macro)
- **Inputs:** Baseline + constraints.
- **Actions:** Create 6–10 loop hypotheses across categories (viral/referral, content/UGC, SEO, partner/integration, sales, paid). For each, specify: input → action → output → feedback. Include at least one “bigger bet” loop if in a fast-moving category.
- **Outputs:** Loop candidates list + draft mechanism library.
- **Checks:** Each candidate has a plausible “self-reinforcing” feedback path and a likely cycle time.

### 4) Model loops qualitatively (shared understanding)
- **Inputs:** Loop candidates; stakeholder context.
- **Actions:** Produce a qualitative **loop map**: micro loops connected into a macro loop. Document assumptions, bottlenecks, and where you expect compounding.
- **Outputs:** Loop map (diagram or table) + bottleneck hypotheses.
- **Checks:** Someone unfamiliar with the product can explain “how we grow” in 60 seconds using the map.

### 5) Quantify + prioritize (scorecard + gates)
- **Inputs:** Qual loop map; best-available metrics.
- **Actions:** Estimate loop throughput with simple math (conversion × frequency × invites/content × acceptance). Score loops using a scorecard (impact, confidence, effort, cycle time). Apply gates:
  - **Paid loops:** only proceed if LTV/margin supports CAC/payback targets.
  - **Channel fit:** ensure Customer × Business × Medium alignment.
- **Outputs:** Loop scorecard + top 1–2 loop picks + innovate/optimize split recommendation.
- **Checks:** Each chosen loop has (a) a measurable KPI, (b) a first experiment, and (c) a reason it wins vs alternatives.

### 6) Design the measurement plan (metrics + instrumentation)
- **Inputs:** Selected loop(s).
- **Actions:** Define loop KPIs and leading indicators; specify required events/properties and dashboards. Identify instrumentation gaps and the minimum tracking needed to learn.
- **Outputs:** Measurement + instrumentation plan.
- **Checks:** Every experiment metric is traceable to an event definition and a data source.

### 7) Build the experiment plan + quality gate
- **Inputs:** Draft pack; [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- **Actions:** Create an experiment backlog and 30/60/90 plan (sequencing, dependencies, owners if known). Run the checklist and score with the rubric. Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final Growth Loop Design Pack.
- **Checks:** Next 2 weeks of work are unblocked and measurable; risks include policy/ethics considerations.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS, partner/integration loop):**  
“Use `designing-growth-loops`. Product: AI onboarding assistant for mid-market HR teams. Goal: +30% WAU in 90 days. Channels today: outbound + partnerships. Output: a Growth Loop Design Pack with an integration/partner loop and a referral loop, including metrics and a 30/60/90 experiment plan.”

**Example 2 (B2C, viral/content loop):**  
“We’re building a mobile photo editor for creators. Goal: grow from 20k to 60k MAU in 8 weeks. Output a loop map, a mechanism library for Instagram/TikTok sharing, and a prioritized experiment backlog.”

**Boundary example (not a loop problem):**  
“Write copy for our landing page headline.”  
Response: this is primarily copywriting/positioning, not loop design; clarify the goal and use `copywriting` or a messaging skill instead.

