---
name: gh-issue
description: Create a GitHub issue following project guidelines
argument-hint: <title or description>
allowed-tools: Read, Grep, Glob, mcp__github__create_issue, mcp__github__list_issues, mcp__github__search_issues
---

# Create GitHub Issue

Create a new GitHub issue for the gittower/git-flow-next repository.

## Instructions

1. **Read ISSUE_GUIDELINES.md** for all formatting rules and conventions

2. **Gather Information**
   - If `$ARGUMENTS` is provided, use it as the issue title/description
   - If no arguments, ask the user for a brief description

3. **Check for Duplicates**
   - Search existing issues for similar topics
   - If potential duplicates found, show them and ask to confirm creation

4. **Create the Issue**
   - Determine type and apply `bug` or `enhancement` label per ISSUE_GUIDELINES.md
   - Write title and body following ISSUE_GUIDELINES.md conventions
   - Use `mcp__github__create_issue` to create on gittower/git-flow-next

5. **Report Result**
   - Show the created issue URL
   - Suggest next step: `/analyze-issue <number>` to start working on it
