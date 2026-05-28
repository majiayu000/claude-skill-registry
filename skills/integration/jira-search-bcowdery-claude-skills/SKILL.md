---
name: jira-search
description: This skill should be used when searching for JIRA tickets using JQL queries, when finding tickets by status, assignee, or other criteria, or when the user says "find tickets", "search JIRA", "my open tickets", etc.
allowed-tools:
  - Bash
  - AskUserQuestion
---

# JIRA Search Skill

## Overview

Search for JIRA tickets using JQL (JIRA Query Language) via the Atlassian MCP Server or Atlassian CLI (`acli`), supporting both predefined quick filters and custom queries with formatted results.

**Note: Prefer using the Atlassian MCP Server tools when available. The MCP server provides direct API integration without requiring CLI installation.**

## When to Use

Use this skill when:
- Searching for tickets by any criteria (status, assignee, labels, etc.)
- Using quick filters like "my open tickets", "blocked tickets", "bugs"
- Building custom JQL queries
- Listing tickets from a sprint, epic, or project

Do NOT use this skill for:
- Creating new tickets (use `jira-create` instead)
- Updating existing tickets (use `jira-update` instead)
- Sprint planning analysis (use `jira-backlog-summary` instead)

## Quick Reference

### MCP Server (Preferred)

**Natural Language Search (Rovo):**
```
mcp__plugin_patsy_atlassian__search
  query: "my open high priority tickets"
```

**JQL Search:**
```
mcp__plugin_patsy_atlassian__searchJiraIssuesUsingJql
  cloudId: "your-cloud-id"
  jql: "assignee = currentUser() AND status NOT IN (Done, Closed)"
  maxResults: 50
```

**Get Single Issue:**
```
mcp__plugin_patsy_atlassian__getJiraIssue
  cloudId: "your-cloud-id"
  issueIdOrKey: "KEY-123"
```

### CLI Fallback

**Search Issues:**
```bash
acli jira workitem search \
  --jql "assignee = currentUser() AND status NOT IN (Done, Closed)" \
  --limit 50
```

**Get Single Issue:**
```bash
acli jira workitem search \
  --jql "key = KEY-123" \
  --limit 1
```

### Quick Filters

| Shortcut | JQL |
|----------|-----|
| `mine` | `assignee = currentUser() AND status NOT IN (Done, Closed)` |
| `review` | `assignee = currentUser() AND status IN ("In Review", "Code Review")` |
| `blocked` | `status = Blocked OR labels = "blocked"` |
| `urgent` | `priority IN (High, Highest) AND status != Done` |
| `bugs` | `type = Bug AND status != Done` |
| `recent` | `updated >= -7d ORDER BY updated DESC` |
| `unassigned` | `assignee is EMPTY AND status != Done` |
| `sprint` | `sprint in openSprints()` |

## Step-by-Step Process

### 1. Check for MCP Server Availability

First, check if the Atlassian MCP Server is available by looking for these tools:
- `mcp__plugin_patsy_atlassian__search` - Natural language search across Jira and Confluence (Rovo)
- `mcp__plugin_patsy_atlassian__searchJiraIssuesUsingJql` - Search JIRA issues using JQL
- `mcp__plugin_patsy_atlassian__getJiraIssue` - Get a specific JIRA issue by key
- `mcp__plugin_patsy_atlassian__fetch` - Get details by ARI (from search results)
- `mcp__plugin_patsy_atlassian__getAccessibleAtlassianResources` - Get cloud ID

If MCP tools are available, prefer using them over the CLI approach described below.

### 2. Understand User Intent

Parse the request to determine:
- Quick filter or custom search?
- Search parameters: assignee, status, project, labels, etc.

### 3. Build JQL Query

**Natural Language Mapping:**

