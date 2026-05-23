---
name: architecture-patterns
description: Provides architectural pattern knowledge for designing feature implementations including MVC, event-driven, microservices, and CQRS patterns. Use when designing system architecture or choosing implementation patterns.
dependencies: []
---

# Architecture Patterns

This skill provides knowledge about common architectural patterns to help design feature implementations. Apply these patterns based on the project's existing architecture and the feature's requirements.

## Diagram Convention

Architecture visualizations use Mermaid syntax with `classDef` styling (`color:#000` for text readability). When creating architecture visualizations based on these patterns, follow the technical-diagrams skill conventions.

## Pattern Selection Guide

Choose patterns based on:
1. **Existing architecture** - Match what's already in use
2. **Team familiarity** - Use patterns the team knows
3. **Feature requirements** - Some patterns fit better for certain features
4. **Scale requirements** - Consider current and future scale

---

## Layered Architecture (N-Tier)

**When to use:** Most web applications, CRUD operations, clear separation of concerns needed

**Layers:**
```mermaid
flowchart TD
    A["Presentation Layer — UI, API endpoints, controllers"]:::primary
    B["Application Layer — Use cases, orchestration, DTOs"]:::secondary
    C["Domain Layer — Business logic, entities, rules"]:::success
    D["Infrastructure Layer — Database, external services, I/O"]:::neutral
    A --> B --> C --> D

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000
```

**Key rules:**
- Dependencies flow downward only
- Each layer only talks to the layer directly below
- Domain layer has no external dependencies

**Implementation tips:**
- Use interfaces at layer boundaries
- Keep domain logic in the domain layer, not controllers
- Use DTOs to transfer data between layers

---

## MVC (Model-View-Controller)

**When to use:** Web applications with server-rendered views, simple CRUD apps

**Components:**
```mermaid
flowchart LR
    U1[User]:::neutral -->|input| CT[Controller]:::primary
    CT -->|updates| M[Model]:::secondary
    M -->|reads| CT
    CT -->|renders| V[View]:::success
    V -->|response| U2[User]:::neutral

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000
```

**Model:** Data and business logic
**View:** Presentation/UI
**Controller:** Handles input, coordinates model and view

**Implementation tips:**
- Keep controllers thin - delegate to services
- Models should be framework-agnostic when possible
- Views should have minimal logic

---

## Repository Pattern

**When to use:** Data access abstraction, testability, multiple data sources

**Structure:**
```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<void>;
}

class PostgresUserRepository implements UserRepository {
  // Implementation using PostgreSQL
}

class InMemoryUserRepository implements UserRepository {
  // Implementation for testing
}
```

**Benefits:**
- Abstracts data access details
- Easy to swap implementations
- Simplifies testing with in-memory implementations

---

## Service Layer Pattern

**When to use:** Complex business logic, multiple entry points (API, CLI, queue)

**Structure:**
```typescript
class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService,
    private logger: Logger
  ) {}

  async registerUser(data: RegisterDTO): Promise<User> {
    // Validation
    // Business logic
    // Coordination of multiple repositories/services
    // Return result
  }
}
```

**Implementation tips:**
- Services contain business logic, not controllers
- One service per domain concept
- Services can call other services (but avoid cycles)

---

## Event-Driven Architecture

**When to use:** Decoupled components, async processing, audit trails, notifications

**Patterns:**

### Event Emitter (Simple)
```typescript
// Emit events for side effects
userService.on('userCreated', async (user) => {
  await emailService.sendWelcome(user);
  await analyticsService.trackSignup(user);
});
```

### Message Queue (Distributed)
```mermaid
flowchart LR
    P[Producer]:::primary --> Q[Queue]:::warning
    Q --> C1[Consumer 1]:::secondary
    Q --> C2[Consumer 2]:::secondary

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef warning fill:#fef3c7,stroke:#d97706,color:#000
```

**Event structure:**
```typescript
interface DomainEvent {
  type: string;
  timestamp: Date;
  payload: unknown;
  metadata: {
    correlationId: string;
    causationId: string;
  };
}
```

**Implementation tips:**
- Events should be immutable
- Include enough context to process without additional queries
- Handle idempotency for at-least-once delivery

---

## CQRS (Command Query Responsibility Segregation)

**When to use:** Complex domains, different read/write patterns, high-performance reads needed

