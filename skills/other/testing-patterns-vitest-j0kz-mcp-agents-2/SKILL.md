---
name: testing-patterns-vitest
description: "Vitest testing conventions and patterns for @j0kz/mcp-agents including test organization, naming, assertion patterns, mocking strategies, and coverage targets (75%). Use when writing tests, organiz..."
---

# Vitest Testing Patterns for @j0kz/mcp-agents

Comprehensive testing patterns and conventions using Vitest 3.2.4 across the monorepo.

## When to Use This Skill

- Writing new test files
- Organizing test suites
- Debugging test failures
- Improving test coverage
- Setting up mocks and spies
- Writing integration tests

## Evidence Base

**Current Testing Stats:**
- 632+ passing tests across 11 packages
- Vitest 3.2.4 with v8 coverage
- 75% coverage target (packages/shared/vitest.config.ts)
- Test files: *.test.ts pattern
- Parallel execution (max 4 threads)

---

## Quick Start

### Generate Tests Automatically

```bash
# Generate comprehensive tests for any file
npx @j0kz/test-generator@latest generate src/your-file.ts

# With specific framework
npx @j0kz/test-generator@latest generate src/your-file.ts --framework=vitest

# Include edge cases
npx @j0kz/test-generator@latest generate src/your-file.ts --edge-cases --error-cases
```

### Run Tests

```bash
# Run all tests
npm test

# Run specific package tests
npm test -- packages/smart-reviewer-mcp

# Watch mode
npm test -- --watch

# Coverage report
npm test -- --coverage

# Run specific test file
npx vitest run src/analyzer.test.ts
```

---

## Test Organization

### File Structure

```
packages/
  your-package/
    src/
      analyzer.ts          # Source file
    tests/
      analyzer.test.ts     # Test file
    vitest.config.ts       # Package config
```

### Test File Template

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { YourClass } from '../src/your-class.js';

