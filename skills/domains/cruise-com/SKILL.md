---
name: cruise-com
description: Search and book cruises, compare cruise lines, and manage cruise reservations through Cruise.com
category: travel
---

# Cruise.com Skill

## Overview
Enables Claude to search and compare cruises across multiple cruise lines, find deals and promotions, and manage cruise vacation bookings through Cruise.com's comprehensive platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/cruise-com/install.sh | bash
```

Or manually:
```bash
cp -r skills/cruise-com ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CRUISE_COM_EMAIL "your-email@example.com"
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
- Search cruises by destination, date, and cruise line
- Compare cabin types and prices across ships
- Find last-minute deals and promotions
- Research cruise lines and ship amenities
- Access shore excursion information
- Track price drops on saved cruises

## Usage Examples

### Example 1: Search Caribbean Cruises
```
User: "Find Caribbean cruises in February under $1000 per person"
Claude: I'll search Cruise.com for Caribbean options.
- Opens cruise.com via Playwright MCP
- Searches Caribbean, February dates
- Filters: Under $1000pp, 7-day cruises
- Shows top deals:
  - Carnival Celebration 7-day: $649pp from Miami
  - Royal Caribbean Wonder: $789pp from FL
  - Norwegian Joy 7-day: $899pp from Miami
- Notes: Prices are cruise-only, port fees extra
```

### Example 2: Compare Cabin Types
```
User: "What cabin options are on that Carnival ship?"
Claude: I'll show cabin comparisons for Carnival Celebration.
- Opens Carnival Celebration ship page
- Shows cabin categories:
  - Interior: $649pp - No windows
  - Ocean View: $799pp - Window or porthole
  - Balcony: $999pp - Private balcony
  - Suite: $1,899pp - Extra space, priority
- Recommends: Balcony worth upgrade for Caribbean
```

### Example 3: Find Last-Minute Deals
```
User: "Any cruise deals departing in the next 60 days?"
Claude: I'll search last-minute cruise deals.
- Navigates to Last Minute section
- Shows departures within 60 days:
  - 4-day Bahamas (3 weeks out): $299pp
  - 7-day Alaska (5 weeks out): $599pp
  - 5-day Mexico (2 weeks out): $349pp
- Notes: Limited cabin availability on deals
```

## Authentication Flow
1. Navigate to cruise.com via Playwright MCP
2. Click "Sign In" and enter email
3. Complete password verification
4. Handle email confirmation if needed
5. Verify saved searches and alerts
6. Maintain session for quotes

## Error Handling
- Login Failed: Retry or continue as guest
- Cruise Sold Out: Suggest waitlist or alternatives
- Date Unavailable: Show nearby departure dates
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Price Changed: Alert user to new pricing

## Self-Improvement Instructions
After each interaction:
- Track deal patterns by cruise line
- Note seasonal pricing trends
- Log popular itinerary requests
- Document UI changes

Suggest updates when:
- Cruise.com updates search interface
- New cruise lines added
- Booking flow changes
- Deal categories expand

## Notes
- Cruise.com is an aggregator - compares multiple lines
- Prices typically per person, double occupancy
- Port fees and taxes add $100-200pp
- Drink packages and excursions sold separately
- Book early for best cabin selection
- Last minute deals have limited choices
- Travel insurance recommended for cruises
