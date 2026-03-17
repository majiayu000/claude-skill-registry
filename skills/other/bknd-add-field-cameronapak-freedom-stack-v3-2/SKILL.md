---
name: bknd-add-field
description: Use when adding a field to an existing Bknd entity. Covers all field types (text, number, boolean, date, enum, json, jsonschema, media), field modifiers (.required(), .unique(), .default()), validation options, and UI vs code approaches.
---

# Add Field to Entity

Add a new field (column) to an existing entity in Bknd.

## Prerequisites

- Existing Bknd entity (see `bknd-create-entity`)
- For code mode: Access to your schema file

## When to Use UI vs Code

### Use UI Mode When
- Quick iteration/prototyping
- Non-developer adding fields
- Testing field configurations before coding

### Use Code Mode When
- Version control needed
- Reproducible schema changes
- Type safety required
- Team collaboration

## UI Approach

### Step 1: Access Entity

1. Start server: `npx bknd run`
2. Open `http://localhost:1337`
3. Navigate to **Data** section
4. Click on the target entity (e.g., `posts`)

### Step 2: Add Field

1. Click **+ Add Field**
2. Select field type from dropdown:
   - **Text**: Strings, emails, URLs
   - **Number**: Integers, decimals
   - **Boolean**: True/false
   - **Date**: Timestamps
   - **Enum**: Fixed set of values
   - **JSON**: Unstructured data
3. Enter field name (snake_case: `first_name`, `created_at`)

### Step 3: Configure Options

Based on field type, configure:

**All Types:**
- **Required**: Toggle on if field cannot be null
- **Default Value**: Set a default

**Text:**
- Min/Max Length
- Pattern (regex validation)

**Number:**
- Minimum/Maximum values
- Multiple Of (for integers)

**Enum:**
- Add enum values (one per line)

### Step 4: Save and Sync

1. Click **Save Field**
2. Click **Sync Database** to apply changes

## Code Approach

### Step 1: Locate Entity Definition

Find your entity in the schema:

```typescript
const schema = em({
  posts: entity("posts", {
    title: text().required(),
    // Add new fields here
  }),
});
```

### Step 2: Add Field

Add the new field to the entity's field object:

```typescript
const schema = em({
  posts: entity("posts", {
    title: text().required(),
    subtitle: text(),           // NEW: optional text field
    view_count: number(),       // NEW: optional number field
  }),
});
```

### Step 3: Restart Server

Bknd auto-syncs schema on startup. Restart your server to apply changes.

## Field Types Reference

### Text Field

```typescript
import { text } from "bknd";

entity("users", {
  // Basic optional text
  bio: text(),

  // Required text
  email: text().required(),

  // Unique constraint
  username: text().unique(),

  // With validation
  slug: text({
    minLength: 3,
    maxLength: 100,
    pattern: "^[a-z0-9-]+$",
  }).required(),

  // With default value
  status: text({ default_value: "active" }),
})
```

### Number Field

```typescript
import { number } from "bknd";

entity("products", {
  // Basic number
  quantity: number(),

  // Required with validation
  price: number({
    minimum: 0,
    maximum: 99999.99,
  }).required(),

  // Integer only (multipleOf: 1)
  rating: number({
    minimum: 1,
    maximum: 5,
    multipleOf: 1,
  }),
})
```

### Boolean Field

```typescript
import { boolean } from "bknd";

entity("posts", {
  // Defaults to false
  published: boolean(),

  // Default true
  active: boolean({ default_value: true }),
})
```

### Date Field

```typescript
import { date } from "bknd";

entity("events", {
  // Basic date
  start_date: date().required(),

  // Auto-set to current time
  created_at: date({ default_value: "now" }),
})
```

### Enum Field

**Note:** Import is `enumm` (double 'm') to avoid JS reserved word.

```typescript
import { enumm } from "bknd";

entity("posts", {
  // Array syntax
  status: enumm({
    enum: ["draft", "published", "archived"],
    default_value: "draft",
  }).required(),

  // Object syntax (key-value)
  priority: enumm({
    enum: {
      LOW: "low",
      MEDIUM: "medium",
      HIGH: "high",
    },
    default_value: "MEDIUM",
  }),
})
```

