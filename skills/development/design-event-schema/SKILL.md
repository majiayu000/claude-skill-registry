---
name: design-event-schema
description: "Step-by-step guide for designing domain event schemas with JSON Schema, versioning, and implementation following  patterns."
tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
context:
  - type: file
    path: "architecture/**/*.md"
  - type: file
    path: "patterns/**/*.md"
---

# Skill: Design Event Schema

This skill teaches you how to design robust domain event schemas following  architectural patterns. You'll learn to create well-documented events that support evolution, enable idempotent consumers, and maintain backward compatibility across service boundaries.

Domain events are the backbone of event-driven architectures. They represent facts that happened in your domain, enabling loose coupling between bounded contexts. A well-designed event schema ensures consumers can process events reliably and schemas evolve without breaking existing consumers.

## Prerequisites

- Understanding of DDD concepts (aggregates, bounded contexts, domain events)
- Familiarity with JSON Schema basics
- Understanding of semantic versioning (semver)

## Overview

In this skill, you will:
1. Identify domain events from aggregate operations
2. Design the event envelope structure
3. Create JSON Schema definitions
4. Implement types for events
5. Apply semantic versioning
6. Design for backward-compatible evolution
7. Test event serialization

## Step 1: Identify Domain Events

Domain events represent something that happened in your domain. They are facts, not commands. Events use past-tense verbs: `FacilityCreated` (not `CreateFacility`), `AssetRegistered` (not `RegisterAsset`).

For each aggregate operation, ask: Does this state change matter to other bounded contexts? Would consumers need to react? If yes, you need a domain event.

```pseudocode
// Domain events identified for Facility aggregate
// FacilityCreated - Published when a new facility is registered
// Consumers: Asset Context, Billing Context, Grid Context

// FacilityUpdated - Published when facility configuration changes
// FacilityDecommissioned - Published when facility is taken offline
```

Document which bounded contexts consume each event to understand the impact of changes.

## Step 2: Design Event Envelope Structure

All domain events share a common envelope with metadata for routing, tracing, and versioning.

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | UUID | Unique identifier for deduplication |
| `event_type` | string | Dot-notation: `<context>.<action>` |
| `schema_version` | semver | Schema version for compatibility |
| `occurred_at` | ISO 8601 | When the event occurred |
| `aggregate_id` | string | ID of the producing aggregate |
| `correlation_id` | string | Traces request across services |
| `causation_id` | string | ID of causing event (for chains) |
| `payload` | object | Event-specific data |

```pseudocode
// events/envelope

// EventEnvelope wraps all domain events with common metadata.
TYPE EventEnvelope
    eventID: String
    eventType: String
    schemaVersion: String
    occurredAt: Timestamp
    aggregateID: String
    correlationID: String
    causationID: String           // Optional
    payload: Bytes                // Raw JSON payload

// NewEventEnvelope creates an envelope with generated ID and timestamp.
CONSTRUCTOR NewEventEnvelope(
    eventType: String,
    schemaVersion: String,
    aggregateID: String,
    correlationID: String,
    payload: Any
) RETURNS Result<EventEnvelope, Error>
    payloadBytes = Serialize(payload)
    IF payloadBytes.IsError() THEN
        RETURN Error("failed to marshal payload: " + payloadBytes.Error())
    END IF

    RETURN Ok(EventEnvelope{
        eventID: GenerateUUID(),
        eventType: eventType,
        schemaVersion: schemaVersion,
        occurredAt: Now(),
        aggregateID: aggregateID,
        correlationID: correlationID,
        payload: payloadBytes.Value()
    })
END CONSTRUCTOR

// WithCausation sets the causation ID for event chains.
METHOD EventEnvelope.WithCausation(causationID: String) RETURNS EventEnvelope
    this.causationID = causationID
    RETURN this
END METHOD
```

## Step 3: Create JSON Schema Definitions

Store schemas in `/contracts/events/<event-type>/<version>.json`. Include `$id` with version, use `const` for event_type, and provide examples.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://schemas..com/events/facility.created/1.0.0",
  "title": "FacilityCreated",
  "description": "Published when a new facility is created.",
  "type": "object",
  "required": ["event_id", "event_type", "schema_version", "occurred_at", "aggregate_id", "correlation_id", "payload"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event identifier for idempotency."
    },
    "event_type": {
      "const": "facility.created"
    },
    "schema_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "occurred_at": {
      "type": "string",
      "format": "date-time"
    },
    "aggregate_id": {
      "type": "string",
      "pattern": "^fac-[a-z0-9]{6,}$"
    },
    "correlation_id": { "type": "string" },
    "payload": {
      "type": "object",
      "required": ["facility_id", "name", "location", "owner_id"],
      "properties": {
        "facility_id": { "type": "string", "pattern": "^fac-[a-z0-9]{6,}$" },
        "name": { "type": "string", "minLength": 1, "maxLength": 200 },
        "location": {
          "type": "object",
          "required": ["latitude", "longitude"],
          "properties": {
            "latitude": { "type": "number", "minimum": -90, "maximum": 90 },
            "longitude": { "type": "number", "minimum": -180, "maximum": 180 },
            "country": { "type": "string", "pattern": "^[A-Z]{2}$" },
            "timezone": { "type": "string" }
          }
        },
        "owner_id": { "type": "string" },
        "metadata": { "type": "object", "additionalProperties": true }
      }
    }
  }
}
```

## Step 4: Implement Event Types

Create strongly-typed structs matching your JSON Schema with constructor functions.

```pseudocode
// events/base

