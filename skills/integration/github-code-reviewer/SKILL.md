---
name: github-code-reviewer
description: Review GitHub PRs with surgical precision. Flag only high-severity issues (bugs, security, performance, breaking changes) via succinct inline comments on specific lines. Skip style, nits, and minor improvements. High signal, low noise.
allowed-tools: Read, Glob, Grep, Bash
---

# GitHub Code Reviewer

High-precision code review that flags critical issues only. Leave inline comments on specific lines—no verbose summaries.

## Core Principle: High Signal, Low Noise

**Only flag these:**
- **Bugs**: Logic errors, crashes, incorrect behavior, unhandled edge cases
- **Security**: SQL injection, XSS, auth bypass, credential leaks, input validation gaps
- **Performance**: N+1 queries, inefficient algorithms, memory leaks, missing indexes
- **Breaking changes**: API incompatibilities, data migration issues
- **Critical architectural violations**: Layer separation breaks, major pattern deviations

**Never flag these:**
- Style preferences, formatting, naming conventions
- Minor improvements, optimizations, or refactoring suggestions
- Nits, typos, comments about comments
- Positive feedback (unless code prevents a critical bug)
- Anything that doesn't materially affect correctness, security, or performance

## Workflow

### 1. Get PR Context (Fast)
```bash
python scripts/get_pr_info.py <pr_url_or_number>
python scripts/get_pr_diff.py <pr_url_or_number>
```

### 2. Gather System Context (Critical)
**Never review in isolation.** Use tools to understand the larger system:
- `Read`: Check files that interact with changes (callers, implementations, tests)
- `Grep`: Find similar patterns, conventions, how problems are solved elsewhere
- `Glob`: Locate integration points (schemas, APIs, service interfaces)

### 3. Identify Critical Issues Only
Scan for **high-severity problems**:

**Bugs**: Null derefs, unhandled errors, logic errors, edge case failures
**Security**: Injection vulnerabilities, auth bypass, credential exposure, missing validation
**Performance**: N+1 queries, inefficient algorithms, memory/resource leaks
**Breaking changes**: API incompatibilities, migration issues
**Architecture**: Service layer calling external APIs directly, repository layer doing validation

**Skip everything else.** Don't comment on style, naming, minor refactors, or improvements.

### 4. Leave Inline Comments (Required Pattern)

**Primary approach: Inline comments on specific lines where issues exist.**

**Use JSON file + submit_review.py for all reviews:**

1. Create JSON in /tmp with inline comments:
```bash
# Use /tmp to avoid cluttering working directory
/tmp/pr-<number>-review.json
```

Example content:
```json
[
  {
    "path": "src/services/user.service.ts",
    "line": 42,
    "body": "bug: Null reference exception if user.profile is undefined"
  },
  {
    "path": "src/db/queries.ts",
    "line": 89,
    "body": "security: SQL injection via string concatenation - use parameterized query"
  }
]
```

2. Submit as commentary only (never approve/reject):
```bash
python scripts/submit_review.py <pr_number> \
  --repo owner/repo \
  --comments-file /tmp/pr-<number>-review.json \
  --event COMMENT
```

**Always use `--event COMMENT`** - skill provides commentary only, humans make approval decisions.

**When to use summary comment:** Only if issue affects entire PR (e.g., "This PR breaks backward compatibility for all API consumers").

## Comment Format (Succinct)

**Pattern:** `category: issue` (1-2 lines max)

**Examples:**

```
bug: Null pointer exception if response.data is undefined
```

```
security: SQL injection - use parameterized queries instead of string concatenation
```

```
performance: N+1 query - fetch all records with single query instead of loop
```

```
breaking: API response structure changed - will break existing clients
```

**No verbose explanations. No suggested code blocks unless absolutely necessary. Just state the issue and impact.**

## Common Critical Patterns to Check

**Only flag if violation causes actual bug/security/performance issue:**

### General Bugs
- **Nil/null pointer dereferences**: Missing null checks causing crashes
- **Unhandled errors**: Errors silently ignored without proper handling
- **Resource leaks**: Unclosed connections, file handles, or memory leaks
- **Race conditions**: Concurrent access without synchronization

### Security Issues
- **SQL injection**: String concatenation in queries instead of parameterized queries
- **XSS vulnerabilities**: Unescaped user input rendered in HTML
- **Authentication bypass**: Missing auth checks on protected routes/endpoints
- **Authorization gaps**: Missing permission/scope validation
- **Credential exposure**: API keys, secrets, or passwords in code

### Performance Problems
- **N+1 queries**: Database queries in loops instead of batch operations
- **Missing indexes**: Queries on unindexed columns with large datasets
- **Inefficient algorithms**: O(n²) where O(n log n) or O(n) is possible
- **Memory inefficiency**: Loading entire datasets when streaming is appropriate

### Architecture Violations
- **Layer separation breaks**: Business logic in presentation layer, database calls in handlers
- **Tight coupling**: Hard dependencies that should be injected or abstracted

**Context matters:** Check project's CLAUDE.md or similar documentation for project-specific patterns before flagging architectural issues.
