---
name: paddle
description: Integrates billing and subscriptions with Paddle merchant of record platform. Use when selling SaaS subscriptions with checkout overlays, pricing pages, and subscription management.
---

# Paddle

Merchant of record platform for SaaS. Handles payments, taxes, and compliance. Use Paddle.js for frontend checkouts and the Node.js SDK for server-side operations.

## Quick Start - Paddle.js (Frontend)

```html
<script src="https://cdn.paddle.com/paddle/v2/paddle.js"></script>
<script>
  Paddle.Initialize({
    token: 'live_xxxxxxxxxxxxxxxxxxxxxxxx'  // Client-side token
  });
</script>
```

### Open Checkout

```javascript
Paddle.Checkout.open({
  items: [
    { priceId: 'pri_01gm81eqze2vmmvhpjg13bfeqg', quantity: 1 }
  ]
});
```

## Node.js SDK (Server-side)

```bash
npm install @paddle/paddle-node-sdk
```

### Setup

```typescript
import { Paddle, Environment } from '@paddle/paddle-node-sdk';

const paddle = new Paddle(process.env.PADDLE_API_KEY!, {
  environment: Environment.sandbox  // or Environment.production
});
```

## Paddle.js Checkout

### Basic Checkout

```javascript
Paddle.Checkout.open({
  items: [
    { priceId: 'pri_01abc123', quantity: 1 },
    { priceId: 'pri_02def456', quantity: 2 }
  ]
});
```

### With Customer Data

```javascript
Paddle.Checkout.open({
  items: [{ priceId: 'pri_01abc123', quantity: 1 }],
  customer: {
    email: 'customer@example.com',
    address: {
      countryCode: 'US',
      postalCode: '10001'
    }
  },
  customData: {
    userId: 'user_123',
    plan: 'pro'
  }
});
```

### Inline Checkout

```html
<div id="checkout-container"></div>

<script>
Paddle.Checkout.open({
  items: [{ priceId: 'pri_01abc123', quantity: 1 }],
  settings: {
    displayMode: 'inline',
    frameTarget: 'checkout-container',
    frameStyle: 'width: 100%; min-width: 312px; background-color: transparent; border: none;'
  }
});
</script>
```

### Checkout Events

```javascript
Paddle.Checkout.open({
  items: [{ priceId: 'pri_01abc123', quantity: 1 }],
  settings: {
    successUrl: 'https://myapp.com/success?checkout={checkout_id}'
  }
});

// Listen to events
Paddle.Setup({
  eventCallback: function(event) {
    switch (event.name) {
      case 'checkout.loaded':
        console.log('Checkout loaded');
        break;
      case 'checkout.customer.created':
        console.log('Customer:', event.data.customer);
        break;
      case 'checkout.completed':
        console.log('Success! Transaction:', event.data.transaction_id);
        // Redirect or show success
        break;
      case 'checkout.closed':
        console.log('Checkout closed');
        break;
      case 'checkout.error':
        console.error('Error:', event.data);
        break;
    }
  }
});
```

### Update Checkout

```javascript
// Update items
Paddle.Checkout.updateItems([
  { priceId: 'pri_01abc123', quantity: 2 }
]);

// Close checkout
Paddle.Checkout.close();
```

## Price Preview

Calculate prices with localization and taxes.

```javascript
// Frontend with Paddle.js
const pricePreview = await Paddle.PricePreview({
  items: [
    { priceId: 'pri_01abc123', quantity: 1 }
  ],
  address: {
    countryCode: 'US',
    postalCode: '10001'
  }
});

console.log('Subtotal:', pricePreview.data.details.totals.subtotal);
console.log('Tax:', pricePreview.data.details.totals.tax);
console.log('Total:', pricePreview.data.details.totals.total);
```

### Server-side Price Preview

```typescript
const preview = await paddle.pricingPreviews.previewPrices({
  items: [
    { priceId: 'pri_01abc123', quantity: 1 }
  ],
  address: {
    countryCode: 'US',
    postalCode: '10001'
  }
});

console.log(preview.data.details.lineItems[0].formattedTotals);
```

