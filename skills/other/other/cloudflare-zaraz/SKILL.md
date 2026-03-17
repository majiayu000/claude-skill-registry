---
name: cloudflare-zaraz
description: Server-side tag management for third-party tools with edge execution, privacy controls, and near-zero performance impact
version: 1.0.0
tags: [cloudflare, zaraz, tag-management, analytics, privacy, edge, performance, consent]
---

# Cloudflare Zaraz

Server-side tag management platform that loads third-party tools at Cloudflare's edge, eliminating client-side performance impact while providing privacy controls and consent management.

## Overview

Cloudflare Zaraz offloads third-party tools (analytics, advertising pixels, chatbots, marketing automation) to the cloud, executing at the edge rather than in the browser. This architecture delivers near-zero performance impact while enhancing security and privacy.

### Key Benefits

- **Performance**: Load multiple tools with minimal client impact
- **Privacy**: Built-in IP anonymization, referrer hiding, user-agent trimming
- **Security**: Server-side execution reduces attack surface
- **Consent**: Integrated Consent Management Platform (CMP)
- **Simplicity**: No code changes needed for most integrations

## Getting Started

### Prerequisites

- Website proxied through Cloudflare (recommended)
- At least one tool configured in Zaraz
- Auto-inject script enabled (default)

### Adding Third-Party Tools

1. Navigate to **Zaraz > Tools configuration** in Cloudflare dashboard
2. Select **Third-party tools > Add new tool**
3. Browse the tools catalog and select your tool
4. Configure tool-specific settings
5. Set up actions with firing triggers
6. Save configuration

### Automatic Action Types

When tools support automatic actions:

- **Pageviews**: Track all page loads automatically
- **Events**: Monitor via `zaraz.track()` Web API
- **E-Commerce**: Process transactions via `zaraz.ecommerce()` API

## Web API

The Zaraz Web API enables programmatic control from anywhere in the `<body>` tag.

### zaraz.track()

Track custom events and user actions.

```javascript
// Syntax
zaraz.track(eventName, [eventProperties])

// Basic event
zaraz.track("button_click")

// Event with properties
zaraz.track("purchase", {
  value: 200,
  currency: "USD",
  product_id: "SKU-123"
})

// Async usage
await zaraz.track("signup_complete", { plan: "premium" })
```

**Common Use Cases:**
- User actions (sign-ups, button clicks, purchases)
- Page interactions (widget loads, element impressions)
- Form submissions

**Accessing Properties in Triggers:**
```
{{ client.value }}
{{ client.`product_id` }}  // Use backticks for special characters
```

### zaraz.set()

Store variables for use across all events without repetition.

```javascript
// Syntax
zaraz.set(key, value, [options])

// Page scope (cleared on navigation)
zaraz.set("page_category", "blog", { scope: "page" })

// Session scope (persists during session)
zaraz.set("user_tier", "premium", { scope: "session" })

// Persist scope (localStorage, survives sessions) - DEFAULT
zaraz.set("user_id", "12345", { scope: "persist" })
zaraz.set("user_id", "12345")  // Same as above

// Unset a variable
zaraz.set("user_id", undefined)
```

**Scope Options:**
| Scope | Persistence | Use Case |
|-------|-------------|----------|
| `page` | Current page only | Page-specific context |
| `session` | Browser session | User session data |
| `persist` | localStorage (default) | Cross-session identity |

### zaraz.ecommerce()

Track e-commerce events with standardized data structure.

```javascript
// Syntax
zaraz.ecommerce(eventName, eventProperties)

// Product viewed
zaraz.ecommerce("Product Viewed", {
  product_id: "507f1f77",
  sku: "G-32",
  name: "Monopoly",
  price: 18.99,
  category: "Games"
})

// Add to cart
zaraz.ecommerce("Product Added", {
  product_id: "507f1f77",
  name: "Monopoly",
  price: 18.99,
  quantity: 1
})

// Order completed
zaraz.ecommerce("Order Completed", {
  order_id: "50314b8e",
  total: 27.50,
  revenue: 25.00,
  shipping: 3.00,
  tax: 2.00,
  currency: "USD",
  products: [
    {
      product_id: "507f1f77",
      name: "Monopoly",
      price: 18.99,
      quantity: 1
    }
  ]
})
```

