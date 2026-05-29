---
name: skillshare
description: Access Skillshare creative classes and track learning progress
category: education
---

# Skillshare Skill

## Overview
Enables Claude to interact with Skillshare for browsing creative classes, tracking learning progress, managing saved classes, and discovering new creative skills.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/skillshare/install.sh | bash
```

Or manually:
```bash
cp -r skills/skillshare ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SKILLSHARE_EMAIL "your-email@example.com"
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
- Browse creative and business classes
- Track class completion progress
- Manage saved classes list
- View class projects and discussions
- Discover trending classes

## Usage Examples
### Example 1: Find Classes
```
User: "Find me illustration classes on Skillshare"
Claude: I'll search for top-rated illustration classes on Skillshare.
```

### Example 2: Class Progress
```
User: "What classes am I in the middle of?"
Claude: I'll check your in-progress Skillshare classes.
```

### Example 3: Saved Classes
```
User: "What's in my Skillshare saved list?"
Claude: I'll list all the classes you've saved for later.
```

## Authentication Flow
1. Navigate to skillshare.com via Playwright MCP
2. Click "Sign In" button
3. Enter Skillshare credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Subscription Required: Check membership status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Skillshare interface changes
2. Update selectors for new layouts
3. Track trending class categories
4. Monitor new teacher additions

## Notes
- Subscription-based unlimited access
- Focus on creative and business skills
- Project-based learning approach
- Teacher community platform
