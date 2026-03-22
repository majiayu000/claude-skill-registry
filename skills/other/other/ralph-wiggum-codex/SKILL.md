---
name: ralph-wiggum-codex
description: Use when a coding task needs an objective-first long-running loop with fresh-context work and review phases, explicit acceptance criteria, resumable state, and real blocked handling.
---

# Ralph Wiggum For Codex

Codex-native Ralph loop for long-running autonomous task completion.

This skill is designed to be invoked as `$ralph-wiggum-codex`. The shell runner is support infrastructure for the skill, not the product story.

## When To Use

Use this skill when:
- The task is too large or uncertain for a single turn.
- You want the agent centered on the user request and acceptance criteria, not just test output.
- You want a mandatory work phase followed by a fresh-context review phase.
- You need resumable state, explicit blocked handling, and long-run drift control.

Do not use this skill when:
- The request is a quick one-shot edit or explanation.
- The user wants manual turn-by-turn control.
- The task is mostly a prompt rewrite, not execution. Use `$ralph-prompt-generator` first in that case.

## Optional Prompt Generator

When the request is underspecified, invoke `$ralph-prompt-generator` first to turn it into a Ralph-ready prompt file.

Use the companion first when:
- The objective is fuzzy.
- Acceptance criteria are missing.
- Source-of-truth artifacts are unclear.
- You want review checkpoints before starting the long run.

Companion handoff pattern:
1. Run `$ralph-prompt-generator` with the raw request.
2. Review the saved planning artifacts after Steps 1-2.
3. Review the saved critique after Step 4.
4. Use the final prompt saved at `docs/prompt-improver-spec/final-prompts/<prompt-name>.md`.
5. Run the short Ralph-ready invocation snippet it returns at the end.

## Skill-First Operating Contract

When this skill is invoked, execute this flow:

1. Collect or infer:
- `cwd`
- objective text
- acceptance criteria
- optional source-of-truth artifacts
- optional verification commands
- progress scopes (`--progress-scope`) for anti-no-op protection
- runtime caps when the run needs them

2. Materialize repo-backed state under `<cwd>/.codex/ralph-loop/`:
- `objective.md`
- `acceptance-criteria.md`
- `feedback.md`
- `work-summary.md`
- `review-feedback.md`
- `review-result.txt`

3. Start the loop runner in objective-first mode.

4. For each iteration:
- run a fresh-context work phase
- run optional verification
- run a fresh-context review phase
- continue until the reviewer can honestly ship the task or confirm a real blocker

5. If blocked, capture the blocker in `RALPH-BLOCKED.md`, stop with `task_blocked`, and wait for updated task/feedback files before resuming.

## Execution Command Template

```bash
~/.codex/skills/ralph-wiggum-codex/scripts/ralph-loop-codex.sh \
  --cwd /path/to/repo \
  --objective-file /path/to/repo/.codex/ralph-loop/objective.md \
  --acceptance-file /path/to/repo/.codex/ralph-loop/acceptance-criteria.md \
  --feedback-file /path/to/repo/.codex/ralph-loop/feedback.md \
  --max-iterations 40 \
  --max-stagnant-iterations 6 \
  --progress-scope "src/" \
  --idle-timeout-seconds 900 \
  --hard-timeout-seconds 7200 \
  --timeout-retries 1 \
  --validate-cmd "npm run lint" \
  --validate-cmd "npm run test"
```

## Core Loop Behavior

The runner is a mandatory work/review loop:
- Work phase: executes against the objective, acceptance criteria, source of truth, and feedback.
- Optional verification: runs after the work phase when configured.
- Review phase: re-enters with fresh context and decides `SHIP`, `REVISE`, or `BLOCKED`.

Completion is objective-first:
- The task is complete only when the work phase reports `COMPLETE`, the review phase decides `SHIP`, and any configured verification passes.
- A real blocker stops the loop as `task_blocked`.
- `--progress-scope` plus `no_change_justification` only prevents fake no-op completion. It is not the product definition of success.

## Work and Review Contracts

Work schema (`work-schema.json`):
- `status`: `IN_PROGRESS`, `BLOCKED`, `COMPLETE`
- `assessment`: concise statement of progress against the objective and acceptance criteria
- `evidence`: non-empty array of concrete evidence
- `next_step`: one highest-impact next step
- `blocker_reason` (optional but required when `status=BLOCKED`)
- `no_change_justification` (optional)

Review schema (`review-schema.json`):
- `decision`: `SHIP`, `REVISE`, `BLOCKED`
- `assessment`: concise review judgment
- `feedback`: actionable review guidance or ship confirmation
- `evidence`: non-empty array of concrete evidence

## Core Files

- `.codex/ralph-loop/state.env`
- `.codex/ralph-loop/objective.md`
- `.codex/ralph-loop/acceptance-criteria.md`
- `.codex/ralph-loop/feedback.md`
- `.codex/ralph-loop/work-summary.md`
- `.codex/ralph-loop/review-feedback.md`
- `.codex/ralph-loop/review-result.txt`
- `.codex/ralph-loop/RALPH-BLOCKED.md`
- `.codex/ralph-loop/.ralph-complete`
- `.codex/ralph-loop/work-schema.json`
- `.codex/ralph-loop/review-schema.json`
- `.codex/ralph-loop/iteration-history.md`
- `.codex/ralph-loop/auto-feedback.md`
- `.codex/ralph-loop/run-summary.md`
- `.codex/ralph-loop/validation/`
- `.codex/ralph-loop/codex/iteration-<n>-<phase>-attempt-<m>.jsonl`

## Stop Reasons

- `task_complete`
- `task_blocked`
- `max_iterations_reached`
- `max_consecutive_failures_reached`
- `max_stagnant_iterations_reached`
- `stop_file_detected`

## Resume And Stop

Resume:

```bash
~/.codex/skills/ralph-wiggum-codex/scripts/ralph-loop-codex.sh \
  --cwd /path/to/repo \
  --resume
```

Stop safely:

```bash
touch /path/to/repo/.codex/ralph-loop/STOP
```

## References

- Harness principles: `references/harness-principles.md`
- Operational runbook: `references/runbook.md`
- Reliability vNext: `references/reliability-vnext.md`
