---
name: review-pr
description: |
  Use this skill when the user wants to review a pull request, check a PR for
  issues, or get feedback on a GitHub PR. Triggered by "review PR", "check PR",
  "review pull request", or "/review-pr <number>".
argument-hint: "[PR number or URL]"
allowed-tools: "Bash, Read, Grep, Glob"
context: fork
---

# Pull Request Review

Perform a thorough code review of the pull request.

## PR Details

!`gh pr list --limit 5`

## Instructions

1. Fetch the PR diff:
   ```bash
   gh pr diff $ARGUMENTS
   ```
   Or if no number given, use the current branch:
   ```bash
   git diff main...HEAD
   ```

2. Also fetch PR metadata:
   ```bash
   gh pr view $ARGUMENTS
   ```

3. Review the following areas:

### Code Quality
- Logic errors or edge cases
- Code duplication (DRY violations)
- Overly complex functions (> 50 lines)
- Unused imports, variables, dead code

### Security
- Hardcoded secrets or credentials
- SQL injection, XSS, command injection risks
- Improper authentication/authorization
- Insecure dependencies

### Performance
- N+1 query problems
- Unnecessary re-renders (React)
- Missing indexes for new queries
- Large synchronous operations

### Testing
- Are new features tested?
- Are edge cases covered?
- Are tests actually testing the right thing?

### Documentation
- Are public APIs documented?
- Is the PR description clear?
- Are breaking changes noted?

## Output Format

Provide a structured review:

```
## Summary
[1-2 sentence overview]

## ✅ What's Good
- [positive point]

## ⚠️  Issues

### Critical (must fix)
- [file:line] — [description]

### Important (should fix)
- [file:line] — [description]

### Minor (consider fixing)
- [file:line] — [description]

## 💡 Suggestions
- [optional improvements]

## Verdict: APPROVE / REQUEST CHANGES / COMMENT
```

$ARGUMENTS
