---
name: amplitude
description: Analyze product analytics with Amplitude's digital analytics platform.
category: analytics
---
# Amplitude Skill

Analyze product analytics with Amplitude's digital analytics platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/amplitude/install.sh | bash
```

Or manually:
```bash
cp -r skills/amplitude ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AMPLITUDE_API_KEY "your_api_key"
canifi-env set AMPLITUDE_SECRET_KEY "your_secret_key"
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

1. **Event Analytics**: Track and analyze user events
2. **User Journeys**: Visualize user paths and journeys
3. **Cohort Analysis**: Create and analyze user cohorts
4. **Experiment Analysis**: Analyze A/B test results
5. **Behavioral Charts**: Create custom analytics charts

## Usage Examples

### Get Event Stats
```
User: "Show me 'Signup' event counts for this week"
Assistant: Returns event counts and trends
```

### Analyze Journey
```
User: "Show the user journey from signup to first purchase"
Assistant: Returns journey visualization data
```

### Create Cohort
```
User: "Create a cohort of users who purchased in January"
Assistant: Creates cohort with specified criteria
```

### View Chart
```
User: "Show me daily active users for the past month"
Assistant: Returns DAU chart data
```

## Authentication Flow

1. Get API key from Amplitude project settings
2. Get secret key for export APIs
3. API key for tracking events
4. Secret key for querying data

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API keys |
| 403 Forbidden | No access | Check project permissions |
| 400 Bad Request | Invalid query | Fix query parameters |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Product analytics platform
- Generous free tier
- Behavioral cohorting
- Session replay available
- CDP capabilities
- Experiment platform included
