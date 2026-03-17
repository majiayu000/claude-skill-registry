---
name: homedepot
description: Enables Claude to browse Home Depot products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Home Depot Skill

## Overview
Automates Home Depot operations including home improvement product search, list management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/homedepot/install.sh | bash
```

Or manually:
```bash
cp -r skills/homedepot ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HOMEDEPOT_EMAIL "your-email@example.com"
canifi-env set HOMEDEPOT_PASSWORD "your-password"
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
- Search tools and materials
- Add items to lists
- Track order status
- Check store inventory
- Find special buys
- Access Pro benefits
- View project guides
- Browse by department

## Usage Examples

### Example 1: Search Products
```
User: "Find cordless drills at Home Depot"
Claude: I'll search for cordless drills.
- Navigate to homedepot.com
- Search "cordless drill"
- Filter by brand or features
- Sort by rating
- Present top options
```

### Example 2: Check Store Availability
```
User: "Is this in stock at my local Home Depot?"
Claude: I'll check availability.
- Navigate to product page
- Check local store inventory
- View aisle location
- Report stock status
```

### Example 3: Find Special Buys
```
User: "What special buy deals are at Home Depot?"
Claude: I'll find special buys.
- Navigate to Special Buys section
- Browse discounted items
- Note savings
- Present best deals
```

### Example 4: Track Order
```
User: "Track my Home Depot order"
Claude: I'll check your order.
- Navigate to Order History
- Find recent order
- Check delivery status
- Report tracking info
```

## Authentication Flow
1. Navigate to homedepot.com via Playwright MCP
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
- **Out of Stock**: Check nearby stores
- **Store Not Found**: Verify zip code
- **Order Not Found**: Check order number
- **Pro Account Issue**: Check registration
- **Delivery Unavailable**: Check shipping options

## Self-Improvement Instructions
When encountering new Home Depot features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for HD changes

## Notes
- Pro Xtra for contractors
- Tool rental available
- Free in-store pickup
- Installation services
- Project calculators online
- How-to guides provided
- Military discount available
