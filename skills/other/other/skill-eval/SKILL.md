---
name: skill-eval
description: Evaluate skill performance against test cases
version: 1.1.0
tags: [meta, testing, evaluation]
owner: orchestration
status: active
---

# Skill Eval Skill

## Overview

Evaluate skill behavior against predefined scenarios.

## Usage

```
/eval-skill <skill-name>
```

## Identity
**Role**: Agent Evaluator
**Objective**: Run a specific skill against a known scenario and score the output.

## Workflow
**Command**: `/eval-skill <skill-name>`

### 1. Setup Scenario
- **Input**: A `test-cases` directory (e.g., `.claude/skills/<skill>/tests/`).
- **Context**: Create a temporary sandbox directory. Copy fixture files.

### 2. Execution
- **Prompt**: detailed instruction invoking the skill.
- **Run**: Execute the skill (simulated or real).

### 3. Verification
- **Assert**: Check for existence of files, content of files, or specific string outputs.
- **Score (1-5)**:
  - 5: Perfect execution, followed constraints.
  - 4: Worked but minor deviation.
  - 3: Worked but required human intervention.
  - 1: Failed.

## Output
- `eval_report.md`: Summary of pass/fail.

## Outputs

- Skill evaluation score and notes.

## Related Skills

- `/skill-creator` - Create new skills
