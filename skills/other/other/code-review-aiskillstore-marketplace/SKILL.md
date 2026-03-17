---
name: code-review
description: Perform comprehensive code reviews covering security, style, performance, and best practices. Use when reviewing code changes before commit or merge, auditing existing code, or checking for vulnerabilities.
---

# Skill: code-review

Purpose: Perform comprehensive code reviews covering security, style, performance, and best practices.

## When to use this Skill

Use this Skill when:

- Reviewing code changes before commit or merge.
- Auditing existing code for issues.
- Checking for security vulnerabilities.
- Ensuring code follows project conventions.

## Review workflow

### 1. Gather context

Before reviewing:

```bash
# See what changed
git diff --stat
git diff

# Or for specific files
git diff path/to/file
```

Understand:

- What is the purpose of these changes?
- Which files are affected?
- What is the expected behavior?

### 2. Security audit

Check for:

- [ ] **Injection vulnerabilities:** SQL, command, XSS.
- [ ] **Authentication issues:** Weak auth, missing checks.
- [ ] **Authorization flaws:** Missing permission checks.
- [ ] **Sensitive data exposure:** Hardcoded secrets, logs.
- [ ] **Insecure dependencies:** Known vulnerabilities.

Red flags:

- String concatenation in queries.
- `eval()`, `exec()`, or similar.
- Hardcoded credentials or API keys.
- Missing input validation.
- Overly permissive CORS.

### 3. Style check

Verify:

- [ ] **Naming conventions:** Clear, consistent names.
- [ ] **Code formatting:** Consistent indentation, spacing.
- [ ] **Documentation:** Comments where needed.
- [ ] **File organization:** Logical structure.
- [ ] **Import ordering:** Consistent imports.

### 4. Performance review

Look for:

- [ ] **N+1 queries:** Database access in loops.
- [ ] **Unnecessary computation:** Repeated calculations.
- [ ] **Memory issues:** Large allocations, leaks.
- [ ] **Blocking operations:** Sync in async contexts.
- [ ] **Inefficient algorithms:** O(n²) where O(n) possible.

### 5. Best practices

Check:

- [ ] **Error handling:** Proper try/catch, error types.
- [ ] **Logging:** Appropriate log levels.
- [ ] **Testing:** Test coverage for changes.
- [ ] **DRY principle:** No unnecessary duplication.
- [ ] **Single responsibility:** Functions do one thing.

### 6. Generate report

Summarize findings by severity:

```text
## Code Review Summary

### Critical (must fix)
- None found

### High (should fix)
- SQL injection risk in UserService.ts:42

### Medium (consider fixing)
- Function exceeds 50 lines in ApiHandler.ts:120

### Low (nice to have)
- Consider extracting magic number to constant

### Info
- Good use of early returns in validation logic
```

## Severity levels

| Level      | Description                        | Action            |
| ---------- | ---------------------------------- | ----------------- |
| `CRITICAL` | Security vulnerability, data loss  | Must fix now      |
| `HIGH`     | Bugs, significant issues           | Fix before merge  |
| `MEDIUM`   | Code quality, maintainability      | Fix soon          |
| `LOW`      | Minor improvements                 | Nice to have      |
| `INFO`     | Observations, positive feedback    | No action needed  |

## Common patterns

### SQL injection

**Bad:**

```typescript
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

**Good:**

```typescript
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### XSS vulnerability

**Bad:**

```typescript
element.innerHTML = userInput;
```

**Good:**

```typescript
element.textContent = userInput;
```

### N+1 query

**Bad:**

```typescript
const users = await getUsers();
for (const user of users) {
  user.posts = await getPosts(user.id);
}
```

**Good:**

```typescript
const users = await getUsersWithPosts();
```

### Missing error handling

**Bad:**

```typescript
const data = JSON.parse(input);
```

**Good:**

```typescript
try {
  const data = JSON.parse(input);
} catch (error) {
  logger.error('Invalid JSON input', { error });
  throw new ValidationError('Invalid input format');
}
```

## Integration

### With autonomous-ci

1. Make changes.
2. Run `code-review` to check.
3. Fix issues found.
4. Run `autonomous-ci` to verify.

### With smart-commit

1. Make changes.
2. Run `code-review` to check.
3. Fix issues.
4. Use `smart-commit` to commit.

## Checklist

Complete review checklist:

- [ ] Security vulnerabilities checked.
- [ ] Code style verified.
- [ ] Performance issues identified.
- [ ] Error handling reviewed.
- [ ] Test coverage assessed.
- [ ] Documentation checked.
- [ ] Report generated with findings.
