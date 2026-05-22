---
name: test-schema
description: Write tests for Zod schemas. Use when testing entity schemas, DTO validation, query parameter schemas, or any schema validation rules. Triggers on "test schema", "schema tests", "test validation", "test zod".
---

# Test Schema

Write Vitest tests for Zod schemas in this backend template.

## Quick Reference

**Location**: `tests/schemas/{entity-name}.schema.test.ts`
**Run tests**: `pnpm test -- tests/schemas/{entity-name}.schema.test.ts`
**Watch mode**: `pnpm test:watch`

## Instructions

### Step 1: Create the Test File

Create `tests/schemas/{entity-name}.schema.test.ts` mirroring the source structure.

### Step 2: Import Dependencies

```typescript
import { describe, it, expect } from "vitest";
import {
  {entity}Schema,
  create{Entity}Schema,
  update{Entity}Schema,
  {entity}QueryParamsSchema,
} from "@/schemas/{entity-name}.schema";
```

### Step 3: Test Each Schema

Create a `describe` block for each schema with focused test cases.

## Test Patterns

### Base Entity Schema Tests

```typescript
describe("{entity}Schema", () => {
  it("accepts valid {entity}", () => {
    const valid = {
      id: "1",
      // ... all required fields with valid values
      createdBy: "user-1",
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    expect({entity}Schema.parse(valid)).toEqual(valid);
  });

  it("rejects missing required fields", () => {
    expect(() => {entity}Schema.parse({})).toThrow();
  });

  it("rejects invalid field types", () => {
    expect(() =>
      {entity}Schema.parse({
        id: 123, // should be string
        // ... other fields
      })
    ).toThrow();
  });

  it("accepts optional timestamps as undefined", () => {
    const valid = {
      id: "1",
      // ... required fields only, no timestamps
      createdBy: "user-1",
    };
    expect({entity}Schema.parse(valid)).toMatchObject({ id: "1" });
  });
});
```

### Create DTO Schema Tests

```typescript
describe("create{Entity}Schema", () => {
  it("accepts valid create data", () => {
    const valid = {
      // Only fields that user provides (no id, createdBy, timestamps)
      fieldName: "value",
    };
    expect(create{Entity}Schema.parse(valid)).toEqual(valid);
  });

  it("rejects empty required fields", () => {
    expect(() => create{Entity}Schema.parse({ fieldName: "" })).toThrow();
  });

  it("rejects missing required fields", () => {
    expect(() => create{Entity}Schema.parse({})).toThrow();
  });

  it("strips unknown fields", () => {
    const input = { fieldName: "value", unknownField: "ignored" };
    const parsed = create{Entity}Schema.parse(input);
    expect(parsed).not.toHaveProperty("unknownField");
  });
});
```

### Update DTO Schema Tests

```typescript
describe("update{Entity}Schema", () => {
  it("accepts partial update", () => {
    expect(update{Entity}Schema.parse({ fieldName: "updated" })).toEqual({
      fieldName: "updated",
    });
  });

  it("accepts empty object (no fields to update)", () => {
    expect(update{Entity}Schema.parse({})).toEqual({});
  });

  it("accepts multiple fields", () => {
    const update = { field1: "new1", field2: "new2" };
    expect(update{Entity}Schema.parse(update)).toEqual(update);
  });
});
```

### Query Parameters Schema Tests

```typescript
describe("{entity}QueryParamsSchema", () => {
  it("accepts empty object (all optional)", () => {
    expect({entity}QueryParamsSchema.parse({})).toEqual({});
  });

  it("coerces page and limit to numbers", () => {
    const parsed = {entity}QueryParamsSchema.parse({ page: "2", limit: "5" });
    expect(parsed.page).toBe(2);
    expect(parsed.limit).toBe(5);
  });

  it("accepts valid sortOrder values", () => {
    expect({entity}QueryParamsSchema.parse({ sortOrder: "asc" }).sortOrder).toBe("asc");
    expect({entity}QueryParamsSchema.parse({ sortOrder: "desc" }).sortOrder).toBe("desc");
  });

  it("rejects invalid sortOrder", () => {
    expect(() => {entity}QueryParamsSchema.parse({ sortOrder: "invalid" })).toThrow();
  });

  it("accepts entity-specific filters", () => {
    // Test any custom filters added to the query params
    expect({entity}QueryParamsSchema.parse({ createdBy: "user-1" }).createdBy).toBe("user-1");
  });
});
```

