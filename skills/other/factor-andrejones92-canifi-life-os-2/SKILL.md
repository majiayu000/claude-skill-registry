---
name: factor
description: Enables Claude to browse Factor prepared meals and manage subscriptions
version: 1.0.0
author: Canifi
category: food
---

# Factor Skill

## Overview
Automates Factor operations including prepared meal browsing, box customization, and subscription management through browser automation. Note: Actual orders are not automated for security.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/factor/install.sh | bash
```

Or manually:
```bash
cp -r skills/factor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FACTOR_EMAIL "your-email@example.com"
canifi-env set FACTOR_PASSWORD "your-password"
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
- Browse prepared meals
- View nutritional info
- Customize weekly selections
- Track deliveries
- View order history
- Manage dietary preferences
- Check meal plans
- Skip or pause weeks

## Usage Examples

### Example 1: Browse Meals
```
User: "What meals are available on Factor?"
Claude: I'll check the menu.
- Navigate to factor75.com
- View available meals
- List options by category
- Present with nutrition
```

### Example 2: Check Keto Options
```
User: "Show me keto meals on Factor"
Claude: I'll find keto options.
- Navigate to menu
- Filter by keto
- List keto-friendly meals
- Present macros
```

### Example 3: Track Delivery
```
User: "When is my Factor delivery coming?"
Claude: I'll check your delivery.
- Navigate to orders
- Find upcoming delivery
- Check shipping status
- Report arrival date
```

### Example 4: View Nutrition
```
User: "What are the calories in Factor meals?"
Claude: I'll check nutritional info.
- Browse meal options
- Gather calorie data
- List protein and carbs
- Present nutrition summary
```

## Authentication Flow
1. Navigate to factor75.com via Playwright MCP
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
- **Selection Deadline**: Note cutoff
- **Meal Unavailable**: Check alternatives
- **Delivery Issue**: Check address
- **Plan Issue**: Check subscription status
- **Dietary Filter Error**: Reset filters

## Self-Improvement Instructions
When encountering new Factor features:
1. Document new UI elements
2. Add support for new meal types
3. Log successful patterns
4. Update for Factor changes

## Notes
- Prepared meals, no cooking needed
- Orders not automated for security
- Owned by HelloFresh
- Various dietary plans (keto, paleo, etc.)
- Heat and eat convenience
- Chef-prepared meals
- Weekly selection deadline