// DomainEvent is the interface all domain events implement.
INTERFACE DomainEvent
    EventID() RETURNS String
    EventType() RETURNS String
    SchemaVersion() RETURNS String
    OccurredAt() RETURNS Timestamp
    AggregateID() RETURNS String
END INTERFACE

// BaseEvent provides common fields for all events.
TYPE BaseEvent
    id: String
    eventType: String
    version: String
    occurred: Timestamp
    aggregate: String

METHOD BaseEvent.EventID() RETURNS String
    RETURN this.id
END METHOD

METHOD BaseEvent.EventType() RETURNS String
    RETURN this.eventType
END METHOD

METHOD BaseEvent.SchemaVersion() RETURNS String
    RETURN this.version
END METHOD

METHOD BaseEvent.OccurredAt() RETURNS Timestamp
    RETURN this.occurred
END METHOD

METHOD BaseEvent.AggregateID() RETURNS String
    RETURN this.aggregate
END METHOD
```

```pseudocode
// events/facility_events

CONSTANT EventTypeFacilityCreated = "facility.created"
CONSTANT SchemaVersionFacilityCreated = "1.0.0"

TYPE FacilityLocation
    latitude: Float
    longitude: Float
    country: String         // Optional
    timezone: String        // Optional

TYPE FacilityCreatedPayload
    facilityID: String
    name: String
    location: FacilityLocation
    ownerID: String
    metadata: Map<String, Any>     // Optional

TYPE FacilityCreated
    EXTENDS BaseEvent
    correlationID: String
    causationID: String            // Optional
    payload: FacilityCreatedPayload

// NewFacilityCreated creates a FacilityCreated event with all required fields.
CONSTRUCTOR NewFacilityCreated(
    facilityID: String,
    name: String,
    location: FacilityLocation,
    ownerID: String,
    correlationID: String
) RETURNS FacilityCreated
    RETURN FacilityCreated{
        BaseEvent: BaseEvent{
            id: GenerateUUID(),
            eventType: EventTypeFacilityCreated,
            version: SchemaVersionFacilityCreated,
            occurred: Now(),
            aggregate: facilityID
        },
        correlationID: correlationID,
        payload: FacilityCreatedPayload{
            facilityID: facilityID,
            name: name,
            location: location,
            ownerID: ownerID
        }
    }
END CONSTRUCTOR
```

## Step 5: Apply Semantic Versioning

Event schemas use semantic versioning to communicate compatibility:

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Add optional field | MINOR (1.0.0 -> 1.1.0) | Add `metadata` |
| Add required field | MAJOR (1.0.0 -> 2.0.0) | Add required `owner_id` |
| Remove field | MAJOR | Remove `legacy_id` |
| Change field type | MAJOR | string -> integer |
| Rename field | MAJOR | `facility_id` -> `id` |

```pseudocode
// events/version

TYPE Version
    major: Integer
    minor: Integer
    patch: Integer

CONSTRUCTOR ParseVersion(s: String) RETURNS Result<Version, Error>
    parts = Split(s, ".")
    IF Length(parts) != 3 THEN
        RETURN Error("invalid version: " + s)
    END IF

    major = ParseInt(parts[0])
    minor = ParseInt(parts[1])
    patch = ParseInt(parts[2])

    RETURN Ok(Version{major: major, minor: minor, patch: patch})
END CONSTRUCTOR

// IsCompatibleWith checks backward compatibility.
METHOD Version.IsCompatibleWith(consumer: Version) RETURNS Boolean
    IF this.major != consumer.major THEN
        RETURN FALSE
    END IF
    RETURN this.minor >= consumer.minor
END METHOD

FUNCTION CheckEventCompatibility(eventVersion: String, consumerVersion: String) RETURNS Result<Void, Error>
    evResult = ParseVersion(eventVersion)
    IF evResult.IsError() THEN
        RETURN evResult.Error()
    END IF
    ev = evResult.Value()

    cvResult = ParseVersion(consumerVersion)
    IF cvResult.IsError() THEN
        RETURN cvResult.Error()
    END IF
    cv = cvResult.Value()

    IF NOT ev.IsCompatibleWith(cv) THEN
        RETURN Error("incompatible: event=" + eventVersion + ", consumer=" + consumerVersion)
    END IF

    RETURN Ok()
END FUNCTION
```

## Step 6: Design for Evolution

Design events to evolve without breaking consumers. New optional fields are safe (MINOR). New required fields need MAJOR bump.

```pseudocode
// Version 1.0.0 - Original
TYPE FacilityCreatedPayloadV1
    facilityID: String
    name: String
    location: FacilityLocation
    ownerID: String

