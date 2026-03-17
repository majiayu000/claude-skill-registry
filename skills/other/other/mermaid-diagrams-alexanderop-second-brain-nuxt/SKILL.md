---
name: mermaid-diagrams
description: Generate Mermaid diagrams (flowcharts, sequence, class, state, ER, C4, mindmaps, gitgraph). Use when asked to create diagrams, visualize processes, document architecture, or explain systems visually. Triggers include "diagram", "flowchart", "sequence diagram", "class diagram", "state diagram", "ER diagram", "C4", "mindmap", "gitgraph", "visualize", "draw".
---

# Mermaid Diagrams

Generate diagrams using Mermaid syntax. All diagrams render in markdown code blocks with `mermaid` language identifier.

## Decision Guide

| Use Case | Diagram Type |
|----------|--------------|
| Process flow, decision trees | Flowchart |
| API calls, system interactions over time | Sequence |
| OOP structure, domain models | Class |
| State machines, workflows | State |
| Database schemas, data relationships | ER |
| Software architecture (C4 model) | C4 |
| Brainstorming, hierarchical organization | Mindmap |
| Git branching, commit history | GitGraph |

---

## Quick Reference

### Flowchart
```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### Sequence
```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    U->>S: Request
    S-->>U: Response
```

### Class
```mermaid
classDiagram
    Animal <|-- Dog
    Animal : +String name
    Animal : +makeSound()
    Dog : +fetch()
```

### State
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: start
    Processing --> Done: complete
    Done --> [*]
```

### ER
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
```

### C4 Context
```mermaid
C4Context
    Person(user, "User", "End user")
    System(app, "Application", "Main system")
    Rel(user, app, "Uses")
```

### Mindmap
```mermaid
mindmap
  root((Topic))
    Branch A
      Leaf 1
      Leaf 2
    Branch B
```

### GitGraph
```mermaid
gitgraph
    commit
    branch feature
    commit
    checkout main
    merge feature
```

---

## Flowchart Reference

**Directions:** `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left)

### Node Shapes

| Shape | Syntax | Example |
|-------|--------|---------|
| Rectangle | `[text]` | `A[Process]` |
| Rounded | `(text)` | `A(Start)` |
| Stadium | `([text])` | `A([Terminal])` |
| Diamond | `{text}` | `A{Decision}` |
| Circle | `((text))` | `A((Event))` |
| Hexagon | `{{text}}` | `A{{Prepare}}` |
| Cylinder | `[(text)]` | `A[(Database)]` |
| Subroutine | `[[text]]` | `A[[Subprocess]]` |
| Parallelogram | `[/text/]` | `A[/Input/]` |
| Trapezoid | `[\text\]` | `A[\Manual Op\]` |

### Link Types

| Type | Syntax | Description |
|------|--------|-------------|
| Arrow | `-->` | Solid with arrowhead |
| Open | `---` | Solid, no arrowhead |
| Dotted arrow | `-.->` | Dotted with arrowhead |
| Thick arrow | `==>` | Thick with arrowhead |
| With text | `--\|text\|>` | Label on link |
| Multi-length | `---->` | Longer link (more ranks) |

### Subgraphs
```mermaid
flowchart TD
    subgraph Backend["Backend Services"]
        direction LR
        API --> DB[(Database)]
    end
    Client --> API
```

### Styling
```mermaid
flowchart TD
    A[Node]:::highlight
    classDef highlight fill:#ff9,stroke:#333
    style A stroke-width:2px
```

---

## Sequence Diagram Reference

### Arrow Types

| Syntax | Style |
|--------|-------|
| `->>` | Solid with arrowhead |
| `-->>` | Dotted with arrowhead |
| `-x` | Solid with cross |
| `-)` | Async (open arrow) |
| `<<->>` | Bidirectional |

### Participants
```mermaid
sequenceDiagram
    actor User
    participant API as API Server
    participant DB as Database
```

### Activations
```mermaid
sequenceDiagram
    User->>+API: Request
    API->>+DB: Query
    DB-->>-API: Result
    API-->>-User: Response
```

### Control Flow
```mermaid
sequenceDiagram
    alt Success
        A->>B: OK
    else Failure
        A->>B: Error
    end

    loop Every 5s
        A->>B: Ping
    end

    opt Optional
        A->>B: Maybe
    end
```

### Notes
```mermaid
sequenceDiagram
    Note right of A: Single note
    Note over A,B: Spanning note
```

### Grouping with Boxes
```mermaid
sequenceDiagram
    box Blue Frontend
        participant U as User
        participant W as Web
    end
    box Green Backend
        participant A as API
    end
```

---

## Class Diagram Reference

### Visibility Modifiers

| Symbol | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package |

### Relationships

| Type | Syntax | Meaning |
|------|--------|---------|
| Inheritance | `<\|--` | Extends |
| Composition | `*--` | Strong owns |
| Aggregation | `o--` | Weak owns |
| Association | `-->` | Uses |
| Dependency | `..>` | Depends on |
| Realization | `..\|>` | Implements |

### Full Example
```mermaid
classDiagram
    class Animal {
        <<abstract>>
        +String name
        +int age
        +makeSound()* void
    }
    class Dog {
        +String breed
        +fetch() void
    }
    Animal <|-- Dog
    Dog "1" --> "*" Toy : plays with
```

### Generics
```mermaid
classDiagram
    class List~T~ {
        +add(T item)
        +T get(int index)
    }
```

### Annotations
- `<<interface>>` - Interface
- `<<abstract>>` - Abstract class
- `<<service>>` - Service class
- `<<enumeration>>` - Enum

