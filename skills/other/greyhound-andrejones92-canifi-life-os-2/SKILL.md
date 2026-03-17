---
name: greyhound
description: Book bus tickets, check schedules, and manage travel on Greyhound bus lines
category: travel
---

# Greyhound Skill

## Overview
Enables Claude to search and book Greyhound bus tickets, check schedules and routes, manage reservations, and access Road Rewards benefits for affordable intercity travel.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/greyhound/install.sh | bash
```

Or manually:
```bash
cp -r skills/greyhound ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GREYHOUND_EMAIL "your-email@example.com"
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
- Search bus routes and schedules
- Book tickets with Economy or Economy Extra
- Manage existing reservations and changes
- Check real-time bus status and delays
- Access Road Rewards loyalty benefits
- Find station locations and amenities

## Usage Examples

### Example 1: Book Bus Tickets
```
User: "Find a Greyhound from LA to San Diego this weekend"
Claude: I'll search Greyhound for those routes.
- Opens greyhound.com via Playwright MCP
- Enters Los Angeles to San Diego, Saturday
- Shows departures:
  - 7:00am: $19 Economy, 2h 30m
  - 10:00am: $22 Economy, 2h 15m
  - 1:00pm: $24 Economy Extra, 2h 15m
- Economy Extra includes extra legroom, priority boarding
```

### Example 2: Check Trip Status
```
User: "Is my bus to Phoenix running on time?"
Claude: I'll check your bus status.
- Finds reservation details
- Checks real-time tracking:
  - Bus currently 15 minutes behind schedule
  - Current location: Near Palm Springs
  - Revised arrival: 4:15pm
- Notes: One rest stop remaining
```

### Example 3: Compare Routes
```
User: "What's the cheapest way to get from Dallas to Houston?"
Claude: I'll compare Greyhound options.
- Searches DFW to Houston
- Shows price comparison:
  - Direct bus 8am: $25, 4h 30m
  - Direct bus 2pm: $29, 4h 15m
  - 1-stop via Austin: $22, 7h (not recommended)
- Cheapest: Book 2 weeks advance, often $15-18
```

## Authentication Flow
1. Navigate to greyhound.com via Playwright MCP
2. Click "Sign In" and enter email
3. Enter password or use magic link
4. Handle verification if prompted
5. Verify Road Rewards status
6. Maintain session for bookings

## Error Handling
- Login Failed: Try magic link option
- Route Sold Out: Check next departure
- Station Closed: Find alternative pickup point
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 30 seconds, retry
- Bus Canceled: Show rebooking options

## Self-Improvement Instructions
After each interaction:
- Track on-time performance by route
- Note advance purchase savings
- Log common route patterns
- Document UI changes

Suggest updates when:
- Greyhound updates booking flow
- Road Rewards program changes
- New routes or hubs added
- Pricing tiers change

## Notes
- Book 2+ weeks ahead for best prices
- Economy Extra worth it for longer trips
- WiFi and power outlets on most buses
- One personal item + one carry-on free
- Checked baggage has fees
- Some stations are unstaffed
- ID required for travel
