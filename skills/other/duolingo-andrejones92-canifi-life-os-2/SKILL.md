---
name: duolingo
description: Track Duolingo language learning progress and maintain streaks
category: education
---

# Duolingo Skill

## Overview
Enables Claude to interact with Duolingo for tracking language learning progress, maintaining daily streaks, reviewing lesson history, and monitoring XP and league status.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/duolingo/install.sh | bash
```

Or manually:
```bash
cp -r skills/duolingo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DUOLINGO_EMAIL "your-email@example.com"
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
- Track language learning progress
- Monitor daily streak status
- View XP and league standings
- Check lesson completion history
- Review learned words and skills

## Usage Examples
### Example 1: Streak Check
```
User: "What's my Duolingo streak?"
Claude: I'll check your current streak and daily goal status.
```

### Example 2: Progress Overview
```
User: "How's my Spanish learning going?"
Claude: I'll review your Spanish course progress and recent lessons.
```

### Example 3: League Status
```
User: "What's my position in the Duolingo league?"
Claude: I'll check your current league standing and XP this week.
```

## Authentication Flow
1. Navigate to duolingo.com via Playwright MCP
2. Click "I already have an account"
3. Enter Duolingo credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Streak Freeze: Check streak protection status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Duolingo interface changes
2. Update selectors for new layouts
3. Track new language additions
4. Monitor gamification features

## Notes
- Daily streaks for motivation
- Leagues for competitive learning
- Hearts system limits mistakes
- Duolingo Plus removes ads and adds features