**Supported Events (18 total):**
- Product List Viewed, Products Searched
- Product Clicked, Product Viewed, Product Added, Product Removed
- Product Added to Wishlist
- Cart Viewed
- Checkout Started, Checkout Step Viewed, Checkout Step Completed
- Payment Info Entered, Shipping Info Entered
- Order Completed, Order Updated, Order Refunded, Order Cancelled
- Clicked Promotion, Viewed Promotion

**Product Properties:**
| Property | Description |
|----------|-------------|
| `product_id` | Unique identifier |
| `sku` | Stock keeping unit |
| `name` | Product name |
| `brand` | Brand name |
| `category` | Product category |
| `variant` | Product variant |
| `price` | Unit price |
| `quantity` | Number of items |
| `coupon` | Applied coupon |
| `position` | List position |

**Order Properties:**
| Property | Description |
|----------|-------------|
| `order_id` | Order identifier |
| `checkout_id` | Checkout identifier |
| `total` | Total amount |
| `revenue` | Revenue (excl. shipping/tax) |
| `shipping` | Shipping cost |
| `tax` | Tax amount |
| `discount` | Discount applied |
| `currency` | Currency code |

**Compatible Tools:**
- Google Analytics 4
- Google Analytics (Universal)
- Facebook Pixel
- Bing
- Pinterest Conversions API
- TikTok
- Amplitude
- Branch

### SPA Support

For Single Page Applications, Zaraz automatically tracks virtual pageviews when URLs change (enable in Settings).

```javascript
// Manual SPA pageview (advanced use)
zaraz.spaPageview()
```

## Triggers

Triggers define conditions for action execution.

### Match Rule

Compare variables against match strings.

**Variables Available:**
- Event Name
- URL components (pathname, host, query)
- Cookies
- Device Properties
- Page Properties

**Match Operations:**
- Equals / Does not equal
- Contains / Does not contain
- Starts with / Ends with
- Matches regex / Does not match regex
- Greater than / Less than

### Click Listener

Monitor clicks using CSS selectors or XPath.

```css
/* CSS Examples */
#submit-button        /* ID selector */
.cta-button          /* Class selector */
button[type="submit"] /* Attribute selector */
```

**Parameters:**
- **Selector**: CSS selector or XPath expression
- **Wait for actions**: Delay navigation (ms) to ensure requests complete

### Form Submission

Track form submissions with optional validation.

```css
/* Form selector */
#checkout-form
form[name="contact"]
```

**Parameters:**
- **Selector**: CSS selector for form
- **Validate**: Only trigger on valid submissions

### Element Visibility

Fire when elements become visible in viewport.

```css
/* Visibility triggers */
#promo-banner
.video-player
```

### Scroll Depth

Trigger at scroll thresholds.

```
100px     /* Fixed pixel value */
50%       /* Viewport percentage */
```

### Timer

Execute after intervals.

**Parameters:**
- **Interval**: Milliseconds between executions
- **Limit**: Maximum executions (0 = unlimited)

## Blocking Triggers

Prevent actions from firing under specific conditions.

```
Firing Trigger: Pageview
Blocking Trigger: URL contains "/admin"
```

**Key Points:**
- Inverse of firing triggers
- Zaraz script still loads
- Must apply to each action individually

## Consent Management

GDPR and ePrivacy Directive compliance through built-in CMP.

### Key Concepts

**Purpose**: Reason for loading a tool (e.g., "Analytics", "Advertising")
**Consent**: User permission to store/access cookies

### Consent Storage

User preferences stored in first-party cookie:
```json
{
  "analytics": true,
  "advertising": false,
  "functional": true
}
```

