---
name: payment-gateway-integration
description: Integrates payment processing with Stripe, PayPal, or Square including subscriptions, webhooks, and PCI compliance. Use when implementing checkout flows, recurring billing, or handling refunds and disputes.
---

# Payment Gateway Integration

Integrate secure payment processing with proper error handling and compliance.

## Stripe Integration (Node.js)

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

class PaymentService {
  async createPaymentIntent(amount, currency, customerId) {
    return stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to cents
      currency,
      customer: customerId,
      automatic_payment_methods: { enabled: true }
    });
  }

  async createSubscription(customerId, priceId) {
    return stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: 'default_incomplete',
      expand: ['latest_invoice.payment_intent']
    });
  }

  async refund(paymentIntentId, amount = null) {
    const params = { payment_intent: paymentIntentId };
    if (amount) params.amount = Math.round(amount * 100);
    return stripe.refunds.create(params);
  }
}
```

## Webhook Handling

```javascript
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];

  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentSuccess(event.data.object);
      break;
    case 'invoice.payment_failed':
      await handlePaymentFailed(event.data.object);
      break;
  }

  res.json({ received: true });
});
```

## PayPal Integration

See [references/paypal-integration.md](references/paypal-integration.md) for complete PayPal implementation with:
- Order creation and capture
- Refund processing
- Webhook handling
- Frontend SDK integration
- Success/cancel callbacks

## Security Checklist

- [ ] Use official SDK only
- [ ] Verify webhook signatures
- [ ] Never log full card numbers
- [ ] Store minimal payment data
- [ ] Test in sandbox first
- [ ] HTTPS for all payment routes
- [ ] Handle all error cases
- [ ] Use idempotency keys
- [ ] Implement retry logic

## Best Practices

**Do:**
- Use official SDK libraries
- Verify all webhook signatures
- Log transaction IDs (not card data)
- Test in sandbox environment
- Handle all payment states
- Implement proper error messages

**Don't:**
- Process raw card data directly
- Store sensitive payment info
- Hardcode API keys
- Skip webhook signature validation
- Ignore failed payment events
- Use test keys in production
