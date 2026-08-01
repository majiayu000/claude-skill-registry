---
name: skiplagged
description: Find hidden-city flight deals and significantly cheaper airfares using Skiplagged's fare discovery
category: travel
---

# Skiplagged Skill

## Overview
Enables Claude to discover hidden-city ticketing opportunities where booking a flight with a connection can be cheaper than booking direct to the connection city, along with traditional fare comparison.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/skiplagged/install.sh | bash
```

Or manually:
```bash
cp -r skills/skiplagged ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SKIPLAGGED_EMAIL "your-email@example.com"
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
- Find hidden-city flight deals
- Compare traditional flight prices
- Search one-way and roundtrip options
- Identify significant savings opportunities
- Check hotel deals alongside flights
- Set price alerts for routes

## Usage Examples

### Example 1: Find Hidden-City Fare
```
User: "Find the cheapest flight from NYC to Denver"
Claude: I'll search Skiplagged for deals including hidden-city.
- Opens skiplagged.com via Playwright MCP
- Enters NYC to Denver
- Shows results:
  - Direct flight: $289 (United)
  - Hidden-city via Denver to SLC: $149 (skip SLC leg)
  - Traditional: $198 (Spirit with stop)
- Explains: Book NYC-SLC, deplane at Denver
- Savings: $140 using hidden-city
```

### Example 2: Check Risks
```
User: "What are the risks of skiplagging?"
Claude: I'll explain the considerations.
- Key risks:
  1. Can't check bags (would go to final destination)
  2. Only works one-way
  3. Airlines may cancel return if you skip leg
  4. Frequent flyers risk account issues
  5. Must sit through entire layover time
- Best for: One-way, carry-on only travel
- Airlines don't like it but it's legal
```

### Example 3: Compare Normal vs Hidden
```
User: "Show me options to San Francisco, hidden and regular"
Claude: I'll compare all fare types.
- Searches NYC to SFO
- Standard fares:
  - United nonstop: $329
  - JetBlue 1-stop: $279
  - Spirit: $198 (bags extra)
- Hidden-city options:
  - SFO layover to Seattle: $189
  - SFO layover to Portland: $199
- Recommendation: Hidden saves $90, but check timing
```

## Authentication Flow
1. Navigate to skiplagged.com via Playwright MCP
2. Click "Log In" and enter email
3. Complete password verification
4. Verify saved searches load
5. Maintain session for alerts
6. Account optional for basic searches

## Error Handling
- Login Failed: Continue as guest (full functionality)
- No Hidden Fares: Show traditional options
- Route Not Available: Suggest alternate airports
- Session Expired: Re-authenticate for saved data
- Rate Limited: Wait 45 seconds, retry
- Price Expired: Refresh and recompare

## Self-Improvement Instructions
After each interaction:
- Track hidden-city savings by route
- Note which airlines commonly have deals
- Log connection city patterns
- Document UI changes

Suggest updates when:
- Skiplagged changes interface
- New search features added
- Airline policies change
- Hidden-city risks evolve

## Notes
- Hidden-city only works one-way
- Never check bags when skiplagging
- Book separately from loyalty programs
- Can't change/cancel hidden-city easily
- Some routes have consistent savings
- International hidden-city more complex
- Legal but airlines discourage it
