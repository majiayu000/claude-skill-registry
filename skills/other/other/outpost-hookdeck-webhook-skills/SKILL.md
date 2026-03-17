---
name: outpost
description: >
  Hookdeck Outpost — open-source infrastructure for sending webhooks and
  events to user-preferred destinations (HTTP, SQS, RabbitMQ, Pub/Sub,
  EventBridge, Kafka). Use when building a SaaS platform that needs to
  deliver events to customers.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Hookdeck Outpost

Outpost is open-source infrastructure for delivering events to user-preferred destinations: Webhooks (HTTP), SQS, RabbitMQ, Pub/Sub, EventBridge, Kafka, and more. Apache 2.0 licensed, available as managed by Hookdeck or self-hosted.

## When to Use Outpost

- You're building a SaaS or API platform and need to send webhooks to your users
- You need multi-destination support beyond HTTP webhooks (SQS, RabbitMQ, Pub/Sub, EventBridge, Kafka)
- You want self-hostable webhook delivery infrastructure
- You need multi-tenant support with per-user observability
- You want to offer your customers reliable, retryable event delivery

## Quick Start

### Managed (Hookdeck)

The fastest way to get started — Hookdeck hosts and operates Outpost for you:

1. Sign up at [hookdeck.com](https://hookdeck.com)
2. See the [Send Webhooks quickstart](https://hookdeck.com/docs/use-cases/send-webhooks/quickstart)

### Self-Hosted

Run Outpost on your own infrastructure:

1. See the [Outpost documentation](https://outpost.hookdeck.com/docs)
2. Clone from [GitHub](https://github.com/hookdeck/outpost)

## Supported Destinations

| Destination | Protocol |
|-------------|----------|
| Webhooks | HTTP/HTTPS |
| Amazon SQS | AWS SQS |
| RabbitMQ | AMQP |
| Google Pub/Sub | gRPC |
| Amazon EventBridge | AWS EventBridge |
| Apache Kafka | Kafka protocol |

## Full Product Skills

For detailed Outpost skills:

> Coming soon: `npx skills add hookdeck/skills`
>
> In the meantime, see the [Outpost documentation](https://outpost.hookdeck.com/docs)
> and the [GitHub repo](https://github.com/hookdeck/outpost).

## Resources

- [Outpost Documentation](https://outpost.hookdeck.com/docs)
- [GitHub Repository](https://github.com/hookdeck/outpost)
- [Hookdeck Send Webhooks Guide](https://hookdeck.com/docs/use-cases/send-webhooks)

## Related Skills

- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - For receiving and ingesting webhooks (the inbound counterpart)
- [hookdeck-event-gateway-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway-webhooks) - Verify Hookdeck signatures on forwarded webhooks
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Handler sequence, idempotency, error handling, retry logic
