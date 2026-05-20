---
name: stripe-api-integration
description: Integrate Stripe payment processing including customers, payment intents, subscriptions, webhooks. Use when implementing payments, working with Stripe API, or when user mentions Stripe, payments, subscriptions, or billing.
license: MIT
compatibility: Requires Python 3.7+ and the Stripe Python library
---

# Stripe API Integration

Integrate Stripe payment processing into applications with customers, payments, subscriptions, and webhooks.

## When to Use

- Implementing payment processing
- Creating subscription billing
- Managing customer accounts
- Handling payment webhooks
- Testing payment flows

## Prerequisites

1. **Stripe account**: Sign up at https://stripe.com
2. **API keys**: Get from Stripe Dashboard → Developers → API keys
   - Use test keys (pk_test_..., sk_test_...) for development
3. **Python library**: Install Stripe SDK
   ```bash
   pip install stripe
   ```

## Quick Start

### 1. Initialize Stripe

```python
import stripe

# Set your secret key
stripe.api_key = "sk_test_..."  # Use environment variable in production

# Test connection
try:
    account = stripe.Account.retrieve()
    print(f"Connected to Stripe account: {account.id}")
except stripe.error.AuthenticationError:
    print("Invalid API key")
```

### 2. Create a Customer

```python
customer = stripe.Customer.create(
    email="customer@example.com",
    name="John Doe",
    description="Customer for testing"
)

print(f"Created customer: {customer.id}")
```

### 3. Create a Payment Intent

```python
payment_intent = stripe.PaymentIntent.create(
    amount=2000,  # Amount in cents ($20.00)
    currency="usd",
    customer=customer.id,
    payment_method_types=["card"],
    description="Example payment"
)

print(f"Payment Intent: {payment_intent.id}")
print(f"Client Secret: {payment_intent.client_secret}")
# Send client_secret to frontend for payment confirmation
```

## Common Operations

### Customer Management

**Create customer**:
```python
customer = stripe.Customer.create(
    email="user@example.com",
    name="Jane Smith",
    metadata={"user_id": "12345"}  # Your internal ID
)
```

**Retrieve customer**:
```python
customer = stripe.Customer.retrieve("cus_ABC123")
```

**Update customer**:
```python
stripe.Customer.modify(
    "cus_ABC123",
    email="newemail@example.com",
    metadata={"tier": "premium"}
)
```

**List customers**:
```python
customers = stripe.Customer.list(limit=10)
for customer in customers.auto_paging_iter():
    print(customer.email)
```

### Payment Processing

**One-time payment** (full flow):
```python
# 1. Create payment intent
payment_intent = stripe.PaymentIntent.create(
    amount=5000,  # $50.00
    currency="usd",
    customer="cus_ABC123",
    payment_method_types=["card"]
)

# 2. Send client_secret to frontend
client_secret = payment_intent.client_secret

# 3. Frontend confirms with Stripe.js
# (This happens in JavaScript on the frontend)

# 4. Check payment status (after confirmation)
intent = stripe.PaymentIntent.retrieve(payment_intent.id)
if intent.status == "succeeded":
    print("Payment successful!")
```

**Charge a saved card**:
```python
# If customer has default payment method
payment_intent = stripe.PaymentIntent.create(
    amount=1000,
    currency="usd",
    customer="cus_ABC123",
    payment_method="pm_card_visa",  # Payment method ID
    confirm=True,  # Immediately attempt to charge
    return_url="https://example.com/return"
)
```

### Subscription Management

**Create subscription**:
```python
subscription = stripe.Subscription.create(
    customer="cus_ABC123",
    items=[{"price": "price_ABC123"}],  # Price ID from dashboard
    payment_behavior="default_incomplete",
    expand=["latest_invoice.payment_intent"]
)

# Send client_secret to frontend for payment confirmation
client_secret = subscription.latest_invoice.payment_intent.client_secret
```

**Cancel subscription**:
```python
# Cancel at end of period
stripe.Subscription.modify(
    "sub_ABC123",
    cancel_at_period_end=True
)

# Cancel immediately
stripe.Subscription.delete("sub_ABC123")
```

**Update subscription**:
```python
# Change plan
stripe.Subscription.modify(
    "sub_ABC123",
    items=[{
        "id": subscription_item_id,
        "price": "price_NEW123"  # New price ID
    }]
)
```

### Webhook Handling

**Setup endpoint**:
```python
from flask import Flask, request
import stripe

app = Flask(__name__)
endpoint_secret = "whsec_..."  # From Stripe Dashboard

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400
    
    # Handle the event
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        print(f"Payment succeeded: {payment_intent.id}")
        # Update your database, send confirmation email, etc.
    
    elif event.type == "customer.subscription.deleted":
        subscription = event.data.object
        print(f"Subscription canceled: {subscription.id}")
        # Revoke access, update user's subscription status
    
    return {"status": "success"}
```

