---
name: heap
description: Track user behavior automatically with Heap's auto-capture analytics platform.
category: analytics
---
# Heap Skill

Track user behavior automatically with Heap's auto-capture analytics platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/heap/install.sh | bash
```

Or manually:
```bash
cp -r skills/heap ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HEAP_APP_ID "your_app_id"
canifi-env set HEAP_API_KEY "your_api_key"
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

1. **Auto-capture**: Automatically track all user interactions
2. **Retroactive Analysis**: Analyze events retroactively without code
3. **Funnel Analysis**: Build conversion funnels from captured data
4. **Session Replay**: Watch user session recordings
5. **User Segments**: Create and analyze user segments

## Usage Examples

### Define Event
```
User: "Create a virtual event for button clicks on the pricing page"
Assistant: Creates event definition from auto-captured data
```

### Analyze Funnel
```
User: "Show conversion from homepage to signup"
Assistant: Returns funnel analysis with drop-off points
```

### View Session
```
User: "Show me sessions where users abandoned checkout"
Assistant: Returns relevant session recordings
```

### Create Segment
```
User: "Create a segment of power users"
Assistant: Creates user segment with criteria
```

## Authentication Flow

1. Get App ID from Heap project settings
2. Get API key for data access
3. App ID for tracking script
4. API key for data queries

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No project access | Check permissions |
| 400 Bad Request | Invalid query | Fix query format |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Auto-captures all interactions
- Retroactive event definition
- No code changes needed
- Session replay included
- Free tier available
- Point-and-click analysis
