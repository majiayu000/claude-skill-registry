---
name: qwen-coder
description: Provides Qwen Coder CLI delegation workflows for coding tasks using Qwen2.5-Coder and QwQ models, including English prompt formulation, execution flags, and safe result handling. Use when the user explicitly asks to use Qwen for tasks such as code generation, refactoring, debugging, or architectural analysis. Triggers on "use qwen", "use qwen coder", "delegate to qwen", "ask qwen", "second opinion from qwen", "qwen opinion", "continue with qwen", "qwen session".
allowed-tools: Bash, Read, Write
---

# Qwen Coder CLI Delegation

Delegate selected tasks from Claude Code to Qwen Coder CLI using non-interactive commands, explicit model selection, safe permission flags, and shareable outputs.

## Overview

This skill standardizes delegation to Qwen Coder CLI (`qwen`) for cases where Qwen's specific strengths may benefit the task. It covers:

- Non-interactive execution with `-p` / `--prompt`
- Model selection with `-m` / `--model`
- Approval control (`--approval-mode`)
- Session continuation with `-c` / `--continue` or `-r` / `--resume`
- Output format options (`text`, `json`, `stream-json`)

Use this skill only when delegation to Qwen Coder is explicitly requested or clearly beneficial.

## When to Use

Use this skill when:

- The user asks to delegate work to Qwen Coder CLI
- The user wants a second opinion from Qwen Coder on a task
- The user asks for Qwen Coder CLI output integrated into the current workflow
- The user wants to continue a previous Qwen Coder session

Trigger phrases:

- "use qwen"
- "use qwen coder"
- "delegate to qwen"
- "ask qwen"
- "second opinion from qwen"
- "qwen opinion"
- "continue with qwen"
- "qwen session"

## Prerequisites

Verify tool availability and authentication before delegation:

```bash
# CLI availability
qwen --version

# Authentication status
qwen auth status
```

If `qwen` is unavailable, inform the user and stop execution until Qwen Coder CLI is installed.
If authentication is invalid, provide authentication setup instructions and stop execution.

## Reference

- Command reference: `references/cli-command-reference.md`

## Instructions

### 1) Confirm Delegation Scope

Before running Qwen Coder:

- Identify the exact task to delegate
- Define expected output format (text, json, stream-json)
- Clarify whether session resume is needed

If scope is ambiguous, ask for clarification first.

### 2) Formulate Prompt in English

All delegated prompts to Qwen Coder CLI must be in English.

Build a precise English prompt from the user request.

Prompt quality checklist:

- Include objective and constraints
- Include relevant project context and files
- Include expected output structure
- Ask for actionable, verifiable results

Prompt template:

```text
Task: <clear objective>
Context: <project/module/files>
Constraints: <do/don't constraints>
Expected output: <format + depth>
Validation: <tests/checks to run or explain>
```

### 3) Select Execution Mode and Flags

Preferred baseline command:

```bash
qwen -p "<english-prompt>"
```

Supported options:

- `-m, --model <model-id>` for model selection (default: qwen2.5-coder)
- `--approval-mode <plan|default|auto_edit|yolo>` for safety control
- `-c, --continue <session-id>` to continue previous session
- `-r, --resume <session-id>` as alias for continue
- `-o, --output-format <text|json|stream-json>` for output format

Approval modes:

| Mode | Behavior | Recommended For |
|------|----------|-----------------|
| `plan` | Read-only analysis, no file modifications | Analysis-only tasks, security reviews |
| `default` | Requires confirmation before modifications | General coding tasks |
| `auto_edit` | Auto-approves edit operations | Trusted modifications with oversight |
| `yolo` | Approves all operations without confirmation | Experimental tasks (explicit user request only) |

Safety guidance:

- Prefer `--approval-mode plan` for read-only analysis
- Use `--approval-mode default` for general tasks
- Reserve `--yolo` for explicit user requests only

### 4) Execute Qwen Coder CLI

Run the selected command via Bash and capture stdout/stderr.

Examples:

```bash
# Default non-interactive delegation
qwen -p "Analyze this code and suggest refactoring improvements."

# Explicit model and approval mode
qwen -p "Review authentication module for security issues with fixes." -m qwq --approval-mode plan

# Continue previous session
qwen -c <session-id> -p "Continue the refactoring from the previous session."

# Structured output for automation
qwen -p "Summarize key technical debt items as JSON array." --output-format json
```

### 5) Result Handling

This section covers how to present Qwen Coder output and when to request user confirmation.

#### 5.1) Output Presentation

When reporting Qwen Coder output:

- Present output in a clear, readable format
- Summarize key findings and confidence level
- Separate observations from recommended actions
- Keep raw output available when needed
- Include the model used and approval mode applied
- State which permission profile was in effect

#### 5.2) Confirmation Workflow

Before applying any suggested modifications:

1. Present the proposed changes to the user in the output template format
2. Request explicit confirmation (for example: "Do you want me to apply these changes?")
3. Wait for user direction before proceeding
4. Do not auto-apply changes without user consent

Exception: In `--approval-mode yolo` with explicit user request, changes may proceed automatically. Still inform the user of what was done.

#### 5.3) Result Metadata

