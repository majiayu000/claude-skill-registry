---
name: technical-diagrams
description: >-
  Provides Mermaid diagram syntax, best practices, and styling rules for technical
  visualizations. Use when creating diagrams, flowcharts, sequence diagrams, class
  diagrams, state diagrams, ER diagrams, architecture diagrams, C4 diagrams,
  visualizations, or any visual documentation in markdown. Always use this skill
  when generating or updating Mermaid code blocks.
dependencies: []
---

# Technical Diagrams

Mermaid is the standard for all technical diagrams in this project. It renders natively in GitHub, GitLab, MkDocs (with Material theme), and most modern documentation platforms.

This skill provides:
- **Critical styling rules** to ensure readability (especially color contrast)
- **Quick reference** examples for common diagram types
- **Reference files** for advanced syntax when building complex diagrams

Always wrap Mermaid code in fenced code blocks with the `mermaid` language identifier.

---

## Why Mermaid

**Native rendering** -- GitHub, GitLab, Notion, MkDocs, and Docusaurus render Mermaid blocks without plugins or build steps. No external image generation tools needed.

**Text-based and diffable** -- Diagrams live alongside code in version control. Changes appear in pull request diffs, making reviews straightforward and history trackable.

**No external tools** -- No Lucidchart exports, no draw.io XML files, no PNG screenshots that go stale. The diagram source is the single source of truth.

**Maintainable** -- Updating a diagram means editing text, not wrestling with a GUI. Refactoring a component name? Find-and-replace works on diagrams too.

**Consistent** -- A shared syntax produces visually consistent diagrams across all documentation, regardless of who authored them.

---

## Critical Styling Rules

**This is the most important section.** Light text on light backgrounds is the most common Mermaid readability issue. Follow these rules strictly.

### Rule 1: Always use dark text on nodes

Every node must have `color:#000` (or another dark color like `#1a1a1a`, `#333`). Never use white, light gray, or any light-colored text.

### Rule 2: Use `classDef` for consistent styling

Define reusable styles at the bottom of the diagram and apply them with `:::` syntax:

```mermaid
flowchart LR
    A[Input]:::primary --> B[Process]:::secondary --> C[Output]:::success

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
```

### Rule 3: Safe color palettes

Use these pre-tested combinations that guarantee readability:

| Style Name | Fill | Stroke | Text | Use For |
|-----------|------|--------|------|---------|
| `primary` | `#dbeafe` | `#2563eb` | `#000` | Main components, entry points |
| `secondary` | `#f3e8ff` | `#7c3aed` | `#000` | Supporting components |
| `success` | `#dcfce7` | `#16a34a` | `#000` | Success states, outputs |
| `warning` | `#fef3c7` | `#d97706` | `#000` | Warnings, caution areas |
| `danger` | `#fee2e2` | `#dc2626` | `#000` | Errors, critical items |
| `neutral` | `#f3f4f6` | `#6b7280` | `#000` | Background, inactive items |

### Bad vs Good

**Bad -- light text is invisible on light background:**
```
classDef bad fill:#dbeafe,stroke:#2563eb,color:#93c5fd
```

**Good -- dark text is always readable:**
```
classDef good fill:#dbeafe,stroke:#2563eb,color:#000
```

---

## Supported Diagram Types

| Diagram Type | Mermaid Keyword | Use Case | Reference |
|-------------|----------------|----------|-----------|
| Flowchart | `flowchart` | Process flows, decision trees, pipelines | See **Flowcharts** section below |
| Sequence | `sequenceDiagram` | API interactions, message passing, protocols | See **references/sequence-diagrams.md** |
| Class | `classDiagram` | Object models, interfaces, relationships | See **references/class-diagrams.md** |
| State | `stateDiagram-v2` | State machines, lifecycle management | See **references/state-diagrams.md** |
| ER | `erDiagram` | Database schemas, entity relationships | See **references/er-diagrams.md** |
| C4 | `C4Context` / `C4Container` / etc. | System architecture, containers, components | See **C4 Diagrams** section below |

---

