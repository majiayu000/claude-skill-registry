---
name: netlify
description: Check deployments, manage sites, monitor forms, and view analytics on Netlify
category: devops
---

# Netlify Skill

## Overview
Enables Claude to access Netlify to check deployment status, manage site configurations, monitor form submissions, and view analytics for JAMstack deployments.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/netlify/install.sh | bash
```

Or manually:
```bash
cp -r skills/netlify ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NETLIFY_EMAIL "your-email@example.com"
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
- Check site configurations
- Monitor form submissions
- View serverless function logs
- Check identity (auth) users
- Manage environment variables

## Usage Examples

### Example 1: Check Deploy Status
```
User: "Did my Netlify deploy succeed?"
Claude: I'll check your deployment status.
- Opens app.netlify.com via Playwright MCP
- Logs into account
- Latest deploy (my-site):
  - Status: Published
  - Duration: 1m 23s
  - Branch: main
  - URL: my-site.netlify.app
- Deploy previews: 2 active
```

### Example 2: Check Form Submissions
```
User: "Any new form submissions?"
Claude: I'll check your form data.
- Views Forms section
- Contact form submissions:
  - Today: 5 new submissions
  - This week: 23 total
  - Unread: 3
- Spam filtered: 12
- Form notifications: Enabled
```

### Example 3: View Function Logs
```
User: "Check my serverless function logs"
Claude: I'll view function activity.
- Views Functions tab
- Function invocations (24h):
  - api-handler: 1,234 calls
  - auth-verify: 567 calls
  - newsletter-signup: 89 calls
- Errors: 2 (0.1%)
- Avg duration: 145ms
```

## Authentication Flow
1. Navigate to app.netlify.com via Playwright MCP
2. Sign in with email or GitHub
3. Enter password or OAuth
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Try GitHub OAuth
- Deploy Failed: Check build logs
- Function Error: Check function logs
- Session Expired: Re-authenticate
- Form Limit: Note plan limits
- Build Timeout: Check build minutes

## Self-Improvement Instructions
After each interaction:
- Track deployment patterns
- Note form usage
- Log function monitoring
- Document UI changes

Suggest updates when:
- Netlify updates dashboard
- New features added
- Edge Functions expand
- Analytics updated

## Notes
- Great for JAMstack sites
- Built-in forms handling
- Functions (serverless)
- Identity for auth
- Split testing available
- Plugin ecosystem
- Free tier generous
