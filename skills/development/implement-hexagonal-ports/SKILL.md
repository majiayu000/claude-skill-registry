---
name: implement-hexagonal-ports
description: "Step-by-step guide for implementing Hexagonal Architecture ports and adapters."
metadata:
  type: implementation
  patterns: ["Hexagonal Architecture", "Ports and Adapters"]
---

# Skill: Implement Hexagonal Ports

This skill teaches you how to implement Hexagonal Architecture (Ports & Adapters) following  patterns. You'll learn to create clean boundaries between your application core and the outside world, enabling easy testing and adapter swapping.

Hexagonal Architecture lets you drive an application from users, programs, tests, or batch scripts while developing in isolation from runtime devices and databases. The key insight is that your application core defines interfaces (ports) that external code (adapters) must implement, inverting the dependency direction.

This approach provides multiple benefits: test your business logic without infrastructure, swap database implementations without changing core code, and trigger the same use case from REST API, CLI, or event handlers.

## Prerequisites

- Understanding of Clean Architecture principles
- A domain model ready for integration (aggregates, value objects)
- Familiarity with dependency injection patterns

## Overview

In this skill, you will:
1. Define InPorts (Commands and Queries) as interfaces for driving the application
2. Define OutPorts (Repository and external service interfaces) for driven operations
3. Implement a driving adapter (API handler) that calls InPorts
4. Implement a driven adapter (Repository) that implements OutPorts
5. Wire dependencies together using constructor injection
6. Test with adapter substitution for isolation

## Step 1: Define InPorts (Commands and Queries)

InPorts are driving ports - they define how external actors interact with your application. Commands mutate state, queries read state. These interfaces live in the application layer and are owned by your application, not by the callers.

### Command InPort

Commands represent intentions to change state. Define them as explicit types with a use case that executes them.

```pseudocode
// core/application/ports/inports/commands

// RegisterAssetCommand represents the intent to register a new energy asset.
// Commands are immutable data structures containing all input needed.
TYPE RegisterAssetCommand
    FacilityID  String
    Name        String
    AssetType   String
    CapacityKWh Float64
END TYPE

// RegisterAssetResult contains the outcome of successful registration.
TYPE RegisterAssetResult
    AssetID String
END TYPE

// RegisterAssetHandler defines the port for registering assets.
// This is an InPort - driving adapters (API, CLI) call this interface.
INTERFACE RegisterAssetHandler
    METHOD Handle(ctx Context, cmd RegisterAssetCommand) RETURNS (RegisterAssetResult, Error)
END INTERFACE

// UpdateAssetStateCommand represents the intent to update asset operational state.
TYPE UpdateAssetStateCommand
    AssetID  String
    NewState String
    Reason   String
END TYPE

// UpdateAssetStateHandler defines the port for state updates.
INTERFACE UpdateAssetStateHandler
    METHOD Handle(ctx Context, cmd UpdateAssetStateCommand) RETURNS Error
END INTERFACE
```

### Query InPort

Queries retrieve data without side effects. They return read models optimized for the caller's needs.

```pseudocode
// core/application/ports/inports/queries

// GetAssetQuery represents a request to retrieve asset details.
TYPE GetAssetQuery
    AssetID String
END TYPE

// AssetDTO is the read model returned by queries.
// DTOs are presentation-friendly, not domain objects.
TYPE AssetDTO
    ID           String
    FacilityID   String
    Name         String
    AssetType    String
    CapacityKWh  Float64
    CurrentState String
    LastUpdated  DateTime
END TYPE

// GetAssetHandler defines the port for retrieving assets.
INTERFACE GetAssetHandler
    METHOD Handle(ctx Context, query GetAssetQuery) RETURNS (AssetDTO, Error)
END INTERFACE

// ListAssetsByFacilityQuery retrieves all assets for a facility.
TYPE ListAssetsByFacilityQuery
    FacilityID String
    Limit      Integer
    Offset     Integer
END TYPE

// ListAssetsByFacilityHandler defines the port for listing assets.
INTERFACE ListAssetsByFacilityHandler
    METHOD Handle(ctx Context, query ListAssetsByFacilityQuery) RETURNS (List<AssetDTO>, Error)
END INTERFACE
```

InPorts are owned by the application layer. External code (API handlers, HTTP controllers, CLI) must conform to these interfaces. The application never imports adapter code.

## Step 2: Define OutPorts (Repository and External Service Interfaces)

OutPorts are driven ports - they define what external resources your application needs. The application calls these interfaces; adapters implement them. OutPorts express domain concepts, not infrastructure details.

