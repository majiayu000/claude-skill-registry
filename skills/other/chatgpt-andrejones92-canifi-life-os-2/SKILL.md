---
name: chatgpt
description: OpenAI's conversational AI assistant.
category: ai
---
# ChatGPT Skill

OpenAI's conversational AI assistant.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/chatgpt/install.sh | bash
```

Or manually:
```bash
cp -r skills/chatgpt ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set OPENAI_API_KEY "your_api_key"
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

1. **Conversations**: Start and continue chats
2. **Custom GPTs**: Access specialized GPTs
3. **Code Interpreter**: Execute and analyze code
4. **Image Generation**: Create images with DALL-E
5. **Browse Web**: Real-time information lookup

## Usage Examples

### New Chat
```
User: "Ask ChatGPT to explain quantum computing"
Assistant: Sends query and returns response
```

### Use Custom GPT
```
User: "Use the Data Analyst GPT"
Assistant: Engages specialized GPT
```

### Generate Image
```
User: "Create an image of a sunset"
Assistant: Generates with DALL-E
```

### Analyze Code
```
User: "Have ChatGPT review this code"
Assistant: Runs code analysis
```

## Authentication Flow

1. API key authentication
2. OAuth for ChatGPT web
3. Plus subscription for advanced features
4. Organization support

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Rate Limited | Too many requests | Wait or upgrade |
| Context Length | Message too long | Reduce input |
| Model Error | Capacity issue | Retry |

## Notes

- GPT-4 and GPT-3.5
- Custom GPTs
- Plugins available
- Code interpreter
- DALL-E integration
- Vision capabilities
