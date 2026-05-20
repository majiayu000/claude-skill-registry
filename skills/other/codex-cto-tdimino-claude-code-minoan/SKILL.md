---
name: codex-cto
description: Inverted orchestration—Codex CLI acts as CTO (planning and reviewing), Claude Code executes with native tools. Use when a task benefits from external architectural oversight before and after implementation.
argument-hint: [objective]
disable-model-invocation: true
---

# Codex CTO — Inverted Orchestration

Codex plans and reviews. Claude Code executes. This inverts the `codex-orchestrator` pattern: instead of Claude Code delegating to Codex subagents, Codex directs Claude Code as the engineering team.

## Protocol

```
1. CTO plans   →  cto-invoke.sh plan "<objective>"
2. You execute  →  native tools (Read, Edit, Write, Bash, Glob, Grep)
3. CTO reviews  →  cto-invoke.sh review "<objective + results>"
4. Loop         →  if "revise", fix and re-submit for review (max 5 iterations)
```

## Step 1: Get the Plan

Run the plan phase with the user's objective:

```bash
~/.claude/skills/codex-cto/scripts/cto-invoke.sh plan "<OBJECTIVE>" [--model MODEL]
```

Parse the returned JSON. It contains:
- `objective` — what to accomplish
- `analysis` — CTO's assessment of the codebase
- `strategy` — high-level approach
- `tasks[]` — ordered task list with IDs, actions, targets, descriptions, acceptance criteria, and dependencies
- `verification` — commands to run after all tasks complete

## Step 2: Execute Tasks

Work through each task in dependency order using native tools. For each task:

1. Read the `description` and `acceptance_criteria`
2. Execute the action (`create_file`, `modify_file`, `delete_file`, `run_command`, `verify`)
3. Verify each acceptance criterion before moving to the next task
4. Track what was done and what the outcome was

Do not deviate from the plan without reason. If a task is blocked or the plan has an error, note it and continue with unblocked tasks. Report blockers in the review submission.

## Step 3: Submit for Review

After executing all tasks, run the review phase. Include the original objective and a summary of what was done:

```bash
~/.claude/skills/codex-cto/scripts/cto-invoke.sh review "<OBJECTIVE>. Results: <summary of what was done, any issues encountered>"
```

Parse the returned JSON:
- `verdict: "approve"` — done. Report success to the user.
- `verdict: "revise"` — check `task_reviews` for feedback and `revised_tasks` for new/updated tasks. Fix issues and re-submit.
- `verdict: "abort"` — fundamental problem. Report the CTO's `reason` to the user and stop.

## Step 4: Iterate (if revise)

On a "revise" verdict:
1. Read each `task_reviews` entry with status `fail` or `partial`
2. Execute the fixes described in `feedback` and any `revised_tasks`
3. Re-submit for review (step 3)
4. Maximum 5 review iterations. If the CTO issues 3 consecutive "revise" verdicts, escalate to the user.

## Model Selection

The `--model` flag passes through to `codex exec`. Available models:

| Model | ID | Notes |
|-------|----|-------|
| GPT-5.3-Codex | `gpt-5.3-codex` | Default. Fastest, most capable. |
| GPT-5.3-Codex Spark | `gpt-5.3-codex-spark` | Lighter, near-instant. |
| GPT-5.2-Codex | `gpt-5.2-codex` | Previous generation. |

Omit `--model` to use the default from `~/.codex/config.toml`.

## Options

| Option | Description |
|--------|-------------|
| `--model <id>` | Override model (default: config default) |
| `--dry-run` | Print command without executing |

## Artifacts

Plan and review JSON files are saved to `.codex-cto/<PID>/` in the working directory. Each invocation creates sequentially numbered files (`plan-001.json`, `review-001.json`, etc.). PID namespacing prevents conflicts between concurrent sessions.

## Diagnostics

Reuse codex-orchestrator's status script for CLI diagnostics:

```bash
~/.claude/skills/codex-orchestrator/scripts/codex-status.sh
```

## Examples

```bash
# Simple feature
/codex-cto Add a health check endpoint at /health returning {status: "ok"}

# With model override
/codex-cto Refactor the auth module to use JWT --model gpt-5.3-codex-spark

# Dry run to inspect the command
~/.claude/skills/codex-cto/scripts/cto-invoke.sh plan "Add rate limiting" --dry-run
```

## Sister Skill

This skill is the inverse of `codex-orchestrator`. Use `codex-orchestrator` when Claude Code should delegate one-shot specialist tasks to Codex. Use `codex-cto` when Codex should direct Claude Code through a plan-execute-review loop.
