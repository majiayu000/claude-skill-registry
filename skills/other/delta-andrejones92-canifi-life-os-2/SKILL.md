---
name: delta
description: Book flights, manage SkyMiles, check flight status, and access Delta Air Lines services
category: travel
---

# Delta Air Lines Skill

## Overview
Enables Claude to search and book Delta flights, manage SkyMiles account, track Medallion status, check flight status, and access Delta's premium travel services.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/delta/install.sh | bash
```

Or manually:
```bash
cp -r skills/delta ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DELTA_EMAIL "your-email@example.com"
canifi-env set DELTA_SKYMILES "your-skymiles-number"
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
- Search and book Delta and partner airline flights
- Manage reservations, seats, and upgrades
- Track SkyMiles balance and Medallion status
- Check real-time flight status and connections
- Access digital boarding passes
- Book Delta Vacations packages

## Usage Examples

### Example 1: Search Flights
```
User: "Find Delta flights from Atlanta to Los Angeles this weekend"
Claude: I'll search Delta for weekend flights.
- Opens delta.com via Playwright MCP
- Enters ATL to LAX, this Saturday-Sunday
- Shows available flights:
  - DL 123 7:00am Sat: $278, Main Cabin
  - DL 456 11:30am Sat: $312, Comfort+ available
  - DL 789 3:45pm Sat: $298, Delta One upgrade $450
- Notes: 2,456 miles earning, Medallion bonus applies
```

### Example 2: Check Medallion Status
```
User: "What's my Delta status and MQM progress?"
Claude: I'll check your SkyMiles account.
- Logs into Delta account
- Navigates to SkyMiles dashboard
- Returns: Platinum Medallion status
- MQMs: 68,432 of 75,000 for Diamond
- MQDs: $12,450 of $15,000 for Diamond
- Miles balance: 124,567 available
- Choice Benefits: Selected Global Entry, 4 remaining
```

### Example 3: Upgrade with Miles
```
User: "Can I upgrade my LAX flight to first class?"
Claude: I'll check upgrade availability.
- Navigates to My Trips
- Locates LAX reservation
- Checks upgrade options:
  - Comfort+: 8,500 miles + $75
  - First Class: 25,000 miles + $150
  - Delta One: Not available (international only)
- Confirms desired upgrade
- Processes upgrade: Now in First Class, Seat 2A
```

## Authentication Flow
1. Navigate to delta.com via Playwright MCP
2. Click "Log In" and enter SkyMiles number
3. Enter password
4. Handle 2FA via Delta app push or SMS
5. Verify Medallion status displayed
6. Maintain session for account operations

## Error Handling
- Login Failed: Retry, check for account lock
- Flight Full: Show waitlist option, alternatives
- Upgrade Unavailable: Add to upgrade list
- Session Expired: Re-authenticate seamlessly
- Rate Limited: Wait 90 seconds, retry
- 2FA Required: Check Delta app or SMS

## Self-Improvement Instructions
After each interaction:
- Track upgrade clearing patterns
- Note award sweet spots
- Log Medallion qualification progress
- Document interface changes

Suggest updates when:
- Delta changes booking flow
- SkyMiles program updates
- New cabin classes added
- Partner airlines change

## Notes
- Medallion members get complimentary upgrades when available
- Basic Economy cannot be upgraded
- Delta One available on select domestic routes
- SkyMiles don't expire for active accounts
- Companion certificates for Platinum and Diamond
- Sky Club access varies by status and fare class
