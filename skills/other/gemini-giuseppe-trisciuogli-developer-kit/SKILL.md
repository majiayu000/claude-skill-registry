---
name: gemini
description: Provides Gemini CLI delegation workflows for large-context analysis and complex reasoning using Gemini 3.0 Flash and Gemini 3.0 Pro models, including English prompt formulation, execution flags, and safe result handling. Use when the user explicitly asks to use Gemini for tasks such as broad codebase analysis, fast iterations with Gemini 3 Flash, or deep architectural reasoning with Gemini 3 Pro. Triggers on "use gemini", "delegate to gemini", "run gemini cli", "ask gemini", "use gemini for this task", "use gemini 3 flash", "use gemini 3 pro".
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

### Model Selection Guide

Choose the appropriate model based on task complexity:

| Model | Best For | Characteristics |
|-------|----------|-----------------|
| **gemini-3-flash** | Quick iterations, prototyping, cost-sensitive tasks | Fast, cost-effective, great for simple tasks and quick feedback |
| **gemini-3-pro** | Complex reasoning, architectural design, production-quality outputs | Powerful, deeper reasoning, higher-quality output |

**Selection tips**:
- Start with `gemini-3-flash` for quick iterations and prototyping
- Use `gemini-3-pro` for production-quality analysis and complex reasoning
- Reserve `gemini-3-pro` for tasks where accuracy and depth are prioritized over speed
- If unsure, default to `gemini-3-flash` for faster feedback cycles and iterate to `gemini-3-pro` if needed

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
gemini -p "Review auth flows for security issues with concrete fixes." -m gemini-3-pro --approval-mode plan

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
gemini -p "Analyze this repository for security vulnerabilities. Report only high-confidence issues with file paths, severity, and patch recommendations." -m gemini-3-flash --approval-mode plan
```

### Example 2: Documentation synthesis

```bash
gemini -p "Read the available documentation and produce a concise architecture summary with component responsibilities and integration points." -m gemini-3-pro --approval-mode plan
```

### Example 3: Structured output for follow-up automation

```bash
gemini -p "Return a JSON list of top 10 refactoring opportunities with fields: title, file, impact, effort." -m gemini-3-flash --output-format json
```

### Example 4: Quick boilerplate generation

```bash
gemini -p "Generate a minimal Express.js REST endpoint for POST /items with input validation and a unit test. Keep the implementation concise and ready to paste." -m gemini-3-flash
```

### Example 5: Cost-effective CSV summary (fast, low-cost)

```bash
gemini -p "Summarize this CSV file's key statistics: row count, missing-value counts, and top 5 columns by variance. Provide a 6-line bullet summary suitable for quick triage." -m gemini-3-flash --output-format json --approval-mode plan
```

### Example 6: Fast iteration for microcopy prototyping

```bash
gemini -p "Provide 3 short alternative microcopy options (<=20 words each) for an onboarding tooltip that explains account recovery. Include a one-line A/B test metric proposal for each option." -m gemini-3-flash
```

### Example 7: Architectural design analysis

```bash
gemini -p "Analyze the current system architecture and propose a detailed migration strategy to a microservices architecture. Include component boundaries, communication patterns, data ownership, and estimated risks for each migration step." -m gemini-3-pro --approval-mode plan
```

### Example 8: Comprehensive security audit

```bash
gemini -p "Perform a thorough security audit of the authentication and authorization layer. Identify potential vulnerabilities, rate-limiting gaps, token handling weaknesses, and injection vectors. Provide severity ratings and specific remediation steps for each finding." -m gemini-3-pro --approval-mode plan
```

### Example 9: Production-quality module generation

```bash
gemini -p "Generate a production-ready TypeScript module for paginated API responses. Include input validation, error handling, retry logic with exponential backoff, and comprehensive unit tests with mocks. Follow best practices for error types, logging, and type safety." -m gemini-3-pro --approval-mode auto_edit
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
