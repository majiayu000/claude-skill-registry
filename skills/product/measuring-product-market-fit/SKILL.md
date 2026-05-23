---
name: "measuring-product-market-fit"
description: "Measure product-market fit (PMF) and produce a PMF Measurement Pack (Sean Ellis “very disappointed” survey, retention/usage evidence, reference-customer signals, and an action plan). Use for growth teams assessing PMF, PMF drift, and launch readiness."
---

# Measuring Product-Market Fit

## Scope

**Covers**
- Measuring PMF using a **triangulated signal set** (survey + behavior + customer evidence)
- Running and interpreting the **Sean Ellis “Very Disappointed”** survey (overall + by segment)
- Reading **retention curves / cohort retention** as PMF evidence (and knowing when they mislead)
- Using **reference-customer / advocacy** signals as an additional PMF proxy
- Detecting **PMF drift** (market shifts, rising expectations, competitive resets) and setting a re-measurement cadence
- Special handling for **marketplaces** (measure PMF per side; focus on the “hard side” first)

**When to use**
- “Do we have PMF? For which segment?”
- “Run a Sean Ellis PMF survey and tell me what it means.”
- “Build a PMF scorecard with retention + survey + references.”
- “Our market shifted—did we lose PMF?”
- “We want a go/no-go signal for scaling growth spend or launching publicly.”

**When NOT to use**
- You haven’t defined the problem/ICP yet (use `problem-definition`).
- You only need a survey instrument, not a full PMF measurement system (use `designing-surveys`).
- You’re deciding whether/how to pivot (use `startup-pivoting`) rather than measuring PMF signals.
- You need a product vision/strategy doc as the primary output (use `defining-product-vision` / `ai-product-strategy`).

## Inputs

**Minimum required**
- Product + category + current stage (pre-PMF / early PMF / growth / mature)
- Business model: B2B / B2C / marketplace (and, for marketplaces, which side you’re focusing on)
- Your current best guess at the target segment/ICP (and any meaningful segments)
- Definition of **active user** and the **core value moment** (the action that indicates value received)
- What data you can access: survey channels, product analytics, retention cohorts, revenue, qualitative feedback, reference customers/testimonials
- Time horizon and constraints (deadline, privacy/PII constraints, internal-only vs shareable)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md), then proceed.
- If key inputs are missing, proceed with explicit assumptions and label confidence.
- Do not request secrets. If data includes PII, ask for **redacted excerpts** or **aggregated fields**.

## Outputs (deliverables)

Produce a **PMF Measurement Pack** (Markdown in-chat; or as files if requested) containing:

1) **Context snapshot** (product, stage, decision, timebox, segments, constraints)
2) **PMF measurement model** (core value moment, active user definition, signal set, thresholds as heuristics)
3) **Sean Ellis survey plan + results** (sample definition, questions, response counts, “very disappointed” % overall + by segment, top benefits)
4) **Behavioral evidence** (retention/cohort summary + engagement frequency; instrumentation gaps + how they affect confidence)
5) **Reference-customer / advocacy evidence** (who is willing to vouch; quotes; counts vs heuristic targets)
6) **PMF Scorecard** (signals, targets, current state, confidence, evidence links/notes)
7) **Diagnosis + action plan** (PMF status by segment; top drivers; prioritized next actions/experiments)
8) **Risks / Open questions / Next steps** (always included)

Templates and checklists:
- [references/TEMPLATES.md](references/TEMPLATES.md)
- [references/CHECKLISTS.md](references/CHECKLISTS.md)
- [references/RUBRIC.md](references/RUBRIC.md)

## Workflow (7 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the decision (scale spend, launch, refocus ICP, pricing), the timebox, and the audience. Define “what will we do differently based on this?”
- **Outputs:** Context snapshot + measurement constraints.
- **Checks:** A stakeholder can answer: “What decision will this change by <date>?”

