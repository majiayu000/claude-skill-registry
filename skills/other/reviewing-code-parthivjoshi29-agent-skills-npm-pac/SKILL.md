---
name: reviewing-code
description: Analyzes code for bugs, security vulnerabilities, performance issues, and style violations. Use when the user asks for a code review, feedback on specific files, optimization suggestions, or a security audit.
---

# Code Reviewer

## When to use this skill

- User asks to "review", "audit", or "check" code.
- User provides a diff or specific file and asks for improvements.
- User asks "is this secure?" or "can this be optimized?".
- User requests a second opinion on an implementation.

## Workflow

[ ] **Contextualize**: Identify the programming language, framework, and the user's specific goals (e.g., "make it faster" vs. "fix this bug").
[ ] **Security Scan**: Check for common vulnerabilities (SQLi, XSS, secrets in code, unsafe inputs).
[ ] **Logic & Correctness**: Verify that the code yields the expected output and handles edge cases.
[ ] **Performance & Efficiency**: Identify O(n^2) loops, unnecessary re-renders, or memory leaks.
[ ] **Readability & Style**: Check naming conventions, modularity (DRY), and adherence to language idioms.
[ ] **Summary**: Present findings prioritized by severity (Critical -> Major -> Minor).

## Instructions

### 1. The Review Mindset

- **Constructive & Specific**: Don't just say "this is bad." Explain _why_ and provide a code snippet showing the _better_ way.
- **Prioritize**:
  1. **Security** (Credentials, Injection, Auth)
  2. **Crash/Bug Risks** (Null pointers, race conditions)
  3. **Performance** (Resource usage, latency)
  4. **Maintainability** (Clean code, comments)

### 2. Analysis Checklist (Language Agnostic)

- **Input Validation**: Are all external inputs validated/sanitized?
- **Error Handling**: Are try/catch blocks used appropriately? Are errors logged?
- **Hardcoded Values**: Are API keys, URLs, or magic numbers hardcoded?
- **Complexity**: Is a function doing too much? (Cyclomatic complexity).
- **Testability**: Is this code easy to unit test?

### 3. Output Format

When delivering the review, use this structure:

#### 🔍 Summary

_Brief overview of the code quality._

#### 🔴 Critical Issues

_Immediate fixes required._

- **Issue**: [Description]
- **Fix**: [Code Snippet]

#### 🟡 Improvements

_Optimization and cleanup suggestions._

- **Suggestion**: [Description]

#### 🟢 Good Practices

_What the user did well (reinforce good habits)._

## Resources

- [OWASP Top 10 Reference](https://owasp.org/www-project-top-ten/)
