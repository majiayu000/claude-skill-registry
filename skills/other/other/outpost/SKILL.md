---
name: outpost
description: "Sets up and configures Hookdeck Outpost for outbound event delivery to customer endpoints. Use when sending webhooks to customers, building webhook delivery infrastructure, configuring destinations (HTTP, SQS, RabbitMQ, Pub/Sub, EventBridge, Kafka), or managing tenants and subscriptions in Outpost."
allowed-tools: WebFetch
---

# Hookdeck Outpost

Open-source outbound event delivery infrastructure by Hookdeck. Delivers your platform events directly to your users' preferred event destinations (webhooks, message queues, streaming platforms).

- [Outpost docs](https://outpost.hookdeck.com/docs/)
- [GitHub](https://github.com/hookdeck/outpost)
- [API reference](https://outpost.hookdeck.com/docs/api)

## Deployment Options

| Option | Description | Best for |
|---|---|---|
| **Self-hosted** | Run via Docker, Kubernetes, or Railway. Full control. Apache-2.0 license. | Production with custom infra requirements |
| **Managed** | Hookdeck Cloud. No infrastructure to operate. | Teams wanting zero-ops setup |

For managed, sign up at [hookdeck.com](https://hookdeck.com). For self-hosted, see the quickstart below.

## Supported Destination Types

**Available:** Webhooks (HTTP), Hookdeck Event Gateway, AWS SQS, AWS Kinesis, AWS S3, Azure Service Bus, GCP Pub/Sub, RabbitMQ (AMQP)

**Planned:** [AWS EventBridge](https://github.com/hookdeck/outpost/issues/201), [Apache Kafka](https://github.com/hookdeck/outpost/issues/141)

## [Core Concepts](https://outpost.hookdeck.com/docs/concepts)

**Tenants** -- Represent a user, team, or organization in your product. Each tenant manages their own Destinations.

**Destinations** -- A specific instance of a [destination type](https://outpost.hookdeck.com/docs/concepts#tenant-destination-types) belonging to a tenant. For example, a webhook destination with a particular URL, or an SQS queue.

**Topics** -- Categorize events using a Pub/Sub pattern (e.g., `user.created`, `payment.completed`). Destinations subscribe to one or more topics, or `*` for all.

**Events** -- Data representing an action in your system. Published to a topic and delivered to all matching destinations.

**Delivery Attempts** -- Records of each attempt to deliver an event to a destination, including request/response data.

## Self-Hosted Quick Start (Docker)

Requires [Docker](https://docs.docker.com/engine/install/). Uses RabbitMQ for message queuing.

```sh
git clone https://github.com/hookdeck/outpost.git
cd outpost/examples/docker-compose/
cp .env.example .env
# Edit .env and set your API_KEY value
docker-compose -f compose.yml -f compose-rabbitmq.yml -f compose-postgres.yml up
```

Verify the services are running:

```sh
curl localhost:3333/api/v1/healthz
```

## API Access

The Outpost API is a REST-based JSON API. The base URL and authentication differ by deployment:

| Deployment | Base URL | Authentication |
|---|---|---|
| **Self-hosted** | `http://localhost:3333/api/v1` (or your configured host) | `Authorization: Bearer $API_KEY` (the `API_KEY` env var you configured) |
| **Managed** | Provided in your Hookdeck project | `Authorization: Bearer $HOOKDECK_API_KEY` (from [Dashboard > Settings > Secrets](https://dashboard.hookdeck.com/settings/project/secrets)) |

The OpenAPI spec for the self-hosted API is at: https://github.com/hookdeck/outpost/blob/main/docs/apis/openapi.yaml

All curl examples below use the self-hosted base URL. Replace `localhost:3333/api/v1` with the managed URL and use your Hookdeck API key when using the managed version.

## Publish Your First Event

Set shell variables for convenience:

```sh
BASE_URL=localhost:3333/api/v1
API_KEY=your_api_key
TENANT_ID=your_org_name
URL=https://your-webhook-endpoint.example.com
```

Create a tenant, add a webhook destination, and publish an event:

```sh
# Create tenant
curl -X PUT "$BASE_URL/$TENANT_ID" \
  -H "Authorization: Bearer $API_KEY"

# Create webhook destination subscribing to all topics
curl -X POST "$BASE_URL/$TENANT_ID/destinations" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "type": "webhook",
    "topics": ["*"],
    "config": { "url": "'"$URL"'" }
  }'

# Publish an event
curl -X POST "$BASE_URL/publish" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "tenant_id": "'"$TENANT_ID"'",
    "topic": "user.created",
    "eligible_for_retry": true,
    "data": { "user_id": "usr_123" }
  }'
```

## Tenant Portal

Outpost includes a built-in portal UI where tenants manage their destinations and inspect events:

```sh
curl "$BASE_URL/$TENANT_ID/portal" \
  -H "Authorization: Bearer $API_KEY"
# Returns { "redirect_url": "...?token=<jwt>" }
```

## Architecture

Outpost consists of three services (deployable together as a single binary or separately for horizontal scaling): **API Service** (captures events, configuration APIs), **Delivery Service** (delivers to destinations via message queues), and **Log Service** (stores events, status, responses). Requires Redis 6.0+, PostgreSQL, and one supported message queue. See [concepts](https://outpost.hookdeck.com/docs/concepts) for details.

## Future Skills

Destination-specific skills (`outpost-webhooks`, `outpost-sqs`, `outpost-rabbitmq`, etc.) will be added as Outpost documentation matures.

## Deployment Quickstarts

- [Docker](https://outpost.hookdeck.com/docs/quickstarts/docker) | [Kubernetes](https://outpost.hookdeck.com/docs/quickstarts/kubernetes) | [Railway](https://outpost.hookdeck.com/docs/quickstarts/railway) | [Configuration reference](https://outpost.hookdeck.com/docs/references/configuration)

## Related Skills

- [hookdeck](https://github.com/hookdeck/agent-skills/blob/main/skills/hookdeck/SKILL.md) -- skill router for all Hookdeck skills
- [event-gateway](https://github.com/hookdeck/agent-skills/blob/main/skills/event-gateway/SKILL.md) -- Hookdeck Event Gateway (inbound webhooks)
