---
name: create-event-handlers
description: Sets up RabbitMQ event publishers and consumers following ModuleImplementationGuide.md Section 9. RabbitMQ only (no Azure Service Bus). Creates publishers with DomainEvent (tenantId preferred), consumers with handlers, naming {domain}.{entity}.{action}, required fields (id, type, version, timestamp, tenantId, source, data). Use when adding event-driven communication, async workflows, or integrating via events.
---

# Create Event Handlers

Sets up RabbitMQ event publishers and consumers following ModuleImplementationGuide.md Section 9.

## Event Naming Convention

Reference: ModuleImplementationGuide.md Section 9.1

Format: `{domain}.{entity}.{action}`

✅ **Correct:**
- `user.created`
- `auth.login.success`
- `notification.email.sent`
- `secret.rotated`

❌ **Wrong:**
- `userCreated`
- `loginSuccess`
- `emailSent`

**Standard Actions:**
- `created`, `updated`, `deleted`
- `started`, `completed`, `failed`
- `sent`, `received`, `expired`, `rotated`

## Event Structure

Reference: ModuleImplementationGuide.md Section 9.2

```typescript
interface DomainEvent<T = unknown> {
  // Identity
  id: string;                    // Unique event ID (UUID)
  type: string;                  // Event type (domain.entity.action)
  
  // Metadata
  timestamp: string;             // ISO 8601
  version: string;               // Event schema version
  source: string;                // Module that emitted
  correlationId?: string;        // Request correlation
  
  // Context
  tenantId?: string;             // Tenant context (PREFERRED; use for new modules)
  organizationId?: string;       // DEPRECATED for new modules; prefer tenantId
  userId?: string;               // Actor
  
  // Payload
  data: T;                       // Event-specific data
}
```

## Event Publisher

Reference: containers/auth/src/events/publishers/AuthEventPublisher.ts

### src/events/publishers/[Module]EventPublisher.ts

```typescript
import { randomUUID } from 'crypto';
import { EventPublisher, getChannel, closeConnection } from '@coder/shared';
import { log } from '../../utils/logger';
import { getConfig } from '../../config';

let publisher: EventPublisher | null = null;

export async function initializeEventPublisher(): Promise<void> {
  if (publisher) return;
  
  const config = getConfig();
  if (!config.rabbitmq?.url) {
    log.warn('RabbitMQ URL not configured, events will not be published');
    return;
  }
  
  try {
    await getChannel();
    publisher = new EventPublisher(config.rabbitmq.exchange || 'coder_events');
    log.info('Event publisher initialized', { exchange: config.rabbitmq.exchange });
  } catch (error: any) {
    log.error('Failed to initialize event publisher', error);
  }
}

export async function closeEventPublisher(): Promise<void> {
  try {
    await closeConnection();
    publisher = null;
  } catch (error: any) {
    log.error('Error closing event publisher', error);
  }
}

function getPublisher(): EventPublisher | null {
  if (!publisher) {
    const config = getConfig();
    publisher = new EventPublisher(config.rabbitmq.exchange || 'coder_events');
  }
  return publisher;
}

export function createBaseEvent(
  type: string,
  userId?: string,
  tenantId?: string,
  correlationId?: string,
  data?: any
) {
  return {
    id: randomUUID(),
    type,
    timestamp: new Date().toISOString(),
    version: '1.0',
    source: '[module-name]',
    correlationId,
    tenantId,
    userId,
    data: data || {},
  };
}

export async function publishEvent(event: any, routingKey?: string): Promise<void> {
  const pub = getPublisher();
  if (!pub) {
    log.warn('Event publisher not initialized, skipping event', { type: event.type });
    return;
  }
  
  try {
    await pub.publish(routingKey || event.type, event);
    log.debug('Event published', { type: event.type, id: event.id });
  } catch (error: any) {
    log.error('Failed to publish event', error, { type: event.type });
  }
}
```

### Usage in Services

```typescript
import { publishEvent, createBaseEvent } from '../events/publishers/ModuleEventPublisher';

// Publish event (tenantId for tenant context)
const event = createBaseEvent(
  'resource.created',
  userId,
  tenantId,
  correlationId,
  {
    resourceId: resource.id,
    name: resource.name,
  }
);

await publishEvent(event);
```

## Event Consumer

Reference: ModuleImplementationGuide.md Section 9.4

### src/events/consumers/[Resource]Consumer.ts

```typescript
import { EventConsumer } from '@coder/shared';
import { log } from '../../utils/logger';
import { getConfig } from '../../config';

let consumer: EventConsumer | null = null;

export async function initializeEventConsumer(): Promise<void> {
  if (consumer) return;
  
  const config = getConfig();
  if (!config.rabbitmq?.url) {
    log.warn('RabbitMQ URL not configured, events will not be consumed');
    return;
  }
  
  try {
    consumer = new EventConsumer({
      queue: config.rabbitmq.queue || '[module-name]_service',
      exchange: config.rabbitmq.exchange || 'coder_events',
      bindings: config.rabbitmq.bindings || [],
    });
    
    // Register handlers
    consumer.on('other.resource.created', handleResourceCreated);
    consumer.on('other.resource.updated', handleResourceUpdated);
    
    await consumer.start();
    log.info('Event consumer initialized', { queue: config.rabbitmq.queue });
  } catch (error: any) {
    log.error('Failed to initialize event consumer', error);
  }
}

async function handleResourceCreated(event: any): Promise<void> {
  log.info('Resource created event received', { resourceId: event.data.resourceId });
  // Handle the event
}

async function handleResourceUpdated(event: any): Promise<void> {
  log.info('Resource updated event received', { resourceId: event.data.resourceId });
  // Handle the event
}

export async function closeEventConsumer(): Promise<void> {
  try {
    if (consumer) {
      await consumer.stop();
      consumer = null;
    }
  } catch (error: any) {
    log.error('Error closing event consumer', error);
  }
}
```

## Event Documentation

Reference: ModuleImplementationGuide.md Section 9.5

### logs-events.md (if events are logged)

Create in module root if module publishes events that get logged:

```markdown
# [Module Name] - Logs Events

## Published Events

### {domain}.{entity}.{action}

**Description**: When this event is triggered.

**Triggered When**: 
- Condition 1
- Condition 2

**Event Type**: `{domain}.{entity}.{action}`

**Event Schema**:

\`\`\`json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "type", "timestamp", "version", "source", "data"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "type": { "type": "string" },
    "timestamp": { "type": "string", "format": "date-time" },
    "version": { "type": "string" },
    "source": { "type": "string" },
    "tenantId": { "type": "string", "format": "uuid" },
    "userId": { "type": "string", "format": "uuid" },
    "data": {
      "type": "object",
      "properties": {
        "resourceId": { "type": "string" }
      }
    }
  }
}
\`\`\`
```

### notifications-events.md (if events trigger notifications)

Create in module root if module publishes events that trigger notifications.

## Configuration

Add to config/default.yaml:

```yaml
rabbitmq:
  url: ${RABBITMQ_URL}
  exchange: coder_events
  queue: [module-name]_service
  bindings:
    - "other.resource.created"
    - "other.resource.updated"
```

## Checklist

- [ ] Event publisher created following pattern
- [ ] Event consumer created (if consuming events)
- [ ] Events follow naming convention: {domain}.{entity}.{action}
- [ ] Events include all required fields (id, type, version, timestamp, source, data)
- [ ] Events include tenantId when applicable (RabbitMQ only; no Azure Service Bus)
- [ ] logs-events.md created (if events are logged)
- [ ] notifications-events.md created (if events trigger notifications)
- [ ] RabbitMQ config added to default.yaml
