---
name: implement-ddd-aggregate
description: "Step-by-step guide for implementing DDD aggregates following  patterns with Clean Architecture."
allowed-tools: Read, Grep, Glob, Write, Edit
metadata:
  type: implementation
---

# Skill: Implement DDD Aggregate

This skill teaches you how to implement Domain-Driven Design aggregates following  architectural patterns. You will learn to create aggregates that enforce invariants, emit domain events, and integrate cleanly with Clean Architecture principles.

Aggregates are the cornerstone of DDD tactical patterns. They define consistency boundaries, enforce business rules at the domain level, and ensure your domain model remains valid at all times. By following this skill, you will create robust domain models that protect business invariants and emit meaningful events.

## Prerequisites

- Understanding of Clean Architecture principles (dependency inversion, layering)
- Familiarity with DDD concepts (entities, value objects, aggregates, bounded contexts)
- Knowledge of the Aggregate Root Pattern and consistency boundaries
- A domain problem identified with clear business rules to model
- Understanding of domain event patterns and eventual consistency

## Overview

In this skill, you will create a complete aggregate implementation by:
1. Defining value objects with validation rules
2. Creating immutable domain events as facts
3. Defining domain-specific error types
4. Implementing the aggregate root with invariant enforcement
5. Defining the repository port as an interface
6. Creating a use case that orchestrates the aggregate

By the end, you will have a complete domain model that enforces business rules, tracks state changes through events, and integrates with Clean Architecture layers.

## Step 1: Define Value Objects

Value objects are immutable, identified by their attributes rather than identity, and encapsulate validation logic. Create them first as validated building blocks for your aggregate.

### Temperature Value Object

```pseudocode
// Pattern: Value Object with validation in constructor
// Location: Domain layer (no dependencies)

TYPE Temperature
  PRIVATE celsius: Number

CONSTRUCTOR NewTemperature(celsius: Number) -> Result<Temperature, Error>
  // Enforce valid range invariant at construction
  VALIDATE celsius >= -50 AND celsius <= 150
  IF invalid THEN
    RETURN Error("temperature must be between -50 and 150 Celsius")
  END IF

  RETURN Temperature { celsius: celsius }
END CONSTRUCTOR

// Factory for tests or known-valid values
CONSTRUCTOR MustTemperature(celsius: Number) -> Temperature
  result = NewTemperature(celsius)
  IF result is Error THEN
    PANIC with error message
  END IF
  RETURN result value
END CONSTRUCTOR

METHOD Celsius() -> Number
  RETURN this.celsius
END METHOD

METHOD Equals(other: Temperature) -> Boolean
  RETURN this.celsius == other.celsius
END METHOD
```

Value objects validate on construction. If `NewTemperature` succeeds, the value is guaranteed valid. This eliminates defensive validation throughout your codebase.

### HeatCurve Value Object

```pseudocode
// Pattern: Complex value object with business calculation
// Business Rule: Heat curve defines supply temperature based on outdoor conditions

TYPE HeatCurve
  PRIVATE slope: Number
  PRIVATE parallelShift: Number
  PRIVATE minSupply: Temperature
  PRIVATE maxSupply: Temperature

CONSTRUCTOR NewHeatCurve(
  slope: Number,
  parallelShift: Number,
  minSupply: Temperature,
  maxSupply: Temperature
) -> Result<HeatCurve, Error>

  // Validate slope range
  VALIDATE slope >= 0.1 AND slope <= 3.0
  IF invalid THEN
    RETURN Error("slope must be between 0.1 and 3.0")
  END IF

  // Validate parallel shift range
  VALIDATE parallelShift >= -10 AND parallelShift <= 10
  IF invalid THEN
    RETURN Error("parallel shift must be between -10 and 10")
  END IF

  RETURN HeatCurve {
    slope: slope,
    parallelShift: parallelShift,
    minSupply: minSupply,
    maxSupply: maxSupply
  }
END CONSTRUCTOR

METHOD CalculateSupplyTemp(outdoor: Temperature) -> Temperature
  // Business logic: Heat curve formula
  // supply = 20 + slope * (20 - outdoor) + parallelShift
  supply = 20 + this.slope * (20 - outdoor.Celsius()) + this.parallelShift

  // Apply min/max constraints (clamping)
  IF supply < this.minSupply.Celsius() THEN
    RETURN this.minSupply
  END IF

  IF supply > this.maxSupply.Celsius() THEN
    RETURN this.maxSupply
  END IF

  // Return validated temperature (safe because clamped to valid range)
  RETURN MustTemperature(supply)
END METHOD
```

