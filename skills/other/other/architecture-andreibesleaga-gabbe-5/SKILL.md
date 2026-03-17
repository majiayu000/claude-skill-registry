---
name: event-governance
description: Schema Registry enforcement (Avro/JSON), CloudEvents standard, and Event Evolution rules.
role: prod-architect, eng-data
triggers:
  - event schema
  - avro
  - protobuf
  - cloudevents
  - schema registry
  - asyncapi
---

# event-governance Skill

Events are Data Contracts. They must be governed as strictly as APIs.

## 1. CloudEvents Standard
Use the standard envelope structure:
```json
{
  "specversion": "1.0",
  "type": "com.example.order.created",
  "source": "/service/order",
  "id": "A234-1234-1234",
  "time": "20.2.01-01T12:00:00Z",
  "datacontenttype": "application/json",
  "data": { ... }
}
```

## 2. Schema Registry
- **Rule**: All event payloads must be validated against a Schema Registry (e.g., Confluent, Glue) *before* publishing.
- **Formats**: Avro (preferred for compact/evolution), Protobuf, or JSON Schema.

## 3. Schema Evolution (Compatibility)
- **Backward Compatibility**: New consumer can read old data. (Add optional fields).
- **Forward Compatibility**: Old consumer can read new data. (Ignore unknown fields).
- **Full Compatibility**: Both.
- **Breaking Changes**: renaming fields, changing types. **Forbidden** without a new topic version (`orders.v2`).

## 4. Documentation
- Use **AsyncAPI** to document event topography.
- Treat Events as Public APIs.
