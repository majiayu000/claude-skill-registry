---
name: lose-it
description: Track calories with Lose It! - log food, track weight, and monitor nutrition goals
category: health
---

# Lose It! Skill

## Overview
Enables Claude to use Lose It! for calorie and weight tracking including viewing food logs, monitoring weight trends, and checking nutrition goals.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/lose-it/install.sh | bash
```

Or manually:
```bash
cp -r skills/lose-it ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LOSEIT_EMAIL "your-email@example.com"
canifi-env set LOSEIT_PASSWORD "your-password"
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
- View food diary
- Check calorie budget
- Track weight progress
- View nutrition breakdown
- Access meal history
- Check exercise logging

## Usage Examples

### Example 1: Check Calorie Budget
```
User: "How many calories do I have left today?"
Claude: I'll check your budget.
1. Opening Lose It! via Playwright MCP
2. Accessing today's diary
3. Viewing calorie total
4. Calculating remaining
5. Reporting budget status
```

### Example 2: View Weight Trend
```
User: "How's my weight trending this month?"
Claude: I'll analyze your weight trend.
1. Accessing weight section
2. Viewing monthly data
3. Calculating trend
4. Comparing to goal
```

### Example 3: Check Meal Breakdown
```
User: "What did I eat for lunch this week?"
Claude: I'll review your lunches.
1. Accessing food diary
2. Filtering to lunch meals
3. Listing this week's entries
4. Summarizing patterns
```

## Authentication Flow
1. Navigate to loseit.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for diary access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Data Unavailable**: Check for logged entries
- **Sync Error**: Refresh and retry

## Self-Improvement Instructions
When Lose It! updates:
1. Document new tracking features
2. Update food database changes
3. Track premium feature updates
4. Log interface modifications

## Notes
- Calorie-focused approach
- Large food database
- Barcode scanning on mobile
- Premium for detailed nutrients
- Device integrations available
