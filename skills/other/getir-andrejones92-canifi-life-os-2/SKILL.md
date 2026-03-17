---
name: getir
description: Enables Claude to browse Getir products and track ultra-fast deliveries
version: 1.0.0
author: Canifi
category: food
---

# Getir Skill

## Overview
Automates Getir operations including convenience product browsing, favorites management, and delivery tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/getir/install.sh | bash
```

Or manually:
```bash
cp -r skills/getir ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GETIR_EMAIL "your-email@example.com"
canifi-env set GETIR_PASSWORD "your-password"
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
- Browse convenience products
- Search for items
- Track ultra-fast deliveries
- View order history
- Manage favorites
- Check promotions
- View category selections
- Access quick reorder

## Usage Examples

### Example 1: Browse Products
```
User: "What's available on Getir?"
Claude: I'll browse products.
- Navigate to getir.com
- View categories
- List available items
- Present options
```

### Example 2: Find Snacks
```
User: "Find chips on Getir"
Claude: I'll search for chips.
- Search "chips"
- Show available options
- Note prices
- Present results
```

### Example 3: Track Order
```
User: "Track my Getir delivery"
Claude: I'll track your order.
- Navigate to orders
- Find active order
- Check delivery status
- Report ETA (usually 10-15 min)
```

### Example 4: Check Deals
```
User: "What deals are on Getir?"
Claude: I'll find deals.
- Navigate to promotions
- Browse current offers
- List discounts
- Present savings
```

## Authentication Flow
1. Navigate to getir.com via Playwright MCP
2. Click Sign In
3. Enter phone or email from canifi-env
4. Enter password or OTP
5. Handle verification if needed (notify user)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **OTP Required**: iMessage for code
- **Area Not Covered**: Check service area
- **Item Unavailable**: Check alternatives
- **Order Not Found**: Check order ID
- **Delivery Delayed**: Note updated ETA
- **App Required**: Some features mobile-only

## Self-Improvement Instructions
When encountering new Getir features:
1. Document new UI elements
2. Add support for new categories
3. Log successful patterns
4. Update for Getir changes

## Notes
- Ultra-fast delivery (10-15 min)
- Orders not automated for security
- Limited service areas
- Operating own dark stores
- 24/7 in many areas
- Competitive with Gopuff
- Founded in Turkey