## Products & Prices (Server-side)

```typescript
// List products
const products = await paddle.products.list();

// Get product
const product = await paddle.products.get('pro_01abc123');

// List prices for a product
const prices = await paddle.prices.list({
  productId: ['pro_01abc123']
});

// Create a price
const newPrice = await paddle.prices.create({
  productId: 'pro_01abc123',
  description: 'Monthly subscription',
  unitPrice: {
    amount: '999',
    currencyCode: 'USD'
  },
  billingCycle: {
    interval: 'month',
    frequency: 1
  }
});
```

## Subscriptions

### List Subscriptions

```typescript
const subscriptions = await paddle.subscriptions.list({
  customerId: ['ctm_01abc123'],
  status: ['active', 'trialing']
});
```

### Get Subscription

```typescript
const subscription = await paddle.subscriptions.get('sub_01abc123');

console.log('Status:', subscription.status);
console.log('Next billing:', subscription.nextBilledAt);
console.log('Current period ends:', subscription.currentBillingPeriod?.endsAt);
```

### Update Subscription

```typescript
// Change plan
await paddle.subscriptions.update('sub_01abc123', {
  items: [
    { priceId: 'pri_newplan123', quantity: 1 }
  ],
  prorationBillingMode: 'prorated_immediately'
});

// Pause subscription
await paddle.subscriptions.pause('sub_01abc123', {
  effectiveFrom: 'next_billing_period'
});

// Resume subscription
await paddle.subscriptions.resume('sub_01abc123', {
  effectiveFrom: 'immediately'
});
```

### Cancel Subscription

```typescript
await paddle.subscriptions.cancel('sub_01abc123', {
  effectiveFrom: 'next_billing_period'  // or 'immediately'
});
```

### Update Payment Method

Generate a URL for customers to update their payment method.

```typescript
const updateUrl = await paddle.subscriptions.getPaymentMethodChangeTransaction('sub_01abc123');
// Redirect customer to updateUrl
```

## Transactions

```typescript
// List transactions
const transactions = await paddle.transactions.list({
  customerId: ['ctm_01abc123'],
  status: ['completed']
});

// Get transaction
const transaction = await paddle.transactions.get('txn_01abc123');

// Get invoice PDF
const invoice = await paddle.transactions.getInvoicePDF('txn_01abc123');
console.log('Invoice URL:', invoice.url);
```

## Customers

```typescript
// Create customer
const customer = await paddle.customers.create({
  email: 'customer@example.com',
  name: 'John Doe'
});

// Get customer
const existing = await paddle.customers.get('ctm_01abc123');

// Update customer
await paddle.customers.update('ctm_01abc123', {
  name: 'Jane Doe'
});

// List customers
const customers = await paddle.customers.list({
  email: ['customer@example.com']
});
```

## Webhooks

### Setup Webhook Handler

```typescript
import { Paddle, EventName } from '@paddle/paddle-node-sdk';
import express from 'express';

const app = express();

app.post('/webhooks/paddle', express.raw({ type: 'application/json' }), async (req, res) => {
  const signature = req.headers['paddle-signature'] as string;
  const rawBody = req.body.toString();
  const secretKey = process.env.PADDLE_WEBHOOK_SECRET!;

  try {
    const event = paddle.webhooks.unmarshal(rawBody, secretKey, signature);

    switch (event.eventType) {
      case EventName.SubscriptionCreated:
        console.log('New subscription:', event.data.id);
        // Grant access
        break;

      case EventName.SubscriptionUpdated:
        console.log('Subscription updated:', event.data.status);
        // Handle plan changes, pauses
        break;

      case EventName.SubscriptionCanceled:
        console.log('Subscription cancelled:', event.data.id);
        // Revoke access at period end
        break;

      case EventName.TransactionCompleted:
        console.log('Payment received:', event.data.id);
        // Update billing records
        break;

      case EventName.TransactionPaymentFailed:
        console.log('Payment failed:', event.data.id);
        // Notify customer
        break;
    }

    res.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(400).json({ error: 'Invalid signature' });
  }
});
```

