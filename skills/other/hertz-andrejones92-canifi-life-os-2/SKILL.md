---
name: hertz
description: Rent cars, manage Gold Plus Rewards, and access Hertz premium services
category: travel
---

# Hertz Skill

## Overview
Enables Claude to search and book rental cars, manage Hertz Gold Plus Rewards account, access premium vehicle collections, and handle reservations through Hertz's global network.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hertz/install.sh | bash
```

Or manually:
```bash
cp -r skills/hertz ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HERTZ_EMAIL "your-email@example.com"
canifi-env set HERTZ_GOLD_PLUS "your-gold-plus-number"
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
- Search and compare rental car options
- Access Hertz Gold Plus Rewards benefits
- Book premium collections (Dream, Adrenaline, Green)
- Manage existing reservations
- Arrange airport and neighborhood pickups
- Add equipment and protection options

## Usage Examples

### Example 1: Book at Airport
```
User: "Reserve a car at Denver airport for this weekend"
Claude: I'll search Hertz at Denver airport.
- Opens hertz.com via Playwright MCP
- Enters DEN airport, weekend dates
- Shows vehicle options:
  - Economy (Nissan Versa): $55/day
  - Compact (Toyota Corolla): $62/day
  - Standard (Camry/Malibu): $75/day
  - Full-size SUV (Tahoe): $125/day
- Gold Plus members: Walk to your car, skip counter
```

### Example 2: Book Dream Collection
```
User: "I want to rent a luxury car in Miami"
Claude: I'll check the Hertz Dream Collection.
- Navigates to Dream Cars
- Searches Miami locations
- Shows luxury options:
  - Porsche 911: $450/day
  - BMW M4: $325/day
  - Corvette Stingray: $275/day
  - Mercedes S-Class: $395/day
- Includes 75 miles/day, excess at $0.75/mile
```

### Example 3: Check Gold Status
```
User: "What are my Hertz Gold benefits?"
Claude: I'll check your Gold Plus Rewards account.
- Logs into Hertz account
- Returns: President's Circle status
- Points balance: 12,450
- Benefits: Counter bypass, free upgrades, spouse driving
- Free rental day: 550 points
- Recent rentals: 15 this year
```

## Authentication Flow
1. Navigate to hertz.com via Playwright MCP
2. Click "Sign In" and enter Gold Plus number
3. Enter password
4. Handle security verification if needed
5. Verify Gold status tier displayed
6. Maintain session for bookings

## Error Handling
- Login Failed: Retry with email, check account status
- Vehicle Unavailable: Suggest alternatives, nearby locations
- Dream Car Sold Out: Check other premium locations
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Location Closed: Show alternate hours/locations

## Self-Improvement Instructions
After each interaction:
- Track premium car availability
- Note pricing patterns by location/day
- Log Gold tier benefits
- Document UI updates

Suggest updates when:
- Hertz updates booking flow
- Gold Plus program changes
- New collections added
- Pricing structure changes

## Notes
- Gold Plus skip-counter works at airports
- President's Circle is highest tier
- Dream Collection at select locations only
- Adrenaline Collection has performance cars
- Green Collection has EVs and hybrids
- NeverLost GPS available for extra fee
- Young driver surcharge applies under 25
