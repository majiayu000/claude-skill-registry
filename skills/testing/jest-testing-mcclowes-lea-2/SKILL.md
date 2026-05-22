---
name: jest-testing
# prettier-ignore
description: Use when writing Jest tests - covers testing patterns for interpreters, parsers, and async code
---

# Jest Testing Best Practices

## Quick Start

```typescript
import { run } from "../src/api";

describe("interpreter", () => {
  it("evaluates arithmetic expressions", () => {
    expect(run("2 + 3")).toBe(5);
  });

  it("handles errors gracefully", () => {
    expect(() => run("undefined_var")).toThrow(/undefined/i);
  });
});
```

## Core Principles

- **Arrange-Act-Assert**: Structure tests clearly
- **One assertion focus**: Test one behavior per test
- **Descriptive names**: Use "should" or behavior-based naming
- **Isolation**: Tests should not depend on each other

## Testing Patterns

### Interpreter Tests

```typescript
describe("builtins", () => {
  describe("map", () => {
    it("transforms each element", () => {
      const code = `[1, 2, 3] /> map((x) -> x * 2)`;
      expect(run(code)).toEqual([2, 4, 6]);
    });

    it("passes index as second argument", () => {
      const code = `["a", "b"] /> map((x, i) -> i)`;
      expect(run(code)).toEqual([0, 1]);
    });
  });
});
```

### Parser Tests

```typescript
describe("parser", () => {
  it("parses pipe expressions", () => {
    const ast = parse("x /> fn");
    expect(ast.body[0]).toMatchObject({
      type: "ExprStmt",
      expression: {
        type: "PipeExpr",
        left: { type: "Identifier", name: "x" },
        right: { type: "Identifier", name: "fn" }
      }
    });
  });
});
```

### Async Tests

```typescript
it("resolves async operations", async () => {
  const result = await run(`
    let fetch = () -> delay(10) /> then(() -> "done") #async
    await fetch()
  `);
  expect(result).toBe("done");
});
```

### Snapshot Tests

```typescript
it("formats code consistently", () => {
  const formatted = format("let x=1+2");
  expect(formatted).toMatchSnapshot();
});
```

## Configuration

```javascript
// jest.config.js
module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  testMatch: ["**/__tests__/**/*.test.ts"],
  collectCoverageFrom: ["src/**/*.ts", "!src/**/*.d.ts"],
};
```

## Reference Files

- [references/mocking.md](references/mocking.md) - Mocking strategies
- [references/async-testing.md](references/async-testing.md) - Async test patterns
