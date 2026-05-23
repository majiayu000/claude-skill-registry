---
name: magento-events-cron
description: Implement Magento 2 events, observers, cron jobs, and message queues. Use when building event-driven logic, scheduled tasks, or asynchronous processing.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Magento 2 Events, Observers, Cron & Message Queues

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.adobe.com/commerce/php/development/components/events-and-observers/` for events/observers guide
2. Web-search `site:developer.adobe.com commerce php development components message-queues` for message queue guide
3. Web-search `site:developer.adobe.com commerce php development components cron` for cron development

## Events and Observers

### How Events Work

Publish-subscribe pattern: code dispatches named events, and observers respond.

### Dispatching Events

```php
$this->eventManager->dispatch('event_name', ['key' => $value]);
```

`EventManagerInterface` is injected via constructor.

### Observer Configuration (events.xml)

Observers are bound to events in `etc/events.xml` (global), `etc/frontend/events.xml`, or `etc/adminhtml/events.xml`:
- `event name` — event to observe
- `observer name` — unique identifier
- `instance` — observer class (fully qualified)

### Observer Classes

- Located in `Observer/` directory
- Implement `Magento\Framework\Event\ObserverInterface`
- Single method: `execute(Observer $observer)` — access event data via `$observer->getEvent()`

### Area Scoping

- `etc/events.xml` — runs in ALL areas
- `etc/frontend/events.xml` — storefront only
- `etc/adminhtml/events.xml` — admin only
- Use the most specific scope to avoid unintended side effects

### Common Events

Magento dispatches hundreds of events. Common categories:
- `catalog_product_save_before/after` — product save lifecycle
- `checkout_submit_all_after` — order placement
- `customer_register_success` — customer registration
- `sales_order_place_after` — order placed
- `controller_action_predispatch/postdispatch` — request lifecycle

## Cron Jobs

### Configuration (crontab.xml)

Cron jobs are declared in `etc/crontab.xml`:
- `job name` — unique identifier
- `instance` — class name
- `method` — method to call (usually `execute`)
- `schedule` — cron expression (minute hour day month weekday)
- `group` — cron group (default, index; Adobe Commerce also has staging, catalog_event)

### Cron Class

Any class with an `execute()` method. No interface required. Constructor injection for dependencies.

### Cron Groups

- **default** — general tasks
- **index** — indexer-related tasks
- **staging** — staging-related tasks (Adobe Commerce only)
- **catalog_event** — catalog event tasks (Adobe Commerce only)
- Custom groups configurable in `etc/cron_groups.xml`

### Running Cron

```bash
bin/magento cron:run           # Run all due cron jobs
bin/magento cron:install       # Install system crontab entry
```

## Message Queues

### When to Use

For asynchronous, resource-intensive, or decoupled operations. Supports AMQP (RabbitMQ) and MySQL-based queues.

### Configuration Files

- `communication.xml` — defines topics and request/response types
- `queue_consumer.xml` — maps queues to consumer handler classes
- `queue_topology.xml` — exchanges, queues, routing
- `queue_publisher.xml` — defines where topics publish to

### Consumer Pattern

Consumer class with a `process($message)` method. Started via:
```bash
bin/magento queue:consumers:start <consumer_name>
```

## Best Practices

- Keep observers lightweight — offload heavy work to cron or queues
- Use area-specific events.xml to minimize scope
- Prefer message queues over synchronous observers for slow operations
- Use `index` cron group for indexer-related jobs
- Log cron execution for debugging
- Handle exceptions in observers gracefully — a failing observer blocks the event chain

Fetch the events/observers and cron documentation for exact XML schemas, event names, and cron expression syntax before implementing.
