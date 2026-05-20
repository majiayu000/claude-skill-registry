---
name: nestjs-drizzle-crud-generator
description: Generates complete CRUD modules for NestJS applications with Drizzle ORM. Use when building server-side features in NestJS that require database operations, including creating new entities with full CRUD endpoints, services with Drizzle queries, Zod-validated DTOs, and unit tests. Triggered by requests like "generate a user module", "create a product CRUD", "add a new entity with endpoints", or when setting up database-backed features in NestJS.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# NestJS Drizzle CRUD Generator

## Overview

This skill automatically generates complete CRUD (Create, Read, Update, Delete) modules for NestJS applications using Drizzle ORM. It creates all necessary files following the zaccheroni-monorepo patterns.

## When to Use

- Creating new entity modules with full CRUD endpoints
- Building database-backed features in NestJS
- Generating type-safe DTOs with Zod validation
- Adding services with Drizzle ORM queries
- Creating unit tests with mocked database

## Instructions

### Step 1: Identify Feature Requirements

Before generating, gather:
- Entity name (e.g., `user`, `product`, `order`)
- List of fields with types
- Required fields vs optional fields

### Step 2: Run the Generator

Execute the generation script:

```bash
python scripts/generate_crud.py --feature <name> --fields '<json-array>' --output <path>
```

### Step 3: Field Definition Format

Fields must be defined as JSON array with name, type, and required properties.

### Step 4: Integrate Module

After generation, integrate the module into your NestJS application.

## Examples

### Example 1: Generate a User module

```bash
python scripts/generate_crud.py \
  --feature user \
  --fields '[{"name": "name", "type": "string", "required": true}, {"name": "email", "type": "string", "required": true}, {"name": "password", "type": "string", "required": true}]' \
  --output ./libs/server
```

### Example 2: Generate a Product module

```bash
python scripts/generate_crud.py \
  --feature product \
  --fields '[{"name": "title", "type": "string", "required": true}, {"name": "price", "type": "number", "required": true}, {"name": "description", "type": "text", "required": false}, {"name": "inStock", "type": "boolean", "required": false, "default": true}]' \
  --output ./libs/server
```

## Quick Start

### Step 1: Identify Feature Requirements

Before generating, gather:
- Entity name (e.g., `user`, `product`, `order`)
- List of fields with types
- Required fields vs optional fields

### Step 2: Run the Generator

Execute the generation script:

```bash
python scripts/generate_crud.py --feature <name> --fields '<json-array>' --output <path>
```

### Step 3: Field Definition Format

Fields must be defined as JSON array:

```json
[
  {"name": "name", "type": "string", "required": true},
  {"name": "email", "type": "string", "required": true},
  {"name": "age", "type": "integer", "required": false},
  {"name": "isActive", "type": "boolean", "required": false, "default": true},
  {"name": "price", "type": "number", "required": true},
  {"name": "description", "type": "text", "required": false},
  {"name": "uuid", "type": "uuid", "required": false}
]
```

### Step 4: Example Commands

Generate a User module:
```bash
python scripts/generate_crud.py \
  --feature user \
  --fields '[{"name": "name", "type": "string", "required": true}, {"name": "email", "type": "string", "required": true}, {"name": "password", "type": "string", "required": true}]' \
  --output ./libs/server
```

Generate a Product module:
```bash
python scripts/generate_crud.py \
  --feature product \
  --fields '[{"name": "title", "type": "string", "required": true}, {"name": "price", "type": "number", "required": true}, {"name": "description", "type": "text", "required": false}, {"name": "inStock", "type": "boolean", "required": false, "default": true}]' \
  --output ./libs/server
```

## Generated Structure

The generator creates this directory structure:

```
libs/server/{feature-name}/
├── src/
│   ├── index.ts
│   └── lib/
│       ├── {feature}-feature.module.ts
│       ├── controllers/
│       │   ├── index.ts
│       │   └── {feature}.controller.ts
│       ├── services/
│       │   ├── index.ts
│       │   ├── {feature}.service.ts
│       │   └── {feature}.service.spec.ts
│       ├── dto/
│       │   ├── index.ts
│       │   └── {feature}.dto.ts
│       └── schema/
│           └── {feature}.table.ts
```

## Supported Field Types

| Type | Drizzle Column | Zod Schema |
|------|---------------|------------|
| string | text | z.string() |
| text | text | z.string() |
| number | real | z.number() |
| integer | integer | z.number().int() |
| boolean | boolean | z.boolean() |
| date | timestamp | z.date() |
| uuid | uuid | z.string().uuid() |
| email | text | z.string().email() |

## Features

### Module
- Uses `forRootAsync` pattern for lazy configuration
- Exports generated service for other modules
- Imports DatabaseModule for feature tables

### Controller
- Full CRUD endpoints: POST, GET, PATCH, DELETE
- Query parameter validation for pagination
- Zod validation pipe integration

### Service
- Drizzle ORM query methods
- Soft delete support (via `deletedAt` column)
- Pagination with limit/offset
- Filtering support
- Type-safe return types

### DTOs
- Zod schemas for Create and Update
- Query parameter schemas for filtering
- NestJS DTO integration

### Tests
- Jest test suite
- Mocked Drizzle database
- Test cases for all CRUD operations

## Manual Integration

After generation, integrate into your app module:

```typescript
// app.module.ts
import { {{FeatureName}}FeatureModule } from '@your-org/server-{{feature}}';

@Module({
  imports: [
    {{FeatureName}}FeatureModule.forRootAsync({
      useFactory: () => ({
        defaultPageSize: 10,
        maxPageSize: 100,
      }),
    }),
  ],
})
export class AppModule {}
```

## Field Options

Each field supports:
- `name`: Field name
- `type`: Data type (string, text, number, integer, boolean, date, uuid, email)
- `required`: Boolean for mandatory fields
- `default`: Default value for non-required fields
- `maxLength`: Maximum length for strings
- `minLength`: Minimum length for strings

## Dependencies

The generated code requires:
- `@nestjs/common`
- `@nestjs/core`
- `drizzle-orm`
- `drizzle-zod`
- `zod`
- `nestjs-zod`

## Best Practices

1. **Verify generated code**: Always review generated files before committing
2. **Run tests**: Execute unit tests to verify the generated code works
3. **Customize as needed**: Add business logic to services after generation
4. **Database migrations**: Manually create migrations for the generated schema
5. **Type safety**: Use the generated types in your application code

## Constraints and Warnings

- **Soft delete only**: The generated delete method uses soft delete (sets `deletedAt`). Hard deletes require manual modification
- **No authentication**: Generated code does not include auth guards - add them separately
- **Basic CRUD only**: Complex queries or business logic must be implemented manually
- **JSON field escaping**: When passing fields JSON on command line, use single quotes around the JSON array

