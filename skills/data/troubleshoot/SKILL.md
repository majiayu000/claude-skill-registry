---
name: troubleshoot
description: Isolate root causes and propose targeted fixes with clear validation steps.
---

# Troubleshoot

## Objective
- Reproduce and isolate the issue.
- Identify the most probable root cause and next actions.

## When to use
- A bug or failure is reported or observed.
- Symptoms are unclear and need narrowing down.

## Inputs
- User-reported symptoms, logs, or reproduction steps.
- AGENTS.md, rules, relevant code/tests.
- Environment details if available.

## Process
1) Confirm and restate the symptom; note missing repro info.
2) Form quick hypotheses; prioritize simplest checks.
3) Collect minimal evidence (logs/tests/inputs) to confirm/deny hypotheses.
4) Identify the likely root cause or narrow to top candidates.
5) Propose next actions (fix path or deeper check) and validation steps.

## Outputs
- Likely root cause (or narrowed hypotheses).
- Evidence collected and what’s still unknown.
- Proposed fix direction and validation plan.

## Edge cases
- If repro is missing, request exact steps or data.
- Avoid broad changes; focus on evidence-driven narrowing.
