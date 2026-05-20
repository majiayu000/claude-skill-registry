---
name: 33god-service-development
description: "Guide for creating, registering, and deploying new microservices in the 33GOD event-driven ecosystem. Use when (1) Creating new event consumer services, (2) Registering services in the Bloodbank registry, (3) Implementing FastStream-based event handlers, (4) Setting up service infrastructure (Docker, dependencies, testing), (5) Understanding 33GOD architecture and event patterns, (6) Migrating services to FastStream from legacy patterns."
---

# 33GOD Service Developer

Expert guide for onboarding new microservices into the **33GOD event-driven ecosystem**.

## Core Principles

Services in 33GOD are:

- **Event-Driven**: React to Bloodbank events rather than being called directly
- **Passive Consumers**: Sleep until relevant events arrive on their `agent.{name}.inbox`
- **Heartbeat-Aware**: Consume `system.heartbeat.tick` for periodic tasks and orchestration
- **Single Responsibility**: Do one thing well (e.g., "Process Transcripts", "Calculate Costs")
- **Stateless**: Store state in Candystore (events), Vault (filesystem), or database—not in memory
- **Schema-First**: Event contracts defined in Holyfields before code is written

## Architecture Context

33GOD uses Bloodbank (RabbitMQ topic exchange) as its event bus. All services participate in the event flow:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SERVICE IN EVENT FLOW                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   HOLYFIELDS → BLOODBANK → CANDYSTORE → HOLOCENE → YOUR SERVICE             │
│   (Schema)      (Event)      (History)      (View)      (Action)            │
│                                │                                             │
│                                │         ┌─────────────────────────────┐     │
│                                │         │  Your Service Consumer      │     │
│                                │         │  (FastStream)               │     │
│                                │         │                             │     │
│                                │         │  Queue: agent.yourservice.  │     │
│                                │         │         inbox               │     │
│                                │         │  Routing: agent.yourservice.│     │
│                                │         │           #                 │     │
│                                │         │                             │     │
│                                │         │  Handles:                   │     │
│                                │         │  • system.heartbeat.tick    │     │
│                                │         │  • domain.resource.action   │     │
│                                │         │                             │     │
│                                │         │  Emits:                     │     │
│                                │         │  • agent.yourservice.result │     │
│                                │         └─────────────────────────────┘     │
│                                │                       │                      │
│                                └───────────────────────┤                      │
│                                                        ▼                      │
│                                              Back to Bloodbank                │
│                                              (new events)                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Registry**: `/home/delorenj/code/33GOD/services/registry.yaml` is the single source of truth for:
- Service definitions and metadata
- Event routing mappings
- Service topology layers

## Service Development Workflow

### Phase 1: Planning & Registration

1. **Define the service purpose**
   - What single responsibility does it serve?
   - What events trigger it?
   - What events does it produce?

2. **Register in registry.yaml**
   - Add service entry under `services`
   - Define queue name and routing keys
   - Add to `event_subscriptions` mapping
   - Place in appropriate topology layer

See [references/registry_guide.md](references/registry_guide.md) for registry schema and examples.

### Phase 2: Implementation

1. **Scaffold from template**
   ```bash
   cd /home/delorenj/code/33GOD/services
   cp -r templates/generic-consumer/{{cookiecutter.service_slug}} ./my-new-service
   ```

2. **Implement FastStream consumer**
   - Use FastStream with RabbitBroker (ADR-0002 pattern)
   - Unwrap EventEnvelope in handler
   - Use Pydantic models for payload validation

See [references/faststream_patterns.md](references/faststream_patterns.md) for implementation patterns.

### Phase 3: Configuration & Dependencies

1. **Update pyproject.toml**
   - Add bloodbank as local dependency
   - Include any service-specific dependencies

2. **Configure environment**
   - Define settings in `src/config.py`
   - Use Pydantic BaseSettings

3. **Docker setup**
   - Update Dockerfile if needed
   - Ensure bloodbank volume mount for local dev

### Phase 4: Testing & Deployment

1. **Write tests**
   - Create `tests/test_consumer.py`
   - Mock EventEnvelope and payload
   - Test handler logic in isolation

2. **Local testing**
   ```bash
   cd services/my-new-service
   uv run pytest
   ```

3. **Run service**
   ```bash
   uv run faststream run src.consumer:app
   ```

## Reference Files

Detailed guides for specific aspects:

- **[registry_guide.md](references/registry_guide.md)**: Registry schema, examples, topology layers
- **[faststream_patterns.md](references/faststream_patterns.md)**: FastStream implementation patterns, EventEnvelope handling
- **[testing_guide.md](references/testing_guide.md)**: Testing strategies, mocking patterns
- **[deployment_guide.md](references/deployment_guide.md)**: Docker, environment configuration, running services

## Quick Reference

**Common routing key patterns**:
- `domain.event.action` (e.g., `fireflies.transcript.ready`)
- `#` wildcard for all events (infrastructure services only)
- Hierarchical namespacing (e.g., `theboard.meeting.*`)

**Service types**:
- `event-consumer`: Subscribes to events, performs work
- `event-producer`: Produces events (often FastAPI services)
- `hybrid`: Both consumer and producer

**Status values**:
- `active`: Running in production
- `planned`: Defined but not implemented
- `deprecated`: Being phased out
