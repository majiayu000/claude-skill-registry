---
name: redfin
description: Search homes and work with Redfin agents on the real estate platform.
category: realestate
---
# Redfin Skill

Search homes and work with Redfin agents on the real estate platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/redfin/install.sh | bash
```

Or manually:
```bash
cp -r skills/redfin ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set REDFIN_EMAIL "your_email"
canifi-env set REDFIN_PASSWORD "your_password"
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

1. **Home Search**: Search homes for sale with detailed filters
2. **Price History**: View price history and comparable sales
3. **Tour Scheduling**: Schedule home tours with Redfin agents
4. **Market Insights**: Access local market data and trends
5. **Estimate**: Get Redfin Estimate for home values

## Usage Examples

### Search Homes
```
User: "Find homes in Seattle with at least 4 bedrooms"
Assistant: Returns matching listings
```

### Schedule Tour
```
User: "Schedule a tour for this property"
Assistant: Initiates tour scheduling
```

### View Estimate
```
User: "What's the Redfin Estimate for this address?"
Assistant: Returns property value estimate
```

### Check Market
```
User: "How's the housing market in Portland?"
Assistant: Returns market data
```

## Authentication Flow

1. Redfin uses account authentication
2. No official public API
3. Browser automation for access
4. Session-based login

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check email/password |
| Property Not Found | Invalid address | Verify address |
| Session Expired | Timeout | Re-authenticate |
| Rate Limited | Too many requests | Slow down |

## Notes

- Real estate brokerage
- Agent services included
- No official public API
- Competitive commission rates
- 3D walkthrough tours
- Mobile apps available
