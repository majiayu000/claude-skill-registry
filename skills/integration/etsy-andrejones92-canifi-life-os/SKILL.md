---
name: etsy
description: Enables Claude to browse Etsy products, manage favorites, and explore handmade items
version: 1.0.0
author: Canifi
category: ecommerce
---

# Etsy Skill

## Overview
Automates Etsy operations including searching handmade and vintage items, managing favorites, and exploring shops through browser automation. Note: Actual purchases are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/etsy/install.sh | bash
```

Or manually:
```bash
cp -r skills/etsy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ETSY_EMAIL "your-email@example.com"
canifi-env set ETSY_PASSWORD "your-password"
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
- Search handmade and vintage items
- Add items to favorites
- Explore seller shops
- Track order status
- Browse categories
- Read reviews
- Save favorite shops
- Compare similar items

## Usage Examples

### Example 1: Search Products
```
User: "Find handmade leather wallets on Etsy"
Claude: I'll search for those wallets.
- Navigate to etsy.com
- Search "handmade leather wallet"
- Filter by handmade/custom
- Sort by reviews
- Present top options
```

### Example 2: Add to Favorites
```
User: "Save this item to my Etsy favorites"
Claude: I'll add that to favorites.
- Navigate to item page
- Click heart/favorite button
- Confirm added to favorites
```

### Example 3: Explore Shop
```
User: "Show me more items from this Etsy shop"
Claude: I'll explore their shop.
- Navigate to seller's shop
- Browse available items
- Note shop policies
- Present popular items
```

### Example 4: Track Order
```
User: "Check my Etsy order status"
Claude: I'll check your orders.
- Navigate to Purchases
- Find recent order
- Check shipping status
- Report estimated delivery
```

## Authentication Flow
1. Navigate to etsy.com via Playwright MCP
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
- **Item Unavailable**: May be sold out
- **Shop Closed**: Check shop vacation status
- **Processing Time**: Note custom item delays
- **Favorites Full**: Check list limits
- **Shipping Unavailable**: Check seller location

## Self-Improvement Instructions
When encountering new Etsy features:
1. Document new UI elements
2. Add support for new item types
3. Log successful search patterns
4. Update for Etsy changes

## Notes
- Etsy specializes in handmade/vintage
- Processing times vary by seller
- Custom orders may take longer
- Shop reviews indicate reliability
- Shipping costs vary significantly
- Star Seller badge for top shops
- Gift wrapping often available
