---
name: atlassian-mcp
description: Use the Atlassian MCP Server to interact with JIRA from coding agents (Cursor, Claude Code). This skill documents how to use the official Atlassian MCP server for JIRA operations instead of the ai_first_* tools. Enable this MCP server in your Cursor/Claude Code settings for JIRA access.
---

# Atlassian MCP Server for JIRA

The Atlassian MCP Server provides direct access to JIRA from coding agents. Use this instead of `ai_first_*` JIRA tools when you need full JIRA capabilities in Cursor or Claude Code.

## Setup

### In Cursor

The Atlassian MCP Server is already configured globally. To enable it:

1. Open Cursor Settings
2. Go to Tools & MCP
3. Enable "Atlassian-MCP-Server"

Configuration location: `~/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "Atlassian-MCP-Server": {
      "url": "https://mcp.atlassian.com/v1/sse"
    }
  }
}
```

### In Claude Code

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "Atlassian-MCP-Server": {
      "url": "https://mcp.atlassian.com/v1/sse"
    }
  }
}
```

## Available Tools

When enabled, the Atlassian MCP Server provides these tools:

### Issue Operations

| Tool                                     | Description                     |
| ---------------------------------------- | ------------------------------- |
| `mcp_Atlassian_getJiraIssue`             | Get details of a specific issue |
| `mcp_Atlassian_createJiraIssue`          | Create a new issue              |
| `mcp_Atlassian_editJiraIssue`            | Update an existing issue        |
| `mcp_Atlassian_transitionJiraIssue`      | Change issue status             |
| `mcp_Atlassian_searchJiraIssuesUsingJql` | Search issues with JQL          |

### Comments

| Tool                                  | Description                |
| ------------------------------------- | -------------------------- |
| `mcp_Atlassian_addCommentToJiraIssue` | Add a comment to an issue  |
| `mcp_Atlassian_getJiraIssueComments`  | Get comments from an issue |

### Confluence (if enabled)

| Tool                                 | Description              |
| ------------------------------------ | ------------------------ |
| `mcp_Atlassian_createConfluencePage` | Create a Confluence page |
| `mcp_Atlassian_getConfluencePage`    | Get a Confluence page    |
| `mcp_Atlassian_searchConfluence`     | Search Confluence        |

## Common Patterns

### Get Issue Details

```
Use mcp_Atlassian_getJiraIssue with issueKey: "PROJ-123"
```

### Search for Issues

```
Use mcp_Atlassian_searchJiraIssuesUsingJql with:
  jql: "project = YOUR_PROJECT AND component = 'YOUR_COMPONENT' AND status = 'In Progress'"
```

### Create an Issue

```
Use mcp_Atlassian_createJiraIssue with:
  project: "YOUR_PROJECT"
  issueType: "Story"
  summary: "Implement new feature"
  description: "Description of the feature"
  components: ["YOUR_COMPONENT"]
```

### Transition Issue Status

```
Use mcp_Atlassian_transitionJiraIssue with:
  issueKey: "PROJ-123"
  transition: "In Progress"
```

### Add Comment

```
Use mcp_Atlassian_addCommentToJiraIssue with:
  issueKey: "PROJ-123"
  comment: "Started working on this issue"
```

## JQL Quick Reference

Common JQL queries for the Orient Task Force:

```jql
# All issues for YOUR_COMPONENT
project = YOUR_PROJECT AND component = "YOUR_COMPONENT"

# In Progress issues
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND status = "In Progress"

# Blockers
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND (priority = Blocker OR labels = blocked)

# Recent issues (last 7 days)
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND created >= -7d

# My issues
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND assignee = currentUser()

# Sprint issues
project = YOUR_PROJECT AND component = "YOUR_COMPONENT" AND sprint in openSprints()
```

## When to Use Which

| Need                                 | Use This                                                   |
| ------------------------------------ | ---------------------------------------------------------- |
| Quick issue lookup from Cursor       | Atlassian MCP Server                                       |
| Create/update issues from IDE        | Atlassian MCP Server                                       |
| Complex queries in IDE               | Atlassian MCP Server (full JQL)                            |
| Automated workflows (WhatsApp/Slack) | `ai_first_*` tools                                         |
| Presentation updates                 | `ai_first_*` tools (has slide integration)                 |
| SLA monitoring                       | `ai_first_check_sla_breaches`                              |
| Digest/summary reports               | `ai_first_get_daily_digest`, `ai_first_get_weekly_summary` |

## Comparison

| Feature               | Atlassian MCP       | ai*first*\* tools |
| --------------------- | ------------------- | ----------------- |
| Authentication        | OAuth via Atlassian | API token         |
| Issue CRUD            | Full support        | Read + links only |
| Comments              | Full support        | Not available     |
| Transitions           | Full support        | Not available     |
| JQL Search            | Full support        | Pre-built queries |
| Workspace integration | None                | Slack/WhatsApp    |
| Presentation sync     | None                | Built-in          |

## Troubleshooting

### "Tool not found" Error

Make sure the Atlassian MCP Server is enabled in your IDE settings. The tools won't appear until the server is connected.

### Authentication Issues

The Atlassian MCP Server uses OAuth. If you're not authenticated:

1. The tool will prompt you to authenticate
2. Follow the OAuth flow in your browser
3. Grant the necessary permissions

### Rate Limits

The Atlassian MCP Server is subject to Atlassian's rate limits. If you hit limits:

- Reduce query frequency
- Use more specific JQL to reduce result sets
- Cache results when appropriate
