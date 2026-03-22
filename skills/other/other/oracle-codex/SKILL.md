---
argument-hint: <query> [--reasoning <level>]
disable-model-invocation: false
name: oracle-codex
user-invocable: true
description: This skill should be used when the user asks to "use Codex", "ask Codex", "consult Codex", "use GPT for planning", "ask GPT to review", "get GPT's opinion", "what does GPT think", "second opinion on code", "consult the oracle", "ask the oracle", or mentions using an AI oracle for planning or code review. NOT for implementation tasks.
---

# Codex Oracle

Use OpenAI Codex CLI as a **read-only oracle** — planning, review, and analysis only. Codex provides its perspective; you synthesize and present results to the user.

**Sandbox is always `read-only`**. Codex must never implement changes.

## Arguments

Parse `$ARGUMENTS` for:

- **query** — the main question or task (everything not a flag). **Required** — if empty, tell the user to provide a query and stop.
- `--reasoning <level>` — override reasoning effort (`low`, `medium`, `high`, `xhigh`). Optional; default is auto-selected based on complexity.

## Prerequisites

Run the check script before any Codex invocation:

```bash
scripts/check-codex.sh
```

If it exits non-zero, display the error and stop. Use the wrapper for all `codex exec` calls:

```bash
scripts/run-codex-exec.sh
```

## Configuration

| Setting   | Default         | Override                                         |
| --------- | --------------- | ------------------------------------------------ |
| Model     | `gpt-5.3-codex` | Allowlist only (see `references/codex-flags.md`) |
| Reasoning | Auto            | `--reasoning <level>` or user prose              |
| Sandbox   | `read-only`     | Not overridable                                  |

### Reasoning Effort

| Complexity | Effort   | Timeout  | Criteria                             |
| ---------- | -------- | -------- | ------------------------------------ |
| Simple     | `low`    | 300000ms | \<3 files, quick question            |
| Moderate   | `medium` | 300000ms | 3–10 files, focused analysis         |
| Complex    | `high`   | 600000ms | Multi-module, architectural thinking |
| Maximum    | `xhigh`  | 600000ms | Full codebase, critical decisions    |

For `xhigh` tasks that may exceed 10 minutes, use `run_in_background: true` on the Bash tool and set `CODEX_OUTPUT` so you can read the output later.

See `references/codex-flags.md` for full flag documentation.

## Workflow

### 1. Parse and Validate

1. Parse `$ARGUMENTS` for query and `--reasoning`
2. Run `scripts/check-codex.sh` — abort on failure
3. Assess complexity to select reasoning effort (unless overridden)

### 2. Construct Prompt

Build a focused prompt from the user's query and any relevant context (diffs, file contents, prior conversation). Keep it direct — state what you want Codex to analyze and what kind of output you need. Do not implement; request analysis and recommendations only.

### 3. Execute

Invoke via the wrapper with HEREDOC. Set the Bash tool timeout per the reasoning effort table above.

```bash
EFFORT="<effort>" \
CODEX_OUTPUT="/tmp/codex-${RANDOM}${RANDOM}.txt" \
scripts/run-codex-exec.sh <<'EOF'
[constructed prompt]
EOF
```

For `xhigh`, consider `run_in_background: true` on the Bash tool call, then read `CODEX_OUTPUT` when done.

### 4. Present Results

Read the output file and present with attribution:

```
## Codex Analysis

[Codex output — summarize if >200 lines]

---
Model: gpt-5.3-codex | Reasoning: [effort level]
```

Synthesize key insights and actionable items for the user.
