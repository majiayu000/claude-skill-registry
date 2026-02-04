---
name: payments
description: Payment integration expert for Stripe, PayPal, and marketplace payments (Stripe Connect). Checkout flows, webhooks, subscriptions, Direct/Destination Charge patterns, and idempotent payment processing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Payments Expert - Stripe, PayPal, Connect

Comprehensive payment processing expertise for Stripe, PayPal, and marketplace payments.

## Stripe Checkout (Quick Start)

```python
import stripe

session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'Premium'},
            'unit_amount': 2000,  # $20.00
        },
        'quantity': 1,
    }],
    mode='payment',  # or 'subscription'
    success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://example.com/cancel',
)
# Redirect to session.url
```

## Webhook Handling

```python
@app.route('/webhook', methods=['POST'])
def webhook():
    event = stripe.Webhook.construct_event(
        request.data,
        request.headers.get('Stripe-Signature'),
        webhook_secret
    )

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        await confirm_payment(session.id)

    return 'Success', 200
```

### Critical Events

| Event | Use Case |
|-------|----------|
| `checkout.session.completed` | Payment successful |
| `payment_intent.payment_failed` | Payment failed |
| `customer.subscription.updated` | Subscription changed |
| `account.updated` | Connect account status |

## Stripe Connect (Marketplaces)

### Charge Types

| Type | Who Creates | Webhook Location |
|------|-------------|------------------|
| **Direct** | Connected Account | Connect endpoint |
| **Destination** | Platform | Platform endpoint |

### Direct Charge Webhook Setup

```python
# /webhooks/stripe/connect - CRITICAL for Direct Charge!
@app.route('/webhooks/stripe/connect', methods=['POST'])
def connect_webhook():
    event = stripe.webhooks.constructEvent(
        request.data, sig, connect_webhook_secret
    )

    if event['type'] == 'checkout.session.completed':
        # Direct Charge sessions complete here!
        await handle_connect_checkout(event.data.object)
```

## Critical Patterns

### Dual Confirmation (Webhook + Frontend)

```typescript
// Both webhook and frontend call this - idempotent!
async function confirmPayment(sessionId: string) {
  const result = await db.update(orders)
    .set({ status: 'paid' })
    .where(and(
      eq(orders.stripeSessionId, sessionId),
      eq(orders.status, 'pending')  // Only if pending!
    ));

  if (result.changes === 0) return false; // Already processed
  await decrementInventory(sessionId);
  return true;
}
```

### 100% Promo Code Detection

```python
# ✅ CORRECT - amount_total=0 + payment_status='paid'
def is_100_percent_promo(session):
    return (
        session.payment_status == 'paid' and
        session.amount_total == 0 and
        session.payment_intent is None
    )

# ❌ WRONG - no_payment_required is different!
```

### Web vs Native Browser Handling

```typescript
// WebBrowser result types differ by platform!
switch (result.type) {
  case 'dismiss':  // Native: browser closed - NOW verify
    await verifyPayment(sessionId);
    break;
  case 'opened':   // Web: user still on Stripe page - DON'T verify yet!
    Alert.alert('Complete payment in browser');
    break;
}
```

## Subscriptions

```python
subscription = stripe.Subscription.create(
    customer=customer_id,
    items=[{'price': price_id}],
    payment_behavior='default_incomplete',
    expand=['latest_invoice.payment_intent'],
)
```

## PayPal Integration

```javascript
// PayPal SDK
paypal.Buttons({
  createOrder: (data, actions) => {
    return actions.order.create({
      purchase_units: [{ amount: { value: '20.00' } }]
    });
  },
  onApprove: async (data, actions) => {
    const order = await actions.order.capture();
    await verifyPayment(order.id);
  }
}).render('#paypal-button');
```

## Testing

```python
TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
}
```

## Best Practices

1. **Always use webhooks** - Don't rely on frontend only
2. **Idempotency** - Handle duplicate events
3. **Verify signatures** - Always validate webhooks
4. **Never store raw card data** - Use Stripe Elements
5. **Implement SCA** - 3D Secure for Europe

## Related Skills

- `billing` - Subscription management
- `compliance` - PCI compliance
