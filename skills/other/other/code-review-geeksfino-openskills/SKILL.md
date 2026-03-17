---
name: code-review
description: Reviews code for quality, best practices, and potential issues. Use when asked to review, audit, or check code for problems.
allowed-tools: Read, Grep, Glob, LS
context: fork
agent: Explore
---

# Code Review Skill

Perform thorough code reviews following this methodology.

## Review Checklist

### 1. Correctness
- Does the code do what it's supposed to do?
- Are there any logic errors?
- Are edge cases handled?

### 2. Security
- Input validation and sanitization
- Authentication and authorization
- Sensitive data handling
- SQL injection, XSS, and other vulnerabilities

### 3. Performance
- Algorithm complexity
- Unnecessary computations
- Memory leaks or inefficient memory usage
- Database query optimization

### 4. Maintainability
- Code readability and clarity
- Appropriate naming conventions
- Single responsibility principle
- DRY (Don't Repeat Yourself)

### 5. Testing
- Test coverage
- Edge case testing
- Integration tests where appropriate

## Output Format

Structure your review as:

```
## Summary
[One paragraph overview]

## Critical Issues
[Must fix before merge]

## Suggestions
[Nice to have improvements]

## Positive Observations
[What's done well]
```

## Guidelines

- Be constructive, not critical
- Explain *why* something is an issue
- Suggest specific fixes when possible
- Acknowledge good patterns and practices
