---
name: vibeguard
description: Lightweight anti-hallucination workflow for task kickoff, review prioritization, and regression retrospectives. Use when the user asks for guardrails, task contracts, risk scoring, or review templates.
---

# VibeGuard

Lightweight VibeGuard for everyday use inside Spellbook.

This skill helps with three moments where AI-assisted work usually drifts:
- before implementation starts
- while review findings are being prioritized
- after regressions or avoidable mistakes happen

## What This Skill Includes

- A task contract checklist for scoping work before coding
- A scoring matrix for prioritizing findings with evidence
- A weekly review template for regression and guardrail retrospectives

## Hard Boundaries

This skill is intentionally lightweight.

It does:
- guide task kickoff
- structure review output
- make risk tradeoffs explicit

It does not:
- install hooks
- run guard scripts automatically
- patch global Claude or Codex configuration
- claim that full VibeGuard enforcement is active

If the user asks for automated interception, repo-level rules, or environment setup, escalate to the full VibeGuard repository and tooling.

## When To Use It

Trigger this skill when the user asks for:
- anti-hallucination guardrails
- task startup checks
- review scoring or triage
- regression prevention
- retrospective templates
- "vibeguard" by name

## Workflow

### 1. Start With The Task Contract

Open [`references/task-contract.yaml`](./references/task-contract.yaml) and confirm:
- goal
- source of truth
- acceptance criteria
- scope

Do not move into implementation until these are concrete.

### 2. Score Findings Before Acting

Open [`references/scoring-matrix.md`](./references/scoring-matrix.md) and score each finding on:
- impact
- effort
- risk
- confidence

Use the score to separate urgent fixes from weak guesses.

### 3. Pick The Right Delivery Mode

- 1-2 files: implement directly once the contract is clear
- 3-5 files: write a short spec or step plan first
- 6+ files: produce a full design/spec and staged execution plan

### 4. Review The Failure, Not Just The Symptom

If something regressed, identify which defense failed:
- scope control
- source-of-truth validation
- verification depth
- review prioritization
- missing guardrail

Then capture the follow-up in [`references/review-template.md`](./references/review-template.md).

## Expected Outputs

Depending on the request, produce one of these:
- a filled task contract
- a scored findings table with priorities
- a short regression review or weekly retrospective

## Reference Files

- [`references/task-contract.yaml`](./references/task-contract.yaml) - kickoff checklist
- [`references/scoring-matrix.md`](./references/scoring-matrix.md) - prioritization model
- [`references/review-template.md`](./references/review-template.md) - retrospective template