### Next.js Webhook Handler

```typescript
// app/api/webhooks/paddle/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { Paddle, EventName } from '@paddle/paddle-node-sdk';

const paddle = new Paddle(process.env.PADDLE_API_KEY!);

export async function POST(request: NextRequest) {
  const signature = request.headers.get('paddle-signature') || '';
  const rawBody = await request.text();

  try {
    const event = paddle.webhooks.unmarshal(
      rawBody,
      process.env.PADDLE_WEBHOOK_SECRET!,
      signature
    );

    switch (event.eventType) {
      case EventName.SubscriptionCreated:
        const customData = event.data.customData as { userId: string };
        // Update user in database
        await db.user.update({
          where: { id: customData.userId },
          data: {
            subscriptionId: event.data.id,
            subscriptionStatus: event.data.status,
          },
        });
        break;

      case EventName.SubscriptionCanceled:
        // Handle cancellation
        break;
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    return NextResponse.json({ error: 'Invalid webhook' }, { status: 400 });
  }
}
```

## Paddle Retain (Churn Prevention)

```javascript
// Initialize cancellation flow
Paddle.Retain.initCancellationFlow({
  subscriptionId: 'sub_01abc123'
});
```

## React Integration

```tsx
// components/PaddleCheckout.tsx
'use client';

import { useEffect } from 'react';

declare global {
  interface Window {
    Paddle: any;
  }
}

export function usePaddle() {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.paddle.com/paddle/v2/paddle.js';
    script.async = true;
    script.onload = () => {
      window.Paddle.Initialize({
        token: process.env.NEXT_PUBLIC_PADDLE_CLIENT_TOKEN!
      });
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);
}

export function openCheckout(priceId: string, customData?: Record<string, any>) {
  window.Paddle.Checkout.open({
    items: [{ priceId, quantity: 1 }],
    customData
  });
}
```

### Checkout Button Component

```tsx
'use client';

import { usePaddle, openCheckout } from './PaddleCheckout';

export function PricingCard({ priceId, name, price }: {
  priceId: string;
  name: string;
  price: string;
}) {
  usePaddle();

  const handleSubscribe = () => {
    openCheckout(priceId, {
      userId: 'user_123'
    });
  };

  return (
    <div className="pricing-card">
      <h3>{name}</h3>
      <p>{price}/month</p>
      <button onClick={handleSubscribe}>
        Subscribe
      </button>
    </div>
  );
}
```

## Sandbox Testing

```typescript
// Use sandbox environment
const paddle = new Paddle(process.env.PADDLE_SANDBOX_API_KEY!, {
  environment: Environment.sandbox
});
```

```javascript
// Frontend sandbox
Paddle.Environment.set('sandbox');
Paddle.Initialize({
  token: 'test_xxxxxxxxxxxxxxxxxxxxxxxx'
});
```

## Environment Variables

```bash
# Server-side
PADDLE_API_KEY=your_api_key
PADDLE_WEBHOOK_SECRET=your_webhook_secret

# Client-side
NEXT_PUBLIC_PADDLE_CLIENT_TOKEN=your_client_token

# Sandbox (for testing)
PADDLE_SANDBOX_API_KEY=your_sandbox_api_key
NEXT_PUBLIC_PADDLE_SANDBOX_TOKEN=your_sandbox_client_token
```

## Best Practices

1. **Use client tokens** - Never expose API keys in frontend
2. **Verify webhooks** - Always validate signatures server-side
3. **Test in sandbox** - Use sandbox environment for development
4. **Store custom data** - Pass userId to correlate purchases
5. **Handle all events** - Account for failed payments, cancellations
6. **Use Retain** - Reduce churn with cancellation flows
7. **Localize prices** - Use PricePreview for regional pricing