describe('YourClass', () => {
  let instance: YourClass;

  beforeEach(() => {
    instance = new YourClass();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('methodName', () => {
    it('should handle normal case', () => {
      // Arrange
      const input = 'test';

      // Act
      const result = instance.methodName(input);

      // Assert
      expect(result).toBe('expected');
    });

    it('should handle edge case', () => {
      // Test edge cases
    });

    it('should handle error case', () => {
      // Test error handling
    });
  });
});
```

---

## Assertion Patterns

For comprehensive assertion patterns and examples:

```bash
cat .claude/skills/testing-patterns-vitest/references/assertion-patterns-guide.md
```

### Quick Reference

```typescript
// Basic assertions
expect(value).toBe(expected);
expect(value).toEqual(expected);
expect(value).toBeDefined();
expect(value).toBeTruthy();

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toMatchObject({ key: 'value' });

// Errors
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('specific message');

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```

---

## Mocking Strategies

For detailed mocking patterns:

```bash
cat .claude/skills/testing-patterns-vitest/references/mocking-strategies-guide.md
```

### Quick Examples

```typescript
// Mock module
vi.mock('../src/utils.js', () => ({
  utilFunction: vi.fn().mockReturnValue('mocked')
}));

// Spy on method
const spy = vi.spyOn(instance, 'method');
expect(spy).toHaveBeenCalledWith('arg');

// Mock file system
vi.mock('fs/promises', () => ({
  readFile: vi.fn().mockResolvedValue('content'),
  writeFile: vi.fn().mockResolvedValue(undefined)
}));
```

---

## Coverage Guidelines

For comprehensive coverage guide:

```bash
cat .claude/skills/testing-patterns-vitest/references/coverage-guide.md
```

### Coverage Targets

- **Minimum:** 75% overall
- **Goal:** 80%+ for critical packages
- **Exclude:** dist/, node_modules/, *.config.ts

### Check Coverage

```bash
# Generate coverage report
npm test -- --coverage

# Open HTML report
open coverage/index.html

# Check if meeting threshold
npm run test:coverage:check
```

---

## Common Test Patterns

### Testing Async Functions

```typescript
it('should handle async operations', async () => {
  const result = await asyncFunction();
  expect(result).toBe('expected');
});

it('should handle async errors', async () => {
  await expect(asyncFunction()).rejects.toThrow('error message');
});
```

### Testing Classes

```typescript
describe('MyClass', () => {
  let instance: MyClass;

  beforeEach(() => {
    instance = new MyClass();
  });

  it('should initialize with defaults', () => {
    expect(instance.property).toBe('default');
  });

  it('should update state', () => {
    instance.updateState('new');
    expect(instance.property).toBe('new');
  });
});
```

### Testing with Files

```typescript
import { vi } from 'vitest';
import * as fs from 'fs/promises';

vi.mock('fs/promises');

it('should read file', async () => {
  vi.mocked(fs.readFile).mockResolvedValue('content');

  const result = await readConfig('config.json');

  expect(fs.readFile).toHaveBeenCalledWith('config.json', 'utf-8');
  expect(result).toBe('content');
});
```

---

## Debugging Test Failures

For comprehensive debugging strategies:

```bash
cat .claude/skills/testing-patterns-vitest/references/debugging-test-failures-guide.md
```

### Quick Debug Tips

```bash
# Run single test with verbose output
npx vitest run src/analyzer.test.ts --reporter=verbose

# Run with Node debugging
node --inspect-brk ./node_modules/.bin/vitest run

# Show full error stacks
npx vitest run --full-trace

# Run specific test by name
npx vitest run -t "should handle edge case"
```

---

## Integration Testing

### Testing MCP Tools

```typescript
describe('MCP Tool Integration', () => {
  it('should handle tool execution', async () => {
    const server = new Server();

    const request = {
      method: 'tools/call',
      params: {
        name: 'analyze',
        arguments: { path: './src' }
      }
    };

    const response = await server.handleRequest(request);

    expect(response).toHaveProperty('success', true);
    expect(response).toHaveProperty('data');
  });
});
```

### Testing with Real Files

```typescript
import { mkdtemp, rm } from 'fs/promises';
import { tmpdir } from 'os';
import { join } from 'path';

describe('File Operations', () => {
  let tempDir: string;

  beforeEach(async () => {
    tempDir = await mkdtemp(join(tmpdir(), 'test-'));
  });

  afterEach(async () => {
    await rm(tempDir, { recursive: true });
  });

  it('should process files', async () => {
    // Use tempDir for test files
  });
});
```

---

## Best Practices

1. **Follow AAA Pattern:** Arrange, Act, Assert
2. **One assertion per test** (when practical)
3. **Descriptive test names** that explain what and why
4. **Test behavior, not implementation**
5. **Clean up after tests** (restore mocks, delete temp files)
6. **Group related tests** with describe blocks
7. **Test edge cases and errors**, not just happy path
8. **Keep tests fast** (<100ms per test ideal)
9. **Avoid test interdependence**
10. **Use data-driven tests** for multiple scenarios

---

## Example: Complete Test Suite

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { SecurityScanner } from '../src/scanner.js';
import * as fs from 'fs/promises';

vi.mock('fs/promises');

describe('SecurityScanner', () => {
  let scanner: SecurityScanner;

  beforeEach(() => {
    scanner = new SecurityScanner();
    vi.clearAllMocks();
  });

  describe('scan', () => {
    it('should detect SQL injection', async () => {
      const code = "query = 'SELECT * FROM users WHERE id = ' + userId;";
      const result = await scanner.scan(code);

      expect(result.issues).toHaveLength(1);
      expect(result.issues[0].type).toBe('sql-injection');
    });

    it('should handle file read errors', async () => {
      vi.mocked(fs.readFile).mockRejectedValue(new Error('File not found'));

      await expect(scanner.scanFile('missing.ts')).rejects.toThrow('File not found');
    });

    it('should skip binary files', async () => {
      const result = await scanner.scan('image.png');

      expect(result.skipped).toBe(true);
      expect(result.reason).toBe('binary file');
    });
  });
});
```

---

**Verification:** Run `npm test` to see 632+ tests passing!