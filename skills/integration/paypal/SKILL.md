---
name: paypal
description: Integrates PayPal payments with the JavaScript SDK for checkout buttons and card fields. Use when accepting PayPal, Venmo, Pay Later, and credit card payments in web applications.
---

# PayPal JavaScript SDK

Accept PayPal, Venmo, Pay Later, and credit/debit cards. Renders smart payment buttons that adapt to buyer preferences.

## Quick Start

```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>

<div id="paypal-button-container"></div>

<script>
paypal.Buttons({
  createOrder: async () => {
    const response = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        amount: '99.00'
      })
    });
    const data = await response.json();
    return data.id;
  },
  onApprove: async (data) => {
    const response = await fetch(`/api/orders/${data.orderID}/capture`, {
      method: 'POST'
    });
    const details = await response.json();
    alert(`Transaction completed by ${details.payer.name.given_name}`);
  }
}).render('#paypal-button-container');
</script>
```

## SDK Configuration

### Script Parameters

```html
<!-- Basic -->
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID"></script>

<!-- With options -->
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD&intent=capture&components=buttons,card-fields"></script>
```

| Parameter | Description | Values |
|-----------|-------------|--------|
| client-id | Your PayPal client ID | Required |
| currency | Transaction currency | USD, EUR, GBP, etc. |
| intent | Payment intent | capture (default), authorize |
| components | SDK components to load | buttons, card-fields, marks |
| disable-funding | Disable payment methods | credit, paylater, venmo, card |
| enable-funding | Enable payment methods | venmo, paylater |

### Dynamic Loading

```javascript
// Load SDK dynamically
function loadPayPalScript(clientId) {
  return new Promise((resolve) => {
    const script = document.createElement('script');
    script.src = `https://www.paypal.com/sdk/js?client-id=${clientId}&currency=USD`;
    script.onload = () => resolve(window.paypal);
    document.body.appendChild(script);
  });
}

const paypal = await loadPayPalScript('YOUR_CLIENT_ID');
```

## Payment Buttons

### Basic Buttons

```javascript
paypal.Buttons({
  createOrder: (data, actions) => {
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: '99.00'
        }
      }]
    });
  },
  onApprove: (data, actions) => {
    return actions.order.capture().then((details) => {
      console.log('Transaction completed:', details);
    });
  }
}).render('#paypal-button-container');
```

### Server-Side Integration (Recommended)

```javascript
paypal.Buttons({
  // Create order on server
  createOrder: async () => {
    const response = await fetch('/api/paypal/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: [
          { name: 'Product', quantity: 1, price: '99.00' }
        ]
      })
    });
    const order = await response.json();
    return order.id;
  },

  // Capture on server
  onApprove: async (data) => {
    const response = await fetch(`/api/paypal/orders/${data.orderID}/capture`, {
      method: 'POST'
    });
    const details = await response.json();

    if (details.status === 'COMPLETED') {
      // Show success message
      window.location.href = '/success';
    }
  },

  onCancel: (data) => {
    console.log('Order cancelled:', data.orderID);
    // Return to cart
  },

  onError: (err) => {
    console.error('PayPal error:', err);
    // Show error message
  }
}).render('#paypal-button-container');
```

### Button Styling

```javascript
paypal.Buttons({
  style: {
    layout: 'vertical',     // vertical, horizontal
    color: 'gold',          // gold, blue, silver, white, black
    shape: 'rect',          // rect, pill
    label: 'paypal',        // paypal, checkout, buynow, pay, subscribe
    height: 40,             // 25-55
    tagline: false          // Show "The safer, easier way to pay"
  },
  createOrder: () => { /* ... */ },
  onApprove: () => { /* ... */ }
}).render('#paypal-button-container');
```

### Standalone Buttons

```javascript
// PayPal only
paypal.Buttons({
  fundingSource: paypal.FUNDING.PAYPAL,
  createOrder: () => { /* ... */ },
  onApprove: () => { /* ... */ }
}).render('#paypal-button');

// Venmo only
paypal.Buttons({
  fundingSource: paypal.FUNDING.VENMO,
  createOrder: () => { /* ... */ },
  onApprove: () => { /* ... */ }
}).render('#venmo-button');

// Pay Later
paypal.Buttons({
  fundingSource: paypal.FUNDING.PAYLATER,
  createOrder: () => { /* ... */ },
  onApprove: () => { /* ... */ }
}).render('#paylater-button');
```

## Card Fields

Accept credit/debit cards directly on your site.

```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&components=card-fields"></script>

<div id="card-name-field-container"></div>
<div id="card-number-field-container"></div>
<div id="card-expiry-field-container"></div>
<div id="card-cvv-field-container"></div>
<button id="card-submit-button">Pay with Card</button>
```

```javascript
const cardField = paypal.CardFields({
  createOrder: async () => {
    const response = await fetch('/api/paypal/orders', {
      method: 'POST',
      body: JSON.stringify({ amount: '99.00' })
    });
    const data = await response.json();
    return data.id;
  },
  onApprove: async (data) => {
    const response = await fetch(`/api/paypal/orders/${data.orderID}/capture`, {
      method: 'POST'
    });
    const details = await response.json();
    console.log('Card payment completed:', details);
  },
  onError: (err) => {
    console.error('Card error:', err);
  }
});

