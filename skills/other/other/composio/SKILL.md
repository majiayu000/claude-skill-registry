---
name: composio
description: Unified API integration platform for Unite-Hub. Connects to 800+ apps via Composio MCP — manages OAuth connections, discovers tools, executes actions across Gmail, GitHub, Slack, Linear, Notion, HubSpot, Stripe, and more. The single gateway for all third-party integrations.
category: backend
priority: 2
version: 1.0.0
status: active
dependencies: []
auto_load_for: [composio, connection, integration, connect app, third-party, oauth, api platform, unified api, tool search]
compatible_agents: [orchestrator, backend, email-agent, content-agent]
estimated_tokens: 800
---

# Composio Integration Skill

## Overview

Composio is Unite-Hub's **unified API gateway** — a single platform that replaces managing dozens of individual API integrations. Instead of writing custom OAuth flows, token management, and API wrappers for each service, Composio provides:

- **800+ pre-built toolkits** (Gmail, GitHub, Slack, Linear, Notion, HubSpot, Jira, etc.)
- **Managed OAuth flows** — handles token refresh, scopes, and auth state
- **MCP-native** — tools are exposed directly to Claude via the MCP protocol
- **Meta tools** — search for tools, manage connections, and execute actions dynamically

### Why Composio for Unite-Hub

Unite-Hub currently has custom integrations for Gmail, Google Analytics, Google Search Console, Linear, Stripe, Xero, and Outlook. Composio standardizes all of these (and hundreds more) behind a single interface, eliminating:
- Custom OAuth callback routes per service
- Token refresh logic per provider
- Individual API wrapper maintenance
- Authentication state management

## Configuration

### MCP Server (Project-Level)

**File**: `.claude/mcp.json`

```json
{
  "composio": {
    "command": "npx",
    "args": [
      "-y",
      "mcp-remote",
      "https://backend.composio.dev/v3/mcp/a34e0fe7-4c26-4da1-89e3-be9af2c086ea/mcp?user_id=pg-test-916354cc-3dbe-4fbd-973c-a02ea115698b"
    ],
    "env": {
      "npm_config_yes": "true"
    }
  }
}
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `COMPOSIO_API_KEY` | Composio project API key | Yes |
| `COMPOSIO_USER_ID` | Default user ID for connections | Yes |

**Values** (stored in `.env.local`):
```
COMPOSIO_API_KEY=ak_DtXrvQL_4y8VPJYiU6To
COMPOSIO_USER_ID=pg-test-916354cc-3dbe-4fbd-973c-a02ea115698b
```

## Core Capabilities

### 1. Tool Discovery (Meta Tool)

Use `COMPOSIO_SEARCH_TOOLS` to find actions across 800+ apps:

```
Search for "send email" → discovers GMAIL_SEND_EMAIL, OUTLOOK_SEND_EMAIL, etc.
Search for "create issue" → discovers GITHUB_CREATE_ISSUE, LINEAR_CREATE_ISSUE, JIRA_CREATE_ISSUE
Search for "send message" → discovers SLACK_SEND_MESSAGE, DISCORD_SEND_MESSAGE, etc.
```

**When to use**: You need a capability but don't know which toolkit provides it.

### 2. Connection Management

Use `COMPOSIO_MANAGE_CONNECTIONS` to add, list, and manage OAuth connections:

**Add a new connection:**
```
Connect Gmail → generates OAuth URL → user authenticates → connection saved
Connect GitHub → generates OAuth URL → user authenticates → connection saved
Connect Slack → generates OAuth URL → user authenticates → connection saved
```

**List active connections:**
```
List connections → shows all authenticated services with status
```

**Check connection health:**
```
Check connection "gmail" → returns auth status, token expiry, scopes
```

**When to use**: Setting up a new integration, verifying auth status, troubleshooting failures.

### 3. Action Execution

Once connected, execute actions directly through the MCP tools:

**Gmail Actions:**
- `GMAIL_FETCH_EMAILS` — Retrieve emails with filters
- `GMAIL_SEND_EMAIL` — Send emails
- `GMAIL_SEARCH_EMAILS` — Search by query
- `GMAIL_CREATE_DRAFT` — Create draft emails
- `GMAIL_CREATE_LABEL` — Manage labels

**GitHub Actions:**
- `GITHUB_CREATE_ISSUE` — Create issues
- `GITHUB_CREATE_PR` — Create pull requests
- `GITHUB_LIST_REPOS` — List repositories
- `GITHUB_GET_REPO_CONTENT` — Read repo files

**Slack Actions:**
- `SLACK_SEND_MESSAGE` — Send messages to channels
- `SLACK_LIST_CHANNELS` — List available channels
- `SLACK_SEARCH_MESSAGES` — Search message history

**Linear Actions:**
- `LINEAR_CREATE_ISSUE` — Create issues
- `LINEAR_LIST_ISSUES` — List project issues
- `LINEAR_UPDATE_ISSUE` — Update issue status

**HubSpot Actions:**
- `HUBSPOT_CREATE_CONTACT` — Create CRM contacts
- `HUBSPOT_LIST_CONTACTS` — List contacts
- `HUBSPOT_CREATE_DEAL` — Create deals

**Notion Actions:**
- `NOTION_CREATE_PAGE` — Create pages
- `NOTION_SEARCH` — Search workspace
- `NOTION_UPDATE_PAGE` — Update page content

### 4. Programmatic API Access

For server-side usage in Next.js API routes, use the TypeScript helper:

```typescript
import { composio } from '@/lib/integrations/composio';