// Version 1.1.0 - Added optional metadata (MINOR)
TYPE FacilityCreatedPayloadV1_1
    facilityID: String
    name: String
    location: FacilityLocation
    ownerID: String
    metadata: Map<String, Any>     // NEW: optional

// Version 2.0.0 - Added required grid_zone (MAJOR)
TYPE FacilityCreatedPayloadV2
    facilityID: String
    name: String
    location: FacilityLocation
    ownerID: String
    gridZone: String               // NEW: required
    metadata: Map<String, Any>
```

Consumer strategy: check major version and route to appropriate handler:

```pseudocode
METHOD Consumer.Handle(envelope: EventEnvelope) RETURNS Result<Void, Error>
    versionResult = ParseVersion(envelope.schemaVersion)
    IF versionResult.IsError() THEN
        RETURN versionResult.Error()
    END IF
    version = versionResult.Value()

    SWITCH version.major
        CASE 1:
            payload = Deserialize<FacilityCreatedPayloadV1_1>(envelope.payload)
            RETURN this.processV1(payload.Value())
        CASE 2:
            payload = Deserialize<FacilityCreatedPayloadV2>(envelope.payload)
            RETURN this.processV2(payload.Value())
        DEFAULT:
            RETURN Error("unsupported version: " + version.major)
    END SWITCH
END METHOD
```

## Step 7: Test Event Serialization

```pseudocode
// events/facility_events_test

FUNCTION TestFacilityCreated_Serialization()
    location = FacilityLocation{
        latitude: 59.3293,
        longitude: 18.0686,
        country: "SE",
        timezone: "Europe/Stockholm"
    }

    event = NewFacilityCreated(
        "fac-abc123",
        "Solar Farm Alpha",
        location,
        "tenant-001",
        "corr-xyz789"
    )

    // Serialize and deserialize
    jsonBytes = Serialize(event)
    AssertNoError(jsonBytes)

    deserialized = Deserialize<FacilityCreated>(jsonBytes.Value())
    AssertNoError(deserialized)

    // Assert envelope
    AssertNotEmpty(deserialized.Value().EventID())
    AssertEqual("facility.created", deserialized.Value().EventType())
    AssertEqual("1.0.0", deserialized.Value().SchemaVersion())
    AssertEqual("fac-abc123", deserialized.Value().AggregateID())
    AssertWithinDuration(Now(), deserialized.Value().OccurredAt(), Second)

    // Assert payload
    AssertEqual("fac-abc123", deserialized.Value().payload.facilityID)
    AssertEqual("Solar Farm Alpha", deserialized.Value().payload.name)
    AssertEqual(59.3293, deserialized.Value().payload.location.latitude)
END FUNCTION

FUNCTION TestFacilityCreated_JSONStructure()
    location = FacilityLocation{latitude: 59.3293, longitude: 18.0686}
    event = NewFacilityCreated(
        "fac-abc123",
        "Test",
        location,
        "tenant-001",
        "corr-xyz789"
    )

    jsonBytes = Serialize(event)
    jsonMap = DeserializeToMap(jsonBytes.Value())

    // Verify required envelope fields
    AssertContains(jsonMap, "event_id")
    AssertContains(jsonMap, "event_type")
    AssertContains(jsonMap, "schema_version")
    AssertContains(jsonMap, "occurred_at")
    AssertContains(jsonMap, "aggregate_id")
    AssertContains(jsonMap, "payload")

    payload = jsonMap["payload"]
    AssertContains(payload, "facility_id")
    AssertContains(payload, "name")
    AssertContains(payload, "location")
END FUNCTION
```

### Schema Validation Test

```pseudocode
FUNCTION TestFacilityCreated_SchemaValidation()
    schemaPath = "../contracts/events/facility.created/1.0.0.json"
    schema = LoadJSONSchema(schemaPath)
    AssertNoError(schema)

    location = FacilityLocation{
        latitude: 59.3293,
        longitude: 18.0686,
        country: "SE",
        timezone: "Europe/Stockholm"
    }
    event = NewFacilityCreated(
        "fac-abc123",
        "Solar Farm Alpha",
        location,
        "tenant-001",
        "corr-xyz789"
    )

    jsonBytes = Serialize(event)
    jsonData = DeserializeToAny(jsonBytes.Value())

    validationResult = schema.Value().Validate(jsonData.Value())
    AssertNoError(validationResult, "event should validate against schema")
END FUNCTION
```

## Verification Checklist

After implementing your event schema, verify:

- [ ] Events are named in past-tense (facts, not commands)
- [ ] Event envelope includes all required fields (id, type, version, timestamp, aggregate_id)
- [ ] JSON Schema exists in `/contracts/events/<event-type>/<version>.json`
- [ ] Schema includes `$id` with version for registry
- [ ] Schema has `const` for event_type
- [ ] Types match JSON Schema structure exactly
- [ ] Constructor functions ensure valid event creation
- [ ] Schema version follows semantic versioning rules
- [ ] MINOR changes only add optional fields
- [ ] MAJOR changes are documented with migration guide
- [ ] Consumers check version compatibility before processing
- [ ] Serialization tests verify JSON structure
- [ ] Events can round-trip without data loss