**Important webhook events**:
- `payment_intent.succeeded` - Payment completed
- `payment_intent.payment_failed` - Payment failed
- `customer.subscription.created` - New subscription
- `customer.subscription.updated` - Subscription changed
- `customer.subscription.deleted` - Subscription canceled
- `invoice.payment_failed` - Subscription payment failed

For complete webhook event reference, see `references/WEBHOOK_EVENTS.md`.

## Error Handling

Stripe errors should be caught and handled appropriately:

```python
import stripe

try:
    payment_intent = stripe.PaymentIntent.create(
        amount=1000,
        currency="usd",
        customer="cus_ABC123"
    )
except stripe.error.CardError as e:
    # Card was declined
    print(f"Card error: {e.user_message}")
except stripe.error.RateLimitError:
    # Too many requests
    print("Rate limit exceeded, retry later")
except stripe.error.InvalidRequestError as e:
    # Invalid parameters
    print(f"Invalid request: {e}")
except stripe.error.AuthenticationError:
    # Invalid API key
    print("Authentication failed")
except stripe.error.APIConnectionError:
    # Network issue
    print("Network error, retry")
except stripe.error.StripeError as e:
    # Generic Stripe error
    print(f"Stripe error: {e}")
except Exception as e:
    # Non-Stripe error
    print(f"Unexpected error: {e}")
```

For complete error types and handling, see `references/ERROR_HANDLING.md`.

## Testing

### Use Test Cards

Stripe provides test card numbers:

```python
# Success
# Card: 4242 4242 4242 4242
# Exp: Any future date, CVC: Any 3 digits

# Decline
# Card: 4000 0000 0000 0002

# Requires authentication (3D Secure)
# Card: 4000 0027 6000 3184
```

### Test Mode

Always use test keys for development:
```python
stripe.api_key = "sk_test_..."  # Test secret key
```

Test mode data is completely separate from live mode.

### Test Webhooks Locally

Use Stripe CLI to forward webhooks to localhost:
```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:5000/webhook
```

## Best Practices

1. **Use environment variables** for API keys:
   ```python
   import os
   stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
   ```

2. **Store customer IDs** in your database to link Stripe customers to your users

3. **Use idempotency keys** for critical operations:
   ```python
   stripe.PaymentIntent.create(
       amount=1000,
       currency="usd",
       idempotency_key="order_12345"  # Prevents duplicate charges
   )
   ```

4. **Verify webhook signatures** to ensure requests are from Stripe

5. **Handle errors gracefully** and provide user-friendly messages

6. **Use test mode** extensively before going live

7. **Implement proper logging** for payment operations

8. **Store metadata** to link Stripe objects to your system:
   ```python
   metadata={"order_id": "12345", "user_id": "67890"}
   ```

For comprehensive best practices, see `references/BEST_PRACTICES.md`.

## Troubleshooting

### Authentication Failed
**Problem**: `stripe.error.AuthenticationError`
**Solution**: 
- Verify API key is correct
- Ensure using secret key (sk_...) not publishable key (pk_...)
- Check key matches environment (test vs live)

### Payment Intent Requires Action
**Problem**: Payment intent status is `requires_action`
**Solution**: 
- Customer needs to complete authentication (3D Secure)
- Send `client_secret` to frontend for confirmation
- Use Stripe.js to handle authentication flow

### Invalid Request
**Problem**: `stripe.error.InvalidRequestError`
**Solution**:
- Check API parameters match documentation
- Verify resource IDs are valid
- Ensure required fields are provided

### Rate Limit Exceeded
**Problem**: `stripe.error.RateLimitError`
**Solution**:
- Implement exponential backoff
- Reduce request frequency
- Contact Stripe to increase rate limits if needed

For more troubleshooting, see `references/TROUBLESHOOTING.md`.

## Additional Resources

- **Complete API reference**: `references/API_REFERENCE.md`
- **Webhook events guide**: `references/WEBHOOK_EVENTS.md`
- **Error handling patterns**: `references/ERROR_HANDLING.md`
- **Testing strategies**: `references/TESTING.md`
- **Best practices**: `references/BEST_PRACTICES.md`
- **Troubleshooting guide**: `references/TROUBLESHOOTING.md`

## Official Documentation

- Stripe API Docs: https://stripe.com/docs/api
- Python Library: https://stripe.com/docs/api/python
- Testing: https://stripe.com/docs/testing
- Webhooks: https://stripe.com/docs/webhooks
