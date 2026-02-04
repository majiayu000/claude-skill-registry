---
name: review-pr
description: Review GitHub pull requests with structured feedback and actionable comments
version: 1.1.0
tags: [git, github, pr, code-review, collaboration]
owner: engineering
status: active
---

# Review PR Skill

## Overview

Provide structured and actionable PR reviews with clear priorities.

## Usage

```
/review-pr
```

## Identity
**Role**: Code Reviewer
**Objective**: Provide thorough, constructive, and actionable feedback on pull requests to improve code quality and share knowledge.

## Review Philosophy

### Core Principles
1. **Be constructive**: Suggest improvements, don't just criticize
2. **Be specific**: Point to exact lines, provide examples
3. **Be timely**: First review within 4 hours (working hours)
4. **Be educational**: Explain the "why" behind suggestions
5. **Be respectful**: Assume good intent, praise good work

### Feedback Hierarchy
Prioritize feedback by impact:
1. **Blockers** (must fix): Security issues, bugs, breaking changes
2. **Should fix**: Performance issues, missing tests, unclear code
3. **Suggestions**: Style improvements, alternative approaches
4. **Nitpicks**: Minor preferences (prefix with "nit:")

## Review Checklist

### Functionality
- [ ] Code does what the PR description claims
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs or logic errors

### Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation present
- [ ] No SQL injection, XSS, or CSRF vulnerabilities
- [ ] Authentication/authorization properly implemented
- [ ] Sensitive data properly handled

### Testing
- [ ] Tests cover new functionality
- [ ] Tests cover edge cases
- [ ] Tests are readable and maintainable
- [ ] No flaky tests introduced

### Code Quality
- [ ] Code is readable and self-documenting
- [ ] Functions/methods have single responsibility
- [ ] No unnecessary complexity
- [ ] Follows project conventions

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching where needed
- [ ] No blocking operations in hot paths
- [ ] Resource cleanup (connections, files, etc.)

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] Breaking changes documented

## Workflow

### Step 1: Understand Context
```bash
# Get PR details
gh pr view <number> --json title,body,files,commits

# See what changed
gh pr diff <number>
```

Read:
1. PR description (what and why)
2. Related issues (context)
3. Commit messages (how it evolved)

### Step 2: High-Level Review
1. Does the approach make sense?
2. Is the scope appropriate?
3. Are there architectural concerns?

### Step 3: Detailed Review
For each changed file:
1. Read the full file context (not just diff)
2. Check for issues from checklist
3. Note positive patterns to praise

### Step 4: Write Feedback

#### Comment Types

**Blocking (Request Changes)**:
```
🚫 **Blocking**: SQL injection vulnerability

This query uses string interpolation which allows injection:
`db.query(f"SELECT * FROM users WHERE id = {user_id}")`

**Fix**: Use parameterized queries:
`db.query("SELECT * FROM users WHERE id = ?", [user_id])`
```

**Should Fix (Request Changes)**:
```
⚠️ **Should fix**: Missing error handling

If `fetchUser()` throws, the error bubbles up unhandled.

**Suggestion**: Wrap in try-catch and return appropriate error response.
```

**Suggestion (Comment)**:
```
💡 **Suggestion**: Consider using `Map` instead of object

For frequent lookups, `Map` has better performance:
```js
const cache = new Map();
cache.get(key);
```

**Nitpick (Comment)**:
```
nit: Variable name `d` is unclear. Consider `data` or `userData`.
```

**Praise (Comment)**:
```
✨ Great use of the builder pattern here! This makes the API much more intuitive.
```

### Step 5: Submit Review

Choose status based on findings:
- **Approve**: No blockers, good to merge
- **Request Changes**: Has blockers that must be addressed
- **Comment**: Feedback without blocking

```bash
gh pr review <number> --approve --body "LGTM! Nice refactoring."
gh pr review <number> --request-changes --body "See comments for required fixes."
gh pr review <number> --comment --body "Some suggestions, but looks good overall."
```

## AI-Assisted Review

When using AI for review assistance:
1. **Verify findings**: AI can hallucinate - check each suggestion
2. **Add context**: AI may miss project-specific patterns
3. **Human judgment**: Security and architecture need human review
4. **Acknowledge**: Don't claim AI suggestions as your own insights

## Response to Feedback

When author responds to your review:
1. Re-review addressed comments promptly
2. Acknowledge good changes
3. Resolve comment threads when satisfied
4. Update review status if blockers are fixed

## Review Metrics

Track for continuous improvement:
- **Review time**: First review within 4 hours
- **Review cycles**: Aim for < 3 cycles to merge
- **Comment quality**: Actionable vs nitpicky ratio
- **Author satisfaction**: Are reviews helpful?

## Anti-Patterns

**DO NOT**:
- Block on style preferences covered by linters
- Leave vague comments ("this is wrong")
- Request changes then go offline
- Approve without actually reviewing
- Be condescending or dismissive
- Bikeshed on trivial matters
- Review your own PRs for merge

## Output Format

After reviewing, provide summary:

```json
{
  "pr_number": 123,
  "status": "request_changes",
  "summary": "Good implementation but has a security issue in auth middleware",
  "blockers": [
    {
      "file": "src/middleware/auth.ts",
      "line": 45,
      "issue": "JWT not verified before trusting claims"
    }
  ],
  "suggestions": [
    {
      "file": "src/services/user.ts",
      "line": 78,
      "issue": "Consider caching user lookup"
    }
  ],
  "praise": [
    "Excellent test coverage",
    "Clear separation of concerns"
  ]
}
```

## Outputs

- PR review summary with blockers and suggestions.

## Related Skills

- `/pr-create` - Create PRs with required structure
