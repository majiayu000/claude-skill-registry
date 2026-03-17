---
name: prd
description: "Generate an ML-centric PRD for ML-Ralph. Use when planning an ML project, experiment plan, or when asked to create an ML PRD. Triggers on: create a prd, write prd for, plan this ML feature, requirements for, spec out."
---

# ML PRD Generator

Create ML-centric PRDs that are evidence-driven, stack-agnostic, and suitable for ML-Ralph.

---

## The Job

1. Receive a project description
2. Ask 3-5 essential clarifying questions (one at a time)
3. Generate a structured ML PRD
4. Save to `tasks/prd-[feature-name].md`

**Important:** Do NOT start implementing. Just create the PRD.

---

## Step 1: Clarifying Questions (One at a Time)

Focus on:
- **Objective/Metric:** What is success? What metric matters?
- **Data Context:** What data exists? Any leakage risks? Any constraints?
- **Evaluation:** What validation scheme is appropriate?
- **Scope:** What should NOT be done?

**Example format:**
```
1) What is the primary objective?
   A. Classification
   B. Regression
   C. Ranking
   D. Other: [specify]
```

---

## Step 2: PRD Structure

Generate the PRD with these sections:

### 1. Introduction/Overview
Brief description of the ML task and why it matters.

### 2. Goals
Specific, measurable objectives (bullet list).

### 3. Assumptions
Explicit assumptions (data availability, metric definitions, constraints).

### 4. Evaluation Plan
- Metric definition
- Split strategy (random/stratified/group/time)
- Leakage rules

### 5. User Stories (ML-centric)
Each story must include:
- **Title**
- **Description**
- **Type**: discovery | experiment | evaluation | implementation | ops
- **Hypothesis** (optional but preferred)
- **Evidence Required** (what must be logged, including W&B run URL/ID for experiment/evaluation stories)
- **Acceptance Criteria** (verifiable)

**Format:**
```markdown
### US-001: [Title]
**Description:** As a [role], I want [outcome] so that [benefit].
**Type:** discovery | experiment | evaluation | implementation | ops
**Hypothesis:** If ..., then ... because ...
**Evidence Required:** [What must appear in progress.jsonl or artifacts; include W&B run URL/ID for experiment/evaluation stories]

**Acceptance Criteria:**
- [ ] Specific, verifiable criterion
- [ ] Another criterion
- [ ] Ruff check passes
- [ ] Ruff format passes
- [ ] Mypy passes
- [ ] Pytest passes (if tests exist)
- [ ] Evidence logged in progress.jsonl
```

**Important:**
- Stories must be small enough for one iteration.
- Acceptance criteria must be verifiable.
- Include evidence logging for every story.

### 6. Functional Requirements
Numbered list of required behaviors or components.

### 7. Non-Goals (Out of Scope)
Explicitly list what will not be done.

### 8. Risks / Uncertainties
Known unknowns and how they’ll be resolved.

### 9. Success Metrics
Define “done” in measurable terms.

### 10. Open Questions
Remaining questions that might alter the plan.

---

## ML-Ralph Dynamic Backlog Guidance

PRDs are **living** documents. ML-Ralph may refine `prd.json` each iteration based on evidence:
- add/split/reorder/supersede stories
- never delete stories
- log changes in `progress.jsonl`

---

## Output

- **Format:** Markdown (`.md`)
- **Location:** `tasks/`
- **Filename:** `prd-[feature-name].md` (kebab-case)
