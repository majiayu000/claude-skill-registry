---
name: blog-mermaid
description: Create mermaid diagrams for blog posts using the blog's sky/zinc color theme. Use when adding flowcharts, sequence diagrams, or other mermaid visualizations to blog content.
---

# Blog Mermaid Diagrams

Create mermaid diagrams that match the blog's visual theme.

## Color Theme

The blog uses **sky** as primary and **zinc** as neutral colors.

| Element          | Light Mode | Dark Mode |
| ---------------- | ---------- | --------- |
| Background       | white      | #020618   |
| Primary fill     | sky-100    | sky-900   |
| Secondary fill   | zinc-100   | zinc-800  |
| Borders/lines    | sky-600    | sky-500   |
| Text             | zinc-900   | zinc-100  |
| Accent/highlight | sky-400    | sky-400   |

## Diagram Style Guidelines

1. **Keep it simple** - Prefer fewer nodes with clear relationships
2. **Use horizontal layouts** - `flowchart LR` reads better than `TB` for most cases
3. **Group related items** - Use subgraphs to cluster concepts
4. **Consolidate arrows** - Use `&` syntax: `A & B & C --> D`
5. **Minimal labels** - Edge labels should be 1-3 words max

## Flowchart Template

```mermaid
flowchart LR
    subgraph GroupName
        A[Node A]
        B[Node B]
    end

    A --> C[Result]
    B --> C
```

## Sequence Diagram Template

```mermaid
sequenceDiagram
    participant A as Actor
    participant B as System

    A->>B: action
    B-->>A: response
```

## State Diagram Alternative

Prefer flowcharts over state diagrams - they render more reliably:

```mermaid
flowchart TB
    Start([Start]) --> State1
    State1 -->|condition| State2
    State2 --> End([End])
```

## Examples

### Good: Simple and clear

```mermaid
flowchart LR
    Lead[Orchestrator] -->|spawns| W1 & W2 & W3
    W1 & W2 & W3 -->|report| Lead
```

### Bad: Over-complicated

```mermaid
flowchart TB
    subgraph Layer1[First Layer]
        direction LR
        A1[Component A1] --> A2[Component A2]
        A2 --> A3[Component A3]
    end
    subgraph Layer2[Second Layer]
        direction LR
        B1[Component B1] --> B2[Component B2]
    end
    A1 --> B1
    A2 --> B2
    A3 --> B1
    A3 --> B2
```

Simplify to essential relationships only.
