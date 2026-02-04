---
name: acc-mermaid-template
description: Generates Mermaid diagrams for technical documentation. Provides templates for flowcharts, sequence diagrams, class diagrams, ER diagrams, and C4 models.
---

# Mermaid Diagram Template Generator

Generate Mermaid diagrams for technical documentation.

## Diagram Templates

### Flowchart - Basic

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### Flowchart - Process

```mermaid
flowchart LR
    subgraph Input
        A[Request]
    end

    subgraph Processing
        B[Validate]
        C[Transform]
        D[Store]
    end

    subgraph Output
        E[Response]
    end

    A --> B --> C --> D --> E
```

### Flowchart - Architecture Layers

```mermaid
flowchart TB
    subgraph presentation[Presentation Layer]
        direction LR
        AC[Action]
        RS[Responder]
    end

    subgraph application[Application Layer]
        direction LR
        UC[UseCase]
        DTO[DTO]
    end

    subgraph domain[Domain Layer]
        direction LR
        EN[Entity]
        VO[ValueObject]
        EV[Event]
    end

    subgraph infrastructure[Infrastructure Layer]
        direction LR
        RP[Repository]
        AD[Adapter]
    end

    presentation --> application
    application --> domain
    infrastructure -.-> domain
```

### Sequence - Basic

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database

    C->>S: Request
    S->>D: Query
    D-->>S: Result
    S-->>C: Response
```

### Sequence - With Authentication

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Auth
    participant S as Service
    participant D as Database

    C->>A: Login(credentials)
    A->>D: Verify user
    D-->>A: User data
    A-->>C: JWT Token

    C->>S: Request + Token
    S->>A: Validate token
    A-->>S: Token valid
    S->>D: Query
    D-->>S: Data
    S-->>C: Response
```

### Sequence - With Error Handling

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Service
    participant D as Database

    C->>S: Create order

    alt Valid request
        S->>D: INSERT order
        D-->>S: order_id
        S-->>C: 201 Created
    else Validation error
        S-->>C: 400 Bad Request
    else Database error
        S->>D: INSERT order
        D-->>S: Error
        S-->>C: 500 Internal Error
    end
```

### Sequence - Async with Queue

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant Q as Queue
    participant W as Worker
    participant D as Database

    C->>A: POST /jobs
    A->>D: Create job (pending)
    A->>Q: Publish job
    A-->>C: 202 Accepted {job_id}

    W->>Q: Consume job
    W->>D: Update job (processing)
    W->>W: Process
    W->>D: Update job (completed)
```

### Class - Domain Model

```mermaid
classDiagram
    class Order {
        <<aggregate root>>
        -OrderId id
        -CustomerId customerId
        -OrderStatus status
        -Money total
        +confirm() void
        +cancel() void
        +ship() void
    }

    class OrderItem {
        <<entity>>
        -OrderItemId id
        -ProductId productId
        -Quantity quantity
        -Money price
    }

    class OrderStatus {
        <<enumeration>>
        PENDING
        CONFIRMED
        SHIPPED
        CANCELLED
    }

    class Money {
        <<value object>>
        -int cents
        -string currency
        +add(Money) Money
        +equals(Money) bool
    }

    Order "1" *-- "*" OrderItem : contains
    Order --> OrderStatus : has
    Order --> Money : total
    OrderItem --> Money : price
```

### Class - Repository Pattern

```mermaid
classDiagram
    class OrderRepositoryInterface {
        <<interface>>
        +findById(OrderId id) Order
        +save(Order order) void
        +delete(OrderId id) void
    }

    class DoctrineOrderRepository {
        -EntityManager em
        +findById(OrderId id) Order
        +save(Order order) void
        +delete(OrderId id) void
    }

    class InMemoryOrderRepository {
        -array orders
        +findById(OrderId id) Order
        +save(Order order) void
        +delete(OrderId id) void
    }

    OrderRepositoryInterface <|.. DoctrineOrderRepository
    OrderRepositoryInterface <|.. InMemoryOrderRepository
```

### ER - Database Schema

