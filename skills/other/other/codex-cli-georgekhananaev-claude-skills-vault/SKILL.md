---
name: codex-cli
description: Run OpenAI Codex CLI for coding tasks and second-opinion audits. Use when a user asks to run/ask/use Codex, says "codex prompt", or wants Claude to delegate a logic/code review to OpenAI models.
---

# Codex CLI

Run OpenAI Codex CLI locally for second-opinion audits, code review, and non-interactive task execution.

## Prerequisites

Codex CLI must be installed and authenticated:

1. **Install:** `npm install -g @openai/codex`
2. **Auth:** `codex login`
3. **Verify:** `codex --version`

## Core Execution Pattern

Use `codex exec` for delegated prompts (non-interactive):

```bash
codex exec "Your prompt here"
```

When the user says "codex prompt", treat it as:

```bash
codex exec "<user prompt>"
```

## Model Guidance

Use the default configured model unless the user asks otherwise.

Latest tested working model in this environment:

```bash
codex exec -m gpt-5.3-codex "Your prompt"
```

Compatibility note:
- `gpt-5-codex` may fail if config uses `model_reasoning_effort = "xhigh"`.
- If you must use `gpt-5-codex`, set reasoning effort explicitly:

```bash
codex exec -m gpt-5-codex -c model_reasoning_effort="high" "Your prompt"
```

## Commands

### Non-Interactive Execution

```bash
# Basic task
codex exec "Audit this logic for edge cases"

# Explicit model
codex exec -m gpt-5.3-codex "Review this implementation strategy"

# Full-auto mode (sandboxed, lower friction)
codex exec --full-auto "Implement the requested refactor"

# Read-only sandbox (analysis only)
codex exec -s read-only "Find bugs in this code path"

# Workspace-write sandbox
codex exec -s workspace-write "Apply the fix and update tests"

# Custom working directory
codex exec -C /path/to/project "Evaluate this repository"

# Save final output to file
codex exec -o output.txt "Summarize key risks"

# JSONL event stream
codex exec --json "Produce structured findings"

# Pipe context from stdin
cat context.txt | codex exec -
```

### Code Review

Use `codex review` for repository diffs:

```bash
# Review uncommitted changes
codex review --uncommitted

# Review against a base branch
codex review --base main

# Review a specific commit
codex review --commit abc123

# Custom review instructions
codex review "Focus on security issues"

# Combined
codex review --base main "Check for performance regressions"
```

## Important Flag Placement

`--search` and `-a/--ask-for-approval` are top-level flags. Put them before `exec` or `review`.

Correct:

```bash
codex --search -a on-request exec "Your prompt"
codex --search -a on-request review --uncommitted
```

Avoid:

```bash
codex exec --search "Your prompt"
codex exec -a on-request "Your prompt"
```

## Useful Flags

| Flag | Description |
|------|-------------|
| `-m` | Model (recommended explicit example: `gpt-5.3-codex`) |
| `-s` | Sandbox: `read-only`, `workspace-write`, `danger-full-access` |
| `-a` | Approval policy (`untrusted`, `on-failure`, `on-request`, `never`) as a top-level flag |
| `-C` | Working directory |
| `-o` | Write last message to file |
| `--full-auto` | Sandboxed auto-execution (`-a on-request -s workspace-write`) |
| `--json` | JSONL event output |
| `--search` | Enable web search tool as a top-level flag |
| `--add-dir` | Additional writable directories |
| `-c key=value` | Override config (example: `-c model_reasoning_effort="high"`) |

## Best Practices

- Prefer `codex exec` for delegated prompts instead of interactive `codex`
- Start with `-s read-only` for audits and second opinions
- Use `--full-auto` only when you expect autonomous edits
- Keep prompts explicit about expected output format
- Add `-o` when another tool or agent must consume the result
- Run `codex review --uncommitted` before committing as a quick extra pass
