---
name: implement-cqrs-pattern
description: "Step-by-step guide for implementing CQRS pattern with separate read/write models, projections, and event-driven view updates."
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
context:
  - docs/architecture
  - docs/patterns
---

# Skill: Implement CQRS Pattern

This skill teaches you how to implement Command Query Responsibility Segregation (CQRS) following  architectural patterns. You'll learn to separate write and read models, build denormalized views via domain events, and create efficient query handlers for different use cases.

CQRS is essential when read patterns differ significantly from write patterns. In 's energy management domain, commands like `OptimizeBuildingHeating` modify state through aggregates (the source of truth), while queries like `GetBuildingDashboard` read from pre-computed, denormalized views optimized for specific use cases. This separation enables independent scaling, optimized data structures, and clear boundaries between mutation and retrieval operations.

## Prerequisites

- Understanding of Clean Architecture and DDD concepts (aggregates, domain events)
- Familiarity with event-driven architecture principles
- A domain with read patterns that differ from write patterns
- Database or data store for views

## Overview

In this skill, you will:
1. Define the command model (aggregates with domain events)
2. Define the query model (denormalized view structures)
3. Create projections that transform events into views
4. Implement command handlers that modify state through aggregates
5. Implement query handlers that read from optimized views
6. Wire the event stream to projections for real-time updates

## Step 1: Define the Command Model (Aggregates)

The command model is your source of truth. Commands modify state through aggregates that enforce invariants and emit domain events.

### Domain Events

```pseudocode
INTERFACE Event
    METHOD EventID() RETURNS String
    METHOD EventType() RETURNS String
    METHOD OccurredAt() RETURNS Timestamp
    METHOD AggregateID() RETURNS String
    METHOD SchemaVersion() RETURNS String
END INTERFACE

TYPE BaseEvent
    id: String
    type: String
    occurred: Timestamp
    aggregateId: String
    version: String

METHOD BaseEvent.EventID() RETURNS String
    RETURN this.id
END METHOD

METHOD BaseEvent.EventType() RETURNS String
    RETURN this.type
END METHOD

METHOD BaseEvent.OccurredAt() RETURNS Timestamp
    RETURN this.occurred
END METHOD

METHOD BaseEvent.AggregateID() RETURNS String
    RETURN this.aggregateId
END METHOD

METHOD BaseEvent.SchemaVersion() RETURNS String
    RETURN this.version
END METHOD

// HeatingOptimized is raised when heating is optimized for a building
TYPE HeatingOptimized EXTENDS BaseEvent
    buildingId: String
    buildingName: String
    outdoorTempCelsius: Float
    supplyTempCelsius: Float
    targetTempCelsius: Float
    energySavedKWh: Float
    optimizationType: String

CONSTRUCTOR NewHeatingOptimized(buildingId: String, name: String, outdoor: Float, supply: Float, target: Float, saved: Float, optType: String) RETURNS HeatingOptimized
    event = HeatingOptimized{
        BaseEvent: BaseEvent{
            id: GenerateUUID(),
            type: "heating.optimized",
            occurred: CurrentTimestamp(),
            aggregateId: buildingId,
            version: "1.0.0"
        },
        buildingId: buildingId,
        buildingName: name,
        outdoorTempCelsius: outdoor,
        supplyTempCelsius: supply,
        targetTempCelsius: target,
        energySavedKWh: saved,
        optimizationType: optType
    }
    RETURN event
END CONSTRUCTOR

// BuildingCreated is raised when a new heating building is registered
TYPE BuildingCreated EXTENDS BaseEvent
    name: String
    address: String
    zoneCount: Integer
    areaSqMeters: Float
```

Events are immutable facts that occurred. They contain all data needed by consumers and include schema versioning for evolution.

### Aggregate Root