Key patterns:
- Validation concentrated in constructors
- Business calculations encapsulated in methods
- Immutability: no setters, only creation and computation
- Type safety: returns Temperature, not raw number

## Step 2: Define Domain Events

Domain events represent immutable facts that occurred in the domain. They are past-tense, contain all necessary data, and enable eventual consistency across bounded contexts.

```pseudocode
// Pattern: Domain Event as immutable fact
// Location: Domain layer
// Purpose: Communicate state changes to other aggregates and bounded contexts

INTERFACE Event
  METHOD EventID() -> String
  METHOD EventType() -> String
  METHOD OccurredAt() -> Timestamp
  METHOD AggregateID() -> String
  METHOD SchemaVersion() -> String  // Semantic versioning for evolution
END INTERFACE

// Base implementation with common fields
TYPE BaseEvent
  PUBLIC id: String
  PUBLIC type: String
  PUBLIC occurredAt: Timestamp
  PUBLIC aggregateID: String
  PUBLIC schemaVersion: String

// Event: Heating building was registered in the system
TYPE HeatingBuildingCreated IMPLEMENTS Event
  INHERITS BaseEvent
  PUBLIC name: String
  PUBLIC address: String
  PUBLIC heatCurveSlope: Number
  PUBLIC heatCurveParallelShift: Number

CONSTRUCTOR NewHeatingBuildingCreated(
  buildingID: String,
  name: String,
  address: String,
  curve: HeatCurve
) -> HeatingBuildingCreated

  RETURN HeatingBuildingCreated {
    BaseEvent: {
      id: GenerateUUID(),
      type: "heating.building.created",
      occurredAt: CurrentUTCTime(),
      aggregateID: buildingID,
      schemaVersion: "1.0.0"
    },
    name: name,
    address: address,
    heatCurveSlope: curve.slope,
    heatCurveParallelShift: curve.parallelShift
  }
END CONSTRUCTOR

// Event: Supply temperature was adjusted based on conditions
TYPE SupplyTemperatureAdjusted IMPLEMENTS Event
  INHERITS BaseEvent
  PUBLIC previousTempCelsius: Number
  PUBLIC newTempCelsius: Number
  PUBLIC reason: String

CONSTRUCTOR NewSupplyTemperatureAdjusted(
  buildingID: String,
  previousTemp: Temperature,
  newTemp: Temperature,
  reason: String
) -> SupplyTemperatureAdjusted

  RETURN SupplyTemperatureAdjusted {
    BaseEvent: {
      id: GenerateUUID(),
      type: "heating.supply_temperature.adjusted",
      occurredAt: CurrentUTCTime(),
      aggregateID: buildingID,
      schemaVersion: "1.0.0"
    },
    previousTempCelsius: previousTemp.Celsius(),
    newTempCelsius: newTemp.Celsius(),
    reason: reason
  }
END CONSTRUCTOR
```

Event design principles:
- **Unique ID**: Each event has a globally unique identifier
- **Type**: Namespaced string for routing and filtering
- **Timestamp**: When the fact occurred (UTC)
- **Aggregate ID**: Which aggregate emitted this event
- **Schema Version**: Enables event schema evolution
- **Past tense**: "Created", "Adjusted", not "Create", "Adjust"
- **Complete data**: Contains all information consumers need

