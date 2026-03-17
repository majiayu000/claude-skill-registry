---
name: gtm-management
description: Manage Google Tag Manager containers, tags, triggers, and variables. Use when working with GTM configuration, analytics tracking, conversion tracking, or event management. Triggers on "GTM", "Google Tag Manager", "tags", "triggers", "analytics".
---

# GTM Management

Manage Google Tag Manager containers using @akson analytics packages.

## When to Use

- User mentions "GTM", "Google Tag Manager"
- User asks about tags, triggers, or variables
- User wants to set up conversion tracking
- User needs to validate analytics configuration
- User mentions Google Ads conversions

## Quick Commands

```bash
# Check GTM status
npm run gtm:status

# Validate configuration
npm run gtm:validate

# Plan changes (dry run)
npm run gtm:plan

# Apply changes
npm run gtm:apply

# Create backup
npm run gtm:backup

# Health check across platforms
npx @akson/cortex-analytics health --verbose
```

## Event Naming Standards

### Lead Generation Events (Landing Pages)

```typescript
import { LEAD_GENERATION_EVENTS, LEAD_SCORES } from '@akson/cortex-utilities/events';

LEAD_GENERATION_EVENTS.LEAD_PAGE_VIEW       // Score: 5
LEAD_GENERATION_EVENTS.LEAD_CONTENT_VIEW    // Score: 15
LEAD_GENERATION_EVENTS.LEAD_INQUIRY_STARTED // Score: 40
LEAD_GENERATION_EVENTS.LEAD_CONTACT_INFO    // Score: 60
LEAD_GENERATION_EVENTS.LEAD_WHATSAPP_CONTACT // Score: 85
LEAD_GENERATION_EVENTS.LEAD_FORM_SUBMITTED  // Score: 100
```

### E-commerce Events (Shopify)

```typescript
import { ECOMMERCE_EVENTS } from '@akson/cortex-utilities/events';

ECOMMERCE_EVENTS.VIEW_ITEM      // Product views
ECOMMERCE_EVENTS.ADD_TO_CART    // Cart additions
ECOMMERCE_EVENTS.BEGIN_CHECKOUT // Checkout started
ECOMMERCE_EVENTS.PURCHASE       // Completed transactions
```

## Platform Configuration

| Platform | ID |
|----------|-----|
| GTM Container | GTM-T8WRBMWV |
| GA4 Property | G-PTZF5JDTMH |
| Google Ads Account | 8847935674 |
| Google Ads Conversion | 659644670 |
| PostHog Project | phc_Y8vb3DFiRumtKXyoKQsVO77XlE26AuDWc1iXaZc8rjC |

## Conversion Labels

| Conversion | Label |
|------------|-------|
| Form Submission | JIHLCN-r-IwbEP7BxboC |
| WhatsApp Contact | o9ylCNyr-IwbEP7BxboC |

## Service Account Setup

```bash
# Get key from 1Password
op document get "MyArmy - GTM Service Account Key" --out-file config/gtm-api-automation.json

# Test access
npm run gtm:status
```

## Environment Variables

```bash
GOOGLE_SERVICE_ACCOUNT_KEY_FILE=config/gtm-api-automation.json
GTM_SERVICE_ACCOUNT_KEY_FILE=config/gtm-api-automation.json
```

## Key Rules

### DO:
- Use standardized event names from @akson/cortex-utilities
- Test in GTM preview mode before publishing
- Create backups before changes
- Validate configuration after updates

### DON'T:
- Mix lead generation and e-commerce event systems
- Use hardcoded event names
- Deploy without testing
- Skip validation step

## Common Patterns

### Add GA4 Event Tag

1. Create trigger for the event
2. Create GA4 Event tag
3. Set event name and parameters
4. Test in preview mode
5. Publish container

### Add Google Ads Conversion

1. Get conversion ID and label
2. Create conversion linker tag
3. Create conversion tag with trigger
4. Test conversion tracking
5. Verify in Google Ads

## Debugging

```bash
# Verbose health check
npx @akson/cortex-analytics health --verbose

# Check specific platform
npx @akson/cortex-analytics gtm status --container GTM-T8WRBMWV
```
