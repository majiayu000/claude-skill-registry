---
name: enterprise
description: Rent cars, manage reservations, and access Enterprise Plus benefits through Enterprise Rent-A-Car
category: travel
---

# Enterprise Rent-A-Car Skill

## Overview
Enables Claude to search and book rental cars, manage reservations, access Enterprise Plus member benefits, and coordinate pickup and return through Enterprise's rental network.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/enterprise/install.sh | bash
```

Or manually:
```bash
cp -r skills/enterprise ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ENTERPRISE_EMAIL "your-email@example.com"
canifi-env set ENTERPRISE_PLUS "your-enterprise-plus-number"
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
- Search rental cars by location and dates
- Compare vehicle classes and prices
- Manage existing reservations
- Access Enterprise Plus member benefits
- Arrange pickup and return at different locations
- Add insurance and additional driver options

## Usage Examples

### Example 1: Book a Rental Car
```
User: "I need a rental car at LAX for next week, compact or midsize"
Claude: I'll search Enterprise for LAX rentals.
- Opens enterprise.com via Playwright MCP
- Enters LAX location, next week dates
- Compares vehicle classes:
  - Compact (Corolla): $42/day, $294 total
  - Midsize (Camry): $48/day, $336 total
  - SUV (RAV4): $62/day, $434 total
- Notes: Enterprise Plus members earn 1 point/dollar
```

### Example 2: One-Way Rental
```
User: "Can I rent from San Francisco and drop off in LA?"
Claude: I'll check one-way availability.
- Enters SFO pickup, LAX return
- Shows one-way options:
  - Midsize: $389 total (includes $75 drop fee)
  - Full-size: $425 total
  - SUV: $512 total
- Notes: One-way fee varies by route
- Airport locations typically have best availability
```

### Example 3: Check Enterprise Plus Status
```
User: "What's my Enterprise Plus status?"
Claude: I'll check your Enterprise Plus account.
- Logs into Enterprise Plus
- Returns: Gold status
- Points balance: 4,850
- Free rental day at 850 points
- Benefits: Skip the counter, guaranteed upgrades
- Rentals this year: 8
```

## Authentication Flow
1. Navigate to enterprise.com via Playwright MCP
2. Click "Sign In" and enter Enterprise Plus number
3. Enter password
4. Handle security verification if prompted
5. Verify Plus status displayed
6. Maintain session for reservations

## Error Handling
- Login Failed: Retry with email, check credentials
- No Availability: Check nearby locations, adjust dates
- Class Sold Out: Suggest alternative vehicles
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 45 seconds, retry
- Location Closed: Suggest alternate pickup times

## Self-Improvement Instructions
After each interaction:
- Track pricing patterns by location
- Note vehicle class availability
- Log Enterprise Plus earning rates
- Document UI changes

Suggest updates when:
- Enterprise updates booking interface
- Enterprise Plus program changes
- New vehicle classes added
- Pricing structure changes

## Notes
- Enterprise picks you up at many locations
- Weekend rates often better than weekday
- Fuel purchase options available
- Insurance coverage varies by state
- Under-25 drivers face surcharge
- Enterprise Plus is free to join
- Points expire after 2 years of inactivity
