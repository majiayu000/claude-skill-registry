---
name: styled-jsx-audit
description: Audit styled-jsx usage for scoping leaks, overly global selectors, unsafe interpolations, and maintainability issues; propose targeted refactors.
argument-hint: "[path or ComponentName]"
allowed-tools: Read, Grep, Glob
disable-model-invocation: true
---

# styled-jsx Audit Skill

Audit for correctness and best practices.

## Check for

- Incorrect use of global styles
- Excessive :global selectors or broad resets
- Deep descendant selectors
- Unsafe CSS interpolations
- Missing focus-visible states on interactive controls
- Styling via brittle DOM structure
- Missing className pass-through when needed

## Output expectations

- Findings (bullets)
- Severity (low/med/high)
- Refactor plan with minimal changes
- Test/story updates needed
