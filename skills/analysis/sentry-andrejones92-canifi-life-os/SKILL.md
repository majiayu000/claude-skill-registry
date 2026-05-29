---
name: sentry
description: Monitor application errors, performance, and issues on Sentry
category: analytics
---

# Sentry Skill

## Overview
Enables Claude to access Sentry to view and triage application errors, monitor performance issues, check release health, and analyze error trends across projects.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/sentry/install.sh | bash
```

Or manually:
```bash
cp -r skills/sentry ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SENTRY_EMAIL "your-email@example.com"
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
- View error issues and trends
- Check performance metrics
- Monitor release health
- View user impact analysis
- Check alert status
- Analyze stack traces

## Usage Examples

### Example 1: Check Issues
```
User: "What errors are happening in production?"
Claude: I'll check your Sentry dashboard.
- Opens sentry.io via Playwright MCP
- Logs into account
- my-app Issues (last 24h):
  - TypeError: Cannot read 'id': 234 events, 45 users
  - NetworkError: fetch failed: 89 events, 23 users
  - ReferenceError: undefined: 12 events, 5 users
- Total: 335 events
- Error rate: 0.3%
- Most affected: /api/users endpoint
```

### Example 2: Check Performance
```
User: "How's my app performance?"
Claude: I'll check Performance.
- Views Performance section
- Web Vitals:
  - LCP: 1.8s (Good)
  - FID: 45ms (Good)
  - CLS: 0.05 (Good)
- Slowest transactions:
  - /api/reports: 2.3s avg
  - /api/search: 1.8s avg
- Throughput: 45k req/hr
- Apdex: 0.94
```

### Example 3: Check Release Health
```
User: "How's the latest release doing?"
Claude: I'll check release health.
- Views Releases section
- v2.4.0 (deployed 6h ago):
  - Crash-free rate: 99.2%
  - Sessions: 12,456
  - Users affected: 98
  - New issues: 3
- Compared to v2.3.9:
  - Errors: +2% (slight regression)
  - Performance: -5% (improved)
```

## Authentication Flow
1. Navigate to sentry.io via Playwright MCP
2. Enter email or use SSO/OAuth
3. Enter password if email login
4. Handle 2FA if enabled
5. Select organization if multiple
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Project Access: Check permissions
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Quota Exceeded: Check plan

## Self-Improvement Instructions
After each interaction:
- Track error patterns
- Note performance trends
- Log release metrics
- Document UI changes

Suggest updates when:
- Sentry updates dashboard
- New features added
- Metrics expand
- Integrations added

## Notes
- Error monitoring standard
- Performance tracking
- Release tracking
- Source map support
- Issue assignment
- Alert integrations
- Self-hosted option
