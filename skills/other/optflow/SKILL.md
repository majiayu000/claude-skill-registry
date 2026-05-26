---
name: optflow
description: "Discover and deliver repository optimization work end to end: identify performance/reliability/maintainability/security/dx/cost optimization points, prioritize by impact-effort-risk, then execute fixes step by step with continuous testing and explicit commit policy (`final_only`, `per_step`, `milestone`). Default to `per_step` for implementation work so each feature is tested then committed before the next feature. Supports optional BDD (Given/When/Then)."
---

# Optflow

## Overview

Use this skill to discover repository optimization opportunities and execute selected optimizations end to end:
- Discover optimization points first (performance, reliability, maintainability, security, cost, DX).
- Prioritize by impact/effort/risk.
- Execute in strict sequence with validation and explicit commit policy.
- Add BDD behavior specs when requested or when requirements are ambiguous.

## Trigger Cues

Trigger this skill when the user asks for one or more of:
- Ask to find optimization opportunities in a repository/library.
- Ask for optimization roadmap + implementation.
- Require test-first optimization delivery and commit (final or per step).
- Require behavior-driven delivery (BDD) or acceptance scenarios.

## Workflow

### 0. Discover Optimization Backlog

- Scan the repository before planning changes.
- Classify findings into: performance, reliability, maintainability, security, developer experience, and cost.
- For each finding, record:
  - symptom and evidence (file/path/metric)
  - expected impact
  - effort estimate
  - risk level
- Build a prioritized backlog using impact/effort/risk.
- Explicitly mark low-confidence findings as hypotheses.

### 1. Define Ready Criteria (DoR)

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

Additional for optflow:
- If implementation is requested and commit style is not explicitly specified, use `per_step` (default).
- If user says "per step optimize and test then commit", use `per_step`.

### 2. Build Complete Plan Before Editing

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

### 3. Add BDD Layer When Needed

Use BDD if user requests it, or if requirements are unclear.

For BDD Lite, Scenario Quality Checklist, Scenario Outline, and Test Layer mapping, see the shared reference:

> [`references/bdd-guide.md`](./references/bdd-guide.md)


### 4. Execute Step by Step

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

- Treat one planned step as one feature boundary whenever possible.
- If `commit_policy = per_step` (default for implementation):
  - Stage only files for current step/feature.
  - Run step-level checks first.
  - Commit immediately after step checks pass.
  - Record step -> commit hash mapping.

### 5. Apply No-Backward-Compatibility Mode (When Requested)

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

### 6. Validate with Test Matrix

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

Per-step mandatory loop (when `commit_policy = per_step`):
1. Implement current feature step.
2. Run mapped step checks (at least one automated command).
3. If checks pass, commit this step immediately.
4. Move to next feature step.

### 7. Commit and Handoff

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

- `per_step`: each step must already be committed before next step starts.

## Output Templates

### Optimization Backlog Template

```text
Finding:
Category: <performance|reliability|maintainability|security|dx|cost>
Evidence: <file/metric/log>
Impact: <high|medium|low>
Effort: <high|medium|low>
Risk: <high|medium|low>
Priority score: <...>
Decision: <implement now|defer>
```

### Optimization Plan Template

```text
Selected Findings:
1. <finding>
2. <finding>

Execution Steps:
1. <step> (done condition: <...>)
2. <step> (done condition: <...>)

Expected Gains:
- <metric or qualitative gain>
```

## Guardrails

- Do not stop at planning when implementation is expected.
- Do not leave partially completed plan steps.
- Do not defer required testing when it can be run now.
- Do not move to the next plan step before committing when `commit_policy = per_step`.
- Do not merge multiple completed feature steps into one commit when `commit_policy = per_step`.
- Do not claim compatibility if user explicitly requested no compatibility work.
- Do not include unrelated pre-existing dirty files in commits.
- Do not hand off without concrete validation evidence.
