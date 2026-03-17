---
name: code-reviewer
description: Code review: security, performance, best practices
allowed-tools: Read, Grep, Glob, Bash
---

# Code Reviewer Skill

Provides automated code review capabilities with focus on security, performance, and coding standards.

## When to Use
- Before committing changes
- During pull request reviews
- When refactoring existing code
- For security vulnerability checks

## Review Areas
1. **Security**: SQL injection, XSS, authentication issues
2. **Performance**: N+1 queries, inefficient loops, memory leaks
3. **Code Quality**: DRY principle, SOLID principles, naming conventions
4. **Testing**: Test coverage, test quality, edge cases
5. **Documentation**: Comments, docstrings, README updates

## Usage Examples
1. "Review this code for security issues"
2. "Check performance bottlenecks in this function"
3. "Verify test coverage for this component"
4. "Review pull request #123"

## Guidelines
- Provide specific, actionable feedback
- Include code examples for improvements
- Flag critical security issues
- Suggest performance optimizations

**Automatic Triggers**:
- After code file modifications
- When git diff shows changes
- When PRs are created or updated
- When code review is requested