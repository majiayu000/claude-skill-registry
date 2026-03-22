---
name: review-checklist
description: >
  Systematic code review checklist with severity classification. Activate whenever the user
  asks for a code review, wants feedback on their code, submits a PR for review, or asks
  what to look for when reviewing code. Also activate when writing review comments or
  discussing code quality standards.
---

# Code Review Checklist

A systematic approach to code review with categorized checks and severity levels.
Focus on issues that matter most: correctness, security, and maintainability.
Provide constructive, actionable feedback.

## When to Use
- Reviewing a pull request or code changes
- Asking Claude to review code you wrote
- Setting up code review standards for a team
- Learning what to look for in code reviews
- Writing review comments on PRs

## Core Patterns

### Severity Levels

Classify every finding by severity to prioritize fixes.

```
CRITICAL - Must fix before merge. Security vulnerabilities, data loss risks,
           broken functionality, production crashes.

HIGH     - Should fix before merge. Bugs, race conditions, missing error handling,
           performance issues with measurable impact.

MEDIUM   - Fix soon, can merge with follow-up ticket. Code smells, missing tests
           for edge cases, suboptimal patterns, unclear naming.

LOW      - Optional improvement. Style preferences, minor readability tweaks,
           documentation suggestions.
```

### Correctness Checks

The most important category. Does the code do what it claims?

```typescript
// CHECK: Off-by-one errors
// WRONG
for (let i = 0; i <= items.length; i++) { // Off-by-one: should be <
  process(items[i]); // items[items.length] is undefined
}

// CHECK: Null/undefined handling
// WRONG
function getDisplayName(user: User): string {
  return user.profile.displayName; // What if profile is null?
}
// CORRECT
function getDisplayName(user: User): string {
  return user.profile?.displayName ?? user.email;
}

// CHECK: Async error handling
// WRONG
async function fetchData() {
  const response = await fetch('/api/data'); // Unhandled rejection
  return response.json();
}
// CORRECT
async function fetchData() {
  const response = await fetch('/api/data');
  if (!response.ok) {
    throw new Error(`Fetch failed: ${response.status} ${response.statusText}`);
  }
  return response.json();
}
```

### Security Checks

Review every PR for security implications.

```typescript
// CHECK: User input flows to dangerous sinks
// Look for: SQL queries, HTML rendering, file paths, shell commands,
// redirects, eval(), RegExp constructors

// CHECK: Authorization on every endpoint
// WRONG: Only checks authentication, not authorization
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  await db.posts.delete(req.params.id); // Anyone authenticated can delete any post
});
// CORRECT: Verify ownership
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  const post = await db.posts.findById(req.params.id);
  if (post.authorId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  await db.posts.delete(req.params.id);
});

// CHECK: Sensitive data exposure
// WRONG: Returning password hash to client
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user); // Includes passwordHash, internalNotes, etc.
});
// CORRECT: Select only needed fields
const { id, name, email, avatar } = await db.users.findById(req.params.id);
res.json({ id, name, email, avatar });
```

### Performance Checks

Identify patterns that cause performance issues at scale.

```typescript
// CHECK: N+1 queries
// WRONG
const posts = await db.posts.findMany();
for (const post of posts) {
  post.author = await db.users.findById(post.authorId); // N+1 queries
}
// CORRECT
const posts = await db.posts.findMany({
  include: { author: true }, // Single query with join
});

// CHECK: Unbounded queries
// WRONG
const allUsers = await db.users.findMany(); // Returns entire table
// CORRECT
const users = await db.users.findMany({ take: 50, skip: offset });

// CHECK: Missing indexes implied by query patterns
// If reviewing a new query with WHERE clauses, verify indexes exist
```

### Constructive Feedback Format

Write reviews that teach, not criticize.

```markdown
## Good review comment format:

**[MEDIUM] Consider using `Map` instead of object for dynamic keys**
The current approach uses a plain object as a lookup table. `Map` provides
better performance for frequent additions/deletions and avoids prototype
pollution risks.

```typescript
// Current
const cache: Record<string, Data> = {};
cache[key] = value;

// Suggested
const cache = new Map<string, Data>();
cache.set(key, value);
```

---

## Bad review comment format:

"This is wrong, use a Map."
(No severity, no explanation, no example, not constructive)
```

### Review Checklist Summary

Walk through this list for every PR:

```markdown
## Correctness
- [ ] Logic handles edge cases (empty arrays, null, zero, negative numbers)
- [ ] Error states are handled (network failures, invalid data, timeouts)
- [ ] Async operations have proper error handling
- [ ] No race conditions in concurrent code

## Security
- [ ] User input is validated at the boundary
- [ ] Authorization checks on every resource access
- [ ] No sensitive data in logs, responses, or error messages
- [ ] No hardcoded secrets or credentials

## Maintainability
- [ ] Functions are focused and under 50 lines
- [ ] Variable and function names clearly express intent
- [ ] No unnecessary complexity or premature abstraction
- [ ] Changes are consistent with existing codebase patterns

## Testing
- [ ] New code has corresponding tests
- [ ] Edge cases are tested
- [ ] Tests verify behavior, not implementation details
- [ ] No flaky test patterns (timeouts, order-dependence)

## Performance
- [ ] No N+1 query patterns
- [ ] Database queries are bounded (LIMIT/pagination)
- [ ] No unnecessary re-renders in UI code
- [ ] Large data sets are handled with streaming or pagination
```

## Anti-Patterns
- Nitpicking style issues that should be handled by linters/formatters
- Rubber-stamping PRs without reading the code ("LGTM" with no comments)
- Rewriting the author's approach in your preferred style without justification
- Blocking on LOW severity items
- Providing only negative feedback with no constructive suggestions
- Reviewing only the diff without understanding the broader context
- Leaving ambiguous comments like "this seems wrong" without explanation

## Quick Reference

| Priority | Focus Area | Key Questions |
|----------|-----------|---------------|
| 1 | Correctness | Does it work? Edge cases handled? |
| 2 | Security | Input validated? Auth checked? Secrets safe? |
| 3 | Performance | N+1 queries? Unbounded results? |
| 4 | Maintainability | Readable? Testable? Consistent? |
| 5 | Testing | Tests exist? Cover edge cases? |
| 6 | Style | Handled by linters, not reviewers |
