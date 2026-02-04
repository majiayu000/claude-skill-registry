---
name: claude-code-oneshot
description: Run Claude Code for deep coding sessions - one-shot execution, no back-and-forth. Use for complex tasks with lots of context that are straightforward to verify.
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      anyBins: ["claude"]
---

# Claude Code One-Shot

For deep coding sessions that need lots of context and are straightforward to test. One-shot execution — no questions, no help, just results.

## When to Use

- Complex refactoring or feature implementation
- Tasks with clear success criteria (tests pass, script runs, etc.)
- Delegating work that would bloat your context
- Parallel task execution across worktrees

## Basic Usage

```bash
# One-shot task (exits when done)
claude --print "Your detailed task here" --dangerously-skip-permissions

# In a specific directory
cd /path/to/project && claude --print "Build X" --dangerously-skip-permissions
```

## Key Flags

| Flag | Purpose |
|------|---------|
| `--print "prompt"` | One-shot mode, exits when complete |
| `--dangerously-skip-permissions` | Auto-approve all file/command operations |

## Prompt Style

Be explicit. Tell it exactly what to do and NOT to do:

```bash
claude --print "Create fizzbuzz.sh that prints FizzBuzz 1-30. Make it executable. ONE SHOT - no questions, just implement it." --dangerously-skip-permissions
```

Key phrases:
- "No questions, just do it"
- "ONE SHOT"
- "Do NOT ask for clarification"

## Background Execution

For longer tasks, run in background with PTY:

```bash
# Start in background
exec pty:true background:true workdir:~/project command:"claude --print 'Build a REST API for todos' --dangerously-skip-permissions"

# Monitor progress
process action:log sessionId:XXX

# Check completion
process action:poll sessionId:XXX
```

## Parallel Tasks with Worktrees

For multiple independent tasks:

```bash
# Create worktrees
git worktree add -b feat/auth /tmp/auth-work main
git worktree add -b feat/api /tmp/api-work main

# Run Claude Code in each (parallel)
cd /tmp/auth-work && claude --print "Implement OAuth2 login" --dangerously-skip-permissions &
cd /tmp/api-work && claude --print "Add REST endpoints for users" --dangerously-skip-permissions &

# Wait for both
wait
```

## NixOS Note

Claude Code may generate `#!/bin/bash` shebangs. Fix with:
```bash
sed -i '1s|#!/bin/bash|#!/usr/bin/env bash|' script.sh
```

## Rules

1. **Verify results** — run the code, check the tests, confirm it works
2. **Clear prompts** — ambiguity leads to questions or wrong output
3. **Isolated workspaces** — don't run in your main project directory for risky tasks
4. **Git init required** — Claude Code needs a git repo to operate
