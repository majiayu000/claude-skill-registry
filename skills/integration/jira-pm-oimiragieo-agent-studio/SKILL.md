---
name: jira-pm
description: Jira project management and issue tracking integration
allowed-tools: [Bash, Read, WebFetch]
version: 1.0
best_practices:
  - Use JQL (Jira Query Language) for precise issue searches
  - Verify project keys before creating issues
  - Use transitions to change issue status through valid workflows
  - Cache project metadata to reduce API calls
error_handling: graceful
streaming: not_supported
---

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

**Required**:

- `JIRA_URL` - Base URL of your Jira instance (e.g., https://yourcompany.atlassian.net)
- `JIRA_API_TOKEN` - API token for authentication (generate at Jira Account Settings → Security → API Tokens)
- `JIRA_USER_EMAIL` - Email address associated with the API token

**Optional**:

- `JIRA_DEFAULT_PROJECT` - Default project key for operations (e.g., PROJ)
- `JIRA_API_VERSION` - API version (default: 3)
  </requirements>

<instructions>
<execution_process>
1. **Authentication**: All requests use Basic Auth with `JIRA_USER_EMAIL` and `JIRA_API_TOKEN`
2. **Progressive Disclosure**: Load only necessary issue fields to minimize API calls
3. **Validation**: Verify project keys and issue keys before operations
4. **Error Handling**: Gracefully handle rate limits, authentication errors, and invalid inputs
</execution_process>

<tool_categories>

## Issues

| Tool             | Description                        | Confirmation Required |
| ---------------- | ---------------------------------- | --------------------- |
| **search**       | Search issues using JQL            | No                    |
| **get-issue**    | Get detailed issue information     | No                    |
| **create-issue** | Create a new issue                 | Yes                   |
| **update-issue** | Update existing issue fields       | Yes                   |
| **transition**   | Change issue status/workflow state | Yes                   |

## Projects

| Tool              | Description                      |
| ----------------- | -------------------------------- |
| **list-projects** | List all accessible projects     |
| **project-info**  | Get detailed project information |

## Sprints

| Tool              | Description                             |
| ----------------- | --------------------------------------- |
| **active-sprint** | Get currently active sprint for a board |
| **sprint-issues** | List all issues in a specific sprint    |

## Comments

| Tool             | Description                       |
| ---------------- | --------------------------------- |
| **get-comments** | Retrieve all comments on an issue |
| **add-comment**  | Add a comment to an issue         |

</tool_categories>

<usage_patterns>

## Common Workflows

**Issue Creation**:

1. List projects to find correct project key
2. Get project info to understand issue types
3. Create issue with appropriate fields
4. Add comment if needed

**Sprint Management**:

1. Get active sprint for board
2. List sprint issues
3. Update issue status using transitions
4. Add comments for status updates

**Issue Search**:

1. Use JQL for targeted searches (e.g., `project = PROJ AND status = "In Progress"`)
2. Retrieve issue details for specific issues
3. Update issues based on search results
   </usage_patterns>

<jql_examples>

## JQL Query Examples

**Common Queries**:

```jql
# Issues assigned to current user
assignee = currentUser()

# Open issues in specific project
project = PROJ AND status != Done

# Issues created this week
created >= startOfWeek()

# High priority bugs
type = Bug AND priority = High

# Issues in current sprint
sprint in openSprints()

# Recently updated issues
updated >= -7d

# Overdue issues
duedate < now() AND status != Done
```

</jql_examples>

<agent_integration>

## Primary Agent: pm (Product Manager)

- **Use Case**: Project backlog management, sprint planning, requirement tracking
- **Common Operations**: Create issues, update priorities, manage sprints

## Secondary Agent: developer

- **Use Case**: Issue tracking during development, status updates
- **Common Operations**: Search assigned issues, transition issues, add comments

## Supporting Agent: qa

- **Use Case**: Bug tracking, test case management
- **Common Operations**: Create bug reports, update test results, search defects
  </agent_integration>

<error_handling>

## Common Error Scenarios

**Authentication Errors**:

- Missing or invalid API token
- Expired credentials
- Insufficient permissions

**Rate Limiting**:

- Too many API requests in short period
- Implement exponential backoff

**Invalid Inputs**:

- Non-existent project keys
- Invalid issue types
- Invalid transition IDs

**Network Errors**:

- Connection timeouts
- Unreachable Jira instance
  </error_handling>

<best_practices>

1. **Use JQL Efficiently**: Craft precise JQL queries to reduce result sets and API calls
2. **Cache Metadata**: Store project keys, issue types, and transitions locally
3. **Verify Before Create**: Always verify project and issue type before creating issues
4. **Use Transitions**: Respect workflow states when changing issue status
5. **Batch Operations**: Group related API calls when possible
6. **Handle Errors Gracefully**: Provide clear error messages and recovery suggestions
7. **Respect Rate Limits**: Implement backoff strategies for high-volume operations
   </best_practices>
   </instructions>

<examples>
<code_example>
**Search Issues**:
```bash
# Using JQL to find issues
search "project = PROJ AND status = 'In Progress'"
```

**Create Issue**:

```bash
# Create a new story
create-issue --project PROJ --type Story --summary "Implement user authentication" --description "Add OAuth2 authentication flow"
```

**Update Issue**:

```bash
# Update issue priority
update-issue --key PROJ-123 --priority High
```

**Transition Issue**:

```bash
# Move issue to "In Progress"
transition --key PROJ-123 --status "In Progress"
```

**Get Sprint Issues**:

```bash
# List issues in active sprint
active-sprint --board-id 42
sprint-issues --sprint-id 123
```

**Add Comment**:

```bash
# Add progress update
add-comment --key PROJ-123 --comment "Completed authentication implementation, ready for review"
```

</code_example>
</examples>

<progressive_disclosure>

## Context Optimization

This skill uses progressive disclosure to minimize context usage:

1. **Lazy Loading**: Only load issue details when explicitly requested
2. **Field Selection**: Request only necessary fields from Jira API
3. **Caching**: Store frequently accessed metadata (projects, issue types)
4. **Streaming**: Not supported - all responses are complete payloads
5. **Pagination**: Automatically handle large result sets

**Context Savings**: 90%+ compared to loading full Jira MCP server
</progressive_disclosure>

<api_reference>

## Jira REST API Endpoints Used

- `/rest/api/3/search` - JQL search
- `/rest/api/3/issue/{issueKey}` - Get/update issue
- `/rest/api/3/issue` - Create issue
- `/rest/api/3/issue/{issueKey}/transitions` - Transition issue
- `/rest/api/3/project` - List projects
- `/rest/api/3/project/{projectKey}` - Get project details
- `/rest/agile/1.0/board/{boardId}/sprint` - Get sprints
- `/rest/agile/1.0/sprint/{sprintId}/issue` - Get sprint issues
- `/rest/api/3/issue/{issueKey}/comment` - Get/add comments

See [Jira REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/) for full reference.
</api_reference>
