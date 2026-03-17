---
name: fix
description: |
  Bug investigation and resolution workflow. Use when the user mentions:
  - "fix", "broken", "not working", "bug", "error", "issue", "failing"
  - debugging, troubleshooting, investigating problems
  - something that used to work but doesn't anymore
  - errors in console, build failures, test failures
context: fork
---

# Bug Fix Workflow

You are in **Maestro orchestration mode**. Delegate immediately to specialized agents.

## Workflow

1. **Explore** - Spawn `explore` agent to understand the affected codebase area
2. **Reproduce** - Spawn `tester` agent to create a failing test if possible
3. **Diagnose** - Analyze findings to identify root cause
4. **Implement** - Spawn `implementer` agent to fix the issue
5. **Verify** - Spawn `tester` agent to confirm the fix
6. **Learn** - If this was a non-obvious fix, auto-invoke `/learn store bug "..."` to remember it

## Scope Rules

Follow CLAUDE.md Guardrails (scope constraint, 2-iteration limit). Only modify files directly related to the bug.

**Build after every fix**: Run the build after each individual fix attempt. Never stack multiple untested fixes -- verify green before moving on. If the build breaks, fix *that* before continuing.

## Agent Delegation

```
Task(explore, "Investigate the bug: $ARGUMENTS. Find relevant files, trace the issue.")
Task(tester, "Create a failing test that reproduces: $ARGUMENTS")
Task(implementer, "Fix the bug based on findings: [summary from explore] SCOPE: Only modify files identified in exploration. Do NOT refactor adjacent code. Run the build after each fix to verify.")
Task(reviewer, "Quick review of the fix for quality and edge cases")
```

## Output

Return a concise summary:
- **Root cause**: What was wrong
- **Fix applied**: What changed
- **Files modified**: List of files
- **Verification**: How it was tested
- **Learning stored**: If applicable

## Remember

- If the fix involves a library API, **fetch docs first** via `/docs <library>` — APIs change between versions
- Always store non-obvious bug fixes as learnings
- Check if similar bugs were fixed before (recall learnings)
- Run tests after fixing
