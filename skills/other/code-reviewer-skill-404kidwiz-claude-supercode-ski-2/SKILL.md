---
name: code-reviewer
description: Expert at quality-focused code review with security emphasis. Use when reviewing code changes, performing security audits, identifying bugs, ensuring code quality and maintainability, or analyzing pull requests for issues.
---

# Code Reviewer

## Purpose
Provides thorough code review expertise with focus on correctness, security, performance, and maintainability. Identifies bugs, security vulnerabilities, and code quality issues while suggesting improvements.

## When to Use
- Reviewing pull requests or code changes
- Performing security audits on code
- Identifying potential bugs before merge
- Ensuring code follows best practices
- Checking for performance issues
- Validating error handling
- Reviewing architectural decisions in code

## Quick Start
**Invoke this skill when:**
- Reviewing pull requests or code changes
- Performing security audits on code
- Identifying potential bugs before merge
- Ensuring code follows best practices
- Checking for performance issues

**Do NOT invoke when:**
- Debugging runtime issues (use debugger)
- Refactoring code structure (use refactoring-specialist)
- Writing new code (use language-specific skills)
- Reviewing system architecture (use architect-reviewer)

## Decision Framework
```
Review Priority:
├── Security issues → Block merge, fix immediately
├── Correctness bugs → Block merge, require fix
├── Performance issues → Discuss, may block
├── Code style issues → Suggest, non-blocking
├── Documentation gaps → Suggest, non-blocking
└── Refactoring opportunities → Note for future
```

## Core Workflows

### 1. Pull Request Review
1. Understand the intent from PR description
2. Review for correctness and logic errors
3. Check for security vulnerabilities
4. Assess performance implications
5. Verify error handling completeness
6. Check test coverage
7. Provide actionable feedback

### 2. Security-Focused Review
1. Check input validation and sanitization
2. Review authentication and authorization
3. Look for injection vulnerabilities
4. Verify sensitive data handling
5. Check for hardcoded secrets
6. Review dependency security
7. Assess cryptographic usage

### 3. Performance Review
1. Identify N+1 query patterns
2. Check for unnecessary allocations
3. Review algorithm complexity
4. Assess caching opportunities
5. Check for blocking operations
6. Review database query efficiency

## Best Practices
- Review code, not the author
- Be specific about issues and fixes
- Explain the "why" behind suggestions
- Prioritize comments by severity
- Acknowledge good patterns too
- Use automated tools first (linters, SAST)

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Nitpicking style | Wastes time, frustrates authors | Use automated formatters |
| No context | Reviewer doesn't understand changes | Read PR description, linked issues |
| Blocking on opinions | Delays delivery unnecessarily | Distinguish must-fix from nice-to-have |
| Drive-by reviews | Comments without resolution | Follow through on discussions |
| No positive feedback | Demoralizing for authors | Highlight good patterns |
