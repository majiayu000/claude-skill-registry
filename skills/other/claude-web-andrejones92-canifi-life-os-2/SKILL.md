---
name: claude-web
description: Anthropic's Claude AI assistant via web interface.
category: ai
---
# Claude Web Skill

Anthropic's Claude AI assistant via web interface.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/claude-web/install.sh | bash
```

Or manually:
```bash
cp -r skills/claude-web ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set ANTHROPIC_API_KEY "your_api_key"
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

1. **Conversations**: Long-context discussions
2. **Document Analysis**: Process PDFs and files
3. **Code Help**: Programming assistance
4. **Projects**: Organize conversations
5. **Artifacts**: Interactive content creation

## Usage Examples

### Start Chat
```
User: "Ask Claude to summarize this document"
Assistant: Processes and summarizes
```

### Analyze Document
```
User: "Have Claude analyze this PDF"
Assistant: Extracts and analyzes content
```

### Code Review
```
User: "Get Claude's feedback on this code"
Assistant: Provides code review
```

### Create Artifact
```
User: "Have Claude create a React component"
Assistant: Generates interactive artifact
```

## Authentication Flow

1. API key authentication
2. OAuth for web access
3. Pro subscription features
4. Organization support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Rate Limited | Usage exceeded | Wait or upgrade |
| Context Full | Too much content | Reduce input |
| Overloaded | High demand | Retry later |

## Notes

- 200K context window
- Vision support
- Artifacts feature
- Projects organization
- Claude 3 models
- Constitutional AI
