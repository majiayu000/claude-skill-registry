---
name: perplexity
description: AI-powered search engine with real-time answers.
category: ai
---
# Perplexity Skill

AI-powered search engine with real-time answers.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/perplexity/install.sh | bash
```

Or manually:
```bash
cp -r skills/perplexity ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PERPLEXITY_API_KEY "your_api_key"
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

1. **Search Answers**: Get sourced responses
2. **Pro Search**: Deep research mode
3. **Collections**: Organize research
4. **Focus Modes**: Academic, writing, etc.
5. **Follow-ups**: Refine queries

## Usage Examples

### Quick Search
```
User: "Ask Perplexity about recent AI developments"
Assistant: Returns sourced answer
```

### Pro Research
```
User: "Do a deep dive on climate technology"
Assistant: Runs comprehensive research
```

### Academic Search
```
User: "Find academic sources on this topic"
Assistant: Returns scholarly citations
```

### Follow Up
```
User: "Tell me more about that third source"
Assistant: Expands on specific result
```

## Authentication Flow

1. API key authentication
2. Pro subscription for advanced
3. OAuth for integrations
4. Rate limits apply

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Auth Failed | Invalid key | Check API key |
| Rate Limited | Too many queries | Wait |
| Pro Required | Feature limited | Upgrade |
| Search Failed | Query issue | Rephrase |

## Notes

- Real-time web search
- Source citations
- Pro Search depth
- Focus modes
- Collections
- API available