## Step 3: Define Domain Errors

Domain errors represent business rule violations. They express domain concepts, not technical failures.

```pseudocode
// Pattern: Domain-specific error types
// Location: Domain layer
// Purpose: Express business rule violations in domain language

ERROR ErrBuildingNotFound
  MESSAGE "heating building not found"

ERROR ErrBuildingAlreadyExists
  MESSAGE "heating building already exists"

ERROR ErrSupplyTempOutOfRange
  MESSAGE "supply temperature outside heat curve range"

ERROR ErrInvalidBuildingState
  MESSAGE "operation not allowed in current building state"

ERROR ErrInvalidTemperature
  MESSAGE "temperature must be between -50 and 150 Celsius"

ERROR ErrInvalidSlope
  MESSAGE "slope must be between 0.1 and 3.0"

ERROR ErrInvalidParallelShift
  MESSAGE "parallel shift must be between -10 and 10"
```

Domain errors enable:
- Clear business rule communication
- Appropriate adapter responses (HTTP 404 for NotFound, 409 for AlreadyExists)
- Testable failure scenarios
- Separation from infrastructure errors (network, database)

## Step 4: Implement the Aggregate Root

The aggregate root is the entry point to the aggregate. It enforces all invariants, controls access to child entities, and raises domain events when state changes.

```pseudocode
// Pattern: Aggregate Root with invariant enforcement
// Location: Domain layer
// Responsibility: Consistency boundary, business rule enforcement, event emission

TYPE HeatingBuilding
  // Identity
  PRIVATE id: String

  // Attributes
  PRIVATE name: String
  PRIVATE address: String
  PRIVATE heatCurve: HeatCurve
  PRIVATE currentSupplyTemp: Temperature
  PRIVATE outdoorTemp: Temperature
  PRIVATE state: BuildingState
  PRIVATE lastUpdated: Timestamp

  // Uncommitted events (not yet persisted)
  PRIVATE uncommittedEvents: List<Event>

ENUM BuildingState
  ACTIVE
  INACTIVE
  FAULT
END ENUM

// Constructor: Only way to create valid aggregate
CONSTRUCTOR NewHeatingBuilding(
  name: String,
  address: String,
  curve: HeatCurve
) -> Result<HeatingBuilding, Error>

  // Enforce creation invariants
  VALIDATE name is not empty
  IF invalid THEN
    RETURN Error("building name is required")
  END IF

  VALIDATE address is not empty
  IF invalid THEN
    RETURN Error("building address is required")
  END IF

  // Generate identity
  id = GenerateUUID()
  now = CurrentUTCTime()

  // Calculate initial supply (assume 5°C outdoor as default)
  outdoorTemp = MustTemperature(5.0)
  initialSupply = curve.CalculateSupplyTemp(outdoorTemp)

  // Create aggregate instance
  building = HeatingBuilding {
    id: id,
    name: name,
    address: address,
    heatCurve: curve,
    currentSupplyTemp: initialSupply,
    outdoorTemp: outdoorTemp,
    state: BuildingState.ACTIVE,
    lastUpdated: now,
    uncommittedEvents: EmptyList()
  }

  // Raise creation event
  building.Raise(NewHeatingBuildingCreated(id, name, address, curve))

  RETURN building
END CONSTRUCTOR

// Read-only accessors (no setters - enforce controlled mutation)
METHOD ID() -> String
  RETURN this.id
END METHOD

METHOD Name() -> String
  RETURN this.name
END METHOD

METHOD CurrentSupplyTemp() -> Temperature
  RETURN this.currentSupplyTemp
END METHOD

METHOD State() -> BuildingState
  RETURN this.state
END METHOD

// Business operation: Adjust supply temperature based on outdoor conditions
// Invariant: Temperature must follow heat curve
// Invariant: Cannot adjust if building is in fault state
METHOD AdjustSupplyTemperature(
  outdoor: Temperature,
  reason: String
) -> Result<Void, Error>

  // Enforce state invariant
  IF this.state == BuildingState.FAULT THEN
    RETURN Error(ErrInvalidBuildingState, "building in fault state")
  END IF

  // Calculate new supply temperature using heat curve
  newSupply = this.heatCurve.CalculateSupplyTemp(outdoor)

  // Only update and emit event if temperature actually changed
  IF NOT newSupply.Equals(this.currentSupplyTemp) THEN
    previousSupply = this.currentSupplyTemp

    // Update state
    this.currentSupplyTemp = newSupply
    this.outdoorTemp = outdoor
    this.lastUpdated = CurrentUTCTime()

    // Raise domain event
    this.Raise(NewSupplyTemperatureAdjusted(
      this.id,
      previousSupply,
      newSupply,
      reason
    ))
  END IF

  RETURN Success()
END METHOD

// Business operation: Mark building as faulted
METHOD SetFaultState(reason: String) -> Void
  this.state = BuildingState.FAULT
  this.lastUpdated = CurrentUTCTime()
  // Could raise BuildingFaulted event here
END METHOD

// Internal: Add event to uncommitted list
PRIVATE METHOD Raise(event: Event) -> Void
  this.uncommittedEvents.Append(event)
END METHOD

// Repository pattern: Retrieve uncommitted events for persistence
METHOD UncommittedEvents() -> List<Event>
  RETURN this.uncommittedEvents
END METHOD

// Repository pattern: Clear events after persistence
METHOD ClearUncommittedEvents() -> Void
  this.uncommittedEvents = EmptyList()
END METHOD
```

