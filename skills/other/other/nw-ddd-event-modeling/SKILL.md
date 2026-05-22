---
name: nw-ddd-event-modeling
description: Event Modeling facilitation technique — brainstorm events, identify commands and views, define aggregate boundaries, write Given-When-Then specifications
user-invocable: false
disable-model-invocation: true
---

# Event Modeling

Collaborative visual design technique created by Adam Dymitruk. The Event Model IS the specification -- it replaces traditional requirements documents with a single, living visual artifact.

## Key Properties

- **Collaborative**: Everyone participates (devs, business, UX)
- **Visual**: Colored elements on a timeline (physical or digital board)
- **Timeline-based**: Events arranged chronologically, left to right
- **Spec-generating**: Model directly produces testable Given/When/Then specifications
- **Technology-agnostic**: Describes WHAT happens, not HOW it's implemented

## The Color System

| Color | Element | Description | Example |
|-------|---------|-------------|---------|
| Orange | **Event** | Something that happened (past tense) | OrderPlaced, PaymentReceived |
| Blue | **Command** | User intent/action (imperative) | PlaceOrder, ProcessPayment |
| Green | **Read Model/View** | Data displayed to user | Order Summary, Shipping Dashboard |
| White | **Screen/UI** | User interface wireframe | Order Form, Checkout Page |
| Yellow | **Automation/Policy** | System reaction (saga/process manager) | "When PaymentReceived, then ConfirmOrder" |
| Red | **External System** | Integration point | Payment Gateway, Email Service |

## Four Phases

### Phase 1: Event Brainstorming (10-20 min)

Discover all meaningful things that happen in the system.

**Process**: Everyone writes events on orange stickies (past tense, domain language) | Place on timeline (left = earlier, right = later) | No filtering -- capture everything | Group related events vertically (these form swimlanes/slices)

**Facilitation tips**:
- Start with the happy path -- what happens when everything goes right?
- Then add error/exception events
- Ask: "What happens before this? What happens after?"
- Business people identify events developers miss
- Don't worry about order precision -- rough chronological is fine

**Example timeline**:
```
Timeline ─────────────────────────────────────────────────>

[CustomerRegistered] [ItemAddedToCart] [OrderPlaced] [PaymentReceived]
                     [ItemRemovedFromCart]            [PaymentFailed]
                                       [OrderCancelled] [OrderConfirmed]
                                                        [ItemShipped]
                                                        [RefundRequested]
```

### Phase 2: Commands and Views (15-25 min)

Understand what triggers events and what users need to see.

**Commands (blue)**: What action causes each event? Who initiates it? Place ABOVE events.

**Read Models (green)**: What information does the user need to act? What does the screen show after? Place BELOW events.

**Screens (white)**: What does the UI look like? Sketch wireframes. Place at top.

**Wiring pattern**:
```
Screen -> Command -> Event(s) -> Read Model -> Screen
```

### Phase 3: Automations and Integrations (10-15 min)

Find system-driven reactions to events.

**Automations (yellow)**: "When [event] happens, the system should [command]." These become sagas or process managers. Place between triggering event and resulting command.

**External systems (red)**: Payment gateways, email services, shipping providers. Integration boundaries.

### Phase 4: Given/When/Then Specifications (10-20 min)

Turn the model into precise, testable specifications.

For each command-event combination:
```
GIVEN:
  - CustomerRegistered { customerId: "C1", name: "Ale" }
  - ItemAddedToCart { cartId: "CART1", itemId: "ITEM1", quantity: 2 }

WHEN:
  - PlaceOrder { cartId: "CART1", customerId: "C1" }

THEN:
  - OrderPlaced { orderId: "O1", customerId: "C1", items: [...], total: 59.98 }
```

These specifications become: **Tests** (directly translatable) | **Documentation** (readable by everyone) | **Contract** (unambiguous business-dev agreement)

## Four Information Flow Patterns

The Event Model reveals four patterns:

**1. Command (State Change)**: Screen -> Command -> Event(s). User action changes state. Implementation: command handler validates, aggregate emits events.

**2. View (Information Retrieval)**: Event(s) -> Projection -> Read Model -> Screen. Events transformed into query-optimized views. Implementation: projection subscribes and updates read model.

**3. Automation (System Reaction)**: Event(s) -> Policy/Saga -> Command. System reacts to events by issuing new commands. Implementation: saga/process manager.

**4. Translation (External Integration)**: External Event -> Translator -> Internal Command (or reverse). Boundary between systems. Implementation: anti-corruption layer.

## From Model to Vertical Slices

Each column in the Event Model (Screen -> Command -> Event -> Read Model) becomes a vertical slice -- an independently implementable feature.

```
           Slice 1         Slice 2         Slice 3
         ┌──────────┐   ┌──────────┐   ┌──────────┐
UI       │ OrderForm │   │ PaymentPg│   │ Dashboard │
         ├──────────┤   ├──────────┤   ├──────────┤
Cmd/Qry  │PlaceOrder │   │ProcessPay│   │GetOrders  │
         ├──────────┤   ├──────────┤   ├──────────┤
Domain   │OrderAgg   │   │PaymentAgg│   │OrderProj  │
         ├──────────┤   ├──────────┤   ├──────────┤
Infra    │EventStore │   │EventStore│   │ReadModelDB│
         └──────────┘   └──────────┘   └──────────┘
```

**Benefits**: Each slice independently implementable and deployable | Easy to parallelize across team | Model shows exactly how many slices exist and their dependencies | Each slice maps to a portion of the Event Model

## Specification Patterns

**Happy path**: GIVEN events that set up valid state | WHEN valid command | THEN expected events

**Validation failure**: GIVEN events (possibly none) | WHEN invalid command | THEN error (no events emitted)

**Idempotency**: GIVEN events including effect already applied | WHEN same command again | THEN no new events

**State-dependent**: Same command produces different results depending on prior events

## Event Modeling vs Other Techniques

| Aspect | Event Modeling | EventStorming | DDD Strategic Design |
|--------|--------------|---------------|---------------------|
| Focus | Complete system design | Domain exploration | Bounded context mapping |
| Output | Full spec + implementation slices | Shared understanding | Context map + language |
| Detail | Very detailed (down to fields) | Medium (event+command level) | High-level (boundaries) |
| Duration | Half day to full day | Hours to days | Ongoing |
| Code generation | Directly possible | Not directly | Not directly |
| Testing | Produces testable specs | Produces insights | Produces guidance |

**These techniques are complementary**: EventStorming to explore/understand | DDD Strategic Design to identify contexts | Event Modeling to design implementation within each context.

## Session Facilitation Guide

**Preparation**: Invite developers + product owner + domain experts + UX designer | Duration: 2-4 hours (new system), 1-2 hours (feature) | Tools: Miro (digital) or large wall with colored stickies | Pre-work: brief domain introduction (2-3 sentences)

**Flow**: Intro (5 min): explain colors and phases | Event brainstorm (15 min): everyone writes, place on timeline | Organize (10 min): cluster, de-duplicate, identify gaps | Commands & Views (20 min): blue and green stickies | Wire it up (10 min): draw arrows showing data flow | Automations (10 min): policies and external systems | Given/When/Then (20 min): specs for key slices | Review (10 min): walk through entire model as narrative

**Common mistakes**: Too many events at once (start with happy path) | Technical events instead of business language | Skipping views (read models as important as commands) | Not involving business people | Jumping to implementation before finishing model
