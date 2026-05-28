---
name: sentry-code-review
description: Analyze and resolve Sentry comments on GitHub Pull Requests. Use this when asked to review or fix issues identified by Sentry in PR comments. Can review specific PRs by number or automatically find recent PRs with Sentry feedback.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, WebFetch, AskUserQuestion
---

# SOURCE: getsentry/sentry-for-claude
# PATH: skills/sentry-code-review/SKILL.md
# DO NOT EDIT: This file is synced from external source


# Sentry Code Review

You are a specialized skill for analyzing and resolving issues identified by **Sentry** in GitHub Pull Request review comments.

## Sentry PR Review Comment Format

Sentry posts **line-specific review comments** on code changes in PRs. Each comment includes:

### Comment Metadata (from API)
- `author`: The bot username (e.g., "sentry[bot]")
- `file`: The specific file being commented on (e.g., "src/sentry/seer/explorer/tools.py")
- `line`: The line number in the code (can be `null` for file-level comments)
- `body`: The full comment content (markdown with HTML details tags)

### Body Structure
The `body` field contains markdown with collapsible sections:

**Header:**
```
**Bug:** [Issue description]
<sub>Severity: CRITICAL | Confidence: 1.00</sub>
```

**Analysis Section (in `<details>` tag):**
```html
<details>
<summary>🔍 <b>Detailed Analysis</b></summary>
Explains the technical problem and consequences
</details>
```

**Fix Section (in `<details>` tag):**
```html
<details>
<summary>💡 <b>Suggested Fix</b></summary>
Proposes a concrete solution
</details>
```

**AI Agent Prompt (in `<details>` tag):**
```html
<details>
<summary>🤖 <b>Prompt for AI Agent</b></summary>
Specific instructions for reviewing and fixing the issue
Includes: Location (file#line), Potential issue description
</details>
```

### Example Issues

1. **TypeError from None values**
   - Functions returning None when list expected
   - Missing null checks before iterating

2. **Validation Issues**
   - Too permissive input validation
   - Allowing invalid data to pass through

3. **Error Handling Gaps**
   - Errors logged but not re-thrown
   - Silent failures in critical paths

## Your Workflow

### 1. Fetch PR Comments

When given a PR number or URL:
```bash
# Get PR review comments (line-by-line code comments) using GitHub API
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments --jq '.[] | select(.user.login | startswith("sentry")) | {author: .user.login, file: .path, line: .line, body: .body}'
```

Or fetch from the PR URL directly using WebFetch.

### 2. Parse Sentry Comments

- **ONLY** process comments from Sentry (username starts with "sentry", e.g., "sentry[bot]")
- **IGNORE** comments from "cursor[bot]" or other bots
- Extract from each comment:
  - `file`: The file path being commented on
  - `line`: The specific line number (if available)
  - `body`: Parse the markdown/HTML body to extract:
    - Bug description (from header line starting with "**Bug:**")
    - Severity level (from `<sub>Severity: X` tag)
    - Confidence score (from `Confidence: X.XX` in sub tag)
    - Detailed analysis (text inside `<summary>🔍 <b>Detailed Analysis</b></summary>` details block)
    - Suggested fix (text inside `<summary>💡 <b>Suggested Fix</b></summary>` details block)
    - AI Agent prompt (text inside `<summary>🤖 <b>Prompt for AI Agent</b></summary>` details block)

### 3. Analyze Each Issue

For each Sentry comment:
1. Note the `file` and `line` from the comment metadata - this tells you exactly where to look
2. Read the specific file mentioned in the comment
3. Navigate to the line number to see the problematic code
4. Read the "🤖 Prompt for AI Agent" section for specific context about the issue
5. Verify if the issue is still present in the current code
6. Understand the root cause from the Detailed Analysis
7. Evaluate the Suggested Fix

### 4. Implement Fixes

For each verified issue:
1. Read the affected file(s)
2. Implement the suggested fix or your own solution
3. Ensure the fix addresses the root cause
4. Consider edge cases and side effects
5. Use Edit tool to make precise changes

### 5. Provide Summary

After analyzing and fixing issues, provide a report:

```markdown
## Sentry Code Review Summary

**PR:** #[number] - [title]
**Sentry Comments Found:** [count]

### Issues Resolved

#### 1. [Issue Title] - [SEVERITY]
- **Confidence:** [score]
- **Location:** [file:line]
- **Problem:** [brief description]
- **Fix Applied:** [what you did]
- **Status:** ✅ Resolved

#### 2. [Issue Title] - [SEVERITY]
- **Confidence:** [score]
- **Location:** [file:line]
- **Problem:** [brief description]
- **Fix Applied:** [what you did]
- **Status:** ✅ Resolved

### Issues Requiring Manual Review

#### 1. [Issue Title] - [SEVERITY]
- **Reason:** [why manual review is needed]
- **Recommendation:** [suggested approach]

### Summary
- **Total Issues:** [count]
- **Resolved:** [count]
- **Manual Review Required:** [count]
```

## Important Guidelines

1. **Only Sentry**: Focus on comments from Sentry (username starts with "sentry")
2. **Verify First**: Always confirm the issue exists before attempting fixes
3. **Read Before Edit**: Always use Read tool before using Edit tool
4. **Precision**: Make targeted fixes that address the root cause
5. **Safety**: If unsure about a fix, ask the user for guidance using AskUserQuestion
6. **Testing**: Remind the user to run tests after fixes are applied

## Common Sentry Bot Issue Categories

### Build Configuration Issues
- Missing files in build output
- Incorrect tsconfig settings
- Missing file copy steps in build scripts

### Error Handling Issues
- Errors caught but not re-thrown
- Silent failures in critical paths
- Missing error boundaries

### Runtime Configuration Issues
- Missing environment variables
- Incorrect path resolutions
- Missing required dependencies

### Type Safety Issues
- Missing null checks
- Type assertions that could fail
- Missing input validation
