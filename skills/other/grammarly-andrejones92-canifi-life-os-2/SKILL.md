---
name: grammarly
description: AI writing assistant for grammar, style, and tone.
category: ai
---
# Grammarly Skill

AI writing assistant for grammar, style, and tone.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/grammarly/install.sh | bash
```

Or manually:
```bash
cp -r skills/grammarly ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GRAMMARLY_EMAIL "your_email"
canifi-env set GRAMMARLY_PASSWORD "your_password"
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

1. **Grammar Check**: Fix errors and typos
2. **Style Suggestions**: Improve clarity
3. **Tone Detection**: Analyze writing tone
4. **Plagiarism Check**: Detect copied content
5. **GrammarlyGO**: AI writing assistance

## Usage Examples

### Check Grammar
```
User: "Check this text for errors"
Assistant: Returns corrections
```

### Improve Style
```
User: "Make this more concise"
Assistant: Suggests improvements
```

### Check Tone
```
User: "What tone is this email?"
Assistant: Analyzes tone
```

### Check Plagiarism
```
User: "Check for plagiarism"
Assistant: Scans for copied content
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
| Check Failed | Processing error | Retry |
| Rate Limited | Too many checks | Wait |

## Notes

- AI-powered suggestions
- Tone detection
- Plagiarism checker
- Browser extensions
- No public API
- GrammarlyGO AI
