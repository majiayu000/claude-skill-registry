---
name: wsj
description: Access business and financial news from The Wall Street Journal.
category: news
---
# Wall Street Journal Skill

Access business and financial news from The Wall Street Journal.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/wsj/install.sh | bash
```

Or manually:
```bash
cp -r skills/wsj ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set WSJ_EMAIL "your_email"
canifi-env set WSJ_PASSWORD "your_password"
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

1. **Market News**: Get real-time market updates, stock news, and financial analysis
2. **Business Coverage**: Read business, technology, and economy news
3. **Opinion & Analysis**: Access WSJ opinion pieces and expert analysis
4. **Saved Articles**: Save and organize articles for later reading
5. **Personalized Feed**: Get news tailored to your interests and portfolio

## Usage Examples

### Get Market News
```
User: "Show me the latest WSJ market news"
Assistant: Returns top market headlines and stock updates
```

### Search Articles
```
User: "Search WSJ for articles about Federal Reserve"
Assistant: Returns relevant articles about Fed policy and decisions
```

### Browse Section
```
User: "Show me WSJ Tech section articles"
Assistant: Returns latest technology industry news
```

### Save Article
```
User: "Save this WSJ article about Tesla"
Assistant: Saves article to your WSJ account
```

## Authentication Flow

1. WSJ uses subscriber authentication
2. No official public API available
3. Browser automation required for access
4. Subscription required for full content

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Verify subscriber credentials |
| Paywall Block | Subscription required | Subscribe to WSJ |
| Session Expired | Login timeout | Re-authenticate |
| Rate Limited | Too many requests | Implement throttling |

## Notes

- Subscription required for full article access
- Part of Dow Jones media properties
- Real-time market data included
- Mobile apps available with offline reading
- WSJ+ benefits for subscribers
- No official API; uses browser automation
