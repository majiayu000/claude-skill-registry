---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Review Skill

When reviewing code, follow this comprehensive checklist:

## 1. Code Quality

### Readability
- Is the code easy to understand?
- Are variable and function names descriptive?
- Is the code properly formatted?
- Are comments helpful and accurate?

### Structure
- Are functions small and focused?
- Is the code organized logically?
- Is there appropriate separation of concerns?
- Are dependencies managed well?

### Maintainability
- Is the code DRY (Don't Repeat Yourself)?
- Are magic numbers avoided?
- Is the code testable?
- Is error handling comprehensive?

## 2. Security

### Data Protection
- No hardcoded secrets or credentials?
- Sensitive data properly handled?
- No sensitive data in logs?

### Input Validation
- All user input validated?
- SQL injection prevented?
- XSS attacks prevented?

### Authentication/Authorization
- Proper access controls?
- Sessions managed securely?

## 3. Performance

### Efficiency
- Appropriate algorithms used?
- Database queries optimized?
- No unnecessary iterations?

### Resources
- Memory usage reasonable?
- Connections properly closed?
- Caching implemented where beneficial?

## 4. Testing

### Coverage
- New code has tests?
- Edge cases covered?
- Error scenarios tested?

### Quality
- Tests are meaningful?
- Tests are maintainable?
- Tests run quickly?

## Output Format

For each issue found:

```
### [Priority: Critical/Warning/Suggestion]

**Location**: file.ts:42

**Issue**: Description of the problem

**Suggestion**: How to fix it

**Example**:
```code
// Fixed code example
```
```
