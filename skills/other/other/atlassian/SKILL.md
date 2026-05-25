---
name: atlassian
description: |
  Manage Jira issues and Confluence wiki pages in Atlassian Cloud.
  Use when: (1) searching/creating/updating Jira issues with JQL, (2) searching/reading/creating Confluence pages
  with CQL, (3) managing Jira workflows, transitions, and comments, (4) browsing Confluence spaces and page
  hierarchies. Supports OAuth 2.1 via MCP server (recommended) or API token authentication (fallback).
---

# Atlassian (Jira + Confluence)

Full Jira and Confluence integration with two authentication methods:
- **OAuth 2.1** via Atlassian MCP server — browser-based consent, auto-refresh tokens, calls MCP tools
- **API token** — email + token stored in keyring, calls REST API directly

## First-Time Setup

### Option 1: OAuth 2.1 via MCP Server (Recommended)

No API tokens or instance URLs needed. Uses dynamic client registration and PKCE.

```bash
pip install -r requirements.txt
python scripts/auth.py login --oauth
```

A browser opens for Atlassian authorization. Select which products (Jira, Confluence, Compass) to grant access. Tokens are stored in the system keyring and auto-refresh when expired.

Check status:
```bash
python scripts/auth.py status
```

### Option 2: API Token (Fallback)

For environments where browser-based OAuth isn't available.

```bash
pip install -r requirements.txt
python scripts/auth.py login
```

Follow the prompts to enter your Atlassian URL, email, and API token. Credentials are stored securely in the system keyring.

Create an API token at: https://id.atlassian.com/manage-profile/security/api-tokens

Check authentication status:
```bash
python scripts/auth.py status
```

Logout (clears both OAuth and API token credentials):
```bash
python scripts/auth.py logout
```

## Backend Selection

The scripts automatically detect which backend to use based on your auth type:
- **OAuth** → MCP backend (calls Atlassian MCP server tools)
- **API token** → REST backend (calls Atlassian REST API directly)

All commands work identically regardless of backend.

## Jira (scripts/jira.py)

### Search issues with JQL
```bash
python scripts/jira.py search "project = DEV AND status = Open"
python scripts/jira.py search "assignee = currentUser() ORDER BY updated DESC" --limit 10
```

### Get issue details
```bash
python scripts/jira.py get DEV-123
```

### Create an issue
```bash
python scripts/jira.py create --project DEV --summary "Fix login bug" --type Bug
python scripts/jira.py create --project DEV --summary "New feature" --type Story \
  --description "Details here" --priority High --assignee "user@example.com" --labels "backend,urgent"
```

### Update an issue
```bash
python scripts/jira.py update DEV-123 --summary "Updated summary" --priority High
python scripts/jira.py update DEV-123 --assignee "user@example.com"
```

### Transition issue status
```bash
python scripts/jira.py transition DEV-123 "In Progress"
python scripts/jira.py transition DEV-123 "Done"
```

### Add and list comments
```bash
python scripts/jira.py comment DEV-123 --add "This is a comment"
python scripts/jira.py comment DEV-123 --list
```

### List projects and statuses
```bash
python scripts/jira.py list-projects
python scripts/jira.py list-statuses DEV
```

### Test authentication
```bash
python scripts/jira.py auth-info
```

### List available MCP tools (OAuth only)
```bash
python scripts/jira.py list-tools
```

## Confluence (scripts/confluence.py)

### Search pages
```bash
python scripts/confluence.py search "deployment guide"
python scripts/confluence.py search "type=page AND space=DEV AND text~\"deployment\""
python scripts/confluence.py search "onboarding" --limit 10
```

### Read a page
```bash
python scripts/confluence.py read <page-id>
python scripts/confluence.py read <page-id> --json
```

### List spaces
```bash
python scripts/confluence.py list-spaces
python scripts/confluence.py list-spaces --limit 50
```

### Get space details
```bash
python scripts/confluence.py get-space <space-id>
```

### List pages in a space
```bash
python scripts/confluence.py list-pages --space-id <space-id>
```

### Create a page
```bash
python scripts/confluence.py create --title "New Page" --space-id <space-id>
python scripts/confluence.py create --title "Guide" --space-id <id> --body "<p>Content here</p>"
python scripts/confluence.py create --title "Child" --space-id <id> --parent-id <parent-id>
```

### Update a page
```bash
python scripts/confluence.py update <page-id> --title "Updated Title"
python scripts/confluence.py update <page-id> --body "<p>New content</p>"
```

### Get child pages
```bash
python scripts/confluence.py get-children <page-id>
```

### Test authentication
```bash
python scripts/confluence.py auth-info
```

### List available MCP tools (OAuth only)
```bash
python scripts/confluence.py list-tools
```

## Operations Reference

### Jira

| Command | Description | Required Args |
|---------|-------------|---------------|
| search | Search issues with JQL | jql |
| get | Get issue details | issue_key |
| create | Create new issue | --project, --summary, --type |
| update | Update existing issue | issue_key |
| transition | Change issue status | issue_key, status |
| comment | Add or list comments | issue_key |
| list-projects | List accessible projects | - |
| list-statuses | List statuses for project | project_key |
| auth-info | Test API connection | - |
| list-tools | List MCP tools (OAuth only) | - |

### Confluence

| Command | Description | Required Args |
|---------|-------------|---------------|
| search | Search using CQL | query |
| read | Get page content | page_id |
| list-spaces | List all spaces | - |
| get-space | Get space details | space_id |
| list-pages | List pages in a space | --space-id |
| create | Create new page | --title, --space-id |
| update | Update existing page | page_id |
| get-children | Get child pages | page_id |
| auth-info | Test API connection | - |
| list-tools | List MCP tools (OAuth only) | - |

## JSON Output

Add `--json` flag to any script command for machine-readable output.

## Token Management

Credentials stored securely using the system keyring:
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API

Service name: `atlassian-skill`

OAuth tokens auto-refresh when expired (if refresh token is available).
