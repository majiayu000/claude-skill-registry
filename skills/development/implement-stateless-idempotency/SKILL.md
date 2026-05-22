---
name: implement-stateless-idempotency
description: "Step-by-step guide for implementing stateless services and idempotent operations following  patterns."
---

# Skill: Implement Stateless and Idempotent Services

This skill teaches you how to implement stateless services and idempotent operations following  architectural patterns. You'll learn to build services that can scale horizontally, handle retries safely, and maintain data consistency in distributed systems.

Stateless services and idempotent operations are fundamental requirements for cloud-native applications. They enable horizontal scaling (any instance can handle any request), fault tolerance (retries are safe), and simplified deployment (no session affinity needed). In serverless environments, statelessness is enforced by design.

Idempotency ensures that calling an operation multiple times with the same input produces the same result. This is critical when working with at-least-once delivery systems like message queues, event buses, or any scenario where network failures may cause retries.

## Prerequisites

- Understanding of distributed systems concepts
- Familiarity with Clean Architecture principles
- Understanding of event-driven architectures

## Overview

In this skill, you will:
1. Understand idempotency requirements and patterns
2. Implement idempotency key storage
3. Create idempotency middleware for handlers
4. Design upsert operations for natural idempotency
5. Handle concurrent requests with conditional writes
6. Implement event deduplication
7. Test idempotent operations

## Step 1: Understand Idempotency Requirements

