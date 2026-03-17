---
name: hookdeck
description: "Routes to the correct Hookdeck product skill. Covers Event Gateway (inbound: receive webhooks, webhook endpoints, local dev, event queue) and Outpost (outbound: send webhooks to customers). Use when working with any Hookdeck product and unsure which skill to use."
---

# Hookdeck

| What you want to do | Skill |
|---------------------|-------|
| **Receive and process webhooks** | event-gateway |
| **Route events between third-party services** | event-gateway |
| **Build asynchronous APIs (IoT, SDKs, web analytics)** | event-gateway |
| **Test and debug webhooks on localhost** | event-gateway |
| **Send webhooks/events to customers** | outpost |

## Event Gateway

Inbound event infrastructure. One skill covers all use cases:
staged integration workflow, connections, rules, authentication,
local dev, monitoring, and API.

- Skill: [event-gateway](https://github.com/hookdeck/agent-skills/blob/main/skills/event-gateway/SKILL.md)
- Install: `npx skills add hookdeck/agent-skills --skill event-gateway`
- Docs: https://hookdeck.com/docs/

## Outpost

Outbound event delivery to HTTP, SQS, RabbitMQ, Pub/Sub, and more.

- Skill: [outpost](https://github.com/hookdeck/agent-skills/blob/main/skills/outpost/SKILL.md)
- Install: `npx skills add hookdeck/agent-skills --skill outpost`
- Docs: https://outpost.hookdeck.com/docs/

## Provider Webhook Skills

For provider-specific webhook knowledge (Stripe, Shopify, GitHub, etc.),
see [hookdeck/webhook-skills](https://github.com/hookdeck/webhook-skills).
The event-gateway skill references these during the scaffold stage.
