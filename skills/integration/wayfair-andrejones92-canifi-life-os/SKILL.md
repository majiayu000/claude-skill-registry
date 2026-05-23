---
name: wayfair
description: Enables Claude to browse Wayfair furniture and home goods, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Wayfair Skill

## Overview
Automates Wayfair operations including furniture and home decor search, idea boards, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wayfair/install.sh | bash
```

Or manually:
```bash
cp -r skills/wayfair ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WAYFAIR_EMAIL "your-email@example.com"
canifi-env set WAYFAIR_PASSWORD "your-password"
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
- Search furniture and home goods
- Add items to idea boards
- Track order status
- View room ideas
- Compare products
- Check sales and deals
- Manage wishlist
- View delivery estimates

## Usage Examples

### Example 1: Search Products
```
User: "Find mid-century modern sofas on Wayfair"
Claude: I'll search for those sofas.
- Navigate to wayfair.com
- Search "mid-century modern sofa"
- Apply style filters
- Sort by customer rating
- Present top options
```

### Example 2: Add to Idea Board
```
User: "Save this to my living room idea board"
Claude: I'll add it to your board.
- Navigate to product
- Click save to idea board
- Select living room board
- Confirm added
```

### Example 3: Track Order
```
User: "When will my Wayfair order arrive?"
Claude: I'll check your order.
- Navigate to My Orders
- Find recent order
- Check delivery status
- Report estimated delivery
```

### Example 4: Browse Sales
```
User: "What's on sale at Wayfair for outdoor furniture?"
Claude: I'll find outdoor sales.
- Navigate to outdoor category
- Filter by sale items
- Browse discounted furniture
- Present best deals
```

## Authentication Flow
1. Navigate to wayfair.com via Playwright MCP
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
- **Delivery Not Available**: Verify zip code
- **Order Not Found**: Check order number
- **Idea Board Full**: Create new board
- **Sale Ended**: Price may have changed

## Self-Improvement Instructions
When encountering new Wayfair features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Wayfair changes

## Notes
- Free shipping on many items
- Professional delivery for large items
- Assembly available for fee
- Way Day major annual sale
- MyWay rewards program
- Open Box deals available
- Financing options available
