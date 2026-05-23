---
name: "startup-ideation"
description: "Generate and evaluate startup ideas using off-the-beaten-path insights + Why-Now shift analysis. Produces a Startup Ideation Pack (opportunity theses table, scorecard, top idea brief, validation plan). Use for startup ideation, idea selection, “what should we build?”, why now, tarpit avoidance, information diet planning."
---

# Startup Ideation

## Scope

**Covers**
- Turning vague “startup ideas” into structured **opportunity theses**
- Expanding your **information diet** to find off-the-beaten-path opportunities
- Running a **Why Now** analysis based on technology + behavior + distribution shifts
- Identifying **tarpits** (ideas that look good but are structurally hard) and pruning early
- Scoring ideas and producing a **top-idea 1‑pager** + **2‑week validation plan**

**When to use**
- “Help me come up with startup ideas in/around <domain>.”
- “We have 5 ideas — help us pick one and explain why.”
- “What’s a good *Why Now* for this idea?”
- “Pressure to do AI — where are real new opportunities?”
- “How do we avoid idea tarpits and pick something differentiated?”

**When NOT to use**
- You already chose an idea and need a delivery-ready PRD (use `writing-prds`)
- You need to define the problem space for a specific user pain (use `problem-definition`)
- You need to execute research (recruit, interview, synthesize) rather than frame it (use `conducting-user-interviews`)
- You need market sizing / pricing / fundraising pitch materials (adjacent work, not covered here)

## Inputs

**Minimum required**
- Founder/team context + constraints (time, budget, skills, regulatory constraints)
- The decision to make + timeline (e.g., “pick 1 idea to validate in the next 2 weeks”)
- Target customer type (B2B/B2C; any preferred industries or segments)
- Any starting ideas (even rough) + what prompted them

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If still missing, proceed with explicit assumptions and list **Open questions** that could change the recommendation.

## Outputs (deliverables)

Produce a **Startup Ideation Pack** in Markdown (in-chat; or as files if the user requests):

1) **Context snapshot** (goal, constraints, decision, timeline)
2) **Unfair advantage + off-the-beaten-path signals** (what you know/see that others might not)
3) **Shift scan + Why Now candidates** (tech/behavior/distribution/regulatory shifts)
4) **Opportunity theses table** (15–30 ideas, each structured + testable)
5) **Tarpit & differentiation check** (prune to a shortlist)
6) **Idea scorecard** (score top 3–5 with evidence)
7) **Top idea brief (1‑pager)** (clear wedge + Why Now + ICP + risks)
8) **2‑week validation plan** (fastest tests for the highest-risk assumptions)
9) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify decision, time horizon, and constraints. Define success as “pick 1 idea to validate next” (or similar).
- **Outputs:** Context snapshot.
- **Checks:** You can restate the decision in one sentence (“We are deciding whether to… by <date>”).

### 2) Inventory unfair advantage + off-the-beaten-path signals
- **Inputs:** Founder/team background; past work; lived experience; access.
- **Actions:** List 5–15 unique signals: personal pain, workflows you’ve seen, niche communities, privileged distribution, proprietary data access, or operator insight.
- **Outputs:** Unfair advantage + signals list.
- **Checks:** Each signal is specific (who/where/when) and could plausibly lead to a differentiated idea.

### 3) Run a shift scan (“Why now?” raw material)
- **Inputs:** Domain + constraints; current trends the user cares about.
- **Actions:** Generate 10–20 “shifts” across: technology capability, buyer behavior, regulation, distribution, and cost curves. For each, write: “This enables X that was hard before.”
- **Outputs:** Shift scan + Why Now candidates.
- **Checks:** At least 5 shifts are concrete and falsifiable (not vague hype).

### 4) Generate opportunity theses (structured ideas)
- **Inputs:** Signals + shifts.
- **Actions:** Produce 15–30 opportunity theses using the template: *Customer → Job → Pain → Why now → Wedge → First test*.
- **Outputs:** Opportunity theses table.
- **Checks:** Every idea includes a Why Now statement and a proposed first validation test.

### 5) Tarpit & differentiation check (prune)
- **Inputs:** Opportunity theses table.
- **Actions:** Flag tarpits and thinly differentiated ideas. Apply “off-the-beaten-path” pressure: if an idea is widely discussed, require a strong wedge or discard.
- **Outputs:** Pruned list + notes on tarpits/differentiation.
- **Checks:** The remaining shortlist has at least one concrete advantage (distribution, insight, data, speed, regulatory, workflow depth).

### 6) Score + shortlist top 3–5
- **Inputs:** Pruned list; [references/RUBRIC.md](references/RUBRIC.md).
- **Actions:** Score each shortlisted idea with evidence and assumptions. Highlight the 1–2 criteria that dominate the outcome (sensitivity).
- **Outputs:** Idea scorecard + top 3–5 recommendation.
- **Checks:** Scores cite specific evidence or clearly labeled assumptions (no hand-wavy numbers).

### 7) Draft the top idea 1‑pager + 2‑week validation plan
- **Inputs:** Top idea; [references/TEMPLATES.md](references/TEMPLATES.md).
- **Actions:** Write a crisp 1‑pager (ICP, problem, Why Now, wedge, GTM motion hypothesis). Then design the fastest validation plan focused on the riskiest assumptions.
- **Outputs:** Top idea brief + validation plan.
- **Checks:** The plan includes: who to talk to, what to build (if anything), success criteria, and a stop/pivot rule.

### 8) Quality gate + finalize pack
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add **Risks / Open questions / Next steps**.
- **Outputs:** Final Startup Ideation Pack.
- **Checks:** A stakeholder can review async and decide “validate / park / discard” without a meeting.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B):** “We’re ex‑operators in logistics. Generate and score startup ideas; pick 1 to validate in 2 weeks.”  
Expected: opportunity theses rooted in real workflows + a shortlist + a top idea 1‑pager with a concrete validation plan.

**Example 2 (AI shift):** “We think new LLM capabilities enable something new in customer support; help us find a differentiated idea and Why Now.”  
Expected: shift scan → structured theses → tarpit check → top idea brief with a tight wedge and clear risks.

**Boundary example:** “Give me 100 startup ideas with no context.”  
Response: ask intake questions first; if the user won’t provide any, produce a small set of generic theses with explicit assumptions and advise on how to ground them in real signals.

