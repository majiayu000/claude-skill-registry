---
name: moz
description: Research SEO metrics and domain authority with Moz's SEO tools.
category: marketing
---
# Moz Skill

Research SEO metrics and domain authority with Moz's SEO tools.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/moz/install.sh | bash
```

Or manually:
```bash
cp -r skills/moz ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MOZ_ACCESS_ID "your_access_id"
canifi-env set MOZ_SECRET_KEY "your_secret_key"
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

1. **Domain Authority**: Check DA and PA scores
2. **Link Analysis**: Analyze inbound links and linking domains
3. **Keyword Research**: Research keywords with difficulty scores
4. **On-page Optimization**: Get page optimization recommendations
5. **SERP Analysis**: Analyze search results for keywords

## Usage Examples

### Check Domain Authority
```
User: "What's the Domain Authority for example.com?"
Assistant: Returns DA, PA, and spam score
```

### Analyze Links
```
User: "Show me linking domains to my site"
Assistant: Returns linking domain analysis
```

### Keyword Difficulty
```
User: "How hard is it to rank for 'seo tools'?"
Assistant: Returns keyword difficulty and metrics
```

### On-page Analysis
```
User: "Analyze my page for SEO optimization"
Assistant: Returns optimization recommendations
```

## Authentication Flow

1. Get Access ID and Secret Key from Moz
2. Generate signature for each request
3. Include signature in request header
4. Time-based signature expiration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid signature | Regenerate signature |
| 403 Forbidden | No credits | Purchase more credits |
| 404 Not Found | No data | Verify domain/URL |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Created Domain Authority metric
- Link Explorer for backlinks
- Keyword Explorer included
- Moz Pro for full toolkit
- API credits based on plan
- MozBar Chrome extension