### ID Schema Tests (if separate)

```typescript
describe("{entity}IdSchema", () => {
  it("accepts valid string ID", () => {
    expect({entity}IdSchema.parse("abc-123")).toBe("abc-123");
  });

  it("rejects non-string ID", () => {
    expect(() => {entity}IdSchema.parse(123)).toThrow();
  });
});
```

## Testing Guidelines

### What to Test

1. **Happy path** - Valid data passes validation
2. **Missing required fields** - Schema rejects incomplete data
3. **Invalid types** - Wrong data types are rejected
4. **Empty strings** - Required strings with `.min(1)` reject empty
5. **Enum values** - Only valid enum values accepted
6. **Coercion** - Query params coerce strings to numbers
7. **Optional fields** - Can be omitted without error
8. **Default values** - Defaults are applied correctly

### Test Naming Conventions

Use descriptive `it` statements:

- `"accepts valid {entity}"` - Happy path
- `"rejects missing required fields"` - Validation failure
- `"rejects invalid {field}"` - Specific field validation
- `"coerces {field} to {type}"` - Type coercion
- `"accepts optional {field} as undefined"` - Optional handling
- `"applies default value for {field}"` - Default behavior

### Import Rules

- Always use path aliases: `import { x } from "@/schemas/..."`
- Import from vitest: `describe`, `it`, `expect`
- Import `z` from zod only if testing generic schemas

## Complete Example

See `tests/schemas/note.schema.test.ts`:

```typescript
import { describe, it, expect } from "vitest";
import {
  noteSchema,
  createNoteSchema,
  updateNoteSchema,
  noteQueryParamsSchema,
} from "@/schemas/note.schema";

describe("noteSchema", () => {
  it("accepts valid note", () => {
    const valid = {
      id: "1",
      content: "Hello",
      createdBy: "user-1",
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    expect(noteSchema.parse(valid)).toEqual(valid);
  });

  it("rejects missing required fields", () => {
    expect(() => noteSchema.parse({})).toThrow();
  });
});

describe("createNoteSchema", () => {
  it("accepts valid create note", () => {
    expect(createNoteSchema.parse({ content: "Hi" })).toEqual({
      content: "Hi",
    });
  });

  it("rejects empty content", () => {
    expect(() => createNoteSchema.parse({ content: "" })).toThrow();
  });

  it("rejects missing content", () => {
    expect(() => createNoteSchema.parse({})).toThrow();
  });
});

describe("updateNoteSchema", () => {
  it("accepts partial update", () => {
    expect(updateNoteSchema.parse({ content: "Updated" })).toEqual({
      content: "Updated",
    });
  });

  it("accepts empty object (no update)", () => {
    expect(updateNoteSchema.parse({})).toEqual({});
  });
});

describe("noteQueryParamsSchema", () => {
  it("coerces page and limit to numbers", () => {
    const parsed = noteQueryParamsSchema.parse({ page: "2", limit: "5" });
    expect(parsed.page).toBe(2);
    expect(parsed.limit).toBe(5);
  });

  it("accepts optional createdBy", () => {
    expect(noteQueryParamsSchema.parse({ createdBy: "user-1" }).createdBy).toBe(
      "user-1",
    );
  });

  it("accepts empty object (all optional)", () => {
    expect(noteQueryParamsSchema.parse({})).toEqual({});
  });
});
```

## What NOT to Do

- Do NOT test implementation details - test behavior
- Do NOT use snapshots for simple schema validation
- Do NOT mock Zod - test actual schema parsing
- Do NOT skip edge cases - empty strings, wrong types, missing fields
- Do NOT forget to test coercion for query parameters
