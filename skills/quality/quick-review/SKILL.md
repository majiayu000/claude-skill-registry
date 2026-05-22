---
name: quick-review
description: Performs a fast, focused code review checking for common issues, security vulnerabilities, and best practices without over-engineering. Optimized for cost-efficiency by targeting specific concerns rather than broad exploration.
---

# Quick Review

Perform a targeted code review focusing on critical issues without unnecessary elaboration or over-engineering suggestions.

## Review Checklist

### Security & Safety
- SQL injection vulnerabilities
- XSS vulnerabilities
- Command injection risks
- Hardcoded secrets or credentials
- Unsafe file operations
- Authentication/authorization bypass risks

### Common Issues
- Unhandled errors or exceptions
- Resource leaks (files, connections, memory)
- Race conditions or concurrency bugs
- Off-by-one errors
- Null/undefined reference risks
- Type mismatches or coercion issues

### Code Quality
- Functions that are too complex (>50 lines)
- Duplicated code blocks
- Misleading variable/function names
- Commented-out code that should be removed
- Console.log or debug statements left in

### Performance Red Flags
- N+1 query problems
- Inefficient loops (O(n²) or worse when avoidable)
- Unnecessary re-renders or recalculations
- Missing database indexes for queries
- Large objects in state/props

## Guidelines

- **Be concise**: Report only actual issues found, not theoretical improvements
- **Prioritize**: Focus on bugs and security issues over style preferences
- **No over-engineering**: Don't suggest adding abstractions, patterns, or features unless there's a concrete problem
- **No unsolicited improvements**: Only review what was changed, not surrounding code
- **Cost-conscious**: Read only the files that changed, not the entire codebase
- **Specific**: Reference exact line numbers when reporting issues

## Output Format

```
## Issues Found: [N]

### Critical (must fix)
- file.ts:45 - [specific issue with explanation]

### Warnings (should fix)
- file.ts:78 - [specific issue with explanation]

### Notes (optional)
- [minor observations if relevant]
```

If no issues found: "✓ No critical issues detected in review."

## Examples

**Good usage:**
- Review changes before committing
- Quick sanity check on a new feature
- Verify a bug fix doesn't introduce new issues

**Avoid:**
- Reviewing entire codebases (use targeted file paths)
- Style/formatting nitpicks (use linters instead)
- Architectural reviews (use separate planning tools)
