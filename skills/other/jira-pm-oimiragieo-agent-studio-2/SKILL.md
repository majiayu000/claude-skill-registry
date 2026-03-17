---
name: jira-pm
description: Jira project management and issue tracking integration
version: 1.1.0
category: 'Other'
agents: [planner, developer]
tags: [jira, project-management, tickets, agile, sprint]
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, WebFetch]
best_practices:
  - Use JQL (Jira Query Language) for precise issue searches
  - Verify project keys before creating issues
  - Use transitions to change issue status through valid workflows
  - Cache project metadata to reduce API calls
error_handling: graceful
streaming: not_supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

**Mode: Cognitive/Prompt-Driven** - No standalone utility script; use via agent context.

<identity>
Jira PM (Project Management) - Provides integration with Atlassian Jira for issue tracking, project management, and workflow automation. Enables 90%+ context savings over direct MCP integration.
</identity>

<capabilities>
- Issue management: search, create, update, transition
- Project discovery and metadata retrieval
- Sprint management and issue tracking
- Comment management on issues
- JQL-based advanced queries
</capabilities>

<requirements>
## Environment Variables

Required:

- JIRA_URL - Base URL of your Jira instance (e.g., https://yourcompany.atlassian.net)
- JIRA_API_TOKEN - API token for authentication (generate at Jira Account Settings -> Security -> API Tokens)
- JIRA_USER_EMAIL - Email address associated with the API token

Optional:

- JIRA_DEFAULT_PROJECT - Default project key for operations (e.g., PROJ)
- JIRA_API_VERSION - API version (default: 3)
  </requirements>

<instructions>
<execution_process>
1. Authentication: All requests use Basic Auth with JIRA_USER_EMAIL and JIRA_API_TOKEN
2. Progressive Disclosure: Load only necessary issue fields to minimize API calls
3. Validation: Verify project keys and issue keys before operations
4. Error Handling: Gracefully handle rate limits, authentication errors, and invalid inputs
</execution_process>

<tool_categories>

## Issues

| Tool         | Description                        | Confirmation Required |
| ------------ | ---------------------------------- | --------------------- |
| search       | Search issues using JQL            | No                    |
| get-issue    | Get detailed issue information     | No                    |
| create-issue | Create a new issue                 | Yes                   |
| update-issue | Update existing issue fields       | Yes                   |
| transition   | Change issue status/workflow state | Yes                   |

## Projects

| Tool          | Description                      |
| ------------- | -------------------------------- |
| list-projects | List all accessible projects     |
| project-info  | Get detailed project information |

## Sprints

| Tool          | Description                             |
| ------------- | --------------------------------------- |
| active-sprint | Get currently active sprint for a board |
| sprint-issues | List all issues in a specific sprint    |

## Comments

| Tool         | Description                       |
| ------------ | --------------------------------- |
| get-comments | Retrieve all comments on an issue |
| add-comment  | Add a comment to an issue         |

</tool_categories>

<usage_patterns>

## Common Workflows

**Issue Creation**: List projects -> Get project info -> Create issue -> Add comment

**Sprint Management**: Get active sprint -> List sprint issues -> Update issue status -> Add comments

**Issue Search**: Use JQL for targeted searches -> Retrieve issue details -> Update issues

</usage_patterns>

<agent_integration>

## Primary Agent: planner

- Use Case: Project backlog management, sprint planning, requirement tracking
- Common Operations: Create issues, update priorities, manage sprints

## Secondary Agent: developer

- Use Case: Issue tracking during development, status updates
- Common Operations: Search assigned issues, transition issues, add comments

</agent_integration>

<error_handling>

## Common Error Scenarios

- Authentication Errors: Missing or invalid API token, expired credentials, insufficient permissions
- Rate Limiting: Too many API requests in short period, implement exponential backoff
- Invalid Inputs: Non-existent project keys, invalid issue types, invalid transition IDs
- Network Errors: Connection timeouts, unreachable Jira instance

</error_handling>

<best_practices>

1. Use JQL Efficiently: Craft precise JQL queries to reduce result sets and API calls
2. Cache Metadata: Store project keys, issue types, and transitions locally
3. Verify Before Create: Always verify project and issue type before creating issues
4. Use Transitions: Respect workflow states when changing issue status
5. Batch Operations: Group related API calls when possible
6. Handle Errors Gracefully: Provide clear error messages and recovery suggestions
7. Respect Rate Limits: Implement backoff strategies for high-volume operations

</best_practices>
</instructions>

<progressive_disclosure>

## Context Optimization

1. Lazy Loading: Only load issue details when explicitly requested
2. Field Selection: Request only necessary fields from Jira API
3. Caching: Store frequently accessed metadata (projects, issue types)
4. Streaming: Not supported - all responses are complete payloads
5. Pagination: Automatically handle large result sets

Context Savings: 90%+ compared to loading full Jira MCP server
</progressive_disclosure>

<api_reference>

## Jira REST API Endpoints Used

- /rest/api/3/search - JQL search
- /rest/api/3/issue/{issueKey} - Get/update issue
- /rest/api/3/issue - Create issue
- /rest/api/3/issue/{issueKey}/transitions - Transition issue
- /rest/api/3/project - List projects
- /rest/api/3/project/{projectKey} - Get project details
- /rest/agile/1.0/board/{boardId}/sprint - Get sprints
- /rest/agile/1.0/sprint/{sprintId}/issue - Get sprint issues
- /rest/api/3/issue/{issueKey}/comment - Get/add comments

See https://developer.atlassian.com/cloud/jira/platform/rest/v3/ for full reference.
</api_reference>

## Iron Laws

1. **ALWAYS** verify the project key exists before creating an issue — Jira silently ignores invalid project keys in some API versions, creating orphaned issues or returning cryptic errors.
2. **NEVER** use `PUT /issue` to change status — Jira status changes must go through valid workflow transitions via `POST /issue/{key}/transitions`; direct field updates bypass workflow validators and automation rules.
3. **ALWAYS** use JQL for issue searches rather than fetching all issues and filtering client-side — returning all issues wastes quota and causes timeouts on projects with thousands of tickets.
4. **NEVER** create duplicate issues without first searching for existing ones — duplicate tickets fragment tracking, confuse assignees, and produce misleading velocity metrics.
5. **ALWAYS** include `summary`, `issuetype`, and `project` fields when creating an issue — these three fields are the minimum required by Jira Cloud REST API v3; missing any produces a 400 error.

## Anti-Patterns

| Anti-Pattern                                     | Why It Fails                                                                                      | Correct Approach                                                           |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Updating status via field PUT                    | Bypasses workflow guards; invalid state transitions succeed silently; automation rules don't fire | Use `POST /issue/{key}/transitions` with the correct transition ID         |
| Fetching all issues and filtering locally        | Times out on large projects; wastes API quota; slow for paginated results                         | Always use JQL with specific project/sprint/status filters                 |
| Creating issues without duplication check        | Splits work tracking; team sees multiple tickets for same task                                    | Search with JQL (`project = X AND summary ~ "keyword"`) before creating    |
| Hardcoding field IDs (e.g., `customfield_10016`) | Field IDs differ between Jira instances and cloud/server; breaks across projects                  | Discover field IDs dynamically via `/rest/api/3/field` endpoint            |
| No error handling for rate limits (429)          | Jira Cloud rate limits at ~300 requests/minute; unhandled 429 crashes automation                  | Implement exponential backoff; check `Retry-After` header on 429 responses |

## Memory Protocol (MANDATORY)

**Before starting:**
Read .claude/context/memory/learnings.md

**After completing:**

- New pattern -> .claude/context/memory/learnings.md
- Issue found -> .claude/context/memory/issues.md
- Decision made -> .claude/context/memory/decisions.md

> ASSUME INTERRUPTION: If it is not in memory, it did not happen.
