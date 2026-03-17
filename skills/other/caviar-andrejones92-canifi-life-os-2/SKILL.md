---
name: caviar
description: Enables Claude to browse restaurants and track orders on Caviar (DoorDash)
version: 1.0.0
author: Canifi
category: food
---

# Caviar Skill

## Overview
Automates Caviar operations for premium restaurant browsing and order tracking through DoorDash integration. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/caviar/install.sh | bash
```

Or manually:
```bash
cp -r skills/caviar ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set CAVIAR_EMAIL "your-email@example.com"
canifi-env set CAVIAR_PASSWORD "your-password"
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
- Browse premium restaurants
- Search curated selections
- Track active orders
- View order history
- Access via DoorDash
- Find exclusive restaurants
- Check delivery availability
- View chef recommendations

## Usage Examples

### Example 1: Browse Restaurants
```
User: "Find upscale restaurants on Caviar"
Claude: I'll browse Caviar restaurants.
- Navigate to trycaviar.com
- Browse curated selections
- Filter by cuisine
- Present top options
```

### Example 2: Check Exclusives
```
User: "What Caviar-exclusive restaurants are near me?"
Claude: I'll find exclusives.
- Browse exclusive restaurants
- Check availability
- List Caviar-only options
- Present selections
```

### Example 3: Track Order
```
User: "Track my Caviar order"
Claude: I'll track your delivery.
- Navigate to DoorDash (Caviar merged)
- Find active order
- Check delivery status
- Report ETA
```

### Example 4: View Menu
```
User: "Show me the menu at this Caviar restaurant"
Claude: I'll check the menu.
- Navigate to restaurant page
- Browse menu items
- Note chef specials
- Present options
```

## Authentication Flow
1. Navigate to trycaviar.com via Playwright MCP
2. Sign in (may redirect to DoorDash)
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Use DoorDash credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Redirect to DoorDash**: Expected behavior
- **Restaurant Unavailable**: Check hours
- **Order Not Found**: Check DoorDash orders
- **Area Not Covered**: Premium delivery limited
- **Menu Error**: Refresh page

## Self-Improvement Instructions
When encountering Caviar/DoorDash changes:
1. Document integration patterns
2. Update for DoorDash merge
3. Log successful patterns
4. Note premium features

## Notes
- Caviar acquired by DoorDash
- Focus on premium restaurants
- May redirect to DoorDash
- Higher-end dining delivery
- Curated restaurant selection
- Orders not automated for security
- DashPass may apply
