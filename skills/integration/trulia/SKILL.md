---
name: trulia
description: Search homes and explore neighborhoods with Trulia's real estate platform.
category: realestate
---
# Trulia Skill

Search homes and explore neighborhoods with Trulia's real estate platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/trulia/install.sh | bash
```

Or manually:
```bash
cp -r skills/trulia ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TRULIA_EMAIL "your_email"
canifi-env set TRULIA_PASSWORD "your_password"
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

1. **Home Search**: Search homes for sale and rent
2. **Neighborhood Insights**: Explore detailed neighborhood data
3. **Crime Maps**: View local crime statistics
4. **Schools Info**: Access school ratings and info
5. **Commute Times**: Calculate commute times

## Usage Examples

### Search Homes
```
User: "Find family homes in safe neighborhoods in LA"
Assistant: Returns listings with safety scores
```

### Check Neighborhood
```
User: "What's this neighborhood like?"
Assistant: Returns neighborhood insights
```

### View Schools
```
User: "Show me schools near this listing"
Assistant: Returns nearby school ratings
```

### Calculate Commute
```
User: "What's the commute to downtown from here?"
Assistant: Returns commute estimates
```

## Authentication Flow

1. Uses Zillow account (owned by Zillow)
2. No official public API
3. Browser automation for access
4. Session-based login

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check credentials |
| Not Found | Property unavailable | Verify address |
| Session Expired | Timeout | Re-login |
| Rate Limited | Too many requests | Wait |

## Notes

- Owned by Zillow Group
- Neighborhood focus
- Crime and school data
- No public API
- Uses Zillow login
- Mobile apps available
