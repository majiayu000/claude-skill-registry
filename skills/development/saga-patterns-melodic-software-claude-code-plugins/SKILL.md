---
name: event-modeling
description: Adam Dymitruk's Event Modeling methodology with swimlanes
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Event Modeling Skill

## When to Use This Skill

Use this skill when:

- **Event Modeling tasks** - Working on adam dymitruk's event modeling methodology with swimlanes
- **Planning or design** - Need guidance on Event Modeling approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Create Event Models using Adam Dymitruk's visual methodology for designing event-driven systems.

## MANDATORY: Documentation-First Approach

Before creating Event Models:

1. **Invoke `docs-management` skill** for Event Modeling patterns
2. **Verify methodology** via MCP servers (perplexity, eventmodeling.org)
3. **Base guidance on Adam Dymitruk's original methodology**

## Event Modeling Fundamentals

```text
Event Modeling Structure:

TIME FLOWS LEFT TO RIGHT ───────────────────────────────────────────►

┌─────────────────────────────────────────────────────────────────────┐
│ BLUE: UI / Commands / External Triggers                            │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐                           │
│ │ Screen/  │  │ Button   │  │ API      │                           │
│ │ Wireframe│  │ Click    │  │ Call     │                           │
│ └────┬─────┘  └────┬─────┘  └────┬─────┘                           │
├──────┼─────────────┼─────────────┼──────────────────────────────────┤
│      ▼             ▼             ▼                                  │
│ ORANGE: Domain Events (State Changes)                              │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│ │ OrderPlaced  │ │ OrderPaid    │ │ OrderShipped │                 │
│ └──────────────┘ └──────────────┘ └──────────────┘                 │
│      │                 │               │                            │
├──────┼─────────────────┼───────────────┼────────────────────────────┤
│      ▼                 ▼               ▼                            │
│ GREEN: Read Models / Projections                                   │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│ │ Order List   │ │ Payment      │ │ Shipping     │                 │
│ │ View         │ │ Status       │ │ Dashboard    │                 │
│ └──────────────┘ └──────────────┘ └──────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Four Types of Specifications

### 1. Commands (Blue Lane - Top)

```text
Commands: User intentions that may cause state changes

CHARACTERISTICS:
- Represent user actions or external triggers
- May succeed or fail (validation)
- Produce one or more events on success
- Include wireframes/mockups for UI commands

EXAMPLES:
┌─────────────────────────────┐
│ PlaceOrder                  │
├─────────────────────────────┤
│ • Customer ID               │
│ • Items: [ProductId, Qty]   │
│ • Shipping Address          │
│ • Payment Method            │
└─────────────────────────────┘
```

### 2. Events (Orange Lane - Middle)

```text
Events: Facts that have happened (past tense, immutable)

CHARACTERISTICS:
- Past tense naming (OrderPlaced, not PlaceOrder)
- Immutable once recorded
- Capture what happened and when
- Single source of truth

NAMING CONVENTION:
✓ OrderPlaced
✓ PaymentReceived
✓ ShipmentDispatched
✗ PlaceOrder (command, not event)
✗ OrderUpdate (too vague)

EXAMPLE:
┌─────────────────────────────┐
│ OrderPlaced                 │
├─────────────────────────────┤
│ • OrderId: guid             │
│ • CustomerId: guid          │
│ • Items: [...]              │
│ • PlacedAt: timestamp       │
│ • TotalAmount: decimal      │
└─────────────────────────────┘
```

### 3. Read Models (Green Lane - Bottom)

```text
Read Models: Projections optimized for queries

CHARACTERISTICS:
- Built from events
- Optimized for specific query patterns
- Can be rebuilt from event stream
- Eventually consistent

TYPES:
- List views (showing multiple items)
- Detail views (single item details)
- Dashboards (aggregations)
- Search indexes

EXAMPLE:
┌─────────────────────────────┐
│ OrderSummaryView            │
├─────────────────────────────┤
│ • OrderId                   │
│ • CustomerName              │
│ • Status (derived)          │
│ • ItemCount                 │
│ • TotalAmount               │
│ • LastUpdated               │
└─────────────────────────────┘
```

### 4. Automations (Policies/Reactions)

```text
Automations: Processes triggered by events

CHARACTERISTICS:
- React to events automatically
- May produce commands or integrate external systems
- Represent business policies
- Handle async processing

NOTATION:
┌─────────────────────────────┐
│ ⚡ PaymentReceivedPolicy    │
├─────────────────────────────┤
│ WHEN: PaymentReceived       │
│ THEN: InitiateShipment      │
└─────────────────────────────┘
```

## Event Modeling Process

### Step 1: Brain Dump Events

```text
Brainstorm all domain events (orange stickies):

