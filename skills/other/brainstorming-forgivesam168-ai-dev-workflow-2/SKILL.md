---
name: brainstorming
description: 'Start a work item: triage risk, run structured brainstorming to clarify requirements, compare solution options, and produce a decision log + change package skeleton.'
license: MIT
---

# Brainstorming

## When to Use
Use this skill at the **start of any request/change** when:
- Requirements are ambiguous or incomplete
- The change touches security, auth/authz, data flow, CI/CD, or supply chain
- There are multiple plausible implementation approaches
- You need a rationale trail (auditability)

## Workflow

### Phase 0 — Intake & Risk Classification
- Clarify goals/non-goals and acceptance criteria
- Classify risk: **Low** / **Med** / **High**
- Determine if this is brownfield (existing system)
- Decide workflow path:
  - **Standard**: brainstorm → plan → tdd → review
  - **Fast** (low-risk only): plan → tdd → review

### Phase 1 — Clarify
- Ask 3–8 targeted questions (scope, constraints, stakeholders, non-goals)
- List assumptions if the user cannot answer immediately

### Phase 2 — Explore Options
- Produce 2–3 options
- For each: complexity (L/M/H), risks, dependencies, rollback strategy

### Phase 3 — Decide & Record
- Recommend one option and justify
- Produce a **Decision Log** entry (append-only)

### Phase 4 — Change Package Skeleton
- Propose a `changes/<YYYY-MM-DD>-<slug>/` directory
- Provide copy/paste-ready stubs:
  - `01-brainstorm.md`
  - `02-decision-log.md`
  - `03-spec.md` (draft)

## Output Template
- Risk Classification (Low/Med/High)
- Workflow Path Recommendation (Standard/Fast)
- Questions (if needed)
- Assumptions & Constraints
- Options (2–3)
- Recommendation
- Decision Log
- Change Package Skeleton (file stubs)

## Output Mapping (Change Package)
Write results into:
- `changes/<YYYY-MM-DD>-<slug>/01-brainstorm.md`
- `changes/<YYYY-MM-DD>-<slug>/02-decision-log.md`
- Draft/Update `changes/<...>/03-spec.md` (minimum scope + verification)

If the change folder does not exist yet, propose a folder name and include the content in your response so it can be pasted into the files.
