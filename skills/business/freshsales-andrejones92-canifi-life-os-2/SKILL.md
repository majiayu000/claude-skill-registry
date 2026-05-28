---
name: freshsales
description: Manage sales with Freshsales CRM powered by AI and automation.
category: business
---
# Freshsales Skill

Manage sales with Freshsales CRM powered by AI and automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/freshsales/install.sh | bash
```

Or manually:
```bash
cp -r skills/freshsales ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set FRESHSALES_API_KEY "your_api_key"
canifi-env set FRESHSALES_DOMAIN "your_domain.freshsales.io"
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

1. **Contact Management**: Manage contacts with AI-powered scoring and insights
2. **Deal Pipeline**: Track deals with visual pipeline and forecasting
3. **Email & Phone**: Integrated email and phone with automatic logging
4. **AI Assistant**: Use Freddy AI for lead scoring and next actions
5. **Sequence Automation**: Create automated sales sequences and workflows

## Usage Examples

### Create Contact
```
User: "Add Sarah Williams as a new contact in Freshsales"
Assistant: Creates contact with AI enrichment
```

### View Pipeline
```
User: "Show me my Freshsales deal pipeline"
Assistant: Returns deals organized by stage
```

### Start Sequence
```
User: "Add the new lead to the onboarding sequence"
Assistant: Enrolls contact in automated sequence
```

### Check AI Insights
```
User: "What deals should I focus on today?"
Assistant: Returns AI-recommended priority deals
```

## Authentication Flow

1. Get API key from Freshsales admin settings
2. Use API key in request header
3. Domain-specific API endpoint
4. No refresh needed for API key auth

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 403 Forbidden | Insufficient permissions | Check admin access |
| 429 Rate Limited | Too many requests | Implement backoff |
| 404 Not Found | Resource doesn't exist | Verify ID |

## Notes

- Part of Freshworks suite
- Free tier available for small teams
- Freddy AI for intelligent insights
- Native phone and email integration
- Mobile app for field sales
- Customizable sales processes