1. Gather stakeholders
2. Ask: "What happens in this process?"
3. Write events in past tense
4. Don't worry about order yet
5. Include all significant state changes

Example Output:
- OrderPlaced
- OrderConfirmed
- PaymentReceived
- PaymentFailed
- InventoryReserved
- ShipmentCreated
- ShipmentDispatched
- OrderDelivered
```

### Step 2: Arrange Timeline

```text
Organize events chronologically:

1. Find the "happy path" events
2. Arrange left to right
3. Group related events vertically
4. Identify parallel flows
5. Note temporal dependencies

Timeline:
OrderPlaced → OrderConfirmed → PaymentReceived → InventoryReserved → ShipmentCreated → ShipmentDispatched → OrderDelivered
                                   │
                                   └→ PaymentFailed → OrderCancelled
```

### Step 3: Add Commands (Blue)

```text
What triggers each event?

For each event, ask:
- What user action caused this?
- What external system triggered it?
- Is there a UI screen involved?

Add commands above events they produce:
[PlaceOrder] → OrderPlaced
[ProcessPayment] → PaymentReceived
[DispatchShipment] → ShipmentDispatched
```

### Step 4: Add Read Models (Green)

```text
What information is needed for each command?

For each command, ask:
- What data does the user need to see?
- What validation data is required?
- What views enable this action?

Add read models below events that populate them:
OrderPlaced → [OrderConfirmationView]
ShipmentDispatched → [TrackingDashboard]
```

### Step 5: Identify Automations

```text
What happens automatically?

Look for:
- Events that trigger other events
- Integration with external systems
- Time-based rules
- Business policies

Example:
PaymentReceived → ⚡ ReserveInventoryPolicy → InventoryReserved
```

## Event Model Template

```markdown
# Event Model: [Process Name]

## Overview
[What this process accomplishes]

## Actors
- [User type 1]
- [User type 2]
- [External system]

## Event Model Diagram

```text
TIME ──────────────────────────────────────────────────────────────►

COMMANDS (Blue)
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Cmd 1   │    │ Cmd 2   │    │ Cmd 3   │    │ Cmd 4   │
└────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
EVENTS (Orange)
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Event1  │───►│ Event2  │───►│ Event3  │───►│ Event4  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
READ MODELS (Green)
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ View 1  │    │ View 2  │    │ View 3  │    │ View 4  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

## Commands Detail

| Command | Input | Produces Events | Read Model Needed |
|---------|-------|-----------------|-------------------|
| [Name] | [Data] | [Events] | [View] |

## Events Detail

| Event | Data | Triggered By | Updates |
|-------|------|--------------|---------|
| [Name] | [Fields] | [Command/Automation] | [Read Models] |

## Read Models Detail

| Read Model | Purpose | Updated By Events |
|------------|---------|-------------------|
| [Name] | [Query it answers] | [Events list] |

## Automations

| Automation | Trigger Event | Action | Produces |
|------------|---------------|--------|----------|
| [Name] | [Event] | [What it does] | [Events/Side effects] |

```text

```

## Patterns and Guidelines

### Given/When/Then Specifications

```text
Each slice can be expressed as:

GIVEN: [Read Model State / Context]
WHEN: [Command is executed]
THEN: [Events are produced]
  AND: [Read Models are updated]

Example:
GIVEN: Cart exists with items
WHEN: PlaceOrder command executed
THEN: OrderPlaced event recorded
  AND: OrderSummaryView updated
  AND: InventoryReservationRequested event triggered
```

### Slices (Vertical Features)

```text
A slice includes everything for one feature:

┌─────────────────────────────┐
│         SLICE 1             │
│  ┌─────────────────────┐    │
│  │ Command: PlaceOrder │    │
│  └─────────────────────┘    │
│  ┌─────────────────────┐    │
│  │ Event: OrderPlaced  │    │
│  └─────────────────────┘    │
│  ┌─────────────────────┐    │
│  │ View: OrderSummary  │    │
│  └─────────────────────┘    │
└─────────────────────────────┘

Each slice is independently implementable and testable.
```

### Blue Print (Implementation Guide)

```text
Event Model becomes implementation blueprint:

1. Commands → API Endpoints / UI Components
2. Events → Event Store Schema
3. Read Models → Database Tables / Views
4. Automations → Event Handlers / Policies

Each slice maps directly to code.
```

## Workflow

When creating Event Models:

1. **Define Scope**: What process are we modeling?
2. **Brain Dump Events**: List all state changes
3. **Arrange Timeline**: Order events chronologically
4. **Add Commands**: What triggers each event?
5. **Add Read Models**: What data supports each command?
6. **Identify Automations**: What happens automatically?
7. **Validate with Stakeholders**: Does this match reality?
8. **Define Slices**: Group into implementable features

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
