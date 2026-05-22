---
name: c4-documentation
description: C4 model architecture visualization and documentation
allowed-tools: Read, Glob, Grep, Write, Edit
---

# C4 Documentation Skill

Create architecture documentation using the C4 model's four levels of abstraction.

## MANDATORY: Documentation-First Approach

Before creating C4 documentation:

1. **Invoke `docs-management` skill** for C4 patterns
2. **Verify C4 model syntax** via MCP servers (context7 for Structurizr/Mermaid)
3. **Base guidance on c4model.com official documentation**

## C4 Model Overview

```text
C4 Model - Four Levels of Abstraction:

Level 1: System Context
┌─────────────────────────────────────────────────────────────────────────────┐
│  Shows the system in context with users and external systems                 │
│  Audience: Everyone (technical and non-technical)                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
Level 2: Container
┌─────────────────────────────────────────────────────────────────────────────┐
│  Shows high-level technology choices and responsibilities                    │
│  Audience: Technical people (inside and outside the team)                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
Level 3: Component
┌─────────────────────────────────────────────────────────────────────────────┐
│  Shows components within a container                                         │
│  Audience: Software architects and developers                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
Level 4: Code (Optional)
┌─────────────────────────────────────────────────────────────────────────────┐
│  Shows classes, interfaces, and implementation details                       │
│  Audience: Developers (often auto-generated)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Level 1: System Context Diagram

### Purpose

Shows the software system in the context of:

- Who uses it (people)
- What other systems it interacts with

### Mermaid Syntax

```mermaid
C4Context
    title System Context Diagram for [System Name]

    Person(customer, "Customer", "A customer who uses our platform")
    Person(admin, "Administrator", "System administrator")

    System(system, "System Name", "Allows customers to do X and Y")

    System_Ext(email, "Email System", "Sends transactional emails")
    System_Ext(payment, "Payment Gateway", "Processes payments")
    System_Ext(analytics, "Analytics Platform", "Tracks user behavior")

    Rel(customer, system, "Uses", "HTTPS")
    Rel(admin, system, "Manages", "HTTPS")
    Rel(system, email, "Sends emails using", "SMTP")
    Rel(system, payment, "Processes payments via", "HTTPS/REST")
    Rel(system, analytics, "Sends events to", "HTTPS")
```

### PlantUML/Structurizr DSL

```plantuml
@startuml
!include <C4/C4_Context>

title System Context Diagram for [System Name]

Person(customer, "Customer", "A customer who uses our platform")
Person(admin, "Administrator", "System administrator")

System(system, "System Name", "Allows customers to do X and Y")

System_Ext(email, "Email System", "Sends transactional emails")
System_Ext(payment, "Payment Gateway", "Processes payments")

Rel(customer, system, "Uses", "HTTPS")
Rel(admin, system, "Manages", "HTTPS")
Rel(system, email, "Sends emails using", "SMTP")
Rel(system, payment, "Processes payments via", "HTTPS")

@enduml
```

## Level 2: Container Diagram

### Purpose

Shows the high-level shape of the software architecture:

- Applications, data stores, microservices
- How they communicate
- Technology choices

### Mermaid Syntax

```mermaid
C4Container
    title Container Diagram for [System Name]

    Person(customer, "Customer", "End user")

    System_Boundary(system, "System Name") {
        Container(web, "Web Application", "Blazor", "Delivers the UI")
        Container(api, "API Gateway", "Kong", "Routes and secures APIs")
        Container(order, "Order Service", ".NET 10", "Handles order processing")
        Container(inventory, "Inventory Service", ".NET 10", "Manages stock")
        ContainerDb(db, "Database", "PostgreSQL", "Stores orders and inventory")
        ContainerQueue(queue, "Message Broker", "Kafka", "Async messaging")
    }

    Rel(customer, web, "Uses", "HTTPS")
    Rel(web, api, "Makes API calls", "HTTPS/JSON")
    Rel(api, order, "Routes to", "gRPC")
    Rel(api, inventory, "Routes to", "gRPC")
    Rel(order, db, "Reads/Writes", "TCP")
    Rel(inventory, db, "Reads/Writes", "TCP")
    Rel(order, queue, "Publishes events", "Kafka protocol")
    Rel(inventory, queue, "Subscribes to events", "Kafka protocol")
```

### Container Types

| Type | Usage | Example |
|------|-------|---------|
| `Container` | Application/service | API, web app, microservice |
| `ContainerDb` | Database | PostgreSQL, MongoDB, Redis |
| `ContainerQueue` | Message queue | Kafka, RabbitMQ, SQS |
| `Container_Ext` | External container | Third-party API hosted elsewhere |

## Level 3: Component Diagram

### Purpose

Shows the internal structure of a container:

- Major components and their responsibilities
- Interactions between components
- Technology implementation

### Mermaid Syntax

```mermaid
C4Component
    title Component Diagram for Order Service

    Container_Boundary(order, "Order Service") {
        Component(api, "API Controller", ".NET", "Handles HTTP requests")
        Component(handler, "Command Handlers", "MediatR", "Processes commands")
        Component(domain, "Domain Model", "C#", "Business logic and rules")
        Component(repo, "Repository", "EF Core", "Data access abstraction")
        Component(events, "Event Publisher", "MassTransit", "Publishes domain events")
    }

    ContainerDb(db, "Database", "PostgreSQL", "Stores order data")
    ContainerQueue(queue, "Message Broker", "Kafka", "Event transport")

    Rel(api, handler, "Dispatches to")
    Rel(handler, domain, "Uses")
    Rel(handler, repo, "Uses")
    Rel(handler, events, "Publishes via")
    Rel(repo, db, "Reads/Writes")
    Rel(events, queue, "Publishes to")
