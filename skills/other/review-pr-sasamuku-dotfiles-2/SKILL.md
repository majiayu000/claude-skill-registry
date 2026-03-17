---
name: review-pr
description: Comprehensive PR review with code analysis and feedback
disable-model-invocation: true
---

# Review PR

Perform a thorough code review of a GitHub Pull Request.

## Arguments

PR number or PR URL (e.g., `123` or `https://github.com/owner/repo/pull/123`)

$ARGUMENTS

## Steps

1. Extract PR number from argument

2. Fetch PR information:
   ```bash
   gh pr view <number>
   ```

3. Get the diff:
   ```bash
   gh pr diff <number>
   ```

4. Fetch existing review comments:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments
   gh api repos/{owner}/{repo}/pulls/{number}/reviews
   ```

5. Use **code-reviewer** agent to perform the review with:
   - PR title and description
   - All changed files (diff)
   - Existing review comments for context

## Output

The code-reviewer agent provides structured feedback organized by priority:
- **Critical**: Security issues, bugs
- **Warning**: Code quality concerns
- **Suggestion**: Improvements

With specific file locations and fix recommendations.
