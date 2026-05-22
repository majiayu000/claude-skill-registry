---
name: code-review
description: "Self-review before declaring work complete"
---

# Code Review

## Core Principle

Review your own code before declaring it done. You're your first code reviewer.

## When to Use

- After completing a feature
- After fixing a bug
- Before committing code
- Before creating a pull request

## Protocol

### 1. Announce

State that you're doing a review:
> "I'm reviewing the implementation before marking it complete."

### 2. Check Requirements

- Does this do what was asked?
- Are all requirements met?
- Any edge cases missing?

### 3. Code Quality Review

Run through these checks:

**Security**
- [ ] No SQL injection (use parameterized queries)
- [ ] No XSS (escape output)
- [ ] Input validation present
- [ ] Auth/authz implemented
- [ ] No secrets in code

**Performance**
- [ ] No N+1 queries
- [ ] Indexes on frequently queried columns
- [ ] No unnecessary loops

**Error Handling**
- [ ] Errors handled gracefully
- [ ] Appropriate error messages
- [ ] No uncaught exceptions

**Code Structure**
- [ ] Functions do one thing
- [ ] No unnecessary duplication
- [ ] Clear naming
- [ ] Comments only where needed

### 4. Run Tests

```bash
# With database backup
./scripts/safe-test.sh [your test command]
```

Check:
- [ ] Tests exist for new code
- [ ] All tests pass
- [ ] Edge cases tested

### 5. Report Findings

**If clean:**
```
Review complete. All requirements met, tests passing, no issues found.
```

**If issues found:**
```
Review found issues:

Critical (must fix):
- [issue] at [location]

Minor (should fix):
- [issue] at [location]

Fixing critical issues before completing.
```

### 6. Fix Issues

Fix critical issues before declaring done. Document minor issues for later.

## Checklist Summary

| Category | Check |
|----------|-------|
| Requirements | All met? |
| Security | SQL injection, XSS, auth? |
| Performance | N+1 queries, indexes? |
| Tests | Exist, pass, coverage? |
| Code | Readable, DRY, named well? |

## Tips

- Review the full file, not just your changes
- Run tests as part of review
- Fix critical issues before committing
- Document what you reviewed

## After Review

Use `verification-before-completion` skill for final checks before declaring done.