```pseudocode
// HeatingBuilding is the aggregate root for heating optimization
// This is the WRITE model - the source of truth
TYPE HeatingBuilding
    id: String
    name: String
    address: String
    zoneCount: Integer
    areaSqMeters: Float
    currentSupplyCelsius: Float
    outdoorTempCelsius: Float
    totalEnergySaved: Float
    lastOptimized: Timestamp
    uncommittedEvents: List<Event>

CONSTRUCTOR NewHeatingBuilding(name: String, address: String, zoneCount: Integer, areaSqMeters: Float) RETURNS Result<HeatingBuilding, Error>
    IF name == "" THEN
        RETURN Error("building name is required")
    END IF
    IF zoneCount <= 0 THEN
        RETURN Error("zone count must be positive")
    END IF

    id = GenerateUUID()
    building = HeatingBuilding{
        id: id,
        name: name,
        address: address,
        zoneCount: zoneCount,
        areaSqMeters: areaSqMeters,
        uncommittedEvents: []
    }

    event = BuildingCreated{
        BaseEvent: BaseEvent{
            id: GenerateUUID(),
            type: "heating.building.created",
            occurred: CurrentTimestamp(),
            aggregateId: id,
            version: "1.0.0"
        },
        name: name,
        address: address,
        zoneCount: zoneCount,
        areaSqMeters: areaSqMeters
    }
    building.raise(event)

    RETURN Ok(building)
END CONSTRUCTOR

METHOD HeatingBuilding.ID() RETURNS String
    RETURN this.id
END METHOD

// Optimize performs heating optimization and raises an event
METHOD HeatingBuilding.Optimize(outdoorTempCelsius: Float, targetTempCelsius: Float) RETURNS Result<Void, Error>
    // Calculate optimal supply temperature based on outdoor conditions
    supplyTempCelsius = this.calculateSupplyTemp(outdoorTempCelsius, targetTempCelsius)

    // Calculate energy savings from optimization
    energySaved = this.calculateEnergySavings(this.currentSupplyCelsius, supplyTempCelsius)

    // Update aggregate state
    this.currentSupplyCelsius = supplyTempCelsius
    this.outdoorTempCelsius = outdoorTempCelsius
    this.totalEnergySaved = this.totalEnergySaved + energySaved
    this.lastOptimized = CurrentTimestamp()

    // Determine optimization type
    optType = "standard"
    IF outdoorTempCelsius < -10 THEN
        optType = "cold_weather"
    ELSE IF outdoorTempCelsius > 15 THEN
        optType = "mild_weather"
    END IF

    // Raise event for projections to consume
    event = NewHeatingOptimized(
        this.id, this.name,
        outdoorTempCelsius, supplyTempCelsius, targetTempCelsius,
        energySaved, optType
    )
    this.raise(event)

    RETURN Ok()
END METHOD

METHOD HeatingBuilding.calculateSupplyTemp(outdoor: Float, target: Float) RETURNS Float
    // Heat curve calculation: supply = target + factor * (target - outdoor)
    factor = 0.8
    RETURN target + factor * (target - outdoor)
END METHOD

METHOD HeatingBuilding.calculateEnergySavings(oldSupply: Float, newSupply: Float) RETURNS Float
    // Simplified savings calculation
    RETURN (oldSupply - newSupply) * this.areaSqMeters * 0.01
END METHOD

METHOD HeatingBuilding.raise(event: Event)
    this.uncommittedEvents.append(event)
END METHOD

METHOD HeatingBuilding.UncommittedEvents() RETURNS List<Event>
    RETURN this.uncommittedEvents
END METHOD

METHOD HeatingBuilding.ClearUncommittedEvents()
    this.uncommittedEvents = []
END METHOD
```

The aggregate enforces all business rules and emits events when state changes. This is the authoritative source of truth for write operations.

## Step 2: Define the Query Model (Denormalized Views)

Query models are optimized for reading. They're denormalized, pre-computed, and tailored for specific use cases.

