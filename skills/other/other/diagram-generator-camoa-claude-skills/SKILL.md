---
name: diagram-generator
description: "Use when visualizing architecture - generates Mermaid diagrams for data flow, service relationships, or entity structures. Trigger: 'draw diagram', 'visualize', 'show relationships', 'mermaid chart'."
version: 1.1.0
---

# Diagram Generator

Create Mermaid diagrams for architecture visualization.

## Activation

Activate when you detect:
- "Create diagram for X"
- "Visualize the architecture"
- "Show me the data flow"
- "Draw the entity relationships"

## Workflow

### 1. Determine Diagram Type

Ask if unclear:
```
What should this diagram show?
1. Data flow (how data moves through system)
2. Service relationships (dependencies between services)
3. Entity relationships (database structure)
4. Sequence (interaction over time)
5. State (entity lifecycle)
```

### 2. Gather Elements

Based on type, ask:

**Data Flow:**
- What is the starting point?
- What are the processing steps?
- What is the final destination?

**Service Relationships:**
- What is the main service?
- What does it depend on?
- Are there event subscribers?

**Entity Relationships:**
- What entities are involved?
- What are the relationships (one-to-many, etc.)?

### 3. Generate Diagram

Create appropriate Mermaid code:

**Data Flow:**
```mermaid
flowchart LR
    A[Input] --> B[Process]
    B --> C[Output]
```

**Service Dependencies:**
```mermaid
graph TD
    A[MainService] --> B[Dependency1]
    A --> C[Dependency2]
```

**Entity Relationships:**
```mermaid
erDiagram
    ENTITY1 ||--o{ ENTITY2 : has
    ENTITY1 ||--|| ENTITY3 : references
```

**Sequence:**
```mermaid
sequenceDiagram
    Actor->>Component: Action
    Component-->>Actor: Response
```

**State:**
```mermaid
stateDiagram-v2
    [*] --> State1
    State1 --> State2
    State2 --> [*]
```

### 4. Present Diagram

Show the Mermaid code to user and ask:
```
Here's the diagram:

{mermaid code block}

Adjustments needed? (describe changes or "looks good")
```

### 5. Add to Architecture

Once approved, use `Edit` tool to add to appropriate architecture file:

```markdown
## {Diagram Title}

{One sentence describing what this shows}

\`\`\`mermaid
{diagram code}
\`\`\`
```

## Diagram Templates

### Drupal Request Flow
```mermaid
flowchart LR
    A[Request] --> B[Routing]
    B --> C[Controller]
    C --> D[Service]
    D --> E[Entity]
    E --> F[Response]
```

### Plugin System
```mermaid
graph TD
    A[PluginManager] --> B[Discovery]
    A --> C[Factory]
    B --> D[Annotations]
    B --> E[YAML]
    C --> F[Plugin Instance]
```

### Form Submit Flow
```mermaid
sequenceDiagram
    User->>Form: Submit
    Form->>Form: validateForm()
    Form->>Form: submitForm()
    Form->>Service: Process data
    Service-->>Form: Result
    Form-->>User: Redirect/Message
```

## Stop Points

STOP and wait for user:
- After asking diagram type
- After showing generated diagram
- Before adding to architecture file