Aggregate root patterns:
- **Single entry point**: All operations go through the root
- **Constructor enforcement**: Only way to create valid instances
- **Invariant protection**: Business rules checked before state changes
- **Event emission**: Events raised from within aggregate methods
- **Encapsulation**: Private fields, controlled access through methods
- **Consistency boundary**: All changes happen transactionally within the aggregate

## Step 5: Define the Repository Port

The repository port defines the interface for aggregate persistence. It lives in the domain or application layer as a contract that adapters implement.

```pseudocode
// Pattern: Repository port (interface)
// Location: Domain or application layer
// Implementations: Live in adapters layer (DynamoDB, PostgreSQL, in-memory)

INTERFACE BuildingRepository

  // Persist aggregate and publish events
  // Business rule: Save is transactional (aggregate + events)
  METHOD Save(context: Context, building: HeatingBuilding) -> Result<Void, Error>

  // Retrieve aggregate by identity
  // Returns: ErrBuildingNotFound if not found
  METHOD FindByID(context: Context, id: String) -> Result<HeatingBuilding, Error>

  // Query all buildings
  METHOD FindAll(context: Context) -> Result<List<HeatingBuilding>, Error>

  // Query buildings by state
  METHOD FindByState(
    context: Context,
    state: BuildingState
  ) -> Result<List<HeatingBuilding>, Error>
END INTERFACE
```

Repository responsibilities:
- **Persistence abstraction**: Hide storage details from domain
- **Aggregate lifecycle**: Load, save, delete complete aggregates
- **Event publishing**: Typically handled in Save implementation
- **Transactionality**: Ensure aggregate and events saved together
- **Query interface**: Find by identity and simple criteria

Adapter implementations (not shown in pseudocode):
- DynamoDB adapter: Uses single-table design, PK/SK patterns
- PostgreSQL adapter: Maps to relational tables
- In-memory adapter: For testing, uses map/dictionary

## Step 6: Implement a Use Case

Use cases orchestrate domain operations without containing business logic themselves. They coordinate aggregates, repositories, and external services.

