---
name: managing-database-schemas
description: Analyzes database schemas and suggests improvements for Prisma, TypeORM, or Drizzle. Use when the user asks about database schema, migrations, ORM setup, or wants to generate TypeScript types from database models.
---

# Database Schema Manager

## When to use this skill

- User asks to analyze or review database schema
- User wants to create or modify migrations
- User mentions Prisma, TypeORM, or Drizzle
- User asks to generate TypeScript types from schema
- User wants to detect schema issues or duplications

## Workflow

- [ ] Detect ORM/schema tool in use
- [ ] Read current schema files
- [ ] Analyze schema structure
- [ ] Identify issues and improvements
- [ ] Suggest DRY refactors if applicable
- [ ] Generate TypeScript types if requested

## Instructions

### Step 1: Detect Schema Tool

Check for ORM configurations:

| Tool    | Config Files                                      |
| ------- | ------------------------------------------------- |
| Prisma  | `prisma/schema.prisma`, `package.json` (prisma)   |
| TypeORM | `ormconfig.*`, `data-source.ts`, `typeorm` in pkg |
| Drizzle | `drizzle.config.*`, `drizzle` in package.json     |

```bash
ls prisma/schema.prisma 2>/dev/null && echo "Prisma"
ls drizzle.config.* 2>/dev/null && echo "Drizzle"
grep -l "typeorm\|TypeOrmModule" src/**/*.ts 2>/dev/null | head -1 && echo "TypeORM"
```

### Step 2: Read Schema Files

**Prisma:**

```bash
cat prisma/schema.prisma
```

**Drizzle:**

```bash
cat src/db/schema.ts src/db/schema/*.ts 2>/dev/null
```

**TypeORM:**

```bash
find src -name "*.entity.ts" -exec cat {} \;
```

### Step 3: Analyze Schema Structure

Extract and categorize:

- Models/tables and their fields
- Relationships (one-to-one, one-to-many, many-to-many)
- Indexes and constraints
- Enums and custom types

Look for:

- Field naming conventions
- Consistent timestamp fields (`createdAt`, `updatedAt`)
- Soft delete patterns (`deletedAt`)
- Audit fields consistency

### Step 4: Identify Issues

**Common schema issues:**

| Issue                  | Detection                      | Suggestion                      |
| ---------------------- | ------------------------------ | ------------------------------- |
| Missing indexes        | Foreign keys without `@index`  | Add index for query performance |
| Inconsistent naming    | Mixed `camelCase`/`snake_case` | Standardize naming convention   |
| Missing timestamps     | Tables without `createdAt`     | Add audit timestamps            |
| Duplicate field groups | Same fields across models      | Extract to shared type/mixin    |
| Missing relations      | IDs without `@relation`        | Add proper relation decorators  |
| N+1 risk               | Nested relations without eager | Document loading strategy       |

### Step 5: Suggest DRY Refactors

**Prisma — Abstract fields pattern:**

```prisma
// Before: Repeated in every model
model User {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  // ...
}

model Post {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  // ...
}
```

Document the pattern (Prisma doesn't support inheritance, but document for consistency):

```prisma
// Standard fields for all models:
// id        String   @id @default(cuid())
// createdAt DateTime @default(now())
// updatedAt DateTime @updatedAt
```

**Drizzle — Shared columns:**

```typescript
// src/db/shared.ts
import { timestamp, varchar } from "drizzle-orm/pg-core";

export const timestamps = {
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
};

export const primaryId = {
  id: varchar("id", { length: 36 }).primaryKey(),
};

// src/db/schema/users.ts
import { pgTable, varchar } from "drizzle-orm/pg-core";
import { primaryId, timestamps } from "../shared";

export const users = pgTable("users", {
  ...primaryId,
  ...timestamps,
  email: varchar("email", { length: 255 }).notNull().unique(),
});
```

**TypeORM — Base entity:**

```typescript
// src/entities/base.entity.ts
import {
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from "typeorm";

export abstract class BaseEntity {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}

// src/entities/user.entity.ts
import { Entity, Column } from "typeorm";
import { BaseEntity } from "./base.entity";

@Entity("users")
export class User extends BaseEntity {
  @Column({ unique: true })
  email: string;
}
```

### Step 6: Generate TypeScript Types

**From Prisma (built-in):**

```bash
npx prisma generate
# Types available at @prisma/client
```

**From Drizzle (built-in):**

```typescript
import { InferSelectModel, InferInsertModel } from "drizzle-orm";
import { users } from "./schema";

export type User = InferSelectModel<typeof users>;
export type NewUser = InferInsertModel<typeof users>;
```

**From TypeORM entities:**

```typescript
// Types are the entity classes themselves
import { User } from "./entities/user.entity";

// For DTOs, create separate types
export type CreateUserDto = Pick<User, "email" | "name">;
export type UpdateUserDto = Partial<CreateUserDto>;
```

## Migration Commands

**Prisma:**

```bash
# Create migration
npx prisma migrate dev --name <migration-name>

# Apply migrations (production)
npx prisma migrate deploy

# Reset database
npx prisma migrate reset

# View migration status
npx prisma migrate status
```

**Drizzle:**

```bash
# Generate migration
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push changes directly (dev only)
npx drizzle-kit push

# View schema diff
npx drizzle-kit diff
```

**TypeORM:**

```bash
# Generate migration
npx typeorm migration:generate -n <MigrationName>

# Run migrations
npx typeorm migration:run

# Revert last migration
npx typeorm migration:revert

# Show migrations
npx typeorm migration:show
```

## Schema Change Impact Analysis

When analyzing schema changes, report:

```markdown
## Schema Change Analysis

### Added

- `users.phoneNumber` (varchar, nullable) — No migration needed for existing data

### Modified

- `posts.status` enum — Added 'archived' value — Existing rows unaffected

### Removed

- `users.legacyId` — ⚠️ Ensure no code references before removing

### Index Changes

- Added index on `orders.userId` — Improves query performance, no data impact

### Breaking Changes

- ⚠️ `users.email` now NOT NULL — Requires data migration for null values
```

## Validation

Before completing:

- [ ] Schema syntax is valid
- [ ] All relations have proper back-references
- [ ] Indexes exist for foreign keys
- [ ] Naming conventions are consistent
- [ ] Migration files are generated if needed
- [ ] TypeScript types are in sync

## Error Handling

- **Schema validation fails**: Run ORM-specific validate command (`prisma validate`, etc.).
- **Migration conflicts**: Check migration history and resolve manually.
- **Type generation fails**: Ensure schema is valid and ORM client is installed.
- **Unsure about command**: Run `npx <tool> --help` for available options.

## Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Drizzle Documentation](https://orm.drizzle.team/docs/overview)
- [TypeORM Documentation](https://typeorm.io/)
