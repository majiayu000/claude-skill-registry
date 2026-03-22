---
name: google-calendar-mcp
description: Step-by-step guide for setting up Google Calendar MCP server in Claude Code CLI. Use when users want to (1) connect Google Calendar to Claude Code, (2) set up the @cocal/google-calendar-mcp server, (3) configure OAuth credentials for Google Calendar API, or (4) troubleshoot Google Calendar MCP connection issues.
---

# Google Calendar MCP Setup Guide

Set up Google Calendar integration for Claude Code CLI using the @cocal/google-calendar-mcp server.

**Source:** https://github.com/nspady/google-calendar-mcp

## Prerequisites

- Node.js installed (for npx)
- Google account
- Claude Code CLI installed

## Part 1: Google Cloud Console Setup

### Step 1: Create Project
1. Go to https://console.cloud.google.com/
2. Click project dropdown (top-left) → **New Project**
3. Name: `Claude Calendar` → **Create**
4. Select the new project from dropdown

### Step 2: Enable Calendar API
1. Go to **APIs & Services** → **Library**
2. Search **"Google Calendar API"** → Click → **Enable**

### Step 3: OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** → **Create**
3. Fill required fields:
   - App name: `Claude Calendar`
   - User support email: (your email)
   - Developer contact: (your email)
4. Click **Save and Continue**
5. **Scopes** page → **Add or Remove Scopes**
   - Add: `https://www.googleapis.com/auth/calendar`
   - Click **Update** → **Save and Continue**
6. **Test Users** → **Add Users** → Add your Gmail → **Save and Continue**

### Step 4: Create Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `Claude Code`
5. Click **Create** → **Download JSON**

## Part 2: Save Credentials

Save the downloaded JSON file:

**Windows:**
```
C:\Users\salmanferoz\.google-calendar-mcp\gcp-oauth.keys.json
```

**Mac/Linux:**
```
~/.google-calendar-mcp/gcp-oauth.keys.json
```

Create the `.google-calendar-mcp` folder if it doesn't exist.

## Part 3: Add MCP to Claude Code

### Auto-Setup Command

When the user has saved their credentials, run this command automatically:

**Windows:**
```bash
claude mcp add --scope user --transport stdio google-calendar --env GOOGLE_OAUTH_CREDENTIALS="C:\Users\salmanferoz\.google-calendar-mcp\gcp-oauth.keys.json" -- npx -y @cocal/google-calendar-mcp
```

**Mac/Linux:**
```bash
claude mcp add --scope user --transport stdio google-calendar --env GOOGLE_OAUTH_CREDENTIALS="$HOME/.google-calendar-mcp/gcp-oauth.keys.json" -- npx -y @cocal/google-calendar-mcp
```

### Manual JSON Config (Alternative)

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "google-calendar": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@cocal/google-calendar-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/path/to/.google-calendar-mcp/gcp-oauth.keys.json"
      }
    }
  }
}
```

## Part 4: First Authorization

1. Restart Claude Code: `claude`
2. Ask: "What's on my calendar today?"
3. Browser opens → Sign in with Google
4. Click **Continue** (ignore "unverified app" warning)
5. Grant calendar permissions
6. Token saved automatically to `.google-calendar-mcp/token.json`

## Available Tools

| Tool | Description |
|------|-------------|
| list-calendars | Enumerate available calendars |
| list-events | Retrieve events with date filtering |
| get-event | Fetch specific event details by ID |
| search-events | Query events by text |
| create-event | Add new calendar events |
| update-event | Modify existing events |
| delete-event | Remove events |
| respond-to-event | Accept/decline/maybe invitations |
| get-freebusy | Check cross-calendar availability |
| get-current-time | Retrieve current date/time in timezone |
| list-colors | View available event colors |
| manage-accounts | Add/list/remove Google accounts |

## Features

| Feature | Description |
|---------|-------------|
| Multi-Account | Connect multiple Google accounts |
| Multi-Calendar | Query multiple calendars at once |
| Conflict Detection | Find overlapping events across accounts |
| Full CRUD | Create, read, update, delete events |
| Recurring Events | Manage recurring event patterns |
| Free/Busy | Check availability across calendars |
| Natural Language | Schedule events using natural language |
| Event Import | Import events from images/PDFs/web links |

## Environment Variables

| Variable | Description |
|----------|-------------|
| GOOGLE_OAUTH_CREDENTIALS | Path to OAuth credentials file (required) |
| GOOGLE_CALENDAR_MCP_TOKEN_PATH | Custom token storage location (optional) |

## MCP Management Commands

```bash
# List configured servers
claude mcp list

# Check status (inside Claude Code)
/mcp

# Remove server
claude mcp remove google-calendar

# Get server details
claude mcp get google-calendar
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Credentials not found" | Check `GOOGLE_OAUTH_CREDENTIALS` path is correct |
| "Access denied" | Add your email as test user in OAuth consent screen |
| "API not enabled" | Enable Google Calendar API in Cloud Console |
| Token expired | Delete `token.json` and re-authorize |
| Weekly re-auth required | Publish app to production mode in Cloud Console |

## File Locations Summary

| File | Purpose | Location |
|------|---------|----------|
| gcp-oauth.keys.json | OAuth credentials | `~/.google-calendar-mcp/` |
| token.json | Auth token (auto-created) | `~/.google-calendar-mcp/` |
| ~/.claude.json | Claude Code config | User home directory |