```

## Level 4: Code Diagram

### Purpose

Shows implementation details (usually auto-generated):

- Class diagrams
- Entity relationships
- Interface definitions

### When to Use

- Complex domain models
- Framework documentation
- Public API documentation

```mermaid
classDiagram
    class Order {
        +Guid Id
        +Guid CustomerId
        +OrderStatus Status
        +IReadOnlyList~LineItem~ Items
        +Money Total
        +AddItem(Product, int)
        +Submit()
        +Cancel()
    }

    class LineItem {
        +Guid ProductId
        +string ProductName
        +int Quantity
        +Money UnitPrice
        +Money Total
    }

    class OrderStatus {
        <<enumeration>>
        Draft
        Submitted
        Confirmed
        Shipped
        Delivered
        Cancelled
    }

    Order "1" *-- "*" LineItem
    Order --> OrderStatus
```

## Supplementary Diagrams

### Deployment Diagram

```mermaid
C4Deployment
    title Deployment Diagram for Production

    Deployment_Node(azure, "Azure Cloud", "Cloud Platform") {
        Deployment_Node(region, "East US", "Azure Region") {
            Deployment_Node(aks, "AKS Cluster", "Kubernetes 1.28") {
                Deployment_Node(ns, "production namespace") {
                    Container(api, "API Pods", "3 replicas")
                    Container(worker, "Worker Pods", "2 replicas")
                }
            }
            Deployment_Node(data, "Data Services") {
                ContainerDb(db, "Azure PostgreSQL", "Flexible Server")
                ContainerDb(redis, "Azure Redis", "Premium tier")
            }
        }
    }

    Rel(api, db, "Connects to", "TCP/5432")
    Rel(api, redis, "Caches with", "TCP/6379")
```

### Dynamic Diagram (Sequence)

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web App
    participant A as API Gateway
    participant O as Order Service
    participant D as Database

    U->>W: Click "Place Order"
    W->>A: POST /api/orders
    A->>O: CreateOrder
    O->>D: INSERT order
    D-->>O: Order created
    O-->>A: OrderCreated
    A-->>W: 201 Created
    W-->>U: Order confirmation
```

## C4 Documentation Template

```markdown
# C4 Architecture Documentation: [System Name]

## 1. System Context

### Diagram

[Level 1 Context Diagram]

### Description

[Narrative explaining the context]

### Actors and External Systems

| Element | Type | Description |
|---------|------|-------------|
| [Name] | Person | [Description] |
| [Name] | External System | [Description] |

---

## 2. Container View

### Diagram

[Level 2 Container Diagram]

### Container Catalog

| Container | Technology | Responsibility |
|-----------|------------|----------------|
| [Name] | [Tech] | [What it does] |

---

## 3. Component Views

### 3.1 [Container Name] Components

#### Diagram

[Level 3 Component Diagram]

#### Component Catalog

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| [Name] | [Tech] | [What it does] |

---

## 4. Deployment View

### Diagram

[Deployment Diagram]

### Infrastructure Elements

| Element | Technology | Purpose |
|---------|------------|---------|
| [Name] | [Tech] | [Purpose] |

---

## 5. Key Scenarios

### 5.1 [Scenario Name]

[Dynamic/Sequence Diagram]

[Narrative description]
```

## C# Model for C4 Elements

```csharp
// C4 Model Elements
public abstract record C4Element
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public string? Technology { get; init; }
}

public sealed record Person : C4Element
{
    public string? Role { get; init; }
}

public sealed record SoftwareSystem : C4Element
{
    public bool IsExternal { get; init; }
    public IReadOnlyList<Container> Containers { get; init; } = [];
}

public sealed record Container : C4Element
{
    public required ContainerType Type { get; init; }
    public IReadOnlyList<Component> Components { get; init; } = [];
}

public enum ContainerType
{
    WebApplication,
    MobileApp,
    DesktopApp,
    Service,
    Database,
    FileSystem,
    MessageBroker,
    Cache
}

public sealed record Component : C4Element
{
    public string? Interface { get; init; }
}

public sealed record Relationship
{
    public required string SourceId { get; init; }
    public required string DestinationId { get; init; }
    public required string Description { get; init; }
    public string? Technology { get; init; }
}

// C4 Diagram Generator
public interface IC4DiagramGenerator
{
    string GenerateContextDiagram(
        SoftwareSystem system,
        IEnumerable<Person> people,
        IEnumerable<SoftwareSystem> externalSystems,
        IEnumerable<Relationship> relationships);

    string GenerateContainerDiagram(
        SoftwareSystem system,
        IEnumerable<Relationship> relationships);

    string GenerateComponentDiagram(
        Container container,
        IEnumerable<Relationship> relationships);
}
```

## Best Practices

### Do's

- Keep diagrams simple and focused
- Use consistent notation and colors
- Include a legend when needed
- Update diagrams when architecture changes
- Use automated generation where possible

### Don'ts

- Don't show every component on every diagram
- Don't mix abstraction levels
- Don't forget the narrative description
- Don't create diagrams that never get updated

## Workflow

When creating C4 documentation:

1. **Start with Context**: Level 1 shows the big picture
2. **Zoom into Containers**: Level 2 shows technology choices
3. **Detail as Needed**: Level 3 for complex containers
4. **Add Scenarios**: Dynamic diagrams for key flows
5. **Include Deployment**: Show infrastructure mapping
6. **Maintain Currency**: Keep diagrams synchronized with code

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