### 2) Define the PMF measurement model (and segments)
- **Inputs:** Product + segment hypotheses; data availability.
- **Actions:** Define:
  - The **core value moment** and **active user** definition
  - The segment(s) to evaluate (ICP + meaningful slices)
  - The signal set (survey + behavior + customer evidence) and what “good” looks like (as heuristics)
- **Outputs:** PMF measurement model + segment plan.
- **Checks:** Each signal has (a) a metric definition, (b) a data source, and (c) a limitation note.

### 3) Run the Sean Ellis PMF survey (must-have test)
- **Inputs:** Target population list (active users); distribution channel; [references/TEMPLATES.md](references/TEMPLATES.md) (PMF block).
- **Actions:** Draft and run:
  - “How would you feel if you could no longer use <product>?” (Very / Somewhat / Not disappointed)
  - Follow-up: “What is the primary benefit you receive?” (text)
  - Segment respondents (persona/ICP, use case, tenure) to find the “must-have” cohort
- **Outputs:** Survey plan + results table (overall + by segment) + top benefit themes.
- **Checks:** Sample definition is explicit; results include counts (n), not only percentages; major bias risks are listed.

### 4) Analyze behavioral evidence (retention + engagement)
- **Inputs:** Product usage data or best-available proxy; activation definition.
- **Actions:** Build a minimal behavioral picture:
  - Cohort retention (or repeat usage/purchase) by segment and tenure
  - Retention curve shape (improving/flat/decaying) and interpretation
  - Engagement frequency vs the product’s natural cadence (daily/weekly/monthly)
- **Outputs:** Retention/engagement summary + confidence notes + instrumentation gaps.
- **Checks:** Retention is measured from a clear cohort start; analysis separates **activation** from **retention**.

### 5) Collect reference-customer / advocacy evidence
- **Inputs:** Customer list; CS/sales notes; reviews; testimonials.
- **Actions:** Identify users willing to vouch publicly/privately:
  - B2B heuristic target: **6–8** reference customers
  - B2C heuristic target: **15–25** strong references/advocates
  - Capture the “why” (benefit) and the segment they represent
- **Outputs:** Reference evidence log + gaps by segment.
- **Checks:** References map to the intended ICP/segment; evidence is current (not from a different market era).

### 6) Synthesize into a PMF scorecard + diagnosis (by segment)
- **Inputs:** Survey + behavior + reference evidence.
- **Actions:** Triangulate signals to answer:
  - Do we have PMF for any segment? Which one is strongest?
  - What are the top drivers of “must-have” value?
  - What’s blocking PMF for adjacent segments?
  - Are we at risk of PMF drift (market shift, expectations rising)?
- **Outputs:** PMF Scorecard + diagnosis narrative + confidence rating.
- **Checks:** Diagnosis is segment-specific and evidence-backed; “unknowns” are explicit.

### 7) Quality gate + action plan + cadence
- **Inputs:** Draft pack; [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- **Actions:** Run the checklist + score with rubric. Produce:
  - Prioritized next actions/experiments (what to change, how to measure impact)
  - A PMF re-measurement cadence + drift triggers
  - **Risks / Open questions / Next steps**
- **Outputs:** Final PMF Measurement Pack.
- **Checks:** Actions are concrete enough to execute next sprint/quarter; measurement plan includes owners and dates (if known).

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS, early growth):**  
“Use `measuring-product-market-fit`. Product: AI meeting notes for account executives. Segments: mid-market sales teams vs SMB founders. Data: 90-day cohorts + in-app survey. Decision: whether to scale paid acquisition next quarter. Output: a PMF Measurement Pack.”

**Example 2 (Marketplace, supply-first):**  
“We’re building a caregiver marketplace. We have early demand, but supply is thin. Measure PMF for the supply side first using a PMF survey + retention proxies. Output a scorecard and a plan to strengthen the core value exchange.”

**Boundary example (insufficient inputs):**  
“Do we have PMF?”  
Response: ask up to 5 intake questions (segment, active user definition, data sources, survey channel, decision), then produce a minimal PMF Measurement Pack with explicit assumptions and confidence limits.

