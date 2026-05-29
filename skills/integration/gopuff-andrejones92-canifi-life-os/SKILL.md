---
name: gopuff
description: Enables Claude to browse Gopuff convenience items and track deliveries
version: 1.0.0
author: Canifi
category: food
---

# Gopuff Skill

## Overview
Automates Gopuff operations including convenience item browsing, favorites management, and delivery tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gopuff/install.sh | bash
```

Or manually:
```bash
cp -r skills/gopuff ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOPUFF_EMAIL "your-email@example.com"
canifi-env set GOPUFF_PASSWORD "your-password"
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
- Browse convenience items
- Search for products
- Track active deliveries
- View order history
- Manage favorites
- Check Fam membership
- Find deals and promotions
- View category selections

## Usage Examples

### Example 1: Browse Items
```
User: "What snacks are on Gopuff?"
Claude: I'll browse snacks.
- Navigate to gopuff.com
- Go to snacks category
- Browse available items
- Present options
```

### Example 2: Search Products
```
User: "Find energy drinks on Gopuff"
Claude: I'll search for those.
- Search "energy drinks"
- Show available brands
- Present with prices
- Note any deals
```

### Example 3: Track Order
```
User: "Track my Gopuff delivery"
Claude: I'll track your order.
- Navigate to Orders
- Find active order
- Check delivery status
- Report ETA (often 30 min)
```

### Example 4: Check Deals
```
User: "What's on sale at Gopuff?"
Claude: I'll find deals.
- Navigate to deals section
- Browse promotions
- List discounted items
- Present savings
```

## Authentication Flow
1. Navigate to gopuff.com via Playwright MCP
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
- **Area Not Served**: Check delivery zone
- **Item Unavailable**: May vary by location
- **Order Not Found**: Check order ID
- **Delivery Delayed**: Check status
- **Fam Issue**: Check subscription status

## Self-Improvement Instructions
When encountering new Gopuff features:
1. Document new UI elements
2. Add support for new categories
3. Log successful patterns
4. Update for Gopuff changes

## Notes
- Orders not automated for security
- 30-minute delivery promise
- Gopuff Fam membership for perks
- Operates own warehouses
- 24/7 in many areas
- Alcohol delivery where legal
- Limited to Gopuff service areas
