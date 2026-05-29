---
name: walmart
description: Enables Claude to browse Walmart products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Walmart Skill

## Overview
Automates Walmart operations including product search, list management, order tracking, and deal discovery through browser automation. Note: Actual purchases are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/walmart/install.sh | bash
```

Or manually:
```bash
cp -r skills/walmart ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WALMART_EMAIL "your-email@example.com"
canifi-env set WALMART_PASSWORD "your-password"
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
- Search and browse products
- Add items to lists
- Track order status
- Check store availability
- Compare prices
- Find deals and rollbacks
- Manage pickup/delivery preferences
- View order history

## Usage Examples

### Example 1: Search Products
```
User: "Find air fryers on Walmart under $80"
Claude: I'll search for air fryers.
- Navigate to walmart.com
- Search "air fryer"
- Apply price filter under $80
- Sort by customer rating
- Present top options
```

### Example 2: Check Store Availability
```
User: "Is this item available at my local Walmart?"
Claude: I'll check store availability.
- Navigate to product page
- Check store pickup option
- View local store inventory
- Report availability status
```

### Example 3: Track Order
```
User: "Where is my Walmart order?"
Claude: I'll check your order status.
- Navigate to Account > Orders
- Find recent order
- Check shipping/pickup status
- Report tracking info
```

### Example 4: Find Deals
```
User: "Show me current Walmart rollback deals on electronics"
Claude: I'll find those deals.
- Navigate to deals section
- Filter by electronics
- Find rollback prices
- Present best savings
```

## Authentication Flow
1. Navigate to walmart.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Complete CAPTCHA if shown (notify user)
7. Verify account access
8. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **CAPTCHA Required**: Notify user to complete
- **Out of Stock**: Check other stores or online
- **Price Changed**: Note the difference
- **Store Not Found**: Verify zip code
- **Order Not Found**: Check order number

## Self-Improvement Instructions
When encountering new Walmart features:
1. Document new UI elements
2. Add support for new features
3. Log successful search patterns
4. Update for Walmart changes

## Notes
- Walmart+ membership for extra benefits
- In-store pickup available
- Express delivery in some areas
- Rollback prices are temporary
- Price match policy available
- Marketplace sellers included
- Pharmacy and services separate
