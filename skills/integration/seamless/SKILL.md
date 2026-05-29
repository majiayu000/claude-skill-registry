---
name: seamless
description: Enables Claude to browse restaurants and track orders on Seamless (Grubhub)
version: 1.0.0
author: Canifi
category: food
---

# Seamless Skill

## Overview
Automates Seamless operations including restaurant browsing and order tracking through browser automation. Seamless is part of Grubhub. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/seamless/install.sh | bash
```

Or manually:
```bash
cp -r skills/seamless ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SEAMLESS_EMAIL "your-email@example.com"
canifi-env set SEAMLESS_PASSWORD "your-password"
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
- Browse restaurants
- Search cuisines and dishes
- Track active orders
- View order history
- Manage favorites
- Check corporate accounts
- Find deals
- Reorder past orders

## Usage Examples

### Example 1: Browse Restaurants
```
User: "Find sushi on Seamless"
Claude: I'll find sushi restaurants.
- Navigate to seamless.com
- Search "sushi"
- Filter by available
- Present top options
```

### Example 2: View History
```
User: "Show my recent Seamless orders"
Claude: I'll check your history.
- Navigate to Order History
- List recent orders
- Show restaurants and dates
- Present summary
```

### Example 3: Track Order
```
User: "Track my Seamless order"
Claude: I'll track your delivery.
- Navigate to Orders
- Find active order
- Check delivery status
- Report ETA
```

### Example 4: Reorder
```
User: "Show me my last order to reorder"
Claude: I'll find that order.
- Navigate to Order History
- Find most recent order
- Display items
- Ready for reorder
```

## Authentication Flow
1. Navigate to seamless.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Restaurant Closed**: Note hours
- **Order Not Found**: Check order ID
- **Corporate Account Issue**: Check work account
- **Address Error**: Verify delivery address
- **Menu Unavailable**: Try refresh

## Self-Improvement Instructions
When encountering new Seamless features:
1. Document UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Grubhub integration

## Notes
- Seamless is owned by Grubhub
- Popular in NYC metro area
- Corporate accounts common
- Same backend as Grubhub
- Grubhub+ applies
- Orders not automated for security
- Interface similar to Grubhub
