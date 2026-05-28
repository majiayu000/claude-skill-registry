---
name: otter-ai
description: AI meeting transcription and note-taking assistant.
category: productivity
---
# Otter.ai Skill

AI meeting transcription and note-taking assistant.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/otter-ai/install.sh | bash
```

Or manually:
```bash
cp -r skills/otter-ai ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OTTER_EMAIL "your_email"
canifi-env set OTTER_PASSWORD "your_password"
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

1. **Live Transcription**: Real-time meeting notes
2. **Recording**: Capture and transcribe
3. **Summary**: AI meeting summaries
4. **Highlights**: Mark key moments
5. **Speaker ID**: Identify speakers

## Usage Examples

### Start Recording
```
User: "Start transcribing my meeting"
Assistant: Begins live transcription
```

### Get Summary
```
User: "Summarize the last meeting"
Assistant: Returns AI summary
```

### Search Notes
```
User: "Find mentions of the budget"
Assistant: Searches transcripts
```

### Export Transcript
```
User: "Export this transcript"
Assistant: Generates document
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation
4. Calendar integrations

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Recording Failed | Audio issue | Check permissions |
| Transcription Error | Quality issue | Improve audio |
| Limit Reached | Minutes exceeded | Upgrade plan |

## Notes

- Real-time transcription
- Speaker identification
- OtterPilot for meetings
- Calendar sync
- No public API
- Mobile apps