Idempotency protects against duplicate processing from:
- Network retries (client didn't receive response, retries)
- Message redelivery (at-least-once delivery)
- Event duplication (event bus may deliver same event twice)
- User double-clicks (frontend form submissions)

### Idempotency Types and Records

```pseudocode
// core/domain/idempotency/types

TYPE IdempotencyKey = String

TYPE IdempotencyRecord
    key: IdempotencyKey
    status: ProcessStatus
    result: Bytes
    error: String
    processedAt: Timestamp
    expiresAt: Timestamp

TYPE ProcessStatus = String

CONSTANT StatusInProgress: ProcessStatus = "IN_PROGRESS"
CONSTANT StatusCompleted: ProcessStatus = "COMPLETED"
CONSTANT StatusFailed: ProcessStatus = "FAILED"

METHOD ProcessStatus.IsTerminal() RETURNS Boolean
    RETURN this == StatusCompleted OR this == StatusFailed
END METHOD
```

### Domain Errors

```pseudocode
// core/domain/idempotency/errors

CONSTANT ErrDuplicateRequest = Error("duplicate request: operation already processed")
CONSTANT ErrOperationInProgress = Error("operation in progress by another request")
CONSTANT ErrIdempotencyKeyRequired = Error("idempotency key is required")
CONSTANT ErrIdempotencyKeyExpired = Error("idempotency record has expired")
```

## Step 2: Implement Idempotency Key Storage

### Repository Port

```pseudocode
// core/application/ports/outports/idempotency_store

INTERFACE IdempotencyStore
    TryAcquire(ctx: Context, key: IdempotencyKey, ttl: Duration) RETURNS Result<IdempotencyRecord?, Error>
    Complete(ctx: Context, key: IdempotencyKey, result: Bytes) RETURNS Result<Void, Error>
    Fail(ctx: Context, key: IdempotencyKey, errMsg: String) RETURNS Result<Void, Error>
    Get(ctx: Context, key: IdempotencyKey) RETURNS Result<IdempotencyRecord?, Error>
END INTERFACE
```

### Database Implementation

```pseudocode
// adapters/secondary/database/idempotency_store

TYPE IdempotencyStoreAdapter
    client: DatabaseClient
    tableName: String

CONSTRUCTOR NewIdempotencyStore(client: DatabaseClient, tableName: String) RETURNS IdempotencyStoreAdapter
    RETURN IdempotencyStoreAdapter{client: client, tableName: tableName}
END CONSTRUCTOR

METHOD IdempotencyStoreAdapter.TryAcquire(ctx: Context, key: IdempotencyKey, ttl: Duration) RETURNS Result<IdempotencyRecord?, Error>
    now = Now()
    expiresAt = now.Add(ttl)

    item = Map{
        "pk": key,
        "status": StatusInProgress,
        "processedAt": now.Unix(),
        "ttl": expiresAt.Unix()
    }

    // Conditional put: only succeed if key doesn't exist
    result = this.client.PutItemConditional(ctx, this.tableName, item, "pk NOT EXISTS")

    IF result.IsError() THEN
        IF result.Error().IsConditionFailed() THEN
            existing = this.Get(ctx, key)
            IF existing.IsError() THEN
                RETURN Error("failed to get existing record: " + existing.Error())
            END IF
            RETURN Ok(existing.Value())
        END IF
        RETURN Error("failed to put item: " + result.Error())
    END IF

    RETURN Ok(NULL)
END METHOD

METHOD IdempotencyStoreAdapter.Complete(ctx: Context, key: IdempotencyKey, result: Bytes) RETURNS Result<Void, Error>
    update = Map{"status": StatusCompleted, "result": result}
    RETURN this.client.UpdateItem(ctx, this.tableName, key, update)
END METHOD

METHOD IdempotencyStoreAdapter.Fail(ctx: Context, key: IdempotencyKey, errMsg: String) RETURNS Result<Void, Error>
    update = Map{"status": StatusFailed, "error": errMsg}
    RETURN this.client.UpdateItem(ctx, this.tableName, key, update)
END METHOD
```

## Step 3: Create Idempotency Middleware

```pseudocode
// core/application/middleware/idempotency

TYPE IdempotentHandler<Request, Response>
    store: IdempotencyStore
    ttl: Duration
    keyFunc: Function(Request) RETURNS IdempotencyKey
    handler: Function(Context, Request) RETURNS Result<Response, Error>

CONSTRUCTOR NewIdempotentHandler<Request, Response>(
    store: IdempotencyStore,
    ttl: Duration,
    keyFunc: Function(Request) RETURNS IdempotencyKey,
    handler: Function(Context, Request) RETURNS Result<Response, Error>
) RETURNS IdempotentHandler<Request, Response>
    RETURN IdempotentHandler<Request, Response>{
        store: store, ttl: ttl, keyFunc: keyFunc, handler: handler
    }
END CONSTRUCTOR

METHOD IdempotentHandler<Request, Response>.Handle(ctx: Context, req: Request) RETURNS Result<Response, Error>
    key = this.keyFunc(req)
    IF key == "" THEN
        RETURN Error(ErrIdempotencyKeyRequired)
    END IF

    existingResult = this.store.TryAcquire(ctx, key, this.ttl)
    IF existingResult.IsError() THEN
        RETURN Error("failed to acquire idempotency lock: " + existingResult.Error())
    END IF
    existing = existingResult.Value()

    IF existing != NULL THEN
        SWITCH existing.status
            CASE StatusCompleted:
                result = Deserialize<Response>(existing.result)
                RETURN Ok(result.Value())
            CASE StatusFailed:
                RETURN Error(ErrDuplicateRequest + ": " + existing.error)
            CASE StatusInProgress:
                RETURN Error(ErrOperationInProgress)
        END SWITCH
    END IF

    result = this.handler(ctx, req)
    IF result.IsError() THEN
        this.store.Fail(ctx, key, result.Error().Message())
        RETURN result.Error()
    END IF

    resultBytes = Serialize(result.Value())
    this.store.Complete(ctx, key, resultBytes.Value())

    RETURN result
END METHOD
```

## Step 4: Design Upsert Operations

```pseudocode
// adapters/secondary/database/asset_repository

TYPE AssetRepository
    client: DatabaseClient
    tableName: String

METHOD AssetRepository.UpsertAsset(ctx: Context, a: Asset) RETURNS Result<Void, Error>
    item = Map{
        "pk": "ASSET#" + a.ID,
        "sk": "METADATA",
        "assetID": a.ID,
        "facilityID": a.FacilityID,
        "assetType": a.Type,
        "capacityKW": a.Capacity,
        "currentLoad": a.CurrentLoad,
        "state": a.State,
        "updatedAt": Now()
    }

    // PutItem is idempotent: same key, same data = same result
    result = this.client.PutItem(ctx, this.tableName, item)
    IF result.IsError() THEN
        RETURN Error("failed to put asset: " + result.Error())
    END IF

    RETURN Ok()
END METHOD
```

## Step 5: Handle Concurrent Requests with Conditional Writes

```pseudocode
// adapters/secondary/database/versioned_repository

CONSTANT ErrConcurrentModification = Error("concurrent modification detected")

TYPE VersionedAsset
    id: String
    version: Integer
    state: String
    currentLoad: Float

METHOD AssetRepository.UpdateAssetWithVersion(ctx: Context, asset: VersionedAsset) RETURNS Result<Void, Error>
    newVersion = asset.version + 1

    condition = "pk NOT EXISTS OR version = :expectedVersion"
    conditionValues = Map{":expectedVersion": asset.version}

    asset.version = newVersion

    result = this.client.PutItemConditional(ctx, this.tableName, asset, condition, conditionValues)

    IF result.IsError() THEN
        IF result.Error().IsConditionFailed() THEN
            RETURN Error(ErrConcurrentModification)
        END IF
        RETURN Error("failed to update asset: " + result.Error())
    END IF

    RETURN Ok()
END METHOD
```

## Step 6: Implement Event Deduplication

```pseudocode
// core/application/handlers/event_handler

INTERFACE ProcessedEventStore
    Exists(ctx: Context, eventID: String) RETURNS Result<Boolean, Error>
    MarkProcessed(ctx: Context, eventID: String, ttl: Duration) RETURNS Result<Void, Error>
END INTERFACE

TYPE AssetEventHandler
    processedStore: ProcessedEventStore
    assetRepo: AssetRepository

TYPE EventEnvelope
    eventID: String
    eventType: String
    aggregateID: String
    occurredAt: Timestamp
    payload: Bytes

METHOD AssetEventHandler.Handle(ctx: Context, event: EventEnvelope) RETURNS Result<Void, Error>
    // Step 1: Check if already processed
    existsResult = this.processedStore.Exists(ctx, event.eventID)
    IF existsResult.IsError() THEN
        RETURN Error("failed to check event status: " + existsResult.Error())
    END IF
    IF existsResult.Value() THEN
        RETURN Ok()  // Already processed - idempotent behavior
    END IF

    // Step 2: Process the event based on type
    SWITCH event.eventType
        CASE "asset.state_changed":
            processResult = this.handleAssetStateChanged(ctx, event)
            IF processResult.IsError() THEN
                RETURN processResult.Error()
            END IF
        CASE "asset.registered":
            processResult = this.handleAssetRegistered(ctx, event)
            IF processResult.IsError() THEN
                RETURN processResult.Error()
            END IF
        DEFAULT:
            RETURN Error("unknown event type: " + event.eventType)
    END SWITCH

    // Step 3: Mark as processed with 30-day TTL
    this.processedStore.MarkProcessed(ctx, event.eventID, Duration(30 * Day))

    RETURN Ok()
END METHOD
```

## Step 7: Stateless Handler

```pseudocode
// cmd/api/main

TYPE Handler
    eventHandler: AssetEventHandler

VARIABLE handler: Handler

FUNCTION init()
    ctx = NewContext()
    cfg = LoadConfig()
    dbClient = NewDatabaseClient(cfg)

    tableName = GetEnv("TABLE_NAME")
    processedStore = NewProcessedEventStore(dbClient, tableName)
    assetRepo = NewAssetRepository(dbClient, tableName)

    handler = Handler{
        eventHandler: NewAssetEventHandler(processedStore, assetRepo)
    }
END FUNCTION

METHOD Handler.Handle(ctx: Context, event: EventBridgeEvent) RETURNS Result<Void, Error>
    envelope = EventEnvelope{
        eventID: event.ID,
        eventType: event.DetailType,
        occurredAt: event.Time,
        payload: event.Detail
    }

    RETURN this.eventHandler.Handle(ctx, envelope)
END METHOD

FUNCTION main()
    StartServerlessRuntime(handler.Handle)
END FUNCTION
```

## Verification Checklist

- [ ] No mutable global state between requests
- [ ] All state stored in external systems (database, cache, storage)
- [ ] Idempotency keys uniquely identify operations
- [ ] Deduplication lookup checks before processing
- [ ] Upsert operations used for persistence
- [ ] Conditional writes handle concurrent requests
- [ ] Event IDs checked for deduplication
- [ ] TTL configured for idempotency records
- [ ] Failed operations properly marked for retry visibility
- [ ] Same input always produces same output (deterministic)
- [ ] Middleware can be applied to any handler uniformly