## Quick Reference

Minimal copy-paste examples for simple diagrams. For complex use cases, load the corresponding reference file.

### Flowchart

```mermaid
flowchart TD
    A[Start]:::primary --> B{Decision}:::neutral
    B -->|Yes| C[Action A]:::success
    B -->|No| D[Action B]:::warning
    C --> E[End]:::primary
    D --> E

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
    classDef warning fill:#fef3c7,stroke:#d97706,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database

    C->>S: POST /api/resource
    activate S
    S->>D: INSERT INTO resources
    D-->>S: OK
    S-->>C: 201 Created
    deactivate S
```

### Class Diagram

```mermaid
classDiagram
    class Service {
        -repository: Repository
        +create(data: CreateDTO): Entity
        +findById(id: string): Entity
    }
    class Repository {
        <<interface>>
        +save(entity: Entity): void
        +findById(id: string): Entity
    }
    Service --> Repository : uses
```

### State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : submit
    Review --> Approved : approve
    Review --> Draft : reject
    Approved --> Published : publish
    Published --> [*]
```

### ER Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "appears in"

    USER {
        int id PK
        string email UK
        string name
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
    }
```

### C4 Context Diagram

```mermaid
C4Context
    title System Context Diagram

    Person(user, "User", "End user of the system")
    System(system, "Application", "Main system under design")
    System_Ext(ext, "External API", "Third-party service")

    Rel(user, system, "Uses", "HTTPS")
    Rel(system, ext, "Calls", "REST API")
```

---

## Styling and Theming

### `classDef` -- Reusable Style Classes

Define once, apply to many nodes:

```mermaid
flowchart LR
    A[Node A]:::primary --> B[Node B]:::secondary

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
```

### `:::` Shorthand -- Apply Class Inline

```
A[Label]:::className
```

### `style` -- One-Off Inline Styling

For single-node overrides (prefer `classDef` for consistency):

```
style nodeId fill:#dbeafe,stroke:#2563eb,color:#000
```

### Standard Style Classes

Define these at the bottom of any diagram that uses multiple styles:

```
classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
classDef success fill:#dcfce7,stroke:#16a34a,color:#000
classDef warning fill:#fef3c7,stroke:#d97706,color:#000
classDef danger fill:#fee2e2,stroke:#dc2626,color:#000
classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000
```

### Subgraph Styling

Subgraphs can be styled via `style` directives:

```mermaid
flowchart LR
    subgraph backend["Backend Services"]
        A[API]:::primary --> B[Worker]:::secondary
    end
    style backend fill:#f8fafc,stroke:#94a3b8,color:#000
```

### Edge Styling with `linkStyle`

Style specific edges by their index (0-based, in order of definition):

```
linkStyle 0 stroke:#2563eb,stroke-width:2px
linkStyle 1 stroke:#dc2626,stroke-width:2px,stroke-dasharray:5
```

---

## Best Practices

### Keep diagrams focused
Limit to 15-20 nodes maximum. If a diagram grows beyond that, split it into multiple diagrams or use subgraphs to manage complexity.

### Choose direction deliberately
- **TD (top-down)** -- Hierarchies, data flow, process steps
- **LR (left-right)** -- Timelines, pipelines, request flows
- **BT (bottom-up)** -- Dependency trees (leaves at top)
- **RL (right-left)** -- Rarely used, avoid unless it matches a specific mental model

### Use meaningful labels
```
A[User Service] --> B[Auth Service]    %% Good: descriptive
A --> B                                 %% Bad: meaningless
```

### Label edges
```
A -->|validates| B    %% Good: explains the relationship
A --> B               %% Acceptable only if the relationship is obvious
```

### Group with subgraphs
Use subgraphs to visually separate layers, domains, or subsystems:

```mermaid
flowchart TD
    subgraph frontend["Frontend"]
        A[React App]:::primary
    end
    subgraph backend["Backend"]
        B[API Server]:::secondary --> C[Database]:::neutral
    end
    A --> B

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000
```

