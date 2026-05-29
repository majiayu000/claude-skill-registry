---
name: hashnode
description: Enables Claude to manage Hashnode blog posts, engagement, and developer community participation
version: 1.0.0
author: Canifi
category: productivity
---

# Hashnode Skill

## Overview
Automates Hashnode operations including publishing blog posts, managing your publication, engaging with content, and participating in the developer blogging community through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hashnode/install.sh | bash
```

Or manually:
```bash
cp -r skills/hashnode ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HASHNODE_EMAIL "your-email@example.com"
canifi-env set HASHNODE_PASSWORD "your-password"
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
- Write and publish articles
- Manage personal publication
- React to and comment on posts
- Follow users and blogs
- Search content and tags
- Access drafts and scheduled posts
- View analytics
- Manage blog settings

## Usage Examples

### Example 1: Publish Article
```
User: "Publish this tutorial to my Hashnode blog"
Claude: I'll publish that article.
- Navigate to hashnode.com
- Access blog dashboard
- Click Write Article
- Enter content with markdown
- Add tags and cover image
- Publish article
```

### Example 2: React to Post
```
User: "Like that article about web development"
Claude: I'll add a reaction.
- Navigate to article
- Click like/reaction button
- Confirm reaction added
```

### Example 3: Schedule Post
```
User: "Schedule this article for tomorrow morning"
Claude: I'll schedule that post.
- Create article in editor
- Set schedule date/time
- Save as scheduled
- Confirm scheduling
```

### Example 4: Check Analytics
```
User: "Show me my Hashnode blog analytics"
Claude: I'll pull your analytics.
- Navigate to dashboard
- Access Analytics section
- Gather views and reactions
- Present performance summary
```

## Authentication Flow
1. Navigate to hashnode.com via Playwright MCP
2. Click login and select email option
3. Enter email and password from canifi-env
4. Handle magic link if used (check email)
5. Verify dashboard access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Check for magic link email
- **Session Expired**: Re-authenticate automatically
- **Article Failed**: Check markdown syntax
- **Rate Limited**: Wait before continuing
- **Blog Not Setup**: Guide user to create publication
- **Tag Not Found**: Create or suggest alternatives
- **Image Upload Failed**: Check format and size
- **Scheduling Failed**: Verify date/time format

## Self-Improvement Instructions
When encountering new Hashnode features:
1. Document new editor elements
2. Add support for new blog features
3. Log successful publishing patterns
4. Update for platform changes

## Notes
- Hashnode provides custom domain support
- Publications are individual blogs
- Tags help with SEO
- Newsletter integration available
- GitHub backup supported
- Series for multi-part content
- Headless CMS capabilities
