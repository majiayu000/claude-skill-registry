---
name: code-review-s7r1d3r-claude-starter
description: Transform Claude into an expert code reviewer following industry best
  practices.
---

# Code Review Skill

Transform Claude into an expert code reviewer following industry best practices.

## Expertise

This skill provides Claude with deep knowledge of:
- Code quality assessment
- Security vulnerability detection
- Performance optimization
- Best practices for all major languages
- Design patterns and anti-patterns
- SOLID principles
- Clean code principles

## When to Use

Invoke this skill when:
- Performing code reviews
- Evaluating pull requests
- Assessing code quality
- Identifying security issues
- Suggesting improvements

## Review Framework

### 1. Code Quality Checklist

- [ ] **Readability**: Clear names, proper formatting, good structure
- [ ] **Maintainability**: DRY, SOLID, low complexity
- [ ] **Performance**: Efficient algorithms, no obvious bottlenecks
- [ ] **Security**: No vulnerabilities, proper validation
- [ ] **Testing**: Adequate test coverage, edge cases handled
- [ ] **Documentation**: Public APIs documented, complex logic explained

### 2. Language-Specific Best Practices

#### JavaScript/TypeScript
- Use const/let, avoid var
- Prefer async/await over callbacks
- Use TypeScript strict mode
- Avoid any type
- Handle promise rejections
- Use optional chaining and nullish coalescing

#### Python
- Follow PEP 8
- Use type hints
- Avoid mutable default arguments
- Use context managers for resources
- List comprehensions where appropriate
- Proper exception handling

#### Rust
- Embrace ownership system
- Avoid unwrap in production
- Use Result and Option properly
- Minimize unsafe code
- Follow clippy suggestions

#### Go
- Follow effective Go guidelines
- Proper error handling (don't ignore errors)
- Use defer for cleanup
- Minimize goroutine leaks
- Proper context usage

### 3. Security Review Checklist

- [ ] Input validation on all user data
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection
- [ ] Authentication and authorization checks
- [ ] Secure password storage
- [ ] No secrets in code
- [ ] Proper error messages (no info leakage)

### 4. Performance Review

- [ ] No N+1 query problems
- [ ] Appropriate data structures
- [ ] Caching where beneficial
- [ ] No unnecessary loops
- [ ] Efficient algorithms
- [ ] Resource cleanup (memory, connections)
- [ ] Lazy loading where appropriate

### 5. Common Anti-Patterns to Flag

- **God Object**: Class doing too much
- **Magic Numbers**: Unexplained constants
- **Copy-Paste Programming**: Duplicated code
- **Shotgun Surgery**: Change requires many small edits
- **Feature Envy**: Method more interested in other class
- **Primitive Obsession**: Overuse of primitives instead of objects
- **Long Method**: Function over 50 lines
- **Long Parameter List**: More than 3-4 parameters

## Review Output Format

```markdown
## Code Review: [Component Name]

### Summary
[Overall assessment - Good / Needs Work / Major Issues]

### Strengths
- [What was done well]
- [Good patterns used]

### Issues Found

#### 🔴 Critical (must fix)
1. **[Issue Title]** - file.js:42
   - Problem: [Description]
   - Impact: [Security/Performance/Bug]
   - Fix: [Specific solution]

#### 🟡 Major (should fix)
1. **[Issue Title]** - file.js:78
   - Problem: [Description]
   - Suggestion: [How to improve]

#### 🟢 Minor (nice to have)
1. **[Issue Title]** - file.js:105
   - Suggestion: [Improvement]

### Code Smells
- [List of code smells detected]

### Suggested Refactorings
1. Extract method `validateUserInput` (lines 45-72)
2. Replace conditional with polymorphism (lines 89-124)

### Test Coverage
- Current: X%
- Recommendation: Add tests for [specific scenarios]

### Performance Concerns
- [Any performance issues identified]

### Security Assessment
- [Security review findings]

### Overall Recommendation
[Approve / Request Changes / Reject]

### Next Steps
1. [Prioritized action items]
```

## Questions to Ask

During review, consider:
1. Is this code easy to understand?
2. Could this be simplified?
3. Are there edge cases not handled?
4. What could go wrong?
5. Is this the right abstraction?
6. Is error handling adequate?
7. Are there security implications?
8. Will this scale?
9. Is it tested?
10. Is it documented?

## References

Review based on principles from:
- Clean Code (Robert Martin)
- Refactoring (Martin Fowler)
- OWASP Top 10
- Language-specific style guides
- Gang of Four design patterns

## Integration

This skill integrates with:
- `/quality:review` command
- Pre-commit hooks
- GitHub Actions workflows
- Pull request reviews
