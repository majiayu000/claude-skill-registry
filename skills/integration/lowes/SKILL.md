---
name: lowes
description: Enables Claude to browse Lowe's products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Lowe's Skill

## Overview
Automates Lowe's operations including home improvement product search, list management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lowes/install.sh | bash
```

Or manually:
```bash
cp -r skills/lowes ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LOWES_EMAIL "your-email@example.com"
canifi-env set LOWES_PASSWORD "your-password"
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
- Find deals of the day
- Access MyLowe's benefits
- View project ideas
- Browse by department

## Usage Examples

### Example 1: Search Products
```
User: "Find lawn mowers at Lowe's"
Claude: I'll search for lawn mowers.
- Navigate to lowes.com
- Search "lawn mower"
- Filter by type and brand
- Sort by rating
- Present top options
```

### Example 2: Check Store Availability
```
User: "Is this available at my local Lowe's?"
Claude: I'll check availability.
- Navigate to product page
- Check local store inventory
- View aisle location
- Report stock status
```

### Example 3: Find Daily Deals
```
User: "What's on deal at Lowe's today?"
Claude: I'll find today's deals.
- Navigate to deals section
- Browse daily discounts
- Note significant savings
- Present best offers
```

### Example 4: Track Order
```
User: "Track my Lowe's order"
Claude: I'll check your order.
- Navigate to Order History
- Find recent order
- Check delivery status
- Report tracking info
```

## Authentication Flow
1. Navigate to lowes.com via Playwright MCP
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
- **MyLowe's Error**: Check account status
- **Delivery Unavailable**: Check shipping options

## Self-Improvement Instructions
When encountering new Lowe's features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Lowe's changes

## Notes
- MyLowe's loyalty program
- Pro rewards for contractors
- Free store pickup
- Installation services
- Price match guarantee
- Military discount available
- Appliance delivery options
