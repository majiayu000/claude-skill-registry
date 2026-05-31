---
name: nestjs-drizzle-crud-generator
description: Generates complete CRUD modules for NestJS applications with Drizzle ORM. Use when building server-side features in NestJS that require database operations, including creating new entities with full CRUD endpoints, services with Drizzle queries, Zod-validated DTOs, and unit tests. Triggered by requests like "generate a user module", "create a product CRUD", "add a new entity with endpoints", or when setting up database-backed features in NestJS.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# NestJS Drizzle CRUD Generator

## Overview

Automatically generates complete CRUD modules for NestJS applications using Drizzle ORM. Creates all necessary files following the zaccheroni-monorepo patterns: feature modules, controllers, services, Zod-validated DTOs, Drizzle schemas, and Jest unit tests.

## When to Use

- Creating new entity modules with full CRUD endpoints
- Building database-backed features in NestJS
- Generating type-safe DTOs with Zod validation
- Adding services with Drizzle ORM queries
- Creating unit tests with mocked database

## Instructions

### Step 1: Define Entity Fields

Gather entity definition:
- Entity name (e.g., `user`, `product`, `order`)
- List of fields with types (see `references/field-types.md` for supported types)
- Required fields vs optional fields with defaults

### Step 2: Run the Generator

```bash
python scripts/generate_crud.py --feature <name> --fields '<json-array>' --output <path>
```

### Step 3: Verify Generated Files

Check that all expected files were created:

```bash
ls -la libs/server/<feature-name>/src/lib/
```

Expected structure:
```
controllers/
services/
dto/
schema/
<feature>-feature.module.ts
```

### Step 4: Run TypeScript Compilation

```bash
cd libs/server && npx tsc --noEmit
```

### Step 5: Execute Unit Tests

```bash
cd libs/server && npm test -- --testPathPattern=<feature-name>
```

## Examples

### Generate a User module

```bash
python scripts/generate_crud.py \
  --feature user \
  --fields '[{"name": "name", "type": "string", "required": true}, {"name": "email", "type": "email", "required": true}, {"name": "password", "type": "string", "required": true}]' \
  --output ./libs/server
```

### Generate a Product module

```bash
python scripts/generate_crud.py \
  --feature product \
  --fields '[{"name": "title", "type": "string", "required": true}, {"name": "price", "type": "number", "required": true}, {"name": "description", "type": "text", "required": false}, {"name": "inStock", "type": "boolean", "required": false, "default": true}]' \
  --output ./libs/server
```

## Generated Structure

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

## Dependencies

Required packages:
- `@nestjs/common`
- `@nestjs/core`
- `drizzle-orm`
- `drizzle-zod`
- `zod`
- `nestjs-zod`

## Best Practices

1. **Verify before commit**: Always run `tsc --noEmit` and tests before committing generated code
2. **Customize services**: Add business logic to generated services after validation
3. **Database migrations**: Create migrations separately for generated Drizzle schemas
4. **Use generated types**: Reference generated types in your application code
5. **Review DTOs**: Adjust Zod validation rules based on your API requirements

## Constraints and Warnings

- **Soft delete only**: Delete operations use soft delete (`deletedAt` timestamp). Hard deletes require manual modification
- **No authentication**: Generated code does not include auth guards - add them based on your security requirements
- **Basic CRUD only**: Complex queries, transactions, or business logic must be implemented manually
- **JSON escaping**: Use single quotes around the JSON array when passing fields on command line
