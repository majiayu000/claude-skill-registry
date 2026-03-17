---
name: codex-collab
description: Delegate tasks to Codex — run prompts, code review, research, pair programming, or any collaboration mode. Use when the user asks to use Codex, send work to Codex, have Codex review/investigate/implement something, or collaborate with Codex. Also use proactively when you want external feedback, a second opinion, or a fresh pair of eyes on code, architecture, or decisions.
---

# codex-collab

codex-collab is a bridge between Claude and Codex. It communicates with Codex via the `codex app-server` JSON-RPC protocol, giving you structured, event-driven access to Codex's capabilities — prompting, code review, tool use, and file editing.

## Collaboration Modes

- **Run** — Single-command `run` for any prompted task (research, analysis, implementation). Starts a thread, sends prompt, waits for completion, returns output.
- **Code review** — Single-command `review` for PR-style, uncommitted, or commit-level review.
- **Parallel work** — You and Codex work on different parts simultaneously. Start multiple jobs.
- **Research** — Spin up a read-only Codex session to investigate something while you continue other work.

## Run Command (Recommended for Prompted Tasks)

The `run` command handles prompted tasks in one call: starts a thread, sends the prompt, waits for the turn to complete, and prints output.

```bash
# Research task
codex-collab run "what does this project do?" -s read-only --content-only

# Implementation task
codex-collab run "add input validation to the login form" --content-only

# Resume an existing thread (preserves conversation context)
codex-collab run --resume <id> "now check the error handling" --content-only

# Specify working directory (omit -d if already in the project dir)
codex-collab run "investigate the auth module" -d /path/to/project --content-only
```

**IMPORTANT: Always use `dangerouslyDisableSandbox=true`** for all `codex-collab` Bash commands — the tool writes to `~/.codex-collab/` which is outside the sandbox allowlist.

For **`run` and `review`** commands, also use `run_in_background=true` — these take minutes. You will be notified automatically when the command finishes. After launching, tell the user it's running and end your turn. Do NOT use TaskOutput, block, poll, wait, or spawn an agent to monitor the result — the background task notification handles this automatically.

For **all other commands** (`kill`, `jobs`, `progress`, `output`, `approve`, `decline`, `clean`, `delete`, `models`, `health`), run in the **foreground** — they complete in seconds.

If the user asks about progress mid-task, use `progress` to check the recent activity:

```bash
codex-collab progress <id>
```

Or use `TaskOutput(block=false)` to check the current output stream without blocking.

## Code Review (Recommended: Single Command)

The `review` command handles the entire review workflow in one call.

**Note**: When no `--mode` is specified, passing a prompt string switches from the default `pr` mode to `custom` mode, which sends custom instructions instead of using the built-in diff workflow. For a standard PR review, do not pass a prompt.

```bash
# PR-style review against main (default — no prompt)
codex-collab review -d /path/to/project --content-only

# Review uncommitted changes
codex-collab review --mode uncommitted -d /path/to/project --content-only

# Review a specific commit
codex-collab review --mode commit --ref abc1234 -d /path/to/project --content-only

# Custom review focus
codex-collab review "Focus on security issues" -d /path/to/project --content-only

# Resume an existing thread for follow-up review
codex-collab review --resume <id> -d /path/to/project --content-only
```

Review modes: `pr` (default), `uncommitted`, `commit`

**IMPORTANT: Use `run_in_background=true` and `dangerouslyDisableSandbox=true`** — reviews typically take 5-20 minutes. You will be notified automatically when done. After launching, tell the user it's running and end your turn. Do NOT use TaskOutput, block, poll, wait, or spawn an agent to monitor the result — the background task notification handles this automatically.

## Context Efficiency

- **Use `--content-only`** when reading output — prints only the result text, suppressing progress lines.
- **`run` and `review` print results on completion** — no separate `output` call needed.
- **Use `output <id>`** only to re-read the full log for a previously completed thread.

## Resuming Threads

When consecutive tasks relate to the same project, resume the existing thread. Codex retains the conversation history, so follow-ups like "now fix what you found" or "check the tests too" work better when Codex already has context from the previous exchange. Start a fresh thread when the task is unrelated or targets a different project.

| Situation | Action |
|-----------|--------|
| Same project, new prompt | `codex-collab run --resume <id> "prompt"` |
| Same project, want review | `codex-collab review --resume <id>` |
| Different project | Start new thread |
| Thread stuck / errored | `codex-collab kill <id>` then start new |

If you've lost track of the thread ID, use `codex-collab jobs` to find active threads.

## Checking Progress

If the user asks about a running task:

