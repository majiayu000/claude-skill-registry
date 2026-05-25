---
name: github-fix-issue
description: Fix GitHub issues end-to-end — from analysis through branch creation, implementation, testing, and PR submission. Use this skill whenever the user mentions fixing a GitHub issue, resolving a bug from an issue tracker, working on a GitHub issue number, or says things like "fix issue #123", "work on this issue", "resolve the bug in issue", or references a GitHub issue URL. Also trigger when the user wants to investigate and implement a fix for a reported problem on GitHub.
---

# Fix GitHub Issue

A structured workflow for analyzing, fixing, and submitting a PR for a GitHub issue. This skill uses the GitHub CLI (`gh`) for all GitHub interactions.

## Workflow

### 1. Understand the Issue

- Run `gh issue view <number>` to get full issue details (title, body, labels, comments)
- Read through the problem description carefully
- If the issue is unclear or missing key details, ask the user clarifying questions before proceeding

### 2. Research Prior Art

Before jumping into code, gather context — understanding what's been tried or discussed prevents duplicate work and surfaces useful patterns:

- Search the codebase for files and functions related to the issue
- Check if related PRs exist with `gh pr list --search "<keywords>"`
- Look for scratchpads or notes from previous investigation
- Read relevant source files to understand the current behavior

### 3. Plan the Fix

Think through how to break the issue into small, manageable tasks. Document your plan in a scratchpad file:

- Name the file descriptively (include the issue reference)
- Include a link back to the issue
- List the specific changes needed and their order
- Note any risks or edge cases

### 4. Implement

- Create a new branch for the issue (e.g., `fix/issue-123-description`)
- Work through the plan in small steps
- Commit after each meaningful change — small commits are easier to review and revert

### 5. Test

Thorough testing prevents the fix from introducing new problems:

- Write unit tests that describe the expected behavior
- Run the full test suite to catch regressions
- If UI changes were made and browser automation (e.g., Puppeteer MCP) is available, use it to verify visually
- Fix any failing tests before moving on

### 6. Open Pull Request

- Push the branch and open a PR with `gh pr create`
- Reference the issue in the PR description (e.g., "Fixes #123")
- Request a review

## gh Command Reference

```sh
# View issue details
gh issue view 123

# Create a branch
git checkout -b fix/issue-123-description

# Open a PR that closes the issue
gh pr create --title "Fix: description" --body "Fixes #123"

# Request review
gh pr edit 456 --add-reviewer username
```
