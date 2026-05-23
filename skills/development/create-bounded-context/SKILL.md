---
name: create-bounded-context
description: "Step-by-step guide for creating DDD Bounded Contexts with ubiquitous language, context maps, and cross-context communication."
allowed-tools: Read, Grep, Glob, Write, Edit
metadata:
  type: implementation
  patterns: ["DDD", "Bounded Contexts"]
---

# Skill: Create Bounded Context

This skill teaches you how to design and implement a DDD Bounded Context following  architectural patterns. You'll learn to identify business capabilities, define ubiquitous language, map context relationships, and establish clear boundaries with proper cross-context communication.

A Bounded Context is an explicit boundary within which a domain model is defined and applicable. In , each Bounded Context is implemented as one microservice. The same word can mean different things in different contexts - "Asset" in the Asset Context differs from "Asset" in the Billing Context. This isolation enables teams to evolve independently while maintaining clear contracts.

Understanding Bounded Contexts is fundamental to DDD. They prevent the "big ball of mud" by ensuring each context owns its data, speaks its language, and communicates through explicit contracts.

## Prerequisites

- Understanding of DDD strategic patterns (contexts, subdomains, context maps)
- Familiarity with Clean Architecture and Hexagonal Architecture principles
- A business capability to model (we'll use Facility Context as example)
- Understanding of domain events and eventual consistency

## Overview

In this skill, you will:
1. Identify the business capability and subdomain
2. Define the ubiquitous language glossary
3. Create a context map with relationships
4. Define aggregates within the context
5. Design ports for cross-context communication
6. Document context boundaries and contracts
7. Implement the context structure

## Step 1: Identify the Business Capability

Before writing code, clearly define what business capability this context owns. A Bounded Context should have clear ownership of data and behavior.

### Capability Analysis Template

Use this template to analyze your business capability:

```text
Context Name: Facility Context

Business Capability:
  - Manages physical facility definitions and topology
  - Owns facility hierarchy (building -> zones -> points)
  - Maintains facility metadata and configuration

Data Ownership (Source of Truth):
  - Facility entity (id, name, address, type)
  - Zone entity (id, facilityId, name, purpose)
  - Topology relationships (parent-child, adjacency)

NOT Owned (References Only):
  - Assets (owned by Asset Context, referenced by ID)
  - Optimization schedules (owned by Braiin Context)
  - Billing information (owned by Billing Context)

Change Drivers:
  - Adding new facility types
  - Topology structure changes
  - Metadata schema evolution

Team Ownership:
  - Platform Team (Facility subdomain)
```

### Splitting Criteria

A capability should be its own Bounded Context when:

```pseudocode
// criteria/split_decision

// SplitCriteria helps decide if a capability warrants its own context.
TYPE SplitCriteria
    // HasOwnLanguage indicates the capability has distinct terminology.
    // Example: "Zone" means physical area in Facility, but "Zone" might mean
    // pricing zone in Billing. Different meanings = different contexts.
    HasOwnLanguage Boolean

    // ChangesIndependently indicates different change rates or drivers.
    // Example: Facility topology changes rarely; Asset telemetry changes constantly.
    ChangesIndependently Boolean

    // OwnsData indicates the capability is the source of truth for some data.
    // Example: Facility Context owns facility definitions. Asset Context owns assets.
    OwnsData Boolean

    // CanTestInIsolation indicates the capability can be tested without others.
    // Example: Facility CRUD doesn't require Asset or Billing to test.
    CanTestInIsolation Boolean
END TYPE

// ShouldSplit returns true if the capability warrants its own Bounded Context.
METHOD (c SplitCriteria) ShouldSplit() RETURNS Boolean
    // All four criteria should be true for a clear split
    RETURN c.HasOwnLanguage AND c.ChangesIndependently AND c.OwnsData AND c.CanTestInIsolation
END METHOD
```

Avoid splitting if the capability is just data transformation (that's an adapter, not a context) or if it shares the same language and data ownership as an existing context.

## Step 2: Define Ubiquitous Language Glossary

The Ubiquitous Language is the shared vocabulary between developers and domain experts within the context. Document it explicitly.

### Glossary Structure

```pseudocode
// docs/glossary

// FacilityContextGlossary defines the Ubiquitous Language for the Facility Context.
// Every term here has a precise meaning within this context ONLY.
// The same word may mean something different in another context.

/*
FACILITY CONTEXT GLOSSARY

Facility
  Definition: A physical location where energy assets are installed and managed.
  Examples: Office building, residential complex, industrial plant, data center.
  NOT: A billing account or a user organization.

Zone
  Definition: A logical subdivision of a facility for management purposes.
  Examples: Floor, wing, HVAC zone, electrical panel zone.
  Invariant: A zone belongs to exactly one facility.
  NOT: A pricing zone or a geographic region.

Topology
  Definition: The hierarchical and spatial relationships between facility components.
  Examples: Building contains floors, floors contain zones, zones contain measurement points.
  Invariant: Topology forms a tree (no cycles).

Point
  Definition: A specific measurement or control location within a zone.
  Examples: Temperature sensor, power meter, HVAC setpoint.
  NOT: A time series data point (that's telemetry, owned by Asset Context).

Commissioning
  Definition: The process of bringing a new facility online in the system.
  Invariant: A facility must be commissioned before assets can be registered.

Decommissioning
  Definition: The process of retiring a facility from active management.
  Invariant: All assets must be removed before decommissioning.
*/
```

### Cross-Context Term Mapping

When the same word has different meanings across contexts, document the mapping:

```pseudocode
// docs/cross_context_terms

// CrossContextTermMapping documents terms that differ across contexts.
// This prevents confusion when contexts communicate.

/*
TERM: "Asset"

In Asset Context (Owner):
  - Physical energy device (battery, PV panel, heat pump)
  - Has telemetry, state, capacity
  - Source of truth for asset properties

In Facility Context (Reference):
  - Asset ID only (foreign reference)
  - Used to track which assets are in which zones
  - No asset properties stored

In Billing Context (Reference):
  - Billable asset
  - Has pricing tier, contract terms
  - Different lifecycle than physical asset

---

TERM: "Zone"

In Facility Context (Owner):
  - Physical/logical area within facility
  - Has topology, contains points

In Billing Context:
  - Pricing zone (geographic tariff region)
  - Different entity entirely!

---

TERM: "Schedule"

In Braiin Context (Owner):
  - Optimization schedule for asset operation
  - Contains setpoints, time windows, constraints

In Facility Context (Reference):
  - Operating hours for facility
  - Different meaning entirely
*/
```

## Step 3: Create Context Map

The Context Map visualizes how bounded contexts relate to each other. Document the integration patterns used.

### Context Map Diagram

```text
+-----------------------------------------------------------------------------+
|                            CONTEXT MAP                                 |
+-----------------------------------------------------------------------------+

+------------------+          +------------------+          +------------------+
|  Facility        |<-events--|  Asset           |--events->|  Braiin          |
|  Context         |          |  Context         |          |  Context         |
|                  |          |                  |          |  (Core Domain)   |
|  [Aggregate      |--sync--->|  [Aggregate      |<--sync---|                  |
|   Owner]         |  query   |   Owner]         |  query   |  [Upstream]      |
+--------+---------+          +--------+---------+          +--------+---------+
         |                             |                             |
         | FacilityCreated             | AssetRegistered             | ScheduleOptimized
         | ZoneAdded                   | TelemetryReceived           | PeakShaved
         | TopologyChanged             | AssetStateChanged           | FlexibilityCommitted
         |                             |                             |
         +-----------------------------+-----------------------------+
                                       |
                           +-----------+------------+
                           |                        |
                   +-------v-------+        +-------v-------+
                   |  Grid         |        |  Billing      |
                   |  Context      |        |  Context      |
                   |               |        |               |
                   |  [ACL for     |        |  [Policy +    |
                   |   External]   |        |   Calculation]|
                   +---------------+        +---------------+
                           |                        |
                    External Grid           Settlement
                    Operators               Systems
```

### Relationship Types

```pseudocode
// contextmap/relationships

// RelationshipType defines how two contexts relate.
TYPE RelationshipType = String

CONSTANT Upstream RelationshipType = "upstream"
    // Upstream indicates this context provides data/events to downstream.
    // The upstream context sets the contract; downstream conforms.

CONSTANT Downstream RelationshipType = "downstream"
    // Downstream indicates this context consumes from upstream.
    // Must conform to upstream's contract.

CONSTANT Partnership RelationshipType = "partnership"
    // Partnership indicates mutual collaboration.
    // Both contexts negotiate contracts together.

CONSTANT CustomerSupplier RelationshipType = "customer-supplier"
    // CustomerSupplier indicates formal contract.
    // Supplier (upstream) meets customer (downstream) needs.

CONSTANT Conformist RelationshipType = "conformist"
    // Conformist indicates downstream must fully conform.
    // No negotiation; take what upstream provides.

CONSTANT ACL RelationshipType = "acl"
    // ACL indicates Anti-Corruption Layer.
    // Translates external model to domain model.

// ContextRelationship documents a relationship between two contexts.
TYPE ContextRelationship
    Source          String
    Target          String
    Type            RelationshipType
    IntegrationMode String // "sync-api", "async-events", "acl"
    Contract        String // Path to contract definition
END TYPE

// FacilityContextRelationships returns all relationships for Facility Context.
FUNCTION FacilityContextRelationships() RETURNS []ContextRelationship
    RETURN [
        ContextRelationship{
            Source:          "FacilityContext",
            Target:          "AssetContext",
            Type:            Upstream,
            IntegrationMode: "async-events",
            Contract:        "contracts/events/facility_created.json",
        },
        ContextRelationship{
            Source:          "AssetContext",
            Target:          "FacilityContext",
            Type:            Downstream,
            IntegrationMode: "sync-api",
            Contract:        "api/openapi.yaml",
        },
        ContextRelationship{
            Source:          "FacilityContext",
            Target:          "BraainContext",
            Type:            CustomerSupplier,
            IntegrationMode: "async-events",
            Contract:        "contracts/events/facility_created.json",
        },
    ]
END FUNCTION
```

## Step 4: Define Aggregates Within Context

Each Bounded Context contains one or more aggregates. Identify the aggregate roots and their boundaries.

### Aggregate Identification

```pseudocode
// core/domain/facility/aggregates

/*
FACILITY CONTEXT AGGREGATES

Aggregate 1: Facility (Root)
  - Root Entity: Facility
  - Child Entities: None (zones are separate aggregate)
  - Value Objects: Address, GeoLocation, FacilityType
  - Invariants:
    - Facility must have valid address
    - Facility type must be supported
    - Name must be unique within organization

Aggregate 2: Zone
  - Root Entity: Zone
  - Child Entities: Point (measurement/control points)
  - Value Objects: ZonePurpose, ZoneCapacity
  - Invariants:
    - Zone must reference valid facility (by ID)
    - Zone capacity must be positive
    - Points within zone must have unique names

Why separate aggregates?
  - Facility and Zone have different change rates
  - Zone can be modified without locking Facility
  - Points change frequently; Facility rarely changes
  - Smaller transaction boundaries = better concurrency
*/
```

### Facility Aggregate Implementation

```pseudocode
// core/domain/facility/facility

CONSTANT ErrInvalidStatus = Error("invalid facility status transition")

// FacilityType classifies the facility.
TYPE FacilityType = String

CONSTANT FacilityTypeCommercial FacilityType = "commercial"
CONSTANT FacilityTypeResidential FacilityType = "residential"
CONSTANT FacilityTypeIndustrial FacilityType = "industrial"
CONSTANT FacilityTypeDataCenter FacilityType = "data_center"

// FacilityStatus represents lifecycle status.
TYPE FacilityStatus = String

CONSTANT FacilityStatusDraft FacilityStatus = "draft"
CONSTANT FacilityStatusCommissioned FacilityStatus = "commissioned"
CONSTANT FacilityStatusActive FacilityStatus = "active"
CONSTANT FacilityStatusDecommissioned FacilityStatus = "decommissioned"

// Facility is the aggregate root for physical facilities.
TYPE Facility
    id              String
    organizationID  String
    name            String
    address         Address
    facilityType    FacilityType
    status          FacilityStatus
    commissionedAt  *Time
    createdAt       Time
    uncommittedEvents []Event
END TYPE

// NewFacility creates a new Facility aggregate.
CONSTRUCTOR NewFacility(orgID String, name String, addr Address, fType FacilityType) RETURNS (*Facility, Error)
    IF orgID == "" THEN
        RETURN nil, Error("organization ID is required")
    END IF
    IF name == "" THEN
        RETURN nil, Error("facility name is required")
    END IF
    IF err := addr.Validate(); err != nil THEN
        RETURN nil, Error("invalid address: " + err)
    END IF

    id := GenerateUUID()
    now := CurrentTimeUTC()

    f := &Facility{
        id:             id,
        organizationID: orgID,
        name:           name,
        address:        addr,
        facilityType:   fType,
        status:         FacilityStatusDraft,
        createdAt:      now,
    }

    f.raise(NewFacilityCreated(id, orgID, name, String(fType), addr))

    RETURN f, nil
END CONSTRUCTOR

// ID returns the facility identifier.
METHOD (f *Facility) ID() RETURNS String
    RETURN f.id
END METHOD

// Commission transitions facility to commissioned status.
METHOD (f *Facility) Commission() RETURNS Error
    IF f.status != FacilityStatusDraft THEN
        RETURN Error(ErrInvalidStatus + ": can only commission from draft status")
    END IF

    now := CurrentTimeUTC()
    f.status = FacilityStatusCommissioned
    f.commissionedAt = &now

    f.raise(NewFacilityCommissioned(f.id, now))

    RETURN nil
END METHOD

// Activate transitions facility to active status.
METHOD (f *Facility) Activate() RETURNS Error
    IF f.status != FacilityStatusCommissioned THEN
        RETURN Error(ErrInvalidStatus + ": can only activate commissioned facility")
    END IF

    f.status = FacilityStatusActive
    f.raise(NewFacilityActivated(f.id))

    RETURN nil
END METHOD

METHOD (f *Facility) raise(event Event)
    f.uncommittedEvents = APPEND(f.uncommittedEvents, event)
END METHOD

// UncommittedEvents returns events not yet persisted.
METHOD (f *Facility) UncommittedEvents() RETURNS []Event
    RETURN f.uncommittedEvents
END METHOD

// ClearUncommittedEvents clears events after persistence.
METHOD (f *Facility) ClearUncommittedEvents()
    f.uncommittedEvents = nil
END METHOD
```

### Address Value Object

```pseudocode
// core/domain/facility/address

CONSTANT ErrInvalidAddress = Error("invalid address")

// Address represents a physical location.
TYPE Address
    street     String
    city       String
    postalCode String
    country    String
    geo        *GeoLocation
END TYPE

// NewAddress creates a validated Address.
CONSTRUCTOR NewAddress(street String, city String, postalCode String, country String) RETURNS (Address, Error)
    IF street == "" THEN
        RETURN Address{}, Error(ErrInvalidAddress + ": street is required")
    END IF
    IF city == "" THEN
        RETURN Address{}, Error(ErrInvalidAddress + ": city is required")
    END IF
    IF country == "" THEN
        RETURN Address{}, Error(ErrInvalidAddress + ": country is required")
    END IF

    RETURN Address{
        street:     street,
        city:       city,
        postalCode: postalCode,
        country:    country,
    }, nil
END CONSTRUCTOR

// Validate checks address validity.
METHOD (a Address) Validate() RETURNS Error
    IF a.street == "" OR a.city == "" OR a.country == "" THEN
        RETURN ErrInvalidAddress
    END IF
    RETURN nil
END METHOD

// WithGeoLocation returns address with geo coordinates.
METHOD (a Address) WithGeoLocation(lat Float64, lon Float64) RETURNS (Address, Error)
    geo, err := NewGeoLocation(lat, lon)
    IF err != nil THEN
        RETURN Address{}, err
    END IF
    a.geo = &geo
    RETURN a, nil
END METHOD

// GeoLocation represents latitude/longitude coordinates.
TYPE GeoLocation
    latitude  Float64
    longitude Float64
END TYPE

// NewGeoLocation creates validated coordinates.
CONSTRUCTOR NewGeoLocation(lat Float64, lon Float64) RETURNS (GeoLocation, Error)
    IF lat < -90 OR lat > 90 THEN
        RETURN GeoLocation{}, Error("latitude must be between -90 and 90")
    END IF
    IF lon < -180 OR lon > 180 THEN
        RETURN GeoLocation{}, Error("longitude must be between -180 and 180")
    END IF
    RETURN GeoLocation{latitude: lat, longitude: lon}, nil
END CONSTRUCTOR
```

## Step 5: Design Cross-Context Communication Ports

Define how this context communicates with others. Use ports (interfaces) for clean boundaries.

### OutPorts for External Context Queries

```pseudocode
// core/application/ports/outports/external_contexts

// AssetContextClient provides access to Asset Context.
// This is an OutPort - implementation lives in adapters.
INTERFACE AssetContextClient
    // GetAssetsByFacility retrieves asset IDs for a facility.
    // Returns only IDs - asset details are owned by Asset Context.
    METHOD GetAssetsByFacility(ctx Context, facilityID String) RETURNS ([]String, Error)

    // HasActiveAssets checks if facility has any active assets.
    // Used before allowing facility decommission.
    METHOD HasActiveAssets(ctx Context, facilityID String) RETURNS (Boolean, Error)
END INTERFACE

// BraainContextClient provides access to Braiin Context.
INTERFACE BraainContextClient
    // GetActiveSchedules retrieves active optimization schedules for facility.
    // Used for facility dashboard aggregation.
    METHOD GetActiveSchedules(ctx Context, facilityID String) RETURNS ([]ScheduleSummary, Error)
END INTERFACE

// ScheduleSummary is a DTO for schedule information from Braiin Context.
// This is a read model, not a domain entity.
TYPE ScheduleSummary
    ScheduleID String
    StartTime  String
    EndTime    String
    Status     String
END TYPE
```

### Event Publishing Port

```pseudocode
// core/application/ports/outports/event_publisher

// EventPublisher publishes domain events to the event bus.
INTERFACE EventPublisher
    // Publish sends events to the event bus.
    // Events are published after successful aggregate persistence.
    METHOD Publish(ctx Context, events []Event) RETURNS Error
END INTERFACE
```

### InPort for Commands

```pseudocode
// core/application/ports/inports/facility_commands

// CreateFacilityCommand contains input for facility creation.
TYPE CreateFacilityCommand
    OrganizationID String
    Name           String
    Street         String
    City           String
    PostalCode     String
    Country        String
    FacilityType   String
    Latitude       *Float64
    Longitude      *Float64
END TYPE

// CreateFacilityResult contains output from facility creation.
TYPE CreateFacilityResult
    FacilityID String
END TYPE

// FacilityCommandHandler handles facility commands.
INTERFACE FacilityCommandHandler
    METHOD CreateFacility(ctx Context, cmd CreateFacilityCommand) RETURNS (*CreateFacilityResult, Error)
    METHOD CommissionFacility(ctx Context, facilityID String) RETURNS Error
    METHOD ActivateFacility(ctx Context, facilityID String) RETURNS Error
    METHOD DecommissionFacility(ctx Context, facilityID String) RETURNS Error
END INTERFACE
```

## Step 6: Document Context Boundaries

Create explicit documentation of what the context owns and its contracts.

### Context Boundary Documentation

```yaml
# docs/context-boundary.yaml
context:
  name: FacilityContext
  description: "Manages physical facility definitions, topology, and lifecycle"
  team: Platform Team
  repository: github.com//services/facility-context

ownership:
  entities:
    - name: Facility
      description: "Physical location where energy assets are managed"
      source_of_truth: true
    - name: Zone
      description: "Logical subdivision within a facility"
      source_of_truth: true
    - name: Point
      description: "Measurement or control location within a zone"
      source_of_truth: true

  references_only:
    - entity: Asset
      owned_by: AssetContext
      reference_type: "asset_id only"
    - entity: Organization
      owned_by: UserContext
      reference_type: "organization_id only"

published_events:
  - name: FacilityCreated
    schema: contracts/events/facility_created.json
    version: "1.0.0"
    description: "Raised when a new facility is created"
  - name: FacilityCommissioned
    schema: contracts/events/facility_commissioned.json
    version: "1.0.0"
    description: "Raised when facility is ready for asset registration"
  - name: ZoneAdded
    schema: contracts/events/zone_added.json
    version: "1.0.0"
    description: "Raised when a zone is added to a facility"

consumed_events:
  - name: AssetRegistered
    from: AssetContext
    handler: "Update facility asset count cache"
  - name: AssetRemoved
    from: AssetContext
    handler: "Update facility asset count cache"

public_apis:
  - path: /v1/facilities
    methods: [GET, POST]
    contract: api/openapi.yaml
  - path: /v1/facilities/{id}
    methods: [GET, PUT, DELETE]
    contract: api/openapi.yaml
  - path: /v1/facilities/{id}/zones
    methods: [GET, POST]
    contract: api/openapi.yaml

dependencies:
  sync:
    - context: AssetContext
      purpose: "Check for active assets before decommission"
      api: "/v1/facilities/{id}/assets"
  async:
    - context: BraainContext
      purpose: "Receive optimization updates"
      events: [ScheduleOptimized]
```

### Directory Structure

```text
services/facility-context/
+-- cmd/
|   +-- api/
|       +-- main.go                    # Lambda entry point
+-- core/
|   +-- domain/
|   |   +-- facility/
|   |       +-- facility.go            # Facility aggregate root
|   |       +-- zone.go                # Zone aggregate root
|   |       +-- address.go             # Address value object
|   |       +-- events.go              # Domain events
|   |       +-- errors.go              # Domain errors
|   |       +-- repository.go          # Repository port
|   +-- application/
|       +-- ports/
|       |   +-- inports/
|       |   |   +-- facility_commands.go
|       |   +-- outports/
|       |       +-- facility_repository.go
|       |       +-- event_publisher.go
|       |       +-- external_contexts.go
|       +-- usecases/
|           +-- create_facility.go
|           +-- commission_facility.go
|           +-- add_zone.go
+-- adapters/
|   +-- primary/
|   |   +-- lambda/
|   |       +-- handler.go
|   +-- secondary/
|       +-- dynamodb/
|       |   +-- facility_repository.go
|       +-- eventbridge/
|       |   +-- publisher.go
|       +-- clients/
|           +-- asset_context_client.go
+-- contracts/
|   +-- events/
|   |   +-- facility_created.json
|   |   +-- zone_added.json
|   +-- mocks/
|       +-- asset_client.go
+-- api/
|   +-- openapi.yaml
+-- docs/
|   +-- glossary.md
|   +-- context-boundary.yaml
|   +-- context-map.md
+-- Makefile
+-- go.mod
```

## Step 7: Implement Use Case with Context Awareness

Use cases should respect context boundaries and use ports for cross-context communication.

```pseudocode
// core/application/usecases/decommission_facility

CONSTANT ErrCannotDecommission = Error("cannot decommission facility")

// DecommissionFacilityUseCase handles facility decommissioning.
TYPE DecommissionFacilityUseCase
    repo        FacilityRepository
    assetClient AssetContextClient
    publisher   EventPublisher
END TYPE

// NewDecommissionFacilityUseCase creates the use case with dependencies.
CONSTRUCTOR NewDecommissionFacilityUseCase(
    repo FacilityRepository,
    assetClient AssetContextClient,
    publisher EventPublisher,
) RETURNS *DecommissionFacilityUseCase
    RETURN &DecommissionFacilityUseCase{
        repo:        repo,
        assetClient: assetClient,
        publisher:   publisher,
    }
END CONSTRUCTOR

// Execute decommissions a facility if business rules allow.
METHOD (uc *DecommissionFacilityUseCase) Execute(ctx Context, facilityID String) RETURNS Error
    // Load aggregate from repository
    fac, err := uc.repo.FindByID(ctx, facilityID)
    IF err != nil THEN
        RETURN Error("failed to find facility: " + err)
    END IF

    // Cross-context check: ensure no active assets
    // This queries Asset Context through the port, respecting boundaries
    hasAssets, err := uc.assetClient.HasActiveAssets(ctx, facilityID)
    IF err != nil THEN
        RETURN Error("failed to check assets: " + err)
    END IF
    IF hasAssets THEN
        RETURN Error(ErrCannotDecommission + ": facility has active assets")
    END IF

    // Execute domain operation (business logic in aggregate)
    IF err := fac.Decommission(); err != nil THEN
        RETURN Error("failed to decommission: " + err)
    END IF

    // Persist changes
    IF err := uc.repo.Save(ctx, fac); err != nil THEN
        RETURN Error("failed to save facility: " + err)
    END IF

    // Publish events for other contexts to react
    IF err := uc.publisher.Publish(ctx, fac.UncommittedEvents()); err != nil THEN
        RETURN Error("failed to publish events: " + err)
    END IF

    fac.ClearUncommittedEvents()

    RETURN nil
END METHOD
```

The use case queries Asset Context through a port (not by accessing Asset's database), respecting the Bounded Context boundary.

## Verification Checklist

After creating your Bounded Context, verify:

- [ ] Business capability is clearly identified with data ownership
- [ ] Ubiquitous Language glossary is documented with context-specific meanings
- [ ] Context map shows relationships with other contexts
- [ ] Integration patterns (sync/async, upstream/downstream) are explicit
- [ ] Aggregates are identified with clear boundaries
- [ ] Cross-context communication uses ports (interfaces)
- [ ] No direct access to other contexts' databases
- [ ] Domain events are published for state changes
- [ ] Event schemas are versioned and documented
- [ ] OpenAPI contract is defined for public APIs
- [ ] Directory structure follows Clean Architecture layers
- [ ] Domain layer has no infrastructure imports
- [ ] Context boundary documentation exists (glossary, contracts, ownership)
