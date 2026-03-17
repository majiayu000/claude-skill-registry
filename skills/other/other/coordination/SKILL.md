---
name: meta-optimize
description: The "Self-Refining" Engine. Analyzes failure patterns in other skills (e.g., `ci-autofix` failing repeatedly) and rewrites their prompts/logic to improve future performance.
triggers: [optimize skill, refine prompt, improve agent, meta-learning, self-evolution, fix recurring error]
context_cost: high
---

# Meta-Optimize Skill

## Goal
Enable the Agentic System to "Learn" from its mistakes by rewriting its own instructions (Skills and Prompts).

## Flow

### 1. Failure Pattern Analysis
**Input**: `metrics/analytics.jsonl` or Task Failure Logs.
**Trigger**: A specific skill has failed > 3 times with the *same error type*.
**Action**: Retrieve the `.skill.md` file for the failing skill.

### 2. Diagnosis (The "Why")
Ask the **Meta-Architect Persona**:
*   "Why did `ci-autofix` fail to solve `TS2322`?"
*   *Hypothesis*: "The prompt didn't specify checking `tsconfig.json` strictness."

### 3. Optimization (The "Rewrite")
**Action**: Edit the target `.skill.md` file.
*   **Add Context**: Insert a new "Tip" or "Strategy" block.
*   **Refine Prompt**: Clarify the specific instruction causing ambiguity.
*   **Example**:
    *   *Before*: "Fix the type error."
    *   *After*: "Fix the type error. CHECK `tsconfig.json` first. Do not use `any` unless absolutely necessary."

### 4. Validation
**Action**: Run a "Regression Test" (if available) or wait for next execution.
*   Log the change in `meta-evolution.log`: "Updated ci-autofix.skill.md: Added tsconfig check."

## Safety Guardrails
*   **Backup**: Always backup the original `.skill.md` before overwriting.
*   **Limit**: Max 1 optimization per skill per day (prevent "drift").
*   **Human Review**: Flag the optimization for human review in `project/tasks.md`.
