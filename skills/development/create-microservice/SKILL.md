---
name: create-microservice
description: "Step-by-step guide for scaffolding a new  microservice with Clean Architecture, Hexagonal, and DDD integration."
---

# Skill: Create Microservice

This skill teaches you how to scaffold a complete microservice following  architectural patterns. You'll create a production-ready service structure combining Clean Architecture layers, Hexagonal ports and adapters, DDD patterns, and serverless deployment.

A well-structured microservice ensures maintainability, testability, and clear domain boundaries. Following consistent patterns across services enables team members to quickly understand and contribute to any service in the monorepo. This skill guides you through creating the complete scaffolding for a new bounded context.

The scaffolding you create will support multiple entry points (API, event handlers, scheduled tasks), proper dependency injection, contract-driven development with OpenAPI, and infrastructure-as-code deployment.

## Prerequisites

- Understanding of Clean Architecture, Hexagonal Architecture, and DDD concepts
- Bounded context identified and domain model designed
- Familiarity with serverless patterns and NoSQL databases

## Overview

In this skill, you will:
1. Initialize the module and create the monorepo directory structure
2. Create the domain layer with aggregates, value objects, events, and errors
3. Create the application layer with ports (inbound/outbound) and use cases
4. Create primary adapters (serverless handlers)
5. Create secondary adapters (repository, event publisher)
6. Set up the entry point with dependency injection
7. Define the OpenAPI contract
8. Create the Makefile for build, test, and deployment

## Step 1: Initialize Project Structure

Create the monorepo-style directory structure that follows Clean Architecture and Hexagonal patterns.

### Create Directory Structure

```bash
# Create service directory in the monorepo
mkdir -p services/asset-svc
cd services/asset-svc

# Create Clean Architecture layer directories
mkdir -p cmd/api
mkdir -p cmd/worker
mkdir -p cmd/eventhandler

# Create internal core (the Hexagon)
mkdir -p internal/core/domain/asset
mkdir -p internal/core/domain/services
mkdir -p internal/core/ports/inbound
mkdir -p internal/core/ports/outbound
mkdir -p internal/core/application

# Create adapters
mkdir -p internal/adapters/inbound/lambda
mkdir -p internal/adapters/inbound/http
mkdir -p internal/adapters/outbound/repository
mkdir -p internal/adapters/outbound/eventpublisher

# Create handlers
mkdir -p internal/handlers

# Create contracts and API specifications
mkdir -p api
mkdir -p contracts/events
mkdir -p contracts/mocks

# Create deployment and testing directories
mkdir -p deploy/iac/constructs
mkdir -p tests/unit
mkdir -p tests/service
mkdir -p tests/contract
mkdir -p tests/integration
```

### Directory Structure Explained

```
services/asset-svc/                       # One Bounded Context = One Microservice
├── api/
│   └── openapi.yaml                      # HTTP API contract (OpenAPI 3.x)
├── contracts/
│   ├── events/                           # Domain event schemas (JSON Schema)
│   └── mocks/                            # Generated contract mocks
├── cmd/                                  # Entry points (handlers)
├── internal/
│   ├── handlers/                         # Handler implementations
│   ├── core/                             # The Hexagon (Application Core)
│   │   ├── domain/                       # DDD Domain Model
│   │   ├── ports/                        # Hexagonal Ports
│   │   └── application/                  # Use Cases Layer
│   └── adapters/                         # Hexagonal Adapters
│       ├── inbound/
│       └── outbound/
├── deploy/
│   └── iac/                              # Infrastructure as Code
├── tests/
└── Makefile
```

## Step 2: Create Domain Layer

The domain layer contains all business rules and has zero dependencies on infrastructure.

### Domain Errors

```pseudocode
// internal/core/domain/asset/errors

CONSTANT ErrAssetNotFound = Error("asset not found")
CONSTANT ErrAssetAlreadyExists = Error("asset already exists")
CONSTANT ErrInvalidAssetState = Error("operation not allowed in current asset state")
CONSTANT ErrInvalidCapacity = Error("capacity must be positive")
CONSTANT ErrInvalidStateOfCharge = Error("state of charge must be between 0 and 100")
CONSTANT ErrFacilityRequired = Error("facility ID is required")
CONSTANT ErrNameRequired = Error("asset name is required")
```

