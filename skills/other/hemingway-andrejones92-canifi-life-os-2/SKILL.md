---
name: hemingway
description: Writing editor for bold and clear content.
category: ai
---
# Hemingway Editor Skill

Writing editor for bold and clear content.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/hemingway/install.sh | bash
```

Or manually:
```bash
cp -r skills/hemingway ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set HEMINGWAY_EMAIL "your_email"
canifi-env set HEMINGWAY_PASSWORD "your_password"
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

1. **Readability Score**: Grade level analysis
2. **Simplify Writing**: Reduce complexity
3. **Passive Voice**: Detect and fix
4. **Adverb Detection**: Highlight weak words
5. **Sentence Length**: Identify long sentences

## Usage Examples

### Check Readability
```
User: "What's the grade level of this text?"
Assistant: Returns readability score
```

### Simplify Text
```
User: "Make this writing clearer"
Assistant: Highlights complex sentences
```

### Fix Passive Voice
```
User: "Find passive voice in my writing"
Assistant: Identifies passive constructions
```

### Reduce Adverbs
```
User: "Which adverbs should I remove?"
Assistant: Highlights weak adverbs
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation
4. Desktop app available

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Analysis Failed | Text too long | Split content |
| App Error | Browser issue | Retry |
| Export Failed | Format issue | Try different format |

## Notes

- Bold, clear writing
- Color-coded feedback
- Grade level scoring
- Desktop app
- No public API
- Simple interface
