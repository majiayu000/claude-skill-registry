---
description: Schema Registry expert for Avro, Protobuf, and JSON Schema management. Covers schema evolution strategies, compatibility modes, validation, and best practices for managing schemas in Confluent Cloud and self-hosted Schema Registry. Activates for schema registry, avro, protobuf, json schema, schema evolution, compatibility modes, schema validation.
---

# Confluent Schema Registry Skill

Expert knowledge of Confluent Schema Registry for managing Avro, Protobuf, and JSON Schema schemas in Kafka ecosystems.

## What I Know

### Schema Formats

**Avro** (Most Popular):
- Binary serialization format
- Schema evolution support
- Smaller message size vs JSON
- Self-describing with schema ID in header
- Best for: High-throughput applications, data warehousing

**Protobuf** (Google Protocol Buffers):
- Binary serialization
- Strong typing with .proto files
- Language-agnostic (Java, Python, Go, C++, etc.)
- Efficient encoding
- Best for: Polyglot environments, gRPC integration

**JSON Schema**:
- Human-readable text format
- Easy debugging
- Widely supported
- Larger message size
- Best for: Development, debugging, REST APIs

### Compatibility Modes

| Mode | Producer Can | Consumer Can | Use Case |
|------|-------------|-------------|----------|
| **BACKWARD** | Remove fields, add optional fields | Read old data with new schema | Most common, safe for consumers |
| **FORWARD** | Add fields, remove optional fields | Read new data with old schema | Safe for producers |
| **FULL** | Add/remove optional fields only | Bi-directional compatibility | Both producers and consumers upgrade independently |
| **NONE** | Any change | Must coordinate upgrades | Development only, NOT production |
| **BACKWARD_TRANSITIVE** | BACKWARD across all versions | Read any old data | Strictest backward compatibility |
| **FORWARD_TRANSITIVE** | FORWARD across all versions | Read any new data | Strictest forward compatibility |
| **FULL_TRANSITIVE** | FULL across all versions | Complete bi-directional | Strictest overall |

**Default**: `BACKWARD` (recommended for production)

### Schema Evolution Strategies

**Adding Fields**:
```avro
// V1
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"}
  ]
}

// V2 - BACKWARD compatible (added optional field with default)
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

**Removing Fields** (BACKWARD compatible):
```avro
// V1
{"name": "address", "type": "string"}

// V2 - Remove field (old consumers will ignore it)
// Field removed from schema
```

**Changing Field Types** (Breaking Change!):
```avro
// ❌ BREAKING - Cannot change string to int
{"name": "age", "type": "string"} → {"name": "age", "type": "int"}

// ✅ SAFE - Use union types
{"name": "age", "type": ["string", "int"], "default": "unknown"}
```

## When to Use This Skill

Activate me when you need help with:
- Schema evolution strategies ("How do I evolve my Avro schema?")
- Compatibility mode selection ("Which compatibility mode for production?")
- Schema validation ("Validate my Avro schema")
- Best practices ("Schema Registry best practices")
- Schema registration ("Register Avro schema with Schema Registry")
- Debugging schema issues ("Schema compatibility error")
- Format comparison ("Avro vs Protobuf vs JSON Schema")

## Best Practices

### 1. Always Use Compatible Evolution

✅ **DO**:
- Add optional fields with defaults
- Remove optional fields
- Use union types for flexibility
- Test schema changes in staging first

❌ **DON'T**:
- Change field types
- Remove required fields
- Rename fields (add new + deprecate old)
- Use `NONE` compatibility in production

### 2. Schema Naming Conventions

**Hierarchical Namespaces**:
```
com.company.domain.EntityName
com.acme.ecommerce.Order
com.acme.ecommerce.OrderLineItem
```

**Subject Naming** (Kafka topics):
- `<topic-name>-value` - For record values
- `<topic-name>-key` - For record keys
- Example: `orders-value`, `orders-key`

### 3. Schema Registry Configuration

**Producer** (with Avro):
```javascript
const { Kafka } = require('kafkajs');
const { SchemaRegistry } = require('@kafkajs/confluent-schema-registry');

const registry = new SchemaRegistry({
  host: 'https://schema-registry:8081',
  auth: {
    username: 'SR_API_KEY',
    password: 'SR_API_SECRET'
  }
});

// Register schema
const schema = `
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "id", "type": "long"},
    {"name": "name", "type": "string"}
  ]
}
`;

const { id } = await registry.register({
  type: SchemaType.AVRO,
  schema
});

