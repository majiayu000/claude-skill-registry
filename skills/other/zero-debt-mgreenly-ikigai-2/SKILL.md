---
name: zero-debt
description: Zero Technical Debt skill for the ikigai project
---

# Zero Technical Debt

## Description
Zero technical debt philosophy and work style principles for ikigai.

## Details

### Zero Technical Debt Principle

When you discover any problem, inconsistency, or standards violation:

1. Fix it immediately - don't defer or document
2. Fix it completely - address root cause, not symptoms
3. Fix it systematically - search for similar issues elsewhere

Examples requiring immediate fixes:
- Missing assertions on function preconditions
- Inconsistent naming conventions
- Code violating error handling philosophy
- Test coverage gaps
- Code not following established patterns

**When to ask first:**
- Architectural changes
- Unclear which solution is correct
- Breaking changes to public APIs
- Uncertainty about project conventions

If you discover deficiencies in existing code while working nearby, fix them as part of your current work.

### Work Style

**CRITICAL**: Do not make architectural, structural, or refactoring changes unless explicitly requested.

Acceptable without asking:
- Formatting with `make fmt`
- Running `make check` and `make lint`
- Minor code style consistency

When discussing improvements:
- Present options and trade-offs
- Wait for explicit approval before implementing
