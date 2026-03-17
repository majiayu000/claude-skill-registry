---
name: jira-ticket
description: Look up Jira ticket details including summary, type, and description. Use this to fetch ticket context for branch naming, PR creation, or understanding requirements.
---

# Jira Ticket Lookup

Fetch details about a Jira ticket.

## Requirements

This skill requires the [mcp-server-atlassian-jira](https://github.com/aashari/mcp-server-atlassian-jira) MCP server configured with the name `jira`.

## Usage

```
/jira-ticket SP-123
```

## Instructions

### 1. Look Up the Jira Ticket

Use the Jira MCP tools to fetch the ticket details:

```
mcp__jira__jira_get with:
  path: /rest/api/3/issue/{ticketNumber}
  jq: "{key: key, summary: fields.summary, type: fields.issuetype.name, description: fields.description}"
```

### 2. Determine Branch Prefix

Map the Jira issue type to a conventional commit prefix:

| Issue Type | Branch Prefix |
|------------|---------------|
| Story | `feat` |
| Task | `feat` |
| Bug | `fix` |
| Spike | `chore` |
| Sub-task | inherit from parent, or `feat` |
| Improvement | `feat` |
| Technical Debt | `refactor` |
| Documentation | `docs` |
| Default | `feat` |

### 3. Return Ticket Info

Provide the user with:
- Ticket key (e.g., `SP-123`)
- Summary
- Issue type
- Suggested branch prefix based on type
- Description (if available and requested)

### Example Output

```
Ticket: SP-123
Summary: Add user authentication
Type: Story
Suggested prefix: feat
Branch name: feat/SP-123-add-user-authentication
```
