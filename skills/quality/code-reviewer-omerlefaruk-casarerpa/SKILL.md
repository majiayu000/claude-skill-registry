---
name: code-reviewer
description: Structured code review output format for the reviewer agent. Provides APPROVED/ISSUES format with file:line references. Use when: reviewing code changes, code quality checks, architecture compliance checks, approving code for merge, identifying critical/major/minor issues.
---

# Code Reviewer

Structured format for code reviews.

## Output Format

### If APPROVED

```markdown
## APPROVED

**Summary**: Brief description of what was reviewed

**Quality**: Good | Excellent
**Tests**: Adequate | Comprehensive
**Security**: No issues found

Proceed to QA phase.
```

### If ISSUES Found

```markdown
## ISSUES

### Critical (Must Fix)
1. **src/file.py:123** - Issue description
   - **Why**: Explanation
   - **Fix**: Suggested solution

### Major (Should Fix)
2. **src/file.py:456** - Issue description

### Minor (Consider)
3. **src/file.py:789** - Issue description
```

## Review Checklist

### Code Quality
- Readable, self-documenting code
- Small, single-responsibility functions (<50 lines)
- No placeholder code (TODO, pass, ...)
- Proper error handling with loguru logging
- Complete type hints on all functions

### Architecture Compliance
- Follows Clean DDD layers
- Dependencies flow inward
- Domain layer has NO external dependencies
- Nodes have logic + visual wrappers separate

### Async Patterns
- All Playwright operations are async
- Consistent async/await usage
- No blocking calls in async functions

## Severity Definitions

| Severity | Definition | Action |
|----------|------------|--------|
| Critical | Breaks functionality, security vulnerability | Must fix |
| Major | Reduces maintainability, missing tests | Should fix |
| Minor | Style, naming improvements | Consider |
