---
name: bitbucket
description: Manage repositories, check pipelines, review PRs, and collaborate on Bitbucket
category: devops
---

# Bitbucket Skill

## Overview
Enables Claude to access Bitbucket to manage Git repositories, review pull requests, check Bitbucket Pipelines, and collaborate through Atlassian's code hosting platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bitbucket/install.sh | bash
```

Or manually:
```bash
cp -r skills/bitbucket ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BITBUCKET_EMAIL "your-email@example.com"
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
- View repositories and branches
- Check pull request status
- Monitor Bitbucket Pipelines
- View and manage issues (Jira integration)
- Check deployment status
- Manage repository settings

## Usage Examples

### Example 1: Check Pull Requests
```
User: "What PRs need my review?"
Claude: I'll check your Bitbucket PRs.
- Opens bitbucket.org via Playwright MCP
- Logs into account
- PRs requiring review:
  - PR #45 "API refactor" - 2 days old
  - PR #48 "Bug fix" - 5 hours old
- Your open PRs:
  - PR #44 "Feature complete" - 1 approval, needs 1 more
- Total open: 8 PRs
```

### Example 2: Check Pipeline Status
```
User: "Did the deploy succeed?"
Claude: I'll check the pipeline status.
- Views Pipelines
- Latest pipeline (main):
  - Status: Successful
  - Duration: 5m 12s
  - Steps: Build, Test, Deploy
  - Deployed to: Production
- Last 5 runs: All passed
```

### Example 3: View Repository Activity
```
User: "What's happened in the repo today?"
Claude: I'll check recent activity.
- Views repository activity
- Today's activity:
  - 12 commits to main
  - 3 PRs merged
  - 2 branches created
- Most active: feature/user-auth (8 commits)
- Contributors today: 4
```

## Authentication Flow
1. Navigate to bitbucket.org via Playwright MCP
2. Enter email (Atlassian account)
3. Enter password
4. Handle 2FA if enabled
5. Maintain session for operations

## Error Handling
- Login Failed: Check Atlassian credentials
- 2FA Required: Complete verification
- Pipeline Failed: Check step logs
- Session Expired: Re-authenticate
- Permission Denied: Check workspace access
- Rate Limited: Wait and retry

## Self-Improvement Instructions
After each interaction:
- Track PR review patterns
- Note pipeline configurations
- Log common queries
- Document UI changes

Suggest updates when:
- Bitbucket updates interface
- Pipeline features change
- Jira integration updates
- Deployment features expand

## Notes
- Part of Atlassian ecosystem
- Strong Jira integration
- Pipelines for CI/CD
- Deployments tracking built-in
- Code Insights for quality
- Merge checks configurable
- Free for small teams
