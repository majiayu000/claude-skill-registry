---
name: linear-create
description: Create new Linear issues for bugs, features, improvements, or tasks. Use when asked to file a ticket, log work, track a task, or create an issue.
user-invocable: true
argument-hint: "<title> [--bug|--feature|--improvement] [--priority urgent|high|normal|low]"
allowed-tools:
  - mcp__linear-server__save_issue
  - mcp__linear-server__save_comment
  - mcp__linear-server__list_issue_labels
  - mcp__linear-server__list_issue_statuses
  - mcp__linear-server__list_projects
  - mcp__linear-server__list_issues
  - mcp__linear-server__create_issue_label
---

# Linear Issue Creator

You create well-structured Linear issues in the Lsdippo team workspace.

## Workspace Context

- **Team:** Lsdippo
- **Labels:** Bug, Feature, Improvement, ADR, Planning, Done
- **Priorities:** 1=Urgent, 2=High, 3=Normal, 4=Low

## Issue Creation Flow

1. **Parse the user's request** to extract: title, type, priority, description details
2. **Determine the label** from flags or context:
   - `--bug` or mentions of broken/fix/error → Bug label
   - `--feature` or mentions of new/add/build → Feature label
   - `--improvement` or mentions of refactor/optimize/update → Improvement label
3. **Determine priority** from flags or context (default: Normal/3)
4. **Create the issue** with a well-written description

## Description Template

Write descriptions in this format:

```markdown
## Summary
[One-line summary of what needs to happen]

## Context
[Why this is needed, what triggered it]

## Acceptance Criteria
- [ ] [Specific, testable criterion]
- [ ] [Another criterion]

## Branch
`<type>/LSD-XX-<slug>`

## Notes
[Any additional context, links, related issues]
```

**Branch type mapping:**
- Bug → `fix/`, Feature → `feat/`, Improvement → `improve/`

Populate the `## Branch` section with the expected branch name after the issue is created and you have the identifier. This gives anyone picking up the ticket the exact branch to create.

## Bulk Creation

If the user provides multiple items (e.g., "create tickets for X, Y, and Z"):
- Create each as a separate issue
- Link related issues using `relatedTo`
- Present a summary table of all created issues

## After Creation

Always report back:
- Issue identifier (e.g., LSD-123)
- Title
- Link/status confirmation
- Suggest: "Want me to add more detail, set a due date, or assign it?"
