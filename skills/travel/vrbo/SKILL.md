---
name: vrbo
description: Search and book vacation rentals, manage reservations, and communicate with property owners on Vrbo
category: travel
---

# Vrbo Skill

## Overview
Enables Claude to search vacation rentals, book entire homes and condos, communicate with property owners, and manage reservations through Vrbo's platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/vrbo/install.sh | bash
```

Or manually:
```bash
cp -r skills/vrbo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set VRBO_EMAIL "your-email@example.com"
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
- Search vacation rentals by location, size, and amenities
- Filter by property type, price, and reviews
- View property details, photos, and availability calendars
- Communicate with property owners/managers
- Manage existing bookings and payments
- Access One Key rewards from bookings

## Usage Examples

### Example 1: Find Vacation Rental
```
User: "Find a beach house in Destin for a family of 6 in July"
Claude: I'll search Vrbo for Destin beach houses.
- Opens vrbo.com via Playwright MCP
- Enters Destin, FL, July dates
- Filters: 3+ bedrooms, 6+ guests, beachfront
- Shows top results:
  - "Gulf View Paradise": 4BR, $350/night, pool
  - "Sandy Toes Retreat": 3BR, $275/night, beach access
  - "Ocean Breeze Villa": 4BR, $425/night, private beach
- Notes total costs including cleaning fees
```

### Example 2: Check Property Availability
```
User: "Is that beach house available for 4th of July week?"
Claude: I'll check the availability calendar.
- Opens property listing
- Views July calendar
- Returns: July 1-8 available
- Total: $2,450 (7 nights x $350)
- Cleaning fee: $275
- Service fee: $345
- Grand total: $3,070
- Cancellation: Full refund until June 1
```

### Example 3: Message Property Owner
```
User: "Ask if they allow small dogs"
Claude: I'll message the property owner.
- Opens messaging interface
- Composes inquiry: "Hi! We're interested in booking your property for July 1-8. We have a small, well-behaved dog (15 lbs). Are pets allowed? Thank you!"
- Sends message
- Reports: Message sent, owners typically respond within 4 hours
```

## Authentication Flow
1. Navigate to vrbo.com via Playwright MCP
2. Click "Sign in" and enter email
3. Complete password verification
4. Handle email confirmation if needed
5. Verify account dashboard loads
6. Maintain session for bookings

## Error Handling
- Login Failed: Retry with password reset link
- Property Unavailable: Suggest similar nearby properties
- Booking Failed: Verify payment, contact owner
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 60 seconds, retry
- Owner Unresponsive: Suggest alternative listings

## Self-Improvement Instructions
After each interaction:
- Track property availability patterns
- Note seasonal pricing trends
- Log owner response rates
- Document UI changes

Suggest updates when:
- Vrbo updates search interface
- One Key integration changes
- New filter options added
- Messaging system updates

## Notes
- Vrbo focuses on entire homes (not shared spaces)
- Total cost includes cleaning and service fees
- Book It Now properties can be reserved instantly
- Premier Host properties have higher standards
- One Key rewards work across Expedia family
- Always verify pet, event, and smoking policies
- Damage protection may be required
