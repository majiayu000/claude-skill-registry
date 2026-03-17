---
name: claude-skill
description: Use when work should be delegated to Claude Code CLI, especially headless `claude -p` runs, automation scripts, CI jobs, resumable sessions, or requests to use Claude/Claude Code for a task.
compatibility: Requires Claude Code CLI (`claude`) installed and authenticated on the target machine.
---

# Claude Code Headless Mode

Use this skill when the job should be executed through Claude Code itself, not solved inline. Focus on commands and workflows that match current stable Claude Code behavior.

## Core Rules

- Treat `claude --help` on the target machine as the compatibility floor. CLI flags move faster than blog posts and copied examples.
- Permission rule syntax varies by build. Anthropic docs often show forms like `Bash(git diff *)`, while the installed `claude 2.1.71` help on this machine still shows `Bash(git:*)`. Mirror the syntax shown by the target machine's `claude --help`.
- Default to the model the user already configured through `/model`, settings, or `ANTHROPIC_MODEL`.
- Do **not** add `--model` unless the user explicitly asked for a model override or the workflow must pin a model for reproducibility.
- Prefer `--append-system-prompt` over `--system-prompt` unless replacing the default Claude Code behavior is intentional.
- Default to safe automation. If the user wants a truly unattended run, use explicit permission rules or `dontAsk`; reserve `bypassPermissions` for isolated environments.

## Quick Verification

Run these checks before giving advanced advice:

```bash
claude --version
claude auth status --text
claude --help
```

If installation or updates look odd, use:

```bash
claude doctor
```

## Installation Guidance

- Anthropic's getting-started docs still show `npm install -g @anthropic-ai/claude-code` as the standard install path.
- Newer builds may also support native installer flows and `claude install`.
- If the user needs installation help, point them to the official Claude Code setup docs and verify the result with `claude doctor` rather than assuming one installer path is universal.

## Headless Command Patterns

### Basic Non-Interactive Run

Use `-p` / `--print` for non-interactive execution:

```bash
claude -p "summarize the repository architecture"
```

Add `--output-format json` when the caller needs machine-readable output:

```bash
claude -p "review the auth layer for risks" --output-format json
```

### Model Selection

- Omit `--model` by default.
- If the user explicitly wants a model override, use `claude --model <alias-or-name> ...`.
- For persistent defaults, prefer settings (`model`) or `ANTHROPIC_MODEL`.
- For third-party deployments, pin models via settings or environment variables instead of bolting `--model` onto every command example.

### Permission Modes

Claude Code supports these permission modes:

| Mode | Use |
| --- | --- |
| `default` | Interactive exploration. Prompts on first use of write/bash-style tools. |
| `acceptEdits` | Recommended starting point for coding automation. Auto-accepts edits, but command execution can still prompt. |
| `plan` | Analysis only. No file changes or command execution. |
| `dontAsk` | Auto-denies anything not already approved by permission rules. Good for unattended-but-constrained runs. |
| `bypassPermissions` | Skips prompts entirely. Only for strong sandbox / container / VM isolation. |

Important clarifications:

- `acceptEdits` is the skill's recommended default, not the CLI default.
- If the user says "no prompts at all," prefer permission rules or `dontAsk` with explicit allow rules.
- Only recommend `bypassPermissions` when the environment is already isolated and the user accepts the risk.
- For read-only analysis, prefer `--tools` plus `default` or `plan`; do not reach for `bypassPermissions` just to suppress prompts.

### Tool Availability vs Permission Approval

Do not mix these up:

- `--tools` restricts which built-in tools are available at all.
- `--allowedTools` pre-approves specific tools or tool rules so Claude does not prompt for them.
- `--disallowedTools` removes tools or rules from context.

Permission rules follow `Tool` or `Tool(specifier)` syntax.

Use wildcard rules when the command will include arguments:

- Good: `Bash(git diff *)`
- Good: `Bash(npm run test *)`
- Risky for real use: `Bash(find)` because it matches only the exact literal command `find`

If the local CLI help shows colon syntax such as `Bash(find:*)`, use that form on that machine. The important part is to allow an argument-aware rule rather than an exact literal command.

If the user wants Claude limited to a narrow tool family, you should usually use both `--tools` and `--allowedTools`: `--tools` defines the hard boundary, `--allowedTools` removes prompts inside that boundary.

### Output Formats

- `text`: default human-readable output
- `json`: one final structured result
- `stream-json`: event stream for long-running automation

Do not promise a fixed JSON schema unless you have validated it on the target version. Prefer wording like "returns a final result object with response text, timing, and session metadata."

### Commonly Safe Flags

These are appropriate starting points on current stable builds:

- `--append-system-prompt`
- `--allowedTools`
- `--disallowedTools`
- `--tools`
- `--permission-mode`
- `--output-format`
- `--mcp-config`
- `--continue` / `--resume`
- `--settings` / `--setting-sources`
- `--session-id`
- `--add-dir`
- `--max-budget-usd`
- `--fallback-model` for print mode

### Version-Sensitive Flags

Published docs sometimes mention flags that are absent from the installed binary on a given machine. Before emitting less-common flags, verify them with `claude --help`.

## Recommended Command Templates

### Read-Only Analysis

```bash
claude -p "count the total lines of code in this repo, grouped by language" \
  --permission-mode default \
  --tools "Bash,Read" \
  --allowedTools "Read" "Bash(find:*)" "Bash(wc:*)"
```

### Safe Edit Run

```bash
claude -p "fix the failing login test and rerun the relevant test command" \
  --permission-mode acceptEdits \
  --tools "Bash,Read,Edit,Write" \
  --allowedTools "Read" "Edit" "Write" "Bash(npm test *)"
```

### JSON Report

```bash
claude -p "review the repository for security issues and produce a concise report" \
  --output-format json \
  --append-system-prompt "Focus on concrete findings, exploitability, and mitigations."
```

### Resume a Session

```bash
claude -r "$session_id" -p "continue by updating the tests and summarizing what changed"
```

### Continue the Most Recent Session

```bash
claude -c -p "continue with the next step"
```

### Use MCP Tools

```bash
claude -p "investigate the API latency spike" \
  --permission-mode acceptEdits \
  --mcp-config monitoring-tools.json \
  --allowedTools "Read" "mcp__datadog__*" "mcp__prometheus__*"
```

### Fully Unattended Execution in an Isolated Environment

Use only when the environment is already sandboxed:

```bash
claude -p "run the migration and fix the resulting type errors" \
  --permission-mode bypassPermissions \
  --tools "Bash,Read,Edit,Write"
```

## Execution Workflow

1. Confirm the user wants Claude Code CLI rather than an inline answer.
2. Verify the installed CLI shape with `claude --help` if you plan to use uncommon flags.
3. Choose the least-permissive mode that still fits the task.
4. Build the command without `--model` unless the user explicitly asked for an override.
5. Restrict tools with `--tools` when safety or predictability matters.
6. Use `--allowedTools` for prompt-free approval of known-safe actions.
7. Return exact commands plus short caveats about assumptions and safety.

## When To Pause

Pause only when one of these is materially unclear:

- The user wants a specific model or provider behavior that requires pinning.
- They asked for a fully unattended run in an environment that is not clearly sandboxed.
- The workflow depends on a Claude Code feature that is not visible in `claude --help`.

Otherwise, proceed and give the best current command.

## Final Response Expectations

When using this skill, the output should usually include:

- the exact command or command sequence
- a one-line note that the configured Claude model is being used by default
- any permission or isolation caveat
- the resume command if the workflow is meant to continue later

## References

- `references/examples.md` for extended patterns
