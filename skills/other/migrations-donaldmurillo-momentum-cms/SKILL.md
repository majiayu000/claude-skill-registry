---
name: migrations
description: Run migrations, generate schemas, and manage code generation for Momentum CMS. Use when working with database migrations, Drizzle schema generation, type generation, or Angular schematics.
argument-hint: <generate|run|status|rollback|codegen>
---

# Migrations & Code Generation

Reference for database migrations and type/config generation in the Momentum CMS monorepo.

## Arguments

- `$ARGUMENTS` - Operation: `generate`, `run`, `status`, `rollback`, or `codegen`

## Momentum Migration CLI (`@momentumcms/migrations`)

```bash
# In the monorepo (via Nx targets on example apps):
nx run example-angular:migrate:generate   # Diff schema, create migration file
nx run example-angular:migrate:run        # Apply pending migrations
nx run example-angular:migrate:status     # Show applied vs pending
nx run example-angular:migrate:rollback   # Rollback latest batch
```

## Drizzle Kit

```bash
nx run db-drizzle:generate-schema  # Generate schema from collections
npx drizzle-kit generate           # Create SQL migrations
npx drizzle-kit migrate            # Apply migrations
npx drizzle-kit push               # Direct push (dev only)
```

## Code Generation (Unified Generator)

The generator reads `momentum.config.ts` (server-side, Node) and outputs:

1. **TypeScript types** — interfaces for all collections, blocks, where clauses
2. **Browser-safe admin config** — inlined collections with server-only props stripped

```bash
nx run example-angular:generate          # One-shot generation
nx run example-angular:generate:watch    # Watch mode
```

## Angular Schematics

Both `@momentumcms/core` and `@momentumcms/migrations` ship Angular schematics:

```bash
# Type/config generation (in scaffolded Angular projects)
ng generate @momentumcms/core:types

# Migrations (in scaffolded Angular projects)
ng generate @momentumcms/migrations:generate
ng generate @momentumcms/migrations:run
ng generate @momentumcms/migrations:status
ng generate @momentumcms/migrations:rollback
```

## Workflow

1. Make collection changes in `libs/example-config/src/collections/`
2. Run `nx run example-angular:generate` to regenerate types + admin config
3. Run `nx run example-angular:migrate:generate` to create a migration file
4. Review the generated migration SQL
5. Run `nx run example-angular:migrate:run` to apply
