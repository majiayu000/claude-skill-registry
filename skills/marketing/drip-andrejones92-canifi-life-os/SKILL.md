---
name: drip
description: Manage e-commerce email marketing with Drip's revenue-focused automation platform.
category: marketing
---
# Drip Skill

Manage e-commerce email marketing with Drip's revenue-focused automation platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/drip/install.sh | bash
```

Or manually:
```bash
cp -r skills/drip ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set DRIP_API_KEY "your_api_key"
canifi-env set DRIP_ACCOUNT_ID "your_account_id"
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

1. **Subscriber Management**: Track subscribers with rich e-commerce data
2. **Email Campaigns**: Create branded email campaigns
3. **Workflow Automation**: Build automated journeys based on behavior
4. **Segmentation**: Create segments based on purchase and browse behavior
5. **Revenue Attribution**: Track email impact on revenue

## Usage Examples

### Add Subscriber
```
User: "Add a new subscriber to Drip from the checkout"
Assistant: Creates subscriber with e-commerce data
```

### Create Campaign
```
User: "Create a product recommendation campaign in Drip"
Assistant: Creates campaign with product blocks
```

### Start Workflow
```
User: "Trigger the abandoned cart workflow for this subscriber"
Assistant: Enrolls subscriber in workflow
```

### View Revenue
```
User: "Show me Drip revenue from email this month"
Assistant: Returns revenue attribution metrics
```

## Authentication Flow

1. Get API key from Drip account settings
2. Note your account ID from settings
3. Use Basic Auth with API key
4. Account ID required for most endpoints

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 404 Not Found | Resource not found | Check account ID |
| 422 Validation Error | Invalid data | Fix request format |
| 429 Rate Limited | Too many requests | Implement backoff |

## Notes

- E-commerce marketing focus
- Deep Shopify integration
- Visual workflow builder
- Revenue tracking built-in
- Pre-built automation templates
- 14-day free trial
