---
name: blueapron
description: Enables Claude to browse Blue Apron meal kits and manage subscriptions
version: 1.0.0
author: Canifi
category: food
---

# Blue Apron Skill

## Overview
Automates Blue Apron operations including meal selection, wine pairings, and subscription management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/blueapron/install.sh | bash
```

Or manually:
```bash
cp -r skills/blueapron ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BLUEAPRON_EMAIL "your-email@example.com"
canifi-env set BLUEAPRON_PASSWORD "your-password"
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
- Browse weekly recipes
- View cooking instructions
- Select meals for box
- Track deliveries
- View order history
- Manage wine subscription
- Customize preferences
- Skip or pause weeks

## Usage Examples

### Example 1: Browse Recipes
```
User: "What recipes are on Blue Apron this week?"
Claude: I'll check the menu.
- Navigate to blueapron.com
- View weekly recipes
- List available dishes
- Present cooking times
```

### Example 2: View Recipe Details
```
User: "Show me how to make the salmon dish"
Claude: I'll get the recipe.
- Find salmon recipe
- View ingredients list
- Show step-by-step instructions
- Present cooking tips
```

### Example 3: Track Delivery
```
User: "When is my Blue Apron arriving?"
Claude: I'll check your delivery.
- Navigate to orders
- Find upcoming delivery
- Check shipping status
- Report arrival date
```

### Example 4: Check Wine Pairing
```
User: "What wine pairs with my meals this week?"
Claude: I'll check wine options.
- Navigate to wine section
- View pairing suggestions
- List recommended wines
- Present options
```

## Authentication Flow
1. Navigate to blueapron.com via Playwright MCP
2. Click Log In
3. Enter email from canifi-env
4. Enter password
5. Handle 2FA if enabled (notify user via iMessage)
6. Verify account access
7. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Selection Deadline**: Note cutoff time
- **Recipe Unavailable**: Check alternatives
- **Delivery Issue**: Check address
- **Wine Age Verify**: May need verification
- **Subscription Paused**: Check status

## Self-Improvement Instructions
When encountering new Blue Apron features:
1. Document new UI elements
2. Add support for new recipe types
3. Log successful patterns
4. Update for Blue Apron changes

## Notes
- Subscription meal kit service
- Orders not automated for security
- Wine service requires age verification
- Chef-designed recipes
- Weekly selection deadline
- Can skip or pause
- Premium ingredients included
