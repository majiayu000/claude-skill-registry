---
name: hellofresh
description: Enables Claude to browse HelloFresh meal kits and manage subscriptions
version: 1.0.0
author: Canifi
category: food
---

# HelloFresh Skill

## Overview
Automates HelloFresh operations including meal selection, box management, and delivery tracking through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hellofresh/install.sh | bash
```

Or manually:
```bash
cp -r skills/hellofresh ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HELLOFRESH_EMAIL "your-email@example.com"
canifi-env set HELLOFRESH_PASSWORD "your-password"
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
- Browse weekly meal options
- View recipe details
- Manage box selections
- Track deliveries
- View order history
- Customize meal plan
- Manage subscription
- Skip or pause weeks

## Usage Examples

### Example 1: Browse Meals
```
User: "What meals are available on HelloFresh this week?"
Claude: I'll check this week's menu.
- Navigate to hellofresh.com
- View weekly menu
- List available recipes
- Present meal options
```

### Example 2: View Recipe
```
User: "Show me the recipe details for the chicken dish"
Claude: I'll get the recipe.
- Find chicken recipe
- View ingredients
- Show cooking steps
- Present nutritional info
```

### Example 3: Track Delivery
```
User: "When will my HelloFresh box arrive?"
Claude: I'll check your delivery.
- Navigate to deliveries
- Find upcoming box
- Check tracking status
- Report delivery date
```

### Example 4: Check Subscription
```
User: "What's my HelloFresh plan status?"
Claude: I'll check your subscription.
- Navigate to account
- View plan details
- Check meals per week
- Present subscription info
```

## Authentication Flow
1. Navigate to hellofresh.com via Playwright MCP
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
- **Selection Deadline Passed**: Note cutoff
- **Meal Unavailable**: Check alternatives
- **Delivery Issue**: Check address and date
- **Subscription Paused**: Reactivate if needed
- **Order Not Found**: Check delivery date

## Self-Improvement Instructions
When encountering new HelloFresh features:
1. Document new UI elements
2. Add support for new meal types
3. Log successful patterns
4. Update for HelloFresh changes

## Notes
- Subscription meal kit service
- Orders not automated for security
- Weekly selection deadline
- Recipe cards included
- Various plan sizes available
- Can skip weeks
- Green Chef is sister brand
