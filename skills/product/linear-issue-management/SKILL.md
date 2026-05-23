---
id: linear-issue-management
name: Linear Issue Management
description: List/search issues, triage, assign
role: engineering
requiredTools:
  - type: mcpService
    serviceType: linear
---

## Linear Issue Management

When managing issues in Linear:

- List issues with filters (team, project, assignee, state) to find relevant work.
- Use get issue for full details before summarizing or updating.
- When triaging, report issue state, assignee, and labels; suggest assignee or state changes when appropriate.
- Search issues by query when the user asks for something specific (e.g. bug, feature name).
- Prefer listing by team or project when the user context is clear.

## Step-by-step instructions

1. For “find issues”: list issues with filters (team, project, assignee, state) or use search/query for text (e.g. bug, feature name).
2. For a single issue: get issue by ID or identifier; then summarize title, state, assignee, labels, and description excerpt.
3. For triage: list relevant issues; report state, assignee, labels; suggest state or assignee changes only when the user asks.
4. For updates: use the Linear tool to update issue state or assignee after the user confirms.

## Examples of inputs and outputs

- **Input**: “What’s in the backlog for Team Platform?”  
  **Output**: Short list of issues (title, state, assignee) from list issues filtered by team and state=backlog; optionally count.

- **Input**: “Details for issue ENG-123.”  
  **Output**: Title, state, assignee, labels, description summary (and link if available) from get issue.

## Common edge cases

- **No team/project given**: Ask which team or project, or list teams/projects and let the user choose.
- **Issue not found**: Say “Issue [id] not found” and suggest checking the identifier or permissions.
- **Ambiguous “backlog”**: Use the team’s or project’s backlog state (e.g. “Backlog” state) and say which state you used.
- **API/oauth error**: Report that Linear returned an error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **List issues**: Use for backlog, by assignee, by state, or by project/team; always apply relevant filters.
- **Get issue**: Use for full details of one issue by ID or identifier.
- **Search/query**: Use when the user asks for “bugs”, “feature X”, or text-based search.
- **Update issue**: Use to change state or assignee only after the user explicitly asks to update.
