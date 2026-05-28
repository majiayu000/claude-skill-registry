---
name: gtm-myarmy
extends: analytics-framework/gtm-integration
description: MyArmy GTM implementation with Swiss military market conversion tracking
---

# MyArmy GTM Implementation

Extends `analytics-framework/gtm-integration` with MyArmy-specific configuration for Swiss military e-commerce and lead generation.

## Configuration

**GTM Container**: `GTM-T8WRBMWV` (ID: 226061083)
**Google Ads Account**: `8847935674`
**Conversion ID**: `659644670`

## Conversion Labels

| Event | Conversion Label | Value | Description |
|-------|------------------|-------|-------------|
| Form Submission | `JIHLCN-r-IwbEP7BxboC` | Lead score (1-100) | Contact form completed |
| WhatsApp Contact | `o9ylCNyr-IwbEP7BxboC` | Lead score (85) | WhatsApp link clicked |

## Event Tracking

MyArmy uses **dual event systems** (see CLAUDE.md analytics section):

### Lead Generation Events (Landing Page)
```typescript
import { LEAD_GENERATION_EVENTS } from '@akson/cortex-utilities/events';

// Track lead journey with scoring
trackEvent(LEAD_GENERATION_EVENTS.LEAD_PAGE_VIEW, { page: '/funktionsabzeichen' }); // +5
trackEvent(LEAD_GENERATION_EVENTS.LEAD_CONTENT_VIEW, { content: 'custom-badges' }); // +15
trackEvent(LEAD_GENERATION_EVENTS.LEAD_INQUIRY_STARTED, { formId: 'contact' }); // +40
trackEvent(LEAD_GENERATION_EVENTS.LEAD_CONTACT_INFO, { email: '...' }); // +60
trackEvent(LEAD_GENERATION_EVENTS.LEAD_WHATSAPP_CONTACT, { number: '...' }); // +85
trackEvent(LEAD_GENERATION_EVENTS.LEAD_FORM_SUBMITTED, { leadScore: 100 }); // +100
```

### E-commerce Events (Shopify)
```typescript
import { ECOMMERCE_EVENTS } from '@akson/cortex-utilities/events';

// Track e-commerce with actual CHF values
trackEvent(ECOMMERCE_EVENTS.VIEW_ITEM, { productId: '...', value: 149.90 });
trackEvent(ECOMMERCE_EVENTS.ADD_TO_CART, { productId: '...', value: 149.90 });
trackEvent(ECOMMERCE_EVENTS.BEGIN_CHECKOUT, { cartValue: 299.80 });
trackEvent(ECOMMERCE_EVENTS.PURCHASE, { orderId: '...', value: 299.80 });
```

## GTM Configuration

Managed via `@akson/cortex-gtm` package:

```bash
# Validate current GTM setup
npm run gtm:validate

# Preview changes (dry run)
npm run gtm:plan

# Apply configuration
npm run gtm:apply

# Check status
npm run gtm:status
```

## Service Account

**Email**: `gtm-api-automation@myarmy-ads-prod.iam.gserviceaccount.com`
**Key Location**: `landing/config/gtm-api-automation.json` (from 1Password)

**Permissions**:
- GTM Container `GTM-T8WRBMWV`: Full access
- Google Ads Account `8847935674`: Conversion tracking
- GA4 Property `G-PTZF5JDTMH`: Event tracking

## Swiss Market Context

### Target Keywords (GSC)
- `militär badge` - Primary Swiss German keyword
- `funktionsabzeichen` - Technical term for function badges
- `rekrutenschule souvenir` - Recruitment school souvenirs
- `schweizer armee` - Swiss Army (brand)
- `abzeichen schweizer armee` - Swiss Army badges

### Conversion Funnel
```
1. Organic Search (militär badge) → Landing Page
2. Product Page View (custom badges)
3. Design Inquiry Form Started
4. Contact Info Submitted
5. WhatsApp Contact → Quote Request
6. Order Placed (Shopify)
```

## Platform Integration

### PostHog (Product Analytics)
**Project ID**: `phc_Y8vb3DFiRumtKXyoKQsVO77XlE26AuDWc1iXaZc8rjC`

Events are sent to both GTM and PostHog for cross-validation:
```typescript
function trackConversion(eventName: string, data: any) {
  // GTM for ads platforms
  dataLayer.push({ event: eventName, ...data });

  // PostHog for product analytics
  if (window.posthog) {
    window.posthog.capture(eventName, data);
  }
}
```

### GA4 (Google Analytics)
**Measurement ID**: `G-PTZF5JDTMH`

All lead generation events flow through GTM → GA4 for funnel analysis.

## Debugging

Enable debug logging in Next.js app:

```typescript
import { createDebugLogger } from '@/app/lib/debug/debug-logger';

const debug = createDebugLogger('GTM');

debug.log('DataLayer push:', { event: 'form_submitted', formId: 'contact' });
debug.time('gtm-tag-fire');
// ... wait for tag
debug.timeEnd('gtm-tag-fire');
```

## Key Rules

### DO:
- Use standardized event names from `@akson/cortex-utilities`
- Track lead score (1-100) with every event
- Test in GTM Preview mode before publishing
- Use CHF currency for all monetary values
- Separate lead generation events from e-commerce events

### DON'T:
- Mix event naming conventions
- Hardcode conversion labels (use env vars)
- Deploy without validation (`npm run gtm:validate`)
- Skip PostHog tracking (needed for attribution)
- Forget to update event documentation when adding new events

## Environment Variables

```bash
GTM_CONTAINER_ID="GTM-T8WRBMWV"
GA4_MEASUREMENT_ID="G-PTZF5JDTMH"
GOOGLE_ADS_CUSTOMER_ID="8847935674"
GOOGLE_ADS_CONVERSION_ID="659644670"
CONVERSION_LABEL_FORM="JIHLCN-r-IwbEP7BxboC"
CONVERSION_LABEL_WHATSAPP="o9ylCNyr-IwbEP7BxboC"
POSTHOG_PROJECT_KEY="phc_Y8vb3DFiRumtKXyoKQsVO77XlE26AuDWc1iXaZc8rjC"
```

## Resources

- **Framework**: `analytics-framework/gtm-integration`
- **CLAUDE.md**: Analytics & Event Standardization section
- **@akson Packages**: `cortex-gtm`, `cortex-analytics`, `cortex-utilities`
- **Landing Docs**: `/landing/docs/03-analytics/`
