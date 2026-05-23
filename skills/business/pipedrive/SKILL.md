---
name: pipedrive
description: Manage sales pipeline with Pipedrive's visual deal-focused CRM.
category: business
---
# Pipedrive Skill

Manage sales pipeline with Pipedrive's visual deal-focused CRM.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/pipedrive/install.sh | bash
```

Or manually:
```bash
cp -r skills/pipedrive ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set PIPEDRIVE_API_TOKEN "your_api_token"
canifi-env set PIPEDRIVE_COMPANY_DOMAIN "your_company_domain"
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

1. **Deal Management**: Create and manage deals with visual pipeline stages
2. **Contact Organization**: Organize people and organizations with deal links
3. **Activity Scheduling**: Schedule calls, meetings, and follow-up activities
4. **Email Integration**: Sync emails and track communications
5. **Sales Insights**: Access sales metrics, forecasts, and performance data

## Usage Examples

### Create Deal
```
User: "Create a new deal in Pipedrive for Software License worth $5000"
Assistant: Creates deal with value and links to contact
```

### Move Deal Stage
```
User: "Move the Marketing Package deal to Demo Scheduled"
Assistant: Updates deal stage in pipeline
```

### Log Activity
```
User: "Log a call with John about the proposal"
Assistant: Creates activity record linked to contact and deal
```

### Get Pipeline Stats
```
User: "Show me my Pipedrive pipeline overview"
Assistant: Returns deals by stage with values
```

## Authentication Flow

1. Get API token from Personal Preferences in Pipedrive
2. Use token for all API requests
3. OAuth 2.0 available for app marketplace
4. Token provides full account access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API token | Verify token in settings |
| 403 Forbidden | Feature not available | Check subscription tier |
| 429 Rate Limited | Too many requests | Implement rate limiting |
| 404 Not Found | Resource doesn't exist | Verify ID |

## Notes

- Visual pipeline focus for sales teams
- Free trial, paid plans start at Essential
- API rate limit: 80 requests per 2 seconds
- Marketplace for extensions and integrations
- Mobile apps for on-the-go access
- Smart contact data enrichment available
