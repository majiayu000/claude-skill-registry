---
name: claude-code-cli
description: Executes tasks using the Claude Code CLI (`claude`). Automatically determines the safest permission mode (plan, acceptEdits, or bypassPermissions) based on the task type.
---

# executing-claude

## Purpose

Use this skill to perform coding, research, or automation tasks using the `claude` CLI. It maps requests to Claude's native permission modes to balance automation with security.

## Permission Tiers

| Tier  | Claude Mode         | Capability                                   | Approval Required   | Typical Tasks                             |
| :---- | :------------------ | :------------------------------------------- | :------------------ | :---------------------------------------- |
| **0** | `plan`              | Read-only access, analysis, research.        | **No**              | Code review, audits, web research.        |
| **1** | `acceptEdits`       | Auto-approves file edits; prompts for shell. | **Yes**             | Refactoring, documentation, lint fixes.   |
| **2** | `bypassPermissions` | Auto-approves ALL tools (edits + shell).     | **Yes (High Risk)** | CI/CD, complex builds, automated testing. |

## Implementation Workflow

### 1. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0 (Plan)**: Does the task only involve reading code or searching for information?
- **Tier 1 (Accept Edits)**: Does the task involve modifying files but no command execution?
- **Tier 2 (Bypass Permissions)**: Does the task require running tests, build scripts, or managing dependencies autonomously?

### 2. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `claude` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Accept Edits/Bypass Permissions] permissions to [modify files/run shell commands]. OK to proceed?"

### 3. Execution

Execute `claude` using the mode determined by the tier.

```bash
# Tier 0 (Plan)
claude -p "<prompt>" --permission-mode plan

# Tier 1 (Accept Edits)
claude -p "<prompt>" --permission-mode acceptEdits

# Tier 2 (Bypass Permissions)
claude -p "<prompt>" --permission-mode bypassPermissions
```

**Security Rules:**

- **NEVER** use `--permission-mode bypassPermissions` without explicit confirmation of the risks.
- **ALWAYS** use the most restrictive mode possible (prefer `plan`).
- If you are unsure, default to `plan` and escalate only if `claude` reports it cannot complete the task.

## Configuration

This skill leverages native `claude` CLI flags to enforce the permission tiers. No additional configuration files are required.

## Examples

Refer to [references/usage-examples.md](./references/usage-examples.md) for concrete scenarios.