### Use consistent arrow types
Within a single diagram, stick to one arrow style unless you need to distinguish different relationship types:
- `-->` solid arrow (primary flow)
- `-.->` dotted arrow (optional or async)
- `==>` thick arrow (critical path)

### Prefer `flowchart` over `graph`
`flowchart` is the modern syntax with more features (subgraph styling, `:::` shorthand, more shapes). `graph` is legacy -- use `flowchart` for all new diagrams.

### Platform compatibility
- GitHub/GitLab: Full support for flowcharts, sequence, class, state, ER, Gantt, pie
- C4 diagrams: Require Mermaid 10.6+ -- verify platform support before using
- MkDocs: Requires `pymdownx.superfences` with custom Mermaid fence config

---

## When to Load Reference Files

**Simple diagrams** -- The quick reference above is sufficient. Use it for:
- Basic flowcharts with fewer than 10 nodes
- Simple sequence diagrams with 2-3 participants
- Standard ER diagrams with straightforward relationships

**Complex or unfamiliar diagrams** -- Load the reference file when:
- Using advanced features (composite states, parallel blocks, fork/join)
- Building class diagrams with generics, namespaces, or cardinality
- Needing the full set of node shapes, arrow types, or relationship notations
- Working with a diagram type for the first time

**C4 diagrams** -- Always review the C4 section below. C4 uses a unique function-call syntax (`Person()`, `System()`, `Container()`, etc.) that differs significantly from other Mermaid diagrams.

---

## Flowcharts Reference

Flowcharts visualize process flows, decision trees, pipelines, and system architectures. They are the most versatile Mermaid diagram type.

**Keyword:** `flowchart` (prefer over legacy `graph`)

### Direction Keywords

| Keyword | Direction | Best For |
|---------|-----------|----------|
| `TD` / `TB` | Top to bottom | Hierarchies, process steps |
| `LR` | Left to right | Pipelines, request flows, timelines |
| `BT` | Bottom to top | Dependency trees |
| `RL` | Right to left | Rarely used |

```mermaid
flowchart LR
    A --> B --> C
```

### Node Shapes

| Syntax | Shape | Use For |
|--------|-------|---------|
| `A[Text]` | Rectangle | Default, general purpose |
| `A(Text)` | Rounded rectangle | Processes, steps |
| `A([Text])` | Stadium | Start/end points |
| `A[[Text]]` | Subroutine | External processes |
| `A[(Text)]` | Cylinder | Databases, storage |
| `A((Text))` | Circle | Connectors, small nodes |
| `A{Text}` | Diamond | Decisions, conditions |
| `A{{Text}}` | Hexagon | Preparation steps |
| `A>Text]` | Asymmetric | Flags, signals |
| `A[/Text/]` | Parallelogram | Input/output |
| `A[\Text\]` | Alt parallelogram | Alt input/output |
| `A[/Text\]` | Trapezoid | Transforms |
| `A[\Text/]` | Alt trapezoid | Alt transforms |
| `A(((Text)))` | Double circle | Critical nodes |

### Edge Types

#### Solid Edges

| Syntax | Description |
|--------|-------------|
| `A --> B` | Arrow |
| `A --- B` | Line (no arrow) |
| `A -->\|label\| B` | Arrow with label |
| `A --label--> B` | Arrow with label (alt) |

#### Dotted Edges

| Syntax | Description |
|--------|-------------|
| `A -.-> B` | Dotted arrow |
| `A -.- B` | Dotted line |
| `A -.->\|label\| B` | Dotted arrow with label |

#### Thick Edges

| Syntax | Description |
|--------|-------------|
| `A ==> B` | Thick arrow |
| `A === B` | Thick line |
| `A ==>\|label\| B` | Thick arrow with label |

#### Multi-Directional

| Syntax | Description |
|--------|-------------|
| `A <--> B` | Bidirectional arrow |
| `A o--o B` | Circle endpoints |
| `A x--x B` | Cross endpoints |

#### Edge Length

Add extra dashes/dots/equals to make edges longer:
- `A ---> B` (longer than `A --> B`)
- `A -----> B` (even longer)

