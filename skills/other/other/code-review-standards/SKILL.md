---
name: code-review-standards
description: Use when the Architect is reviewing code changes, evaluating pull requests, assessing implementation quality, checking for security issues, or verifying code follows architectural patterns. Activates for any code review, implementation evaluation, or quality assessment.
version: 1.0.0
---

# Code Review Standards

## When This Applies

Apply this guidance when:
- Reviewing code submitted for review (tasks in `review` status)
- Evaluating whether an implementation follows the architecture
- Checking for security, performance, or quality issues
- Providing feedback to Developer via the queue

## Review Checklist

### 1. Architecture Alignment

- [ ] Follows the component boundaries defined in ARCHITECTURE.md
- [ ] Uses the prescribed patterns (not introducing new patterns without discussion)
- [ ] API contracts match the design specification
- [ ] Data model changes are consistent with the schema design
- [ ] No unauthorized cross-component dependencies

### 2. Code Quality

- [ ] Functions are focused (single responsibility)
- [ ] Naming is clear and consistent with project conventions
- [ ] No dead code, commented-out blocks, or debug artifacts
- [ ] Error handling is appropriate (not swallowing errors)
- [ ] No hardcoded values that should be configurable

### 3. Security

- [ ] No hardcoded secrets, tokens, or credentials
- [ ] Input validation at system boundaries
- [ ] SQL queries use parameterized statements (no string concatenation)
- [ ] Authentication/authorization checks are in place
- [ ] No sensitive data in logs or error messages
- [ ] Dependencies are from trusted sources

### 4. Performance

- [ ] No N+1 query patterns
- [ ] Appropriate use of caching where needed
- [ ] No blocking operations in async contexts
- [ ] Large data sets are paginated
- [ ] No unnecessary database calls in loops

### 5. Maintainability

- [ ] Code is self-documenting (comments explain WHY, not WHAT)
- [ ] Complex logic has explanatory comments
- [ ] No deep nesting (max 3 levels)
- [ ] Consistent formatting with project style
- [ ] Changes are minimal and focused on the task

## Review Feedback Format

Structure feedback as:

```
TASK-NNN Code Review

APPROVED / NEEDS CHANGES / REJECTED

Strengths:
- What was done well

Issues:
- [MUST FIX] Critical issues that block approval
- [SHOULD FIX] Important issues for code quality
- [CONSIDER] Suggestions for improvement

Next Steps:
- What the Developer should do
```

## Review Decision Criteria

| Decision | Criteria |
|----------|----------|
| **APPROVED** | No critical issues, meets architecture, tests pass |
| **NEEDS CHANGES** | Minor issues that need fixing, re-review not needed |
| **REJECTED** | Fundamental approach is wrong, needs redesign |
