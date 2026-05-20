---
name: review-pr
description: Comprehensive PR review with specialized agents. Triggers on "review PR", "code review", "review changes", "check my code".
---

# PR Review

A multi-agent PR review workflow that checks code quality, simplicity, types, tests, and potential silent failures.

## When to Use

- Before merging a PR
- After completing a feature implementation
- When asked to review code changes
- Self-review before pushing

## When NOT to Use

- Reviewing a single line change
- Draft/WIP PRs (unless asked)

## Core Principles

- Review the diff, not the entire file (unless context is needed)
- Prioritize: critical bugs > logic errors > style > nitpicks
- Suggest specific fixes, not vague complaints
- Acknowledge what's done well

## Review Agents

### 1. Code Reviewer

**Focus**: Logic, correctness, React patterns

- Check for bugs, race conditions, edge cases
- Verify proper error handling
- Ensure correct React hooks usage
- Check for memory leaks (missing cleanup)

### 2. Code Simplifier

**Focus**: Readability, DRY, unnecessary complexity

- Identify overly complex code that could be simplified
- Find duplicated logic that should be extracted
- Suggest cleaner alternatives
- Flag over-engineering

### 3. Type Design Analyzer

**Focus**: TypeScript quality

- Check for `any` types
- Verify interface completeness
- Ensure proper generic usage
- Check for type narrowing opportunities

### 4. Silent Failure Hunter

**Focus**: Error paths that fail silently

- Find unhandled promise rejections
- Check for missing error boundaries
- Identify try/catch blocks that swallow errors
- Find missing loading/error states

### 5. Comment Analyzer

**Focus**: Code documentation quality

- Check for misleading or outdated comments
- Identify complex code that needs comments
- Flag redundant comments that just restate the code
- Verify JSDoc on exported functions

### 6. PR Test Analyzer

**Focus**: Test coverage and quality

- Check if new features have corresponding tests
- Verify edge cases are covered
- Identify untested error paths
- Suggest missing test scenarios

## Output Format

```markdown
# PR Review: [PR title or description]

## Summary
[1-2 sentence overall assessment]
**Verdict**: Approve / Request Changes / Needs Discussion

## Critical Issues
- [ ] [issue]: [file:line] — [description and fix]

## Suggestions
- [ ] [suggestion]: [file:line] — [why and how]

## Positive Notes
- [what's done well]

## Test Coverage
- [assessment of test coverage for changes]
```

## Related Skills

| Skill | When to Chain |
|-------|--------------|
| feature-dev | Review after feature implementation |
| git-commit | After review passes, commit and push |