### Subgraphs

Group related nodes into labeled regions:

```mermaid
flowchart TD
    subgraph frontend["Frontend Layer"]
        A[React App] --> B[State Manager]
    end
    subgraph backend["Backend Layer"]
        C[API Server] --> D[Database]
    end
    B --> C
```

#### Nested Subgraphs

```mermaid
flowchart TD
    subgraph cloud["Cloud Infrastructure"]
        subgraph compute["Compute"]
            A[App Server]
        end
        subgraph storage["Storage"]
            B[Object Store]
        end
    end
    A --> B
```

#### Subgraph Direction

Override direction inside a subgraph:

```
subgraph section["Section"]
    direction LR
    A --> B --> C
end
```

### Flowchart Styling

#### classDef and :::

```mermaid
flowchart LR
    A[Input]:::primary --> B[Process]:::secondary --> C[Output]:::success

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
```

#### Inline style

```
style A fill:#dbeafe,stroke:#2563eb,color:#000
```

#### Subgraph styling

```
style subgraphId fill:#f8fafc,stroke:#94a3b8,color:#000
```

#### linkStyle

Style edges by their 0-based index (order of definition):

```
linkStyle 0 stroke:#2563eb,stroke-width:2px
linkStyle 1 stroke:#dc2626,stroke-dasharray:5
```

#### Apply class to multiple nodes

```
class A,B,C primary
```

### Flowchart Examples

#### CI/CD Pipeline

```mermaid
flowchart LR
    A([Push]):::neutral --> B[Lint]:::primary
    B --> C[Test]:::primary
    C --> D{Pass?}:::neutral
    D -->|Yes| E[Build]:::primary
    D -->|No| F[Notify]:::danger
    E --> G[Deploy Staging]:::warning
    G --> H{Approve?}:::neutral
    H -->|Yes| I[Deploy Prod]:::success
    H -->|No| J[Rollback]:::danger

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
    classDef warning fill:#fef3c7,stroke:#d97706,color:#000
    classDef danger fill:#fee2e2,stroke:#dc2626,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000
```

#### Layered Architecture

```mermaid
flowchart TD
    subgraph presentation["Presentation Layer"]
        direction LR
        A[Web UI]:::primary
        B[Mobile App]:::primary
        C[CLI]:::primary
    end

    subgraph application["Application Layer"]
        direction LR
        D[Auth Service]:::secondary
        E[User Service]:::secondary
        F[Order Service]:::secondary
    end

    subgraph data["Data Layer"]
        direction LR
        G[(PostgreSQL)]:::neutral
        H[(Redis Cache)]:::neutral
        I[(S3 Storage)]:::neutral
    end

    A & B & C --> D & E & F
    D --> G
    E --> G & H
    F --> G & I

    classDef primary fill:#dbeafe,stroke:#2563eb,color:#000
    classDef secondary fill:#f3e8ff,stroke:#7c3aed,color:#000
    classDef neutral fill:#f3f4f6,stroke:#6b7280,color:#000

    style presentation fill:#eff6ff,stroke:#93c5fd,color:#000
    style application fill:#f5f3ff,stroke:#c4b5fd,color:#000
    style data fill:#f9fafb,stroke:#d1d5db,color:#000
```

---

## C4 Diagrams Reference

C4 diagrams model software architecture at multiple zoom levels -- from system context down to individual components. C4 uses a unique function-call syntax that differs from other Mermaid diagram types.

**Keywords:** `C4Context`, `C4Container`, `C4Component`, `C4Dynamic`, `C4Deployment`

**Compatibility note:** C4 requires Mermaid 10.6+. Verify your rendering platform supports it.

### Diagram Levels

| Level | Keyword | Scope | Shows |
|-------|---------|-------|-------|
| Context | `C4Context` | Entire system | People, systems, external dependencies |
| Container | `C4Container` | Single system | Applications, databases, services within one system |
| Component | `C4Component` | Single container | Internal components of one application |
| Dynamic | `C4Dynamic` | Interaction flow | Numbered sequence of interactions |
| Deployment | `C4Deployment` | Infrastructure | Where containers run (servers, cloud, VMs) |

