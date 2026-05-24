---
name: github-pr
description: GitHub PR utilities for code review workflows
version: 0.1.0-beta
license: MIT
compatibility: opencode
---

## Overview

CLI tools for GitHub pull request operations. Designed to support automated code review workflows. Requires the GitHub CLI (`gh`) to be installed and authenticated.

## Prerequisites

- [bun](https://bun.sh) runtime installed
- [GitHub CLI](https://cli.github.com/) installed and authenticated
  ```bash
  brew install gh
  gh auth login
  ```

## Commands

### Check Review Needed

Determines if a PR should be reviewed by checking various conditions.

```bash
bun .opencode/skill/github-pr/check-review-needed.js [pr-number]
```

**Arguments:**
- `pr-number` - PR number (optional, defaults to current branch's PR)

**Output:**
JSON object with:
- `shouldReview` - boolean indicating if review should proceed
- `reason` - explanation for the decision
- `prNumber` - the PR number checked

**Conditions checked:**
- PR is not closed or merged
- PR is not a draft
- PR is not from a known bot (dependabot, renovate, etc.)
- PR title doesn't indicate automation (bump, chore(deps), etc.)
- PR has not already been reviewed by Claude/AI
- PR is not trivial (2 or fewer lines changed)

**Examples:**
```bash
# Check current branch's PR
bun .opencode/skill/github-pr/check-review-needed.js

# Check specific PR
bun .opencode/skill/github-pr/check-review-needed.js 123
```

---

### List Guideline Files

Finds AGENTS.md (or CLAUDE.md) files relevant to a PR's changes.

```bash
bun .opencode/skill/github-pr/list-guideline-files.js [pr-number] [--json]
```

**Arguments:**
- `pr-number` - PR number (optional, defaults to current branch's PR)

**Options:**
- `--json` - Output as JSON array with file contents

**Search locations:**
- Repository root
- All directories containing files modified in the PR
- Parent directories of modified files

**Priority:** If both AGENTS.md and CLAUDE.md exist in the same directory, AGENTS.md takes precedence.

**Examples:**
```bash
# List guideline files for current PR
bun .opencode/skill/github-pr/list-guideline-files.js

# Get full content as JSON
bun .opencode/skill/github-pr/list-guideline-files.js 123 --json
```

**JSON Output Format:**
```json
[
  {
    "path": "AGENTS.md",
    "content": "# Project Guidelines\n..."
  },
  {
    "path": "src/components/AGENTS.md",
    "content": "# Component Guidelines\n..."
  }
]
```

---

### Post Inline Comment

Posts a review comment on a specific line or line range in a PR.

```bash
bun .opencode/skill/github-pr/post-inline-comment.js <pr-number> --path <file> --line <n> --body <text>
```

**Arguments:**
- `pr-number` - PR number (optional if on a PR branch)

**Options:**
- `--path <file>` - File path to comment on (required)
- `--line <n>` - Line number to comment on (required)
- `--start-line <n>` - Start line for multi-line comments (optional)
- `--body <text>` - Comment body in markdown (required)

**Suggestion blocks:**
Include a suggestion block for small fixes that can be committed directly:

````markdown
Fix the error handling:

```suggestion
try {
  await authenticate();
} catch (e) {
  handleAuthError(e);
}
```
````

**Important:** Suggestions must be complete. The author should be able to click "Commit suggestion" without needing additional changes elsewhere.

**Examples:**
```bash
# Single line comment
bun .opencode/skill/github-pr/post-inline-comment.js 123 \
  --path src/auth.ts \
  --line 67 \
  --body "Missing error handling for OAuth callback"

# Multi-line comment (lines 65-70)
bun .opencode/skill/github-pr/post-inline-comment.js 123 \
  --path src/auth.ts \
  --line 70 \
  --start-line 65 \
  --body "This authentication block needs refactoring"
```

---

## Integration with gh CLI

These tools wrap the GitHub CLI (`gh`). For operations not covered by these utilities, use `gh` directly:

```bash
# View PR details
gh pr view 123 --json title,body,state,isDraft,files

# Get PR diff
gh pr diff 123

# View PR comments
gh pr view 123 --comments

# Post a regular comment
gh pr comment 123 --body "Comment text"

# View file at PR head
gh api repos/{owner}/{repo}/contents/{path}?ref={branch}
```

## Output Behavior

- Command output is displayed directly to the user in the terminal
- JSON output is formatted for readability and piping
- Use `--json` flag when you need to process output programmatically
