---
name: review-branch
description: A skill for reviewing git branches. It helps analyze changes, commit history, and provide feedback to ensure code quality and adherence to project conventions before merging.
metadata:
  version: "1.0"
---

# Review Branch

## When to use this skill

Use this skill when a user wants to review a git branch, analyze the differences between branches (e.g., comparing a feature branch to `main`), or perform a pre-merge inspection. This is useful for identifying potential bugs, ensuring consistent coding style, and verifying commit message standards.

## Instructions

### 1. Identify the Scope of Review

- Determine if the review is for a local branch or a Pull Request (PR).
- For PRs, you can fetch the PR head to a local branch using:
  `git fetch origin pull/<pr-number>/head:pr-<pr-number>`
  Then, check out the new branch: `git checkout pr-<pr-number>`
- Determine the source branch (the branch being reviewed) and the target branch (the branch it will be merged into, e.g., `main` or `develop`).
- If not specified, default to comparing the current branch against `HEAD`'s tracking branch or a common base like `main`.

### 2. Gather Context

- Run `git status` to check for any uncommitted changes that might affect the review.
- Run `git log <target-branch>..<source-branch>` to review the commit history, messages, and authorship.
- Run `git diff <target-branch>...<source-branch>` (triple-dot diff) to see the changes introduced in the source branch since it diverged from the target.

### 3. Analyze Commits

- **Commit Messages**: Check if they follow the project's format (e.g., Conventional Commits).
- **Commit Granularity**: Ensure commits are logical and atomic.

### 4. Analyze Code Changes

- **Conventions**: Verify adherence to project naming, formatting, and architectural patterns.
- **Safety & Security**: Look for hardcoded secrets, unsafe operations, or lack of error handling.
- **Test Coverage**: Check if new features or bug fixes include corresponding tests.
- **Complexity**: Identify overly complex functions or large files that may need refactoring.

### 5. Provide Feedback

- Generate a structured review report highlighting:
  - **Summary**: High-level overview of the changes.
  - **Strengths**: What was done well.
  - **Issues/Suggestions**: Clear, actionable items for improvement, categorized by severity (e.g., Critical, Minor, Suggestion).
  - **Verification Status**: Mention if tests pass or if new tests are missing.

### 6. Finalize

- Ask the user if they would like you to automatically fix any of the identified minor issues (e.g., formatting) or if they need more details on specific changes.
