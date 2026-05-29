---
name: postmates
description: Enables Claude to browse merchants and track deliveries on Postmates (now part of Uber Eats)
version: 1.0.0
author: Canifi
category: food
---

# Postmates Skill

## Overview
Automates Postmates operations including merchant browsing and order tracking through Uber Eats integration. Note: Postmates has merged with Uber Eats, so most functionality redirects there. Actual orders are not automated.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/postmates/install.sh | bash
```

Or manually:
```bash
cp -r skills/postmates ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set POSTMATES_EMAIL "your-email@example.com"
canifi-env set POSTMATES_PASSWORD "your-password"
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
- Search for items
- Track active orders
- View order history
- Access via Uber Eats
- Find delivery options
- Check merchant hours
- View past favorites

## Usage Examples

### Example 1: Browse Merchants
```
User: "Find stores delivering on Postmates"
Claude: I'll find delivery options.
- Navigate to Uber Eats (Postmates merged)
- Browse available stores
- Check delivery times
- Present options
```

### Example 2: Track Order
```
User: "Track my Postmates order"
Claude: I'll track your delivery.
- Navigate to orders (via Uber Eats)
- Find active order
- Check delivery status
- Report ETA
```

### Example 3: Search Items
```
User: "Find who delivers ice cream nearby"
Claude: I'll search for that.
- Search "ice cream"
- Filter by delivery
- Show available stores
- Present options
```

### Example 4: View History
```
User: "Show my past Postmates orders"
Claude: I'll check your history.
- Navigate to order history
- List past orders
- Show merchants and dates
- Present summary
```

## Authentication Flow
1. Navigate to postmates.com (redirects to Uber Eats) via Playwright MCP
2. Sign in with Uber/Postmates account
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Use Uber Eats credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Redirect to Uber Eats**: Expected behavior
- **Store Closed**: Note hours
- **Order Not Found**: Check Uber Eats orders
- **Legacy Account**: May need migration
- **Address Error**: Verify delivery address

## Self-Improvement Instructions
When encountering Postmates/Uber Eats changes:
1. Document redirect patterns
2. Update for Uber Eats integration
3. Log successful patterns
4. Note deprecated features

## Notes
- Postmates merged with Uber Eats in 2020
- Legacy accounts migrated to Uber
- Use Uber Eats for new orders
- Fleet remains for merchants
- Some branding may still appear
- History accessible via Uber Eats
- Orders not automated for security
