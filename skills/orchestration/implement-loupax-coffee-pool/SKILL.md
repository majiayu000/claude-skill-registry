---
name: implement
description: Run the full orchestrator → developer → qa pipeline for a game implementation task. Use when the user asks to implement, add, or change something in the PICO-8 codebase.
argument-hint: <task description>
allowed-tools: Agent, Read, Glob, Grep, Bash
---

Run the full implementation pipeline for the following task: $ARGUMENTS

## Pipeline

### Step 1 — Orchestrate (inline)
Research the task directly:
- Read `barista.p8` to understand current code state
- Identify scope, affected systems (physics, scoring, UI, levels, state machine)
- Produce a precise, scoped implementation brief
- Consider token budget impact

### Step 2 — Develop
Spawn an Agent with `subagent_type: "developer"` and a clear, scoped task prompt including exact file paths, line numbers, and instructions.
Collect the developer's report: file paths, line numbers, assumptions, token impact.

### Step 3 — QA
Spawn an Agent with `subagent_type: "qa"` and a review prompt describing what was changed and what to validate.
Collect the verdict: PASS / FAIL / PASS WITH NOTES with findings.

### Step 4 — Act on QA findings
- If FAIL: send the developer back with specific fixes, then re-run QA
- If PASS WITH NOTES: address notes or document them as follow-up
- If PASS: report to the user — do not auto-commit

### Step 5 — Report
Summarize the full pipeline result to the user:
- What was changed and where
- QA verdict and any findings
- Token budget impact