### Repository OutPort

Repositories abstract persistence. The interface is defined in the domain or application layer, using domain types.

```pseudocode
// core/application/ports/outports/asset_repository

// AssetRepository defines persistence operations for Asset aggregates.
// This is an OutPort - driven adapters (database implementations) implement this.
INTERFACE AssetRepository
    // Save persists the asset aggregate.
    // Implementations should also handle publishing uncommitted domain events.
    METHOD Save(ctx Context, asset Asset) RETURNS Error

    // FindByID retrieves an asset by its unique identifier.
    // Returns ErrAssetNotFound if the asset doesn't exist.
    METHOD FindByID(ctx Context, id String) RETURNS (Asset, Error)

    // FindByFacility retrieves all assets belonging to a facility.
    METHOD FindByFacility(ctx Context, facilityID String) RETURNS (List<Asset>, Error)

    // Delete removes an asset from persistence.
    METHOD Delete(ctx Context, id String) RETURNS Error
END INTERFACE
```

### External Service OutPort

External integrations (weather APIs, pricing services, notification systems) are also OutPorts.

```pseudocode
// core/application/ports/outports/external_services

// WeatherForecast represents weather data needed by the domain.
// This is a domain concept, not a third-party API response.
TYPE WeatherForecast
    Location    String
    Temperature Float64
    Humidity    Float64
    ForecastAt  DateTime
END TYPE

// WeatherProvider abstracts weather forecast retrieval.
// Could be implemented by any weather service adapter or mock for testing.
INTERFACE WeatherProvider
    METHOD GetForecast(ctx Context, location String, at DateTime) RETURNS (WeatherForecast, Error)
END INTERFACE

// PricePoint represents electricity price at a point in time.
TYPE PricePoint
    Timestamp DateTime
    PriceEUR  Float64
    Zone      String
END TYPE

// PricingProvider abstracts electricity price retrieval.
INTERFACE PricingProvider
    METHOD GetPrices(ctx Context, zone String, from DateTime, to DateTime) RETURNS (List<PricePoint>, Error)
END INTERFACE

// EventPublisher abstracts domain event publishing.
INTERFACE EventPublisher
    METHOD Publish(ctx Context, events List<Event>) RETURNS Error
END INTERFACE
```

OutPorts express what the application needs in domain terms. They don't leak infrastructure details like table names or message bus ARNs - those belong in adapters.

## Step 3: Implement Use Cases (Application Services)

Use cases implement InPorts and orchestrate domain logic using OutPorts. They're the bridge between ports.

```pseudocode
// core/application/usecases/register_asset

// RegisterAssetUseCase implements RegisterAssetHandler.
// It orchestrates domain operations without containing business logic.
TYPE RegisterAssetUseCase
    repo      AssetRepository
    publisher EventPublisher
END TYPE

// Constructor creates the use case with required dependencies.
// Dependencies are injected as OutPort interfaces, not concrete implementations.
CONSTRUCTOR NewRegisterAssetUseCase(repo AssetRepository, publisher EventPublisher)
    RETURNS RegisterAssetUseCase
    RETURN RegisterAssetUseCase{repo: repo, publisher: publisher}
END CONSTRUCTOR

// Handle executes the registration use case.
// This method implements RegisterAssetHandler.
METHOD (uc RegisterAssetUseCase) Handle(ctx Context, cmd RegisterAssetCommand)
    RETURNS (RegisterAssetResult, Error)

    // Create validated value object
    capacity, err := NewCapacity(cmd.CapacityKWh)
    IF err != nil THEN
        RETURN nil, Error("invalid capacity: " + err)
    END IF

    // Create aggregate (domain logic in aggregate factory)
    newAsset, err := NewAsset(cmd.FacilityID, cmd.Name, AssetType(cmd.AssetType), capacity)
    IF err != nil THEN
        RETURN nil, Error("failed to create asset: " + err)
    END IF

    // Persist via OutPort (repository)
    IF err := uc.repo.Save(ctx, newAsset); err != nil THEN
        RETURN nil, Error("failed to save asset: " + err)
    END IF

    // Publish domain events via OutPort
    IF err := uc.publisher.Publish(ctx, newAsset.UncommittedEvents()); err != nil THEN
        RETURN nil, Error("failed to publish events: " + err)
    END IF

    newAsset.ClearUncommittedEvents()

    RETURN RegisterAssetResult{AssetID: newAsset.ID()}, nil
END METHOD
```

Use cases orchestrate but don't contain business logic - that belongs in aggregates. They load aggregates, call methods, and persist changes.

