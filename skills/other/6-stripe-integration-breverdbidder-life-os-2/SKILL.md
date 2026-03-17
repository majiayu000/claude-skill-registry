---
name: stripe-integration
description: Guides consistent, correct implementation of Stripe payment processing including payment flows, webhooks, subscriptions, and customer management. Use when integrating Stripe payments, setting up subscriptions, implementing webhooks, or managing customer billing.
---

# Stripe Integration

This skill ensures Stripe payment integration is implemented correctly the first time, following best practices for security, reliability, and user experience.

## When to Use This Skill

Use this skill when:
- Adding Stripe to a new application
- Implementing subscription billing
- Setting up payment processing
- Configuring webhooks
- Managing customer lifecycle
- Handling refunds or disputes
- Implementing checkout flows

## Core Principles

**Security First**:
- Never expose secret keys client-side
- Always use HTTPS in production
- Validate webhook signatures
- Use Stripe's client-side libraries for card handling

**Idempotency**:
- Use idempotency keys for API requests
- Handle duplicate webhook events
- Design for retry-safety

**User Experience**:
- Clear error messages
- Loading states during payment
- Success/failure feedback
- Email confirmations

## Implementation Workflow

### 1. Environment Setup

**Required Credentials**:
```
STRIPE_PUBLISHABLE_KEY_TEST=pk_test_...
STRIPE_SECRET_KEY_TEST=sk_test_...
STRIPE_WEBHOOK_SECRET_TEST=whsec_...

STRIPE_PUBLISHABLE_KEY_PROD=pk_live_...
STRIPE_SECRET_KEY_PROD=sk_live_...
STRIPE_WEBHOOK_SECRET_PROD=whsec_...
```

**Never Commit**:
- Add to .env or secrets manager
- Use .gitignore for env files
- Different keys for dev/staging/prod

**Installation**:
```bash
# Node.js
npm install stripe @stripe/stripe-js

# Python
pip install stripe
```

### 2. Basic Payment Flow

**Client-Side (React example)**:
```javascript
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);

function CheckoutForm() {
  const stripe = useStripe();
  const elements = useElements();

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!stripe || !elements) return;

    // Create payment intent on backend first
    const { clientSecret } = await fetch('/api/create-payment-intent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount: 5000 }) // $50.00
    }).then(r => r.json());

    // Confirm payment on client
    const { error, paymentIntent } = await stripe.confirmCardPayment(
      clientSecret,
      {
        payment_method: {
          card: elements.getElement(CardElement),
          billing_details: {
            name: 'Customer Name',
            email: 'customer@example.com'
          }
        }
      }
    );

    if (error) {
      console.error(error.message);
    } else if (paymentIntent.status === 'succeeded') {
      // Payment successful
      console.log('Payment succeeded!');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <CardElement />
      <button type="submit" disabled={!stripe}>
        Pay
      </button>
    </form>
  );
}
```

**Server-Side (Node.js example)**:
```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

app.post('/api/create-payment-intent', async (req, res) => {
  try {
    const { amount } = req.body;

    const paymentIntent = await stripe.paymentIntents.create({
      amount: amount,
      currency: 'usd',
      automatic_payment_methods: {
        enabled: true,
      },
      metadata: {
        userId: req.user.id, // Track in your DB
        orderId: req.body.orderId
      }
    });

    res.json({ clientSecret: paymentIntent.client_secret });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### 3. Subscription Implementation

**Create Subscription**:
```javascript
// Server-side
async function createSubscription(customerId, priceId) {
  const subscription = await stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    payment_settings: {
      save_default_payment_method: 'on_subscription'
    },
    expand: ['latest_invoice.payment_intent']
  });

  return {
    subscriptionId: subscription.id,
    clientSecret: subscription.latest_invoice.payment_intent.client_secret
  };
}
```

**Handle Subscription Lifecycle**:
- Customer signs up → create customer + subscription
- Payment succeeds → activate features
- Payment fails → notify customer, retry
- Cancellation requested → process at period_end
- Renewal → webhook confirms payment

### 4. Webhook Configuration

**CRITICAL**: Webhooks are how Stripe notifies you of events. Must be implemented correctly.

**Endpoint Setup**:
```javascript
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