```pseudocode
// BuildingDashboardView is optimized for UI dashboard display
// This is the READ model - denormalized for fast queries
TYPE BuildingDashboardView
    buildingId: String          // Primary key
    viewType: String            // Sort key, always "DASHBOARD"
    name: String
    address: String
    currentSupplyTempCelsius: Float
    currentOutdoorTempCelsius: Float
    totalEnergySavedKWh: Float
    optimizationCount: Integer
    lastOptimizedAt: Timestamp
    status: String              // "optimal", "suboptimal", "offline"
    updatedAt: Timestamp

// BuildingAnalyticsView is optimized for reporting and analytics
TYPE BuildingAnalyticsView
    buildingId: String          // Primary key
    viewType: String            // Sort key, "ANALYTICS#YYYY-MM"
    month: String
    totalOptimizations: Integer
    totalEnergySavedKWh: Float
    avgSupplyTempCelsius: Float
    coldWeatherCount: Integer
    mildWeatherCount: Integer
    standardCount: Integer
    costSavingsEstimate: Float
    updatedAt: Timestamp

// BuildingListView is optimized for listing all buildings
TYPE BuildingListView
    buildingId: String          // Primary key
    viewType: String            // Sort key, "LIST"
    name: String
    address: String
    zoneCount: Integer
    areaSqMeters: Float
    status: String
    createdAt: Timestamp
```

Each view is tailored for a specific query use case. Views are updated asynchronously by projections when events occur.

## Step 3: Create Projections (Event to View)

Projections listen to domain events and update the read models. They transform event data into optimized view structures.

