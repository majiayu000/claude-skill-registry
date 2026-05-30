---
name: copilot-cli
description: Provides GitHub Copilot CLI task delegation in non-interactive mode with multi-model support (Claude, GPT, Gemini), permission controls, output sharing, and session resume. Use when users ask to hand work to Copilot, compare models, or run Copilot programmatically from Claude Code.
allowed-tools: Bash, Read, Write
---

# Copilot CLI Delegation

Delegate selected tasks from Claude Code to GitHub Copilot CLI using non-interactive commands, explicit model selection, safe permission flags, and shareable outputs.

## Overview

This skill standardizes delegation to GitHub Copilot CLI (`copilot`) for cases where a different model may be more suitable for a task. It covers:

- Non-interactive execution with `-p` / `--prompt`
- Model selection with `--model`
- Permission control (`--allow-tool`, `--allow-all-tools`, `--allow-all-paths`, `--allow-all-urls`, `--yolo`)
- Output capture with `--silent`
- Session export with `--share`
- Session resume with `--resume`

Use this skill only when delegation to Copilot is explicitly requested or clearly beneficial.

## When to Use

Use this skill when:

- The user asks to delegate work to GitHub Copilot CLI
- The user wants a specific model (for example GPT-5.x, Claude Sonnet/Opus/Haiku, Gemini)
- The user asks for side-by-side model comparison on the same task
- The user wants a reusable scripted Copilot invocation
- The user wants Copilot session output exported to markdown for review

Trigger phrases:

- "ask copilot"
- "delegate to copilot"
- "run copilot cli"
- "use copilot with gpt-5"
- "use copilot with sonnet"
- "use copilot with gemini"
- "resume copilot session"

## Instructions

### 1) Verify prerequisites

```bash
# CLI availability
copilot --version

# GitHub authentication status
gh auth status
```

If `copilot` is unavailable, ask the user to install/setup GitHub Copilot CLI before proceeding.

### 2) Convert task request to English prompt

All delegated prompts to Copilot CLI must be in English.

- Keep prompts concrete and outcome-driven
- Include file paths, constraints, expected output format, and acceptance criteria
- Avoid ambiguous goals such as "improve this"

Prompt template:

```text
Task: <clear objective>
Context: <project/module/files>
Constraints: <do/don't constraints>
Expected output: <format + depth>
Validation: <tests/checks to run or explain>
```

### 3) Choose model intentionally

Pick a model based on task type and user preference.

- Complex architecture, deep reasoning: prefer high-capacity models (for example Opus / GPT-5.2 class)
- Balanced coding tasks: Sonnet-class model
- Quick/low-cost iterations: Haiku-class or mini models
- If user specifies a model, respect it

Use exact model names available in the local Copilot CLI model list.

### 4) Select permissions with least privilege

Default to the minimum required capability.

- Prefer `--allow-tool '<tool>'` when task scope is narrow
- Use `--allow-all-tools` only when multiple tools are clearly needed
- Add `--allow-all-paths` only if task requires broad filesystem access
- Add `--allow-all-urls` only if external URLs are required
- Do not use `--yolo` unless the user explicitly requests full permissions

### 5) Run delegation command

Base pattern:

```bash
copilot -p "<english prompt>" --model <model-name> --allow-all-tools --silent
```

Add optional flags only as needed:

```bash
# Capture session to markdown
copilot -p "<english prompt>" --model <model-name> --allow-all-tools --share

# Resume existing session
copilot --resume <session-id> --allow-all-tools

# Strictly silent scripted output
copilot -p "<english prompt>" --model <model-name> --allow-all-tools --silent
```

### 6) Return results clearly

After command execution:

- Return Copilot output concisely
- State model and permission profile used
- If `--share` is used, provide generated markdown path
- If output is long, provide summary plus key excerpts and next-step options

### 7) Optional multi-model comparison

When requested, run the same prompt with multiple models and compare:

- Correctness
- Practicality of proposed changes
- Risk/security concerns
- Effort estimate

Keep the comparison objective and concise.

## Examples

### Example 1: Refactor with GPT model

Input:

```text
Ask Copilot to refactor this service using GPT-5.2 and return only concrete code changes.
```

Command:

```bash
copilot -p "Refactor the payment service in src/services/payment.ts to reduce duplication. Keep public behavior unchanged, keep TypeScript strict typing, and output a patch-style response." \
  --model gpt-5.2 \
  --allow-all-tools \
  --silent
```

Output:

```text
Copilot proposes extracting three private helpers, consolidating error mapping, and provides a patch for payment.ts with unchanged API signatures.
```

### Example 2: Code review with Sonnet and shared session

Input:

```text
Use Copilot CLI with Sonnet to review this module and share the session in markdown.
```

Command:

```bash
copilot -p "Review src/modules/auth for security and correctness. Report only high-confidence findings with severity and file references." \
  --model claude-sonnet-4.6 \
  --allow-all-tools \
  --share
```

Output:

```text
Review completed. Session exported to ./copilot-session-<id>.md.
```

### Example 3: Resume session

Input:

```text
Continue the previous Copilot analysis session.
```

Command:

```bash
copilot --resume <session-id> --allow-all-tools
```

Output:

```text
Session resumed and continued from prior context.
```

## Best Practices

- Keep delegated prompts in English and highly specific
- Prefer least-privilege flags over blanket permissions
- Capture sessions with `--share` when auditability matters
- For risky tasks, request read-only analysis first, then apply changes in a separate step
- Re-run with another model only when there is clear value (quality, speed, or cost)

## Constraints and Warnings

- Copilot CLI output is external model output: validate before applying code changes
- Never include secrets, API keys, or credentials in delegated prompts
- `--allow-all-tools`, `--allow-all-paths`, `--allow-all-urls`, and `--yolo` increase risk; use only when justified
- Do not treat Copilot suggestions as authoritative without local verification (tests/lint/type checks)

For additional option details, see `references/cli-command-reference.md`.
