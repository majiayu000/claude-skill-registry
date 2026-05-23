---
name: doordash
description: Enables Claude to browse restaurants, manage orders, and track deliveries on DoorDash
version: 1.0.0
author: Canifi
category: food
---

# DoorDash Skill

## Overview
Automates DoorDash operations including restaurant discovery, order tracking, and saved stores management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/doordash/install.sh | bash
```

Or manually:
```bash
cp -r skills/doordash ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DOORDASH_EMAIL "your-email@example.com"
canifi-env set DOORDASH_PASSWORD "your-password"
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
- Browse restaurants and menus
- Search by cuisine or dish
- Track active deliveries
- View past orders
- Manage saved stores
- Check DashPass benefits
- Find deals and promotions
- Reorder from history

## Usage Examples

### Example 1: Browse Restaurants
```
User: "Find pizza places on DoorDash"
Claude: I'll find pizza restaurants.
- Navigate to doordash.com
- Search "pizza"
- Filter by open and nearby
- Sort by rating
- Present top options
```

### Example 2: Check Menu
```
User: "What's on the McDonald's menu on DoorDash?"
Claude: I'll check their menu.
- Search for McDonald's
- Open store page
- Browse menu sections
- Present available items
```

### Example 3: Track Delivery
```
User: "Track my DoorDash order"
Claude: I'll track your delivery.
- Navigate to Orders
- Find active order
- Check Dasher location
- Report delivery ETA
```

### Example 4: Reorder Favorite
```
User: "Show me my last order from Chipotle"
Claude: I'll find that order.
- Navigate to Orders
- Search Chipotle orders
- Display order details
- Ready for reorder
```

## Authentication Flow
1. Navigate to doordash.com via Playwright MCP
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
- **Store Closed**: Show hours and suggest alternatives
- **No Dashers**: Area may be busy
- **Order Not Found**: Check order ID
- **Menu Error**: Refresh or check store hours
- **Address Issue**: Verify delivery address

## Self-Improvement Instructions
When encountering new DoorDash features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for DoorDash changes

## Notes
- Orders not automated for security
- DashPass membership for benefits
- Dashers are independent contractors
- Peak times may have longer waits
- Some stores are virtual brands
- Group orders available
- Schedule orders in advance
