---
name: community-code-reviewer
description: Perform thorough, constructive code reviews on pull requests and code changes. Use when the user asks to review code, review a PR, check code quality, or provide code feedback.
---

# Code Review Skill

Perform thorough, constructive code reviews on pull requests and code changes.

## Instructions

When reviewing code:

### 1. First Pass - Understanding
- Read the PR description and linked issues
- Understand the intent and context
- Identify the scope of changes

### 2. Check for Issues

**Correctness**
- Logic errors or bugs
- Edge cases not handled
- Race conditions or concurrency issues
- Null/undefined handling

**Security**
- Input validation
- SQL injection, XSS vulnerabilities
- Hardcoded secrets or credentials
- Proper authentication/authorization

**Performance**
- Unnecessary loops or computations
- N+1 queries
- Memory leaks
- Missing caching opportunities

**Maintainability**
- Code clarity and readability
- Proper naming conventions
- DRY principle violations
- Missing or unclear comments

**Testing**
- Test coverage for new code
- Edge cases tested
- Integration tests where needed

### 3. Provide Feedback

Use this format for each comment:

```
**[Category]** File:Line

Description of the issue or suggestion.

Suggested fix (if applicable):
\`\`\`
code example
\`\`\`
```

### 4. Summary

End with a summary:
- Overall assessment (Approve/Request Changes/Comment)
- Key strengths of the PR
- Critical issues that must be addressed
- Nice-to-have improvements

## Tone Guidelines

- Be constructive, not critical
- Explain the "why" behind suggestions
- Acknowledge good practices
- Ask questions rather than make demands
- Offer to help if complex changes needed
