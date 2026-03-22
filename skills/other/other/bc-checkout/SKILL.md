---
name: bc-checkout
description: Customize BigCommerce checkout — Checkout SDK, embedded checkout, server-side checkout API, custom checkout UI, and checkout extensions. Use when modifying the checkout experience or building headless checkout flows.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Checkout Customization

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.bigcommerce.com/docs/storefront/cart-checkout/checkout-sdk` for Checkout SDK
2. Web-search `site:developer.bigcommerce.com checkout api` for Checkout API reference
3. Web-search `bigcommerce embedded checkout headless` for embedded checkout patterns

## Checkout Architecture

### Three Approaches

| Approach | Where | Use Case |
|----------|-------|----------|
| **Native Checkout** | BigCommerce storefront | Default — customize via SDK or theme |
| **Embedded Checkout** | External site (iframe) | Headless with BigCommerce-hosted checkout |
| **Custom Checkout** | Your own frontend | Fully custom using Checkout/Payments API |

## Checkout SDK

### What It Is

A JavaScript SDK for customizing the native BigCommerce checkout:
- Renders checkout UI in a target DOM element
- Provides methods to interact with checkout state
- Fires events for checkout lifecycle
- Available as `@bigcommerce/checkout-sdk` npm package

### Installation

```bash
npm install @bigcommerce/checkout-sdk
```

### Core Methods

```javascript
import { createCheckoutService } from '@bigcommerce/checkout-sdk';

const service = createCheckoutService();

// Load checkout
await service.loadCheckout(checkoutId);

// Get current state
const state = service.getState();
const checkout = state.data.getCheckout();

// Update shipping address
await service.updateShippingAddress(address);

// Select shipping option
await service.selectShippingOption(optionId);

// Apply coupon
await service.applyCoupon(code);

// Submit order
await service.submitOrder(orderPayload);
```

### State Selectors

The state object provides selectors:
- `getCheckout()` — full checkout data
- `getCart()` — cart items and totals
- `getCustomer()` — customer info
- `getShippingAddress()` — shipping address
- `getBillingAddress()` — billing address
- `getShippingOptions()` — available shipping methods
- `getPaymentMethods()` — available payment methods
- `getOrder()` — completed order

### Checkout Events

Subscribe to state changes:
```javascript
service.subscribe(state => {
  const checkout = state.data.getCheckout();
  // React to checkout state changes
});
```

## Embedded Checkout

### How It Works

Embed BigCommerce's checkout in an external site via iframe:
1. Create a cart via the Server-to-Server Cart API
2. Generate a checkout URL (from the cart's `redirect_urls.checkout_url`)
3. Embed the URL in an iframe on your site
4. Listen for `postMessage` events from the iframe

### Setup

Include the Embedded Checkout script:
```javascript
import { embedCheckout } from '@bigcommerce/checkout-sdk';

embedCheckout({
  url: checkoutUrl,
  containerId: 'checkout-container',
  onComplete: () => { /* order placed */ },
  onError: (error) => { /* handle error */ },
  onFrameLoad: () => { /* checkout loaded */ },
});
```

### Requirements

- HTTPS on your domain
- Configure "Trusted Domains" in BigCommerce admin
- Set `X-Frame-Options` and CSP headers to allow embedding

## Server-Side Checkout API

### Cart to Checkout Flow

1. **Create Cart**: `POST /v3/carts` with line items
2. **Add Billing Address**: `POST /v3/checkouts/{id}/billing-address`
3. **Add Consignment (Shipping)**: `POST /v3/checkouts/{id}/consignments`
4. **Select Shipping Option**: `PUT /v3/checkouts/{id}/consignments/{consignmentId}`
5. **Create Order**: `POST /v3/checkouts/{id}/orders`
6. **Process Payment**: `POST /v3/payments` (via Payments API)

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v3/carts` | POST | Create cart |
| `/v3/carts/{id}/items` | POST, PUT, DELETE | Manage cart items |
| `/v3/carts/{id}/redirect_urls` | POST | Get checkout URL |
| `/v3/checkouts/{id}` | GET | Get checkout state |
| `/v3/checkouts/{id}/billing-address` | POST, PUT | Set billing address |
| `/v3/checkouts/{id}/consignments` | POST | Add shipping info |
| `/v3/checkouts/{id}/coupons` | POST, DELETE | Apply/remove coupons |
| `/v3/checkouts/{id}/orders` | POST | Create order from checkout |

## Checkout Customization in Stencil

### Theme Template

Checkout uses `templates/pages/checkout.html` with special handling:
- Uses the `empty` layout (minimal wrapper)
- Checkout UI is primarily JavaScript-rendered
- Limited template customization compared to other pages

### Checkout JS Customization

Override checkout JavaScript for UI modifications:
- Fork the open-source checkout: `github.com/bigcommerce/checkout-js`
- Build custom React checkout components
- Deploy as a custom checkout script

## Best Practices

- Use Embedded Checkout for headless — avoids PCI scope expansion
- Use the Checkout SDK for programmatic control
- Always use HTTPS for checkout flows
- Handle payment failures gracefully with clear error messages
- Test the full checkout flow with real payment sandbox credentials
- Support guest checkout and registered customer checkout
- Validate all addresses server-side
- Handle coupon edge cases (expired, minimum spend, etc.)

Fetch the Checkout SDK docs and BigCommerce Checkout API reference for exact method signatures, state structure, and configuration options before implementing.