// Check if card fields are eligible
if (cardField.isEligible()) {
  // Render individual fields
  cardField.NameField().render('#card-name-field-container');
  cardField.NumberField().render('#card-number-field-container');
  cardField.ExpiryField().render('#card-expiry-field-container');
  cardField.CVVField().render('#card-cvv-field-container');

  // Submit handler
  document.getElementById('card-submit-button').addEventListener('click', () => {
    cardField.submit();
  });
}
```

### Card Field Styling

```javascript
const cardField = paypal.CardFields({
  style: {
    input: {
      'font-size': '16px',
      'font-family': 'monospace',
      color: '#333'
    },
    '.invalid': {
      color: '#dc3545'
    }
  },
  createOrder: () => { /* ... */ },
  onApprove: () => { /* ... */ }
});
```

## Server-Side API (Node.js)

### Setup

```bash
npm install @paypal/paypal-server-sdk
```

```typescript
import { PayPalHttpClient, SandboxEnvironment, LiveEnvironment } from '@paypal/paypal-server-sdk';

const environment = process.env.NODE_ENV === 'production'
  ? new LiveEnvironment(
      process.env.PAYPAL_CLIENT_ID!,
      process.env.PAYPAL_CLIENT_SECRET!
    )
  : new SandboxEnvironment(
      process.env.PAYPAL_SANDBOX_CLIENT_ID!,
      process.env.PAYPAL_SANDBOX_CLIENT_SECRET!
    );

const client = new PayPalHttpClient(environment);
```

### Create Order

```typescript
// app/api/paypal/orders/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { amount, items } = await request.json();

  const accessToken = await getAccessToken();

  const response = await fetch('https://api-m.sandbox.paypal.com/v2/checkout/orders', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      intent: 'CAPTURE',
      purchase_units: [{
        amount: {
          currency_code: 'USD',
          value: amount,
          breakdown: {
            item_total: { currency_code: 'USD', value: amount }
          }
        },
        items: items.map((item: any) => ({
          name: item.name,
          quantity: String(item.quantity),
          unit_amount: {
            currency_code: 'USD',
            value: item.price
          }
        }))
      }]
    })
  });

  const order = await response.json();
  return NextResponse.json(order);
}

async function getAccessToken() {
  const auth = Buffer.from(
    `${process.env.PAYPAL_CLIENT_ID}:${process.env.PAYPAL_CLIENT_SECRET}`
  ).toString('base64');

  const response = await fetch('https://api-m.sandbox.paypal.com/v1/oauth2/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      Authorization: `Basic ${auth}`
    },
    body: 'grant_type=client_credentials'
  });

  const data = await response.json();
  return data.access_token;
}
```

### Capture Order

```typescript
// app/api/paypal/orders/[orderId]/capture/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: { orderId: string } }
) {
  const accessToken = await getAccessToken();

  const response = await fetch(
    `https://api-m.sandbox.paypal.com/v2/checkout/orders/${params.orderId}/capture`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`
      }
    }
  );

  const capture = await response.json();

  if (capture.status === 'COMPLETED') {
    // Update database, send confirmation email, etc.
    const transactionId = capture.purchase_units[0].payments.captures[0].id;
    console.log('Payment captured:', transactionId);
  }

  return NextResponse.json(capture);
}
```

## Subscriptions

```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&vault=true&intent=subscription"></script>
```

```javascript
paypal.Buttons({
  style: {
    label: 'subscribe'
  },
  createSubscription: (data, actions) => {
    return actions.subscription.create({
      plan_id: 'P-XXXXXXXXXXXXXXXXXXXXXXXX'
    });
  },
  onApprove: (data) => {
    console.log('Subscription ID:', data.subscriptionID);
    // Save subscription ID to database
  }
}).render('#paypal-button-container');
```

### Server-Side Subscription Management

```typescript
// Create subscription plan
async function createPlan(accessToken: string) {
  const response = await fetch('https://api-m.sandbox.paypal.com/v1/billing/plans', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      product_id: 'PROD-XXXXX',
      name: 'Monthly Plan',
      billing_cycles: [{
        frequency: { interval_unit: 'MONTH', interval_count: 1 },
        tenure_type: 'REGULAR',
        sequence: 1,
        total_cycles: 0,
        pricing_scheme: {
          fixed_price: { value: '9.99', currency_code: 'USD' }
        }
      }],
      payment_preferences: {
        auto_bill_outstanding: true,
        payment_failure_threshold: 3
      }
    })
  });

  return response.json();
}

// Cancel subscription
async function cancelSubscription(subscriptionId: string, accessToken: string) {
  await fetch(
    `https://api-m.sandbox.paypal.com/v1/billing/subscriptions/${subscriptionId}/cancel`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        reason: 'Customer requested cancellation'
      })
    }
  );
}
```

## Webhooks

### Setup Webhook Handler

```typescript
// app/api/webhooks/paypal/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const body = await request.json();
  const headers = Object.fromEntries(request.headers);

  // Verify webhook signature
  const isValid = await verifyWebhookSignature(headers, body);
  if (!isValid) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const eventType = body.event_type;

  switch (eventType) {
    case 'CHECKOUT.ORDER.APPROVED':
      console.log('Order approved:', body.resource.id);
      break;

    case 'PAYMENT.CAPTURE.COMPLETED':
      console.log('Payment captured:', body.resource.id);
      // Fulfill order
      break;

    case 'PAYMENT.CAPTURE.DENIED':
      console.log('Payment denied:', body.resource.id);
      // Handle failed payment
      break;

    case 'BILLING.SUBSCRIPTION.CREATED':
      console.log('Subscription created:', body.resource.id);
      break;

    case 'BILLING.SUBSCRIPTION.ACTIVATED':
      console.log('Subscription activated:', body.resource.id);
      // Grant access
      break;

    case 'BILLING.SUBSCRIPTION.CANCELLED':
      console.log('Subscription cancelled:', body.resource.id);
      // Revoke access
      break;

    case 'PAYMENT.SALE.COMPLETED':
      console.log('Subscription payment:', body.resource.id);
      // Update billing records
      break;
  }

  return NextResponse.json({ received: true });
}

