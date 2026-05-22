---
name: vercel
description: Check deployments, monitor domains, view analytics, and manage projects on Vercel
category: devops
---

# Vercel Skill

## Overview
Enables Claude to access Vercel to check deployment status, monitor domain configurations, view analytics, and manage frontend project deployments on this leading deployment platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/vercel/install.sh | bash
```

Or manually:
```bash
cp -r skills/vercel ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set VERCEL_EMAIL "your-email@example.com"
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
- Check domain configurations
- Monitor Web Vitals and analytics
- View build logs
- Check environment variables
- Manage project settings

## Usage Examples

### Example 1: Check Deployment Status
```
User: "What's the latest deployment status?"
Claude: I'll check your Vercel deployments.
- Opens vercel.com via Playwright MCP
- Logs into account
- Latest deployment:
  - Project: my-app
  - Status: Ready
  - URL: my-app-abc123.vercel.app
  - Duration: 45s
  - Branch: main
- Preview deployments: 3 active
```

### Example 2: Check Domain Status
```
User: "Are my domains working?"
Claude: I'll check your domain configuration.
- Views domains section
- Domains:
  - myapp.com: Valid SSL, pointing correctly
  - api.myapp.com: Valid SSL, edge function
  - staging.myapp.com: Preview branch
- SSL: All certificates valid
- DNS: All records configured
```

### Example 3: View Analytics
```
User: "How's the site performance?"
Claude: I'll check Web Vitals.
- Views Analytics tab
- Web Vitals (last 7 days):
  - LCP: 1.2s (Good)
  - FID: 15ms (Good)
  - CLS: 0.05 (Good)
- Traffic: 45,000 visits
- Top pages: /, /about, /products
- Edge regions: All healthy
```

## Authentication Flow
1. Navigate to vercel.com via Playwright MCP
2. Sign in with email or GitHub
3. Enter password or OAuth
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Try GitHub OAuth
- Deployment Failed: Check build logs
- Domain Issue: Verify DNS settings
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Build Error: Check function logs

## Self-Improvement Instructions
After each interaction:
- Track deployment patterns
- Note common issues
- Log analytics preferences
- Document UI changes

Suggest updates when:
- Vercel updates dashboard
- New features added
- Edge features expand
- Analytics updated

## Notes
- Optimized for Next.js
- Edge Functions supported
- Preview deployments automatic
- Environment per branch
- Analytics built-in
- Team collaboration
- Free tier generous
