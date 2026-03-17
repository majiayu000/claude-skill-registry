---
name: loopnet
description: Search commercial real estate listings with LoopNet's marketplace.
category: realestate
---
# LoopNet Skill

Search commercial real estate listings with LoopNet's marketplace.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/loopnet/install.sh | bash
```

Or manually:
```bash
cp -r skills/loopnet ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LOOPNET_EMAIL "your_email"
canifi-env set LOOPNET_PASSWORD "your_password"
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

1. **Commercial Search**: Search commercial properties for sale and lease
2. **Property Listings**: View detailed commercial listings
3. **Broker Connections**: Connect with commercial brokers
4. **Market Reports**: Access commercial market data
5. **Saved Searches**: Save search criteria and alerts

## Usage Examples

### Search Commercial
```
User: "Find retail spaces in Chicago"
Assistant: Returns commercial listings
```

### View Listing
```
User: "Show me details for this office building"
Assistant: Returns property details
```

### Contact Broker
```
User: "Connect me with the listing broker"
Assistant: Initiates broker contact
```

### Set Alert
```
User: "Alert me about new industrial listings in Denver"
Assistant: Creates search alert
```

## Authentication Flow

1. Uses account authentication
2. Part of CoStar Group
3. Browser-based access
4. Free and premium tiers

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Verify account |
| Listing Removed | Property sold/leased | Search alternatives |
| Access Limited | Premium feature | Upgrade account |
| Session Expired | Timeout | Re-login |

## Notes

- Commercial RE marketplace
- CoStar Group owned
- Free basic access
- Premium for more data
- No public API
- Broker network