| User Says | JQL |
|-----------|-----|
| "my tickets" | `assignee = currentUser()` |
| "high priority" | `priority IN (High, Highest)` |
| "bugs" | `type = Bug` |
| "in review" | `status IN ("In Review", "Code Review")` |
| "unassigned" | `assignee is EMPTY` |
| "updated this week" | `updated >= -7d` |
| "created today" | `created >= startOfDay()` |
| "overdue" | `duedate < now() AND status != Done` |

**Combine conditions:**
```jql
project = KEY AND status = "In Progress" AND assignee = currentUser()
```

### 4. Execute Search

**Option A: Using MCP Server - Natural Language (Preferred)**

For simple queries, use the natural language Rovo search:

```
Use mcp__plugin_patsy_atlassian__search with:
- query: "my open tickets assigned to me"
```

This returns ARI identifiers. Use `mcp__plugin_patsy_atlassian__fetch` with the ARI to get full details.

**Option B: Using MCP Server - JQL**

For complex queries requiring precise JQL:

```
Use mcp__plugin_patsy_atlassian__searchJiraIssuesUsingJql with:
- cloudId: "your-cloud-id"
- jql: "assignee = currentUser() AND status NOT IN (Done, Closed)"
- maxResults: 50
- fields: ["summary", "description", "status", "priority"]
```

**Option C: Using Atlassian CLI (Fallback)**

```bash
acli jira workitem search \
  --jql "assignee = currentUser() AND status NOT IN (Done, Closed)" \
  --limit 50
```

Add `--json` for programmatic parsing or omit for table output.

### 5. Format Results

**Compact format** (5+ results):
```
Found 12 tickets:

PROJ-101  [Story] [High] Implement JWT authentication
          Assignee: user@example.com | Status: In Progress

PROJ-102  [Bug] [Highest] Login page crashes on mobile
          Assignee: Unassigned | Status: To Do
```

**Detailed format** (1-4 results):
```
PROJ-101: Implement JWT authentication
Type: Story | Priority: High | Status: In Progress
Assignee: user@example.com
Labels: authentication, backend
Description: Implement JWT-based authentication...
Link: https://your-domain.atlassian.net/browse/PROJ-101
```

### 6. Provide Summary

- Total count and breakdown by status/priority if relevant
- Suggest refinements if too many (50+) or no results

## JQL Syntax Reference

### Operators
- Comparison: `=`, `!=`, `>`, `>=`, `<`, `<=`
- Lists: `IN (val1, val2)`, `NOT IN (val1, val2)`
- Text: `~ "search phrase"`
- Empty: `IS EMPTY`, `IS NOT EMPTY`

### Logical
- `AND`, `OR`, `NOT`

### Functions
- `currentUser()` - Logged in user
- `now()` - Current time
- `startOfDay()`, `endOfDay()`
- `startOfWeek()`, `endOfWeek()`
- `openSprints()` - Active sprints

### Date Ranges
- `-7d` (7 days ago)
- `-2w` (2 weeks ago)
- `-1M` (1 month ago)

### Sorting
```jql
ORDER BY priority DESC, created DESC
ORDER BY rank ASC  -- backlog order
```

## Common JQL Patterns

### My Open Tickets
```jql
assignee = currentUser() AND status NOT IN (Done, Closed, Resolved)
```

### High Priority Bugs
```jql
type = Bug AND priority IN (High, Highest) AND status != Done
```

### Current Sprint
```jql
sprint in openSprints() AND project = KEY
```

### Recently Updated
```jql
updated >= -7d ORDER BY updated DESC
```

### Text Search
```jql
text ~ "authentication" AND project = KEY
```

### Tickets by Epic
```jql
"Epic Link" = EPIC-123 ORDER BY rank ASC
```

## Advanced CLI Usage

### With Specific Fields (JSON)
```bash
acli jira workitem search \
  --jql "project = KEY" \
  --fields "key,summary,status,assignee" \
  --json
```

### With Sorting
```bash
acli jira workitem search \
  --jql "assignee = currentUser() ORDER BY priority DESC, created DESC" \
  --limit 50
```

