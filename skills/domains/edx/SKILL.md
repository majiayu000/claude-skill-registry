---
name: edx
description: Access edX university courses, MicroMasters, and professional certificates
category: education
---

# edX Skill

## Overview
Enables Claude to interact with edX for accessing university courses from top institutions, tracking learning progress, and earning verified certificates and credentials.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/edx/install.sh | bash
```

Or manually:
```bash
cp -r skills/edx ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set EDX_EMAIL "your-email@example.com"
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
- Browse courses from top universities
- Track course progress and deadlines
- Access MicroMasters programs
- Earn verified certificates
- Follow executive education programs

## Usage Examples
### Example 1: Find Courses
```
User: "Find computer science courses from MIT on edX"
Claude: I'll search for MIT computer science courses on edX.
```

### Example 2: Course Progress
```
User: "What's my progress in the Harvard CS50 course?"
Claude: I'll check your progress in CS50 on edX.
```

### Example 3: Certificates
```
User: "What edX certificates have I earned?"
Claude: I'll list your completed and verified certificates.
```

## Authentication Flow
1. Navigate to edx.org via Playwright MCP
2. Click "Sign In" button
3. Enter edX credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Certificate Fee: Check verified track enrollment

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document edX interface changes
2. Update selectors for new layouts
3. Track new course and program additions
4. Monitor credential requirements

## Notes
- Founded by MIT and Harvard
- Audit mode for free access
- Verified certificates for fee
- MicroMasters for graduate credit
