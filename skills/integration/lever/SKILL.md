---
name: lever
description: Manage talent acquisition with Lever's modern ATS and CRM platform.
category: hr
---
# Lever Skill

Manage talent acquisition with Lever's modern ATS and CRM platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lever/install.sh | bash
```

Or manually:
```bash
cp -r skills/lever ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LEVER_API_KEY "your_api_key"
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

1. **Candidate CRM**: Manage candidates as a talent CRM
2. **Pipeline Management**: Track candidates through custom stages
3. **Interview Coordination**: Schedule and manage interviews
4. **Feedback Collection**: Collect structured interview feedback
5. **Nurture Campaigns**: Send automated nurture emails

## Usage Examples

### Add Opportunity
```
User: "Create an opportunity for Jane Doe for the PM role"
Assistant: Creates candidate opportunity
```

### Move Stage
```
User: "Advance this candidate to the onsite stage"
Assistant: Updates opportunity stage
```

### Schedule Interview
```
User: "Schedule a phone screen for tomorrow"
Assistant: Creates interview event
```

### Send Nurture
```
User: "Add this candidate to the nurture campaign"
Assistant: Enrolls in nurture sequence
```

## Authentication Flow

1. Generate API key in Lever settings
2. Use API key for authentication
3. Key has associated permissions
4. Sandbox environment available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Combined ATS and CRM
- Talent sourcing features
- Visual pipeline builder
- Collaborative hiring
- Advanced analytics
- Slack integration