### Value Objects

```pseudocode
// internal/core/domain/asset/capacity

TYPE Capacity
    kWh: Float

CONSTRUCTOR NewCapacity(kWh: Float) RETURNS Result<Capacity, Error>
    IF kWh <= 0 THEN
        RETURN Error(ErrInvalidCapacity + ": got " + kWh + " kWh")
    END IF
    RETURN Ok(Capacity{kWh: kWh})
END CONSTRUCTOR

METHOD Capacity.KWh() RETURNS Float
    RETURN this.kWh
END METHOD
```

```pseudocode
// internal/core/domain/asset/state_of_charge

TYPE StateOfCharge
    percentage: Float

CONSTRUCTOR NewStateOfCharge(percentage: Float) RETURNS Result<StateOfCharge, Error>
    IF percentage < 0 OR percentage > 100 THEN
        RETURN Error(ErrInvalidStateOfCharge + ": got " + percentage + "%")
    END IF
    RETURN Ok(StateOfCharge{percentage: percentage})
END CONSTRUCTOR

METHOD StateOfCharge.Percentage() RETURNS Float
    RETURN this.percentage
END METHOD

METHOD StateOfCharge.IsLow() RETURNS Boolean
    RETURN this.percentage < 20
END METHOD

METHOD StateOfCharge.IsCritical() RETURNS Boolean
    RETURN this.percentage < 10
END METHOD
```

### Domain Events

```pseudocode
// internal/core/domain/asset/events

INTERFACE Event
    EventType() RETURNS String
    OccurredAt() RETURNS Timestamp
    AggregateID() RETURNS String
END INTERFACE

TYPE BaseEvent
    occurredAt: Timestamp
    aggregateID: String

TYPE BatteryRegistered
    EXTENDS BaseEvent
    facilityID: String
    name: String
    capacityKWh: Float

METHOD BatteryRegistered.EventType() RETURNS String
    RETURN "asset.battery.registered"
END METHOD

TYPE StateOfChargeUpdated
    EXTENDS BaseEvent
    previousSoC: Float
    newSoC: Float

METHOD StateOfChargeUpdated.EventType() RETURNS String
    RETURN "asset.battery.soc_updated"
END METHOD
```

### Aggregate Root

```pseudocode
// internal/core/domain/asset/battery

TYPE AssetState = String

CONSTANT AssetStateOnline: AssetState = "online"
CONSTANT AssetStateOffline: AssetState = "offline"
CONSTANT AssetStateFault: AssetState = "fault"
CONSTANT AssetStateMaintenance: AssetState = "maintenance"

TYPE Battery
    id: String
    facilityID: String
    name: String
    capacity: Capacity
    soc: StateOfCharge
    state: AssetState
    registeredAt: Timestamp
    updatedAt: Timestamp
    uncommittedEvents: List<Event>

CONSTRUCTOR NewBattery(facilityID: String, name: String, capacity: Capacity) RETURNS Result<Battery, Error>
    IF facilityID == "" THEN
        RETURN Error(ErrFacilityRequired)
    END IF
    IF name == "" THEN
        RETURN Error(ErrNameRequired)
    END IF

    id = GenerateUUID()
    now = Now()
    initialSoC = MustStateOfCharge(50)

    battery = Battery{
        id: id,
        facilityID: facilityID,
        name: name,
        capacity: capacity,
        soc: initialSoC,
        state: AssetStateOnline,
        registeredAt: now,
        updatedAt: now,
        uncommittedEvents: []
    }

    battery.raise(NewBatteryRegistered(id, facilityID, name, capacity.KWh()))

    RETURN Ok(battery)
END CONSTRUCTOR

METHOD Battery.UpdateStateOfCharge(newSoC: StateOfCharge) RETURNS Result<Void, Error>
    IF this.state == AssetStateFault THEN
        RETURN Error(ErrInvalidAssetState + ": battery is in fault state")
    END IF

    previousSoC = this.soc
    this.soc = newSoC
    this.updatedAt = Now()

    this.raise(NewStateOfChargeUpdated(this.id, previousSoC.Percentage(), newSoC.Percentage()))

    RETURN Ok()
END METHOD

METHOD Battery.UncommittedEvents() RETURNS List<Event>
    RETURN this.uncommittedEvents
END METHOD

METHOD Battery.ClearUncommittedEvents()
    this.uncommittedEvents = []
END METHOD
```

