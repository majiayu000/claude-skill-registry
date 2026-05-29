---
name: bubble
description: Build web applications with Bubble - create no-code apps with databases, workflows, and complex logic
category: productivity
---

# Bubble Skill

## Overview
Enables Claude to use Bubble for no-code web application development including managing data, configuring workflows, updating designs, and deploying applications.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bubble/install.sh | bash
```

Or manually:
```bash
cp -r skills/bubble ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BUBBLE_EMAIL "your-email@example.com"
canifi-env set BUBBLE_PASSWORD "your-password"
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
- Edit application pages and elements
- Manage database records
- Configure workflows and logic
- View application logs and analytics
- Deploy to development and production
- Manage user data and settings

## Usage Examples

### Example 1: Update Database
```
User: "Add a new user role to my Bubble app database"
Claude: I'll add the new role.
1. Opening Bubble via Playwright MCP
2. Navigating to your app's data tab
3. Opening the User data type
4. Adding new field for role
5. Saving database changes
```

### Example 2: Deploy to Production
```
User: "Deploy my app changes to live"
Claude: I'll deploy your application.
1. Opening your Bubble app
2. Clicking deployment menu
3. Selecting deploy to live
4. Confirming deployment
5. Verifying live app is updated
```

### Example 3: Check App Logs
```
User: "Show me recent error logs from my app"
Claude: I'll retrieve error logs.
1. Opening your Bubble app
2. Navigating to logs section
3. Filtering for errors
4. Listing recent issues
5. Summarizing error patterns
```

## Authentication Flow
1. Navigate to bubble.io via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Deploy Failed**: Check for workflow errors
- **Database Error**: Verify data type constraints

## Self-Improvement Instructions
When Bubble updates:
1. Document new element types
2. Update workflow action patterns
3. Track database feature changes
4. Log plugin integration updates

## Notes
- Bubble is powerful but has learning curve
- Performance depends on app optimization
- Plugins extend functionality
- Separate dev and live environments
- API connector for external services
