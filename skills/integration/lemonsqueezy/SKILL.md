---
name: lemonsqueezy
description: Integrates payments and subscriptions with Lemon Squeezy merchant of record platform. Use when selling digital products, SaaS subscriptions, or software licenses with built-in tax handling.
---

# Lemon Squeezy

Merchant of record platform for digital products and SaaS. Handles payments, taxes, and compliance globally. Official JavaScript SDK for server-side integration.

## Quick Start

```bash
npm install @lemonsqueezy/lemonsqueezy.js
```

### Setup

```typescript
import { lemonSqueezySetup, getAuthenticatedUser } from '@lemonsqueezy/lemonsqueezy.js';

lemonSqueezySetup({
  apiKey: process.env.LEMONSQUEEZY_API_KEY,
  onError: (error) => console.error('Lemon Squeezy Error:', error),
});

// Verify setup
const { data, error } = await getAuthenticatedUser();
if (error) {
  console.error('Auth failed:', error.message);
} else {
  console.log('Connected as:', data.attributes.name);
}
```

## Create Checkout

Generate checkout URLs for customers to purchase.

```typescript
import { createCheckout } from '@lemonsqueezy/lemonsqueezy.js';

async function createPaymentCheckout(variantId: string, customerEmail: string) {
  const { data, error } = await createCheckout(process.env.LEMONSQUEEZY_STORE_ID!, {
    productOptions: {
      redirectUrl: 'https://myapp.com/success',
      receiptButtonText: 'Go to Dashboard',
      receiptThankYouNote: 'Thank you for your purchase!',
    },
    checkoutOptions: {
      embed: true,
      media: true,
      logo: true,
    },
    checkoutData: {
      email: customerEmail,
      custom: {
        userId: 'user_123',
      },
    },
    expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours
    preview: false,
  }, {
    relationships: {
      variant: {
        data: {
          type: 'variants',
          id: variantId,
        },
      },
    },
  });

  if (error) throw new Error(error.message);
  return data.attributes.url;
}
```

### With Discount

```typescript
const { data } = await createCheckout(storeId, {
  checkoutData: {
    discountCode: 'SAVE20',
    email: customerEmail,
  },
}, {
  relationships: {
    variant: {
      data: { type: 'variants', id: variantId },
    },
  },
});
```

## Products & Variants

```typescript
import { listProducts, listVariants, getProduct, getVariant } from '@lemonsqueezy/lemonsqueezy.js';

// List all products
const { data: products } = await listProducts({
  filter: { storeId: process.env.LEMONSQUEEZY_STORE_ID },
});

products.forEach((product) => {
  console.log(product.attributes.name, product.attributes.price_formatted);
});

// Get single product
const { data: product } = await getProduct('prod_123');

// List variants for a product
const { data: variants } = await listVariants({
  filter: { productId: 'prod_123' },
});

// Get variant details
const { data: variant } = await getVariant('var_123');
```

## Subscriptions

```typescript
import {
  listSubscriptions,
  getSubscription,
  updateSubscription,
  cancelSubscription,
} from '@lemonsqueezy/lemonsqueezy.js';

// List user's subscriptions
const { data: subscriptions } = await listSubscriptions({
  filter: {
    storeId: process.env.LEMONSQUEEZY_STORE_ID,
    userEmail: 'customer@example.com',
  },
});

// Get subscription details
const { data: subscription } = await getSubscription('sub_123');
console.log('Status:', subscription.attributes.status);
console.log('Renews at:', subscription.attributes.renews_at);

// Pause subscription
await updateSubscription('sub_123', {
  pause: {
    mode: 'void',  // or 'free'
    resumesAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
  },
});

// Resume subscription
await updateSubscription('sub_123', {
  pause: null,
});

// Change plan (upgrade/downgrade)
await updateSubscription('sub_123', {
  variantId: 'new_variant_id',
  invoiceImmediately: true,
});

// Cancel subscription
await cancelSubscription('sub_123');
```

## License Keys