## Step 3: Create Application Layer

### Output Ports (Driven Interfaces)

```pseudocode
// internal/core/ports/outbound/repository

INTERFACE BatteryRepository
    Save(ctx: Context, battery: Battery) RETURNS Result<Void, Error>
    FindByID(ctx: Context, id: String) RETURNS Result<Battery, Error>
    FindByFacility(ctx: Context, facilityID: String) RETURNS Result<List<Battery>, Error>
    Delete(ctx: Context, id: String) RETURNS Result<Void, Error>
END INTERFACE
```

```pseudocode
// internal/core/ports/outbound/publisher

INTERFACE EventPublisher
    Publish(ctx: Context, events: List<Event>) RETURNS Result<Void, Error>
END INTERFACE
```

### Input Ports (Commands and Queries)

```pseudocode
// internal/core/ports/inbound/commands

TYPE RegisterBatteryCommand
    facilityID: String
    name: String
    capacityKWh: Float

TYPE RegisterBatteryResult
    batteryID: String

INTERFACE BatteryCommandHandler
    RegisterBattery(ctx: Context, cmd: RegisterBatteryCommand) RETURNS Result<RegisterBatteryResult, Error>
    UpdateStateOfCharge(ctx: Context, cmd: UpdateStateOfChargeCommand) RETURNS Result<Void, Error>
END INTERFACE
```

### Use Cases (Application Service)

```pseudocode
// internal/core/application/service

TYPE BatteryService
    repo: BatteryRepository
    publisher: EventPublisher

CONSTRUCTOR NewBatteryService(repo: BatteryRepository, publisher: EventPublisher) RETURNS BatteryService
    RETURN BatteryService{repo: repo, publisher: publisher}
END CONSTRUCTOR

METHOD BatteryService.RegisterBattery(ctx: Context, cmd: RegisterBatteryCommand) RETURNS Result<RegisterBatteryResult, Error>
    // Create validated value object
    capacityResult = NewCapacity(cmd.capacityKWh)
    IF capacityResult.IsError() THEN
        RETURN Error("invalid capacity: " + capacityResult.Error())
    END IF

    // Create aggregate (factory enforces invariants)
    batteryResult = NewBattery(cmd.facilityID, cmd.name, capacityResult.Value())
    IF batteryResult.IsError() THEN
        RETURN Error("failed to create battery: " + batteryResult.Error())
    END IF
    battery = batteryResult.Value()

    // Persist aggregate
    saveResult = this.repo.Save(ctx, battery)
    IF saveResult.IsError() THEN
        RETURN Error("failed to save battery: " + saveResult.Error())
    END IF

    // Publish domain events
    this.publisher.Publish(ctx, battery.UncommittedEvents())
    battery.ClearUncommittedEvents()

    RETURN Ok(RegisterBatteryResult{batteryID: battery.ID()})
END METHOD
```

## Step 4: Create Primary Adapters

```pseudocode
// internal/adapters/inbound/lambda/handler

TYPE APIHandler
    commands: BatteryCommandHandler
    queries: BatteryQueryHandler

CONSTRUCTOR NewAPIHandler(commands: BatteryCommandHandler, queries: BatteryQueryHandler) RETURNS APIHandler
    RETURN APIHandler{commands: commands, queries: queries}
END CONSTRUCTOR

METHOD APIHandler.Handle(ctx: Context, request: APIRequest) RETURNS Result<APIResponse, Error>
    SWITCH
        CASE request.Method == "POST" AND request.Resource == "/batteries":
            RETURN this.registerBattery(ctx, request)
        CASE request.Method == "GET" AND request.Resource == "/batteries/{id}":
            RETURN this.getBattery(ctx, request)
        DEFAULT:
            RETURN this.notFound()
    END SWITCH
END METHOD
```

## Step 5: Create Secondary Adapters

### Repository Adapter

