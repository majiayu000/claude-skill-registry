---
name: neon
description: Manage serverless Postgres databases and branches on Neon
category: devops
---

# Neon Skill

## Overview
Enables Claude to access Neon to view and manage serverless Postgres databases, database branches, connection pooling, and monitor query performance and usage.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/neon/install.sh | bash
```

Or manually:
```bash
cp -r skills/neon ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NEON_EMAIL "your-email@example.com"
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
- View project and database status
- Check branch topology
- Monitor compute usage
- View connection strings
- Check storage usage
- View billing and usage

## Usage Examples

### Example 1: Check Projects
```
User: "How are my Neon databases?"
Claude: I'll check your Neon console.
- Opens console.neon.tech via Playwright MCP
- Logs into account
- Projects:
  - my-saas-prod: 2 branches, 4GB storage
    - Compute: 0.25 CU, scales to 2 CU
    - Region: us-east-1
  - my-saas-dev: 3 branches, 500MB storage
- All projects healthy
- Compute: Currently scaled down (idle)
```

### Example 2: Check Branches
```
User: "What branches are active?"
Claude: I'll check database branches.
- Views my-saas-prod detail
- Branches:
  - main (primary): 4GB, active
  - staging: 800MB, active
  - preview-pr-42: 200MB, idle
- Recent activity:
  - 23k queries today
  - Compute time: 2.4 hours
- Auto-suspend: Enabled (5 min idle)
```

### Example 3: View Usage
```
User: "What's my Neon usage?"
Claude: I'll check usage metrics.
- Views Billing section
- Current month:
  - Compute: 45 hours ($9.00)
  - Storage: 4.5GB ($4.50)
  - Data transfer: 2GB (free)
- Total: $13.50
- Free tier: 300 compute hours remaining
- Project limit: 10 of 10 used
```

## Authentication Flow
1. Navigate to console.neon.tech via Playwright MCP
2. Enter email or use GitHub/Google OAuth
3. Enter password if email login
4. Handle 2FA if enabled
5. Maintain session for console access

## Error Handling
- Login Failed: Retry credentials
- 2FA Required: Complete verification
- Connection Issue: Check pooler
- Session Expired: Re-authenticate
- Compute Limit: Wait for scale-up
- Storage Limit: Check plan

## Self-Improvement Instructions
After each interaction:
- Track compute patterns
- Note branch usage
- Log storage growth
- Document UI changes

Suggest updates when:
- Neon updates console
- New features added
- Pricing changes
- Performance improves

## Notes
- Serverless Postgres
- Branching for dev/preview
- Auto-suspend saves costs
- Instant provisioning
- Connection pooling included
- Scale to zero
- Postgres compatible
