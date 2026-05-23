---
name: "conducting-user-interviews"
description: "Plan, conduct, and synthesize high-signal user interviews and produce a User Interview Pack (recruiting plan, screener, discussion guide, notes template, synthesis report). Use for user interview, customer interview, discovery interview, JTBD switch interview, concept interview."
---

# Conducting User Interviews

## Scope

**Covers**
- Planning an interview study that supports a specific product decision
- Recruiting the right participants (including early adopters when appropriate)
- Running interviews that capture **specific stories and behaviors** (not opinions)
- Synthesizing interviews into **actionable** insights, opportunities, and next steps
- Creating a lightweight “customer panel” habit for fast follow-ups

**When to use**
- “Create a discussion guide for discovery interviews.”
- “Recruit and run 8 user interviews about onboarding / activation.”
- “We need to understand why users switched (or churned) — run switch interviews.”
- “Help me synthesize interviews into insights + opportunities.”
- “I’m a PM and need to run customer conversations next week.”

**When NOT to use**
- You primarily need **quantitative** evidence (survey/experiment/analytics) or statistical confidence
- You’re doing **usability testing** with task-based evaluation as the main output (different protocol)
- You’re working with **high-risk populations or sensitive topics** (medical, legal, minors) without appropriate approvals/training
- You have no decision to support (you’ll produce anecdotes without impact)

## Inputs

**Minimum required**
- Product + target user/customer segment (who, context of use)
- The decision the interviews should inform (e.g., positioning, onboarding redesign, roadmap bet)
- Interview type: discovery / JTBD switch / churn / concept test (or “recommend”)
- Target participants (role, behaviors, situation, recency) + “who NOT to interview”
- Constraints: number of interviews, time box, language/region, recording allowed, incentives (if any)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns.

## Outputs (deliverables)

Produce a **User Interview Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (goal, decision, hypotheses, constraints)
2) **Recruiting plan** (channels, outreach copy, scheduling logistics) + **screener**
3) **Interview guide** (script + question bank + probes) + **consent/recording plan**
4) **Note-taking template** + **tagging scheme**
5) **Synthesis report** (themes, evidence, opportunities, recommendations, confidence)
6) **Follow-up plan** (thank-you, keep-in-touch, “customer panel” list/cadence)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Frame the decision and choose interview type
- **Inputs:** Context + [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Define the decision, what you need to learn (unknowns), and pick the interview type (discovery vs switch vs churn vs concept).
- **Outputs:** Context snapshot + study intent.
- **Checks:** You can answer: “What will we do differently after these interviews?”

### 2) Define participant criteria (who/when/why) and sampling plan
- **Inputs:** Target segment, product context, constraints.
- **Actions:** Specify inclusion/exclusion criteria; prioritize **recency** (recent switch/churn/attempt) when relevant; decide sample mix (e.g., 6 core + 2 edge cases).
- **Outputs:** Participant profile + sampling plan.
- **Checks:** Criteria are behavior/situation-based (not demographic proxies).

### 3) Create recruiting plan + screener + outreach copy
- **Inputs:** Participant profile; available channels (CRM, support, community, ads, LinkedIn).
- **Actions:** Draft outreach messages, a screener, and scheduling logistics. Expect high drop-off; plan volume accordingly.
- **Outputs:** Recruiting plan + screener + outreach copy.
- **Checks:** Screener screens for the *story* you need (recency, context, alternatives), not “interest in our product.”

### 4) Draft the interview guide (story-first)
- **Inputs:** Interview type + hypotheses/unknowns.
- **Actions:** Build a guide that elicits **specific stories** (“last time…”) and avoids leading questions. Include probes, pivots, and time boxes. Add consent/recording script.
- **Outputs:** Interview guide + consent/recording plan.
- **Checks:** At least 70% of questions ask about past behavior and concrete examples.

### 5) Run interviews + capture clean notes (PM/Design present)
- **Inputs:** Guide, logistics, notes template.
- **Actions:** Run the session, follow the story, and capture verbatims. If possible, have PM + design observe live (or listen to recordings) to avoid secondhand dilution.
- **Outputs:** Completed notes per interview + key quotes + immediate highlights.
- **Checks:** Each interview yields 2–5 “story moments” (trigger → struggle → workaround → outcome).

### 6) Debrief immediately and normalize evidence
- **Inputs:** Interview notes, recordings/transcripts (if any).
- **Actions:** Do a 10–15 min debrief right after each interview: surprises, hypotheses updates, follow-ups. Tag notes consistently.
- **Outputs:** Debrief bullets + tagged notes.
- **Checks:** Unclear claims are marked as “needs follow-up” instead of treated as facts.

### 7) Synthesize across interviews into themes and opportunities
- **Inputs:** Tagged notes across interviews.
- **Actions:** Cluster by outcomes/struggles; capture contradictions; quantify lightly (counts) without over-claiming. Translate insights into opportunities and recommendations with confidence levels.
- **Outputs:** Synthesis report + opportunity list.
- **Checks:** Every major insight has at least 2 supporting interviews (or is labeled “single anecdote”).

### 8) Share, decide, follow up, and run the quality gate
- **Inputs:** Draft pack.
- **Actions:** Produce a shareable readout, propose next steps, and create a lightweight customer panel habit (5–10 engaged users). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md).
- **Outputs:** Final User Interview Pack + Risks/Open questions/Next steps.
- **Checks:** Stakeholders can restate (a) key learning, (b) decision implication, (c) what happens next.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Discovery):** “I’m redesigning onboarding for a B2B product. Create a recruiting plan + discussion guide for 8 discovery interviews with new trial users.”  
Expected: participant criteria, outreach + screener, discovery guide, notes template, synthesis plan, and a ready-to-run pack.

**Example 2 (Switch/JTBD):** “We lose deals to spreadsheets. Run switch interviews to learn what triggers teams to move off spreadsheets and what they try instead.”  
Expected: switch interview guide (timeline + forces), recruiting criteria emphasizing recency, and a synthesis structure that outputs ‘push/pull/anxieties/habits’.

**Boundary example:** “Ask users what features they want and build whatever they say.”  
Response: redirect to story-based interviewing; clarify decision context; avoid feature-request interviews without behavioral grounding.

