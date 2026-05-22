---
name: gemini-cli
description: Executes tasks using the Gemini CLI (`gemini`). Automatically determines the safest approval mode (plan, auto_edit, or yolo) based on the task type.
---

# executing-gemini

## Purpose

Use this skill to perform coding, research, or automation tasks using the `gemini` CLI. It maps requests to Gemini's native approval modes to balance automation with security.

## Permission Tiers

| Tier  | Gemini Mode | Capability                                   | Approval Required   | Typical Tasks                             |
| :---- | :---------- | :------------------------------------------- | :------------------ | :---------------------------------------- |
| **0** | `plan`      | Read-only access, analysis, research.        | **No**              | Code review, audits, web research.        |
| **1** | `auto_edit` | Auto-approves file edits; prompts for shell. | **Yes**             | Refactoring, documentation, lint fixes.   |
| **2** | `yolo`      | Auto-approves ALL tools (edits + shell).     | **Yes (High Risk)** | CI/CD, complex builds, automated testing. |

## Implementation Workflow

### 1. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0 (Plan)**: Does the task only involve reading code or searching for information?
- **Tier 1 (Auto-Edit)**: Does the task involve modifying files but no command execution?
- **Tier 2 (YOLO)**: Does the task require running tests, build scripts, or managing dependencies autonomously?

### 2. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `gemini` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Auto-Edit/YOLO] permissions to [modify files/run shell commands]. OK to proceed?"

### 3. Execution

Execute `gemini` using the mode determined by the tier.

```bash
# Tier 0 (Plan)
gemini -p "<prompt>" --approval-mode plan --sandbox

# Tier 1 (Auto-Edit)
gemini -p "<prompt>" --approval-mode auto_edit

# Tier 2 (YOLO)
gemini -p "<prompt>" --approval-mode yolo
```

**Security Rules:**

- **NEVER** use `--approval-mode yolo` without explicit confirmation of the risks.
- **ALWAYS** use the most restrictive mode possible (prefer `plan`).
- If you are unsure, default to `plan` and escalate only if `gemini` reports it cannot complete the task.

## Configuration

This skill leverages native `gemini` CLI flags to enforce the permission tiers. No additional configuration files are required.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
