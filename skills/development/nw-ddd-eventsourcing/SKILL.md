---
name: nw-ddd-eventsourcing
description: Event Sourcing and CQRS as DDD implementation patterns — when to use, aggregate event streams, projections, snapshots, sagas, upcasting, conflict resolution
user-invocable: false
disable-model-invocation: true
---

# Event Sourcing and CQRS

Implementation patterns for DDD. Event Sourcing stores every state change as an immutable event and derives current state from replay. CQRS separates write and read models. These are tools, not mandatory architecture -- apply selectively to domains where they add value.

## When to Use Event Sourcing

**ES adds value when**:
- Complete audit trail required (financial, regulatory, medical)
- Temporal queries needed ("what was the state on January 15?")
- Multiple views of same data (different read models for different consumers)
- Complex domain with rich business rules (natural fit with DDD aggregates)
- Event-driven integration with other systems
- Debugging requires replay ("what exactly happened?")

**ES is overkill when**:
- Simple CRUD with no audit requirements
- Team unfamiliar and project has no learning budget
- No business value from history
- Domain has no behavior (data in, data out)

**Key question**: "Does knowing the history of how we got here provide business value?" Yes -> consider ES. No -> traditional CRUD is simpler.

## Core Concepts

### Events as Facts

Events are immutable records of things that happened. Past tense: `OrderPlaced`, `PaymentReceived`, `ItemShipped`.

**Event structure**: Include all data needed to understand what happened (self-contained) | Use domain language | One event per meaningful business fact | Events carry data only, no behavior

**Granularity**: Too coarse (`OrderUpdated { order: {...} }`) loses what changed. Too fine (`OrderFieldChanged { field, old, new }`) is generic audit log. Just right (`OrderConfirmed { orderId, confirmedBy, confirmedAt }`) has clear business meaning.

### The Event Store

Single source of truth. Core operations:
- `append(streamId, expectedVersion, events)` -> success or concurrency conflict
- `read(streamId)` -> ordered list of events
- `subscribe(filter)` -> push notification for new events

**Properties**: Append-only (never modify/delete) | Ordered within stream | Immutable | Versioned (each event has position)

**Stream identity**: Each aggregate instance owns a stream: `Order-123`, `Customer-789`. The stream ID is the aggregate ID.

### Aggregate Event Lifecycle

1. Receive command -> validate business rules
2. Emit events -> record what happened
3. Apply events -> update internal state (no validation, no side effects)
4. Persist events -> append to event store

**Loading (rehydration)**: Read all events from stream -> create empty aggregate -> apply each event in order -> aggregate in current state, ready for commands.

### CQRS Split

| Aspect | Write Side (Commands) | Read Side (Queries) |
|--------|----------------------|---------------------|
| Purpose | Validate + change state | Serve information |
| Model | Aggregates (normalized) | Projections (denormalized) |
| Optimization | Consistency, correctness | Query speed, UX |
| Scale | Lower throughput typically | Higher throughput |
| Technology | Event store | Any DB (SQL, NoSQL, search, graph) |

**Data flow**: Command -> Aggregate -> Event Store -> Projection -> Read Model -> Query

## Key Patterns

### Projections and Read Models

Projections transform events into query-optimized views. Properties: **disposable** (rebuild from event store anytime) | **eventually consistent** (lag between event and update) | **purpose-specific** (one per use case) | **multiple** (same events feed many views)

**Types**: Live (real-time as events arrive) | Catch-up (replay from beginning, then switch to live) | One-off (replay once for analytics/migration)

**Rebuilding**: Delete read model -> replay all events from position 0 -> switch to live processing. This is a superpower: add new views retroactively from complete history.

### Snapshots

For aggregates with thousands of events, periodically save state snapshot. On load: load latest snapshot + replay only events after snapshot. Fewer events to process.

**When**: After every N events (e.g., 100) or when load time exceeds threshold. Don't snapshot prematurely -- most aggregates have <100 events and load in milliseconds.

### Sagas and Process Managers

Business processes spanning multiple aggregates. A saga listens for events and issues commands to coordinate multi-step processes.

**Key principles**: React to events, issue commands (no business logic in saga) | Maintain process state (which step completed) | Handle compensation (rollback on failure) | Keep simple -- complex saga = design smell

**Todo Pattern** (alternative): Model process as a "todo list" aggregate tracking what needs to be done. All state visible in one place, progress queryable, easy to add/remove steps.

### Upcasting (Event Versioning)

Events are immutable, but schemas evolve. Transform old formats to new during loading.

**Weak schema** (start here): Flexible format (JSON), handle missing fields with defaults.

**Explicit upcaster**: Transform V1 -> V2 in a pipeline during event loading, before reaching aggregate/projection.

**Upcaster chain**: V1 -> V2 -> V3. Each handles one version jump. Test all paths.

### Conflict Resolution

Two concurrent commands on same aggregate cause version conflict. Strategies: **Retry** (default, reload and re-execute) | **Merge** (domain-specific, both changes apply) | **Reject** (inform user, safest for critical operations). Start with retry -- most conflicts resolve automatically.

### Eventual Consistency

Read side lags write side. Typical: microseconds (same process) to low seconds (across network).

**Mitigation**: Read-your-own-writes (return command result directly, not from read model) | Optimistic UI (apply expected change on client immediately) | Causal consistency (version token with queries, wait until projection catches up)

## Additional Patterns

**Reservation Pattern**: Enforce uniqueness constraints (unique email) using dedicated reservation aggregate or DB constraint. Uniqueness in ES is harder than CRUD -- choose strictness based on criticality.

**Outbox Pattern**: Atomically update event store AND publish to message broker by writing to outbox table in same transaction. Relay process publishes to broker asynchronously.

**Decider Pattern**: Purely functional aggregate: `decide(Command, State) -> List<Event>`, `evolve(State, Event) -> State`, `initialState() -> State`. Trivially testable, framework-agnostic.

**Tombstone Events**: Handle deletion in append-only store by emitting a tombstone event. Aggregate refuses commands after tombstone. For GDPR: crypto-shredding or event replacement.

**Event-Carried State Transfer**: Include relevant data in events even if duplicated from other aggregates. Self-contained events eliminate callback lookups for projections.

**Temporal Queries**: Replay events up to a timestamp to reconstruct historical state. Impossible with traditional state-based storage. Use for: compliance, debugging, analytics, dispute resolution.

## Technology Options

| Technology | Platform | Notes |
|-----------|----------|-------|
| EventStoreDB | Any (gRPC) | Purpose-built, native projections, by Greg Young |
| Axon Server/Framework | Java/Kotlin | Full CQRS/ES framework with command/query bus |
| Marten | .NET (C#) | PostgreSQL as event store + document DB |
| PostgreSQL (manual) | Any | Append-only table with indexing -- simple but manual |
| Eventuous | .NET (C#) | Lightweight modern .NET ES framework |

## Testing Strategy

**Given/When/Then** is the primary pattern:
```
GIVEN: [prior events that set up state]
WHEN:  [command being issued]
THEN:  [resulting events OR error]
```

**Testing pyramid**: Value Objects (base) -> Aggregate G/W/T (bulk) -> Projection tests -> Saga tests -> E2E (few)

**Implementation maps directly from Event Model specifications to test code.** The specification IS the test.
