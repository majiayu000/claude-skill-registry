---
name: render
description: Check deployments, manage services, monitor databases, and view logs on Render
category: devops
---

# Render Skill

## Overview
Enables Claude to access Render to check deployment status, manage web services and databases, monitor resource usage, and view logs for cloud deployments.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/render/install.sh | bash
```

Or manually:
```bash
cp -r skills/render ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RENDER_EMAIL "your-email@example.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- View deployment status and history
- Check service health and metrics
- Monitor database connections
- View service logs
- Check scheduled jobs (cron)
- Manage environment groups

## Usage Examples

### Example 1: Check Services
```
User: "What's the status of my Render services?"
Claude: I'll check your Render dashboard.
- Opens dashboard.render.com via Playwright MCP
- Logs into account
- Services:
  - Web Service (api): Running
  - Web Service (frontend): Running
  - PostgreSQL: Available
  - Redis: Available
- All services healthy
- Last deploy: 4 hours ago
```

### Example 2: View Logs
```
User: "Show logs for my API"
Claude: I'll check the service logs.
- Views API service logs
- Recent activity:
  - Server listening on port 10000
  - Connected to database
  - Healthy endpoint responding
  - 234 requests/minute
- Errors: 0 in last hour
- Memory: 256MB used
```

### Example 3: Check Database
```
User: "How's my Render database?"
Claude: I'll check database status.
- Views PostgreSQL instance
- Status: Available
- Connections: 5/100
- Storage: 1.2GB / 5GB
- Backups: Daily, 7 retained
- Last backup: 6 hours ago
- Region: Oregon
```

## Authentication Flow
1. Navigate to dashboard.render.com via Playwright MCP
2. Sign in with email or GitHub
3. Enter password or OAuth
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Try GitHub OAuth
- Service Down: Check crash logs
- Database Full: Alert user
- Session Expired: Re-authenticate
- Deploy Failed: View build logs
- Rate Limited: Wait and retry

## Self-Improvement Instructions
After each interaction:
- Track deployment patterns
- Note resource usage
- Log common errors
- Document UI changes

Suggest updates when:
- Render updates dashboard
- New regions added
- Features expand
- Pricing changes

## Notes
- Simple cloud platform
- Free tier for static sites
- Managed databases included
- Auto-scaling available
- Preview environments
- Blueprint for IaC
- Good Heroku alternative
