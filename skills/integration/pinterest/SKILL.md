---
name: pinterest
description: Enables Claude to manage Pinterest pins, boards, and visual content discovery
version: 1.0.0
author: Canifi
category: social
---

# Pinterest Skill

## Overview
Automates Pinterest operations including creating pins, managing boards, discovering content, and analyzing engagement through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pinterest/install.sh | bash
```

Or manually:
```bash
cp -r skills/pinterest ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PINTEREST_EMAIL "your-email@example.com"
canifi-env set PINTEREST_PASSWORD "your-password"
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
- Create and publish pins
- Create and organize boards
- Save pins to boards
- Follow accounts and boards
- Search for inspiration
- Access analytics (business accounts)
- Schedule pins
- Manage pin descriptions and links

## Usage Examples

### Example 1: Create a Pin
```
User: "Pin this image to my Travel board"
Claude: I'll create that pin.
- Navigate to pinterest.com
- Click Create > Create Pin
- Upload image
- Add title and description
- Select Travel board
- Publish pin
```

### Example 2: Create New Board
```
User: "Create a Pinterest board called 'Home Decor Ideas'"
Claude: I'll create that board.
- Navigate to profile
- Click Create board
- Name it "Home Decor Ideas"
- Set visibility (public/secret)
- Confirm creation
```

### Example 3: Search and Save
```
User: "Find and save recipe pins to my Recipes board"
Claude: I'll find recipe pins.
- Search for recipes
- Browse results
- Save interesting pins to Recipes board
- Confirm pins saved
```

### Example 4: Check Pin Performance
```
User: "Show me how my pins performed this week"
Claude: I'll check your analytics.
- Navigate to Analytics section
- Gather impressions and engagement
- List top performing pins
- Present weekly summary
```

## Authentication Flow
1. Navigate to pinterest.com via Playwright MCP
2. Enter email and password from canifi-env
3. Handle 2FA if enabled (notify user via iMessage)
4. Verify home feed access
5. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **2FA Required**: iMessage for verification code
- **Pin Failed**: Check image format and size
- **Board Not Found**: List available boards
- **Rate Limited**: Implement backoff
- **Content Blocked**: Check community guidelines
- **Link Invalid**: Verify destination URL

## Self-Improvement Instructions
When encountering new Pinterest features:
1. Document new UI elements
2. Add support for new pin types
3. Log successful pinning patterns
4. Update for Pinterest changes

## Notes
- Business accounts have analytics
- Rich Pins require setup
- Idea Pins are different from standard
- Scheduling requires business account
- SEO important for pin discovery
- Video pins have different specs
- Shop features for ecommerce
