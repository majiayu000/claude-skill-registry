---
name: codex-cli
description: Executes tasks using the Codex CLI (`codex`). Automatically determines the least privilege required (Read-Only, Editor, or Autonomous) based on the user's request and handles security approvals.
---

# executing-codex

## Purpose

Use this skill to perform coding tasks, research, or system analysis using the `codex` CLI. This skill follows the Principle of Least Privilege by automatically mapping requests to the safest possible profile and gating dangerous operations behind user approval.

## Permission Tiers

| Tier  | Profile      | Capability                         | Approval Required | Typical Tasks                          |
| :---- | :----------- | :--------------------------------- | :---------------- | :------------------------------------- |
| **0** | `readonly`   | Read files, live search, analysis. | **No**            | Research, code review, explanation.    |
| **1** | `editor`     | File edits, cached search.         | **Yes**           | Refactoring, bug fixes, formatting.    |
| **2** | `autonomous` | Edits + Sandbox commands.          | **Yes**           | Testing, building, dependency updates. |

## Implementation Workflow

### 1. Analyze & Classify

Analyze the user's intent to determine the required permission tier.

- **Tier 0**: Does the task only involve reading code or searching for information?
- **Tier 1**: Does the task involve modifying files but no command execution?
- **Tier 2**: Does the task require running tests, build scripts, or managing dependencies?

### 2. Approval Protocol

If the task maps to **Tier 1** or **Tier 2**, you **MUST** obtain user approval before executing the `codex` command.

Use the `AskQuestion` tool to confirm:

> "I've detected that this task requires [Editor/Autonomous] permissions to [modify files/run commands]. OK to proceed?"

### 3. Execution

Execute `codex` using the flags corresponding to the tier.

```bash
# Tier 0 (Read-only)
codex -q "<prompt>"

# Tier 1 (Editor)
codex --auto-edit "<prompt>"

# Tier 2 (Autonomous)
codex --full-auto "<prompt>"
```

**Security Rules:**

- **NEVER** use `--dangerously-auto-approve-everything`.
- **ALWAYS** use the most restrictive flags possible.
- If you are unsure, default to Tier 0 (`-q`) and escalate only if `codex` reports it cannot complete the task.

## Configuration

This skill leverages native `codex` CLI flags to enforce the permission tiers. No additional configuration files are required.

## Examples

### Research (Tier 0)

> User: "What are the latest best practices for Python packaging in 2026?"
> Action: Execute `codex --profile readonly "..."`

### Refactor (Tier 1)

> User: "Rename the 'User' class to 'Account' across the whole repo."
> Action:
>
> 1. Request approval for `editor` profile.
> 2. Execute `codex --profile editor "..."`

### Automated Testing (Tier 2)

> User: "Run the test suite and fix any failures found."
> Action:
>
> 1. Request approval for `autonomous` profile.
> 2. Execute `codex --profile autonomous "..."`
