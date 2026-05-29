---
name: target
description: Enables Claude to browse Target products, manage lists, and track orders
version: 1.0.0
author: Canifi
category: ecommerce
---

# Target Skill

## Overview
Automates Target operations including product search, list management, Circle deals, and order tracking through browser automation. Note: Actual purchases are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/target/install.sh | bash
```

Or manually:
```bash
cp -r skills/target ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TARGET_EMAIL "your-email@example.com"
canifi-env set TARGET_PASSWORD "your-password"
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
- Access Target Circle deals
- View weekly ad
- Manage pickup preferences
- Check RedCard benefits

## Usage Examples

### Example 1: Search Products
```
User: "Find throw blankets at Target"
Claude: I'll search for throw blankets.
- Navigate to target.com
- Search "throw blanket"
- Apply filters if requested
- Sort by rating or price
- Present top options
```

### Example 2: Check Circle Deals
```
User: "What Target Circle deals are available?"
Claude: I'll check Circle deals.
- Navigate to Circle section
- Browse available offers
- List relevant deals
- Note expiration dates
```

### Example 3: Check Store Pickup
```
User: "Can I pick this up at my Target today?"
Claude: I'll check availability.
- Navigate to product page
- Check same-day pickup
- View local store inventory
- Report pickup window
```

### Example 4: Track Order
```
User: "Track my Target order"
Claude: I'll check your order.
- Navigate to Orders
- Find recent order
- Check delivery/pickup status
- Report tracking info
```

## Authentication Flow
1. Navigate to target.com via Playwright MCP
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
- **Out of Stock**: Check other stores
- **Circle Expired**: Note expired offers
- **Store Not Found**: Verify zip code
- **Order Not Found**: Check order number
- **Pickup Unavailable**: Suggest shipping

## Self-Improvement Instructions
When encountering new Target features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Target changes

## Notes
- Target Circle is free loyalty program
- RedCard gives 5% discount
- Drive Up for contactless pickup
- Same-day delivery available
- Weekly ad changes Sunday
- Price match within 14 days
- Gift registry available
