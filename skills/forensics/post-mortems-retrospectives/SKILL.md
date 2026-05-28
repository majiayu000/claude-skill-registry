---
name: "post-mortems-retrospectives"
description: "Run blameless post-mortems & retrospectives and produce a Post-mortems & Retrospectives Pack (brief + agenda, facts/timeline, contributing factors + root causes, decisions + action tracker, kill criteria, learning dissemination plan). Use for postmortem, post-mortem, retrospective, retro, after action review, lessons learned. Category: Leadership."
---

# Post-mortems & Retrospectives

## Scope

**Covers**
- Running **blameless** incident post-mortems and project/OKR retrospectives
- Turning “what happened?” into **system learnings + decisions** (not blame)
- Creating **follow-through**: owners, due dates, success signals, and review cadence
- Adding **kill criteria / triggers** so future pre-mortems lead to real action
- Institutionalizing learning via a lightweight “**Impact & Learnings**” review

**When to use**
- “Run a postmortem / retrospective for <incident/project> and write the doc.”
- “We missed OKRs—lead a retro focused on learning and systemic blockers.”
- “Create an after-action review with action items and owners.”
- “Set up a weekly impact & learnings review so insights don’t die in docs.”
- “Do a pre-mortem and define kill criteria / pivot triggers.”

**When NOT to use**
- The incident is **still active** (do incident response first; schedule the review after stabilization)
- The goal is to **assign blame** or evaluate an individual’s performance (use HR/management processes)
- You need deep technical debugging without the right experts (this skill facilitates; it doesn’t replace engineering investigation)
- You need to decide *what problem to solve* (use a problem-definition / discovery process first)

## Inputs

**Minimum required**
- What are we reviewing? (incident / project / OKR period) + 1–2 sentence summary
- Time window and key dates (start/end; detection time; resolution time if incident)
- Desired outcome (learning, prevention, speed, quality, alignment)
- Participants/roles (facilitator, scribe, decision owner; key stakeholders)
- Evidence available (timeline notes, metrics, dashboards, tickets, docs)
- Constraints (privacy; what to anonymize; audience)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If details are unavailable, proceed with explicit assumptions and label unknowns.
- Do not request secrets or personal data; use anonymized descriptions.

## Outputs (deliverables)

Produce a **Post-mortems & Retrospectives Pack** in Markdown (in-chat; or as files if requested):

1) **Retro brief + agenda** (purpose, attendees, roles, pre-reads, ground rules)
2) **Facts + timeline** (what happened; impact; timestamps; links)
3) **Contributing factors + root cause hypotheses** (systems lens; “why it made sense”)
4) **Learnings + decisions** (what changes; why; tradeoffs)
5) **Action tracker** (owner, due date, success signal, follow-up date)
6) **Kill criteria / triggers** (signals → committed action) for future work
7) **Learning dissemination plan** (how to socialize + a recurring “Impact & Learnings” review)
8) **Risks / Open questions / Next steps** (always)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Classify the review + set blameless ground rules
- **Inputs:** request context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Identify the review type (incident / project / OKR). Set a blameless norm (“fix systems, not people”) and decide whether to reframe language as “retrospective” to signal learning. Confirm facilitator, scribe, and decision owner.
- **Outputs:** Retro brief (draft) + attendee list + meeting invite outline.
- **Checks:** Objective is explicit (learning + improvement). Roles are assigned.

### 2) Assemble facts and a shared timeline (separate facts from stories)
- **Inputs:** artifacts (tickets, dashboards, logs, notes).
- **Actions:** Build a timestamped timeline; quantify impact; list “known facts” vs “assumptions to verify”.
- **Outputs:** Facts + timeline section using [references/TEMPLATES.md](references/TEMPLATES.md).
- **Checks:** Timeline has timestamps and links/evidence where possible. Assumptions are labeled.

### 3) Diagnose contributing factors (systems lens)
- **Inputs:** timeline + impact.
- **Actions:** Cluster causes across People / Process / Product / Tech / Comms / Environment. Use a “make it reasonable” lens: what conditions made the outcome likely? Optionally run 5 Whys on the top 1–2 factors.
- **Outputs:** Contributing factors map + root cause hypotheses.
- **Checks:** Avoids individual blame language; identifies system conditions that can be changed.

### 4) Extract learnings and decide what to change
- **Inputs:** contributing factors.
- **Actions:** Write 3–7 crisp learnings (“we learned that…”). Convert learnings into decisions (fix, guardrail, instrumentation, runbook, training, scope change). Keep OKR/grade discussion secondary to “why” and “what changes next”.
- **Outputs:** Learnings + decisions section.
- **Checks:** Each learning is tied to evidence and produces a concrete decision or experiment.

### 5) Build the action tracker (owners + dates + success signals)
- **Inputs:** decisions.
- **Actions:** Create action items with an owner, due date, and success signal. Add a follow-up review date (or a recurring review). Limit to what can realistically be executed; explicitly park “later ideas”.
- **Outputs:** Action tracker table + follow-up plan.
- **Checks:** No orphan actions: every item has owner + date. Top actions address top factors.

### 6) Add kill criteria / triggers (pre-commit to future action)
- **Inputs:** learnings; “what would we do differently next time?”
- **Actions:** Define 3–10 signals that indicate failure modes or lack of traction. For each signal, pre-commit to an action (pause, pivot, kill, escalate, add investment).
- **Outputs:** Kill criteria / trigger list.
- **Checks:** Each criterion is observable/measurable and has a committed action (not “discuss it”).

### 7) Disseminate learning + quality gate + finalize
- **Inputs:** full draft pack.
- **Actions:** Create a 1-page shareout (TL;DR, top actions, decisions). Propose a lightweight weekly/biweekly “Impact & Learnings” review to socialize learnings beyond the team. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add **Risks / Open questions / Next steps**.
- **Outputs:** Final Post-mortems & Retrospectives Pack.
- **Checks:** Shareout is understandable by the intended audience; follow-through mechanism exists; rubric passes.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (incident postmortem):** “We had a 45-minute outage in our payments API yesterday. Run a blameless postmortem and output the full Pack (timeline, contributing factors, action tracker, and a shareout).”  
Expected: evidence-backed timeline, systems causes, owned actions, dissemination plan.

**Example 2 (OKR retro):** “We hit 0.8 on our Q4 activation OKR. Lead a retrospective focused on why (systemic blockers) and what we change next quarter. Output the full Pack and kill criteria for the next initiative.”  
Expected: learnings > grade, decisions, owned actions, triggers for early course correction.

**Boundary example:** “Write a postmortem proving that Person X caused the incident.”  
Response: refuse blame framing; redirect to systems-based review and, if needed, suggest a separate HR/management process for performance topics.
