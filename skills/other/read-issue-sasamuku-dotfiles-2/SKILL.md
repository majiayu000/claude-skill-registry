---
name: read-issue
description: Fetch and read a GitHub issue using gh command
disable-model-invocation: true
---

# Read Issue

Fetch and display a GitHub issue with sub-issues.

## Arguments

Issue number (e.g., `123` or `#123`)

$ARGUMENTS

## Steps

1. Extract the issue number from arguments
2. Fetch issue details:
   ```bash
   gh issue view <issue-number> --json number,title,body,state,url,comments
   ```
3. Parse the issue body to find ALL sub-issues:
   - Task list patterns: `- [ ] #123`, `- [x] #456`
   - Direct issue references: `#123`
   - Markdown links: `[text](#123)`
4. For EACH sub-issue found, fetch its details:
   ```bash
   gh issue view <sub-issue-number> --json number,title,body,state,url
   ```
5. Search the codebase for relevant files
6. Present the issue information:
   - Parent issue summary
   - Sub-issues list with status (open/closed)
   - Relevant code context
