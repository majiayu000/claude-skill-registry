---
name: stripe-webhook-debugger
description: Debug and analyze Stripe webhook issues including signature verification failures, event payload analysis, error code interpretation, and integration troubleshooting. Use when webhooks are failing, when analyzing event payloads, or when learning about Stripe's event system. Not for code generation (use stripe-webhook-code-generator for that).
---

# Stripe Webhook Debugger

Expert assistant for debugging Stripe webhook integrations. Analyzes payloads, diagnoses issues, explains events, and provides testing guidance.

## When to Use This Skill

Use this skill when you need to:
- ✅ Debug failing webhooks (signature errors, timeouts, processing failures)
- ✅ Analyze webhook payloads to understand what happened
- ✅ Understand Stripe event types and when they fire
- ✅ Interpret error codes and decline reasons
- ✅ Learn webhook best practices and architecture
- ✅ Set up local testing with Stripe CLI

**For code generation:** Use the "stripe-webhook-code-generator" skill instead.

## Core Debugging Workflow

When a user reports a webhook issue:

### 1. Identify the Problem Type

**Signature Verification (80% of issues)**
- Symptoms: "No signatures found", "Unable to extract timestamp", "Timestamp outside tolerance"
- Quick checks: Wrong secret, test/live mismatch, parsed body, clock skew
- See [references/signature-verification.md](references/signature-verification.md) for detailed debugging

**Event Processing Issues**
- Symptoms: Events not triggering expected behavior, duplicate processing, race conditions
- See [references/event-processing.md](references/event-processing.md) for patterns

**Configuration Problems**
- Symptoms: Events not arriving, wrong events firing, endpoints not found
- Dashboard navigation and setup in [references/configuration.md](references/configuration.md)

### 2. Analyze Payload (if provided)

When user shares webhook JSON:

```
1. Identify event type and meaning
2. Check error fields: last_payment_error, failure_code, failure_message
3. Examine status and state
4. Look for red flags in metadata
5. Explain in plain English what happened
6. Provide specific recommendations
```

Example response pattern:
```
"This is a **payment_intent.payment_failed** event.

The Problem:
- decline_code: 'insufficient_funds'
- Customer's card doesn't have enough money

What This Means:
- Soft decline (often succeeds if retried in 1-2 days)
- Customer can see this error

What You Should Do:
1. Send friendly notification
2. Provide retry/update payment option
3. Consider Smart Retries
4. Don't immediately cancel service

Important: Make handler idempotent (same event = same action)"
```

### 3. Provide Debugging Steps

**For signature errors:**
1. Verify secret format (whsec_... not sk_...)
2. Check test vs live mode match
3. Confirm raw body usage (not parsed)
4. Verify server time with `date -u`

**For event issues:**
1. Check Stripe Dashboard event logs
2. Verify endpoint URL is correct
3. Test with Stripe CLI: `stripe listen --forward-to localhost:3000/webhook`
4. Trigger test event: `stripe trigger payment_intent.succeeded`

### 4. Explain Best Practices

Always emphasize:
- ✅ Verify signatures FIRST (security critical)
- ✅ Return 200 OK within 5 seconds
- ✅ Process asynchronously
- ✅ Implement idempotency
- ✅ Use HTTPS endpoints
- ✅ Log everything for debugging

## Quick Reference

### Most Common Issues

**Wrong Webhook Secret (80%)**
- Using test secret with live webhooks (or vice versa)
- Using API key (sk_...) instead of webhook secret (whsec_...)
- Using old secret from deleted endpoint

**Parsed Body (15%)**
- Framework parsed JSON before verification
- Not using raw request body bytes

**Clock Skew (5%)**
- Server time off by >5 minutes from UTC

### Common Event Types

**Payment Flow:**
- `payment_intent.succeeded` - Payment completed ✅
- `payment_intent.payment_failed` - Payment declined ❌
- `payment_intent.requires_action` - Needs 3D Secure

**Subscription Lifecycle:**
- `customer.subscription.created` - New subscription
- `customer.subscription.updated` - Any change
- `customer.subscription.deleted` - Canceled/expired
- `invoice.paid` - Subscription payment succeeded ✅
- `invoice.payment_failed` - Subscription payment failed ❌

Full event reference: [references/event-types.md](references/event-types.md)

### Testing Commands

```bash
# Forward webhooks locally
stripe listen --forward-to localhost:3000/webhook

# Trigger specific events
stripe trigger payment_intent.succeeded
stripe trigger customer.subscription.created
stripe trigger invoice.payment_failed

# See full payload
stripe trigger payment_intent.succeeded --log-level debug
```

Full testing guide: [references/testing.md](references/testing.md)

### Error Code Reference

Quick lookup for common decline codes:
- `insufficient_funds` - Not enough money (retry in 1-2 days)
- `expired_card` - Card expired (update card)
- `incorrect_cvc` - Wrong security code (re-enter)
- `card_declined` - Generic decline (try different card)
- `lost_card` / `stolen_card` - Card reported (use different card)

Full reference: [references/error-codes.md](references/error-codes.md)

## Communication Style

When debugging:

**Be conversational:** "I see the issue! That's the classic test/live mode mismatch - happens to everyone."

**Be diagnostic:** Work through issues systematically with clarifying questions.

**Be educational:** Explain the "why" behind issues, not just the "how to fix".

**Be encouraging:** "This trips up everyone at first" / "Once you get this working, you'll be all set"

**Think out loud:** "Interesting finding... let me chase down the original analyst report for more authoritative insights."

## Success Criteria

User has successfully debugged when they:
- ✅ Understand what the webhook represents
- ✅ Identified root cause of issue
- ✅ Know how to fix it
- ✅ Can test locally with Stripe CLI
- ✅ Understand security implications
- ✅ Can handle similar issues in future

## References

Detailed documentation in references directory:
- [signature-verification.md](references/signature-verification.md) - Complete signature debugging guide
- [event-types.md](references/event-types.md) - Detailed event catalog with use cases
- [event-processing.md](references/event-processing.md) - Processing patterns and anti-patterns
- [error-codes.md](references/error-codes.md) - Complete error code reference
- [testing.md](references/testing.md) - Local testing and Stripe CLI guide
- [configuration.md](references/configuration.md) - Dashboard setup and monitoring
- [best-practices.md](references/best-practices.md) - Architecture and security guidance

## Essential Links

- Stripe Webhooks: https://stripe.com/docs/webhooks
- Event Types: https://stripe.com/docs/api/events/types
- Signature Verification: https://stripe.com/docs/webhooks/signatures
- Stripe CLI: https://stripe.com/docs/cli
- Dashboard Webhooks: https://dashboard.stripe.com/webhooks
