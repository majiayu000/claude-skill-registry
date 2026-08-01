---
name: expedia
description: Book flights, hotels, vacation packages, and rental cars through Expedia's travel platform
category: travel
---

# Expedia Skill

## Overview
Enables Claude to search and book complete travel arrangements including flights, hotels, car rentals, and bundled packages through Expedia's comprehensive travel platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/expedia/install.sh | bash
```

Or manually:
```bash
cp -r skills/expedia ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EXPEDIA_EMAIL "your-email@example.com"
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
- Search and compare flights across multiple airlines
- Book hotels with One Key member benefits
- Create vacation packages (flight + hotel bundles)
- Reserve rental cars with pickup/dropoff flexibility
- Manage existing itineraries and reservations
- Access One Key rewards and member pricing

## Usage Examples

### Example 1: Search Vacation Package
```
User: "Find a flight and hotel package to Cancun for spring break, March 15-22"
Claude: I'll search Expedia for Cancun packages.
- Opens Expedia via Playwright MCP
- Selects "Vacation Packages" tab
- Enters departure city, Cancun destination
- Sets dates March 15-22
- Returns bundle options:
  - Package 1: Delta + Hyatt Ziva, $1,450/person
  - Package 2: United + Dreams Resort, $1,280/person
- Notes: Save $340 vs booking separately
```

### Example 2: Compare Flight Options
```
User: "What flights are available from LAX to JFK next Tuesday?"
Claude: I'll search Expedia for those flights.
- Navigates to Flights section
- Enters LAX to JFK, next Tuesday
- Compares options:
  - JetBlue 6am: $189, 5h 15m nonstop
  - Delta 9am: $245, 5h 30m nonstop
  - American 2pm: $178, 7h 45m (1 stop)
- Filters by One Key member pricing
```

### Example 3: Check Itinerary
```
User: "Show me my upcoming Expedia trips"
Claude: I'll retrieve your Expedia itineraries.
- Logs into Expedia account
- Navigates to My Trips
- Lists upcoming travel:
  - Miami: Feb 10-14, Marriott + American Airlines
  - Denver: March 5-8, Hilton only
- Provides confirmation numbers and check-in details
```

## Authentication Flow
1. Navigate to expedia.com via Playwright MCP
2. Click "Sign in" and enter email
3. Complete password or magic link verification
4. Handle 2FA if required
5. Confirm One Key status
6. Maintain session for bookings

## Error Handling
- Login Failed: Try password reset flow, notify user
- Flight Sold Out: Show alternative times/airlines
- Price Changed: Alert user, show new price
- Session Expired: Re-authenticate seamlessly
- Rate Limited: Wait 90 seconds, retry
- 2FA Required: Check email for verification link

## Self-Improvement Instructions
After each interaction:
- Track bundle savings vs separate bookings
- Log popular route pricing patterns
- Note One Key earning opportunities
- Document UI selector changes

Suggest updates when:
- Expedia updates booking flow
- One Key program changes
- New travel categories added
- Search filters modified

## Notes
- One Key members earn points across Expedia, Hotels.com, Vrbo
- Bundle deals often save 10-20% vs separate bookings
- Free cancellation varies by fare class and hotel
- Price tracking available for flexible dates
- VIP Access hotels offer extra perks for members