### Element Functions

#### People

```
Person(alias, "Label", "Description")
Person_Ext(alias, "Label", "Description")
```

- `Person` -- Internal user
- `Person_Ext` -- External user

#### Systems

```
System(alias, "Label", "Description")
System_Ext(alias, "Label", "Description")
System_Boundary(alias, "Label") { ... }
```

- `System` -- System under design
- `System_Ext` -- External system
- `System_Boundary` -- Groups elements belonging to one system

#### Containers

```
Container(alias, "Label", "Technology", "Description")
ContainerDb(alias, "Label", "Technology", "Description")
ContainerQueue(alias, "Label", "Technology", "Description")
Container_Ext(alias, "Label", "Technology", "Description")
Container_Boundary(alias, "Label") { ... }
```

- `Container` -- Application/service
- `ContainerDb` -- Database
- `ContainerQueue` -- Message queue
- `Container_Ext` -- External container
- `Container_Boundary` -- Groups containers

#### Components

```
Component(alias, "Label", "Technology", "Description")
ComponentDb(alias, "Label", "Technology", "Description")
ComponentQueue(alias, "Label", "Technology", "Description")
Component_Ext(alias, "Label", "Technology", "Description")
```

#### Deployment Nodes

```
Deployment_Node(alias, "Label", "Technology") { ... }
Node(alias, "Label", "Technology") { ... }
```

### Relationships

```
Rel(from, to, "Label")
Rel(from, to, "Label", "Technology/Protocol")

Rel_D(from, to, "Label")    %% Downward
Rel_U(from, to, "Label")    %% Upward
Rel_L(from, to, "Label")    %% Left
Rel_R(from, to, "Label")    %% Right

Rel_Back(from, to, "Label")          %% Reverse direction
BiRel(from, to, "Label")             %% Bidirectional
```

### C4 Styling

#### UpdateElementStyle

```
UpdateElementStyle(alias, $bgColor="color", $fontColor="color", $borderColor="color")
```

#### UpdateRelStyle

```
UpdateRelStyle(from, to, $textColor="color", $lineColor="color", $offsetX="n", $offsetY="n")
```

#### Layout

```
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### Title and Description

Always include a title for context:

```
title System Context Diagram for My Application
```

### C4 Examples

#### System Context Diagram

```mermaid
C4Context
    title System Context -- SaaS Platform

    Person(customer, "Customer", "Uses the web application to manage their account and resources")
    Person(admin, "Admin", "Manages platform settings, users, and billing")
    Person_Ext(developer, "Developer", "Integrates via API")

    System(platform, "SaaS Platform", "Core platform providing resource management and analytics")

    System_Ext(email, "Email Service", "SendGrid -- transactional and marketing emails")
    System_Ext(payment, "Payment Gateway", "Stripe -- subscription billing and payments")
    System_Ext(monitoring, "Monitoring", "Datadog -- metrics, logs, and alerting")
    System_Ext(cdn, "CDN", "CloudFront -- static asset delivery")

    Rel(customer, platform, "Uses", "HTTPS")
    Rel(admin, platform, "Manages", "HTTPS")
    Rel(developer, platform, "Integrates", "REST API")
    Rel(platform, email, "Sends emails", "SMTP/API")
    Rel(platform, payment, "Processes payments", "API")
    Rel(platform, monitoring, "Sends telemetry", "Agent")
    Rel(platform, cdn, "Serves assets", "HTTPS")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

#### Container Diagram

