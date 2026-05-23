---
name: lyft
description: Book Lyft rides, check ride history, manage payment methods, and access Lyft Pink benefits
category: travel
---

# Lyft Skill

## Overview
Enables Claude to interact with Lyft's ride-sharing platform to request rides, manage account settings, view trip history, and utilize Lyft Pink membership benefits through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lyft/install.sh | bash
```

Or manually:
```bash
cp -r skills/lyft ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LYFT_EMAIL "your-email@example.com"
canifi-env set LYFT_PHONE "+1234567890"
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
- Request rides with specific pickup/dropoff and ride preferences
- Compare ride options (Standard, XL, Lux, Shared)
- View ride history and download receipts
- Check Lyft Pink membership status and benefits
- Manage saved addresses and payment methods
- Schedule rides in advance

## Usage Examples

### Example 1: Book a Lyft
```
User: "Book me a Lyft XL to the convention center"
Claude: I'll book a Lyft XL for you.
- Opens Lyft via Playwright MCP
- Sets destination to convention center
- Selects Lyft XL option
- Shows price: $32.50, ETA: 6 minutes
- Confirms booking and provides driver info: Toyota Highlander, License ABC123
```

### Example 2: Check Lyft Pink Benefits
```
User: "What Lyft Pink benefits do I have?"
Claude: I'll check your Lyft Pink membership status.
- Navigates to membership section
- Reports: Lyft Pink All Access active
- Benefits: 15% off all rides, priority pickup, relaxed cancellations
- 3 free Grubhub+ months remaining
- Next billing: $199/year on March 15
```

### Example 3: Schedule a Ride
```
User: "Schedule a Lyft for tomorrow at 7am from home to the office"
Claude: I'll schedule that ride for you.
- Opens Lyft scheduler
- Sets pickup: Home (saved address)
- Sets destination: Work (saved address)
- Schedules for tomorrow 7:00 AM
- Confirms: Lyft Standard scheduled, estimated $18-22
```

## Authentication Flow
1. Navigate to lyft.com via Playwright MCP
2. Click "Log in" and enter phone number
3. Receive and enter SMS verification code (via iMessage)
4. Complete any additional security verification
5. Store session for future requests

## Error Handling
- Login Failed: Retry authentication, notify via iMessage if persistent
- No Drivers: Retry in 2 minutes, suggest alternative times
- Payment Declined: Alert user to check payment method
- Session Expired: Re-authenticate silently
- Rate Limited: Implement 30-second backoff
- 2FA Required: Auto-retrieve code from iMessage

## Self-Improvement Instructions
After each interaction:
- Log successful selector patterns for UI elements
- Track fare estimate vs actual price accuracy
- Document new ride types or features
- Note regional availability differences

Suggest updates when:
- Lyft updates their web interface
- New ride categories are added
- Lyft Pink benefits change
- Authentication requirements change

## Notes
- Lyft Pink members get priority matching
- Shared rides not available in all markets
- Wait & Save can reduce fares by 10-25%
- Business profiles have separate expense tracking
- Scheduled rides can be modified up to 1 hour before