### Complex Query
```bash
acli jira workitem search \
  --jql "project = KEY AND (status = 'To Do' OR status = 'In Progress') AND (priority = High OR labels = 'urgent') ORDER BY rank ASC" \
  --limit 50
```

## Common Mistakes

| Mistake | Solution |
|---------|----------|
| No result limit | Always include `--limit` to avoid huge result sets |
| Wrong status names | Check project's actual status values (might be "Open" not "To Do") |
| Forgetting quotes | Multi-word status values need quotes: `status = "In Progress"` |
| Case sensitivity | Field values are case-sensitive in some instances |
| Empty results confusion | Suggest widening filters or checking project key |

## Troubleshooting

- **JQL syntax errors**: Check operator usage, quotes, field names
- **Unknown fields**: Use standard field names or check custom field IDs
- **Invalid values**: Status, priority values vary by project configuration
- **Permission errors**: User may not have access to some projects
- **Too many results**: Add filters or reduce limit

## MCP Server Integration

### Available Tools

The Atlassian MCP Server provides these JIRA search tools:

- **`mcp__plugin_patsy_atlassian__search`** - Natural language search (Rovo)
  - Parameters: `query` (string) - Natural language search query
  - Returns: Array of results with ARI identifiers for Jira and Confluence content
  - Use this for simple queries like "my open tickets" or "bugs in project X"
  - Follow up with `fetch` to get full details

- **`mcp__plugin_patsy_atlassian__fetch`** - Get content by ARI
  - Parameters: `id` (string) - ARI from search results
  - Returns: Full details of the Jira issue or Confluence page
  - Use this after search to get complete information

- **`mcp__plugin_patsy_atlassian__searchJiraIssuesUsingJql`** - Search using JQL
  - Parameters:
    - `cloudId` (string) - Atlassian cloud instance ID or site URL
    - `jql` (string) - JQL query
    - `maxResults` (number, default 50, max 100)
    - `fields` (array, optional) - Specific fields to return
    - `nextPageToken` (string, optional) - For pagination
  - Returns: Array of issue objects with requested fields
  - Use this for precise, complex queries requiring JQL syntax

- **`mcp__plugin_patsy_atlassian__getJiraIssue`** - Get a specific issue by key
  - Parameters:
    - `cloudId` (string) - Atlassian cloud instance ID or site URL
    - `issueIdOrKey` (string) - Issue key (e.g., "PROJ-123")
  - Returns: Full issue details

### When to Use MCP vs CLI

**Use MCP Server when:**
- Available in the environment
- Need consistent API responses
- Want to avoid CLI installation
- Prefer structured JSON output

**Use Natural Language Search (Rovo) when:**
- User query is simple and conversational
- Searching across both Jira and Confluence
- Don't need precise JQL filtering
- Want fastest, simplest results

**Use JQL Search when:**
- Need precise filtering with multiple conditions
- Searching by specific fields or date ranges
- Using JQL functions (currentUser(), openSprints(), etc.)
- Need exact control over ordering and limits

**Use CLI when:**
- MCP server is not configured
- Need interactive table output
- Working with custom acli configurations
- Performing batch operations

### Example MCP Workflows

**Natural language search:**
```
1. Use mcp__plugin_patsy_atlassian__search with:
   query: "my open high priority bugs"

2. Get full details for a result:
   Use mcp__plugin_patsy_atlassian__fetch with:
   id: "ari:cloud:jira:cloudId:issue/12345"
```

**JQL search with specific fields:**
```
1. Use mcp__plugin_patsy_atlassian__searchJiraIssuesUsingJql with:
   cloudId: "your-cloud-id"
   jql: "project = PROJ AND status = 'In Progress' ORDER BY priority DESC"
   maxResults: 50
   fields: ["key", "summary", "status", "priority", "assignee"]
```
