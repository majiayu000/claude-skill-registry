---
name: checkout
description: Checkout flow with cart, shipping, Stripe/PayPal payments, and order completion. Use when modifying checkout, debugging payment issues, or implementing checkout features.
---

# Checkout Flow Guide

Complete checkout system with Stripe and PayPal integration.

## Checkout Flow Overview

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│  Cart   │───▶│ Customer │───▶│ Shipping │───▶│ Payment │───▶│ Complete │
└─────────┘    └──────────┘    └──────────┘    └─────────┘    └──────────┘
     │              │               │               │               │
     ▼              ▼               ▼               ▼               ▼
 Create         Set email      Set address     Stripe or       Create
 checkout       (guest or      + method        PayPal          order
                 login)
```

## API Endpoints

| Endpoint                                   | Method | Purpose                     |
| ------------------------------------------ | ------ | --------------------------- |
| `/api/checkout/create`                     | POST   | Create checkout from cart   |
| `/api/checkout/$id`                        | GET    | Get checkout state          |
| `/api/checkout/$id/customer`               | POST   | Set customer email          |
| `/api/checkout/$id/shipping-address`       | POST   | Set shipping address        |
| `/api/checkout/$id/shipping-rates`         | GET    | Get shipping options        |
| `/api/checkout/$id/shipping-method`        | POST   | Select shipping method      |
| `/api/checkout/$id/payment/stripe`         | POST   | Create Stripe PaymentIntent |
| `/api/checkout/$id/payment/paypal`         | POST   | Create PayPal order         |
| `/api/checkout/$id/payment/paypal.capture` | POST   | Capture PayPal payment      |
| `/api/checkout/$id/complete`               | POST   | Complete checkout           |

## Step 1: Create Checkout

```typescript
// src/routes/api/checkout/create.ts
POST: async ({ request }) => {
  const { items } = await request.json()
  // items: [{ productId, variantId, quantity }]

  // Validate and get current prices
  const cartItems = await Promise.all(
    items.map(async (item) => {
      const [variant] = await db
        .select()
        .from(productVariants)
        .where(eq(productVariants.id, item.variantId))
        .limit(1)

      const [product] = await db
        .select()
        .from(products)
        .where(eq(products.id, item.productId))
        .limit(1)

      return {
        productId: item.productId,
        variantId: item.variantId,
        quantity: item.quantity,
        title: product.name.en,
        variantTitle: variant.title,
        sku: variant.sku,
        price: parseFloat(variant.price),
        imageUrl: null, // Fetch image separately
      }
    }),
  )

  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0,
  )

  const [checkout] = await db
    .insert(checkouts)
    .values({
      cartItems,
      subtotal: subtotal.toFixed(2),
      total: subtotal.toFixed(2),
      currency: 'USD',
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
    })
    .returning()

  // Set checkout session cookie
  const token = generateCheckoutToken(checkout.id)
  const response = successResponse({ checkout }, 201)
  setCheckoutCookie(response, token)

  return response
}
```

## Step 2: Set Customer

```typescript
// src/routes/api/checkout/$checkoutId/customer.ts
POST: async ({ request, params }) => {
  const { checkoutId } = params
  const { email, createAccount, password } = await request.json()

  // Validate checkout access
  const validation = await validateCheckoutAccess(request, checkoutId)
  if (!validation.valid) {
    return simpleErrorResponse(validation.error, 401)
  }

  // Check if user exists
  const session = await validateSession(request)

  if (session.success) {
    // Logged in user - link to their customer record
    let [customer] = await db
      .select()
      .from(customers)
      .where(eq(customers.userId, session.user.id))
      .limit(1)

    if (!customer) {
      ;[customer] = await db
        .insert(customers)
        .values({
          userId: session.user.id,
          email: session.user.email,
        })
        .returning()
    }

    await db
      .update(checkouts)
      .set({ customerId: customer.id, email: customer.email })
      .where(eq(checkouts.id, checkoutId))
  } else {
    // Guest checkout
    await db
      .update(checkouts)
      .set({ email })
      .where(eq(checkouts.id, checkoutId))
  }

  return successResponse({ success: true })
}
```

## Step 3: Shipping Address

```typescript
// src/routes/api/checkout/$checkoutId/shipping-address.ts
POST: async ({ request, params }) => {
  const { checkoutId } = params
  const address = await request.json()

  // Validate required fields
  const required = [
    'firstName',
    'lastName',
    'address1',
    'city',
    'country',
    'countryCode',
    'zip',
  ]
  for (const field of required) {
    if (!address[field]?.trim()) {
      return simpleErrorResponse(`${field} is required`)
    }
  }

  const [updated] = await db
    .update(checkouts)
    .set({
      shippingAddress: address,
      updatedAt: new Date(),
    })
    .where(eq(checkouts.id, checkoutId))
    .returning()

  return successResponse({ checkout: updated })
}
```

## Step 4: Shipping Method

```typescript
// GET shipping rates
GET: async ({ request, params }) => {
  const rates = await db
    .select()
    .from(shippingRates)
    .where(eq(shippingRates.isActive, true))
    .orderBy(asc(shippingRates.position))

  return successResponse({ rates })
}

