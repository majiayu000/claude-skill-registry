---
name: linear-pm
description: Linear project management - issues, projects, cycles, and roadmaps. Use for Linear-related tasks like managing issues, tracking sprints, and organizing projects.
version: 1.1.0
category: 'Other'
agents: [planner, developer]
tags: [linear, project-management, issues, agile, roadmap]
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Bash, WebFetch]
best_practices:
  - Verify LINEAR_API_KEY is set
  - Use filters to reduce API calls
  - Cache team and project metadata
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

**Mode: Cognitive/Prompt-Driven** - No standalone utility script; use via agent context.

# Linear PM Skill

## Overview

This skill provides comprehensive Linear project management capabilities with progressive disclosure for optimal context usage.

Context Savings: ~92% reduction

- Direct API Mode: ~15,000 tokens for full API documentation
- Skill Mode: ~300 tokens metadata + on-demand loading

## Requirements

- LINEAR_API_KEY environment variable set
- Internet connectivity for Linear API access

## Toolsets

| Toolset  | Description                                      |
| -------- | ------------------------------------------------ |
| issues   | Issue creation, updates, comments, state changes |
| projects | Project management and issue association         |
| cycles   | Sprint/cycle management and planning             |
| teams    | Team structure and member management             |
| labels   | Label and workflow state management              |

## Tools by Category

### Issue Operations (Confirmation Required for Mutations)

| Tool          | Description                                       | Confirmation |
| ------------- | ------------------------------------------------- | ------------ |
| list-issues   | List issues with filters (state, assignee, label) | No           |
| get-issue     | Get detailed issue information                    | No           |
| create-issue  | Create new issue with title, description, team    | Yes          |
| update-issue  | Update issue fields (state, assignee, priority)   | Yes          |
| add-comment   | Add comment to an issue                           | Yes          |
| search-issues | Search issues by text query                       | No           |
| assign-issue  | Assign issue to team member                       | Yes          |
| set-priority  | Set issue priority (urgent, high, medium, low)    | Yes          |
| add-label     | Add label to issue                                | Yes          |

### Project Operations

| Tool           | Description                      | Confirmation |
| -------------- | -------------------------------- | ------------ |
| list-projects  | List all projects for a team     | No           |
| get-project    | Get project details and metadata | No           |
| project-issues | Get all issues in a project      | No           |
| create-project | Create new project               | Yes          |
| update-project | Update project details           | Yes          |

### Cycle Operations (Sprints)

| Tool           | Description                    | Confirmation |
| -------------- | ------------------------------ | ------------ |
| list-cycles    | List cycles for a team         | No           |
| current-cycle  | Get current active cycle       | No           |
| cycle-issues   | Get issues in a specific cycle | No           |
| cycle-progress | Get cycle completion metrics   | No           |

### Team Operations

| Tool         | Description                 | Confirmation |
| ------------ | --------------------------- | ------------ |
| list-teams   | List all teams in workspace | No           |
| get-team     | Get team details            | No           |
| team-members | List team members           | No           |

### Label & State Operations

| Tool         | Description                                              | Confirmation |
| ------------ | -------------------------------------------------------- | ------------ |
| list-labels  | List all labels for a team                               | No           |
| list-states  | List workflow states (backlog, to-do, in-progress, done) | No           |
| create-label | Create new label                                         | Yes          |

## Security

- Never expose LINEAR_API_KEY in logs or output
- API key should have minimal required permissions
- All tools that modify data require confirmation

## Error Handling

1. Verify API Key: Check LINEAR_API_KEY is set correctly
2. Check API Rate Limits: GraphQL 1500 requests/hour; REST 500 requests/hour
3. Validate Query Syntax: Ensure GraphQL queries are well-formed
4. Check Team/Issue IDs: Verify IDs exist and are accessible

## Agent Integration

- planner: Project management and backlog prioritization
- developer: Issue tracking during development

## Common Workflows

### Sprint Planning

1. current-cycle - Get current sprint
2. list-issues --state Backlog - Get backlog items
3. update-issue --cycle-id ... - Assign issues to sprint

### Issue Triage

1. list-issues --state Backlog - Get unplanned issues
2. set-priority --issue-id ... --priority 2 - Set priority
3. add-label --issue-id ... --label bug - Categorize

### Project Tracking

1. list-projects --team-id ... - Get all projects
2. project-issues --project-id ... - Get project issues
3. cycle-progress --cycle-id ... - Check sprint progress

## Related

- Official Linear API Documentation: https://developers.linear.app/docs/graphql/working-with-the-graphql-api
- Linear GraphQL Explorer: https://studio.apollographql.com/public/Linear-API/home
- Linear Webhook Documentation: https://developers.linear.app/docs/graphql/webhooks

## Iron Laws

1. **ALWAYS** verify `LINEAR_API_KEY` is set before any API call — Linear's API returns a 401 with a generic error message when the key is missing or expired; early validation produces a clear, actionable error.
2. **NEVER** create duplicate issues without first searching by title — Linear doesn't deduplicate issues automatically; running the skill twice without a search creates duplicate work items that confuse team tracking.
3. **ALWAYS** use issue state IDs (not state names) when transitioning issues — state names are case-sensitive, locale-dependent, and change when teams rename states; IDs are stable.
4. **NEVER** fetch all team issues without a filter — unbounded team queries return thousands of issues, exhaust the API rate limit, and produce unusable context dumps.
5. **ALWAYS** cache team and project metadata within a session — team IDs and project keys don't change during a session; re-fetching on every operation wastes API quota and slows workflows.

## Anti-Patterns

| Anti-Pattern                                    | Why It Fails                                                     | Correct Approach                                                                         |
| ----------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Creating issues without deduplication check     | Duplicate issues split tracking; team velocity metrics skewed    | Search with a title filter (`issues` query with `filter.title.eq` field) before creating |
| Using state names in transitions                | Case-sensitive; breaks when team renames state; locale issues    | Use `workflowState { id }` query to get stable IDs; transition by ID                     |
| Fetching all team issues without filter         | Thousands of results; rate limit hit; unusable output            | Filter by `state`, `assignee`, `cycle`, or `label` in GraphQL query                      |
| Re-fetching team/project metadata per operation | Multiple identical API calls; rate limit waste; slow execution   | Fetch team and project IDs once at session start; reuse for all subsequent calls         |
| Ignoring pagination cursors                     | Only first page returned; missed issues cause incomplete reports | Use `pageInfo { hasNextPage, endCursor }` and paginate until `hasNextPage: false`        |

## Memory Protocol (MANDATORY)

**Before starting:**
Read .claude/context/memory/learnings.md

**After completing:**

- New pattern -> .claude/context/memory/learnings.md
- Issue found -> .claude/context/memory/issues.md
- Decision made -> .claude/context/memory/decisions.md

> ASSUME INTERRUPTION: If it is not in memory, it did not happen.
