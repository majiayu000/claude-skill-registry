---
name: uber
description: Request rides, check trip history, manage payment methods, and track drivers via Uber
category: travel
---

# Uber Skill

## Overview
Enables Claude to interact with Uber's ride-sharing platform to request rides, view trip history, check fare estimates, and manage account settings through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/uber/install.sh | bash
```

Or manually:
```bash
cp -r skills/uber ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set UBER_EMAIL "your-email@example.com"
canifi-env set UBER_PHONE "+1234567890"
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
- Request rides with pickup/dropoff locations and ride type preferences
- Get fare estimates before booking
- View and export trip history with receipts
- Track driver location and ETA in real-time
- Manage saved places (home, work, favorites)
- Check Uber Cash balance and promotions

## Usage Examples

### Example 1: Request a Ride
```
User: "Get me an Uber from my current location to SFO airport"
Claude: I'll request an Uber to SFO for you.
- Opens Uber via Playwright MCP
- Enters destination as SFO International Airport
- Shows available ride options with prices
- Confirms UberX at $45.50, arriving in 4 minutes
- Requests the ride and provides driver details
```

### Example 2: Check Trip History
```
User: "How much did I spend on Uber last month?"
Claude: I'll check your Uber trip history.
- Navigates to trip history section
- Filters trips from last month
- Calculates total: 12 trips totaling $287.45
- Offers to export receipts or add to LifeOS Finance tracking
```

### Example 3: Get Fare Estimate
```
User: "What would an Uber from downtown to the airport cost tomorrow at 6am?"
Claude: I'll get a fare estimate for that route and time.
- Uses Uber's fare estimator
- Shows UberX: $42-55, Comfort: $58-72, Black: $85-105
- Notes surge pricing unlikely at 6am
- Offers to schedule the ride in advance
```

## Authentication Flow
1. Navigate to uber.com via Playwright MCP
2. Click "Log in" and enter phone number from canifi-env
3. Handle SMS verification code (check iMessage via osascript)
4. Complete 2FA if prompted
5. Maintain session cookies for subsequent requests

## Error Handling
- Login Failed: Retry with alternate credentials, send iMessage notification
- No Drivers Available: Check again in 2 minutes, suggest alternative ride types
- Payment Failed: Alert user to update payment method manually
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry with exponential backoff
- 2FA Required: Extract code from iMessage, auto-enter

## Self-Improvement Instructions
After each interaction, document:
- New UI element selectors if Uber updates their interface
- Successful authentication patterns
- Common user request patterns to optimize responses
- Fare estimation accuracy vs actual charges

Suggest SKILL.md updates when:
- Uber adds new ride types or features
- Authentication flow changes
- API endpoints or selectors need updating

## Notes
- Uber requires phone verification for security
- Scheduled rides can be booked up to 30 days in advance
- Business profiles may have different payment flows
- Some regions have different ride type availability
- Never store payment card details - redirect user to add manually
