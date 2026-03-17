---
name: milhouse
description: Iterative development loop that feeds the same prompt back after each iteration until task completion.
argument-hint: "<prompt-file> [--inline TEXT] [--max-iterations N] [--promise TEXT] [--gate CMD] [--stuck-limit N] [--init-harness]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
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
/bluera-base:milhouse .claude/prompts/my-task.md

# With max iterations and gates
/bluera-base:milhouse task.md --max-iterations 10 --gate "npm test"

# Inline prompt (for simple tasks)
/bluera-base:milhouse --inline "Refactor the auth module to use JWT tokens"

# With context harness (creates plan.md and activity.md)
/bluera-base:milhouse task.md --init-harness
```

See [references/options.md](references/options.md) for all options.

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

## Gates & Stopping

- **Gates**: Commands that must pass before exit. See [references/gates.md](references/gates.md).
- **Max iterations**: Use `--max-iterations N` to auto-stop
- **Manual cancel**: Run `/bluera-base:milhouse cancel`
- **Stuck detection**: Auto-stops after 3 identical gate failures

## Internals

For state file format and token-efficient continuation, see [references/internals.md](references/internals.md).

## Use Cases

1. **TDD loops**: Keep iterating until all tests pass
2. **Performance optimization**: Iterate until benchmark targets are met
3. **Bug hunting**: Keep investigating until root cause is found
4. **Feature implementation**: Iterate through design, implement, test cycles

## Example: TDD Loop

```bash
/bluera-base:milhouse .claude/prompts/add-auth.md \
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
