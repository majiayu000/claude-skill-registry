---
name: gorgias
description: Manage e-commerce customer support with Gorgias's Shopify-focused help desk.
category: business
---
# Gorgias Skill

Manage e-commerce customer support with Gorgias's Shopify-focused help desk.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/gorgias/install.sh | bash
```

Or manually:
```bash
cp -r skills/gorgias ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GORGIAS_DOMAIN "your_store.gorgias.com"
canifi-env set GORGIAS_API_KEY "your_api_key"
canifi-env set GORGIAS_API_USER "your_api_user"
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

1. **Ticket Management**: Handle customer tickets across all channels
2. **Shopify Integration**: Access order data and perform actions directly
3. **Macros & Templates**: Use automated responses with dynamic variables
4. **Automation Rules**: Set up auto-responses and routing rules
5. **Revenue Tracking**: Track support impact on revenue and conversions

## Usage Examples

### View Ticket
```
User: "Show me the latest Gorgias ticket about shipping"
Assistant: Returns recent shipping-related ticket
```

### Check Order
```
User: "Look up order #1234 for this customer ticket"
Assistant: Retrieves Shopify order details
```

### Apply Macro
```
User: "Apply the 'shipping delay' macro to this ticket"
Assistant: Applies macro with order details
```

### Close Ticket
```
User: "Mark this Gorgias ticket as resolved"
Assistant: Updates ticket status to closed
```

## Authentication Flow

1. Get API credentials from Gorgias settings
2. Use HTTP Basic Auth with user:key
3. Domain-specific API endpoints
4. API access varies by plan

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify API user and key |
| 403 Forbidden | Feature not available | Check plan tier |
| 404 Not Found | Ticket not found | Verify ticket ID |
| 429 Rate Limited | Too many requests | Implement throttling |

## Notes

- Built specifically for e-commerce
- Deep Shopify, WooCommerce integration
- Automated responses with order data
- Revenue attribution tracking
- Self-service order management
- AI-powered suggested responses
