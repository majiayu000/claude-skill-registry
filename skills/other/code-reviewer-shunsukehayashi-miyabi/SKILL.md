---
name: code-reviewer
description: Review code for best practices, bugs, security issues, and improvements. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Code Reviewer

**Version**: 1.0.0
**Purpose**: Comprehensive code review with quality scoring

---

## Triggers

| Trigger | Examples |
|---------|----------|
| Review request | "review this code", "check this PR", "コードレビューして" |
| Quality check | "is this code good?", "品質チェック" |
| Bug hunt | "find bugs", "バグを探して" |

---

## Review Checklist

### 1. Correctness

```typescript
// Check for off-by-one errors
for (let i = 0; i < array.length; i++) { }  // Correct
for (let i = 0; i <= array.length; i++) { } // Bug

// Check null handling
const value = obj?.property ?? defaultValue;
```

- [ ] Logic is correct
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] Null/undefined checks

### 2. Security

```typescript
// SQL injection prevention
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]); // Parameterized

// XSS prevention
const safe = DOMPurify.sanitize(userInput);
```

- [ ] Input validation
- [ ] No SQL injection
- [ ] No XSS vulnerabilities
- [ ] Secrets not hardcoded

### 3. Performance

```typescript
// Avoid N+1 queries
const users = await db.query(`
  SELECT u.*, array_agg(o.*) as orders
  FROM users u LEFT JOIN orders o ON u.id = o.user_id
  GROUP BY u.id
`);
```

- [ ] No N+1 queries
- [ ] Proper indexing
- [ ] Efficient algorithms
- [ ] Memory management

### 4. Maintainability

- [ ] Clear naming
- [ ] Single responsibility
- [ ] DRY principle
- [ ] Proper types (TypeScript)

---

## Quality Score (100 points)

| Category | Weight | Criteria |
|----------|--------|----------|
| Correctness | 30 | Logic, edge cases, error handling |
| Security | 25 | OWASP Top 10 compliance |
| Performance | 20 | Efficiency, no bottlenecks |
| Maintainability | 15 | Readability, structure |
| Testing | 10 | Coverage, quality |

**Pass threshold**: 80+ points

---

## Output Format

```json
{
  "score": 85,
  "issues": [
    {
      "severity": "warning",
      "file": "src/api.ts",
      "line": 42,
      "message": "Consider adding error handling"
    }
  ],
  "suggestions": ["Add unit tests", "Extract helper function"]
}
```