```mermaid
erDiagram
    users ||--o{ orders : places
    orders ||--|{ order_items : contains
    order_items }o--|| products : references

    users {
        uuid id PK
        varchar email UK
        varchar name
        timestamp created_at
    }

    orders {
        uuid id PK
        uuid user_id FK
        varchar status
        int total_cents
        varchar currency
        timestamp created_at
    }

    order_items {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        int price_cents
    }

    products {
        uuid id PK
        varchar name
        varchar sku UK
        int price_cents
        varchar currency
    }
```

### State - Entity Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Draft : create()

    Draft --> Pending : submit()
    Draft --> [*] : delete()

    Pending --> Approved : approve()
    Pending --> Rejected : reject()
    Pending --> Draft : requestChanges()

    Approved --> Published : publish()
    Approved --> Draft : unpublish()

    Rejected --> Draft : revise()
    Rejected --> [*] : delete()

    Published --> Archived : archive()
    Published --> Draft : unpublish()

    Archived --> [*]
```

### C4 - Context Diagram

```mermaid
flowchart TB
    subgraph boundary[System Boundary]
        S[("📦 Order Management System\n\nManages customer orders\nand inventory")]
    end

    C[("👤 Customer\n\nPlaces and tracks orders")]
    A[("👤 Admin\n\nManages products\nand orders")]
    P[("💳 Payment Gateway\n\nProcesses payments")]
    E[("📧 Email Service\n\nSends notifications")]
    W[("🚚 Warehouse\n\nFulfills orders")]

    C -->|"Browse, Order, Track"| S
    A -->|"Manage"| S
    S -->|"Process payment"| P
    S -->|"Send emails"| E
    S -->|"Ship orders"| W
```

### C4 - Container Diagram

```mermaid
flowchart TB
    subgraph boundary[Order Management System]
        WA[("🌐 Web App\nReact SPA")]
        API[("⚙️ API\nPHP/Symfony")]
        WRK[("⚡ Worker\nPHP")]
        DB[("🗄️ Database\nPostgreSQL")]
        CACHE[("💾 Cache\nRedis")]
        Q[("📬 Queue\nRabbitMQ")]
    end

    C[("👤 Customer")]
    P[("💳 Payment")]
    E[("📧 Email")]

    C -->|"HTTPS"| WA
    WA -->|"REST/JSON"| API
    API -->|"SQL"| DB
    API -->|"Cache"| CACHE
    API -->|"Publish"| Q
    WRK -->|"Consume"| Q
    WRK -->|"SQL"| DB
    API -->|"HTTPS"| P
    WRK -->|"SMTP"| E
```

### CQRS Flow

```mermaid
flowchart LR
    subgraph commands[Write Side]
        CMD[Command] --> CH[Handler]
        CH --> AG[Aggregate]
        AG --> ES[Event Store]
    end

    subgraph events[Event Bus]
        ES --> EB[Event Bus]
    end

    subgraph queries[Read Side]
        EB --> PR[Projector]
        PR --> RM[Read Model]
        Q[Query] --> QH[Handler]
        QH --> RM
    end
```

## Node Shapes Reference

```mermaid
flowchart LR
    A[Rectangle] --> B(Rounded)
    B --> C{Diamond}
    C --> D([Stadium])
    D --> E[(Database)]
    E --> F((Circle))
    F --> G>Asymmetric]
    G --> H{{Hexagon}}
```

## Arrow Reference

```mermaid
flowchart LR
    A1 --> B1
    A2 --- B2
    A3 -.-> B3
    A4 ==> B4
    A5 --o B5
    A6 --x B6
    A7 <--> B7
    A8 -->|label| B8
```

## Styling

```mermaid
flowchart LR
    A[Start]:::green --> B[Process]:::blue --> C[End]:::red

    classDef green fill:#9f6,stroke:#333,stroke-width:2px
    classDef blue fill:#69f,stroke:#333,stroke-width:2px
    classDef red fill:#f66,stroke:#333,stroke-width:2px
```

## Generation Instructions

When generating Mermaid diagrams:

1. **Choose appropriate type** based on what you're showing
2. **Limit to 7±2 elements** per diagram
3. **Use descriptive labels** (not A, B, C)
4. **Add subgraphs** for grouping
5. **Show direction** of flow/dependencies
6. **Include legend** if using custom styles
7. **Test rendering** before finalizing
