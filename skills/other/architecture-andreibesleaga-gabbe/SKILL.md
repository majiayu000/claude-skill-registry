---
name: diagramming
description: Choose the right diagram type for a documentation need, then create it using standard notation. Covers all major diagram families: UML structural/behavioral, C4 architecture, ER data, BPMN process, and domain diagrams. Produces Mermaid-compatible syntax where possible.
triggers: [create diagram, draw diagram, which diagram, diagram this, visualize, sequence diagram, class diagram, flowchart, architecture diagram, ER diagram, state diagram, activity diagram, context diagram, swimlane]
context_cost: low
---

# Diagramming Skill

## Goal

Select the appropriate diagram type for the communication need, create it using correct
notation and standards, and produce output in Mermaid syntax (or PlantUML as fallback).
Diagrams are communication tools — choose based on what question the reader needs answered.

---

## Diagram Selection Guide

```
Question being answered → Diagram type

"What IS the system and who uses it?"           → System Context (C4 Level 1)
"What are the major deployable parts?"           → Container Diagram (C4 Level 2)
"What are the components inside a container?"    → Component Diagram (C4 Level 3)
"How are business objects structured?"           → Domain Class Diagram
"How are data tables related?"                   → Entity-Relationship Diagram
"What packages/modules exist?"                   → Package Diagram
"How does process X flow step by step?"          → Sequence Diagram
"What are all the paths through a use case?"     → Activity Diagram
"What states can object X be in?"                → State Machine Diagram
"Who does what in a process?"                    → Swimlane Diagram (BPMN or Activity)
"How does the business process work end-to-end?" → BPMN Process Diagram
"What are all the use cases for an actor?"       → Use Case Diagram
"Where is the system deployed physically?"       → Deployment Diagram (C4 or UML)
"How does data flow through the system?"         → Data Flow Diagram (DFD)
"What are the business capabilities?"            → Capability Map
"How do domains relate to each other?"           → Context Map
"What happened in what order (events)?"          → Event Storming / Timeline
```

---

## Diagram Standards by Type

### C4 Architecture Diagrams (Mermaid C4)

```
Level of abstraction:
  Level 1 — System Context: whole system as one box + external actors
  Level 2 — Container:      major deployable units (apps, databases, services)
  Level 3 — Component:      major components inside ONE container
  Level 4 — Code:           class/entity level (use sparingly)

Rules:
  - Each diagram has ONE level of zoom
  - Include title, description for each element
  - Show communication protocol on relationship arrows
  - External systems in grey/different color
  - Boundary boxes for systems

Mermaid C4 syntax:
  C4Context, C4Container, C4Component, C4Deployment
  Person(), System(), System_Ext(), Container(), ContainerDb()
  Rel(from, to, "label", "protocol")
```

**Mermaid C4 Context Example:**
```mermaid
C4Context
    title System Context — Order Management System
    Person(customer, "Customer", "Registered user placing orders")
    Person(admin, "Admin", "Internal staff managing orders")
    System(oms, "Order Management", "Handles order lifecycle")
    System_Ext(payment, "Payment Gateway", "Processes payments")
    System_Ext(email, "Email Service", "Sends notifications")
    Rel(customer, oms, "Places orders", "HTTPS")
    Rel(admin, oms, "Manages orders", "HTTPS")
    Rel(oms, payment, "Charges customer", "HTTPS/API")
    Rel(oms, email, "Sends confirmation", "HTTPS")
```

---

### Sequence Diagram (interaction over time)

```
Use when: showing how components/actors interact in a specific scenario.
Strengths: clear temporal ordering, shows synchronous vs async, highlights round-trips.

Rules:
  - Show ONE use case scenario per diagram (not all scenarios in one)
  - Label all arrows with the operation/message name
  - Use activation bars for synchronous calls
  - Show return messages explicitly (dashed arrows)
  - Use alt/opt/loop for conditional flows

Anti-patterns:
  - Too many actors (> 6) — split into smaller diagrams
  - Showing all edge cases in one diagram — use separate diagrams
  - Missing return arrows — always show response
```

