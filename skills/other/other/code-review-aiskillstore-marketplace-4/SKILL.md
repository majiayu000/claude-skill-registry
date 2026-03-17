---
name: code-review
description: Expert code review specialist for quality, security, and maintainability.
  Use when reviewing code changes, ensuring high development standards, or conducting
  security audits. Provides actionable feedback organized by priority.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Code Review

This skill provides expert code review capabilities focusing on code quality, security vulnerabilities, and maintainability. It analyzes code changes and provides prioritized, actionable feedback.

## When to Use This Skill

- After writing or modifying code to ensure quality standards
- Before merging pull requests or deploying changes
- When conducting security audits or vulnerability assessments
- When establishing code quality standards for a project
- When reviewing code for performance optimizations
- When ensuring code follows project conventions and best practices

## What This Skill Does

1. **Analyzes Code Changes**: Reviews git diffs and modified files to understand what changed
2. **Security Auditing**: Identifies exposed secrets, API keys, and security vulnerabilities
3. **Quality Assessment**: Evaluates code readability, maintainability, and best practices
4. **Performance Review**: Identifies potential performance issues and optimization opportunities
5. **Standards Compliance**: Ensures code follows project conventions and style guidelines
6. **Prioritized Feedback**: Organizes findings by severity (Critical, Warnings, Suggestions)

## How to Use

### Basic Code Review

```
Review the recent code changes in this branch
```

```
Check this file for security issues and code quality
```

### Review Specific Files

```
Review src/auth.js for security vulnerabilities
```

```
Review the changes in this pull request
```

## Review Process

### 1. Analyze Changes

When invoked:

1. **Get Recent Changes**: Run `git diff` to see what changed

   ```bash
   git diff $(git merge-base HEAD main)..HEAD
   ```

2. **Focus on Modified Files**: Prioritize files with actual changes
3. **Review Context**: Understand the purpose of changes from commit messages or conversation

### 2. Review Checklist

For each file, check:

**Code Quality:**

- Code is simple and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- Good test coverage
- Performance considerations addressed

**Security:**

- No exposed secrets or API keys
- Input validation implemented
- Proper authentication/authorization
- Safe handling of user input
- No SQL injection or XSS vulnerabilities

**Maintainability:**

- Consistent code style
- Appropriate comments (not excessive)
- Clear function/method structure
- Proper separation of concerns
- No unnecessary complexity

**Best Practices:**

- Follows framework/library conventions
- Proper use of design patterns
- Efficient algorithms and data structures
- Appropriate use of async/await or promises
- Proper resource cleanup

### 3. Organize Feedback

Provide feedback in three priority levels:

**Critical Issues (Must Fix):**

- Security vulnerabilities
- Bugs that will cause failures
- Code that breaks existing functionality
- Performance issues that will impact users

**Warnings (Should Fix):**

- Code quality issues that affect maintainability
- Potential bugs or edge cases
- Performance optimizations
- Missing error handling
- Incomplete test coverage

**Suggestions (Consider Improving):**

- Code style improvements
- Refactoring opportunities
- Documentation enhancements
- Best practice recommendations
- Minor optimizations

### 4. Provide Specific Examples

For each issue found:

- **Location**: File path and line number
- **Issue**: Clear description of the problem
- **Impact**: Why this matters
- **Fix**: Specific code example showing how to fix it
- **Rationale**: Explanation of why the fix is better

## Examples

### Example 1: Security Issue Found

**Input**: Review `src/api/auth.js`

**Output**:

```markdown
## Code Review: src/api/auth.js

### Critical Issues

**1. Exposed API Key**
- **Location**: `src/api/auth.js:23`
- **Issue**: Hardcoded API key in source code
- **Code**:
  ```javascript
  const API_KEY = "sk_live_1234567890abcdef"; // ❌ Exposed secret
  ```

- **Fix**: Use environment variables

  ```javascript
  const API_KEY = process.env.API_KEY; // ✅ Secure
  ```

- **Impact**: This exposes your API key in version control, allowing unauthorized access

### Warnings

**2. Missing Input Validation**

- **Location**: `src/api/auth.js:45`
- **Issue**: No validation on user input before processing
- **Recommendation**: Add input validation before authentication

### Example 2: Code Quality Review

**Input**: Review recent changes

**Output**:

```markdown
## Code Review Summary

**Files Reviewed**: 5
**Critical Issues**: 0
**Warnings**: 3
**Suggestions**: 5

### Warnings

**1. Duplicated Code**
- **Files**: `src/utils/format.js:12-25` and `src/utils/display.js:8-21`
- **Issue**: Same formatting logic duplicated
- **Fix**: Extract to shared utility function

**2. Missing Error Handling**
- **Location**: `src/api/users.js:34`
- **Issue**: No try/catch for async operation
- **Fix**: Add proper error handling

### Suggestions

**1. Improve Variable Naming**
- **Location**: `src/components/List.jsx:15`
- **Current**: `const d = data.map(...)`
- **Suggested**: `const formattedItems = data.map(...)`
```

## Reference Files

For comprehensive review checklists, load reference files as needed:

- **`references/review_checklist.md`** - Detailed checklists for security, code quality, performance, testing, documentation, and best practices
- **`references/CODE_ANALYSIS.template.md`** - Code analysis report template with security, performance, and maintainability sections

When conducting thorough reviews, load `references/review_checklist.md` and use the appropriate checklist sections.

## Best Practices

### Review Focus Areas

1. **Security First**: Always check for security vulnerabilities first
2. **Context Matters**: Understand the purpose of changes before reviewing
3. **Be Constructive**: Provide actionable feedback, not just criticism
4. **Prioritize**: Focus on critical issues that must be fixed
5. **Explain Why**: Help developers understand the reasoning behind suggestions

### Review Guidelines

- **Be Specific**: Point to exact lines and provide code examples
- **Be Balanced**: Acknowledge good code as well as issues
- **Be Practical**: Consider the context and urgency of changes
- **Be Educational**: Help developers learn and improve
- **Be Consistent**: Apply the same standards across all reviews

### Common Patterns to Check

**Security:**

- Hardcoded secrets or credentials
- SQL injection vulnerabilities
- XSS vulnerabilities
- Missing authentication/authorization
- Insecure random number generation

**Code Quality:**

- Code duplication
- Magic numbers without constants
- Deeply nested conditionals
- Functions that do too much
- Poor error messages

**Performance:**

- N+1 query problems
- Missing indexes
- Inefficient algorithms
- Unnecessary re-renders (React)
- Memory leaks

## Related Use Cases

- Pre-commit code reviews
- Pull request reviews
- Security audits
- Code quality assessments
- Onboarding new team members
- Establishing coding standards
