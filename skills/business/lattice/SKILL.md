---
name: lattice
description: Manage people performance with Lattice's performance management platform.
category: hr
---
# Lattice Skill

Manage people performance with Lattice's performance management platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lattice/install.sh | bash
```

Or manually:
```bash
cp -r skills/lattice ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LATTICE_API_KEY "your_api_key"
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

1. **Performance Reviews**: Run review cycles and collect feedback
2. **Goal Management**: Set and track OKRs and goals
3. **1:1 Meetings**: Schedule and track one-on-ones
4. **Feedback**: Facilitate continuous feedback
5. **Engagement**: Run employee engagement surveys

## Usage Examples

### Start Review Cycle
```
User: "Launch the Q4 performance review cycle"
Assistant: Creates and starts review cycle
```

### Set Goals
```
User: "Create an OKR for the engineering team"
Assistant: Creates goal with key results
```

### Schedule 1:1
```
User: "Set up a recurring 1:1 with my direct report"
Assistant: Creates 1:1 series
```

### Run Survey
```
User: "Send out the quarterly engagement survey"
Assistant: Launches engagement survey
```

## Authentication Flow

1. Generate API key in Lattice admin settings
2. Use API key for authentication
3. Bearer token in header
4. Admin access required

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No admin access | Check user role |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Performance management focus
- OKR tracking built-in
- Continuous feedback features
- Engagement surveys included
- Analytics and insights
- Integration with HRIS systems
