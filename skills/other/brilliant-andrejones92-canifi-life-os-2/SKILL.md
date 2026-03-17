---
name: brilliant
description: Access Brilliant interactive STEM courses and track problem-solving progress
category: education
---

# Brilliant Skill

## Overview
Enables Claude to interact with Brilliant for accessing interactive STEM courses, solving daily challenges, tracking learning progress, and developing quantitative thinking skills.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/brilliant/install.sh | bash
```

Or manually:
```bash
cp -r skills/brilliant ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BRILLIANT_EMAIL "your-email@example.com"
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
- Browse math, science, and CS courses
- Solve daily challenges
- Track problem-solving progress
- Access interactive lessons
- View streak and achievements

## Usage Examples
### Example 1: Daily Challenge
```
User: "What's today's Brilliant daily challenge?"
Claude: I'll check today's daily problem on Brilliant.
```

### Example 2: Course Progress
```
User: "How far am I in the Logic course?"
Claude: I'll check your progress in the Logic course on Brilliant.
```

### Example 3: Find Courses
```
User: "What math courses does Brilliant have?"
Claude: I'll browse Brilliant's mathematics course offerings.
```

## Authentication Flow
1. Navigate to brilliant.org via Playwright MCP
2. Click "Log in" button
3. Enter Brilliant credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Premium Required: Check subscription for full access

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Brilliant interface changes
2. Update selectors for new layouts
3. Track new course additions
4. Monitor interactive feature updates

## Notes
- Interactive problem-based learning
- Daily challenges for practice
- Premium unlocks all courses
- Focus on STEM subjects
