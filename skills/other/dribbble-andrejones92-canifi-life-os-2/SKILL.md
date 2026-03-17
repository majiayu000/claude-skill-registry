---
name: dribbble
description: Discover and share design work on Dribbble - browse design inspiration, manage portfolio, and find designers
category: design
---

# Dribbble Skill

## Overview
Enables Claude to interact with Dribbble for design inspiration, portfolio management, and designer discovery including browsing shots, saving collections, and managing design uploads.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/dribbble/install.sh | bash
```

Or manually:
```bash
cp -r skills/dribbble ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DRIBBBLE_EMAIL "your-email@example.com"
canifi-env set DRIBBBLE_PASSWORD "your-password"
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
- Browse and search design shots
- Save designs to collections/buckets
- View designer profiles and portfolios
- Manage uploaded shots and projects
- Follow designers and teams
- Search for design jobs and freelance work

## Usage Examples

### Example 1: Find Design Inspiration
```
User: "Find mobile app UI inspiration for a fitness app"
Claude: I'll search for fitness app designs on Dribbble.
1. Opening Dribbble via Playwright MCP
2. Searching for "fitness app mobile UI"
3. Browsing top-rated shots
4. Saving relevant designs to a collection
5. Compiling inspiration summary with links
```

### Example 2: Review Portfolio
```
User: "Show me my Dribbble portfolio analytics"
Claude: I'll pull up your portfolio stats.
1. Navigating to your Dribbble profile
2. Accessing shot analytics
3. Reviewing views, likes, and saves
4. Summarizing performance trends
```

### Example 3: Find Designers
```
User: "Find UI designers available for freelance work"
Claude: I'll search for available designers.
1. Accessing Dribbble Pro/Hiring section
2. Filtering for UI designers
3. Filtering by availability status
4. Compiling list of potential candidates
```

## Authentication Flow
1. Navigate to dribbble.com via Playwright MCP
2. Click "Sign in" and enter credentials
3. Handle 2FA if enabled (via iMessage)
4. Maintain session cookies
5. Handle Pro features if subscribed

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement backoff for API-like actions
- **2FA Required**: Send iMessage notification
- **Search Failed**: Try alternative search terms
- **Profile Not Found**: Verify username or prompt user

## Self-Improvement Instructions
When Dribbble updates features:
1. Document new search filters and options
2. Update navigation patterns for shots
3. Track any changes to profile layouts
4. Log new portfolio features

## Notes
- Pro features require Dribbble Pro subscription
- Shot uploads have quality and format requirements
- Hiring features may have additional verification
- Collection limits vary by account type
- Some features are member-only