```typescript
import {
  listLicenseKeys,
  getLicenseKey,
  updateLicenseKey,
  activateLicense,
  validateLicense,
  deactivateLicense,
} from '@lemonsqueezy/lemonsqueezy.js';

// List license keys
const { data: licenses } = await listLicenseKeys({
  filter: { orderId: 'order_123' },
});

// Activate license (no API key required)
const { data: activation } = await activateLicense('LICENSE-KEY-HERE', 'instance-name');
console.log('License valid:', activation.valid);
console.log('Activations:', activation.license_key.activation_usage);

// Validate license (no API key required)
const { data: validation } = await validateLicense('LICENSE-KEY-HERE', 'instance-name');
if (validation.valid) {
  console.log('License is active');
} else {
  console.log('Invalid:', validation.error);
}

// Deactivate license (no API key required)
await deactivateLicense('LICENSE-KEY-HERE', 'instance-id');

// Disable/enable license key (requires API key)
await updateLicenseKey('lk_123', {
  disabled: true,
});
```

## Orders

```typescript
import { listOrders, getOrder, listOrderItems, generateOrderInvoice } from '@lemonsqueezy/lemonsqueezy.js';

// List orders
const { data: orders } = await listOrders({
  filter: {
    storeId: process.env.LEMONSQUEEZY_STORE_ID,
    userEmail: 'customer@example.com',
  },
});

// Get order details
const { data: order } = await getOrder('order_123');
console.log('Total:', order.attributes.total_formatted);
console.log('Status:', order.attributes.status);

// Get order items
const { data: items } = await listOrderItems({
  filter: { orderId: 'order_123' },
});

// Generate invoice PDF
const { data: invoice } = await generateOrderInvoice('order_123');
console.log('Invoice URL:', invoice.attributes.url);
```

## Customers

```typescript
import {
  createCustomer,
  getCustomer,
  listCustomers,
  updateCustomer,
  archiveCustomer,
} from '@lemonsqueezy/lemonsqueezy.js';

// Create customer
const { data: customer } = await createCustomer(process.env.LEMONSQUEEZY_STORE_ID!, {
  name: 'John Doe',
  email: 'john@example.com',
  city: 'New York',
  country: 'US',
});

// List customers
const { data: customers } = await listCustomers({
  filter: { storeId: process.env.LEMONSQUEEZY_STORE_ID },
});

// Update customer
await updateCustomer('cust_123', {
  name: 'Jane Doe',
});

// Archive customer
await archiveCustomer('cust_123');
```

## Discounts

```typescript
import {
  createDiscount,
  listDiscounts,
  getDiscount,
  deleteDiscount,
} from '@lemonsqueezy/lemonsqueezy.js';

// Create discount
const { data: discount } = await createDiscount(process.env.LEMONSQUEEZY_STORE_ID!, {
  name: 'Summer Sale',
  code: 'SUMMER2024',
  amount: 20,
  amountType: 'percent',  // or 'fixed'
  isLimitedToProducts: false,
  isLimitedRedemptions: true,
  maxRedemptions: 100,
  startsAt: new Date().toISOString(),
  expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
});

// List discounts
const { data: discounts } = await listDiscounts({
  filter: { storeId: process.env.LEMONSQUEEZY_STORE_ID },
});

// Delete discount
await deleteDiscount('disc_123');
```

## Webhooks

### Setup Webhook Handler

```typescript
import { createWebhook, listWebhooks } from '@lemonsqueezy/lemonsqueezy.js';
import crypto from 'crypto';

// Create webhook programmatically
const { data: webhook } = await createWebhook(process.env.LEMONSQUEEZY_STORE_ID!, {
  url: 'https://myapp.com/api/webhooks/lemonsqueezy',
  events: [
    'order_created',
    'subscription_created',
    'subscription_updated',
    'subscription_cancelled',
    'subscription_payment_success',
    'subscription_payment_failed',
    'license_key_created',
  ],
  secret: process.env.LEMONSQUEEZY_WEBHOOK_SECRET,
});
```

### Handle Webhooks (Next.js)

