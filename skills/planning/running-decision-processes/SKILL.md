---
name: "running-decision-processes"
description: "Run a high-quality decision process and produce a Decision Process Pack (decision brief/pre-read, options + criteria matrix, RAPID/DACI roles, decision meeting plan, decision log entry, comms, review plan). Use for decision making, decision memo, decision log, one-way door vs two-way door, RAPID, DACI, RACI, exec alignment."
---

# Running Decision Processes

## Scope

**Covers**
- Running an end-to-end decision process for a cross-functional, high-stakes, or high-ambiguity decision
- Making **implicit assumptions explicit** (so they can be tested and reviewed later)
- Avoiding “decision drift” (hesitation, hidden vetoes, unclear decision rights)
- Capturing durable artifacts: decision brief, roles, meeting plan, decision log, comms, and a review loop

**When to use**
- “Draft a decision memo / pre-read and run the decision meeting.”
- “We’re stuck between two bad options—help us decide and commit.”
- “Set up RAPID/DACI/RACI for this decision and clarify who decides.”
- “Create an options + criteria matrix and a decision log entry.”
- “This feels like a one-way door / irreversible decision—tighten the process.”

**When NOT to use**
- You need to decide **what problem to solve** (do problem definition first).
- You need **prioritization across many opportunities** (use a roadmap/prioritization workflow).
- The “decision” is actually a **status update** or routine coordination (use a meeting/operating cadence).
- The decision is **personal/legal/HR** or requires specialist counsel (escalate to humans and domain experts).

## Inputs

**Minimum required**
- Decision to make (one sentence) and decision deadline (or “no later than” date)
- Context/why now (what changed; what happens if you don’t decide)
- Scope boundaries + non-negotiables (policy, budget, timeline, customer commitments)
- Stakeholders and required approvers (who can block / who must live with the outcome)
- Current options under consideration (even if rough) and key uncertainties

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers are unavailable, proceed with explicit assumptions and label unknowns.

## Outputs (deliverables)

Produce a **Decision Process Pack** (Markdown in-chat, or files if requested) in this order:
1) **Decision Brief / Pre-read** (problem, context, decision statement, constraints, criteria, options, recommendation if any)
2) **Options + Criteria Matrix** (including assumptions/unknowns that drive the choice)
3) **Decision Rights + Process** (RAPID/DACI/RACI, roles, timeline, meeting plan)
4) **Decision Log Entry** (decision, rationale, tradeoffs, assumptions, owner, review date)
5) **Decision Communication** (announcement + what changes + next steps)
6) **Decision Review Plan** (what to measure, when to revisit, how to learn)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Classify the decision (speed vs rigor)
- **Inputs:** Decision statement (draft); deadline; stakes.
- **Actions:** Classify as **one-way door** (hard to reverse) vs **two-way door** (reversible). Set a timebox and required rigor (light/standard/heavy). Name the failure cost (what’s the worst credible outcome?).
- **Outputs:** Decision classification + process intensity + timebox.
- **Checks:** The process chosen matches reversibility and stakes (no “heavy process” for reversible choices; no “wing it” for irreversible ones).

### 2) Make the decision explicit (anti-hesitation)
- **Inputs:** Context/why now; constraints; success criteria.
- **Actions:** Turn implicit debate into a crisp decision: “We are deciding **X** by **date** to achieve **Y**.” List non-negotiables and what “good” means.
- **Outputs:** Decision Brief sections: Decision statement, Why now, Success criteria, Constraints.
- **Checks:** A stakeholder can restate the decision in one sentence without adding qualifiers.

### 3) Gather context (historian pass)
- **Inputs:** Prior docs; past decisions; stakeholder perspectives.
- **Actions:** Reconstruct relevant history (what was tried, what failed, and why). Surface “baggage” and hidden constraints. Collect only the decision-relevant facts.
- **Outputs:** Decision Brief sections: Background, Prior decisions + rationale, Known constraints.
- **Checks:** The brief distinguishes **facts** vs **assumptions** vs **opinions**.

### 4) Generate options + criteria; log assumptions
- **Inputs:** Candidate options; goals; constraints.
- **Actions:** Define evaluation criteria and (if helpful) weights. Expand to 2–4 viable options (including “do nothing” if appropriate). For each option, make key assumptions explicit (what must be true for this to work?).
- **Outputs:** Options + Criteria Matrix; Assumptions/Unknowns list.
- **Checks:** Each option has at least 2–3 explicit assumptions; criteria reflect actual tradeoffs (not “everything is important”).

### 5) Design the decision process + decision rights
- **Inputs:** Stakeholder list; org constraints; decision intensity.
- **Actions:** Choose a decision-rights model (RAPID/DACI/RACI). Assign roles (who recommends, who decides, who must be consulted, who is informed). Create a tight plan: pre-read, input window, meeting, decision capture, comms.
- **Outputs:** Decision Rights + Process doc; meeting plan.
- **Checks:** There is exactly one **Decider** (or a clearly defined decision body), and veto power is explicit.

### 6) Run a “curiosity loop” (contextual advice)
- **Inputs:** Key unknowns; list of 8–12 people to consult (mix of experts + context-aware peers).
- **Actions:** Ask lightweight, specific questions that demand rationale (“pick top 2 and why”, “what would change your mind?”). Capture inputs, disagreements, and decision-relevant evidence. Update options/assumptions accordingly.
- **Outputs:** Curiosity Loop input summary; updated matrix/assumptions.
- **Checks:** Inputs are specific and actionable (not generic opinions); dissent is recorded, not smoothed over.

### 7) Decide and commit (document the why)
- **Inputs:** Final brief + matrix; role assignments; meeting agenda.
- **Actions:** Run the decision meeting (or async decision) with a bias toward clarity. Make the decision explicit, name the tradeoffs, assign an owner, and set a review date. Document rationale and what would cause a revisit.
- **Outputs:** Decision Log Entry; committed next steps; decision announcement draft.
- **Checks:** The decision and owner are unambiguous; the team knows what changes tomorrow.

### 8) Communicate, execute, and review (learning loop)
- **Inputs:** Decision log; implementation plan; metrics.
- **Actions:** Send the decision communication. Translate into tasks/milestones. Schedule a review to compare outcomes vs assumptions and capture learning (keep “intuition” testable).
- **Outputs:** Sent comms (or ready-to-send); review plan; retrospective prompts.
- **Checks:** A review date and measurement plan exist; assumptions are testable and tracked.

## Quality gate (required)
- Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1:** “We need to decide whether to sunset Feature X by March 15. Create a decision memo, run a RAPID decision process, and draft the announcement.”  
Expected: Decision Brief + options/criteria matrix + RAPID roles + decision log entry + comms + review plan.

**Example 2:** “We’re split on building vs buying an analytics tool. It’s a one-way door. Set up a rigorous process and capture assumptions so we can learn.”  
Expected: One-way door classification + weighted criteria + assumptions log + consultation loop + decision log with review date.

**Boundary example:** “Help me decide if I should change careers.”  
Response: This skill is for organizational product/leadership decisions; suggest a personal decision framework or coach instead.