**Mermaid Sequence Example:**
```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant OrderService
    participant InventoryService
    participant PaymentGateway

    Customer->>OrderService: POST /orders {items, paymentToken}
    OrderService->>InventoryService: checkStock(items)
    InventoryService-->>OrderService: stockAvailable: true
    OrderService->>PaymentGateway: chargeCard(paymentToken, amount)
    PaymentGateway-->>OrderService: paymentConfirmed: {transactionId}
    OrderService-->>Customer: 201 Created {orderId}
```

---

### State Machine Diagram (object lifecycle)

```
Use when: showing all valid states an entity can be in and transitions between them.
Strengths: captures business rules about what transitions are allowed.

Rules:
  - Start state: filled circle (●)
  - End state: filled circle with ring (⊙)
  - Transitions labeled with: trigger [guard condition] / action
  - Every state should be reachable from start
  - Every non-terminal state should have at least one exit

Anti-patterns:
  - Missing guard conditions (ambiguous transitions)
  - No final state (infinite loop entity)
```

**Mermaid State Example:**
```mermaid
stateDiagram-v2
    [*] --> Pending : OrderPlaced
    Pending --> Confirmed : PaymentReceived
    Pending --> Cancelled : PaymentFailed / timeout
    Confirmed --> Shipped : FulfilmentCompleted
    Confirmed --> Cancelled : CustomerCancelled [before shipping]
    Shipped --> Delivered : DeliveryConfirmed
    Shipped --> ReturnRequested : CustomerReturns
    Delivered --> ReturnRequested : CustomerReturns [within 30 days]
    ReturnRequested --> Refunded : ReturnReceived
    Cancelled --> [*]
    Delivered --> [*]
    Refunded --> [*]
```

---

### Entity-Relationship Diagram (data model)

```
Use when: showing data model — tables, entities, and relationships.
Strengths: precise notation for cardinality, clear data ownership.

Cardinality notation (Chen / crow's foot):
  ||--|| : exactly one to exactly one
  ||--o{ : exactly one to zero-or-more
  }o--o{ : zero-or-more to zero-or-more
  ||--|{ : exactly one to one-or-more

Rules:
  - Every entity has a primary key attribute
  - Relationship lines include cardinality
  - Attribute names use domain language (not column names)
  - Foreign key relationships shown as lines, not as duplicate attributes
```