```pseudocode
// ViewStore defines persistence operations for views
INTERFACE ViewStore
    METHOD SaveDashboardView(ctx: Context, view: BuildingDashboardView) RETURNS Result<Void, Error>
    METHOD GetDashboardView(ctx: Context, buildingId: String) RETURNS Result<BuildingDashboardView, Error>
    METHOD SaveAnalyticsView(ctx: Context, view: BuildingAnalyticsView) RETURNS Result<Void, Error>
    METHOD GetAnalyticsView(ctx: Context, buildingId: String, month: String) RETURNS Result<BuildingAnalyticsView, Error>
    METHOD SaveListView(ctx: Context, view: BuildingListView) RETURNS Result<Void, Error>
END INTERFACE

// BuildingDashboardProjection updates dashboard views from events
TYPE BuildingDashboardProjection
    store: ViewStore

CONSTRUCTOR NewBuildingDashboardProjection(store: ViewStore) RETURNS BuildingDashboardProjection
    RETURN BuildingDashboardProjection{store: store}
END CONSTRUCTOR

// Handle processes an event and updates the appropriate view
METHOD BuildingDashboardProjection.Handle(ctx: Context, event: Event) RETURNS Result<Void, Error>
    MATCH event TYPE
        CASE BuildingCreated:
            RETURN this.handleBuildingCreated(ctx, event)
        CASE HeatingOptimized:
            RETURN this.handleHeatingOptimized(ctx, event)
        DEFAULT:
            // Unknown event type - skip silently
            RETURN Ok()
    END MATCH
END METHOD

METHOD BuildingDashboardProjection.handleBuildingCreated(ctx: Context, e: BuildingCreated) RETURNS Result<Void, Error>
    // Create initial dashboard view
    dashboard = BuildingDashboardView{
        buildingId: e.AggregateID(),
        viewType: "DASHBOARD",
        name: e.name,
        address: e.address,
        status: "offline",
        updatedAt: CurrentTimestamp()
    }

    result = this.store.SaveDashboardView(ctx, dashboard)
    IF result.IsError() THEN
        RETURN Error("failed to save dashboard view: " + result.Error())
    END IF

    // Create list view entry
    listView = BuildingListView{
        buildingId: e.AggregateID(),
        viewType: "LIST",
        name: e.name,
        address: e.address,
        zoneCount: e.zoneCount,
        areaSqMeters: e.areaSqMeters,
        status: "offline",
        createdAt: e.OccurredAt()
    }

    RETURN this.store.SaveListView(ctx, listView)
END METHOD

METHOD BuildingDashboardProjection.handleHeatingOptimized(ctx: Context, e: HeatingOptimized) RETURNS Result<Void, Error>
    // Get existing view or create new one
    viewResult = this.store.GetDashboardView(ctx, e.buildingId)
    IF viewResult.IsError() THEN
        // Create new view if not found
        view = BuildingDashboardView{
            buildingId: e.buildingId,
            viewType: "DASHBOARD",
            name: e.buildingName
        }
    ELSE
        view = viewResult.Value()
    END IF

    // Update view with event data
    view.currentSupplyTempCelsius = e.supplyTempCelsius
    view.currentOutdoorTempCelsius = e.outdoorTempCelsius
    view.totalEnergySavedKWh = view.totalEnergySavedKWh + e.energySavedKWh
    view.optimizationCount = view.optimizationCount + 1
    view.lastOptimizedAt = e.OccurredAt()
    view.status = "optimal"
    view.updatedAt = CurrentTimestamp()

    RETURN this.store.SaveDashboardView(ctx, view)
END METHOD

// BuildingAnalyticsProjection updates analytics views from events
TYPE BuildingAnalyticsProjection
    store: ViewStore

CONSTRUCTOR NewBuildingAnalyticsProjection(store: ViewStore) RETURNS BuildingAnalyticsProjection
    RETURN BuildingAnalyticsProjection{store: store}
END CONSTRUCTOR

// Handle processes an event and updates analytics views
METHOD BuildingAnalyticsProjection.Handle(ctx: Context, event: Event) RETURNS Result<Void, Error>
    // Only handle HeatingOptimized events
    IF NOT (event IS HeatingOptimized) THEN
        RETURN Ok()
    END IF

    e = event AS HeatingOptimized
    month = FormatDate(e.OccurredAt(), "YYYY-MM")

    // Get existing analytics view for this month
    viewResult = this.store.GetAnalyticsView(ctx, e.buildingId, month)
    IF viewResult.IsError() THEN
        // Create new monthly analytics view
        view = BuildingAnalyticsView{
            buildingId: e.buildingId,
            viewType: "ANALYTICS#" + month,
            month: month
        }
    ELSE
        view = viewResult.Value()
    END IF

    // Update aggregated statistics
    view.totalOptimizations = view.totalOptimizations + 1
    view.totalEnergySavedKWh = view.totalEnergySavedKWh + e.energySavedKWh

    // Running average for supply temperature
    prevCount = view.totalOptimizations - 1
    view.avgSupplyTempCelsius = ((view.avgSupplyTempCelsius * prevCount) + e.supplyTempCelsius) / view.totalOptimizations

    // Count by optimization type
    MATCH e.optimizationType
        CASE "cold_weather":
            view.coldWeatherCount = view.coldWeatherCount + 1
        CASE "mild_weather":
            view.mildWeatherCount = view.mildWeatherCount + 1
        DEFAULT:
            view.standardCount = view.standardCount + 1
    END MATCH

    // Estimate cost savings (simplified: 0.15 per kWh)
    view.costSavingsEstimate = view.totalEnergySavedKWh * 0.15
    view.updatedAt = CurrentTimestamp()

    RETURN this.store.SaveAnalyticsView(ctx, view)
END METHOD
```

Projections are the bridge between write and read models. They transform events into denormalized views optimized for queries.

## Step 4: Implement Command Handlers

Command handlers orchestrate the write side. They load aggregates, execute commands, and persist changes.

