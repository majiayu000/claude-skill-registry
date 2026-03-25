---
name: review
description: Review current code changes for quality, security, and performance issues
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

Review all current code changes thoroughly.

## Steps

1. **Get the diff**
   ```
   git diff
   git diff --cached
   ```

2. **Read each changed file** in full to understand context

3. **Check for issues in these categories:**

### Code Quality
- Dead code or unused imports
- Duplicated logic
- Functions too long (> 50 lines)
- Deeply nested conditionals
- Magic numbers or hardcoded strings
- Missing error handling
- Inconsistent naming

### Security
- Hardcoded secrets, API keys, passwords
- SQL injection vulnerabilities
- XSS vulnerabilities
- Unsanitized user input
- Insecure crypto or hashing
- Missing authentication/authorization checks
- Sensitive data in logs

### Performance
- N+1 query patterns
- Missing database indexes
- Unnecessary re-renders (React)
- Large synchronous operations
- Missing pagination
- Memory leaks (unclosed resources)

### Conventions
- Does it follow existing codebase patterns?
- Consistent with CLAUDE.md rules?
- Test coverage for new code?

4. **Output structured review:**

```
## Code Review Summary

### Critical (must fix)
- [file:line] [issue]

### Warning (should fix)
- [file:line] [issue]

### Suggestion (nice to have)
- [file:line] [issue]

### Good
- [what was done well]
```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
