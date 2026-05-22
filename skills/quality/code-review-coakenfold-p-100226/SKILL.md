---
name: code-review
description: "Review code changes with security, performance, and style checks"
argument-hint: "[file-or-directory]"
allowed-tools: "Read, Glob, Grep, Bash, Task"
---

# Code Review Workflow

> PROSE constraint: **Orchestrated Composition** — chains multiple analysis
> steps into a complete review process.

## Context Loading Phase

1. Get the changes to review:
   - If `$ARGUMENTS` is provided, review that file or directory
   - Otherwise, review uncommitted changes via `git diff`
2. Read the relevant `.claude/rules/` files for applicable standards

## Review Process

### 1. Security Scan

Check for OWASP Top 10 issues:
- SQL injection (string concatenation in queries)
- XSS (unescaped output)
- Hardcoded secrets or credentials
- Missing input validation
- Insecure direct object references

### 2. Code Quality

- Type safety (no `any`, proper null checks)
- Error handling (try-catch at boundaries, custom error types)
- Naming clarity (functions describe actions, variables describe values)
- DRY violations (duplicated logic that should be extracted)

### 3. Performance

- Render-blocking resources (JS without defer, large CSS)
- Unoptimized images (missing width/height, wrong format)
- N+1 query patterns in database code
- Unbounded list operations

### 4. Test Coverage

- Are new code paths tested?
- Do tests cover both success and error cases?
- Are edge cases addressed?

## Output Format

Organize findings by severity:

```markdown
## Review: [scope]

### Critical (must fix)
- [finding]

### Warning (should fix)
- [finding]

### Suggestion (nice to have)
- [finding]

### Looks Good
- [positive observation]
```

## Validation Gate

If critical issues are found, clearly state they must be resolved before merging.