```pseudocode
// BuildingRepository defines persistence for aggregates
INTERFACE BuildingRepository
    METHOD FindByID(ctx: Context, id: String) RETURNS Result<HeatingBuilding, Error>
    METHOD Save(ctx: Context, building: HeatingBuilding) RETURNS Result<Void, Error>
END INTERFACE

// EventPublisher publishes domain events
INTERFACE EventPublisher
    METHOD Publish(ctx: Context, events: List<Event>) RETURNS Result<Void, Error>
END INTERFACE

// OptimizeBuildingCommand is the input for optimization
TYPE OptimizeBuildingCommand
    buildingId: String
    outdoorTempCelsius: Float
    targetTempCelsius: Float

// OptimizeBuildingHandler handles the optimization command
TYPE OptimizeBuildingHandler
    repo: BuildingRepository
    publisher: EventPublisher

CONSTRUCTOR NewOptimizeBuildingHandler(repo: BuildingRepository, pub: EventPublisher) RETURNS OptimizeBuildingHandler
    RETURN OptimizeBuildingHandler{repo: repo, publisher: pub}
END CONSTRUCTOR

// Handle executes the optimization command
METHOD OptimizeBuildingHandler.Handle(ctx: Context, cmd: OptimizeBuildingCommand) RETURNS Result<Void, Error>
    // Load aggregate from repository
    buildingResult = this.repo.FindByID(ctx, cmd.buildingId)
    IF buildingResult.IsError() THEN
        RETURN Error("failed to find building: " + buildingResult.Error())
    END IF
    building = buildingResult.Value()

    // Execute command on aggregate (business logic lives here)
    optimizeResult = building.Optimize(cmd.outdoorTempCelsius, cmd.targetTempCelsius)
    IF optimizeResult.IsError() THEN
        RETURN Error("failed to optimize building: " + optimizeResult.Error())
    END IF

    // Persist aggregate changes
    saveResult = this.repo.Save(ctx, building)
    IF saveResult.IsError() THEN
        RETURN Error("failed to save building: " + saveResult.Error())
    END IF

    // Publish events for projections
    events = building.UncommittedEvents()
    IF events.Length() > 0 THEN
        publishResult = this.publisher.Publish(ctx, events)
        IF publishResult.IsError() THEN
            RETURN Error("failed to publish events: " + publishResult.Error())
        END IF
        building.ClearUncommittedEvents()
    END IF

    RETURN Ok()
END METHOD

// CreateBuildingCommand is the input for building creation
TYPE CreateBuildingCommand
    name: String
    address: String
    zoneCount: Integer
    areaSqMeters: Float

// CreateBuildingResult is the output of building creation
TYPE CreateBuildingResult
    buildingId: String

// CreateBuildingHandler handles building creation
TYPE CreateBuildingHandler
    repo: BuildingRepository
    publisher: EventPublisher

CONSTRUCTOR NewCreateBuildingHandler(repo: BuildingRepository, pub: EventPublisher) RETURNS CreateBuildingHandler
    RETURN CreateBuildingHandler{repo: repo, publisher: pub}
END CONSTRUCTOR

// Handle creates a new building
METHOD CreateBuildingHandler.Handle(ctx: Context, cmd: CreateBuildingCommand) RETURNS Result<CreateBuildingResult, Error>
    // Create aggregate (validates invariants)
    buildingResult = NewHeatingBuilding(cmd.name, cmd.address, cmd.zoneCount, cmd.areaSqMeters)
    IF buildingResult.IsError() THEN
        RETURN Error("failed to create building: " + buildingResult.Error())
    END IF
    building = buildingResult.Value()

    // Persist
    saveResult = this.repo.Save(ctx, building)
    IF saveResult.IsError() THEN
        RETURN Error("failed to save building: " + saveResult.Error())
    END IF

    // Publish creation event
    events = building.UncommittedEvents()
    IF events.Length() > 0 THEN
        publishResult = this.publisher.Publish(ctx, events)
        IF publishResult.IsError() THEN
            RETURN Error("failed to publish events: " + publishResult.Error())
        END IF
        building.ClearUncommittedEvents()
    END IF

    RETURN Ok(CreateBuildingResult{buildingId: building.ID()})
END METHOD
```

Command handlers coordinate the write path: load aggregate, execute business logic, persist, publish events.

## Step 5: Implement Query Handlers

