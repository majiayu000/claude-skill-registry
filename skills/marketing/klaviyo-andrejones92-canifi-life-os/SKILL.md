---
name: klaviyo
description: Manage e-commerce email and SMS marketing with Klaviyo's data-driven platform.
category: marketing
---
# Klaviyo Skill

Manage e-commerce email and SMS marketing with Klaviyo's data-driven platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/klaviyo/install.sh | bash
```

Or manually:
```bash
cp -r skills/klaviyo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set KLAVIYO_API_KEY "your_api_key"
canifi-env set KLAVIYO_PRIVATE_KEY "your_private_key"
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

1. **Profile Management**: Create and manage customer profiles with event data
2. **Campaign Creation**: Build and send email and SMS campaigns
3. **Flow Automation**: Create automated marketing flows
4. **Segmentation**: Build dynamic segments based on behavior
5. **Analytics**: Access detailed performance metrics and revenue tracking

## Usage Examples

### Add Profile
```
User: "Add a new customer profile to Klaviyo"
Assistant: Creates profile with provided details
```

### Create Campaign
```
User: "Create a product launch email campaign in Klaviyo"
Assistant: Creates campaign with template and settings
```

### Build Segment
```
User: "Create a segment of customers who purchased in the last 30 days"
Assistant: Creates segment with purchase criteria
```

### View Analytics
```
User: "Show me Klaviyo revenue attribution for last month"
Assistant: Returns revenue metrics by campaign and flow
```

## Authentication Flow

1. Get API keys from Klaviyo account settings
2. Public key for tracking and subscriptions
3. Private key for full API access
4. Use appropriate key based on operation

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify private key |
| 403 Forbidden | Insufficient permissions | Check key access |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- Built for e-commerce businesses
- Deep Shopify integration
- Predictive analytics included
- SMS marketing support
- Revenue attribution tracking
- Free tier up to 250 contacts