## Step 4: Implement Driving Adapters (API Handler)

Driving adapters call InPorts. They translate external formats (HTTP requests, messages) into domain commands/queries.

```pseudocode
// adapters/primary/api/api_handler

// APIHandler is a driving adapter that translates API requests
// into InPort calls. It's thin: parse, validate, delegate, respond.
TYPE APIHandler
    registerHandler RegisterAssetHandler
    getHandler      GetAssetHandler
    listHandler     ListAssetsByFacilityHandler
END TYPE

// Constructor creates the handler with InPort dependencies.
// Note: we depend on interfaces (InPorts), not concrete use cases.
CONSTRUCTOR NewAPIHandler(register RegisterAssetHandler, get GetAssetHandler, list ListAssetsByFacilityHandler)
    RETURNS APIHandler
    RETURN APIHandler{
        registerHandler: register,
        getHandler: get,
        listHandler: list
    }
END CONSTRUCTOR

// Handle routes API requests to appropriate handlers.
METHOD (h APIHandler) Handle(ctx Context, req Request) RETURNS (Response, Error)
    SWITCH
        CASE req.Method == "POST" AND req.Path == "/assets":
            RETURN h.handleRegister(ctx, req)
        CASE req.Method == "GET" AND req.PathParams["id"] != "":
            RETURN h.handleGet(ctx, req)
        CASE req.Method == "GET" AND req.QueryParams["facility_id"] != "":
            RETURN h.handleList(ctx, req)
        DEFAULT:
            RETURN JsonResponse(404, {error: "not found"})
    END SWITCH
END METHOD

// handleRegister translates POST /assets into RegisterAssetCommand.
METHOD (h APIHandler) handleRegister(ctx Context, req Request) RETURNS (Response, Error)
    // Parse request body (adapter responsibility: format translation)
    input := ParseJSON(req.Body) AS RegisterAssetRequest
    IF input == nil THEN
        RETURN JsonResponse(400, {error: "invalid JSON body"})
    END IF

    // Validate request at boundary
    IF err := input.Validate(); err != nil THEN
        RETURN JsonResponse(400, {error: err.Message})
    END IF

    // Translate to command and delegate to InPort
    result, err := h.registerHandler.Handle(ctx, RegisterAssetCommand{
        FacilityID:  input.FacilityID,
        Name:        input.Name,
        AssetType:   input.AssetType,
        CapacityKWh: input.CapacityKWh
    })
    IF err != nil THEN
        RETURN h.mapError(err)
    END IF

    // Translate result to response
    RETURN JsonResponse(201, RegisterAssetResponse{AssetID: result.AssetID})
END METHOD

// mapError translates domain errors to HTTP responses.
// This is adapter logic - mapping domain concepts to transport concerns.
METHOD (h APIHandler) mapError(err Error) RETURNS (Response, Error)
    SWITCH
        CASE IsError(err, ErrAssetNotFound):
            RETURN JsonResponse(404, {error: "asset not found"})
        CASE IsError(err, ErrAssetAlreadyExists):
            RETURN JsonResponse(409, {error: "asset already exists"})
        CASE IsError(err, ErrInvalidCapacity):
            RETURN JsonResponse(400, {error: err.Message})
        DEFAULT:
            // Log actual error, return generic message to client
            RETURN JsonResponse(500, {error: "internal server error"})
    END SWITCH
END METHOD
```

### Request/Response DTOs

```pseudocode
// adapters/primary/api/dto

// RegisterAssetRequest is the API request format.
// DTOs translate between external JSON and internal commands.
TYPE RegisterAssetRequest
    FacilityID  String
    Name        String
    AssetType   String
    CapacityKWh Float64
END TYPE

// Validate performs boundary validation before reaching domain.
METHOD (r RegisterAssetRequest) Validate() RETURNS Error
    IF r.FacilityID == "" THEN
        RETURN Error("facility_id is required")
    END IF
    IF r.Name == "" THEN
        RETURN Error("name is required")
    END IF
    IF r.AssetType == "" THEN
        RETURN Error("asset_type is required")
    END IF
    IF r.CapacityKWh <= 0 THEN
        RETURN Error("capacity_kwh must be positive")
    END IF
    RETURN nil
END METHOD

// RegisterAssetResponse is the API response format.
TYPE RegisterAssetResponse
    AssetID String
END TYPE
```

Driving adapters are thin: parse input, validate format, call InPort, translate result. No business logic lives here.

## Step 5: Implement Driven Adapters (Repository)

Driven adapters implement OutPorts. They translate between domain types and infrastructure formats.

