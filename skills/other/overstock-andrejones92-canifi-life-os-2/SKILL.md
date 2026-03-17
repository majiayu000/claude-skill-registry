---
name: overstock
description: Enables Claude to browse Overstock products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Overstock Skill

## Overview
Automates Overstock (now Bed Bath & Beyond) operations including home goods search, list management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/overstock/install.sh | bash
```

Or manually:
```bash
cp -r skills/overstock ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OVERSTOCK_EMAIL "your-email@example.com"
canifi-env set OVERSTOCK_PASSWORD "your-password"
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
- Search home and furniture items
- Add items to wishlist
- Track order status
- Find clearance deals
- Compare products
- View order history
- Check delivery estimates
- Browse by room

## Usage Examples

### Example 1: Search Products
```
User: "Find area rugs on Overstock"
Claude: I'll search for area rugs.
- Navigate to overstock.com
- Search "area rugs"
- Apply size filters if specified
- Sort by popularity
- Present top options
```

### Example 2: Check Clearance
```
User: "What's in clearance on Overstock?"
Claude: I'll browse clearance.
- Navigate to clearance section
- Browse marked-down items
- List significant discounts
- Present best deals
```

### Example 3: Track Order
```
User: "Track my Overstock order"
Claude: I'll check your order.
- Navigate to My Orders
- Find recent order
- Check shipping status
- Report delivery estimate
```

### Example 4: Browse by Room
```
User: "Show me bedroom furniture on Overstock"
Claude: I'll browse bedroom items.
- Navigate to bedroom category
- Browse furniture and decor
- Filter as requested
- Present curated options
```

## Authentication Flow
1. Navigate to overstock.com via Playwright MCP
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
- **Out of Stock**: Check similar items
- **Order Not Found**: Check order number
- **Clearance Sold**: Limited availability
- **Delivery Error**: Verify address
- **Price Changed**: Item may have updated

## Self-Improvement Instructions
When encountering new Overstock features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for platform changes

## Notes
- Overstock merged with Bed Bath & Beyond brand
- Club O membership for benefits
- Free shipping thresholds apply
- Clearance items may be final sale
- Price match available
- White glove delivery for furniture
- Easy returns policy