```mermaid
C4Container
    title Container Diagram -- SaaS Platform

    Person(customer, "Customer", "End user")
    Person(developer, "Developer", "API consumer")

    System_Boundary(platform, "SaaS Platform") {
        Container(spa, "Web App", "React, TypeScript", "Single-page application for customers")
        Container(api, "API Server", "Node.js, Express", "REST API handling all business logic")
        Container(worker, "Background Worker", "Node.js, Bull", "Async job processing")
        ContainerDb(db, "Database", "PostgreSQL", "Stores users, resources, billing")
        ContainerDb(cache, "Cache", "Redis", "Session store, rate limiting, job queue")
        ContainerQueue(queue, "Message Queue", "Redis/Bull", "Job queue for async processing")
        Container(scheduler, "Task Scheduler", "Node.js, cron", "Periodic maintenance tasks")
    }

    System_Ext(email, "Email Service", "SendGrid")
    System_Ext(payment, "Payment Gateway", "Stripe")
    System_Ext(storage, "Object Storage", "S3")

    Rel(customer, spa, "Uses", "HTTPS")
    Rel(developer, api, "Calls", "REST/HTTPS")
    Rel(spa, api, "Calls", "HTTPS/JSON")
    Rel(api, db, "Reads/writes", "SQL")
    Rel(api, cache, "Reads/writes", "Redis protocol")
    Rel(api, queue, "Enqueues jobs", "Redis protocol")
    Rel(worker, queue, "Processes jobs", "Redis protocol")
    Rel(worker, db, "Reads/writes", "SQL")
    Rel(worker, email, "Sends", "API")
    Rel(worker, storage, "Uploads", "S3 API")
    Rel(api, payment, "Charges", "API")
    Rel(scheduler, db, "Queries", "SQL")
    Rel(scheduler, queue, "Enqueues", "Redis protocol")

    UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="1")
```

#### Component Diagram

```mermaid
C4Component
    title Component Diagram -- API Server

    Container_Boundary(api, "API Server") {
        Component(router, "Router", "Express Router", "Routes HTTP requests to controllers")
        Component(auth, "Auth Middleware", "Passport.js", "JWT validation and session management")
        Component(controllers, "Controllers", "Express", "Request handling and response formatting")
        Component(services, "Service Layer", "TypeScript", "Business logic and orchestration")
        Component(repos, "Repositories", "TypeORM", "Data access and query building")
        Component(validators, "Validators", "Zod", "Request payload validation")
        Component(events, "Event Emitter", "EventEmitter2", "Domain event publishing")
    }

    ContainerDb(db, "Database", "PostgreSQL")
    ContainerDb(cache, "Cache", "Redis")
    ContainerQueue(queue, "Job Queue", "Bull/Redis")

    Rel(router, auth, "Authenticates via")
    Rel(router, controllers, "Delegates to")
    Rel(controllers, validators, "Validates with")
    Rel(controllers, services, "Calls")
    Rel(services, repos, "Queries via")
    Rel(services, events, "Publishes to")
    Rel(repos, db, "Reads/writes")
    Rel(services, cache, "Caches in")
    Rel(events, queue, "Enqueues to")
```

#### Dynamic Diagram

```mermaid
C4Dynamic
    title User Login Flow

    ContainerDb(db, "Database", "PostgreSQL")
    ContainerDb(cache, "Cache", "Redis")
    Container(api, "API Server", "Node.js")
    Container(spa, "Web App", "React")

    Rel(spa, api, "1. POST /auth/login", "HTTPS")
    Rel(api, db, "2. Validate credentials", "SQL")
    Rel(api, api, "3. Generate JWT")
    Rel(api, cache, "4. Store session", "Redis")
    Rel(api, spa, "5. Return token", "HTTPS")
```

---

## Integration Notes

**What this component does:** Provides comprehensive Mermaid diagram syntax, styling rules, and examples for creating technical visualizations. Includes inline content for flowcharts and C4 diagrams, with separate reference files for sequence, class, state, and ER diagrams.

**Origin:** Skill (reference/leaf node with reference files)

**Capabilities needed:**
- File reading (to load the separate reference files in `references/` when building complex diagrams)

**Adaptation guidance:**
- This is primarily a reference skill. The main content and two diagram types (flowcharts, C4) are fully inlined.
- Four additional diagram type references are in separate files under `references/`: sequence-diagrams.md, class-diagrams.md, state-diagrams.md, er-diagrams.md. Load these when building complex diagrams of those types.
- No orchestration or tool-specific behavior to adapt.
