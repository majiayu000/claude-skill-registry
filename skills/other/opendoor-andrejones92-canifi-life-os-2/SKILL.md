---
name: opendoor
description: Buy and sell homes with Opendoor's iBuyer platform.
category: realestate
---
# Opendoor Skill

Buy and sell homes with Opendoor's iBuyer platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/opendoor/install.sh | bash
```

Or manually:
```bash
cp -r skills/opendoor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OPENDOOR_EMAIL "your_email"
canifi-env set OPENDOOR_PASSWORD "your_password"
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

1. **Get Offer**: Get instant cash offer for your home
2. **Browse Homes**: Browse Opendoor-owned homes for sale
3. **Tour Homes**: Schedule self-guided home tours
4. **Track Offer**: Track your home sale progress
5. **Mortgage**: Get pre-approved for mortgage

## Usage Examples

### Get Offer
```
User: "Get an instant offer for my home at 123 Oak St"
Assistant: Initiates offer request
```

### Browse Homes
```
User: "Show me Opendoor homes in Phoenix"
Assistant: Returns available listings
```

### Schedule Tour
```
User: "Schedule a tour for tomorrow at 2pm"
Assistant: Books self-guided tour
```

### Track Sale
```
User: "What's the status of my home sale?"
Assistant: Returns sale progress
```

## Authentication Flow

1. Uses account authentication
2. No official API
3. Browser-based access
4. Session management

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Address Invalid | Not in service area | Check coverage |
| Tour Unavailable | Time slot taken | Choose another |
| Offer Expired | Timeout | Request new offer |

## Notes

- iBuyer model
- Instant cash offers
- Limited markets
- Self-tour access
- No public API
- Mobile apps available
