---
name: instacart
description: Enables Claude to browse grocery stores, manage lists, and track deliveries on Instacart
version: 1.0.0
author: Canifi
category: food
---

# Instacart Skill

## Overview
Automates Instacart operations including grocery store browsing, list management, and order tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/instacart/install.sh | bash
```

Or manually:
```bash
cp -r skills/instacart ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set INSTACART_EMAIL "your-email@example.com"
canifi-env set INSTACART_PASSWORD "your-password"
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
- Browse grocery stores
- Search for products
- Manage shopping lists
- Track active orders
- View order history
- Check Instacart+ benefits
- Compare store prices
- Find deals and coupons

## Usage Examples

### Example 1: Browse Store
```
User: "Show me what's at Costco on Instacart"
Claude: I'll browse Costco.
- Navigate to instacart.com
- Select Costco
- Browse departments
- Present available categories
```

### Example 2: Search Products
```
User: "Find organic milk on Instacart"
Claude: I'll search for organic milk.
- Search "organic milk"
- Show results from available stores
- Compare prices
- Present options
```

### Example 3: Track Order
```
User: "Where is my Instacart order?"
Claude: I'll track your order.
- Navigate to Orders
- Find active order
- Check shopper progress
- Report delivery ETA
```

### Example 4: Create List
```
User: "Add eggs and bread to my Instacart list"
Claude: I'll add those items.
- Navigate to lists
- Add eggs to list
- Add bread to list
- Confirm items added
```

## Authentication Flow
1. Navigate to instacart.com via Playwright MCP
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
- **Store Unavailable**: Check delivery address
- **Item Out of Stock**: Suggest alternatives
- **Order Not Found**: Check order ID
- **Shopper Issue**: Check order status
- **Address Error**: Verify delivery address

## Self-Improvement Instructions
When encountering new Instacart features:
1. Document new UI elements
2. Add support for new stores
3. Log successful patterns
4. Update for Instacart changes

## Notes
- Orders not automated for security
- Instacart+ for free delivery over $35
- Personal shoppers fulfill orders
- Replacements may be suggested
- Same-day delivery available
- Tips are customary
- Price may differ from in-store