// List active connections
const connections = await composio.listConnections();

// Initiate new connection
const authUrl = await composio.initiateConnection('gmail');

// Execute an action
const result = await composio.executeAction('GMAIL_FETCH_EMAILS', {
  max_results: 10,
  query: 'is:unread',
});

// Search for available tools
const tools = await composio.searchTools('send email');
```

## Workflows

### Workflow 1: Connect a New App

**User says**: "Connect my Gmail to Unite-Hub"

**Steps:**
1. Check if Gmail connection already exists via `COMPOSIO_MANAGE_CONNECTIONS`
2. If not connected, initiate OAuth flow
3. Provide the authorization URL to the user
4. User completes OAuth in browser
5. Verify connection is active
6. Confirm available Gmail actions

### Workflow 2: Discover Integration Capabilities

**User says**: "What can I do with Slack through Composio?"

**Steps:**
1. Use `COMPOSIO_SEARCH_TOOLS` with toolkit filter "slack"
2. List all available Slack actions with descriptions
3. Check if Slack connection exists
4. If not connected, offer to set it up
5. Show example usage for top actions

### Workflow 3: Execute Cross-Platform Action

**User says**: "When a new email arrives from a lead, create a Linear issue"

**Steps:**
1. Verify Gmail and Linear connections are active
2. Use `GMAIL_FETCH_EMAILS` to get recent unread emails
3. Filter for emails matching lead criteria
4. For each matching email, use `LINEAR_CREATE_ISSUE` to create a ticket
5. Log the cross-platform action in Unite-Hub's audit trail

### Workflow 4: Audit All Connections

**User says**: "Show me all active integrations"

**Steps:**
1. Call `COMPOSIO_MANAGE_CONNECTIONS` to list all connections
2. For each connection, check auth status and token health
3. Identify any expired or failing connections
4. Present a summary table with status indicators
5. Recommend re-authentication for any unhealthy connections

## Integration with Unite-Hub

### Replacing Existing Integrations

Composio can progressively replace custom integration code:

| Current Custom Integration | Composio Replacement | Status |
|---------------------------|---------------------|--------|
| `src/lib/integrations/gmail.ts` | `GMAIL_*` toolkit | Ready |
| `src/lib/integrations/outlook.ts` | `OUTLOOK_*` toolkit | Ready |
| `src/lib/integrations/linear/` | `LINEAR_*` toolkit | Ready |
| `src/lib/integrations/google-search-console.ts` | `GOOGLE_SEARCH_CONSOLE_*` toolkit | Ready |
| `src/lib/integrations/google-analytics-4.ts` | `GOOGLE_ANALYTICS_*` toolkit | Ready |
| `src/lib/integrations/google-business-profile.ts` | `GOOGLE_BUSINESS_PROFILE_*` toolkit | Ready |
| `src/lib/integrations/xeroIntegrationService.ts` | `XERO_*` toolkit | Ready |

### Agent Integration

Composio tools are available to all Unite-Hub agents:

- **Email Agent** — Use `GMAIL_*` and `OUTLOOK_*` instead of custom Gmail client
- **Content Agent** — Use `NOTION_*`, `GOOGLE_DOCS_*` for content publishing
- **Orchestrator** — Use `SLACK_*`, `LINEAR_*` for workflow notifications
- **Backend** — Use Composio API for connection management UI

### API Route Pattern

```typescript
// src/app/api/integrations/composio/connections/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { composio } from '@/lib/integrations/composio';

