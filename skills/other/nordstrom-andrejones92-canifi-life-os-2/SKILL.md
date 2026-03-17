---
name: nordstrom
description: Enables Claude to browse Nordstrom products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Nordstrom Skill

## Overview
Automates Nordstrom operations including fashion product search, wishlist management, and order tracking through browser automation. Note: Actual purchases are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/nordstrom/install.sh | bash
```

Or manually:
```bash
cp -r skills/nordstrom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set NORDSTROM_EMAIL "your-email@example.com"
canifi-env set NORDSTROM_PASSWORD "your-password"
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
- Search designer fashion
- Add items to wishlist
- Track order status
- Find Anniversary Sale deals
- Check store availability
- View Nordstrom Notes
- Browse by brand
- Access Nordstrom Rack deals

## Usage Examples

### Example 1: Search Products
```
User: "Find designer handbags at Nordstrom"
Claude: I'll search for handbags.
- Navigate to nordstrom.com
- Search "designer handbags"
- Filter by brand if specified
- Sort by relevance
- Present top options
```

### Example 2: Check Anniversary Sale
```
User: "What's on Anniversary Sale at Nordstrom?"
Claude: I'll check the sale.
- Navigate to Anniversary Sale section
- Browse sale items
- Filter by category
- Present top deals
```

### Example 3: Track Order
```
User: "Track my Nordstrom order"
Claude: I'll check your order.
- Navigate to Orders
- Find recent order
- Check shipping status
- Report delivery info
```

### Example 4: Browse Brand
```
User: "Show me Nike products at Nordstrom"
Claude: I'll browse that brand.
- Navigate to brand page
- Browse Nike products
- Filter by category if requested
- Present available items
```

## Authentication Flow
1. Navigate to nordstrom.com via Playwright MCP
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
- **Out of Stock**: Check other sizes/colors
- **Store Not Found**: Verify location
- **Order Not Found**: Check order number
- **Sale Ended**: Check regular price
- **Wishlist Error**: Check list limits

## Self-Improvement Instructions
When encountering new Nordstrom features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Nordstrom changes

## Notes
- Nordstrom Notes rewards program
- Free shipping and returns
- Anniversary Sale in July
- Nordstrom Rack for discounts
- Personal stylists available
- Price matching available
- Alterations services offered
