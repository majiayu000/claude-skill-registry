---
name: bestbuy
description: Enables Claude to browse Best Buy products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Best Buy Skill

## Overview
Automates Best Buy operations including electronics search, product comparison, availability checking, and order tracking through browser automation. Note: Actual purchases are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bestbuy/install.sh | bash
```

Or manually:
```bash
cp -r skills/bestbuy ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BESTBUY_EMAIL "your-email@example.com"
canifi-env set BESTBUY_PASSWORD "your-password"
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
- Search electronics and appliances
- Compare product specifications
- Check store availability
- Track order status
- View open-box deals
- Access My Best Buy rewards
- Manage saved items
- View order history

## Usage Examples

### Example 1: Search Products
```
User: "Find 4K TVs at Best Buy under $500"
Claude: I'll search for 4K TVs.
- Navigate to bestbuy.com
- Search "4K TV"
- Apply price filter under $500
- Sort by customer reviews
- Present top options
```

### Example 2: Compare Products
```
User: "Compare these two laptops"
Claude: I'll compare the specs.
- Navigate to both product pages
- Gather specifications
- Compare features side-by-side
- Present comparison summary
```

### Example 3: Check Open Box Deals
```
User: "Find open box deals on headphones"
Claude: I'll find those deals.
- Navigate to headphones
- Filter by Open Box condition
- List available deals
- Note savings percentage
```

### Example 4: Track Order
```
User: "Where is my Best Buy order?"
Claude: I'll check your order.
- Navigate to Order Status
- Find recent order
- Check shipping info
- Report delivery status
```

## Authentication Flow
1. Navigate to bestbuy.com via Playwright MCP
2. Click Account > Sign In
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
- **Open Box Sold**: Limited availability
- **Store Not Found**: Verify zip code
- **Order Not Found**: Check order number
- **Comparison Failed**: Check product compatibility

## Self-Improvement Instructions
When encountering new Best Buy features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Best Buy changes

## Notes
- My Best Buy rewards program
- Totaltech membership for benefits
- Open Box has condition ratings
- Price match available
- In-store pickup option
- Geek Squad services available
- Magnolia for premium audio/video