Query handlers read from denormalized views. They never touch aggregates.

```pseudocode
// ViewReader defines read operations for views
INTERFACE ViewReader
    METHOD GetDashboardView(ctx: Context, buildingId: String) RETURNS Result<BuildingDashboardView, Error>
    METHOD GetAnalyticsView(ctx: Context, buildingId: String, month: String) RETURNS Result<BuildingAnalyticsView, Error>
    METHOD ListBuildings(ctx: Context, limit: Integer, cursor: String) RETURNS Result<Tuple<List<BuildingListView>, String>, Error>
END INTERFACE

// GetBuildingDashboardQuery is the input for dashboard retrieval
TYPE GetBuildingDashboardQuery
    buildingId: String

// GetBuildingDashboardHandler handles dashboard queries
TYPE GetBuildingDashboardHandler
    reader: ViewReader

CONSTRUCTOR NewGetBuildingDashboardHandler(reader: ViewReader) RETURNS GetBuildingDashboardHandler
    RETURN GetBuildingDashboardHandler{reader: reader}
END CONSTRUCTOR

// Handle retrieves a building dashboard view
METHOD GetBuildingDashboardHandler.Handle(ctx: Context, q: GetBuildingDashboardQuery) RETURNS Result<BuildingDashboardView, Error>
    viewResult = this.reader.GetDashboardView(ctx, q.buildingId)
    IF viewResult.IsError() THEN
        RETURN Error("failed to get dashboard view: " + viewResult.Error())
    END IF
    RETURN Ok(viewResult.Value())
END METHOD

// GetBuildingAnalyticsQuery is the input for analytics retrieval
TYPE GetBuildingAnalyticsQuery
    buildingId: String
    month: String           // Format: "2024-01"

// GetBuildingAnalyticsHandler handles analytics queries
TYPE GetBuildingAnalyticsHandler
    reader: ViewReader

CONSTRUCTOR NewGetBuildingAnalyticsHandler(reader: ViewReader) RETURNS GetBuildingAnalyticsHandler
    RETURN GetBuildingAnalyticsHandler{reader: reader}
END CONSTRUCTOR

// Handle retrieves building analytics for a specific month
METHOD GetBuildingAnalyticsHandler.Handle(ctx: Context, q: GetBuildingAnalyticsQuery) RETURNS Result<BuildingAnalyticsView, Error>
    viewResult = this.reader.GetAnalyticsView(ctx, q.buildingId, q.month)
    IF viewResult.IsError() THEN
        RETURN Error("failed to get analytics view: " + viewResult.Error())
    END IF
    RETURN Ok(viewResult.Value())
END METHOD

// ListBuildingsQuery is the input for listing buildings
TYPE ListBuildingsQuery
    limit: Integer
    cursor: String

// ListBuildingsResult is the output of listing buildings
TYPE ListBuildingsResult
    buildings: List<BuildingListView>
    nextCursor: String

// ListBuildingsHandler handles building list queries
TYPE ListBuildingsHandler
    reader: ViewReader

CONSTRUCTOR NewListBuildingsHandler(reader: ViewReader) RETURNS ListBuildingsHandler
    RETURN ListBuildingsHandler{reader: reader}
END CONSTRUCTOR

// Handle lists buildings with pagination
METHOD ListBuildingsHandler.Handle(ctx: Context, q: ListBuildingsQuery) RETURNS Result<ListBuildingsResult, Error>
    limit = q.limit
    IF limit <= 0 OR limit > 100 THEN
        limit = 20
    END IF

    result = this.reader.ListBuildings(ctx, limit, q.cursor)
    IF result.IsError() THEN
        RETURN Error("failed to list buildings: " + result.Error())
    END IF

    buildings, nextCursor = result.Value()

    RETURN Ok(ListBuildingsResult{
        buildings: buildings,
        nextCursor: nextCursor
    })
END METHOD
```

Query handlers are simple and fast. They read directly from pre-computed views without touching the write model.