### JSON Field

```typescript
import { json } from "bknd";

entity("users", {
  // Untyped JSON
  metadata: json(),

  // Typed JSON (TypeScript only, no runtime validation)
  preferences: json<{
    theme: "light" | "dark";
    notifications: boolean;
  }>(),

  // With default
  tags: json<string[]>({ default_value: [] }),
})
```

### JSON Schema Field

For runtime-validated JSON:

```typescript
import { jsonschema } from "bknd";

entity("webhooks", {
  payload: jsonschema({
    type: "object",
    properties: {
      event: { type: "string" },
      timestamp: { type: "number" },
    },
    required: ["event", "timestamp"],
  }),
})
```

### Media Field

For file attachments:

```typescript
import { media } from "bknd";

entity("posts", {
  // Single file
  cover_image: media({ entity: "posts" }),

  // Multiple files with constraints
  gallery: media({
    entity: "posts",
    min_items: 1,
    max_items: 10,
    mime_types: ["image/jpeg", "image/png", "image/webp"],
  }),
})
```

## Field Modifiers

Chain modifiers after field type:

| Modifier | Description | Example |
|----------|-------------|---------|
| `.required()` | Cannot be null | `text().required()` |
| `.unique()` | Unique constraint | `text().unique()` |
| `.default(value)` | Default value | `text().default("pending")` |
| `.references(target)` | Foreign key | `number().references("users.id")` |

**Chaining example:**

```typescript
entity("users", {
  email: text().required().unique(),
  role: text().default("user"),
  org_id: number().references("organizations.id"),
})
```

## Field Naming Conventions

| Convention | Example | Notes |
|------------|---------|-------|
| snake_case | `first_name` | NOT `firstName` |
| Lowercase | `created_at` | NOT `CreatedAt` |
| Descriptive | `published_at` | NOT `pub` |

## Common Pitfalls

### Field Already Exists

**Error:** `Field "title" already exists on entity "posts"`

**Fix:** Each field name must be unique within an entity. Choose a different name.

### Invalid Field Name

**Error:** `Invalid field name`

**Fix:** Use lowercase letters, numbers, and underscores. Must start with letter.

```typescript
// Valid
title: text()
first_name: text()
item_2: text()

// Invalid
Title: text()        // No uppercase
2_item: text()       // Can't start with number
first-name: text()   // No hyphens
```

### Enum Import Mistake

**Error:** `enum is a reserved word`

**Fix:** Import and use `enumm` (double 'm'):

```typescript
// Wrong
import { enum } from "bknd";

// Correct
import { enumm } from "bknd";

status: enumm({ enum: ["a", "b"] })
```

### Missing Required Modifier on Existing Data

**Problem:** Adding `.required()` to field on entity with existing null values.

**Fix:** Either:
1. Update existing records to have non-null values first
2. Add a default value: `text({ default_value: "N/A" }).required()`
3. Keep field optional

### Field Changes Not Reflecting

**Problem:** Added field in code but not appearing.

**Fixes:**
1. Restart the server (schema syncs on startup)
2. Verify field is in the correct entity definition
3. Check for syntax errors in schema

## Verification

### UI Mode
1. Click on entity in Data section
2. Verify new field appears in field list
3. Create a test record with the new field

### Code Mode
```typescript
const api = app.getApi();

// Create record with new field
const result = await api.data.createOne("posts", {
  title: "Test",
  subtitle: "New field test",  // Your new field
});
console.log(result);
```

### CLI Check
```bash
npx bknd debug paths
# Check entity fields in output
```

## DOs and DON'Ts

**DO:**
- Use snake_case for field names
- Start with optional fields; make required later if needed
- Add default values for required fields on existing data
- Use appropriate field types (don't store numbers as text)

**DON'T:**
- Use `enum` import (use `enumm`)
- Add `.required()` to existing entities without defaults
- Use camelCase or PascalCase for field names
- Create redundant fields (e.g., `id` is auto-generated)

## Related Skills

- **bknd-create-entity** - Create a new entity first
- **bknd-define-relationship** - Add relationships between entities
- **bknd-modify-schema** - Rename or change field types
- **bknd-crud-create** - Insert data using new fields
