---
name: framer
description: Design and publish websites with Framer - create interactive sites, manage projects, and publish directly
category: design
---

# Framer Skill

## Overview
Enables Claude to use Framer for website design and development including creating pages, managing components, configuring settings, and publishing sites.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/framer/install.sh | bash
```

Or manually:
```bash
cp -r skills/framer ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FRAMER_EMAIL "your-email@example.com"
canifi-env set FRAMER_PASSWORD "your-password"
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
- Create and edit website pages
- Manage design components
- Configure site settings and SEO
- View and respond to form submissions
- Publish sites to live URLs
- Access analytics and performance data

## Usage Examples

### Example 1: Update Page Content
```
User: "Update the homepage hero text on my Framer site"
Claude: I'll update your hero section.
1. Opening Framer via Playwright MCP
2. Navigating to your project
3. Selecting the homepage
4. Editing the hero text component
5. Publishing the changes
```

### Example 2: Check Form Submissions
```
User: "Show me recent contact form submissions"
Claude: I'll retrieve your form data.
1. Opening your Framer project
2. Navigating to forms section
3. Accessing contact form submissions
4. Listing recent entries with details
```

### Example 3: Publish Site Updates
```
User: "Publish my site changes to production"
Claude: I'll publish your updates.
1. Opening the Framer project
2. Reviewing pending changes
3. Clicking publish button
4. Confirming deployment
5. Verifying live site is updated
```

## Authentication Flow
1. Navigate to framer.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Publish Failed**: Check for errors and retry
- **Component Error**: Debug and fix before publish

## Self-Improvement Instructions
When Framer updates:
1. Document new design capabilities
2. Update component creation workflows
3. Track publishing process changes
4. Log new integration features

## Notes
- Framer combines design and development
- Code components use React
- Custom domains require paid plans
- CMS features available for dynamic content
- Sites can be exported as code