### Consent API

```javascript
// Wait for API ready
document.addEventListener("zarazConsentAPIReady", () => {
  // Check specific purpose
  const analyticsConsent = zaraz.consent.get("analytics")

  // Get all consent statuses
  const allConsent = zaraz.consent.getAll()

  // Set consent for specific purposes
  zaraz.consent.set({
    analytics: true,
    advertising: false
  })

  // Accept or reject all
  zaraz.consent.setAll(true)   // Accept all
  zaraz.consent.setAll(false)  // Reject all

  // Show consent modal
  zaraz.consent.modal = true
})

// Listen for consent changes
document.addEventListener("zarazConsentChoicesUpdated", () => {
  console.log("User updated consent preferences")
})

// Send queued events after consent
zaraz.consent.sendQueuedEvents()
```

**API Methods:**
| Method | Description |
|--------|-------------|
| `get(purposeId)` | Get consent for specific purpose |
| `set(preferences)` | Update consent for purposes |
| `getAll()` | Get all consent statuses |
| `setAll(status)` | Set all purposes |
| `getAllCheckboxes()` | Get checkbox states |
| `setCheckboxes(states)` | Update checkboxes |
| `setAllCheckboxes(state)` | Set all checkboxes |
| `sendQueuedEvents()` | Send blocked events after consent |

**Properties:**
| Property | Description |
|----------|-------------|
| `modal` | Show/hide consent modal |
| `purposes` | Read-only purpose definitions |
| `APIReady` | Boolean API availability |

### Region-Based Consent

```javascript
document.addEventListener("zarazConsentAPIReady", () => {
  // Show modal only for EU visitors
  if (zaraz.consent.purposes.analytics.region === "EU") {
    zaraz.consent.modal = true
  } else {
    zaraz.consent.setAll(true)
  }
})
```

## Properties Reference

### Event Properties

| Property | Description |
|----------|-------------|
| Event Name | Name from zaraz.track() |
| Track Property | Values from eventProperties or zaraz.set() |

### Page Properties

| Property | Description |
|----------|-------------|
| Page encoding | Document character encoding |
| Page referrer | Referring URL |
| Page title | Document title |
| Query param | Specific URL parameter |
| URL (various) | host, hostname, origin, pathname, port, protocol |

### Device Properties

| Property | Description |
|----------|-------------|
| Browser engine/name/version | Browser details |
| Device type | Desktop, mobile, tablet |
| Device CPU | Processor architecture |
| Language | Browser language |
| Resolution | Screen dimensions |
| Viewport | Browser viewport size |
| OS name/version | Operating system |
| User-agent | Full UA string |
| IP address | Visitor IP |

### Location Properties

| Property | Description |
|----------|-------------|
| City | Visitor city |
| Continent | Geographic continent |
| Country | Country code |
| EU | EU membership (1/0) |
| Region | Region name |
| Region code | ISO 3166-2 code |
| Timezone | Visitor timezone |

### Miscellaneous

| Property | Description |
|----------|-------------|
| Random number | Unique per request |
| Timestamp (ms/s) | Unix timestamp |
| Cookie | Browser cookie value |

## Data Layer Compatibility

Migrate from Google Tag Manager without code changes.

### Enable Compatibility Mode

1. Navigate to **Zaraz > Settings**
2. Enable **Data layer compatibility mode**

### How It Works

```javascript
// Existing GTM code
dataLayer.push({
  event: 'purchase',
  price: '24',
  currency: 'USD'
})

// Automatically converted to
zaraz.track('purchase', { price: '24', currency: 'USD' })
```

**Note:** E-commerce mapping not supported via dataLayer. Use `zaraz.ecommerce()` instead.

## Context Enricher

Enrich event data using Cloudflare Workers.

### Basic Structure

