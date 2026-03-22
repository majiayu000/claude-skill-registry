---
name: webhook-security
description: >-
  Secure webhook endpoints. Use when a user asks to verify webhook signatures,
  prevent replay attacks, handle webhook retries, or implement secure webhook
  receivers for Stripe, GitHub, Slack, or any provider.
license: Apache-2.0
compatibility: 'Any language/framework'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: devops
  tags:
    - webhooks
    - security
    - signatures
    - hmac
    - api
---

# Webhook Security

## Overview

Webhooks deliver real-time data to your app, but an open endpoint is an attack surface. Without verification, anyone can POST fake events to your webhook URL. This skill covers signature verification, replay protection, idempotency, and reliable processing patterns.

## Instructions

### Step 1: Signature Verification

Every major provider signs webhook payloads with HMAC. Verify before processing.

```typescript
// lib/webhooks/verify.ts — Generic HMAC verification
import crypto from 'crypto'

export function verifyHmacSignature(
  payload: string | Buffer,
  signature: string,
  secret: string,
  algorithm: string = 'sha256'
): boolean {
  const expected = crypto
    .createHmac(algorithm, secret)
    .update(payload)
    .digest('hex')

  // Timing-safe comparison prevents timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  )
}
```

### Step 2: Stripe Webhook Verification

```typescript
// routes/webhooks/stripe.ts — Stripe webhook handler
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!)

export async function handleStripeWebhook(req: Request) {
  const body = await req.text()                    // raw body, NOT parsed JSON
  const sig = req.headers.get('stripe-signature')!

  let event: Stripe.Event
  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message)
    return new Response('Invalid signature', { status: 400 })
  }

  // Process event idempotently
  switch (event.type) {
    case 'checkout.session.completed':
      await handleCheckoutComplete(event.data.object)
      break
    case 'invoice.payment_failed':
      await handlePaymentFailed(event.data.object)
      break
    case 'customer.subscription.deleted':
      await handleSubscriptionCanceled(event.data.object)
      break
  }

  return new Response('OK', { status: 200 })
}
```

### Step 3: Replay Protection

```typescript
// lib/webhooks/idempotency.ts — Prevent duplicate processing
import { redis } from '../redis'

export async function processOnce(
  eventId: string,
  handler: () => Promise<void>
): Promise<boolean> {
  // Set with NX (only if not exists) and 48h expiry
  const isNew = await redis.set(`webhook:${eventId}`, '1', 'NX', 'EX', 172800)

  if (!isNew) {
    console.log(`Duplicate webhook ${eventId}, skipping`)
    return false
  }

  try {
    await handler()
    return true
  } catch (err) {
    // Remove key so retry can work
    await redis.del(`webhook:${eventId}`)
    throw err
  }
}

// Usage
await processOnce(event.id, async () => {
  await db.order.update({ where: { stripeSessionId: session.id }, data: { status: 'paid' } })
})
```

### Step 4: GitHub Webhook Verification

```typescript
// routes/webhooks/github.ts — GitHub webhook handler
import crypto from 'crypto'

function verifyGitHubSignature(payload: string, signature: string, secret: string): boolean {
  const expected = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex')

  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))
}

export async function handleGitHubWebhook(req: Request) {
  const body = await req.text()
  const sig = req.headers.get('x-hub-signature-256')!

  if (!verifyGitHubSignature(body, sig, process.env.GITHUB_WEBHOOK_SECRET!)) {
    return new Response('Invalid signature', { status: 401 })
  }

  const event = req.headers.get('x-github-event')
  const payload = JSON.parse(body)

  switch (event) {
    case 'push':
      await handlePush(payload)
      break
    case 'pull_request':
      await handlePR(payload)
      break
  }

  return new Response('OK', { status: 200 })
}
```

## Guidelines

- ALWAYS verify signatures before processing. Never trust unverified webhooks.
- Use `crypto.timingSafeEqual` — regular string comparison leaks timing information.
- Parse the raw body for verification, not JSON-parsed data (parsing may alter the payload).
- Implement idempotency — webhooks are at-least-once delivery; you WILL receive duplicates.
- Return 200 quickly and process asynchronously (queue) to avoid timeout retries.
- Store webhook event IDs for 24-48h to detect replays.
