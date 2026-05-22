---
name: newrelic
description: Monitor APM, infrastructure, and observability on New Relic
category: analytics
---

# New Relic Skill

## Overview
Enables Claude to access New Relic to view APM performance, infrastructure metrics, browser monitoring, and analyze application health across your full observability stack.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/newrelic/install.sh | bash
```

Or manually:
```bash
cp -r skills/newrelic ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NEWRELIC_EMAIL "your-email@example.com"
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
- View APM service performance
- Check infrastructure health
- Monitor browser/RUM data
- View synthetic monitoring
- Check alert conditions
- Analyze distributed tracing

## Usage Examples

### Example 1: Check APM
```
User: "How are my New Relic services?"
Claude: I'll check your New Relic dashboard.
- Opens one.newrelic.com via Playwright MCP
- Logs into account
- APM Services:
  - my-api: 89ms response, 0.1% error rate
  - worker-service: 234ms response, 0.02% error rate
  - frontend-bff: 45ms response, 0.05% error rate
- Throughput: 1.2k rpm
- Apdex: 0.95
- All services healthy
```

### Example 2: Check Infrastructure
```
User: "How's my infrastructure?"
Claude: I'll check Infrastructure.
- Views Infrastructure section
- Hosts: 8 reporting
  - prod-web-1: CPU 34%, Memory 67%
  - prod-web-2: CPU 28%, Memory 72%
  - prod-db-1: CPU 45%, Memory 85%
- Containers: 23 running
- Network: 450 Mbps avg
- Storage: 78% used
```

### Example 3: Check Alerts
```
User: "Any alerts firing?"
Claude: I'll check Alerts & AI.
- Views Alerts section
- Active incidents: 1
  - High Memory on prod-db-1
    - Opened: 15 min ago
    - Condition: Memory > 80%
    - Status: Acknowledged
- Recent incidents: 3 (last 24h)
  - All resolved
- Policies: 12 configured
```

## Authentication Flow
1. Navigate to one.newrelic.com via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA/SSO if enabled
5. Select account if multiple
6. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- SSO Redirect: Follow flow
- Session Expired: Re-authenticate
- Rate Limited: Wait and retry
- Access Denied: Check account permissions

## Self-Improvement Instructions
After each interaction:
- Track performance patterns
- Note alert frequency
- Log service metrics
- Document UI changes

Suggest updates when:
- New Relic updates UI
- New features added
- NRQL queries expand
- Integrations added

## Notes
- Full-stack observability
- NRQL query language
- Distributed tracing
- AI-powered insights
- Generous free tier
- Browser monitoring
- Mobile monitoring
