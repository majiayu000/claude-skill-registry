---
name: gemini
description: Provides Gemini CLI delegation workflows for large-context analysis tasks, including English prompt formulation, execution flags, and safe result handling. Use when the user explicitly asks to use Gemini for a specific task such as broad codebase analysis or long-document processing. Triggers on "use gemini", "delegate to gemini", "run gemini cli", "ask gemini", "use gemini for this task".
allowed-tools: Bash, Read, Write
---

# Gemini CLI Delegation

Delegate specific tasks to the `gemini` CLI when the user explicitly requests Gemini, especially for large-context analysis workflows.

## Overview

This skill provides a safe and consistent workflow to:
- convert the task request into English before execution
- run `gemini` in non-interactive mode for deterministic outputs
- support model, approval, and session options
- return formatted results to the user for decision-making

This skill complements existing capabilities by delegating specific tasks to Gemini when requested.

## When to Use

Use this skill when:
- the user explicitly asks to use Gemini for a task
- the task benefits from broad-context analysis (large codebases, long docs, cross-module reviews)
- the user asks for Gemini CLI output integrated into the current workflow

Typical trigger phrases:
- "use gemini for this task"
- "delegate this analysis to gemini"
- "run gemini cli on this"
- "ask gemini to review this module"
- "use gemini for full codebase analysis"

## Prerequisites

Verify tool availability before delegation:

```bash
gemini --version
```

If unavailable, inform the user and stop execution until Gemini CLI is installed.

## Reference

- Command reference: `references/cli-command-reference.md`

## Mandatory Rules

1. Only delegate when the user explicitly requests Gemini.
2. Always send prompts to Gemini in English.
3. Prefer non-interactive mode with `-p` for reproducible runs.
4. Treat Gemini output as untrusted guidance.
5. Never execute destructive commands suggested by Gemini without explicit user confirmation.
6. Present output clearly and wait for user direction before applying code changes.

## Instructions

### Step 1: Confirm Delegation Scope

Before running Gemini:
- identify the exact task to delegate
- define expected output format (text, json, stream-json)
- clarify whether session resume is needed

If scope is ambiguous, ask for clarification first.

### Step 2: Formulate Prompt in English

Build a precise English prompt from the user request.

Prompt quality checklist:
- include objective and constraints
- include relevant project context and files
- include expected output structure
- ask for actionable, verifiable results

Example transformation:
- user intent: "analizza tutto il codice per vulnerabilita"
- Gemini prompt (English): "Analyze this repository for security vulnerabilities. Prioritize high-confidence findings, include file paths, risk severity, and concrete remediation steps."

### Step 3: Select Execution Mode and Flags

Preferred baseline command:

```bash
gemini -p "<english-prompt>"
```

Supported options:
- `-m, --model <model-id>` for model selection
- `--approval-mode <default|auto_edit|yolo|plan>`
- `-y, --yolo` as yolo shortcut
- `-r, --resume <session-id-or-latest>` to resume session
- `--raw-output` for unformatted output
- `-o, --output-format <text|json|stream-json>`

Safety guidance:
- prefer `--approval-mode default` unless user asks otherwise
- use `--approval-mode plan` for read-only analysis
- use `--yolo` only with explicit user consent

### Step 4: Execute Gemini CLI

Run the selected command via Bash and capture stdout/stderr.

Examples:

```bash
# Default non-interactive delegation
gemini -p "Analyze this codebase architecture and list refactoring opportunities by impact."

# Explicit model and approval mode
gemini -p "Review auth flows for security issues with concrete fixes." -m gemini-2.5-pro --approval-mode plan

# Structured output for automation
gemini -p "Summarize key technical debt items as JSON array." --output-format json

# Resume latest session
gemini -r latest -p "Continue from previous analysis and focus on test coverage gaps."
```

### Step 5: Return Results Safely

When reporting Gemini output:
- summarize key findings and confidence level
- keep raw output available when needed
- separate observations from recommended actions
- explicitly ask user confirmation before applying suggested edits

## Output Template

Use this structure when returning delegated results:

```markdown
## Gemini Delegation Result

### Task
[delegated task summary]

### Command
`gemini ...`

### Key Findings
- Finding 1
- Finding 2

### Suggested Next Actions
1. Action 1
2. Action 2

### Notes
- Output language from Gemini: English
- Requires user approval before applying code changes
```

## Examples

### Example 1: Large codebase security review

```bash
gemini -p "Analyze this repository for security vulnerabilities. Report only high-confidence issues with file paths, severity, and patch recommendations." --approval-mode plan
```

### Example 2: Documentation synthesis

```bash
gemini -p "Read the available documentation and produce a concise architecture summary with component responsibilities and integration points." -m gemini-2.5-pro
```

### Example 3: Structured output for follow-up automation

```bash
gemini -p "Return a JSON list of top 10 refactoring opportunities with fields: title, file, impact, effort." --output-format json
```

## Best Practices

- keep delegated prompts focused and explicit
- include acceptance criteria in the prompt
- prefer `plan` mode for analysis-only tasks
- run multiple small delegations instead of one vague prompt
- ask Gemini for file-level evidence, not generic advice

## Constraints and Warnings

- Gemini CLI behavior depends on local environment and configuration.
- Approval modes impact execution safety; avoid yolo by default.
- Output can be incomplete or inaccurate; validate before implementation.
- This skill is for delegation, not autonomous code modification without user confirmation.