```typescript
// app/api/webhooks/lemonsqueezy/route.ts
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

export async function POST(request: NextRequest) {
  const rawBody = await request.text();
  const signature = request.headers.get('x-signature');

  // Verify signature
  const hmac = crypto.createHmac('sha256', process.env.LEMONSQUEEZY_WEBHOOK_SECRET!);
  const digest = hmac.update(rawBody).digest('hex');

  if (signature !== digest) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const payload = JSON.parse(rawBody);
  const eventName = payload.meta.event_name;
  const data = payload.data;

  switch (eventName) {
    case 'order_created':
      console.log('New order:', data.id);
      // Fulfill order, send email, etc.
      break;

    case 'subscription_created':
      console.log('New subscription:', data.id);
      // Grant access, update database
      break;

    case 'subscription_updated':
      console.log('Subscription updated:', data.attributes.status);
      // Handle plan changes, pauses
      break;

    case 'subscription_cancelled':
      console.log('Subscription cancelled:', data.id);
      // Revoke access, send win-back email
      break;

    case 'subscription_payment_success':
      console.log('Payment received');
      // Update billing records
      break;

    case 'subscription_payment_failed':
      console.log('Payment failed');
      // Notify customer, retry logic
      break;

    case 'license_key_created':
      console.log('License created:', data.attributes.key);
      // Send license to customer
      break;
  }

  return NextResponse.json({ received: true });
}
```

## Lemon.js (Frontend)

For client-side checkout overlays.

```html
<script src="https://app.lemonsqueezy.com/js/lemon.js" defer></script>

<a href="https://mystore.lemonsqueezy.com/checkout/buy/abc123" class="lemonsqueezy-button">
  Buy Now
</a>
```

### With JavaScript

```javascript
// Initialize
window.createLemonSqueezy();

// Open checkout programmatically
window.LemonSqueezy.Url.Open('https://mystore.lemonsqueezy.com/checkout/buy/abc123');

// Listen to events
window.LemonSqueezy.Setup({
  eventHandler: (event) => {
    if (event.event === 'Checkout.Success') {
      console.log('Purchase complete!', event.data);
    }
  },
});
```

## Usage Records (Metered Billing)

```typescript
import { createUsageRecord, listUsageRecords } from '@lemonsqueezy/lemonsqueezy.js';

// Report usage
const { data: record } = await createUsageRecord({
  subscriptionItemId: 'si_123',
  quantity: 100,
  action: 'increment',  // or 'set'
});

// List usage records
const { data: records } = await listUsageRecords({
  filter: { subscriptionItemId: 'si_123' },
});
```

## Next.js Server Actions

```typescript
// app/actions/billing.ts
'use server';

import {
  createCheckout,
  cancelSubscription,
  updateSubscription,
} from '@lemonsqueezy/lemonsqueezy.js';
import { auth } from '@/lib/auth';

export async function createCheckoutAction(variantId: string) {
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');

  const { data, error } = await createCheckout(
    process.env.LEMONSQUEEZY_STORE_ID!,
    {
      checkoutData: {
        email: session.user.email,
        custom: { userId: session.user.id },
      },
    },
    {
      relationships: {
        variant: { data: { type: 'variants', id: variantId } },
      },
    }
  );

  if (error) throw new Error(error.message);
  return data.attributes.url;
}

export async function cancelSubscriptionAction(subscriptionId: string) {
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');

  // Verify ownership before cancelling
  await cancelSubscription(subscriptionId);
  return { success: true };
}
```

## Environment Variables

```bash
LEMONSQUEEZY_API_KEY=your_api_key
LEMONSQUEEZY_STORE_ID=your_store_id
LEMONSQUEEZY_WEBHOOK_SECRET=your_webhook_secret
```

## Best Practices

1. **Server-side only** - Never expose API key in browser
2. **Verify webhooks** - Always validate signatures
3. **Use test mode** - Build integration before going live
4. **Store custom data** - Pass userId in checkout for correlation
5. **Handle all events** - Account for failed payments, cancellations
6. **Idempotent handlers** - Webhooks may be delivered multiple times
