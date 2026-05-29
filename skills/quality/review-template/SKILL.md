---
name: review-template
description: Code review output templates with format specifications and severity guidance. Use when generating code reviews. Provides the review structure and quality bar.
user-invocable: false
---

# Code Review Template

This skill defines the output format, severity levels, and quality bar for code reviews.

## Output Format

Reviews are saved to: `.claude/agent-outputs/reviews/<YYYY-MM-DDTHHmmssZ>-<scope>-review.md`

### Document Structure

```markdown
## Summary

**Scope**: [Files/modules reviewed]
**Verdict**: [APPROVE | NEEDS CHANGES | REJECT]
**Key Finding**: [One sentence - the most important thing the author needs to know]

## Critical Issues

[Issues that MUST be fixed before merge. Empty section = none found.]

### Issue 1: [Descriptive Title]

**Location**: `file.py:42`
**Problem**: [What's wrong - specific and factual]
**Impact**: [Why it matters - security, correctness, data loss, etc.]
**Fix**: [Concrete suggestion]

## Improvements

[Issues that SHOULD be addressed. Grouped by category.]

### Organization
- `file.py:15` - [Issue and suggestion]

### Design
- `file.py:30` - [Issue and suggestion]

## Nitpicks

[Minor style/preference items. Keep brief - one line each.]

- `file.py:10` - [Issue]
- `file.py:25` - [Issue]

## Questions

[Clarifications needed before approval. Don't use for rhetorical questions.]

1. [Specific question about intent or requirements]
```

## Severity Definitions

| Level | Criteria | Blocks Merge? |
|-------|----------|---------------|
| **Critical** | Security vulnerabilities, data corruption, crashes, wrong behavior | Yes |
| **Improvement** | Design flaws, maintainability issues, missing error handling | No, but should address |
| **Nitpick** | Style, naming, minor inconsistencies | No |

### Critical Issue Examples

- SQL injection, XSS, command injection
- Race conditions causing data corruption
- Unhandled exceptions that crash the app
- Logic errors producing wrong results
- Missing authentication/authorization checks

### NOT Critical (even if bad)

- Missing docstrings
- Inconsistent naming
- Suboptimal performance (unless severe)
- Code duplication
- Missing type hints

## Verdict Criteria

| Verdict | When to Use |
|---------|-------------|
| **APPROVE** | No critical issues. Improvements are suggestions, not blockers. |
| **NEEDS CHANGES** | Has critical issues OR many significant improvements needed. |
| **REJECT** | Fundamental design problems requiring rearchitecture. |

## Writing Guidelines

### Be Specific

```markdown
# INCORRECT - vague
The error handling could be better.

# CORRECT - specific
`file.py:42` - Bare `except:` catches KeyboardInterrupt and SystemExit.
Catch specific exceptions: `except (ValueError, KeyError):`.
```

### Be Concise

```markdown
# INCORRECT - verbose
I noticed that on line 42, there appears to be an issue where the function
is not properly validating its input parameters before proceeding with the
main logic, which could potentially lead to unexpected behavior if invalid
data is passed in by the caller.

# CORRECT - direct
`file.py:42` - No input validation. Add: `if not data: raise ValueError("data required")`
```

### Explain Impact, Not Just Rules

```markdown
# INCORRECT - rule citation
This violates PEP 8 naming conventions.

# CORRECT - explains why it matters
`user_ID` mixes snake_case with uppercase. Inconsistent naming makes
code harder to search and remember. Use `user_id`.
```

### Skip Empty Sections

If a section has no items, omit it entirely. Don't write "None found" or "N/A".

### Prioritize

Don't bury critical issues under 20 nitpicks. Lead with what matters.

## Anti-Pattern: Review Inflation

Avoid these behaviors that reduce review value:

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Praise padding | "Great work! However..." dilutes feedback | Skip pleasantries, state findings |
| Hedging | "Maybe consider..." sounds uncertain | State clearly what should change |
| Rhetorical questions | "Should this be validated?" | State: "Add validation for X" |
| Style policing | Flagging every minor preference | Pick battles, focus on substance |
| Kitchen sink | Listing every possible improvement | Limit to actionable items |

## Convention References

When flagging convention violations, reference the skill:

```markdown
**Convention**: See `function-design` skill: Guard Clauses
```

This lets authors learn the standard, not just the specific fix.
