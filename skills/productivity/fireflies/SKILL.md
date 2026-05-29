---
name: fireflies
description: AI meeting assistant for transcription and analysis.
category: productivity
---
# Fireflies.ai Skill

AI meeting assistant for transcription and analysis.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/fireflies/install.sh | bash
```

Or manually:
```bash
cp -r skills/fireflies ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FIREFLIES_API_KEY "your_api_key"
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

1. **Auto-Join**: Join meetings automatically
2. **Transcription**: Accurate meeting notes
3. **AI Summary**: Key points extraction
4. **Action Items**: Identify follow-ups
5. **Integrations**: CRM and tool sync

## Usage Examples

### Get Transcript
```
User: "Show transcript of today's meeting"
Assistant: Returns meeting transcript
```

### Extract Actions
```
User: "What are the action items?"
Assistant: Lists follow-up tasks
```

### Search Meetings
```
User: "Find discussions about Q4 goals"
Assistant: Searches across meetings
```

### Get Summary
```
User: "Summarize the standup"
Assistant: Returns AI summary
```

## Authentication Flow

1. API key authentication
2. OAuth for calendar
3. Meeting bot integration
4. CRM connections

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Bot Error | Join failed | Check permissions |
| Transcription Error | Audio quality | Improve setup |
| Limit Reached | Minutes exceeded | Upgrade |

## Notes

- Auto-join meetings
- CRM integration
- Topic tracking
- Sound bites
- API available
- Browser extension
