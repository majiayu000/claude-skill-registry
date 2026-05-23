---
name: "scoping-cutting"
description: "Right-size scope to ship within a fixed timebox (appetite). Produces a Scoping & Cutting Pack: appetite, minimum lovable slice, cut list, validation plan, and a scope-creep guardrail plan. Use for MVP/descoping/scope creep."
---

# Scoping & Cutting

## Scope

**Covers**
- Converting a fuzzy initiative into a **ship-able slice** that fits a fixed time budget (“appetite”)
- Creating a **cut list** (what to drop/defer) with explicit trade-offs and rationale
- Defining an MVP as a **hypothesis test** (what you’re validating, not just “smaller”)
- Choosing a **Minimum Lovable Slice** (viable *and* emotionally resonant) instead of a “barely works” release
- Using **Wizard-of-Oz / concierge** approaches to validate value before building full automation
- Preventing scope creep via explicit **non-goals + change control**

**When to use**
- “Cut scope / descope this feature so we can ship by <date>.”
- “Define an MVP for this initiative (what hypothesis are we testing?).”
- “We have 2–6 weeks; what can we ship that still matters?”
- “Scope creep is killing us; define what’s in/out and how changes happen.”
- “We need a minimum lovable version, not a compromised mess.”

**When NOT to use**
- You don’t yet know what problem you’re solving (use `problem-definition`)
- You’re choosing between many competing initiatives (use `prioritizing-roadmap`)
- You need a decision-ready PRD with requirements (use `writing-prds`) or a build-ready design/tech spec (use `writing-specs-designs`)
- You’re setting long-term product strategy or vision (use `defining-product-vision`)

## Inputs

**Minimum required**
- The initiative/feature and the **decision** (ship vs defer vs stop) + target date or time budget
- Target user/segment + the **core user journey** you want to improve
- Success metric(s) + 2–5 guardrails (trust, quality, cost, latency, support load)
- Constraints and non-negotiables (legal/privacy, platform, dependencies, team size)
- Candidate scope items (bullets are fine) + known unknowns

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and list **Open questions** that would change the cut decisions.

## Outputs (deliverables)

Produce a **Scoping & Cutting Pack** in Markdown (in-chat; or as files if the user requests):

1) **Context snapshot** (decision, date/appetite, stakeholders/DRI, constraints)
2) **Outcome + hypothesis** (what must be true; what you’ll validate)
3) **Appetite + success bar** (time budget, “done means…”, guardrails)
4) **Minimum Lovable Slice spec** (core flow, must-haves, non-goals)
5) **Cut list** (cut/defer/keep with rationale + impact on risks)
6) **Validation plan** (Wizard-of-Oz/concierge/prototype as needed) + success criteria
7) **Delivery plan** (milestones within appetite + scope-change rules)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the decision, date/appetite, DRI, constraints, and what “shipping” means (where it lands, who uses it).
- **Outputs:** Context snapshot.
- **Checks:** You can state: “We are deciding to ship <slice> by <date> with <team> under <constraints>.”

### 2) Define the outcome and hypothesis (MVP = test)
- **Inputs:** Context snapshot; current evidence/risks.
- **Actions:** Write the outcome in user terms; define the key hypothesis (or 2–3). Choose success metric(s) + guardrails.
- **Outputs:** Outcome + hypothesis section; metrics/guardrails.
- **Checks:** You can answer: “What will we learn/validate by shipping this slice?”

### 3) Set appetite (time as a budget) + non-negotiables
- **Inputs:** Target date/timebox; constraints; team capacity.
- **Actions:** Set a hard time budget (e.g., 2/4/6 weeks). List non-negotiables (policy, privacy, reliability, design constraints).
- **Outputs:** Appetite + constraints section.
- **Checks:** Appetite is explicit and agreed; scope is the variable, not the deadline.

### 4) Design the Minimum Lovable Slice (MLS)
- **Inputs:** Outcome + constraints; candidate scope items.
- **Actions:** Define the smallest end-to-end flow that delivers the core value and feels coherent. Add 1–2 “lovability” elements that increase trust/clarity (not random polish).
- **Outputs:** MLS spec (core flow, must-haves, non-goals, assumptions).
- **Checks:** The slice is end-to-end (not a partial subsystem) and a user could describe why it’s valuable.

### 5) Build a cut list with explicit trade-offs
- **Inputs:** MLS spec + candidate scope items.
- **Actions:** Create a table of items to **keep / cut / defer**, with rationale tied to outcome, risk, and appetite. Convert “nice-to-haves” into “later” with a clear trigger for revisiting.
- **Outputs:** Cut list table + short decision rationale.
- **Checks:** Every removed item has a reason; non-goals are as clear as goals.

### 6) Add a validation plan (Wizard-of-Oz / concierge where helpful)
- **Inputs:** Riskiest assumptions; cut list.
- **Actions:** Choose the fastest validation method to de-risk the top unknown(s) (manual ops, scripted demo, prototype). Define what data/feedback counts as “validated”.
- **Outputs:** Validation plan (method, audience, script, success criteria, timeline).
- **Checks:** The plan can run without building the full system; success criteria are defined before running it.

### 7) Delivery plan + scope-change guardrails
- **Inputs:** MLS spec; validation plan; appetite.
- **Actions:** Break the work into milestones that fit the appetite. Define scope-change rules (how requests are evaluated; what gets traded off; who decides).
- **Outputs:** Delivery plan + scope-change policy.
- **Checks:** New scope can only enter by removing or shrinking something else (“trade, don’t add”).

### 8) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Ensure **Risks / Open questions / Next steps** are present with owners.
- **Outputs:** Final Scoping & Cutting Pack.
- **Checks:** A stakeholder can approve the slice async and the team can execute without re-litigating scope.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS):** “Cut scope for ‘bulk CSV import’ so we can ship a useful version in 4 weeks; include a Wizard-of-Oz validation plan.”  
Expected: an appetite-based MLS, a cut/defer table, and a validation plan that tests value before building every edge case.

**Example 2 (Consumer):** “Define a minimum lovable first version of ‘saved searches’ for mobile within a 2-week appetite.”  
Expected: a coherent end-to-end slice, explicit non-goals, and a scope-change policy to prevent creep.

**Boundary example:** “Decide what our Q2 roadmap should be across 12 initiatives.”  
Response: use `prioritizing-roadmap` first; then apply this skill to right-size the chosen initiative.
