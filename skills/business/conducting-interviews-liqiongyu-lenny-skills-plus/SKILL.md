---
name: "conducting-interviews"
description: "Run structured, behavioral hiring interviews and produce an Interview Execution Pack (plan, questions, scorecard, debrief). Use for interview process, interview questions, interview loop, screening, behavioral interview, structured interview. Category: Hiring & Teams."
---

# Conducting Interviews (Structured, Behavioral)

## Scope

**Covers**
- Preparing and running structured interviews (screen + loop) with consistent criteria
- Behavioral interviewing mapped to competencies/values
- Getting to “substance over polish” (avoiding “confident but shallow” signal)
- Capturing evidence, scoring consistently, and writing a debrief-ready summary

**When to use**
- “Help me conduct interviews for a <role>.”
- “Create an interview script / interview question set / scorecard for <role>.”
- “Design an interview loop and structured rubric for <role>.”
- “Improve interviewer consistency and reduce bias.”

**When NOT to use**
- You need to define the role outcomes or write the job description (use `writing-job-descriptions` first)
- You need legal/HR compliance guidance or to adjudicate complex employment risk (this skill is not legal advice)
- You need compensation/offer strategy or negotiation coaching

## Inputs

**Minimum required**
- Role + level + function (e.g., “Senior PM”, “Engineering Manager”)
- Interview stage(s) to design/run (screen, hiring manager, panel, etc.) + duration(s)
- Evaluation criteria: 4–8 competencies/values to measure (or your existing rubric)
- Company/team context candidates should know (mission, what’s hard, why now)
- Candidate materials (resume/portfolio) + any areas to probe

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If criteria aren’t provided, propose a default criteria set and clearly label it as an assumption.

## Outputs (deliverables)

Produce an **Interview Execution Pack** in Markdown (in-chat; or as files if requested):

1) **Interview plan** (stage purpose, criteria, agenda, timeboxes)
2) **Question map** (questions → competency/value → what good looks like → follow-up probes)
3) **Interviewer script** (opening, transitions, probes, close)
4) **Notes + scorecard** (rating anchors + evidence capture)
5) **Debrief summary template** (evidence-based strengths/concerns + hire/no-hire signal + follow-ups)
6) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + define the stage
- **Inputs:** user request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm role, stage(s), duration, and who else interviews. Identify must-measure criteria and any “must not” red flags.
- **Outputs:** Interview brief + assumptions/unknowns list.
- **Checks:** You can state the stage goal in one sentence (e.g., “screen for X; sell Y; decide Z”).

### 2) Lock evaluation criteria (don’t improvise later)
- **Inputs:** competencies/values; role context.
- **Actions:** Choose 4–8 criteria; define 1–2 “strong” and “weak” anchors per criterion. Ensure each criterion is observable via evidence.
- **Outputs:** Criteria table with anchors.
- **Checks:** Every criterion has a definition + evidence hints; no criterion is “vibe”.

### 3) Build the question map (behavioral first)
- **Inputs:** criteria table.
- **Actions:** Write 1–2 primary questions per criterion (behavioral: “tell me about a time…”). Add probes that force specifics (role, constraints, trade-offs, results, what you’d do differently). Add two global questions: “How did you prepare?” and “Why here?”
- **Outputs:** Question map table.
- **Checks:** Each question maps to exactly one primary criterion; no double-barreled questions.

### 4) Write the interviewer script (runbook)
- **Inputs:** question map; timeboxes.
- **Actions:** Assemble an interview flow: opening (set context + structure), question sequence, note-taking reminders, and a consistent close: “Is there anything else you want to make sure we covered?”
- **Outputs:** Interviewer script with timestamps.
- **Checks:** Script fits in time; includes “sell” moments appropriate to stage; includes candidate questions time.

### 5) Prepare for “substance over polish”
- **Inputs:** question map; candidate materials.
- **Actions:** Add “substance checks” for polished communicators (ask for concrete examples, counterfactuals, and specific decisions). Add “structure help” for less polished candidates (rephrase, clarify what’s being asked) without leading.
- **Outputs:** Substance-vs-delivery guardrails embedded in the script.
- **Checks:** The plan reduces false positives from confident delivery and false negatives from imperfect structure.

### 6) Score using evidence (immediately after)
- **Inputs:** notes; scorecard template.
- **Actions:** Fill the scorecard with evidence snippets before discussing with others. Rate each criterion with anchors. Write a 5–8 sentence evidence-based summary and list follow-up questions.
- **Outputs:** Completed notes + scorecard + summary.
- **Checks:** Every rating has supporting evidence; the overall recommendation is consistent with criterion ratings.

### 7) Debrief + quality gate + finalize pack
- **Inputs:** completed scorecard; debrief template.
- **Actions:** Produce the debrief-ready packet; run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Include Risks/Open questions/Next steps.
- **Outputs:** Final Interview Execution Pack.
- **Checks:** Clear recommendation + uncertainty; fair process; next steps defined (additional interview, reference check, work sample, etc.).

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Screen):** “Create a 30-minute phone screen for a Senior Product Manager. I want to evaluate product sense, execution, and collaboration. Output the Interview Execution Pack with a question map and scorecard.”  
Expected: timeboxed script, behavioral questions, clear anchors, and a scorecard that captures evidence.

**Example 2 (Loop):** “Design a structured interview loop for a Staff Engineer, including a hiring manager interview and a cross-functional panel. Map questions to our values and include a debrief template.”  
Expected: stage goals, consistent criteria across interviewers, and artifacts that make debriefs evidence-based.

**Boundary example:** “Just tell me if this candidate is good; I don’t have criteria or notes.”  
Response: require criteria + evidence; propose default criteria and ask the user to paste notes or run a structured interview first.
