---
name: semrush
description: Research SEO, PPC, and competitive intelligence with SEMrush's marketing toolkit.
category: marketing
---
# SEMrush Skill

Research SEO, PPC, and competitive intelligence with SEMrush's marketing toolkit.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/semrush/install.sh | bash
```

Or manually:
```bash
cp -r skills/semrush ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set SEMRUSH_API_KEY "your_api_key"
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

1. **Keyword Research**: Discover keywords with volume and difficulty
2. **Site Audit**: Analyze technical SEO issues
3. **Backlink Analysis**: Research backlink profiles
4. **Competitive Research**: Analyze competitor strategies
5. **Position Tracking**: Monitor search rankings

## Usage Examples

### Keyword Research
```
User: "Find keywords related to 'digital marketing'"
Assistant: Returns keywords with volume and difficulty
```

### Site Audit
```
User: "Run an SEO audit on my website"
Assistant: Returns technical SEO issues and recommendations
```

### Check Backlinks
```
User: "Show me backlinks for competitor.com"
Assistant: Returns backlink profile analysis
```

### Track Rankings
```
User: "Where do I rank for 'marketing automation'?"
Assistant: Returns current position and history
```

## Authentication Flow

1. Get API key from SEMrush account
2. Use API key in request parameters
3. Credits consumed per request
4. Different endpoints use different credits

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | No credits | Purchase more credits |
| 404 Not Found | No data found | Try different query |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- All-in-one marketing toolkit
- Credit-based API pricing
- 40+ SEO tools included
- Competitive intelligence
- PPC and advertising data
- Content marketing tools
