---
name: milhouse
description: Iterative development loop that feeds the same prompt back after each iteration until task completion. Use /bluera-base:milhouse-loop to start.
---

# Milhouse Loop - Iterative Development

## Overview

The milhouse loop is a powerful pattern for iterative development tasks. It works by:

1. Starting with a prompt (from file or inline)
2. Working on the task
3. When you try to exit, the Stop hook intercepts and feeds the SAME PROMPT back
4. You continue iterating, building on previous work visible in files and git history
5. Loop ends when you output the completion promise, hit max iterations, or get stuck

## Starting a Loop

```bash
# Basic usage with a prompt file
/bluera-base:milhouse-loop .claude/prompts/my-task.md

# With max iterations
/bluera-base:milhouse-loop task.md --max-iterations 10

# With custom completion promise
/bluera-base:milhouse-loop task.md --promise "FEATURE COMPLETE"

# Inline prompt (for simple tasks)
/bluera-base:milhouse-loop --inline "Refactor the auth module to use JWT tokens"

# With objective gates (tests must pass to exit)
/bluera-base:milhouse-loop task.md --gate "npm test" --gate "npm run lint"

# With context harness (creates plan.md and activity.md)
/bluera-base:milhouse-loop task.md --init-harness
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-iterations <n>` | Stop after N iterations | unlimited |
| `--promise <text>` | Completion promise text | "TASK COMPLETE" |
| `--inline <prompt>` | Use inline prompt instead of file | - |
| `--gate <cmd>` | Command that must pass before exit (repeatable) | none |
| `--stuck-limit <n>` | Stop after N identical gate failures | 3 |
| `--init-harness` | Create plan.md and activity.md files | false |

## Completing the Loop

To signal genuine completion, output this EXACT format on its own line:

```text
<promise>TASK COMPLETE</promise>
```

Or with a custom promise:

```text
<promise>YOUR_CUSTOM_PROMISE</promise>
```

**STRICT REQUIREMENTS:**

- The promise must appear on its OWN LINE (last non-empty line)
- Do NOT output false promises to escape the loop
- Only output when the task is genuinely complete

## Objective Gates

Gates are commands that must pass AFTER the promise matches, before the loop exits.

```bash
/bluera-base:milhouse-loop task.md --gate "npm test" --gate "npm run lint"
```

**Behavior:**

1. You output `<promise>TASK COMPLETE</promise>`
2. Each gate runs sequentially
3. If all pass → loop exits
4. If any fail → failure output is injected into the next iteration's prompt

This ensures code is actually correct, not just claimed to be complete.

## Stuck Detection

If the same gate fails 3 times in a row (identical output), the loop auto-stops.

```bash
# Disable stuck detection
/bluera-base:milhouse-loop task.md --gate "npm test" --stuck-limit 0

# More lenient (5 identical failures)
/bluera-base:milhouse-loop task.md --gate "npm test" --stuck-limit 5
```

## Stopping Early

- **Max iterations**: Use `--max-iterations N` to auto-stop after N iterations
- **Manual cancel**: Run `/bluera-base:cancel-milhouse` to stop immediately
- **Stuck detection**: Triggers after 3 identical gate failures (configurable)

## Context Harness

For long-running loops, use `--init-harness` to create tracking files:

```bash
/bluera-base:milhouse-loop task.md --init-harness
```

Creates:

- `.bluera/bluera-base/state/milhouse-plan.md` - Acceptance criteria checklist
- `.bluera/bluera-base/state/milhouse-activity.md` - Per-iteration progress log

Update these files each iteration to maintain context across compactions.

## Session Scoping

Each milhouse loop is tied to the terminal session that started it. If you have multiple Claude Code terminals in the same project, they won't interfere with each other's loops.

## State File

The loop state is stored in `.bluera/bluera-base/state/milhouse-loop.md`:

- Automatically gitignored via `.bluera/` pattern (with config.json excepted)
- Contains: iteration, max_iterations, completion_promise, session_id, gates, failure_hashes
- Full prompt text stored in file body (after `---` frontmatter)

## Token-Efficient Continuation

The milhouse hook uses pointer-based continuation to minimize token usage:

- **On each iteration**, the hook injects a short continuation message, NOT the full prompt
- The model continues based on conversation context and file state
- The full prompt remains in the state file and can be re-read if needed

This design saves ~80-90% of tokens compared to re-injecting the full prompt each iteration.

**Continuation message format:**

```text
Continue working on the milhouse task. Review your previous work visible in files and git history.
State: .bluera/bluera-base/state/milhouse-loop.md
```

If you need to refresh on the original task, read the state file directly.

## Use Cases

1. **TDD loops**: Keep iterating until all tests pass
2. **Performance optimization**: Iterate until benchmark targets are met
3. **Bug hunting**: Keep investigating until root cause is found
4. **Feature implementation**: Iterate through design, implement, test cycles

## Example: TDD Loop

```bash
/bluera-base:milhouse-loop .claude/prompts/add-auth.md \
  --gate "npm test" \
  --gate "npm run lint" \
  --max-iterations 20 \
  --init-harness
```

With prompt file:

```markdown
# Add JWT Authentication

## Requirements
- Add /login endpoint that returns JWT
- Add middleware to validate JWT on protected routes
- Add /me endpoint that returns current user

## Completion
Output <promise>TASK COMPLETE</promise> when all requirements met AND tests pass.
```