**Mermaid ER Example:**
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : "places"
    ORDER ||--|{ ORDER_ITEM : "contains"
    PRODUCT ||--o{ ORDER_ITEM : "included in"
    CUSTOMER {
        uuid id PK
        string email
        string name
        timestamp createdAt
    }
    ORDER {
        uuid id PK
        uuid customerId FK
        string status
        decimal total
        timestamp placedAt
    }
    ORDER_ITEM {
        uuid id PK
        uuid orderId FK
        uuid productId FK
        int quantity
        decimal unitPrice
    }
    PRODUCT {
        uuid id PK
        string name
        decimal price
        int stockQuantity
    }
```

---

### Activity / Flowchart (process flow)

```
Use when: showing decision logic, algorithmic flow, or business process steps.
Strengths: clear decision branches, parallelism notation.

Rules:
  - Start and end nodes clearly marked
  - Decision nodes (diamond) have labeled branches for each outcome
  - Parallel flows shown with fork/join bars
  - Use swimlanes to show who does what
```

**Mermaid Flowchart Example:**
```mermaid
flowchart TD
    A([Start: Order Received]) --> B{Inventory Check}
    B -->|Available| C[Reserve Inventory]
    B -->|Unavailable| D[Notify Customer: Out of Stock]
    D --> Z([End: Order Cancelled])
    C --> E{Payment Processing}
    E -->|Success| F[Confirm Order]
    E -->|Failure| G{Retry count < 3?}
    G -->|Yes| E
    G -->|No| H[Release Inventory]
    H --> I[Notify Customer: Payment Failed]
    I --> Z
    F --> J[Schedule Fulfilment]
    J --> K[Send Confirmation Email]
    K --> Z2([End: Order Confirmed])
```

---

### Data Flow Diagram (DFD)

```
Use when: showing how data moves through a system across processes and stores.
DFD uses a specific notation:
  External Entity: rectangle (data source/sink outside system)
  Process:         rounded rectangle or circle (transforms data)
  Data Store:      open-ended rectangle (persistent storage)
  Data Flow:       labeled arrow (data moving)

Levels:
  Level 0 (Context DFD): System as one process, all external entities, all data flows
  Level 1 (System DFD):  Explode main process into sub-processes
  Level 2:               Explode one sub-process further (only if needed)

Rules:
  - Data stores: data at rest (not processes)
  - Processes: always transform input to output (labeled as verb phrases)
  - All flows must be labeled with what data flows
  - External entities: actors or systems outside system boundary
```

**DFD in Mermaid (approximation using flowchart):**
```mermaid
flowchart LR
    Customer([Customer])
    Admin([Admin])
    subgraph "Order System"
        P1[Process Order]
        P2[Validate Payment]
        P3[Update Inventory]
        DS1[(Order Store)]
        DS2[(Product Store)]
    end
    PaymentGateway([Payment Gateway])

    Customer -->|"Order Request"| P1
    P1 -->|"Payment Details"| P2
    P2 -->|"Charge Request"| PaymentGateway
    PaymentGateway -->|"Payment Result"| P2
    P2 -->|"Confirmed Order"| DS1
    P1 -->|"Stock Query"| DS2
    DS2 -->|"Stock Level"| P1
    P2 -->|"Reserve Items"| P3
    P3 -->|"Updated Stock"| DS2
    Admin -->|"Inventory Update"| P3
    DS1 -->|"Order Confirmation"| Customer
```

---

### Context Map Diagram (domain relationships)

```
Use when: showing how bounded contexts relate to each other.
See domain-model.skill.md for context map patterns.
```

**Mermaid Context Map Example:**
```mermaid
graph TB
    subgraph "Order Management [U]"
        OM[Order Management]
    end
    subgraph "Identity [U]"
        IAM[Identity & Access]
    end
    subgraph "Payment [U]"
        PAY[Payment]
    end
    subgraph "Notification [D]"
        NOT[Notification]
    end
    subgraph "Catalog [U]"
        CAT[Product Catalog]
    end

    IAM -->|"OHS/PL\nUser Identity API"| OM
    CAT -->|"OHS/PL\nProduct API"| OM
    OM -->|"Customer/Supplier\nPayment Intent"| PAY
    OM -->|"OHS\nOrderEvent"| NOT
    PAY -->|"Published Language\nPaymentEvent"| NOT

    style OM fill:#dae8fc
    style IAM fill:#d5e8d4
    style PAY fill:#d5e8d4
    style CAT fill:#d5e8d4
    style NOT fill:#fff2cc
```

---

## Diagram Review Checklist

```
Before finalizing any diagram:
  □ Title: is there a clear, descriptive title?
  □ Scope: is it clear what's IN and what's OUTSIDE the diagram?
  □ Labels: are all elements and arrows labeled clearly?
  □ Legend: does the diagram need a legend for custom notation?
  □ Level: is this diagram one consistent level of abstraction?
  □ Audience: would the target reader understand it without explanation?
  □ Accuracy: does this match the actual system (not wishful thinking)?
  □ Completeness: are all significant elements shown?
  □ Clutter: is there anything that can be removed to improve clarity?
```

---

## Constraints

- One diagram = one question answered. Do not mix levels of abstraction.
- Diagrams must match reality — no aspirational architecture in current-state diagrams
- Prefer Mermaid for text-based portability (renders in GitHub, VS Code, Notion)
- If Mermaid can't represent the diagram type, describe in structured text with explicit notation
- Include diagram title and date — diagrams without metadata become unreliable
- Simple is better — if a diagram needs extensive explanation, simplify the diagram