export async function GET(request: NextRequest) {
  const connections = await composio.listConnections();
  return NextResponse.json({ connections });
}

export async function POST(request: NextRequest) {
  const { app } = await request.json();
  const authUrl = await composio.initiateConnection(app);
  return NextResponse.json({ authUrl });
}
```

## Available Toolkits (Key Categories)

### Communication
Gmail, Outlook, Slack, Discord, Microsoft Teams, Twilio, SendGrid

### Project Management
Linear, Jira, Asana, Trello, Monday, ClickUp, Basecamp, Notion

### CRM & Sales
HubSpot, Salesforce, Pipedrive, Zoho CRM, Close, Freshsales

### Development
GitHub, GitLab, Bitbucket, CircleCI, Vercel, Netlify, Railway

### Productivity
Google Workspace (Docs, Sheets, Calendar, Drive), Microsoft 365, Dropbox

### Marketing
Mailchimp, ConvertKit, Brevo, ActiveCampaign, Buffer, Hootsuite

### Finance
Stripe, QuickBooks, Xero, FreshBooks, Wave

### Analytics
Google Analytics, Mixpanel, Amplitude, Segment, Plausible

### Social Media
Twitter/X, LinkedIn, Facebook, Instagram, YouTube, TikTok, Reddit

> **Full catalog**: 800+ apps at https://composio.dev/tools

## Error Handling

### Connection Failures
```
Error: "Connection expired for gmail"
→ Action: Re-initiate OAuth flow via COMPOSIO_MANAGE_CONNECTIONS
→ Notify user to re-authenticate
```

### Tool Not Found
```
Error: "Tool UNKNOWN_TOOL not found"
→ Action: Use COMPOSIO_SEARCH_TOOLS to find correct tool name
→ Check if the app is connected
```

### Rate Limiting
```
Error: "Rate limit exceeded"
→ Action: Composio handles rate limiting per provider
→ Retry with exponential backoff (automatic)
```

### Authentication Scope Missing
```
Error: "Insufficient permissions for GMAIL_SEND_EMAIL"
→ Action: Re-connect with required scopes
→ Use COMPOSIO_MANAGE_CONNECTIONS to update connection
```

## Command Reference

| Command | Action |
|---------|--------|
| "Connect [app] to Composio" | Initiate OAuth connection for an app |
| "List all connections" | Show all active Composio connections |
| "Search Composio tools for [query]" | Discover available actions |
| "Execute [action] via Composio" | Run a specific toolkit action |
| "Check connection health" | Verify all connections are active |
| "Disconnect [app]" | Remove an app connection |
| "What apps can I connect?" | Browse available toolkits |

## Triggers & Keywords

Auto-triggered by: `composio`, `connect app`, `add integration`, `oauth`, `third-party`, `unified api`, `tool search`, `manage connections`

## Version 1 Scope

**Included**:
- MCP server configuration (project + desktop)
- Connection management (add, list, check, remove)
- Tool discovery and search
- Action execution via MCP tools
- TypeScript helper library for API routes
- Integration with existing Unite-Hub agents

**Post-V1**:
- Composio trigger subscriptions (webhooks)
- Custom toolkit development
- Connection health monitoring dashboard
- Automatic migration from custom integrations
- Multi-tenant connection management (per workspace)

---

**Last Updated**: 2026-02-16
**MCP Server**: `composio` in `.claude/mcp.json`
**TypeScript Library**: `src/lib/integrations/composio.ts`
