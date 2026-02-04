---
name: webhook-handler-patterns
description: >
  Best practices for webhook handlers. Use when implementing the handler
  sequence (verify first, parse second, handle idempotently), idempotency,
  error handling, retry logic, or framework-specific issues with Express,
  Next.js, or FastAPI.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Webhook Handler Patterns

## When to Use This Skill

- Following the correct webhook handler order (verify → parse → handle idempotently)
- Implementing idempotent webhook handlers
- Handling errors and configuring retry behavior
- Understanding framework-specific gotchas (raw body, middleware order)
- Building production-ready webhook infrastructure

## Resources

### Handler Sequence

- [references/handler-sequence.md](references/handler-sequence.md) - Verify first, parse second, handle idempotently third

### Best Practices

- [references/idempotency.md](references/idempotency.md) - Prevent duplicate processing
- [references/error-handling.md](references/error-handling.md) - Return codes, logging, dead letter queues
- [references/retry-logic.md](references/retry-logic.md) - Provider retry schedules, backoff patterns

### Framework Guides

- [references/frameworks/express.md](references/frameworks/express.md) - Express.js patterns and gotchas
- [references/frameworks/nextjs.md](references/frameworks/nextjs.md) - Next.js App Router patterns
- [references/frameworks/fastapi.md](references/frameworks/fastapi.md) - FastAPI/Python patterns

## Quick Reference

### Handler Sequence

1. **Verify signature first** — Use raw body; reject invalid requests with 4xx.
2. **Parse payload second** — After verification, parse or construct the event.
3. **Handle idempotently third** — Check event ID, then process; return 2xx for duplicates.

See [references/handler-sequence.md](references/handler-sequence.md) for details and links to provider verification and idempotency patterns.

### Response Codes

| Code | Meaning | Provider Behavior |
|------|---------|-------------------|
| `2xx` | Success | No retry |
| `4xx` | Client error | Usually no retry (except 429) |
| `5xx` | Server error | Retry with backoff |
| `429` | Rate limited | Retry after delay |

### Idempotency Checklist

1. Extract unique event ID from payload
2. Check if event was already processed
3. Process event within transaction
4. Store event ID after successful processing
5. Return success for duplicate events

## Related Skills

- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe payment webhook handling
- [shopify-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/shopify-webhooks) - Shopify e-commerce webhook handling
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub repository webhook handling
- [resend-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/resend-webhooks) - Resend email webhook handling
- [chargebee-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/chargebee-webhooks) - Chargebee billing webhook handling
- [clerk-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/clerk-webhooks) - Clerk auth webhook handling
- [elevenlabs-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/elevenlabs-webhooks) - ElevenLabs webhook handling
- [openai-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/openai-webhooks) - OpenAI webhook handling
- [paddle-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/paddle-webhooks) - Paddle billing webhook handling
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Production webhook infrastructure (routing, replay, monitoring)
