---
name: "evaluating-candidates"
description: "Make an evidence-based hiring decision and produce a Candidate Evaluation Decision Pack (criteria + scorecard, signal log, work sample/trial plan + rubric, reference check script + summary, decision memo). Use for candidate evaluation, hiring decisions, reference checks, work samples/take-homes, and hiring bar calibration. Category: Hiring & Teams."
---

# Evaluating Candidates

## Scope

**Covers**
- Defining an explicit **hiring bar** (what “great” means for this role at this company, right now)
- Turning interviews, work samples/trials, and references into **evidence**, not vibes
- Designing **job-relevant** work samples (and **paid trials** when appropriate)
- Running high-signal **reference checks** and integrating them into the decision
- Producing a decision-ready recommendation with clear risks and mitigations

**When to use**
- “Help me decide whether to hire this candidate.”
- “Create a scorecard and decision memo based on interview notes + references.”
- “Design a work sample / take-home (or paid trial) and a scoring rubric.”
- “Plan and run reference checks; give me a summary and recommendation.”
- “Calibrate our hiring bar for a <role> and compare candidates fairly.”

**When NOT to use**
- You need to define the role outcomes or write the job description (use `writing-job-descriptions`)
- You need to design/run structured interviews and question maps (use `conducting-interviews`)
- You need legal/HR compliance guidance or to adjudicate high-risk employment issues (this skill is not legal advice)
- You need compensation/offer negotiation strategy

## Inputs

**Minimum required**
- Role + level + function (e.g., “Senior PM”, “Founding AE”, “Staff ML Engineer”)
- Company/team context and “what’s hard” (stage, constraints, velocity expectations)
- Evaluation criteria (4–8 competencies) and any non-negotiables / red flags
- Candidate materials available (resume/portfolio + interview notes, if already interviewed)
- Which signals you want to include: interviews, work sample/take-home, paid trial, references
- Constraints: timeline, confidentiality/PII rules, internal-only vs shareable output

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If criteria or notes are missing, propose a **default criteria set** and clearly label assumptions.
- Do not request secrets. If notes contain sensitive info, ask for **redacted excerpts** or summaries.

## Outputs (deliverables)

Produce a **Candidate Evaluation Decision Pack** in Markdown (in-chat; or as files if requested):

1) **Evaluation brief** (role success definition, criteria, weights, red flags)
2) **Scorecard** (rating anchors + evidence capture)
3) **Signal log** (all signals normalized into one table with evidence)
4) **Work sample / take-home / paid trial plan + rubric** (if used)
5) **Reference check kit** (outreach, script, note form, summary)
6) **Candidate comparison** (if multiple candidates)
7) **Hiring decision memo** (recommendation + risks + mitigations)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + decision framing
- **Inputs:** user context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm role, level, must-haves, and the decision timeline. Identify which signals exist vs need to be created (work sample, trial, references). Record constraints (PII, internal-only, fairness).
- **Outputs:** Context snapshot + assumptions/unknowns list.
- **Checks:** The decision and decision date are explicit (who decides, by when, using which signals).

### 2) Define the bar + criteria (don’t improvise later)
- **Inputs:** role context; existing rubric/values (if any).
- **Actions:** Choose 4–8 criteria; define what “strong / acceptable / weak” looks like with observable anchors. Add explicit red flags. Decide whether to prioritize **raw ability + drive** vs “years of experience” for this role.
- **Outputs:** Evaluation brief + draft scorecard.
- **Checks:** Every criterion is measurable via evidence; no criterion is “vibe” or “culture fit” without definition.

### 3) Build the signal plan + evidence log
- **Inputs:** existing notes; planned stages.
- **Actions:** Decide what each signal is responsible for (interviews = behavioral evidence; work sample = in-context execution; references = longitudinal performance). Create a single signal log so you can compare apples-to-apples.
- **Outputs:** Signal plan + signal log table (empty or partially filled).
- **Checks:** No single signal dominates by default; reference checks and work samples have defined weight when used.

### 4) Design (or evaluate) the work sample / take-home / paid trial
- **Inputs:** role outputs; constraints; candidate seniority.
- **Actions:** Create a job-relevant task with clear deliverables and scoring rubric. If the task is >2–3 hours or resembles real work, prefer a **paid** trial and clarify IP/confidentiality boundaries.
- **Outputs:** Work sample/trial brief + scoring rubric.
- **Checks:** Task predicts real performance, is fair across backgrounds, and has objective scoring anchors.

### 5) Run reference checks (highest-signal when done well)
- **Inputs:** reference targets; outreach constraints; question bank.
- **Actions:** Prioritize references who worked with the candidate for extended periods and in similar contexts. Ask for specific examples, deltas over time, strengths/limits, and “how would you staff them?” Capture verbatim evidence and calibrate for bias.
- **Outputs:** Reference notes + reference summary.
- **Checks:** Summary contains concrete examples and clear hire/no-hire signal, not generic praise.

### 6) Synthesize signals → recommendation + risk mitigation
- **Inputs:** scorecard, signal log, work sample results, reference summary.
- **Actions:** Write a decision memo that cites evidence, calls out disagreements/uncertainty, and proposes mitigations (onboarding plan, coaching, 30/60/90 checkpoints) if hiring.
- **Outputs:** Hiring decision memo + candidate comparison (if applicable).
- **Checks:** Recommendation matches the weighted evidence; red flags are explicitly addressed.

### 7) Quality gate + calibration + finalize pack
- **Inputs:** full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add **Risks / Open questions / Next steps**. If uncertain, propose the smallest additional signal to resolve (targeted reference, scoped trial, specific follow-up interview).
- **Outputs:** Final Candidate Evaluation Decision Pack.
- **Checks:** Evidence is sufficient for the decision; limitations and fairness risks are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (final decision):** “Here are interview notes for a Senior PM candidate. Create a scorecard, summarize signals, and write a hiring decision memo. Include risks and suggested mitigations.”  
Expected: scorecard with anchors + evidence, signal log, decision memo with explicit risks.

**Example 2 (work sample + references):** “We’re hiring a Founding Engineer. Design a 2-day paid trial task and rubric, plus a reference check script. Then show how we should combine those signals into a hire/no-hire decision.”  
Expected: trial brief + rubric, reference kit, and a synthesis framework.

**Boundary example:** “Tell me if this person is good. I only have their resume.”  
Response: require criteria + at least one high-signal input (structured interview notes, work sample plan/results, or references); propose a minimal evaluation plan and list assumptions/unknowns.
