---
name: "prioritizing-roadmap"
description: "Prioritize a product roadmap/backlog and produce a Roadmap Prioritization Pack (season framing, scoring model, ranked opportunities, roadmap, decision narrative, rollout plan)."
---

# Prioritizing Roadmap

## Scope

**Covers**
- Turning messy roadmap inputs into a ranked opportunity list + coherent roadmap
- Defining a planning “season” (macro context) and success criteria
- Using a common-currency scoring model (ICE + assumptions) to compare across teams
- Producing an alignment-ready Roadmap Prioritization Pack

**When to use**
- “What should we build next?”
- “We need a Q2/Q3 roadmap.”
- “We have too many requests and no way to compare them.”
- “We need to prioritize across multiple teams/pods.”

**When NOT to use**
- You don’t have any agreed goal / North Star / strategic intent (do product vision / goals first)
- You need sprint planning or story-level estimation
- You’re only choosing a single experiment within an already-fixed roadmap
- You need a full customer discovery plan from scratch

## Inputs

**Minimum required**
- Product + primary customer segment
- Planning horizon + cadence (e.g., next 6 weeks, next quarter, rolling 12–24 months)
- Success criteria (North Star / business goal) + 2–5 guardrails
- Candidate opportunities (or current roadmap/backlog) with rough size/effort
- Constraints: capacity, commitments, dependencies, deadlines, risk tolerance

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If still missing, proceed with clearly labeled assumptions and provide 2–3 roadmap options.

## Outputs (deliverables)

Produce a **Roadmap Prioritization Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (goal, horizon, constraints, stakeholders)
2) **Season framing** (what changed, key bets, explicit non-goals)
3) **Opportunity inventory** with conviction level (known vs hypothesis) and evidence
4) **Prioritization model** (common currency + ICE scoring + assumptions)
5) **Ranked opportunity list** (top 10–20) + “parking lot”
6) **Roadmap draft** (Now/Next/Later or quarterly themes) + update cadence (rolling plan)
7) **Decision narrative** (why these, why now) + “Think Bigger” ideas
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the decision (backlog vs quarterly roadmap vs annual planning), horizon, stakeholders, constraints, and “must-do” commitments.
- **Outputs:** Context snapshot.
- **Checks:** Everyone agrees what decision will be made and by when.

### 2) Define the “season” + success criteria
- **Inputs:** Context snapshot.
- **Actions:** Name the current season (macro context), define 3–5 season bets, and set success criteria (North Star + guardrails).
- **Outputs:** Season framing section.
- **Checks:** A stakeholder can restate “why now” and “what we’re optimizing for”.

### 3) Build the opportunity inventory (separate truth vs hypotheses)
- **Inputs:** Candidate inputs (requests, ideas, problems).
- **Actions:** Normalize each item into a problem/outcome statement; tag conviction level (Known / Belief / Hypothesis) and evidence; split discovery vs delivery.
- **Outputs:** Opportunity inventory table.
- **Checks:** Every item has an intended outcome metric and a confidence/evidence note.

### 4) Define the common-currency scoring model (ICE + assumptions)
- **Inputs:** Inventory + success criteria.
- **Actions:** Choose a primary “common currency” (e.g., North Star units, revenue, cost, risk reduction) and define ICE scales; estimate impact ranges and confidence based on evidence.
- **Outputs:** Scoring model + filled scoring table.
- **Checks:** Two people using the same scales would produce similar relative rankings.

### 5) Stress-test the ranking (scenarios + constraints)
- **Inputs:** Scored list + constraints.
- **Actions:** Apply constraints (capacity, dependencies, deadlines); run 2–3 scenarios (base / aggressive / conservative); ensure a balanced portfolio (core, growth, quality, big bets).
- **Outputs:** Shortlist (top set) + parking lot + key tradeoffs.
- **Checks:** Tradeoffs and “no’s” are explicit; nothing critical is missing.

### 6) Draft the roadmap (sequencing + cadence)
- **Inputs:** Shortlist + scenario choice.
- **Actions:** Convert priorities into a roadmap (Now/Next/Later or quarterly themes), sequencing by dependencies and learning; define a rolling plan cadence (e.g., rolling 12–24 months, refreshed every 6 months).
- **Outputs:** Roadmap draft + update cadence.
- **Checks:** The roadmap is coherent, feasible, and resilient to new inputs.

### 7) Write the decision narrative + alignment plan
- **Inputs:** Roadmap draft + rationale.
- **Actions:** Write “why these, why now”; include a “Think Bigger” section; define how the roadmap will be communicated and updated.
- **Outputs:** Decision narrative + comms/rollout plan.
- **Checks:** A cross-functional partner can explain the roadmap without you in the room.

### 8) Quality gate + finalize the pack
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final Roadmap Prioritization Pack.
- **Checks:** Pack is shareable as-is; assumptions, owners, and cadence are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS):** “Prioritize our next-quarter roadmap for a collaboration product across Growth + Core.”  
Expected: season framing, scored opportunity inventory, a Now/Next/Later roadmap, and a clear decision narrative with explicit non-goals.

**Example 2 (Marketplace):** “Prioritize 6 months of roadmap across supply, demand, and trust & safety.”  
Expected: a common-currency model that makes cross-team tradeoffs comparable and a rolling plan refreshed on a fixed cadence.

**Boundary example:** “Give me a 2-year roadmap, we don’t have goals or constraints.”  
Response: ask for goals/constraints; if unavailable, produce options + assumptions and recommend doing product vision + North Star first.