```pseudocode
// adapters/secondary/database/asset_repository

// AssetRepository implements AssetRepository OutPort using a database.
// This is a driven adapter - it implements an OutPort interface.
TYPE DatabaseAssetRepository
    client    DatabaseClient
    tableName String
END TYPE

// Constructor creates the repository with database client.
// Infrastructure details (client, table name) are injected here, not in domain.
CONSTRUCTOR NewDatabaseAssetRepository(client DatabaseClient, tableName String)
    RETURNS DatabaseAssetRepository
    RETURN DatabaseAssetRepository{client: client, tableName: tableName}
END CONSTRUCTOR

// assetItem is the database storage representation.
// This is adapter-internal - domain doesn't know about it.
TYPE assetItem
    PK           String
    SK           String
    GSI1PK       String
    GSI1SK       String
    FacilityID   String
    Name         String
    AssetType    String
    CapacityKWh  Float64
    CurrentState String
    RegisteredAt String
    UpdatedAt    String
END TYPE

// Save persists the asset aggregate to the database.
METHOD (r DatabaseAssetRepository) Save(ctx Context, a Asset) RETURNS Error
    now := CurrentTimeUTC()

    item := assetItem{
        PK:           "ASSET#" + a.ID(),
        SK:           "METADATA",
        GSI1PK:       "FACILITY#" + a.FacilityID(),
        GSI1SK:       "ASSET#" + a.ID(),
        FacilityID:   a.FacilityID(),
        Name:         a.Name(),
        AssetType:    String(a.Type()),
        CapacityKWh:  a.Capacity().KWh(),
        CurrentState: String(a.State()),
        RegisteredAt: a.RegisteredAt().Format(RFC3339),
        UpdatedAt:    now.Format(RFC3339)
    }

    err := r.client.PutItem(ctx, r.tableName, item)
    IF err != nil THEN
        RETURN Error("failed to save asset: " + err)
    END IF

    RETURN nil
END METHOD

// FindByID retrieves an asset by its unique identifier.
METHOD (r DatabaseAssetRepository) FindByID(ctx Context, id String) RETURNS (Asset, Error)
    result := r.client.GetItem(ctx, r.tableName, {
        PK: "ASSET#" + id,
        SK: "METADATA"
    })
    IF result == nil THEN
        RETURN nil, ErrAssetNotFound
    END IF

    RETURN r.toDomain(result)
END METHOD

// FindByFacility retrieves all assets for a facility using GSI.
METHOD (r DatabaseAssetRepository) FindByFacility(ctx Context, facilityID String) RETURNS (List<Asset>, Error)
    results := r.client.Query(ctx, r.tableName, "GSI1", {
        GSI1PK: "FACILITY#" + facilityID
    })

    assets := []
    FOR EACH item IN results DO
        asset, err := r.toDomain(item)
        IF err != nil THEN
            RETURN nil, err
        END IF
        assets.Append(asset)
    END FOR

    RETURN assets, nil
END METHOD

// toDomain converts a database item to a domain aggregate.
// This is the adapter's core responsibility: format translation.
METHOD (r DatabaseAssetRepository) toDomain(item assetItem) RETURNS (Asset, Error)
    capacity, err := NewCapacity(item.CapacityKWh)
    IF err != nil THEN
        RETURN nil, Error("invalid stored capacity: " + err)
    END IF

    registeredAt := ParseTime(RFC3339, item.RegisteredAt)

    // Reconstitute aggregate from stored state
    RETURN ReconstructAsset(
        Substring(item.PK, 6),  // Remove "ASSET#" prefix
        item.FacilityID,
        item.Name,
        AssetType(item.AssetType),
        capacity,
        AssetState(item.CurrentState),
        registeredAt
    ), nil
END METHOD
```

Driven adapters handle: mapping between domain and infrastructure types, retries/backoff, authentication, serialization. Business logic stays in the domain.

## Step 6: Wire Dependencies and Test

Wire everything together in the application entry point and create tests that swap adapters.

### Application Entry Point

