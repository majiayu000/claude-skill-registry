---
name: kayak
description: Compare and track flight, hotel, and rental car prices across hundreds of travel sites with Kayak
category: travel
---

# Kayak Skill

## Overview
Enables Claude to search and compare travel prices across hundreds of booking sites, track price changes, set alerts, and find the best deals using Kayak's metasearch platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/kayak/install.sh | bash
```

Or manually:
```bash
cp -r skills/kayak ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set KAYAK_EMAIL "your-email@example.com"
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
- Compare flight prices across all major airlines and OTAs
- Search hotels with price comparison across booking sites
- Find rental car deals from multiple providers
- Set price alerts for specific routes
- Use Explore feature to find cheap destinations
- Access Price Forecast to time purchases optimally

## Usage Examples

### Example 1: Compare Flight Prices
```
User: "Find the cheapest flight from Boston to Seattle in February"
Claude: I'll search Kayak for the best prices.
- Opens Kayak via Playwright MCP
- Enters BOS to SEA, flexible February dates
- Compares across 300+ sites
- Returns price calendar showing cheapest days
- Best deal: Feb 11-18, Alaska $198 roundtrip
- Notes: Price Forecast says BUY NOW (likely to increase)
```

### Example 2: Set Price Alert
```
User: "Alert me if LAX to London drops below $500"
Claude: I'll set up a price alert for that route.
- Navigates to price alerts section
- Creates alert: LAX to LHR
- Sets threshold: under $500 roundtrip
- Confirms: Alert active, checking prices daily
- Current best: $612 on British Airways
```

### Example 3: Explore Destinations
```
User: "Where can I fly from Chicago for under $300 in March?"
Claude: I'll explore cheap destinations from Chicago.
- Uses Kayak Explore feature
- Sets budget: $300 roundtrip max
- Filters: March dates
- Shows map with options:
  - Denver: $148 roundtrip
  - Phoenix: $189 roundtrip
  - New Orleans: $234 roundtrip
  - Miami: $278 roundtrip
```

## Authentication Flow
1. Navigate to kayak.com via Playwright MCP
2. Click "Log in" and enter email
3. Complete password verification
4. Handle email confirmation if required
5. Sync saved searches and alerts
6. Maintain session for tracking

## Error Handling
- Login Failed: Try password reset, notify user
- Search Timeout: Retry with fewer filters
- No Results: Expand date range, suggest alternatives
- Session Expired: Re-authenticate automatically
- Rate Limited: Wait 2 minutes (strict anti-bot measures)
- Redirect to Booking: Note partner site for final booking

## Self-Improvement Instructions
After each interaction:
- Log price forecast accuracy
- Track best times to book patterns
- Note seasonal pricing trends
- Document UI and selector changes

Suggest updates when:
- Kayak changes search interface
- New comparison features added
- Price Forecast algorithm updates
- Explore feature expands

## Notes
- Kayak is a metasearch - actual booking happens on partner sites
- Price Forecast uses historical data for buy/wait recommendations
- Hacker Fares combine one-way tickets from different airlines
- Flex dates often reveal significant savings
- Private browsing may show different prices
- Some airlines (Southwest) not included in results