async function verifyWebhookSignature(headers: any, body: any) {
  const accessToken = await getAccessToken();

  const response = await fetch(
    'https://api-m.sandbox.paypal.com/v1/notifications/verify-webhook-signature',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        auth_algo: headers['paypal-auth-algo'],
        cert_url: headers['paypal-cert-url'],
        transmission_id: headers['paypal-transmission-id'],
        transmission_sig: headers['paypal-transmission-sig'],
        transmission_time: headers['paypal-transmission-time'],
        webhook_id: process.env.PAYPAL_WEBHOOK_ID,
        webhook_event: body
      })
    }
  );

  const result = await response.json();
  return result.verification_status === 'SUCCESS';
}
```

## React Integration

```tsx
// components/PayPalButton.tsx
'use client';

import { useEffect, useRef } from 'react';

interface PayPalButtonProps {
  amount: string;
  onSuccess: (details: any) => void;
}

export function PayPalButton({ amount, onSuccess }: PayPalButtonProps) {
  const buttonRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const script = document.createElement('script');
    script.src = `https://www.paypal.com/sdk/js?client-id=${process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID}&currency=USD`;
    script.async = true;

    script.onload = () => {
      if (buttonRef.current) {
        window.paypal.Buttons({
          createOrder: async () => {
            const response = await fetch('/api/paypal/orders', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ amount })
            });
            const order = await response.json();
            return order.id;
          },
          onApprove: async (data: any) => {
            const response = await fetch(
              `/api/paypal/orders/${data.orderID}/capture`,
              { method: 'POST' }
            );
            const details = await response.json();
            onSuccess(details);
          }
        }).render(buttonRef.current);
      }
    };

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, [amount, onSuccess]);

  return <div ref={buttonRef} />;
}
```

### Using @paypal/react-paypal-js

```bash
npm install @paypal/react-paypal-js
```

```tsx
import { PayPalScriptProvider, PayPalButtons } from '@paypal/react-paypal-js';

function App() {
  return (
    <PayPalScriptProvider options={{
      clientId: process.env.NEXT_PUBLIC_PAYPAL_CLIENT_ID!,
      currency: 'USD'
    }}>
      <PayPalButtons
        style={{ layout: 'vertical' }}
        createOrder={async () => {
          const response = await fetch('/api/paypal/orders', {
            method: 'POST',
            body: JSON.stringify({ amount: '99.00' })
          });
          const order = await response.json();
          return order.id;
        }}
        onApprove={async (data) => {
          const response = await fetch(
            `/api/paypal/orders/${data.orderID}/capture`,
            { method: 'POST' }
          );
          const details = await response.json();
          console.log('Success:', details);
        }}
      />
    </PayPalScriptProvider>
  );
}
```

## Environment Variables

```bash
# Production
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_WEBHOOK_ID=your_webhook_id

# Sandbox (testing)
PAYPAL_SANDBOX_CLIENT_ID=your_sandbox_client_id
PAYPAL_SANDBOX_CLIENT_SECRET=your_sandbox_client_secret

# Client-side
NEXT_PUBLIC_PAYPAL_CLIENT_ID=your_client_id
```

## API Endpoints

| Environment | Base URL |
|-------------|----------|
| Sandbox | https://api-m.sandbox.paypal.com |
| Production | https://api-m.paypal.com |

## Best Practices

1. **Server-side capture** - Always capture payments server-side
2. **Verify webhooks** - Validate signatures before processing
3. **Test in sandbox** - Use sandbox environment for development
4. **Handle errors** - Implement onError and onCancel handlers
5. **Store transaction IDs** - Save for refunds and disputes
6. **Idempotent handlers** - Webhooks may be delivered multiple times
7. **Show loading states** - Disable buttons during processing