```pseudocode
// cmd/api/main

GLOBAL handler APIHandler

// init runs once at startup - wire up all dependencies here.
PROCEDURE init()
    ctx := Context.Background()

    // Load configuration
    config := LoadConfig()

    // Create infrastructure clients
    dbClient := NewDatabaseClient(config)
    eventClient := NewEventClient(config)

    // Read configuration from environment
    tableName := GetEnv("TABLE_NAME")
    eventBusName := GetEnv("EVENT_BUS_NAME")

    // Create driven adapters (OutPort implementations)
    repo := NewDatabaseAssetRepository(dbClient, tableName)
    publisher := NewEventPublisher(eventClient, eventBusName)

    // Create use cases (InPort implementations)
    registerUseCase := NewRegisterAssetUseCase(repo, publisher)
    getUseCase := NewGetAssetUseCase(repo)
    listUseCase := NewListAssetsByFacilityUseCase(repo)

    // Create driving adapter with InPort dependencies
    handler = NewAPIHandler(registerUseCase, getUseCase, listUseCase)
END PROCEDURE

PROCEDURE main()
    StartServer(handler.Handle)
END PROCEDURE
```

### Testing with Mock Adapters

```pseudocode
// core/application/usecases/register_asset_test

// InMemoryAssetRepository is a test double implementing AssetRepository.
TYPE InMemoryAssetRepository
    assets Map<String, Asset>
END TYPE

CONSTRUCTOR NewInMemoryAssetRepository() RETURNS InMemoryAssetRepository
    RETURN InMemoryAssetRepository{assets: NewMap()}
END CONSTRUCTOR

METHOD (r InMemoryAssetRepository) Save(ctx Context, a Asset) RETURNS Error
    r.assets.Set(a.ID(), a)
    RETURN nil
END METHOD

METHOD (r InMemoryAssetRepository) FindByID(ctx Context, id String) RETURNS (Asset, Error)
    IF r.assets.Has(id) THEN
        RETURN r.assets.Get(id), nil
    END IF
    RETURN nil, ErrAssetNotFound
END METHOD

METHOD (r InMemoryAssetRepository) FindByFacility(ctx Context, facilityID String) RETURNS (List<Asset>, Error)
    result := []
    FOR EACH asset IN r.assets.Values() DO
        IF asset.FacilityID() == facilityID THEN
            result.Append(asset)
        END IF
    END FOR
    RETURN result, nil
END METHOD

// SpyEventPublisher records published events for verification.
TYPE SpyEventPublisher
    PublishedEvents List<Event>
END TYPE

METHOD (s SpyEventPublisher) Publish(ctx Context, events List<Event>) RETURNS Error
    s.PublishedEvents.AppendAll(events)
    RETURN nil
END METHOD

TEST TestRegisterAsset_Success
    // Arrange: create test doubles for OutPorts
    repo := NewInMemoryAssetRepository()
    publisher := SpyEventPublisher{}

    // Create use case with test doubles
    useCase := NewRegisterAssetUseCase(repo, publisher)

    // Act
    result, err := useCase.Handle(Context.Background(), RegisterAssetCommand{
        FacilityID:  "facility-123",
        Name:        "Battery-1",
        AssetType:   "battery",
        CapacityKWh: 100.0
    })

    // Assert
    ASSERT err == nil
    ASSERT result.AssetID != ""

    // Verify side effects via test doubles
    ASSERT repo.assets.Size() == 1
    ASSERT publisher.PublishedEvents.Size() > 0
END TEST

TEST TestRegisterAsset_InvalidCapacity
    repo := NewInMemoryAssetRepository()
    publisher := SpyEventPublisher{}
    useCase := NewRegisterAssetUseCase(repo, publisher)

    _, err := useCase.Handle(Context.Background(), RegisterAssetCommand{
        FacilityID:  "facility-123",
        Name:        "Battery-1",
        AssetType:   "battery",
        CapacityKWh: -10.0  // Invalid: negative capacity
    })

    ASSERT err != nil
    ASSERT repo.assets.Size() == 0
END TEST
```

The hexagonal pattern enables testing use cases with in-memory repositories and spy publishers, without any infrastructure.

## Verification Checklist

After implementing hexagonal ports and adapters, verify:

- [ ] InPorts (Commands, Queries) are interfaces in `core/application/ports/inports/`
- [ ] OutPorts (Repositories, External Services) are interfaces in `core/application/ports/outports/`
- [ ] Ports are owned by the application layer, not by adapters
- [ ] Port interfaces use domain types, not infrastructure types
- [ ] Driving adapters (API, HTTP) depend on InPort interfaces
- [ ] Driven adapters (Database, EventBus) implement OutPort interfaces
- [ ] Adapters are thin: mapping, retries, auth, serialization only
- [ ] No business logic in adapters - all in domain layer
- [ ] Use cases orchestrate domain operations via OutPorts
- [ ] Dependencies injected via constructors, not created internally
- [ ] Tests use mock/stub adapters without infrastructure
- [ ] Same use case can be triggered by multiple driving adapters (REST, CLI, events)