```javascript
export default {
  async fetch(request) {
    const { system, client } = await request.json()

    // Add weather data
    const weather = await fetch('https://api.weather.com/...')
    client.weather = await weather.json()

    // Redact email addresses
    for (const key in client) {
      if (typeof client[key] === 'string' && client[key].includes('@')) {
        client[key] = '[REDACTED]'
      }
    }

    return new Response(JSON.stringify({ system, client }))
  }
}
```

### Setup

1. Create Worker in Cloudflare dashboard or via Wrangler
2. Navigate to **Zaraz > Settings**
3. Select your Worker as Context Enricher

## Settings Reference

### Workflow

| Setting | Description |
|---------|-------------|
| Real-time | Changes publish immediately |
| Preview & Publish | Test before deployment |

### Web API

| Setting | Description |
|---------|-------------|
| Debug Key | Enable Debug Mode |
| E-commerce tracking | Enable zaraz.ecommerce() |

### Compatibility

| Setting | Description |
|---------|-------------|
| Data layer mode | GTM dataLayer.push() support |
| SPA support | Virtual pageviews on URL change |

### Privacy

| Setting | Description |
|---------|-------------|
| Remove query params | Strip URL parameters |
| Trim IP addresses | Remove before sending to tools |
| Hide user-agent | Sanitize sensitive details |
| Hide referrer | Hide external referrers |
| Cookie domain | Custom cookie domain |

### Injection

| Setting | Description |
|---------|-------------|
| Auto-inject | Load Zaraz automatically |
| Iframe injection | Inject into iframes |

### Endpoints

| Setting | Description |
|---------|-------------|
| Custom paths | Custom script pathnames |

### Advanced

| Setting | Description |
|---------|-------------|
| Bot threshold | Block suspected bot traffic |
| Context Enricher | Worker for data enrichment |
| Logpush | Export logs (Enterprise) |

## Supported Tools

### Analytics
- Amplitude
- Google Analytics (Universal)
- Google Analytics 4
- Mixpanel
- Segment
- Snowplow
- Pod Sights

### Advertising
- Bing
- Facebook Pixel
- Floodlight
- Google Ads
- LinkedIn Insight
- Outbrain
- Pinterest / Pinterest Conversions API
- Quora
- Reddit
- Snapchat
- Taboola
- Tatari
- TikTok
- Twitter Pixel

### Marketing
- Branch
- HubSpot
- Impact Radius

### Recruiting
- Indeed
- iHire
- Upward
- ZipRecruiter

### Custom Integrations
- Custom HTML
- Custom Image
- HTTP Request

## Monitoring

### Metrics Available

| Metric | Description |
|--------|-------------|
| Loads | Zaraz script loads |
| Events | Tracked events (pageview, custom, ecommerce) |
| Triggers | Trigger activations |
| Actions | Action executions |
| Server-side requests | HTTP status codes from third-party tools |

### Debug Mode

1. Set Debug Key in Zaraz Settings
2. Access via browser console
3. View real-time event flow

## Best Practices

### Performance

1. **Use native integrations** over Custom HTML
2. **Enable SPA support** for single-page applications
3. **Use blocking triggers** to prevent unnecessary actions
4. **Minimize Custom HTML** - runs client-side

### Privacy

1. **Enable IP trimming** for GDPR compliance
2. **Configure consent purposes** before enabling tools
3. **Use Context Enricher** to redact sensitive data
4. **Hide referrers** for cross-domain tracking protection

### Migration from GTM

1. **Don't use GTM with Zaraz** - loses optimization benefits
2. **Enable data layer compatibility** for gradual migration
3. **Convert to native integrations** over time
4. **Use zaraz.ecommerce()** instead of dataLayer for e-commerce

### Debugging

```javascript
// Check if Zaraz is loaded
if (typeof zaraz !== 'undefined') {
  console.log('Zaraz loaded successfully')
}

// Enable Debug Mode in console
// Access real-time event monitoring
```

### Common Issues

