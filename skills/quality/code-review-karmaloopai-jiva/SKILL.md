---
name: code-review
description: >
  Perform comprehensive code reviews covering bugs, style, performance, security,
  and best practices. Use this skill when the user mentions: review my code,
  check this code, code review, find bugs, improve code, refactor suggestions,
  security audit, performance optimization, code quality, static analysis.
license: MIT
metadata:
  author: Jiva Community
  version: 1.0.0
  tags: [code-quality, security, performance, best-practices]
---

# Code Review Skill

## Overview
Perform comprehensive code reviews analyzing bugs, style issues, performance bottlenecks, security vulnerabilities, and adherence to best practices.

## Workflow

### 1. Scan Code Structure
- Use `view` tool to read all relevant files in the codebase
- Identify file types, frameworks, and languages used
- Map dependencies and module relationships

### 2. Analyze Code Quality
Check for the following categories:

**Bugs & Logic Errors:**
- Null/undefined handling
- Off-by-one errors
- Race conditions
- Memory leaks
- Incorrect algorithm implementation

**Security Issues:**
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization flaws
- Sensitive data exposure
- Unsafe dependencies

**Performance Problems:**
- Inefficient algorithms (O(n²) where O(n) possible)
- Unnecessary database queries
- Memory overuse
- Blocking operations
- Missing caching

**Code Style:**
- Naming conventions
- Code formatting inconsistencies
- Magic numbers/strings
- Dead code
- Overly complex functions

**Best Practices:**
- DRY (Don't Repeat Yourself) violations
- SOLID principles adherence
- Error handling patterns
- Testing coverage
- Documentation quality

### 3. Categorize Findings
Group issues by:
- **Critical**: Security vulnerabilities, data loss risks
- **High**: Bugs that cause crashes/errors
- **Medium**: Performance issues, maintainability problems
- **Low**: Style issues, minor improvements

### 4. Provide Solutions
For each issue:
- Explain WHY it's a problem
- Show the problematic code snippet
- Provide a SPECIFIC fix with code examples
- Explain the benefits of the fix

### 5. Generate Report
Structure the output as:

```
# Code Review Report

## Summary
- Total files reviewed: X
- Issues found: Y (Z critical, W high, V medium, U low)

## Critical Issues
[List critical issues with fixes]

## High Priority Issues
[List high priority issues with fixes]

## Medium Priority Issues
[List medium priority issues with fixes]

## Low Priority Issues
[List low priority issues with fixes]

## Strengths
[Mention good practices found in the code]

## Recommendations
[Overall suggestions for improvement]
```

## Resources

### When to Use References
- Read `references/security_checklist.md` when analyzing security
- Consult `references/performance_patterns.md` for performance optimization
- Check `references/language_guides/` for language-specific best practices

### Scripts (Future Enhancement)
- `scripts/run_linter.sh <file>` - Run automated linting
- `scripts/complexity_analysis.py <file>` - Calculate cyclomatic complexity
- `scripts/security_scan.py <dir>` - Run security vulnerability scanner

## Example Usage

**User:** "Review this authentication code"

**Process:**
1. Read authentication-related files with `view` tool
2. Check for common auth vulnerabilities (password storage, session management, etc.)
3. Analyze token handling and encryption
4. Check for privilege escalation risks
5. Provide detailed report with fixes

## Tips for Effective Reviews

1. **Be Specific**: Don't just say "improve error handling" - show exactly how
2. **Prioritize**: Focus on critical/high issues first
3. **Be Constructive**: Acknowledge good code practices too
4. **Provide Context**: Explain the "why" behind each suggestion
5. **Code Examples**: Always show concrete before/after code
6. **Consider Trade-offs**: Mention any downsides to suggested changes
