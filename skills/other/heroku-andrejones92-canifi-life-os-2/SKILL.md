---
name: heroku
description: Deploy apps, manage dynos, and monitor resources on Heroku
category: devops
---

# Heroku Skill

## Overview
Enables Claude to access Heroku to deploy applications, manage dynos and add-ons, view logs, and monitor app performance across the Heroku platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/heroku/install.sh | bash
```

Or manually:
```bash
cp -r skills/heroku ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HEROKU_EMAIL "your-email@example.com"
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
- View app status and metrics
- Check dyno formation and scaling
- Monitor add-ons (Postgres, Redis, etc.)
- View application logs
- Check pipeline and review apps
- View billing and usage

## Usage Examples

### Example 1: Check App Status
```
User: "How are my Heroku apps doing?"
Claude: I'll check your Heroku dashboard.
- Opens dashboard.heroku.com via Playwright MCP
- Logs into account
- Apps:
  - my-api-prod: Running (2 web dynos)
  - my-api-staging: Running (1 web dyno)
  - worker-service: Running (1 worker dyno)
- All apps healthy
- No crashed dynos
```

### Example 2: View App Logs
```
User: "Show me recent logs for my-api-prod"
Claude: I'll check the app logs.
- Views app detail page
- Recent logs:
  - 10:45 - Web.1: Request completed 200
  - 10:44 - Web.2: Database query 45ms
  - 10:43 - Web.1: Cache hit for user:123
- No errors in last hour
- Memory: 412MB / 512MB
```

### Example 3: Check Add-ons
```
User: "What add-ons am I using?"
Claude: I'll check your add-ons.
- Views Resources section
- my-api-prod add-ons:
  - Heroku Postgres: Standard-0 ($50/mo)
  - Heroku Redis: Premium-0 ($15/mo)
  - Papertrail: Choklad ($7/mo)
  - SendGrid: Bronze ($10/mo)
- Total add-on cost: $82/month
- All add-ons healthy
```

## Authentication Flow
1. Navigate to dashboard.heroku.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- App Crashed: Check logs
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Dyno Issue: Check metrics

## Self-Improvement Instructions
After each interaction:
- Track app patterns
- Note deployment frequency
- Log resource usage
- Document UI changes

Suggest updates when:
- Heroku updates dashboard
- New features added
- Pricing changes
- Platform evolves

## Notes
- PaaS platform
- Git-based deploys
- Managed infrastructure
- Good for MVPs
- Add-on ecosystem
- Review apps for PRs
- Pipelines for CI/CD
