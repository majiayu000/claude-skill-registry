---
name: compass
description: Search homes and connect with Compass agents for real estate services.
category: realestate
---
# Compass Skill

Search homes and connect with Compass agents for real estate services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/compass/install.sh | bash
```

Or manually:
```bash
cp -r skills/compass ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set COMPASS_EMAIL "your_email"
canifi-env set COMPASS_PASSWORD "your_password"
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

1. **Home Search**: Search homes with advanced filters
2. **Agent Matching**: Connect with local Compass agents
3. **Property Insights**: View AI-powered property insights
4. **Market Analysis**: Access local market data
5. **Collections**: Create and share property collections

## Usage Examples

### Search Homes
```
User: "Find luxury homes in Manhattan"
Assistant: Returns matching listings
```

### Find Agent
```
User: "Find a Compass agent in my area"
Assistant: Returns agent matches
```

### View Insights
```
User: "Show me market insights for this property"
Assistant: Returns AI-powered analysis
```

### Create Collection
```
User: "Create a collection of my favorite homes"
Assistant: Creates shareable collection
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Session-based access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Agent Unavailable | No matches | Expand search |
| Property Gone | Sold/delisted | Search alternatives |
| Session Expired | Timeout | Re-authenticate |

## Notes

- Technology-focused brokerage
- AI-powered insights
- Luxury market focus
- Agent-centric model
- No public API
- Mobile apps available
