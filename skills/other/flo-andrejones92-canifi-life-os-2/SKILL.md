---
name: webflow
description: Build professional websites with Webflow - design, develop, and publish responsive sites with visual tools
category: design
---

# Webflow Skill

## Overview
Enables Claude to use Webflow for professional website creation including designing pages, managing CMS content, configuring site settings, and publishing to production.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/webflow/install.sh | bash
```

Or manually:
```bash
cp -r skills/webflow ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WEBFLOW_EMAIL "your-email@example.com"
canifi-env set WEBFLOW_PASSWORD "your-password"
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
- Design and edit website pages
- Manage CMS collections and content
- Configure site settings and SEO
- Handle form submissions
- Publish sites and staging versions
- Access e-commerce features

## Usage Examples

### Example 1: Add Blog Post
```
User: "Add a new blog post to my Webflow site"
Claude: I'll create a new blog post.
1. Opening Webflow via Playwright MCP
2. Navigating to your project's CMS
3. Opening Blog Posts collection
4. Creating new item with content
5. Publishing the changes
```

### Example 2: Update Product Info
```
User: "Update the pricing on our premium plan page"
Claude: I'll update the pricing.
1. Opening your Webflow project
2. Navigating to the pricing page
3. Editing the premium plan component
4. Updating price values
5. Publishing to live site
```

### Example 3: Check Form Submissions
```
User: "Show me contact form leads from this week"
Claude: I'll retrieve this week's leads.
1. Accessing Webflow site settings
2. Opening forms section
3. Filtering to this week's submissions
4. Compiling lead information
```

## Authentication Flow
1. Navigate to webflow.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password
4. Handle Google SSO if configured
5. Complete 2FA if required (via iMessage)

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Publish Failed**: Check validation errors
- **CMS Error**: Verify collection structure

## Self-Improvement Instructions
When Webflow updates:
1. Document new design features
2. Update CMS management workflows
3. Track editor interface changes
4. Log e-commerce feature updates

## Notes
- Webflow generates clean, production-ready code
- CMS has item and collection limits by plan
- Custom code can be added to pages
- E-commerce requires specific plans
- Staging URLs available for preview
