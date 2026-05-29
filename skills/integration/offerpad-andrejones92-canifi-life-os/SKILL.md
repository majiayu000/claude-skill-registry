---
name: offerpad
description: Sell your home quickly with Offerpad's iBuyer service.
category: realestate
---
# Offerpad Skill

Sell your home quickly with Offerpad's iBuyer service.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/offerpad/install.sh | bash
```

Or manually:
```bash
cp -r skills/offerpad ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OFFERPAD_EMAIL "your_email"
canifi-env set OFFERPAD_PASSWORD "your_password"
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

1. **Get Offer**: Receive cash offer for your home
2. **Flexible Options**: Choose sale date flexibility
3. **Buy Homes**: Browse Offerpad-owned homes
4. **Trade-In**: Trade current home for new one
5. **Track Progress**: Monitor sale progress

## Usage Examples

### Request Offer
```
User: "Get an offer for my home"
Assistant: Starts offer request process
```

### Choose Date
```
User: "I want to close in 30 days"
Assistant: Sets closing preference
```

### Browse Listings
```
User: "Show me Offerpad homes in Atlanta"
Assistant: Returns available homes
```

### Check Status
```
User: "What's my offer status?"
Assistant: Returns offer details
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation needed
4. Session management

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Bad credentials | Verify account |
| Not Serviceable | Outside market | Check coverage |
| Offer Unavailable | Criteria not met | Contact support |
| Session Expired | Timeout | Re-login |

## Notes

- iBuyer platform
- Flexible closing dates
- Select markets only
- Trade-in program
- No public API
- Mobile access
