---
name: stripe-design
description: |
  Design a Stripe integration based on business requirements and organizational preferences.
  Produces a design document that stripe-scaffold will implement.
---

# Stripe Design

Create a design document for Stripe integration.

## Objective

Produce a clear, implementable design that follows our business model preferences and current Stripe best practices.

## Process

**1. Understand Requirements**

What does this app need? Usually one of:
- Subscription billing (most common)
- One-time payments
- Both

Reference `business-model-preferences` for constraints: single tier, trial with completion on upgrade, no freemium.

**2. Research Current Patterns**

Stripe's API evolves. Before designing:
- Use Gemini to check current Stripe Checkout best practices
- Verify webhook event recommendations
- Check if there are new patterns for your use case

Don't assume last year's patterns are still optimal.

**3. Design the Integration**

Produce a design document covering:

**Checkout Flow**
- Embedded or redirect?
- What mode? (subscription, payment, setup)
- Customer creation strategy
- Success/cancel URLs

**Webhook Events**
- Which events to handle?
- Idempotency strategy
- Error handling approach

**Subscription State**
- What fields to store locally?
- Access control logic
- Trial handling

**Price Structure**
- Monthly price (and annual if applicable)
- Trial duration

**4. Get Validation**

Run the design through Thinktank for multi-perspective review. Billing is critical — get expert opinions before implementation.

## Output

A design document that `stripe-scaffold` can implement. Include:
- Architecture decisions with rationale
- Specific Stripe API features to use
- Data model for subscription state
- Webhook events to subscribe to
- Access control logic

## Adaptation

Design for the detected stack (usually Next.js + Convex + Clerk). If stack differs, adapt the design to that stack's patterns while maintaining the same Stripe concepts.
