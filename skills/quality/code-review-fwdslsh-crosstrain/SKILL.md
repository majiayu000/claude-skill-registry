---
name: code-review
description: Provides thorough code review with actionable feedback
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

## Purpose
Perform thorough code reviews that identify issues and suggest improvements.

## Review Checklist

When reviewing code, check for:

### Code Quality
- [ ] Clear variable and function names
- [ ] DRY (Don't Repeat Yourself) principles
- [ ] Single responsibility principle
- [ ] Appropriate error handling

### Security
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Sensitive data handling

### Performance
- [ ] Unnecessary loops or iterations
- [ ] Database query optimization
- [ ] Memory leaks
- [ ] Caching opportunities

### Maintainability
- [ ] Code documentation
- [ ] Test coverage
- [ ] Consistent coding style
- [ ] Clear module boundaries

## Feedback Format

Provide feedback in this format:
1. **Issue**: Description of the problem
2. **Location**: File and line number
3. **Severity**: Critical/Major/Minor/Suggestion
4. **Fix**: Recommended solution
