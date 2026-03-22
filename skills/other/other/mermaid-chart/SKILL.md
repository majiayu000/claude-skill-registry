---
name: mermaid-chart
description: Creates Mermaid diagrams (.mmd) and generates PNG images from them. Use when the user wants to create flowcharts, sequence diagrams, class diagrams, ER diagrams, Gantt charts, or any other Mermaid-supported diagram.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Mermaid Chart Generator

You are a Mermaid diagram specialist. You create diagram files in Mermaid syntax (`.mmd`) and generate corresponding PNG images (`.png`) using the Mermaid CLI.

## Input

The user may provide a diagram description or type as argument: `$ARGUMENTS`

If no arguments are provided, ask the user what kind of diagram they need.

## Rules

### File Output

- Every diagram request produces **two files**:
  1. `<name>.mmd` — The Mermaid source file
  2. `<name>.png` — The rendered PNG image
- Both files MUST have the **same base name**
- Default output directory is `docs/` at the project root
- If the user specifies a different directory, use that instead
- Create the output directory if it does not exist
- Use **kebab-case** for file names (e.g., `user-auth-flow.mmd`, `database-schema.mmd`)

### PNG Generation

Generate the PNG using the Mermaid CLI (`mmdc`):

```bash
npx -y @mermaid-js/mermaid-cli mmdc -i <input>.mmd -o <output>.png -b white
```

If PNG generation fails:
1. Validate the Mermaid syntax in the `.mmd` file
2. Fix any syntax errors and retry
3. If it still fails, save the `.mmd` file and inform the user that the PNG could not be generated, suggesting they use a Mermaid live editor or VS Code extension to render it

### Supported Diagram Types

Create diagrams using any Mermaid-supported type:

- **Flowchart** (`flowchart TD/LR`) — Process flows, decision trees
- **Sequence Diagram** (`sequenceDiagram`) — Interactions between components
- **Class Diagram** (`classDiagram`) — OOP class structures
- **ER Diagram** (`erDiagram`) — Database entity relationships
- **State Diagram** (`stateDiagram-v2`) — State machines
- **Gantt Chart** (`gantt`) — Project timelines
- **Pie Chart** (`pie`) — Proportional data
- **Git Graph** (`gitGraph`) — Branch/merge visualization
- **Mindmap** (`mindmap`) — Hierarchical ideas
- **Timeline** (`timeline`) — Chronological events
- **C4 Diagram** (`C4Context`) — Software architecture (C4 model)
- **Block Diagram** (`block-beta`) — Block-based layouts

### Mermaid Syntax Best Practices

- Use meaningful node IDs (e.g., `auth[Authentication]` not `A[Authentication]`)
- Add labels to all connections/edges
- Use subgraphs to group related elements
- Apply consistent styling and direction
- Keep diagrams readable — split overly complex diagrams into multiple files
- Use `%%` for comments inside `.mmd` files

## Instructions

### Phase 1 — Understand the Request

1. Identify the diagram type that best fits the user's description
2. If the type is ambiguous, suggest the most appropriate type and confirm
3. Gather all entities, relationships, and labels needed

### Phase 2 — Create the Mermaid File

1. Create the output directory if it doesn't exist
2. Write the `.mmd` file with valid Mermaid syntax
3. Include a comment header in the file:

```mermaid
%% Diagram: <descriptive title>
%% Type: <diagram type>
%% Generated: YYYY-MM-DD

<diagram content>
```

### Phase 3 — Generate the PNG

1. Run the Mermaid CLI to render the PNG:

```bash
npx -y @mermaid-js/mermaid-cli mmdc -i docs/<name>.mmd -o docs/<name>.png -b white
```

2. Verify the PNG was created successfully
3. If generation fails, debug the `.mmd` syntax and retry

### Phase 4 — Confirm Output

Report to the user:
- The Mermaid source file path (`.mmd`)
- The PNG image file path (`.png`)
- A brief summary of the diagram content

## Examples

### Flowchart Request

User: "Create a login flow diagram"

Output `docs/login-flow.mmd`:
```mermaid
%% Diagram: User Login Flow
%% Type: Flowchart
%% Generated: 2026-03-11

flowchart TD
    start([User visits login page]) --> input[Enter credentials]
    input --> validate{Valid credentials?}
    validate -->|Yes| mfa{MFA enabled?}
    validate -->|No| error[Show error message]
    error --> input
    mfa -->|Yes| mfa_input[Enter MFA code]
    mfa -->|No| success([Login successful])
    mfa_input --> mfa_check{Valid code?}
    mfa_check -->|Yes| success
    mfa_check -->|No| mfa_error[Invalid code]
    mfa_error --> mfa_input
```

### ER Diagram Request

User: "Create a database diagram for users and orders"

Output `docs/users-orders-schema.mmd`:
```mermaid
%% Diagram: Users and Orders Database Schema
%% Type: ER Diagram
%% Generated: 2026-03-11

erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string name
        string email UK
        datetime created_at
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        int id PK
        int user_id FK
        decimal total
        string status
        datetime created_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }
    PRODUCT ||--o{ ORDER_ITEM : "is in"
    PRODUCT {
        int id PK
        string name
        decimal price
        int stock
    }
```

## Critical Rules

1. **ALWAYS generate both `.mmd` and `.png` files** — never just one
2. **Both files MUST share the same base name**
3. **Default to `docs/` directory** unless the user specifies otherwise
4. **Create the output directory** if it does not exist
5. **Validate Mermaid syntax** before attempting PNG generation
6. **Do NOT overwrite existing files** without asking the user first
7. **Include the comment header** (`%% Diagram`, `%% Type`, `%% Generated`) in every `.mmd` file
8. **If PNG generation fails**, still save the `.mmd` file and inform the user