// Encode message with schema
const payload = await registry.encode(id, {
  id: 1,
  name: 'John Doe'
});

await producer.send({
  topic: 'users',
  messages: [{ value: payload }]
});
```

**Consumer** (with Avro):
```javascript
const consumer = kafka.consumer({ groupId: 'user-processor' });

await consumer.subscribe({ topic: 'users' });

await consumer.run({
  eachMessage: async ({ message }) => {
    // Decode message (schema ID is in header)
    const decodedMessage = await registry.decode(message.value);
    console.log(decodedMessage); // { id: 1, name: 'John Doe' }
  }
});
```

### 4. Schema Validation Workflow

**Before Registering**:
1. Validate schema syntax (Avro JSON, .proto, JSON Schema)
2. Check compatibility with existing versions
3. Test with sample data
4. Register in dev/staging first
5. Deploy to production after validation

**CLI Validation**:
```bash
# Check compatibility (before registering)
curl -X POST http://localhost:8081/compatibility/subjects/users-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...}"}'

# Register schema
curl -X POST http://localhost:8081/subjects/users-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "{...}"}'
```

## Common Issues & Solutions

### Issue 1: Schema Compatibility Error

**Error**:
```
Schema being registered is incompatible with an earlier schema
```

**Root Cause**: Violates compatibility mode (e.g., removed required field with BACKWARD mode)

**Solution**:
1. Check current compatibility mode:
   ```bash
   curl http://localhost:8081/config/users-value
   ```
2. Fix schema to be compatible OR change mode (carefully!)
3. Validate before registering:
   ```bash
   curl -X POST http://localhost:8081/compatibility/subjects/users-value/versions/latest \
     -d '{"schema": "{...}"}'
   ```

### Issue 2: Schema Not Found

**Error**:
```
Subject 'users-value' not found
```

**Root Cause**: Schema not registered yet OR wrong subject name

**Solution**:
1. List all subjects:
   ```bash
   curl http://localhost:8081/subjects
   ```
2. Register schema if missing
3. Check subject naming convention (`<topic>-key` or `<topic>-value`)

### Issue 3: Message Deserialization Failed

**Error**:
```
Unknown magic byte!
```

**Root Cause**: Message not encoded with Schema Registry (missing magic byte + schema ID)

**Solution**:
1. Ensure producer uses Schema Registry encoder
2. Check message format: [magic_byte(1) + schema_id(4) + payload]
3. Use `@kafkajs/confluent-schema-registry` library

## Schema Evolution Decision Tree

```
Need to change schema?
├─ Adding new field?
│  ├─ Required field? → Add with default value (BACKWARD)
│  └─ Optional field? → Add with default null (BACKWARD)
│
├─ Removing field?
│  ├─ Required field? → ❌ BREAKING CHANGE (coordinate upgrade)
│  └─ Optional field? → ✅ BACKWARD compatible
│
├─ Changing field type?
│  ├─ Compatible types (e.g., int → long)? → Use union types
│  └─ Incompatible types? → ❌ BREAKING CHANGE (add new field, deprecate old)
│
└─ Renaming field?
   └─ ❌ BREAKING CHANGE → Add new field + mark old as deprecated
```

## Avro vs Protobuf vs JSON Schema Comparison

| Feature | Avro | Protobuf | JSON Schema |
|---------|------|----------|-------------|
| **Encoding** | Binary | Binary | Text (JSON) |
| **Message Size** | Small (90% smaller) | Small (80% smaller) | Large (baseline) |
| **Human Readable** | No | No | Yes |
| **Schema Evolution** | Excellent | Good | Fair |
| **Language Support** | Java, Python, C++ | 20+ languages | Universal |
| **Performance** | Very Fast | Very Fast | Slower |
| **Debugging** | Harder | Harder | Easy |
| **Best For** | Data warehousing, ETL | Polyglot, gRPC | REST APIs, dev |

**Recommendation**:
- **Production**: Avro (best balance)
- **Polyglot teams**: Protobuf
- **Development/Debugging**: JSON Schema

## References

- Schema Registry REST API: https://docs.confluent.io/platform/current/schema-registry/develop/api.html
- Avro Specification: https://avro.apache.org/docs/current/spec.html
- Protobuf Guide: https://developers.google.com/protocol-buffers
- JSON Schema Spec: https://json-schema.org/

---

**Invoke me when you need schema management, evolution strategies, or compatibility guidance!**
