---
name: copy-ai
description: AI-powered copywriting and content generation.
category: ai
---
# Copy.ai Skill

AI-powered copywriting and content generation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/copy-ai/install.sh | bash
```

Or manually:
```bash
cp -r skills/copy-ai ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set COPYAI_API_KEY "your_api_key"
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

1. **Generate Copy**: Create marketing content
2. **Workflows**: Automated content pipelines
3. **Infobase**: Knowledge management
4. **Chat**: Conversational content creation
5. **Templates**: Pre-built content types

## Usage Examples

### Generate Copy
```
User: "Write product descriptions"
Assistant: Creates compelling copy
```

### Use Workflow
```
User: "Run the blog workflow"
Assistant: Executes content pipeline
```

### Add to Infobase
```
User: "Save this to my Infobase"
Assistant: Stores for future reference
```

### Chat Mode
```
User: "Help me brainstorm headlines"
Assistant: Collaborates on ideas
```

## Authentication Flow

1. API key authentication
2. Workspace access
3. Team collaboration
4. SSO available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Credits Exhausted | Usage limit | Add credits |
| Workflow Error | Configuration | Check setup |
| Template Error | Not found | Verify template |

## Notes

- Workflow automation
- Infobase knowledge
- Team workspaces
- 90+ templates
- API available
- Enterprise options
