---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Diagram Creator
# ═══════════════════════════════════════════════════════════════════════════════

name: diagram-creator
description: "Create professional diagrams using Mermaid, PlantUML, and other text-based diagram tools. Generate flowcharts, sequence diagrams, architecture diagrams, and more."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: visualization
tags:
  - diagram
  - flowchart
  - mermaid
  - plantuml
  - architecture
department: Engineering/Design

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

capabilities:
  - flowchart_creation
  - sequence_diagrams
  - architecture_diagrams
  - er_diagrams
  - class_diagrams

languages:
  - en
  - zh

related_skills:
  - chart-designer
  - ppt-visual
  - dev-slides
---

# Diagram Creator Skill

## Overview

I help you create professional diagrams using text-based diagram tools like Mermaid and PlantUML. These diagrams can be rendered in documentation, presentations, and development tools.

**What I can do:**
- Create flowcharts and process diagrams
- Generate sequence diagrams
- Build architecture and system diagrams
- Design ER (Entity-Relationship) diagrams
- Create class diagrams and UML
- Generate organizational charts
- Build Gantt charts and timelines

**What I cannot do:**
- Render images directly (use Mermaid live editor or similar)
- Create pixel-perfect custom designs
- Generate raster images

---

## How to Use Me

### Step 1: Describe Your Diagram

Tell me:
- What process/system/concept to visualize
- Type of diagram needed
- Level of detail
- Target audience

### Step 2: Choose Format

- **Mermaid**: Best for web, markdown, GitHub
- **PlantUML**: Best for UML, complex diagrams
- **ASCII**: Simple, universal compatibility
- **D2**: Modern, stylish diagrams

### Step 3: Specify Style

- Colors and themes
- Direction (top-down, left-right)
- Level of detail

---

## Diagram Types

### 1. Flowchart / Process Diagram

**Use for**: Business processes, decision trees, workflows

```mermaid
flowchart TD
    A[Start] --> B{Decision?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### 2. Sequence Diagram

**Use for**: API calls, user interactions, system communication

```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Server
    participant D as Database
    
    U->>A: Click Login
    A->>S: POST /auth/login
    S->>D: Query user
    D-->>S: User data
    S-->>A: JWT token
    A-->>U: Redirect to dashboard
```

### 3. Architecture Diagram

**Use for**: System design, infrastructure, component relationships

```mermaid
flowchart TB
    subgraph Client
        A[Web App]
        B[Mobile App]
    end
    
    subgraph Backend
        C[API Gateway]
        D[Auth Service]
        E[User Service]
        F[Order Service]
    end
    
    subgraph Data
        G[(PostgreSQL)]
        H[(Redis)]
        I[(S3)]
    end
    
    A & B --> C
    C --> D & E & F
    D --> H
    E --> G
    F --> G & I
```

### 4. Entity-Relationship Diagram

**Use for**: Database design, data models

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
    
    CUSTOMER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        date created_at
        int customer_id FK
    }
    PRODUCT {
        int id PK
        string name
        decimal price
    }
```

### 5. Class Diagram

**Use for**: OOP design, code structure

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    class Cat {
        +boolean indoor
        +meow()
    }
    
    Animal <|-- Dog
    Animal <|-- Cat
```

### 6. State Diagram

**Use for**: State machines, status workflows

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: Submit
    Submitted --> InReview: Assign reviewer
    InReview --> Approved: Approve
    InReview --> Rejected: Reject
    Rejected --> Draft: Revise
    Approved --> [*]
```

### 7. Gantt Chart

**Use for**: Project timelines, schedules

```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    
    section Planning
    Requirements    :a1, 2024-01-01, 14d
    Design          :a2, after a1, 21d
    
    section Development
    Backend         :b1, after a2, 30d
    Frontend        :b2, after a2, 30d
    
    section Testing
    QA Testing      :c1, after b1, 14d
    UAT             :c2, after c1, 7d
```

### 8. Mind Map

**Use for**: Brainstorming, concept organization

```mermaid
mindmap
    root((Project))
        Features
            Feature A
            Feature B
            Feature C
        Team
            Frontend
            Backend
            Design
        Timeline
            Q1
            Q2
            Q3
```

### 9. Git Graph

**Use for**: Branch visualization, git workflows

```mermaid
gitGraph
    commit
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
```

---

## Output Format

```markdown
# Diagram: [Name]

**Type**: [Flowchart / Sequence / Architecture / etc.]
**Tool**: [Mermaid / PlantUML]
**Purpose**: [What it illustrates]

---

## Diagram Code

### Mermaid

```mermaid
[Mermaid code here]
```

### PlantUML (Alternative)

```plantuml
[PlantUML code here]
```

---

## Rendering Instructions

1. **Mermaid Live Editor**: https://mermaid.live/
2. **GitHub**: Paste directly in markdown files
3. **VS Code**: Install Mermaid extension
4. **Notion**: Use code block with mermaid type

---

## Customization Options

### Color Theme
Add to the beginning:
```
%%{init: {'theme':'forest'}}%%
```

Available themes: default, forest, dark, neutral

### Direction
- TB (top to bottom)
- BT (bottom to top)
- LR (left to right)
- RL (right to left)

---

## Notes

- [Any notes about the diagram]
- [Assumptions made]
```

---

## PlantUML Examples

### Sequence Diagram
```plantuml
@startuml
actor User
participant "Web App" as App
participant "API Server" as API
database "Database" as DB

User -> App: Login request
App -> API: POST /auth/login
API -> DB: SELECT user
DB --> API: User record
API --> App: JWT token
App --> User: Redirect to dashboard
@enduml
```

### Component Diagram
```plantuml
@startuml
package "Frontend" {
    [React App]
    [Mobile App]
}

package "Backend" {
    [API Gateway]
    [Auth Service]
    [User Service]
}

database "PostgreSQL" as DB

[React App] --> [API Gateway]
[Mobile App] --> [API Gateway]
[API Gateway] --> [Auth Service]
[API Gateway] --> [User Service]
[User Service] --> DB
@enduml
```

---

## Tips for Better Diagrams

1. **Keep it simple** - Don't overcrowd
2. **Use consistent naming** - Clear, descriptive labels
3. **Group related items** - Use subgraphs/packages
4. **Choose appropriate type** - Match diagram to concept
5. **Consider audience** - Technical vs. business
6. **Use colors sparingly** - For emphasis only
7. **Add legends** - When using symbols/colors
8. **Maintain hierarchy** - Top-down or left-right flow

---

## Rendering Tools

| Tool | URL | Best For |
|------|-----|----------|
| Mermaid Live | mermaid.live | Quick editing |
| PlantUML Server | plantuml.com | PlantUML rendering |
| Draw.io | draw.io | Manual editing |
| Excalidraw | excalidraw.com | Hand-drawn style |
| Lucidchart | lucidchart.com | Professional diagrams |

---

## Limitations

- Cannot render images directly
- Complex layouts may need manual adjustment
- Limited styling compared to design tools
- Some diagram types not supported in all tools

---

*Built by the Claude Office Skills community. Contributions welcome!*
