---
name: mermaid-diagrams
# prettier-ignore
description: Use when creating Mermaid diagrams - covers flowcharts, sequence diagrams, and AST visualization
---

# Mermaid Diagram Best Practices

## Quick Start

```mermaid
flowchart TD
    A[Source Code] --> B[Lexer]
    B --> C[Tokens]
    C --> D[Parser]
    D --> E[AST]
    E --> F[Interpreter]
    F --> G[Result]
```

## Diagram Types

### Flowchart (AST Visualization)

```mermaid
flowchart TD
    subgraph "BinaryExpr"
        op["+"]
        left[NumberLiteral: 2]
        right[NumberLiteral: 3]
    end
    op --> left
    op --> right
```

### Sequence Diagram (Execution Flow)

```mermaid
sequenceDiagram
    participant User
    participant REPL
    participant Parser
    participant Interpreter

    User->>REPL: "2 + 3"
    REPL->>Parser: parse()
    Parser-->>REPL: AST
    REPL->>Interpreter: evaluate(AST)
    Interpreter-->>REPL: 5
    REPL-->>User: 5
```

### State Diagram (Token States)

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Number: digit
    Start --> String: quote
    Start --> Identifier: letter
    Number --> Number: digit
    Number --> [*]: other
    String --> String: char
    String --> [*]: quote
```

### Class Diagram (AST Types)

```mermaid
classDiagram
    class Expr {
        <<interface>>
    }
    class NumberLiteral {
        +number value
    }
    class BinaryExpr {
        +string op
        +Expr left
        +Expr right
    }
    Expr <|-- NumberLiteral
    Expr <|-- BinaryExpr
```

## AST Node Styling

```mermaid
flowchart TD
    classDef literal fill:#e1f5fe
    classDef expr fill:#fff3e0
    classDef stmt fill:#e8f5e9

    A[LetStmt]:::stmt --> B[Identifier: x]
    A --> C[BinaryExpr]:::expr
    C --> D[NumberLiteral: 2]:::literal
    C --> E[NumberLiteral: 3]:::literal
```

## Generating from Code

```typescript
function astToMermaid(node: Expr, id = "n0"): string {
  const lines: string[] = [];

  function visit(node: Expr, nodeId: string): void {
    switch (node.type) {
      case "NumberLiteral":
        lines.push(`    ${nodeId}["${node.value}"]`);
        break;
      case "BinaryExpr":
        lines.push(`    ${nodeId}["${node.op}"]`);
        const leftId = `${nodeId}L`;
        const rightId = `${nodeId}R`;
        lines.push(`    ${nodeId} --> ${leftId}`);
        lines.push(`    ${nodeId} --> ${rightId}`);
        visit(node.left, leftId);
        visit(node.right, rightId);
        break;
    }
  }

  visit(node, id);
  return `flowchart TD\n${lines.join("\n")}`;
}
```

## HTML Embedding

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
  <div class="mermaid">
    flowchart TD
      A --> B
  </div>
  <script>mermaid.initialize({ startOnLoad: true });</script>
</body>
</html>
```

## Reference Files

- [references/syntax.md](references/syntax.md) - Complete Mermaid syntax
- [references/theming.md](references/theming.md) - Custom themes and styles