```pseudocode
// internal/adapters/outbound/repository/adapter

TYPE BatteryRepositoryAdapter
    client: DatabaseClient
    tableName: String

CONSTRUCTOR NewBatteryRepository(client: DatabaseClient, tableName: String) RETURNS BatteryRepositoryAdapter
    RETURN BatteryRepositoryAdapter{client: client, tableName: tableName}
END CONSTRUCTOR

METHOD BatteryRepositoryAdapter.Save(ctx: Context, battery: Battery) RETURNS Result<Void, Error>
    item = MapToPersistenceModel(battery)
    result = this.client.PutItem(ctx, this.tableName, item)
    IF result.IsError() THEN
        RETURN Error("failed to put item: " + result.Error())
    END IF
    RETURN Ok()
END METHOD

METHOD BatteryRepositoryAdapter.FindByID(ctx: Context, id: String) RETURNS Result<Battery, Error>
    result = this.client.GetItem(ctx, this.tableName, id)
    IF result.IsError() THEN
        RETURN Error("failed to get item: " + result.Error())
    END IF
    IF result.Value() == NULL THEN
        RETURN Error(ErrAssetNotFound)
    END IF
    RETURN MapToDomainModel(result.Value())
END METHOD
```

### Event Publisher Adapter

```pseudocode
// internal/adapters/outbound/eventpublisher/adapter

TYPE EventPublisherAdapter
    client: MessageBusClient
    busName: String
    source: String

CONSTRUCTOR NewEventPublisher(client: MessageBusClient, busName: String) RETURNS EventPublisherAdapter
    RETURN EventPublisherAdapter{client: client, busName: busName, source: ".asset-svc"}
END CONSTRUCTOR

METHOD EventPublisherAdapter.Publish(ctx: Context, events: List<Event>) RETURNS Result<Void, Error>
    IF Length(events) == 0 THEN
        RETURN Ok()
    END IF

    entries = []
    FOR EACH event IN events DO
        entries = Append(entries, EventEntry{
            busName: this.busName,
            source: this.source,
            detailType: event.EventType(),
            detail: ToJSON(event)
        })
    END FOR

    result = this.client.PublishEvents(ctx, entries)
    IF result.IsError() THEN
        RETURN Error("failed to publish events: " + result.Error())
    END IF

    RETURN Ok()
END METHOD
```

## Step 6: Create Entry Point

```pseudocode
// cmd/api/main

VARIABLE handler: APIHandler

FUNCTION init()
    ctx = NewContext()
    cfg = LoadConfig()

    dbClient = NewDatabaseClient(cfg)
    messageBusClient = NewMessageBusClient(cfg)

    tableName = GetEnv("TABLE_NAME")
    busName = GetEnv("EVENT_BUS_NAME")

    repo = NewBatteryRepository(dbClient, tableName)
    publisher = NewEventPublisher(messageBusClient, busName)
    service = NewBatteryService(repo, publisher)
    handler = NewAPIHandler(service, service)
END FUNCTION

FUNCTION main()
    StartServerlessRuntime(handler.Handle)
END FUNCTION
```

## Verification Checklist

### Structure
- [ ] Directory structure follows Clean Architecture layers
- [ ] The hexagon is clearly defined in `internal/core/`
- [ ] Ports are in `internal/core/ports/` with `inbound/` and `outbound/` separation
- [ ] Adapters are in `internal/adapters/` with `inbound/` and `outbound/` separation

### Domain Layer
- [ ] Domain layer has zero infrastructure imports
- [ ] All value objects validate on construction and are immutable
- [ ] Aggregate root enforces all business invariants
- [ ] Domain events are raised from aggregate methods

### Application Layer
- [ ] Repository and publisher interfaces defined in `ports/outbound/`
- [ ] Command and query interfaces defined in `ports/inbound/`
- [ ] Use cases orchestrate domain operations without business logic

### Adapters
- [ ] Adapters are thin (mapping, serialization, no business logic)
- [ ] Repository adapter maps between domain and persistence models
- [ ] Event publisher adapter handles event serialization

### Build
- [ ] Makefile has `build`, `test`, `lint`, `deploy`, `clean` targets
- [ ] Tests can run without cloud credentials (mocked adapters)