| Issue | Solution |
|-------|----------|
| `zaraz is not defined` | Verify domain is proxied, Auto Injection enabled |
| Browser extension can't detect tools | Use Debug Mode (server-side execution) |
| E-commerce returns undefined | Enable E-commerce tracking in Settings |
| Demographics missing in GA | Use "Anonymize IP" instead of "Hide IP" |

## Integration Examples

### React E-commerce

```jsx
import { useEffect } from 'react'

function ProductPage({ product }) {
  useEffect(() => {
    // Track product view
    if (typeof zaraz !== 'undefined') {
      zaraz.ecommerce('Product Viewed', {
        product_id: product.id,
        name: product.name,
        price: product.price,
        category: product.category
      })
    }
  }, [product])

  const handleAddToCart = () => {
    if (typeof zaraz !== 'undefined') {
      zaraz.ecommerce('Product Added', {
        product_id: product.id,
        name: product.name,
        price: product.price,
        quantity: 1
      })
    }
    // Add to cart logic
  }

  return (
    <div>
      <h1>{product.name}</h1>
      <button onClick={handleAddToCart}>Add to Cart</button>
    </div>
  )
}
```

### Next.js with Consent

```jsx
// components/ConsentBanner.jsx
import { useEffect, useState } from 'react'

export function ConsentBanner() {
  const [showBanner, setShowBanner] = useState(false)

  useEffect(() => {
    const handleReady = () => {
      const allConsent = zaraz.consent.getAll()
      if (Object.keys(allConsent).length === 0) {
        setShowBanner(true)
      }
    }

    document.addEventListener('zarazConsentAPIReady', handleReady)
    return () => document.removeEventListener('zarazConsentAPIReady', handleReady)
  }, [])

  const acceptAll = () => {
    zaraz.consent.setAll(true)
    setShowBanner(false)
  }

  const rejectAll = () => {
    zaraz.consent.setAll(false)
    setShowBanner(false)
  }

  if (!showBanner) return null

  return (
    <div className="consent-banner">
      <p>We use cookies to improve your experience.</p>
      <button onClick={acceptAll}>Accept All</button>
      <button onClick={rejectAll}>Reject All</button>
      <button onClick={() => zaraz.consent.modal = true}>
        Customize
      </button>
    </div>
  )
}
```

### Vue.js Event Tracking

```vue
<template>
  <button @click="trackClick">{{ label }}</button>
</template>

<script setup>
import { onMounted } from 'vue'

const props = defineProps({
  label: String,
  eventName: String,
  eventProps: Object
})

onMounted(() => {
  if (typeof zaraz !== 'undefined') {
    zaraz.set('component_loaded', props.label, { scope: 'page' })
  }
})

function trackClick() {
  if (typeof zaraz !== 'undefined') {
    zaraz.track(props.eventName, props.eventProps)
  }
}
</script>
```

### Checkout Flow

```javascript
// Step 1: Checkout started
zaraz.ecommerce('Checkout Started', {
  checkout_id: 'CHK-123',
  value: 50.00,
  currency: 'USD',
  products: cartItems
})

// Step 2: Shipping info
zaraz.ecommerce('Shipping Info Entered', {
  checkout_id: 'CHK-123',
  shipping_method: 'standard'
})

// Step 3: Payment info
zaraz.ecommerce('Payment Info Entered', {
  checkout_id: 'CHK-123',
  payment_method: 'credit_card'
})

// Step 4: Order completed
zaraz.ecommerce('Order Completed', {
  order_id: 'ORD-456',
  checkout_id: 'CHK-123',
  total: 53.00,
  revenue: 50.00,
  shipping: 3.00,
  tax: 0,
  currency: 'USD',
  products: cartItems
})
```

## Resources

- [Zaraz Documentation](https://developers.cloudflare.com/zaraz/)
- [Zaraz Discord](https://discord.cloudflare.com/)
- [Cloudflare Community Forum](https://community.cloudflare.com/)
- [Managed Components](https://managedcomponents.dev/)