app.post('/webhook', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event;

  try {
    // Verify webhook signature
    event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.log(`Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      await handlePaymentSuccess(paymentIntent);
      break;

    case 'payment_intent.payment_failed':
      const failedPayment = event.data.object;
      await handlePaymentFailure(failedPayment);
      break;

    case 'customer.subscription.created':
      const subscription = event.data.object;
      await handleSubscriptionCreated(subscription);
      break;

    case 'customer.subscription.updated':
      const updatedSub = event.data.object;
      await handleSubscriptionUpdated(updatedSub);
      break;

    case 'customer.subscription.deleted':
      const deletedSub = event.data.object;
      await handleSubscriptionCanceled(deletedSub);
      break;

    case 'invoice.payment_succeeded':
      const invoice = event.data.object;
      await handleInvoicePaymentSucceeded(invoice);
      break;

    case 'invoice.payment_failed':
      const failedInvoice = event.data.object;
      await handleInvoicePaymentFailed(failedInvoice);
      break;

    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({received: true});
});
```

**Essential Events to Handle**:
1. `payment_intent.succeeded` - One-time payment successful
2. `payment_intent.payment_failed` - Payment failed
3. `customer.subscription.created` - New subscription
4. `customer.subscription.updated` - Subscription changed
5. `customer.subscription.deleted` - Subscription canceled
6. `invoice.payment_succeeded` - Recurring payment successful
7. `invoice.payment_failed` - Recurring payment failed

### 5. Customer Management

**Create Customer**:
```javascript
const customer = await stripe.customers.create({
  email: user.email,
  name: user.name,
  metadata: {
    userId: user.id
  }
});

// Store customer.id in your database
await db.users.update(user.id, {
  stripeCustomerId: customer.id
});
```

**Attach Payment Method**:
```javascript
const paymentMethod = await stripe.paymentMethods.attach(
  pm_id,
  { customer: customerId }
);

await stripe.customers.update(customerId, {
  invoice_settings: {
    default_payment_method: pm_id
  }
});
```

### 6. Testing

**Test Mode**:
- Use test keys (pk_test_, sk_test_)
- Test card numbers:
  - Success: `4242 4242 4242 4242`
  - Declined: `4000 0000 0000 0002`
  - 3D Secure: `4000 0027 6000 3184`
- Use stripe CLI for webhook testing:
  ```bash
  stripe listen --forward-to localhost:3000/webhook
  stripe trigger payment_intent.succeeded
  ```

**Webhook Testing**:
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/webhook

# Trigger events manually
stripe trigger customer.subscription.created
```

### 7. Error Handling

**Common Errors to Handle**:
```javascript
try {
  const charge = await stripe.charges.create({...});
} catch (error) {
  switch (error.type) {
    case 'StripeCardError':
      // Card was declined
      console.log('Card declined:', error.message);
      break;
    case 'StripeInvalidRequestError':
      // Invalid parameters
      console.log('Invalid request:', error.message);
      break;
    case 'StripeAPIError':
      // Stripe API error
      console.log('API error:', error.message);
      break;
    case 'StripeConnectionError':
      // Network error
      console.log('Network error');
      break;
    case 'StripeAuthenticationError':
      // Authentication error
      console.log('Auth error');
      break;
    default:
      console.log('Unknown error:', error);
  }
}
```

## Checklist for Production

Before going live:
- [ ] Using live API keys (pk_live_, sk_live_)
- [ ] HTTPS enabled everywhere
- [ ] Webhook endpoint configured in Stripe Dashboard
- [ ] Webhook signature verification implemented
- [ ] All critical events handled
- [ ] Idempotency keys on API calls
- [ ] Customer creation linked to user accounts
- [ ] Error handling for all payment flows
- [ ] Email notifications setup
- [ ] Refund process documented
- [ ] Tested with real test cards
- [ ] Webhook events tested via CLI
- [ ] Subscription renewal flow tested
- [ ] Cancellation flow tested
- [ ] Failed payment retry logic
- [ ] Security review completed

## Common Patterns

### Subscription Tiers

```javascript
const plans = {
  basic: 'price_basic123',
  pro: 'price_pro456',
  enterprise: 'price_enterprise789'
};

function subscribeToPlan(customerId, tier) {
  return stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: plans[tier] }]
  });
}
```

### Usage-Based Billing

```javascript
// Record usage
await stripe.subscriptionItems.createUsageRecord(
  subscriptionItemId,
  {
    quantity: 100,
    timestamp: Math.floor(Date.now() / 1000),
    action: 'increment'
  }
);
```

### Prorated Upgrades

```javascript
await stripe.subscriptions.update(subscriptionId, {
  items: [{
    id: subscriptionItemId,
    price: newPriceId
  }],
  proration_behavior: 'create_prorations'
});
```

## Resources

**Official Docs**:
- https://stripe.com/docs
- https://stripe.com/docs/webhooks
- https://stripe.com/docs/billing/subscriptions/overview

**Testing**:
- https://stripe.com/docs/testing
- https://stripe.com/docs/cli

**Security**:
- https://stripe.com/docs/security/guide
- https://stripe.com/docs/keys

## Tips

1. **Start Simple**: Get basic payments working before subscriptions
2. **Use Stripe Checkout**: Hosted page handles complex flows
3. **Test Webhooks Thoroughly**: Use CLI to simulate all events
4. **Log Everything**: Track payment intents, events in your DB
5. **Handle Failures Gracefully**: Retry logic, user notifications
6. **Keep Test/Prod Separate**: Never mix keys or environments
7. **Monitor Stripe Dashboard**: Check for errors and disputes
8. **Read Stripe Docs**: They're excellent and comprehensive
