---
name: loom
description: Record and share video messages with Loom - create screen recordings, manage video library, and track viewer engagement
category: video
---

# Loom Skill

## Overview
Enables Claude to manage Loom video content including organizing recordings, accessing video analytics, generating transcripts, and managing sharing settings.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/loom/install.sh | bash
```

Or manually:
```bash
cp -r skills/loom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LOOM_EMAIL "your-email@example.com"
canifi-env set LOOM_PASSWORD "your-password"
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
- Browse and organize video library
- Access video transcripts and captions
- View video analytics and engagement
- Manage video sharing settings
- Create folders and organize content
- Download videos for offline use

## Usage Examples

### Example 1: View Video Analytics
```
User: "Show me the engagement stats for my product demo video"
Claude: I'll pull up your video analytics.
1. Opening Loom via Playwright MCP
2. Navigating to your video library
3. Finding the product demo video
4. Accessing analytics dashboard
5. Summarizing views, watch time, and engagement
```

### Example 2: Get Transcript
```
User: "Get the transcript from my last team update recording"
Claude: I'll retrieve the transcript.
1. Finding your most recent team update
2. Accessing the transcript panel
3. Copying the full transcript text
4. Formatting for readability
```

### Example 3: Organize Videos
```
User: "Create a folder for client presentations and move relevant videos"
Claude: I'll organize your videos.
1. Creating new folder "Client Presentations"
2. Searching for client-related videos
3. Moving selected videos to the folder
4. Confirming organization is complete
```

## Authentication Flow
1. Navigate to loom.com via Playwright MCP
2. Click "Log in" and enter email
3. Enter password or use SSO
4. Handle 2FA if required (via iMessage)
5. Maintain session for library access

## Error Handling
- **Login Failed**: Retry up to 3 times, notify via iMessage
- **Session Expired**: Re-authenticate automatically
- **Rate Limited**: Implement exponential backoff
- **2FA Required**: Send iMessage notification
- **Video Not Found**: Search library or check sharing
- **Transcript Unavailable**: Wait for processing or notify user

## Self-Improvement Instructions
When Loom updates its platform:
1. Document new sharing and privacy options
2. Update analytics dashboard navigation
3. Track transcript feature improvements
4. Log new organizational features

## Notes
- Recording is done via Loom desktop/extension
- Transcripts may take time to process
- Some features require Loom Business plan
- Viewer data shows engagement patterns
- Videos can be password-protected
