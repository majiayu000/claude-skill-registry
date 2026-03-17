---
name: code-review
description: Automated code review checklist. Use when reviewing PRs or code changes.
license: MIT
---

# Code Review

Comprehensive checklist for reviewing code changes.

## Pre-Review Checklist

Before starting the review:

- [ ] Understand the context and requirements
- [ ] Check if tests are included
- [ ] Verify CI/CD passes

## Review Categories

### 1. Correctness

- Does the code do what it's supposed to?
- Are edge cases handled?
- Are there potential bugs or race conditions?

### 2. Design

- Is the code well-structured?
- Does it follow SOLID principles?
- Is there unnecessary complexity?

### 3. Readability

- Are variable/function names clear?
- Is the code self-documenting?
- Are comments helpful (not redundant)?

### 4. Performance

- Are there obvious performance issues?
- Is there unnecessary work being done?
- Are there N+1 queries or similar patterns?

### 5. Security

- Is user input validated?
- Are there potential injection vulnerabilities?
- Is sensitive data handled properly?

### 6. Testing

- Are tests comprehensive?
- Do tests cover edge cases?
- Are tests maintainable?

## Providing Feedback

- Be specific and constructive
- Explain the "why" behind suggestions
- Differentiate between blocking and non-blocking issues
- Acknowledge good code


## Parent Hub
- [_process-architecture-mastery](../_process-architecture-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
- [_workflow-security-audit](../_workflow-security-audit/SKILL.md)
