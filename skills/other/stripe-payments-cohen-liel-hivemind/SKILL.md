---
name: stripe-payments
description: Stripe payments integration patterns. Use when implementing payments, subscriptions, webhooks, checkout sessions, or any payment processing with Stripe.
---

# Stripe Payments Patterns

## Setup
```python
# payments.py
import stripe
from fastapi import HTTPException

stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET
```

```typescript
// lib/stripe.ts
import Stripe from 'stripe'
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-06-20',
})
```

## One-Time Payment (Checkout Session)
```python
@router.post("/create-checkout-session")
async def create_checkout_session(user: User = Depends(get_current_user)):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": "price_xyz123",  # Price ID from Stripe dashboard
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{BASE_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{BASE_URL}/cancel",
        customer_email=user.email,
        metadata={"user_id": str(user.id)},
    )
    return {"checkout_url": session.url}
```

```typescript
// Next.js API route
export async function POST(req: Request) {
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{ price: 'price_xyz123', quantity: 1 }],
    mode: 'payment',
    success_url: `${process.env.NEXT_PUBLIC_URL}/success`,
    cancel_url: `${process.env.NEXT_PUBLIC_URL}/cancel`,
  })
  return Response.json({ url: session.url })
}
```

## Subscriptions
```python
@router.post("/create-subscription")
async def create_subscription(
    price_id: str,
    user: User = Depends(get_current_user),
):
    # Create or retrieve Stripe customer
    if not user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=user.email,
            metadata={"user_id": str(user.id)},
        )
        await db.user.update(user.id, stripe_customer_id=customer.id)
        customer_id = customer.id
    else:
        customer_id = user.stripe_customer_id

    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="subscription",
        success_url=f"{BASE_URL}/dashboard?upgraded=1",
        cancel_url=f"{BASE_URL}/pricing",
    )
    return {"checkout_url": session.url}

@router.post("/cancel-subscription")
async def cancel_subscription(user: User = Depends(get_current_user)):
    subscription = stripe.Subscription.retrieve(user.stripe_subscription_id)
    # Cancel at period end (not immediately)
    stripe.Subscription.modify(
        user.stripe_subscription_id,
        cancel_at_period_end=True,
    )
    return {"message": "Subscription will cancel at end of billing period"}
```

## Webhooks (CRITICAL — always verify signature)
```python
@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await handle_checkout_complete(session)

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        await handle_subscription_update(subscription)

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        await handle_subscription_cancel(subscription)

    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        await handle_payment_failed(invoice)

    return {"status": "ok"}

async def handle_checkout_complete(session: dict):
    user_id = session["metadata"]["user_id"]
    if session["mode"] == "subscription":
        sub_id = session["subscription"]
        subscription = stripe.Subscription.retrieve(sub_id)
        await db.user.update(
            user_id,
            stripe_subscription_id=sub_id,
            subscription_status="active",
            plan_expires_at=datetime.fromtimestamp(subscription["current_period_end"]),
        )
    elif session["mode"] == "payment":
        await db.order.create(user_id=user_id, amount=session["amount_total"])
```

## Customer Portal (self-service billing)
```python
@router.post("/billing-portal")
async def create_billing_portal(user: User = Depends(get_current_user)):
    session = stripe.billing_portal.Session.create(
        customer=user.stripe_customer_id,
        return_url=f"{BASE_URL}/dashboard",
    )
    return {"portal_url": session.url}
```

## Payment Intent (custom checkout UI)
```python
@router.post("/create-payment-intent")
async def create_payment_intent(amount: int, currency: str = "usd"):
    intent = stripe.PaymentIntent.create(
        amount=amount,  # In cents (e.g., 1999 = $19.99)
        currency=currency,
        automatic_payment_methods={"enabled": True},
    )
    return {"client_secret": intent.client_secret}
```

```typescript
// React + Stripe Elements
import { loadStripe } from '@stripe/stripe-js'
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js'

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!)

function CheckoutForm() {
  const stripe = useStripe()
  const elements = useElements()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!stripe || !elements) return

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: { return_url: `${window.location.origin}/success` },
    })

    if (error) console.error(error.message)
  }

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button type="submit" disabled={!stripe}>Pay</button>
    </form>
  )
}

function PaymentPage({ clientSecret }: { clientSecret: string }) {
  return (
    <Elements stripe={stripePromise} options={{ clientSecret }}>
      <CheckoutForm />
    </Elements>
  )
}
```

## Testing
```python
# Use Stripe test cards:
# 4242 4242 4242 4242 — success
# 4000 0000 0000 0002 — declined
# 4000 0025 0000 3155 — 3D Secure required

# Test webhooks locally:
# stripe listen --forward-to localhost:8000/webhooks/stripe
```

## Rules
- ALWAYS verify webhook signatures — never trust events without verification
- Store Stripe IDs (customer_id, subscription_id) in your DB — never call Stripe to look them up by email
- Use idempotency keys for payment creation to prevent double-charges
- Handle webhook retries — make handlers idempotent (check if already processed)
- Never log full card data — Stripe handles PCI compliance, you just handle IDs
- Use `cancel_at_period_end=True` not immediate cancellation (better UX)
- Test with Stripe CLI (`stripe listen`) before deploying webhooks
- Keep STRIPE_SECRET_KEY server-side only — publishable key is safe for client