## Step 6: Wire Event Stream to Projections

Connect the event publisher to projections so views update automatically when events occur.

```pseudocode
// Projection handles domain events
INTERFACE Projection
    METHOD Handle(ctx: Context, event: Event) RETURNS Result<Void, Error>
END INTERFACE

// EventProcessor routes events to projections
TYPE EventProcessor
    projections: List<Projection>
    logger: Logger

CONSTRUCTOR NewEventProcessor(projections: List<Projection>) RETURNS EventProcessor
    RETURN EventProcessor{
        projections: projections,
        logger: DefaultLogger()
    }
END CONSTRUCTOR

// ProcessEvent handles events from the event bus
METHOD EventProcessor.ProcessEvent(ctx: Context, eventType: String, payload: RawData) RETURNS Result<Void, Error>
    // Parse event type and deserialize
    eventResult = this.deserializeEvent(eventType, payload)
    IF eventResult.IsError() THEN
        RETURN Error("failed to deserialize event: " + eventResult.Error())
    END IF
    event = eventResult.Value()

    // Route to all projections
    FOR EACH proj IN this.projections DO
        result = proj.Handle(ctx, event)
        IF result.IsError() THEN
            this.logger.Error("projection failed",
                "event_type", eventType,
                "event_id", event.EventID(),
                "error", result.Error()
            )
            // Continue processing other projections
        END IF
    END FOR

    RETURN Ok()
END METHOD

METHOD EventProcessor.deserializeEvent(eventType: String, payload: RawData) RETURNS Result<Event, Error>
    MATCH eventType
        CASE "heating.optimized":
            RETURN DeserializeJSON<HeatingOptimized>(payload)
        CASE "heating.building.created":
            RETURN DeserializeJSON<BuildingCreated>(payload)
        DEFAULT:
            RETURN Error("unknown event type: " + eventType)
    END MATCH
END METHOD

// ProjectionHandler is the entry point for projection updates
TYPE ProjectionHandler
    processor: EventProcessor

CONSTRUCTOR NewProjectionHandler(processor: EventProcessor) RETURNS ProjectionHandler
    RETURN ProjectionHandler{processor: processor}
END CONSTRUCTOR

// Handle processes events from the event bus
METHOD ProjectionHandler.Handle(ctx: Context, eventType: String, payload: RawData) RETURNS Result<Void, Error>
    RETURN this.processor.ProcessEvent(ctx, eventType, payload)
END METHOD
```

### Application Bootstrap

```pseudocode
// Bootstrap wires up all projections and handlers
FUNCTION Bootstrap() RETURNS ProjectionHandler
    // Create data store client
    dataClient = CreateDataStoreClient()
    viewTableName = GetEnvironmentVariable("VIEW_TABLE_NAME")

    // Create view store
    viewStore = NewViewStore(dataClient, viewTableName)

    // Create projections
    dashboardProj = NewBuildingDashboardProjection(viewStore)
    analyticsProj = NewBuildingAnalyticsProjection(viewStore)

    // Create event processor with all projections
    processor = NewEventProcessor([dashboardProj, analyticsProj])

    RETURN NewProjectionHandler(processor)
END FUNCTION
```

The event processor routes events to all registered projections. Each projection updates its specific view independently.

## Verification Checklist

After implementing CQRS, verify:

- [ ] Commands modify state only through aggregates (source of truth)
- [ ] Aggregates emit domain events on state changes
- [ ] Query views are denormalized and optimized for specific use cases
- [ ] Query handlers never touch aggregates directly
- [ ] Projections update views asynchronously from events
- [ ] Each view has clear ownership and purpose
- [ ] Views can be rebuilt by replaying events
- [ ] Event schema includes version for future evolution
- [ ] Command handlers validate input before touching aggregates
- [ ] Query handlers support pagination for list operations
- [ ] Projection failures are logged but don't block event processing
- [ ] Views have appropriate keys for access patterns