---

## State Diagram Reference

### Basic Syntax
```mermaid
stateDiagram-v2
    [*] --> State1
    State1 --> State2: trigger
    State2 --> [*]
```

### Composite States
```mermaid
stateDiagram-v2
    state Active {
        [*] --> Running
        Running --> Paused: pause
        Paused --> Running: resume
    }
    [*] --> Active
    Active --> [*]: stop
```

### Fork and Join
```mermaid
stateDiagram-v2
    state fork <<fork>>
    state join <<join>>
    [*] --> fork
    fork --> Task1
    fork --> Task2
    Task1 --> join
    Task2 --> join
    join --> [*]
```

### Choice
```mermaid
stateDiagram-v2
    state check <<choice>>
    [*] --> check
    check --> Success: valid
    check --> Error: invalid
```

### Notes
```mermaid
stateDiagram-v2
    State1
    note right of State1
        Description here
    end note
```

---

## ER Diagram Reference

### Cardinality

| Left | Right | Meaning |
|------|-------|---------|
| `\|o` | `o\|` | Zero or one |
| `\|\|` | `\|\|` | Exactly one |
| `}o` | `o{` | Zero or more |
| `}\|` | `\|{` | One or more |

### Relationship Types
- `--` Identifying (solid line, child depends on parent)
- `..` Non-identifying (dashed line, independent entities)

### Attributes
```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string name
        datetime created_at
    }
    POST {
        int id PK
        int user_id FK
        string title
        text content
    }
    USER ||--o{ POST : writes
```

---

## C4 Diagram Reference

C4 provides 4 levels of abstraction for architecture documentation.

### Diagram Types
- `C4Context` - System context (level 1)
- `C4Container` - Container diagram (level 2)
- `C4Component` - Component diagram (level 3)
- `C4Dynamic` - Interaction sequences
- `C4Deployment` - Infrastructure layout

### Elements

| Element | Syntax | Use |
|---------|--------|-----|
| Person | `Person(alias, label, desc)` | Users |
| Person_Ext | `Person_Ext(...)` | External users |
| System | `System(alias, label, desc)` | Software systems |
| System_Ext | `System_Ext(...)` | External systems |
| SystemDb | `SystemDb(...)` | Database systems |
| Container | `Container(alias, label, tech, desc)` | Applications |
| ContainerDb | `ContainerDb(...)` | Container databases |
| Component | `Component(alias, label, tech, desc)` | Internal parts |

### Boundaries
```mermaid
C4Container
    System_Boundary(app, "Application") {
        Container(web, "Web App", "React")
        Container(api, "API", "Node.js")
        ContainerDb(db, "Database", "PostgreSQL")
    }
    Rel(web, api, "HTTP/JSON")
    Rel(api, db, "SQL")
```

### Relationships
- `Rel(from, to, label)` - Standard relationship
- `Rel_U/D/L/R(...)` - Directional hints
- `BiRel(from, to, label)` - Bidirectional

### Complete C4 Context Example
```mermaid
C4Context
    Person(user, "Customer", "Uses the system")
    System(app, "E-Commerce", "Online store")
    System_Ext(payment, "Payment Gateway", "Processes payments")
    System_Ext(shipping, "Shipping API", "Handles delivery")

    Rel(user, app, "Browses, orders")
    Rel(app, payment, "Processes payments")
    Rel(app, shipping, "Ships orders")
```

---

## Mindmap Reference

Uses indentation for hierarchy. Root node required.

### Node Shapes
```mermaid
mindmap
    root((Central Topic))
        [Square]
        (Rounded)
        ))Cloud((
        {{Hexagon}}
```

### With Icons
```mermaid
mindmap
    root((Project))
        Tasks ::icon(fa fa-tasks)
        Team ::icon(fa fa-users)
```

### Styling
```mermaid
mindmap
    root
        Important:::urgent
        Normal
```

---

## GitGraph Reference

### Basic Operations
```mermaid
gitgraph
    commit id: "initial"
    commit id: "feature"
    branch develop
    commit
    checkout main
    merge develop tag: "v1.0"
```

### Commit Types
- `type: NORMAL` - Default
- `type: HIGHLIGHT` - Emphasized
- `type: REVERSE` - Reverted

### Full Example
```mermaid
gitgraph
    commit id: "init"
    branch feature
    commit id: "add-login"
    commit id: "add-logout" type: HIGHLIGHT
    checkout main
    commit id: "hotfix" type: REVERSE
    merge feature tag: "v1.0"
```

---

## Best Practices

### DO
- Keep diagrams focused (one concept per diagram)
- Use clear, descriptive labels
- Add direction hints (`TD`, `LR`) explicitly
- Use subgraphs/boundaries for grouping
- Include legends for complex diagrams

### DON'T
- Overcrowd with too many nodes (>15-20)
- Use cryptic single-letter IDs without labels
- Mix multiple concerns in one diagram
- Rely on auto-layout for complex diagrams

### Layout Tips
- **Flowchart**: `LR` for processes, `TD` for hierarchies
- **Sequence**: Order participants by interaction frequency
- **Class**: Group related classes with namespaces
- **C4**: Start with Context, drill down to Container/Component
- **ER**: Place central entities in the middle

### Common Fixes
| Problem | Solution |
|---------|----------|
| Nodes overlap | Reduce node count, use subgraphs |
| Links cross confusingly | Reorder nodes, change direction |
| Text truncated | Use aliases: `A[Long Name] as short` |
| Diagram too wide | Switch `LR` to `TD` |
