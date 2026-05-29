---
name: wish
description: Enables Claude to browse Wish products, manage wishlist, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Wish Skill

## Overview
Automates Wish operations including product discovery, wishlist management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wish/install.sh | bash
```

Or manually:
```bash
cp -r skills/wish ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WISH_EMAIL "your-email@example.com"
canifi-env set WISH_PASSWORD "your-password"
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
- Browse and search products
- Add items to wishlist
- Track order shipping
- View product reviews
- Find flash sales
- Access order history
- Check shipping estimates
- Explore daily deals

## Usage Examples

### Example 1: Search Products
```
User: "Find LED lights on Wish"
Claude: I'll search for LED lights.
- Navigate to wish.com
- Search "LED lights"
- Browse results
- Present interesting options
```

### Example 2: Add to Wishlist
```
User: "Save this item to my Wish wishlist"
Claude: I'll save that item.
- Navigate to product page
- Click save/wishlist button
- Confirm added
```

### Example 3: Track Order
```
User: "Track my Wish order"
Claude: I'll check your order status.
- Navigate to Order History
- Find recent order
- Check shipping progress
- Report current status
```

### Example 4: Browse Flash Sales
```
User: "What's on flash sale on Wish?"
Claude: I'll check flash sales.
- Navigate to flash deals
- Browse time-limited offers
- List notable deals
- Note time remaining
```

## Authentication Flow
1. Navigate to wish.com via Playwright MCP
2. Click Sign In
3. Enter email from canifi-env
4. Enter password
5. Handle CAPTCHA if shown (notify user)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **CAPTCHA Required**: Notify user to complete
- **Order Not Found**: Check order ID format
- **Tracking Delayed**: May take days to update
- **Item Unavailable**: Check similar items
- **Wishlist Full**: Check list limits
- **Sale Ended**: Deal may have expired

## Self-Improvement Instructions
When encountering new Wish features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Wish changes

## Notes
- Shipping times are long (2-4 weeks typically)
- Prices don't include shipping until checkout
- Product quality varies significantly
- Reviews help gauge quality
- Wish Express for faster shipping
- Flash sales time-limited
- Wish Local for faster delivery
