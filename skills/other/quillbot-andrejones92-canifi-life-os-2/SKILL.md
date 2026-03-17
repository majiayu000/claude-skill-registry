---
name: quillbot
description: AI paraphrasing and writing enhancement tool.
category: ai
---
# QuillBot Skill

AI paraphrasing and writing enhancement tool.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/quillbot/install.sh | bash
```

Or manually:
```bash
cp -r skills/quillbot ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set QUILLBOT_EMAIL "your_email"
canifi-env set QUILLBOT_PASSWORD "your_password"
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

1. **Paraphrasing**: Rewrite text in different ways
2. **Grammar Check**: Fix errors
3. **Summarizer**: Condense long content
4. **Citation Generator**: Create citations
5. **Translator**: Translate content

## Usage Examples

### Paraphrase Text
```
User: "Rewrite this paragraph"
Assistant: Returns paraphrased version
```

### Summarize
```
User: "Summarize this article"
Assistant: Creates condensed version
```

### Generate Citation
```
User: "Create a citation for this source"
Assistant: Generates formatted citation
```

### Translate
```
User: "Translate this to Spanish"
Assistant: Returns translation
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation
4. Premium features

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Premium Required | Feature locked | Upgrade |
| Word Limit | Text too long | Split content |
| Mode Error | Unavailable | Try different mode |

## Notes

- Multiple paraphrase modes
- Chrome extension
- Word integration
- Co-Writer feature
- No public API
- Free tier available
