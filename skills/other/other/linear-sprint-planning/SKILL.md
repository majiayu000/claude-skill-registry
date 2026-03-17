---
id: linear-sprint-planning
name: Linear Sprint Planning
description: Project views, team capacity
role: product
requiredTools:
  - type: mcpService
    serviceType: linear
---

## Linear Sprint Planning

When planning sprints or capacity in Linear:

- List teams and projects first to scope the view.
- List issues by team/project and state to see backlog and in-progress work.
- Summarize counts by state or assignee to show capacity or load.
- When asked for sprint scope, filter by project/team and report open or unassigned issues.
- Use issue details (estimate, cycle) when available to enrich summaries.

## Step-by-step instructions

1. If team/project is unclear: list teams and projects and ask or infer from context.
2. List issues filtered by team/project and state (e.g. Backlog, In Progress, Done).
3. Summarize counts by state and optionally by assignee for capacity.
4. For sprint scope: report open or unassigned issues; include estimate or cycle when the tool returns them.
5. Keep summaries short (counts, key issues); avoid dumping full issue lists unless asked.

## Examples of inputs and outputs

- **Input**: “What’s our sprint capacity for Team X?”  
  **Output**: Count of issues by state (and by assignee if useful); optionally total estimate; from list issues for that team.

- **Input**: “What can we pull into the next sprint?”  
  **Output**: List of open/backlog issues (title, state, assignee) for the relevant project/team; optionally with estimates.

## Common edge cases

- **Multiple teams/projects**: Ask which one, or summarize per team/project with clear labels.
- **No issues in state**: Report “No issues in [state]” for that team/project.
- **Estimates missing**: Summarize counts without estimates and note that estimates aren’t set.
- **API/oauth error**: Report Linear error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **List teams/projects**: Use when scope is unknown before listing issues.
- **List issues**: Use with team/project and state filters for backlog, in progress, and sprint scope; use assignee for capacity.
- **Get issue**: Use when you need estimate or cycle for specific issues in a summary.