```pseudocode
// Pattern: Application service (use case)
// Location: Application layer
// Purpose: Orchestration, transaction boundaries, cross-cutting concerns

TYPE AdjustTemperatureCommand
  PUBLIC buildingID: String
  PUBLIC outdoorTempCelsius: Number
  PUBLIC reason: String

TYPE AdjustTemperatureResult
  PUBLIC buildingID: String
  PUBLIC newSupplyTempCelsius: Number

// Use case: Adjust building supply temperature based on outdoor conditions
TYPE AdjustTemperatureUseCase
  PRIVATE repository: BuildingRepository

CONSTRUCTOR NewAdjustTemperatureUseCase(
  repo: BuildingRepository
) -> AdjustTemperatureUseCase
  RETURN AdjustTemperatureUseCase {
    repository: repo
  }
END CONSTRUCTOR

METHOD Execute(
  context: Context,
  command: AdjustTemperatureCommand
) -> Result<AdjustTemperatureResult, Error>

  // Step 1: Validate input and create value object
  outdoorTemp = NewTemperature(command.outdoorTempCelsius)
  IF outdoorTemp is Error THEN
    RETURN Error("invalid outdoor temperature: " + outdoorTemp.message)
  END IF

  // Step 2: Load aggregate from repository
  buildingResult = this.repository.FindByID(context, command.buildingID)
  IF buildingResult is Error THEN
    RETURN Error("failed to find building: " + buildingResult.message)
  END IF
  building = buildingResult.value

  // Step 3: Execute domain operation (business logic in aggregate)
  adjustResult = building.AdjustSupplyTemperature(outdoorTemp, command.reason)
  IF adjustResult is Error THEN
    RETURN Error("failed to adjust temperature: " + adjustResult.message)
  END IF

  // Step 4: Persist aggregate (repository also publishes events)
  saveResult = this.repository.Save(context, building)
  IF saveResult is Error THEN
    RETURN Error("failed to save building: " + saveResult.message)
  END IF

  // Step 5: Return result
  RETURN AdjustTemperatureResult {
    buildingID: building.ID(),
    newSupplyTempCelsius: building.CurrentSupplyTemp().Celsius()
  }
END METHOD
```

Use case patterns:
- **Command objects**: Encapsulate input parameters
- **Result objects**: Encapsulate output data
- **Load-Execute-Save**: Standard workflow pattern
- **Error propagation**: Wrap errors with context
- **No business logic**: Orchestration only, logic stays in domain
- **Transaction boundary**: Use case defines the unit of work

Integration with Clean Architecture:
- **Use case** depends on repository **interface** (defined in domain/application)
- **Adapter** implements repository **interface** (in adapters layer)
- **Controller** creates command, calls use case, maps result (in presentation layer)

Example flow:
```
HTTP Request
  -> Controller (adapters/primary/http)
  -> Create Command object
  -> Call UseCase.Execute()
    -> Load Aggregate via Repository port
    -> Call Aggregate method (business logic)
    -> Save Aggregate via Repository port
      -> Adapter persists to database
      -> Adapter publishes events to message bus
  -> Map Result to HTTP Response
  -> HTTP Response
```

## Verification Checklist

After implementing your aggregate, verify these patterns:

- [ ] Value objects are immutable with validation in constructor
- [ ] Value objects have no public setters, only getters
- [ ] Domain events are past-tense facts with complete data
- [ ] Events include ID, type, timestamp, aggregate ID, schema version
- [ ] Aggregate root enforces all business invariants
- [ ] No way to create aggregate in invalid state
- [ ] All state changes go through aggregate methods
- [ ] Events raised from within aggregate methods, not externally
- [ ] Repository port defined as interface in domain/application layer
- [ ] Use case orchestrates but contains no business logic
- [ ] Domain layer has no infrastructure dependencies
- [ ] All domain errors are explicitly defined with clear names
- [ ] Tests can be written without infrastructure dependencies
- [ ] Aggregate can be reconstituted from events (if using event sourcing)
- [ ] Clear ubiquitous language used in all naming (matches domain expert vocabulary)
- [ ] Aggregate boundaries aligned with transactional consistency requirements
- [ ] Events enable eventual consistency across aggregate boundaries