// POST select shipping method
POST: async ({ request, params }) => {
  const { checkoutId } = params
  const { shippingRateId } = await request.json()

  const [rate] = await db
    .select()
    .from(shippingRates)
    .where(eq(shippingRates.id, shippingRateId))
    .limit(1)

  if (!rate) {
    return simpleErrorResponse('Invalid shipping rate')
  }

  const [checkout] = await db
    .select()
    .from(checkouts)
    .where(eq(checkouts.id, checkoutId))
    .limit(1)

  const subtotal = parseFloat(checkout.subtotal)
  const shippingTotal = parseFloat(rate.price)
  const taxTotal = calculateTax(subtotal + shippingTotal)
  const total = subtotal + shippingTotal + taxTotal

  const [updated] = await db
    .update(checkouts)
    .set({
      shippingRateId: rate.id,
      shippingMethod: rate.name,
      shippingTotal: shippingTotal.toFixed(2),
      taxTotal: taxTotal.toFixed(2),
      total: total.toFixed(2),
      updatedAt: new Date(),
    })
    .where(eq(checkouts.id, checkoutId))
    .returning()

  return successResponse({ checkout: updated })
}
```

## Step 5a: Stripe Payment

```typescript
// src/routes/api/checkout/$checkoutId/payment/stripe.ts
import Stripe from 'stripe'
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

POST: async ({ request, params }) => {
  const { checkoutId } = params

  const [checkout] = await db
    .select()
    .from(checkouts)
    .where(eq(checkouts.id, checkoutId))
    .limit(1)

  if (!checkout) {
    return simpleErrorResponse('Checkout not found', 404)
  }

  // Create PaymentIntent
  const paymentIntent = await stripe.paymentIntents.create({
    amount: Math.round(parseFloat(checkout.total) * 100), // cents
    currency: checkout.currency.toLowerCase(),
    metadata: {
      checkoutId: checkout.id,
    },
  })

  return successResponse({
    clientSecret: paymentIntent.client_secret,
  })
}
```

### Frontend Stripe Integration

```typescript
import { loadStripe } from '@stripe/stripe-js'
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js'

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_KEY!)

function CheckoutPayment({ clientSecret }: { clientSecret: string }) {
  return (
    <Elements stripe={stripePromise} options={{ clientSecret }}>
      <PaymentForm />
    </Elements>
  )
}

function PaymentForm() {
  const stripe = useStripe()
  const elements = useElements()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!stripe || !elements) return

    const { error } = await stripe.confirmPayment({
      elements,
      confirmParams: {
        return_url: `${window.location.origin}/checkout/complete`,
      },
    })

    if (error) {
      console.error(error.message)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button type="submit" disabled={!stripe}>
        Pay Now
      </button>
    </form>
  )
}
```

## Step 5b: PayPal Payment

```typescript
// src/routes/api/checkout/$checkoutId/payment/paypal.ts
POST: async ({ request, params }) => {
  const { checkoutId } = params

  const [checkout] = await db
    .select()
    .from(checkouts)
    .where(eq(checkouts.id, checkoutId))
    .limit(1)

  const order = await paypalClient.orders.create({
    intent: 'CAPTURE',
    purchase_units: [
      {
        amount: {
          currency_code: checkout.currency,
          value: checkout.total,
        },
      },
    ],
  })

  return successResponse({ orderID: order.id })
}