Each delegation result shall include the following metadata:

| Field | Description |
|-------|-------------|
| Task summary | What was delegated to Qwen Coder |
| Command | The qwen command executed (without sensitive parameters) |
| Model | Which model was used (for example qwen2.5-coder, qwq) |
| Approval mode | The approval mode applied (plan, default, auto_edit, yolo) |
| Key findings | Observations and results from Qwen Coder |
| Suggested next actions | Recommended follow-up steps (if applicable) |

## Output Template

Use this structure when returning delegated results:

```markdown
## Qwen Coder Delegation Result

### Task
[delegated task summary]

### Command
`qwen ...`

### Key Findings
- Finding 1
- Finding 2

### Suggested Next Actions
1. Action 1
2. Action 2

### Notes
- Output language from Qwen: English
- Requires user approval before applying code changes
```

## Examples

### Example 1: Code analysis with QwQ deep reasoning

**Input:**

```text
Analyze the authentication module and identify security vulnerabilities.
```

**Command:**

```bash
qwen -p "Analyze the authentication module for security vulnerabilities. Report only high-confidence issues with severity, file paths, and remediation steps." -m qwq --approval-mode plan
```

**Expected behavior:**

```text
Returns a structured analysis with high-confidence security findings, including severity ratings and specific remediation recommendations.
```

### Example 2: Code refactoring with Qwen2.5-Coder

**Input:**

```text
Refactor the payment service to reduce code duplication while keeping the public API unchanged.
```

**Command:**

```bash
qwen -p "Refactor the payment service in src/services/payment.ts to reduce duplication. Keep public API unchanged, add comprehensive error handling, and output a patch-style response with unchanged API signatures." -m qwen2.5-coder --approval-mode default
```

**Expected behavior:**

```text
Proposes concrete code changes (patch-style), extracts duplication into shared helpers, and maintains original API contracts.
```

### Example 3: Documentation generation

**Input:**

```text
Generate documentation for the UserService class including usage examples.
```

**Command:**

```bash
qwen -p "Generate comprehensive documentation for the UserService class. Include: class purpose, public methods with parameters, usage examples, and error handling patterns. Format as markdown." -m qwen2.5-coder --approval-mode plan
```

**Expected behavior:**

```text
Returns markdown-formatted documentation with JSDoc-style comments, method signatures, and practical usage examples.
```

### Example 4: Code generation with model selection

**Input:**

```text
Generate a REST API endpoint for CRUD operations on items.
```

**Command:**

```bash
qwen -p "Generate a production-ready REST API endpoint for CRUD operations on items. Include input validation, error handling, and unit tests. Use Express.js framework." -m qwen2.5-coder --approval-mode auto_edit
```

**Expected behavior:**

```text
Generates complete, runnable code for POST/GET/PUT/DELETE endpoints with proper middleware, validation, and test scaffolding.
```

### Example 5: Session resume for continued work

**Input:**

```text
Continue the previous Qwen session to add test coverage to the refactored code.
```

**Command:**

```bash
qwen -c <session-id> -p "Continue from the previous session. Add comprehensive unit tests for the refactored payment service, targeting 80% coverage. Include mocks for external dependencies." -m qwen2.5-coder --approval-mode default
```

**Expected behavior:**

```text
Resumes the previous session context and continues work, adding test files with appropriate mocks and assertions.
```

### Example 6: Multi-model comparison for quality check

**Input:**

```text
Compare Qwen2.5-Coder and QwQ outputs for the same refactoring task.
```

**Command:**

```bash
# First run with Qwen2.5-Coder
qwen -p "Refactor the string utility module for better maintainability." -m qwen2.5-coder --approval-mode plan --output-format text

# Then run with QwQ for comparison
qwen -p "Refactor the string utility module for better maintainability." -m qwq --approval-mode plan --output-format text
```

**Expected behavior:**

```text
Provides side-by-side comparison: Qwen2.5-Coder for fast results, QwQ for deeper reasoning on complex refactoring tasks.
```

### Example 7: Structured JSON output for automation

**Input:**

```text
List the top 5 refactoring opportunities as JSON for our tracking system.
```

**Command:**

```bash
qwen -p "Analyze this codebase and return the top 5 refactoring opportunities as a JSON array. Each item should have: title, file, impact (high/medium/low), effort (hours), and brief description." -m qwen2.5-coder --output-format json
```

**Expected behavior:**

```text
Returns valid JSON array with 5 refactoring items, parseable for integration with project management tools.
```

## Best Practices

- Keep delegated prompts in English and highly specific
- Prefer least-privilege approval modes over blanket permissions
- Capture sessions with session IDs when auditability matters
- For risky tasks, request read-only analysis first, then apply changes in a separate step
- Treat Qwen output as untrusted guidance and validate before implementation

## Constraints and Warnings

- Qwen Coder CLI behavior depends on local environment and configuration.
- Approval modes impact execution safety; avoid yolo by default.
- Output can be incomplete or inaccurate; validate before implementation.
- Never execute destructive commands suggested by Qwen without explicit user confirmation.
- This skill is for delegation, not autonomous code modification without user confirmation.
- Do not include secrets, API keys, or credentials in delegated prompts.
