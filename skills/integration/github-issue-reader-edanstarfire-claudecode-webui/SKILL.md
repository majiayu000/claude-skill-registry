---
name: github-issue-reader
description: Fetch and analyze GitHub issue details including comments, metadata, and discussion context. Use when user mentions issue numbers, URLs, or you need to understand implementation requirements from a GitHub issue.
---

# GitHub Issue Reader

## Instructions

### When to Invoke This Skill
- User mentions a GitHub issue number (e.g., "issue #42", "#123")
- User provides a GitHub issue URL
- You need context about what needs to be implemented or fixed
- Validating whether an issue has sufficient detail
- Understanding discussion/decisions in issue comments

### Standard Workflow

1. **Fetch Issue Details**
   ```bash
   gh issue view <issue_number> --json title,body,state,labels,assignees,createdAt,updatedAt
   ```

2. **Fetch All Comments**
   ```bash
   gh issue view <issue_number> --comments
   ```

3. **Analyze Content**
   - Parse issue description for requirements
   - Review comments for implementation decisions
   - Identify any existing plans or approaches
   - Note any blockers or dependencies mentioned

4. **Synthesize Context**
   - Summarize what needs to be done
   - Highlight key decisions from discussion
   - Flag any ambiguities or missing information
   - Note relevant links or references

### Error Handling

**If `gh` commands fail:**
- Check authentication: `gh auth status`
- If not authenticated, guide user through: `gh auth login`
- Verify issue number exists in the repository

**If issue is closed:**
- Note the closed state
- Check if there's a linked PR that resolved it
- Determine if reopening is needed

### Output Format

Provide structured summary:
```
Issue #<number>: <title>
Status: <open/closed>
Labels: <label list>

Summary:
<Brief description of what needs to be done>

Key Points from Discussion:
- <Important decision/context from comments>
- <Another key point>

Implementation Approach (if discussed):
<Any implementation details from comments>

Ambiguities/Questions:
- <Anything unclear that needs clarification>
```

## Examples

### Example 1: User mentions issue number
```
User: "Can you look at issue #42?"
Action: Run gh issue view 42 and gh issue view 42 --comments
Output: Structured summary of the issue
```

### Example 2: Issue URL provided
```
User: "Check out https://github.com/owner/repo/issues/123"
Action: Extract issue number (123), fetch details
Output: Analysis of what the issue requires
```

### Example 3: Vague reference
```
User: "What was that bug about the login form?"
Action: May need to search issues first (gh issue list --search "login form")
Output: Identify relevant issue(s) and provide context
```
