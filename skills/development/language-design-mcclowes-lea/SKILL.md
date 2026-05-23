---
name: language-design
# prettier-ignore
description: Use when designing language features - covers lexer, parser, AST, and interpreter patterns
---

# Language Design Patterns

## Quick Start

```
Source Code → Lexer → Tokens → Parser → AST → Interpreter → Result
```

## Lexer Design

### Token Types

```typescript
enum TokenType {
  // Literals
  NUMBER, STRING, IDENTIFIER,

  // Keywords
  LET, IF, ELSE, RETURN,

  // Operators
  PLUS, MINUS, STAR, SLASH,
  PIPE,  // />

  // Delimiters
  LPAREN, RPAREN, LBRACE, RBRACE,

  // Special
  EOF, NEWLINE,
}
```

### Lexer Pattern

```typescript
class Lexer {
  private source: string;
  private pos = 0;
  private line = 1;
  private column = 1;

  nextToken(): Token {
    this.skipWhitespace();

    if (this.isAtEnd()) return this.makeToken(TokenType.EOF);

    const char = this.advance();

    if (this.isDigit(char)) return this.number();
    if (this.isAlpha(char)) return this.identifier();
    if (char === '"') return this.string();

    // Operators
    switch (char) {
      case '+': return this.makeToken(TokenType.PLUS);
      case '/':
        if (this.match('>')) return this.makeToken(TokenType.PIPE);
        return this.makeToken(TokenType.SLASH);
    }

    throw new LexerError(`Unexpected character: ${char}`, this.line, this.column);
  }
}
```

## Parser Design

### Recursive Descent

```typescript
class Parser {
  private tokens: Token[];
  private current = 0;

  parse(): Program {
    const statements: Stmt[] = [];
    while (!this.isAtEnd()) {
      statements.push(this.statement());
    }
    return { type: "Program", body: statements };
  }

  // Precedence climbing
  private expression(): Expr {
    return this.pipe();
  }

  private pipe(): Expr {
    let left = this.equality();
    while (this.match(TokenType.PIPE)) {
      const right = this.equality();
      left = { type: "PipeExpr", left, right };
    }
    return left;
  }

  private equality(): Expr {
    let left = this.comparison();
    while (this.match(TokenType.EQEQ, TokenType.NEQ)) {
      const op = this.previous().type;
      const right = this.comparison();
      left = { type: "BinaryExpr", op, left, right };
    }
    return left;
  }

  // Continue down precedence...
}
```

### Precedence Table

```
1. Ternary     ? :     (lowest)
2. Equality   == !=
3. Comparison < > <= >=
4. Term       + - ++
5. Factor     * / %
6. Pipe       />
7. Unary      -
8. Call       fn()
9. Primary    literals  (highest)
```

## AST Design

### Discriminated Unions

```typescript
type Expr =
  | { type: "NumberLiteral"; value: number; line: number }
  | { type: "StringLiteral"; value: string; line: number }
  | { type: "Identifier"; name: string; line: number }
  | { type: "BinaryExpr"; op: string; left: Expr; right: Expr; line: number }
  | { type: "PipeExpr"; left: Expr; right: Expr; line: number }
  | { type: "CallExpr"; callee: Expr; args: Expr[]; line: number };

type Stmt =
  | { type: "LetStmt"; name: string; value: Expr; line: number }
  | { type: "ExprStmt"; expression: Expr; line: number };
```

## Interpreter Design

### Tree-Walk Pattern

```typescript
class Interpreter {
  private env = new Environment();

  evaluate(expr: Expr): Value {
    switch (expr.type) {
      case "NumberLiteral":
        return expr.value;

      case "BinaryExpr":
        const left = this.evaluate(expr.left);
        const right = this.evaluate(expr.right);
        return this.applyOperator(expr.op, left, right);

      case "PipeExpr":
        const value = this.evaluate(expr.left);
        const fn = this.evaluate(expr.right);
        return this.call(fn, [value]);

      case "Identifier":
        return this.env.get(expr.name);
    }
  }
}
```

### Environment (Scope)

```typescript
class Environment {
  private values = new Map<string, Value>();
  private parent?: Environment;

  constructor(parent?: Environment) {
    this.parent = parent;
  }

  define(name: string, value: Value): void {
    this.values.set(name, value);
  }

  get(name: string): Value {
    if (this.values.has(name)) return this.values.get(name)!;
    if (this.parent) return this.parent.get(name);
    throw new RuntimeError(`Undefined variable: ${name}`);
  }
}
```

## Reference Files

- [references/error-handling.md](references/error-handling.md) - Error recovery patterns
- [references/builtins.md](references/builtins.md) - Builtin function design
