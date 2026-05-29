---
name: mdlive
description: Access telehealth with MDLIVE - view visit history, check providers, and manage healthcare account
category: healthcare
---

# MDLIVE Skill

## Overview
Enables Claude to use MDLIVE for telehealth services including viewing visit history, checking available providers, and managing account information.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/mdlive/install.sh | bash
```

Or manually:
```bash
cp -r skills/mdlive ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MDLIVE_EMAIL "your-email@example.com"
canifi-env set MDLIVE_PASSWORD "your-password"
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
- View visit history
- Check provider availability
- Access visit summaries
- View prescription history
- Check service eligibility
- Manage account profile

## Usage Examples

### Example 1: View Visit History
```
User: "Show me my past MDLIVE visits"
Claude: I'll check your visit history.
1. Opening MDLIVE via Playwright MCP
2. Accessing visit history
3. Listing past consultations
4. Summarizing visit types
```

### Example 2: Check Provider Types
```
User: "What specialists are available on MDLIVE?"
Claude: I'll check available specialists.
1. Navigating to providers section
2. Viewing specialty options
3. Listing available types
4. Noting coverage details
```

### Example 3: View Prescriptions
```
User: "What prescriptions have I received from MDLIVE?"
Claude: I'll check prescription history.
1. Accessing prescriptions section
2. Listing past prescriptions
3. Showing dates and details
4. Noting pharmacy info
```

## Authentication Flow
1. Navigate to mdlive.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle 2FA if required (via iMessage)
5. Maintain session for account access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Provider Unavailable**: Show alternative times
- **Coverage Error**: Verify insurance

## Self-Improvement Instructions
When MDLIVE updates:
1. Document new care services
2. Update provider categories
3. Track platform changes
4. Log integration updates

## Notes
- Part of Cigna health services
- Multiple care specialties
- Behavioral health available
- Prescription services
- Insurance integration