```bash
# Check recent activity from the log
codex-collab progress <id>

# Or check the running command's output stream
# (use TaskOutput with block=false from Claude Code)
```

Progress lines stream in real-time during execution:
```
[codex] Thread a1b2c3d4 started (gpt-5.4, workspace-write)
[codex] Turn started
[codex] Running: npm test
[codex] Edited: src/auth.ts (update)
[codex] Turn completed (2m 14s, 1 file changed)
```

## Approvals

By default, Codex auto-approves all actions (`--approval never`). For stricter control:

```bash
# Require approval for Codex-initiated actions
codex-collab run "refactor the auth module" --approval on-request --content-only
```

When an approval is needed, the progress output will show:
```
[codex] APPROVAL NEEDED
[codex]   Command: rm -rf node_modules
[codex]   Approve: codex-collab approve <approval-id>
[codex]   Decline: codex-collab decline <approval-id>
```

Respond with `approve` or `decline`:
```bash
codex-collab approve <approval-id>
codex-collab decline <approval-id>
```

## CLI Reference

### Run

```bash
codex-collab run "prompt" [options]               # New thread, send prompt, wait, print output
codex-collab run --resume <id> "prompt" [options]  # Resume existing thread
codex-collab run "prompt" -s read-only             # Read-only sandbox
```

### Review

```bash
codex-collab review [options]                      # PR-style (default)
codex-collab review --mode uncommitted [options]   # Uncommitted changes
codex-collab review --mode commit [options]        # Latest commit
codex-collab review --mode commit --ref <hash>     # Specific commit
codex-collab review "instructions" [options]       # Custom review
codex-collab review --resume <id> [options]        # Resume existing thread
```

### Reading Output

```bash
codex-collab output <id>                # Full log for thread
codex-collab progress <id>              # Recent activity (tail of log)
```

### Thread Management

```bash
codex-collab jobs                       # List threads
codex-collab jobs --json                # List threads (JSON)
codex-collab kill <id>                  # Stop a running thread
codex-collab delete <id>               # Archive thread, delete local files
codex-collab clean                      # Delete old logs and stale mappings
```

### Utility

```bash
codex-collab config                     # Show persistent defaults
codex-collab config model gpt-5.3-codex # Set default model
codex-collab config model --unset       # Unset a key (return to auto)
codex-collab config --unset             # Unset all keys (return to auto)
codex-collab models                     # List available models
codex-collab approve <id>              # Approve a pending request
codex-collab decline <id>              # Decline a pending request
codex-collab health                     # Check prerequisites
```

### Options

| Flag | Description |
|------|-------------|
| `-m, --model <model>` | Model name (default: auto — latest available) |
| `-r, --reasoning <level>` | Reasoning effort: low, medium, high, xhigh (default: auto — highest for model) |
| `-s, --sandbox <mode>` | Sandbox: read-only, workspace-write, danger-full-access (default: workspace-write; review always uses read-only) |
| `-d, --dir <path>` | Working directory (default: cwd) |
| `--resume <id>` | Resume existing thread (run and review) |
| `--timeout <sec>` | Turn timeout in seconds (default: 1200) |
| `--approval <policy>` | Approval policy: never, on-request, on-failure, untrusted (default: never) |
| `--mode <mode>` | Review mode: pr, uncommitted, commit |
| `--ref <hash>` | Commit ref for --mode commit |
| `--json` | JSON output (jobs command) |
| `--content-only` | Print only result text (no progress lines) |
| `--limit <n>` | Limit items shown |

## Tips

- **`run --resume` requires a prompt.** `review --resume` works without one (it uses the review workflow), but `run --resume <id>` will error if no prompt is given.
- **Omit `-d` if already in the project directory** — it defaults to cwd. Only pass `-d` when the target project differs from your current directory.
- **Multiple concurrent threads** are supported. Each gets its own Codex app-server process and thread ID.
- **Validate Codex's findings.** After reading Codex's review or analysis output, verify each finding against the actual source code before presenting to the user. Drop false positives, note which findings you verified.

## Error Recovery

| Symptom | Fix |
|---------|-----|
| "codex CLI not found" | Install: `npm install -g @openai/codex` |
| Turn timed out | Increase `--timeout` or check if the task is too large |
| Thread not found | Use `codex-collab jobs` to list active threads |
| Process crashed mid-task | Resume with `--resume <id>` — thread state is persisted |
| Approval request hanging | Run `codex-collab approve <id>` or `codex-collab decline <id>` |

## Prerequisites

Requires bun and codex CLI on PATH. Run `codex-collab health` to verify.