**Structure:**
```mermaid
flowchart TD
    subgraph write["Commands (Write)"]
        CMD[Command]:::primary --> CH[Command Handler]:::secondary
        CH --> WM[Write Model]:::secondary
        WM --> WDB[Write Database]:::neutral
    end
    subgraph read["Queries (Read)"]
        QRY[Query]:::primary --> QH[Query Handler]:::secondary
        QH --> RM[Read Model]:::secondary
        RM --> RDB[Read Database]:::neutral
    end

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000

    style write fill:#f8fafc,stroke:#94a3b8,color:#000
    style read fill:#f8fafc,stroke:#94a3b8,color:#000
```

**Simplified CQRS:**
```typescript
// Commands modify state
class CreateUserCommand {
  execute(data: CreateUserDTO): Promise<void>
}

// Queries return data without modification
class GetUserQuery {
  execute(id: string): Promise<UserDTO>
}
```

**Implementation tips:**
- Start simple - same database, different models
- Use for complex domains where read/write models differ
- Consider eventual consistency implications

---

## Ports and Adapters (Hexagonal)

**When to use:** High testability needs, multiple I/O channels, long-lived applications

**Structure:**
```mermaid
flowchart TD
    subgraph driving["Driving Adapters"]
        H[HTTP]:::primary
        CL[CLI]:::primary
        Q[Queue]:::primary
        T[Timer]:::primary
    end
    subgraph core["Application Core"]
        subgraph domain["Domain Logic"]
            DL[Business Rules]:::success
        end
    end
    subgraph driven["Driven Adapters"]
        DB[Database]:::neutral
        CA[Cache]:::neutral
        EM[Email]:::neutral
        API[External API]:::neutral
    end
    H -->|port| DL
    CL -->|port| DL
    Q -->|port| DL
    T -->|port| DL
    DL -->|port| DB
    DL -->|port| CA
    DL -->|port| EM
    DL -->|port| API

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000

    style driving fill:#f8fafc,stroke:#94a3b8,color:#000
    style core fill:#fefce8,stroke:#ca8a04,color:#000
    style domain fill:#dcfce7,stroke:#16a34a,color:#000
    style driven fill:#f8fafc,stroke:#94a3b8,color:#000
```

**Key concept:** Business logic at center, all I/O through ports/adapters

**Implementation tips:**
- Define ports (interfaces) for all external interactions
- Adapters implement ports for specific technologies
- Domain code never imports adapter code

---

## Microservices Patterns

**When to use:** Large teams, independent deployability, different scaling needs

### API Gateway
Single entry point that routes to services

### Service Discovery
Services register themselves, clients look them up

### Circuit Breaker
Prevent cascade failures when services are down
```typescript
const breaker = new CircuitBreaker(remoteService.call, {
  timeout: 3000,
  errorThreshold: 50,
  resetTimeout: 30000
});
```

### Saga Pattern
Coordinate transactions across services
```mermaid
flowchart LR
    SA[Service A]:::primary -->|step 1| SB[Service B]:::primary -->|step 2| SC[Service C]:::primary
    SC -.->|failure| CC[Compensate C]:::danger
    CC -.-> CB[Compensate B]:::danger
    CB -.-> CA[Compensate A]:::danger

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef danger fill:#fee2e2,stroke:#dc2626,color:#000
```

---

## Choosing the Right Pattern

| Scenario | Recommended Pattern |
|----------|---------------------|
| Simple CRUD app | MVC + Repository |
| Complex business logic | Layered + Service Layer |
| Need audit trail | Event-Driven |
| High read/write disparity | CQRS |
| Maximum testability | Hexagonal |
| Multiple teams/services | Microservices patterns |

## Anti-Patterns to Avoid

1. **Big Ball of Mud** - No clear structure
2. **God Object** - One class does everything
3. **Spaghetti Code** - Tangled dependencies
4. **Golden Hammer** - Using one pattern for everything
5. **Premature Optimization** - Complex patterns for simple needs

## Application Guidelines

1. **Match existing architecture** - Don't introduce new patterns unnecessarily
2. **Start simple** - Add complexity only when needed
3. **Document decisions** - Explain why a pattern was chosen
4. **Consider team skills** - A simpler pattern well-executed beats a complex one poorly understood

## Integration Notes

**What this component does:** Provides architectural pattern knowledge (MVC, layered, event-driven, CQRS, hexagonal, microservices) for designing feature implementations.

**Capabilities needed:**
- File reading (to understand existing codebase architecture)

**Adaptation guidance:**
- This is a pure reference/knowledge skill with no external dependencies
- Loaded by the **feature-dev** skill during its architecture design phase
- Mermaid diagrams follow the technical-diagrams conventions (dark text on nodes)
