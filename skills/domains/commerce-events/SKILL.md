---
name: commerce-events
description: Inspect commerce events, manage the event audit trail, and handle idempotency keys. Use when debugging event history, reviewing the outbox, or ensuring operation idempotency.
---

# Commerce Events

Inspect the commerce event log, manage the outbox for sync, and handle idempotency keys for safe retries.

## How It Works

1. Browse and filter the event log for any commerce entity.
2. Inspect event payloads and metadata.
3. Review the outbox for events pending sync.
4. Manage idempotency keys to prevent duplicate operations.
5. Replay or acknowledge events for debugging and recovery.

## Usage

- CLI: `stateset-events list`, `stateset-events inspect <event_id>`, `stateset-events outbox`.
- MCP tools: `list_events`, `get_event`, `list_outbox`, `acknowledge_event`, `get_idempotency_key`, `create_idempotency_key`.
- Read-only operations do not require `--apply`.

## Event Fields

- `event_id`: Unique event identifier (UUID)
- `event_type`: Operation type (e.g., order.created, inventory.adjusted)
- `entity_type` / `entity_id`: Affected entity
- `payload`: Full event data (JSON)
- `agent_signature`: Ed25519 signature for authenticity
- `created_at`: Event timestamp
- `sequence_number`: Deterministic ordering

## Outbox States

- Pending: awaiting sync to sequencer
- Synced: successfully pushed to sequencer
- Failed: sync attempt failed (will retry)
- Acknowledged: confirmed by sequencer

## Idempotency Keys

Prevent duplicate operations:
- Key is a unique string per operation (e.g., `create_order_ORD-123`)
- If the key already exists, the original result is returned
- Keys expire after a configurable TTL
- Critical for retry safety in distributed systems

## Output

```json
{"events":[{"event_id":"evt_001","event_type":"order.created","entity_type":"order","entity_id":"ord_123","created_at":"2025-01-15T10:30:00Z"}],"total":1}
```

## Present Results to User

- Event timeline for the requested entity.
- Event type, timestamp, and sequence number.
- Outbox status and pending event count.
- Idempotency key status and expiration.

## Troubleshooting

- Event not synced: check outbox for failed events; verify sequencer connectivity.
- Duplicate operation: look up existing idempotency key for the operation.
- Missing events: verify event type filter and time range.
- Signature invalid: check Ed25519 key configuration.

## References
- references/event-types.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/events.rs
- /home/dom/stateset-icommerce/crates/stateset-db/src/migrations/026_idempotency_keys.sql
