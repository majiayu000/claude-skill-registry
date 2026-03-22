---
name: skill-evolution
description: "Global evolution system for ship-faster skills. Uses hooks to capture context, failures, and session summaries, then generates patch suggestions (no auto edits) via skill-improver. Use when you want the skills to self-improve safely and continuously."
---

# Evolution

This skill makes the skills library evolve based on real development signals without auto-editing skills. The default output is a patch suggestion only.

## Why it exists (solving "too passive")

Default hooks can only "log events" without automatically consolidating experience into skills.

The goal of this skill is to turn retrospectives into a **fixed closing action**:
- At the end of each "big task", spend 60 seconds on Q&A confirmation: whether to optimize skills and which areas to prioritize
- When user chooses "yes to optimize", use `skill-improver` to generate **minimal patch suggestions** based on real run artifacts (still no auto-editing of skill library)

## Default strategy

- Capture context and failures into run artifacts
- Generate evolution candidates
- Use `skill-improver` to propose a minimal patch
- Human reviews and applies the patch

## Global hooks (recommended)

Hooks live in: `~/.claude/skills/skill-evolution/hooks/`

Add to your global settings (or project settings) so hooks run automatically.

Example (merge into `~/.claude/settings.json` or `<project>/.claude/settings.json`):

## Evolution settings

Configure behavior via `~/.claude/skills/skill-evolution/hooks/settings.json`:

```json
{
  "min_fail_count": 2,
  "ignore_tool_errors": true,
  "noise_filters": {
    "ignore_patterns": [
      "typescript: type.*already exists",
      "eslint:.*no-unused-vars.*react",
      "prettier:.*prettier-ignore"
    ],
    "max_failures_per_run": 20,
    "recent_only": true,
    "recent_window_minutes": 60
  },
  "output_format": {
    "summary_only": false,
    "include_context": true,
    "include_recent_failures": 20,
    "sort_by": "frequency"
  }
}
```

**Settings explanation**:
- `min_fail_count`: Minimum occurrences of a single error type before generating a candidate
- `ignore_tool_errors`: Whether to ignore tool-level errors (vs user code errors)
- `noise_filters.ignore_patterns`: List of regex patterns to ignore
- `max_failures_per_run`: Maximum failures to record per session (prevent explosion)
- `recent_only`: Only look at failures within recent time window
- `recent_window_minutes`: Only count failures within the last N minutes
- `output_format`: Controls evolution-candidates.md output format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/skill-evolution/hooks/pre-tool.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/skill-evolution/hooks/post-bash.sh \"$TOOL_OUTPUT\" \"$EXIT_CODE\""
          }
        ]
      },
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/skill-evolution/hooks/post-tool.sh \"$TOOL_OUTPUT\" \"$EXIT_CODE\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/skill-evolution/hooks/session-end.sh"
          }
        ]
      }
    ]
  }
}
```

## Run artifacts

Hooks write to project-local run folders:

```
<project-root>/runs/evolution/<run_id>/
  logs/
    events.jsonl
    failures.jsonl
    state.json
    context.json
  evolution-candidates.md
  evolution-review.md
```

`run_id` is stored in `<project-root>/runs/evolution/.current` so all hooks in a session write to the same run.

## Evolution checkpoint (default action at end of big tasks)

When you have just completed a "deliverable big task" (e.g., you have already written `final.md` or filled the run’s `tasks.md` **Delivery summary**), you **must** do a brief retrospective when closing, and give the choice to the user.

In the conversation, ask only 3 questions (prefer multiple choice to reduce cost):

1) Do you want to optimize skills based on this run?
   - A. Yes, propose a patch now (recommend using `skill-improver` first to generate minimal patch)
   - B. Record the issue first, optimize later
   - C. Not needed

2) What was the biggest blocker this time?
   - A. Missing input/context fields (need clearer I/O contracts)
   - B. Unclear plan/granularity too large (need to split or clarify validation steps)
   - C. Environment/dependency/command issues (need scripting or fixed commands)
   - D. UI/design iterations (need clearer design-system or UI subtask splitting)
   - E. External service/permissions/configuration (need clearer confirmation points and verification)
   - F. Other (explain in one sentence)

3) Which direction do you want to prioritize for optimization?
   - A. I/O contracts: Fix artifact names, fields, paths
   - B. Index/summary: Less context, better resume navigation (proposal/tasks)
   - C. Scripts/templates: Turn repetitive steps into deterministic scripts
   - D. Confirmation points: Reduce risky actions, confirm earlier/more clearly

Execution rules:
- If user chooses 1A: Immediately run `skill-improver`, only give `run_dir` path as input (don't paste logs into conversation)
- If user chooses 1B: Write "blocker + desired optimization direction" to `evolution-review.md` (or corresponding workflow run's `final.md` / `tasks.md`), process collectively next time
- If user chooses 1C: Don't interrupt, just end (but still keep run artifacts for future retrospectives)

## When to evolve (Ship Faster focus)

- Next.js upgrade or migration issue solved
- Guardrails problem fixed (lint/typecheck/build)
- Supabase error or migration pattern learned
- Stripe setup or billing flow resolved
- Vercel deploy or GitHub CI issue resolved
- AI SEO setup or indexing issue solved

## How to evolve

1. Hooks create `evolution-candidates.md` + `evolution-review.md` with the latest signals.
2. At the end of a big task, ask the 3 checkpoint questions (above) and let the user decide.
3. If user chooses to evolve: run `skill-improver` with the best `run_dir` (the workflow run_dir is usually better than evolution run_dir).
4. Apply the patch manually and re-validate skills.

## Example event

```json
{"ts":"2026-01-11T12:00:00Z","event":"post-bash","category":"build","exit_code":1,"summary":"next build failed: Module not found","artifacts":["logs/failures.jsonl"]}
```

## Outputs

- `evolution-candidates.md` (auto-generated)
- `evolution-review.md` (auto-generated, includes the 3 questions)
- Suggested patch from `skill-improver` (manual apply)

No skills are edited automatically.
