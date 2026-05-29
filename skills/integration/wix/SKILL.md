---
name: wix
description: Build websites easily with Wix - create, edit, and manage websites using drag-and-drop tools and templates
category: productivity
---

# Wix Skill

## Overview
Enables Claude to use Wix for website creation and management including editing pages, managing content, configuring business tools, and publishing updates.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wix/install.sh | bash
```

Or manually:
```bash
cp -r skills/wix ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WIX_EMAIL "your-email@example.com"
canifi-env set WIX_PASSWORD "your-password"
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
- Edit website pages and content
- Manage blog posts and articles
- Configure business features (bookings, stores)
- Handle contact form submissions
- Publish site updates
- Access site analytics

## Usage Examples

### Example 1: Update Business Hours
```
User: "Update my business hours on my Wix site"
Claude: I'll update your business hours.
1. Opening Wix via Playwright MCP
2. Navigating to your site dashboard
3. Accessing business info settings
4. Updating hours of operation
5. Publishing the changes
```

### Example 2: Add Blog Post
```
User: "Create a new blog post about our latest product"
Claude: I'll create a blog post.
1. Opening Wix blog manager
2. Creating new post
3. Adding title, content, and images
4. Setting categories and SEO
5. Publishing the article
```

### Example 3: Check Bookings
```
User: "Show me this week's appointment bookings"
Claude: I'll retrieve your bookings.
1. Opening Wix Bookings dashboard
2. Filtering to this week's appointments
3. Listing all scheduled sessions
4. Summarizing booking details
```

## Authentication Flow
1. Navigate to wix.com via Playwright MCP
2. Click "Log In" and enter email
3. Enter password
4. Handle Google/SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Publish Failed**: Check for errors
- **Feature Unavailable**: Suggest plan upgrade

## Self-Improvement Instructions
When Wix updates:
1. Document new editor features
2. Update business tool workflows
3. Track dashboard changes
4. Log new app integrations

## Notes
- Wix has many built-in business apps
- Advanced features require premium plans
- Editor uses visual drag-and-drop
- Mobile editor separate from desktop
- Velo (code) available for developers