// Capture payment
// src/routes/api/checkout/$checkoutId/payment/paypal.capture.ts
POST: async ({ request, params }) => {
  const { orderID } = await request.json()

  const capture = await paypalClient.orders.capture(orderID)

  if (capture.status === 'COMPLETED') {
    await completeCheckout(params.checkoutId, 'paypal', orderID)
  }

  return successResponse({ status: capture.status })
}
```

## Step 6: Complete Checkout

```typescript
// src/routes/api/checkout/$checkoutId/complete.ts
async function completeCheckout(
  checkoutId: string,
  paymentProvider: 'stripe' | 'paypal',
  paymentId: string,
) {
  return await db.transaction(async (tx) => {
    // Get checkout
    const [checkout] = await tx
      .select()
      .from(checkouts)
      .where(eq(checkouts.id, checkoutId))
      .limit(1)

    if (!checkout) throw new Error('Checkout not found')
    if (checkout.completedAt) throw new Error('Already completed')

    // Create or get customer
    let customerId = checkout.customerId

    if (!customerId && checkout.email) {
      // Create guest customer
      const [customer] = await tx
        .insert(customers)
        .values({ email: checkout.email })
        .returning()
      customerId = customer.id
    }

    // Create order
    const [order] = await tx
      .insert(orders)
      .values({
        customerId,
        email: checkout.email!,
        subtotal: checkout.subtotal,
        shippingTotal: checkout.shippingTotal || '0',
        taxTotal: checkout.taxTotal || '0',
        total: checkout.total,
        currency: checkout.currency,
        status: 'pending',
        paymentStatus: 'paid',
        fulfillmentStatus: 'unfulfilled',
        shippingMethod: checkout.shippingMethod,
        shippingAddress: checkout.shippingAddress!,
        billingAddress: checkout.billingAddress,
        paymentProvider,
        paymentId,
        paidAt: new Date(),
      })
      .returning()

    // Create order items from cart snapshot
    await tx.insert(orderItems).values(
      checkout.cartItems.map((item) => ({
        orderId: order.id,
        productId: item.productId,
        variantId: item.variantId,
        title: item.title,
        variantTitle: item.variantTitle,
        sku: item.sku,
        price: item.price.toFixed(2),
        quantity: item.quantity,
        total: (item.price * item.quantity).toFixed(2),
        imageUrl: item.imageUrl,
      })),
    )

    // Mark checkout complete
    await tx
      .update(checkouts)
      .set({ completedAt: new Date() })
      .where(eq(checkouts.id, checkoutId))

    // Record audit trail
    await tx.insert(orderStatusHistory).values({
      orderId: order.id,
      field: 'status',
      previousValue: '',
      newValue: 'pending',
      changedBy: 'system',
    })

    return order
  })
}
```

## Webhook Handlers

### Stripe Webhook

```typescript
// src/routes/api/webhooks/stripe.ts
POST: async ({ request }) => {
  const sig = request.headers.get('stripe-signature')
  if (!sig) return new Response('Missing signature', { status: 400 })

  const body = await request.text()

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!,
    )

    switch (event.type) {
      case 'payment_intent.succeeded': {
        const paymentIntent = event.data.object as Stripe.PaymentIntent
        const checkoutId = paymentIntent.metadata.checkoutId

        if (checkoutId) {
          await completeCheckout(checkoutId, 'stripe', paymentIntent.id)
        }
        break
      }

      case 'payment_intent.payment_failed': {
        const paymentIntent = event.data.object as Stripe.PaymentIntent
        console.error('Payment failed:', paymentIntent.id)
        break
      }
    }

    return new Response('OK')
  } catch (err) {
    console.error('Webhook error:', err)
    return new Response('Webhook error', { status: 400 })
  }
}
```

### PayPal Webhook

```typescript
// src/routes/api/webhooks/paypal.ts
POST: async ({ request }) => {
  const body = await request.json()

  // Verify webhook signature
  const isValid = await verifyPayPalWebhook(request, body)
  if (!isValid) {
    return new Response('Invalid signature', { status: 400 })
  }

  switch (body.event_type) {
    case 'CHECKOUT.ORDER.APPROVED':
      // Order approved, ready for capture
      break

    case 'PAYMENT.CAPTURE.COMPLETED':
      // Payment captured successfully
      const orderId = body.resource.supplementary_data.related_ids.order_id
      // Complete checkout if not already done
      break
  }

  return new Response('OK')
}
```

## Tax Calculation

```typescript
// src/lib/tax.ts
export const TAX_RATE = 0.0825 // 8.25%

export function calculateTax(amount: number): number {
  return Math.round(amount * TAX_RATE * 100) / 100
}
```

## Checkout Authentication

```typescript
// src/lib/checkout-auth.ts
import { createHmac, timingSafeEqual } from 'crypto'

const SECRET = process.env.CHECKOUT_SECRET!

export function generateCheckoutToken(checkoutId: string): string {
  return createHmac('sha256', SECRET).update(checkoutId).digest('hex')
}

export function setCheckoutCookie(response: Response, token: string) {
  response.headers.append(
    'Set-Cookie',
    `checkout_session=${token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=86400`,
  )
}

export async function validateCheckoutAccess(
  request: Request,
  checkoutId: string,
): Promise<{ valid: boolean; error?: string }> {
  // Check checkout exists and not expired
  const [checkout] = await db
    .select()
    .from(checkouts)
    .where(eq(checkouts.id, checkoutId))
    .limit(1)

  if (!checkout) return { valid: false, error: 'Checkout not found' }
  if (checkout.completedAt) return { valid: false, error: 'Already completed' }
  if (checkout.expiresAt < new Date()) return { valid: false, error: 'Expired' }

  // Validate token
  const cookie = request.headers.get('cookie')
  const token = parseCookie(cookie, 'checkout_session')
  const expected = generateCheckoutToken(checkoutId)

  if (!token || !timingSafeEqual(Buffer.from(token), Buffer.from(expected))) {
    return { valid: false, error: 'Invalid session' }
  }

  return { valid: true }
}
```

## Debugging Checklist

- [ ] Checkout not expired (`expiresAt > now`)
- [ ] Checkout not completed (`completedAt` is null)
- [ ] Session cookie present and valid
- [ ] Cart items snapshot has valid prices
- [ ] Shipping address set before payment
- [ ] Shipping method selected before payment
- [ ] Stripe/PayPal webhook configured correctly
- [ ] Webhook signature verification passing

## See Also

- `src/routes/api/checkout/` - All checkout endpoints
- `src/routes/api/webhooks/` - Payment webhooks
- `src/lib/checkout-auth.ts` - Checkout authentication
- `src/lib/stripe.ts` - Stripe client
- `src/lib/paypal.ts` - PayPal client
- `src/lib/tax.ts` - Tax calculation
- `security` skill - Checkout security patterns
