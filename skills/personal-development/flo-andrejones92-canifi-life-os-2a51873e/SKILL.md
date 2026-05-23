---
name: flo
description: Track menstrual health with Flo - monitor cycles, symptoms, and reproductive health
category: health
---

# Flo Skill

## Overview
Enables Claude to use Flo for menstrual and reproductive health tracking including viewing cycle predictions, logging symptoms, and accessing health insights.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/flo/install.sh | bash
```

Or manually:
```bash
cp -r skills/flo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FLO_EMAIL "your-email@example.com"
canifi-env set FLO_PASSWORD "your-password"
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
- View cycle predictions
- Check period history
- Access symptom logging
- View health insights
- Check fertility window
- Access daily content

## Usage Examples

### Example 1: Check Cycle Prediction
```
User: "When is my next period expected?"
Claude: I'll check your prediction.
1. Opening Flo via Playwright MCP
2. Accessing calendar view
3. Finding next predicted period
4. Reporting expected dates
```

### Example 2: View Symptom History
```
User: "What symptoms did I log last month?"
Claude: I'll review your symptoms.
1. Accessing symptom history
2. Filtering to last month
3. Listing logged symptoms
4. Identifying patterns
```

### Example 3: Check Insights
```
User: "What health insights does Flo have for me?"
Claude: I'll find your insights.
1. Navigating to insights section
2. Viewing personalized content
3. Summarizing key insights
4. Noting recommendations
```

## Authentication Flow
1. Navigate to flo.health via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for data access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Data Unavailable**: Check logging history
- **Prediction Error**: Note data requirements

## Self-Improvement Instructions
When Flo updates:
1. Document new tracking options
2. Update prediction features
3. Track content additions
4. Log privacy feature changes

## Notes
- Sensitive health data
- AI-powered predictions
- Daily health content
- Premium features available
- Privacy-focused options
