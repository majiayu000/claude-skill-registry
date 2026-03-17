---
name: mermaid-diagrams
description: Mermaid diagram creation for flowcharts, sequences, ERDs, and more. Generate diagrams from text in markdown files. Use for documentation, architecture diagrams, and visual representations. Triggers on mermaid, flowchart, sequence diagram, ERD, entity relationship, gantt chart, pie chart, class diagram, state diagram, journey map.
---

# Mermaid Diagrams

Create diagrams and visualizations using Mermaid's text-based syntax.

## Quick Reference

### Diagram Types

| Type | Syntax | Use Case |
|------|--------|----------|
| **Flowchart** | `flowchart` | Process flows, decisions |
| **Sequence** | `sequenceDiagram` | API calls, interactions |
| **Class** | `classDiagram` | OOP relationships |
| **ERD** | `erDiagram` | Database schemas |
| **State** | `stateDiagram-v2` | State machines |
| **Gantt** | `gantt` | Project timelines |
| **Pie** | `pie` | Proportions |
| **Journey** | `journey` | User experience |

## Flowcharts

### Basic Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### Node Shapes

```mermaid
flowchart LR
    A[Rectangle] --> B(Rounded)
    B --> C([Stadium])
    C --> D[[Subroutine]]
    D --> E[(Database)]
    E --> F((Circle))
    F --> G>Asymmetric]
    G --> H{Diamond}
    H --> I{{Hexagon}}
    I --> J[/Parallelogram/]
```

### Direction Options

```
TD - Top to Down
TB - Top to Bottom
BT - Bottom to Top
LR - Left to Right
RL - Right to Left
```

### Arrow Types

```mermaid
flowchart LR
    A --> B
    A --- C
    A -.-> D
    A ==> E
    A --text--> F
    A ---|text| G
```

### Subgraphs

```mermaid
flowchart TB
    subgraph Frontend
        A[React App]
        B[Vue App]
    end
    subgraph Backend
        C[API Server]
        D[Worker]
    end
    subgraph Database
        E[(PostgreSQL)]
        F[(Redis)]
    end
    A --> C
    B --> C
    C --> E
    D --> F
```

## Sequence Diagrams

### Basic Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant D as Database

    U->>A: POST /login
    A->>D: Query user
    D-->>A: User data
    A-->>U: JWT Token
```

### Arrow Types

```
->>   Solid line with arrowhead
-->>  Dotted line with arrowhead
-)    Solid line with open arrow
--)   Dotted line with open arrow
-x    Solid line with cross
--x   Dotted line with cross
```

### Activations and Notes

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>+S: Request
    Note right of S: Processing...
    S-->>-C: Response

    Note over C,S: Communication complete
```

### Loops and Conditionals

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    loop Every 5 seconds
        C->>S: Ping
        S-->>C: Pong
    end

    alt Success
        S-->>C: Data
    else Failure
        S-->>C: Error
    end

    opt Optional
        C->>S: Additional request
    end
```

## Class Diagrams

### Basic Class

```mermaid
classDiagram
    class User {
        +String id
        +String name
        +String email
        +login()
        +logout()
    }

    class Order {
        +String id
        +Date date
        +Float total
        +process()
        +cancel()
    }

    User "1" --> "*" Order : places
```

### Relationships

```mermaid
classDiagram
    classA <|-- classB : Inheritance
    classC *-- classD : Composition
    classE o-- classF : Aggregation
    classG <-- classH : Association
    classI -- classJ : Link
    classK <.. classL : Dependency
    classM <|.. classN : Realization
```

### Visibility

```
+ Public
- Private
# Protected
~ Package/Internal
```

## Entity Relationship Diagrams

### Basic ERD

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "appears in"

    USER {
        int id PK
        string name
        string email UK
        date created_at
    }

    ORDER {
        int id PK
        int user_id FK
        date order_date
        float total
    }

    PRODUCT {
        int id PK
        string name
        float price
        int stock
    }
```

### Relationship Types

```
||--|| : One to One
||--o{ : One to Zero or More
||--|{ : One to One or More
}o--o{ : Zero or More to Zero or More
```

## State Diagrams

### Basic State Machine

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Pending : Submit
    Pending --> Approved : Approve
    Pending --> Rejected : Reject
    Approved --> [*]
    Rejected --> Draft : Revise
```

### Composite States

```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Idle
        Idle --> Processing : Start
        Processing --> Idle : Complete
    }

    Active --> Suspended : Pause
    Suspended --> Active : Resume
    Active --> [*] : Terminate
```

## Gantt Charts

### Project Timeline

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Planning
    Requirements    :a1, 2024-01-01, 7d
    Design          :a2, after a1, 10d

    section Development
    Backend         :b1, after a2, 14d
    Frontend        :b2, after a2, 14d
    Integration     :b3, after b1, 7d

    section Testing
    QA Testing      :c1, after b3, 7d
    UAT             :c2, after c1, 5d

    section Deployment
    Release         :milestone, after c2, 0d
```

## Pie Charts

```mermaid
pie title Technology Stack
    "JavaScript" : 40
    "Python" : 30
    "Go" : 15
    "Rust" : 10
    "Other" : 5
```

## User Journey

```mermaid
journey
    title User Checkout Journey
    section Browse
      Visit site: 5: User
      Search product: 4: User
      View product: 5: User
    section Purchase
      Add to cart: 4: User
      Checkout: 3: User
      Payment: 2: User
    section Delivery
      Confirmation: 5: User, System
      Shipping: 4: System
      Delivery: 5: System
```

## Git Graphs

```mermaid
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
    branch feature
    checkout feature
    commit
    checkout main
    merge feature
```

## Mindmaps

```mermaid
mindmap
    root((Project))
        Frontend
            React
            TypeScript
            Tailwind
        Backend
            Node.js
            PostgreSQL
            Redis
        DevOps
            Docker
            Kubernetes
            GitHub Actions
```

## Styling

### Custom Styles

```mermaid
flowchart LR
    A[Start]:::green --> B[Process]:::blue --> C[End]:::red

    classDef green fill:#9f6,stroke:#333
    classDef blue fill:#69f,stroke:#333
    classDef red fill:#f66,stroke:#333
```

### Theme Configuration

```mermaid
%%{init: {'theme': 'dark'}}%%
flowchart LR
    A --> B --> C
```

## Markdown Integration

### In Markdown Files

````markdown
```mermaid
flowchart LR
    A --> B --> C
```
````

### GitHub Support

GitHub natively renders Mermaid in markdown files, issues, and pull requests.

### VS Code Extensions

- Markdown Preview Mermaid Support
- Mermaid Editor

## Best Practices

1. **Use subgraphs** - Group related elements
2. **Direction matters** - Choose LR for processes, TD for hierarchies
3. **Label edges** - Add text to clarify relationships
4. **Keep it simple** - Avoid too many nodes in one diagram
5. **Use consistent styling** - Apply class definitions
6. **Add titles** - Include descriptive titles
7. **Break up complexity** - Multiple diagrams over one complex one
8. **Use proper diagram type** - Match diagram type to data
9. **Test rendering** - Verify in target platform
10. **Document with diagrams** - Embed in README and docs

## When to Use This Skill

- Creating flowcharts for documentation
- Designing sequence diagrams for APIs
- Modeling database schemas with ERDs
- Visualizing class relationships
- Planning project timelines
- Documenting state machines
- Creating architecture diagrams
