---
name: fly-io
description: Deploy and manage globally distributed apps on Fly.io
category: devops
---

# Fly.io Skill

## Overview
Enables Claude to access the Fly.io dashboard to view and manage globally distributed applications, check machine status, monitor metrics, and view billing across Fly.io infrastructure.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/fly-io/install.sh | bash
```

Or manually:
```bash
cp -r skills/fly-io ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FLY_EMAIL "your-email@example.com"
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
- View app deployments
- Check machine status
- Monitor app metrics
- View volumes and storage
- Check certificates and domains
- View billing and usage

## Usage Examples

### Example 1: Check Apps
```
User: "How are my Fly.io apps?"
Claude: I'll check your Fly.io dashboard.
- Opens fly.io/dashboard via Playwright MCP
- Logs into account
- Apps:
  - my-api: 3 machines, Running (iad, lhr, sin)
  - my-frontend: 2 machines, Running (iad, lhr)
  - redis-cache: 1 machine, Running (iad)
- All apps healthy
- Global latency: <50ms avg
```

### Example 2: Check Machines
```
User: "What's the status of my Fly machines?"
Claude: I'll check machine status.
- Views Machines section
- my-api machines:
  - iad-1: shared-cpu-1x, 256MB, Running
  - lhr-1: shared-cpu-1x, 256MB, Running
  - sin-1: shared-cpu-1x, 256MB, Running
- CPU: 12% avg across regions
- Memory: 180MB / 256MB avg
- All health checks passing
```

### Example 3: View Billing
```
User: "What's my Fly.io bill?"
Claude: I'll check your usage.
- Views Billing section
- Current month: $23.45
- Breakdown:
  - Machines (compute): $18.00
  - Volumes (storage): $3.00
  - Bandwidth: $2.45
- Free tier credits applied
- Estimated monthly: $28
```

## Authentication Flow
1. Navigate to fly.io/dashboard via Playwright MCP
2. Enter email address
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for dashboard access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- App Issue: Check logs
- Session Expired: Re-authenticate
- Machine Down: Check region status
- Deploy Failed: Check build logs

## Self-Improvement Instructions
After each interaction:
- Track app patterns
- Note regional performance
- Log billing trends
- Document UI changes

Suggest updates when:
- Fly.io updates dashboard
- New features added
- Pricing changes
- Regions expand

## Notes
- Edge computing platform
- Global by default
- Docker-based deploys
- Persistent volumes
- Built-in load balancing
- WireGuard networking
- Great for latency-sensitive apps
