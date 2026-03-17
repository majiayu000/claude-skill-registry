---
name: write-unit-test
description: Generate behavioral unit tests from functional specifications using PreDB/PostDB pattern. Use when user provides specs with PreDB/Workflow/PostDB structure or asks to write tests for a specification before implementation (TDD approach).
---

# Write Unit Test

## Purpose

Convert functional specifications into executable test code. Tests define the behavioral contract that the implementation must satisfy, following Test-Driven Development principles.

## When to Use

This skill should be used when:
- User provides functional specifications with PreDB/Workflow/PostDB structure
- User requests to "write tests" or "implement tests" for a spec
- Starting TDD workflow (tests first, implementation later)
- User says "create tests for this spec"

## Functional Specification Format

Specs follow a three-part structure for each scenario:

**PreDB**: Initial database state (CSV-like format)
```
table_name:
column1, column2, column3
value1, value2, value3
```

**Workflow**: Bullet points describing the sequence of actions
```
* Call `class.method(args)`
* [What happens internally]
* Returns [object type]
```

**PostDB**: Expected database state after execution (includes pre-existing + new rows)
```
table_name:
column1, column2, column3, column4
value1, value2, value3, newvalue
```

Use placeholders for runtime-generated values: `<uuid>`, `<timestamp>`, `<vector>`, `<1536-dim vector>`

## Test Generation Workflow

### 1. Parse the Specification

For each scenario in the spec:
- Extract test name from scenario title (convert to "should [action] when [condition]" format)
- Identify all tables and their initial states from PreDB
- Extract the method call from the first Workflow bullet
- Identify expected return values and database state from PostDB

### 2. Generate Test File Structure

Create test file at `[module]/tests/[class-name].test.ts`:

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { PreDB, PostDB } from '@/lib/db-test';
import { db } from '@/db';
import * as schema from '@/db/schema';
import { ClassName } from '@/path/to/class';

describe('ClassName', () => {
  let instance: ClassName;

  beforeEach(() => {
    instance = new ClassName(db);
  });

  const TEST_TIMEOUT = 120000; // For API calls

  it('[test name]', async () => {
    // PreDB: Setup
    await PreDB(db, schema, { /* ... */ });

    // Execute
    const result = await instance.method();

    // Assertions
    expect(result.field).toBe(expectedValue);

    // PostDB: Verify
    await PostDB(db, schema, { /* ... */ }, { allowExtraRows: true });
  }, TEST_TIMEOUT);
});
```

### 3. Translation Rules

**PreDB → PreDB**:
- Empty tables: `table: []`
- With data: Map CSV rows to objects with proper types
- Timestamps: Use `const now = new Date()`
- Vectors: Use `new Array(1536).fill(0.1)` for test data

**Workflow → Execution**:
- First bullet indicates the public method to call
- Only call the public method, not internal implementation details
- Add comment describing what the method does conceptually

**PostDB → Assertions + PostDB**:
- Derive assertions from expected values (types, ranges, specific values)
- Use `allowExtraRows: true` when pre-existing rows exist
- Only verify the new/changed data, reference actual result values

### 4. Complete All Scenarios

Generate one `it()` block per scenario in the specification. Include all scenarios to ensure comprehensive test coverage.

### 5. Report to User

Show the generated test file and explain:
- Tests will fail initially (no implementation yet)
- Tests define the contract for what needs to be implemented
- Tests document expected behavior

## Key Principles

**TDD Philosophy**:
- Tests are written BEFORE implementation exists
- Expected outcome: tests fail initially (red), then implementation makes them pass (green)
- Tests define the contract, not validate existing code

**Testing Approach**:
- Test behavior (what happens), not implementation (how it works)
- Use real database operations and real API calls (no mocks)
- Make tests readable with clear sections (PreDB, Execute, Verify)
- Use descriptive test names

**Avoid**:
- Mocks, spies, or stubs
- Testing private methods or internal state
- `.toHaveBeenCalledWith()` assertions
- Hardcoding generated values like UUIDs in assertions

## Reference Materials

For detailed translation rules, complete examples, and common patterns, refer to:
- `references/translation-guide.md`: Comprehensive spec-to-test examples, placeholder handling, multi-table scenarios, and best practices

## Required Context

Before generating tests, ensure access to:
1. The functional specification (PreDB/Workflow/PostDB)
2. The class/module name and import path
3. The database schema location (`db/schema.ts`)
4. Knowledge of which tables are involved

If any are missing, ask the user for clarification before proceeding.
