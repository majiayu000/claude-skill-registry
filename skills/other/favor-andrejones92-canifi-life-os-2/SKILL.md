---
name: favor
description: Enables Claude to browse restaurants and track deliveries on Favor (Texas)
version: 1.0.0
author: Canifi
category: food
---

# Favor Skill

## Overview
Automates Favor operations including restaurant browsing, favorites management, and delivery tracking in Texas markets through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/favor/install.sh | bash
```

Or manually:
```bash
cp -r skills/favor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FAVOR_EMAIL "your-email@example.com"
canifi-env set FAVOR_PASSWORD "your-password"
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
- Browse restaurants and stores
- Search for food and items
- Track active deliveries
- View order history
- Manage favorites
- Check delivery areas
- View Runner location
- Access reorder options

## Usage Examples

### Example 1: Browse Restaurants
```
User: "Find BBQ restaurants on Favor"
Claude: I'll find BBQ options.
- Navigate to favordelivery.com
- Search "BBQ"
- Filter by available
- Present options
```

### Example 2: Track Delivery
```
User: "Track my Favor order"
Claude: I'll track your delivery.
- Navigate to orders
- Find active order
- Check Runner status
- Report ETA
```

### Example 3: Browse Stores
```
User: "What stores deliver on Favor?"
Claude: I'll find stores.
- Navigate to store section
- List available stores
- Check delivery times
- Present options
```

### Example 4: View History
```
User: "Show my recent Favor orders"
Claude: I'll check your history.
- Navigate to order history
- List recent orders
- Show restaurants and dates
- Present summary
```

## Authentication Flow
1. Navigate to favordelivery.com via Playwright MCP
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
- **Area Not Covered**: Texas markets only
- **Restaurant Closed**: Note hours
- **Order Not Found**: Check order ID
- **Runner Unavailable**: May be busy period
- **Address Error**: Verify delivery address

## Self-Improvement Instructions
When encountering new Favor features:
1. Document new UI elements
2. Add support for new features
3. Log successful patterns
4. Update for Favor changes

## Notes
- Owned by H-E-B (Texas grocery)
- Texas-only service
- Orders not automated for security
- Runners are independent
- "Anything delivered" concept
- H-E-B grocery integration
- Local Texas businesses featured
