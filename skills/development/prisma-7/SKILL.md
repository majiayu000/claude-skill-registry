---
name: prisma-7
description: Prisma 7 ORM with Rust-free client, 90% smaller bundles, TypedSQL, Omit API, and ESM-first architecture. Use when working with database, schema, migrations, queries, or relations.
versions:
  prisma: 7.3
  nodejs: 20.19
  typescript: 5.4
user-invocable: true
references: references/installation.md, references/client.md, references/client-api.md, references/prisma-config.md, references/cli-reference.md, references/editor-setup.md, references/schema.md, references/schema-reference.md, references/data-modeling.md, references/field-attributes.md, references/model-attributes.md, references/enums.md, references/default-values.md, references/composite-types.md, references/scalar-lists.md, references/referential-actions.md, references/queries.md, references/relations.md, references/filtering.md, references/sorting.md, references/select-include.md, references/pagination-cursor.md, references/pagination-offset.md, references/distinct.md, references/count-exists.md, references/case-sensitivity.md, references/aggregations.md, references/transactions.md, references/typedsql.md, references/raw-queries.md, references/json-fields.md, references/full-text-search.md, references/views.md, references/stored-procedures.md, references/triggers.md, references/constraints.md, references/indexes-advanced.md, references/migrations.md, references/seeding.md, references/baselining.md, references/shadow-database.md, references/migration-history.md, references/squashing.md, references/hotfixing.md, references/down-migrations.md, references/data-migrations.md, references/zero-downtime.md, references/optimization.md, references/query-optimization.md, references/n-plus-one.md, references/batching.md, references/lazy-loading.md, references/caching-strategies.md, references/connection-limits.md, references/cold-starts.md, references/bundle-size.md, references/accelerate.md, references/connection-pooling.md, references/connection-urls.md, references/environment-variables.md, references/ssl-tls.md, references/sql-injection.md, references/row-level-security.md, references/encryption.md, references/audit-logging.md, references/gdpr-compliance.md, references/postgresql.md, references/mysql.md, references/sqlite.md, references/mongodb.md, references/cockroachdb.md, references/planetscale.md, references/supabase.md, references/neon.md, references/turso.md, references/extensions.md, references/driver-adapters.md, references/omit-api.md, references/middleware.md, references/soft-delete.md, references/read-replicas.md, references/multi-database.md, references/multi-schema.md, references/nextjs-integration.md, references/astro.md, references/nuxt.md, references/sveltekit.md, references/solidstart.md, references/remix.md, references/react-router.md, references/hono.md, references/express.md, references/clerk.md, references/authjs.md, references/betterauth.md, references/permit-io.md, references/deployment.md, references/vercel.md, references/netlify.md, references/railway.md, references/render.md, references/flyio.md, references/aws-lambda.md, references/cloudflare-workers.md, references/docker.md, references/heroku.md, references/deno-deploy.md, references/vscode.md, references/github-copilot.md, references/tabnine.md, references/safeql.md, references/prisma-ai.md, references/mcp-server.md, references/turborepo.md, references/pnpm-workspaces.md, references/error-handling.md, references/error-codes.md, references/logging.md, references/opentelemetry.md, references/datadog.md, references/studio.md, references/testing.md, references/vs-typeorm.md, references/vs-sequelize.md, references/vs-drizzle.md, references/vs-mongoose.md, references/vs-kysely.md, references/migrate-from-typeorm.md, references/migrate-from-sequelize.md, references/migrate-from-drizzle.md
related-skills: nextjs-16, better-auth, solid-nextjs
---

# Prisma 7 ORM

Rust-free TypeScript ORM with 90% smaller bundles and 3x faster queries.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing schema and database patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Prisma 7 docs via Context7/Exa
3. **mcp__context7__query-docs** - Check breaking changes and migration guide

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Database access in Next.js 16 applications
- Type-safe queries with full TypeScript inference
- Schema-first database modeling and migrations
- Complex queries requiring TypedSQL
- Excluding sensitive fields with Omit API

### Why Prisma 7

| Feature | Benefit |
|---------|---------|
| Rust-free client | 90% smaller bundles (14MB → 1.6MB) |
| Query performance | Up to 3x faster on large datasets |
| ESM-first | Native ES modules, modern architecture |
| TypedSQL | Type-safe raw SQL queries |
| Omit API | Exclude sensitive fields globally |
| Driver adapters | Direct database driver integration |

---

## Breaking Changes from v6

### Critical Migration Points

| Change | v6 | v7 |
|--------|----|----|
| Provider | `prisma-client-js` | `prisma-client` |
| Output path | Optional | **REQUIRED** |
| Import | `@prisma/client` | `./generated/prisma/client` |
| Drivers | Built-in | Adapter required |
| Config | Schema only | `prisma.config.ts` |

### Required Schema Changes

Provider must be `prisma-client` with explicit output path. No more generation to `node_modules`.

### Driver Adapters Required

PostgreSQL requires `@prisma/adapter-pg`, MySQL requires `@prisma/adapter-mariadb`, SQLite requires `@prisma/adapter-better-sqlite3`.

---

## SOLID Architecture

### Module Structure

Database code organized in `modules/cores/db/`:

- `modules/cores/db/prisma.ts` - Singleton PrismaClient
- `modules/cores/db/generated/` - Generated client
- `prisma/schema.prisma` - Schema definition
- `prisma/migrations/` - Migration history
- `prisma.config.ts` - Prisma configuration

### File Organization

| File | Purpose | Max Lines |
|------|---------|-----------|
| `prisma.ts` | Singleton client | 30 |
| `schema.prisma` | Models, relations | 100 per section |
| `seed.ts` | Database seeding | 50 |

---

## Key Concepts

### Singleton Pattern (Next.js)

Prevent multiple PrismaClient instances during hot-reload. Use `globalThis` to cache instance in development.

### Output Path

Generated client goes to custom path, not `node_modules`. Import from generated folder.

### Driver Adapters

Direct database driver integration for better performance and control. Configure connection pooling at driver level.

### TypedSQL

Write raw SQL with full type safety. Results are typed based on query.

### Omit API

Exclude fields globally or per-query. Perfect for passwords and sensitive data.

---

## Reference Guide (130 files)

### Core Setup
| Need | Reference |
|------|-----------|
| Initial setup | `installation.md` |
| PrismaClient singleton | `client.md` |
| Client API methods | `client-api.md` |
| Configuration | `prisma-config.md` |
| CLI commands | `cli-reference.md` |
| Editor setup | `editor-setup.md` |

### Schema & Modeling
| Need | Reference |
|------|-----------|
| Schema design | `schema.md` |
| Schema syntax | `schema-reference.md` |
| Data modeling | `data-modeling.md` |
| Field attributes | `field-attributes.md` |
| Model attributes | `model-attributes.md` |
| Enums | `enums.md` |
| Default values | `default-values.md` |
| Composite types | `composite-types.md` |
| Scalar lists/arrays | `scalar-lists.md` |
| Referential actions | `referential-actions.md` |

### Queries & Operations
| Need | Reference |
|------|-----------|
| CRUD operations | `queries.md` |
| Relations | `relations.md` |
| Filtering | `filtering.md` |
| Sorting | `sorting.md` |
| Select vs Include | `select-include.md` |
| Pagination (cursor) | `pagination-cursor.md` |
| Pagination (offset) | `pagination-offset.md` |
| Distinct | `distinct.md` |
| Count & exists | `count-exists.md` |
| Case sensitivity | `case-sensitivity.md` |
| Aggregations | `aggregations.md` |
| Transactions | `transactions.md` |

### Advanced Queries
| Need | Reference |
|------|-----------|
| TypedSQL | `typedsql.md` |
| Raw queries | `raw-queries.md` |
| JSON fields | `json-fields.md` |
| Full-text search | `full-text-search.md` |
| Views | `views.md` |
| Stored procedures | `stored-procedures.md` |
| Triggers | `triggers.md` |
| Constraints | `constraints.md` |
| Advanced indexes | `indexes-advanced.md` |

### Migrations
| Need | Reference |
|------|-----------|
| Migration workflow | `migrations.md` |
| Seeding | `seeding.md` |
| Baselining | `baselining.md` |
| Shadow database | `shadow-database.md` |
| Migration history | `migration-history.md` |
| Squashing | `squashing.md` |
| Hotfixing | `hotfixing.md` |
| Down migrations | `down-migrations.md` |
| Data migrations | `data-migrations.md` |
| Zero-downtime | `zero-downtime.md` |

### Performance
| Need | Reference |
|------|-----------|
| Optimization | `optimization.md` |
| Query optimization | `query-optimization.md` |
| N+1 problem | `n-plus-one.md` |
| Batching | `batching.md` |
| Lazy loading | `lazy-loading.md` |
| Caching strategies | `caching-strategies.md` |
| Connection limits | `connection-limits.md` |
| Cold starts | `cold-starts.md` |
| Bundle size | `bundle-size.md` |
| Accelerate | `accelerate.md` |
| Connection pooling | `connection-pooling.md` |

### Security
| Need | Reference |
|------|-----------|
| Connection URLs | `connection-urls.md` |
| Environment variables | `environment-variables.md` |
| SSL/TLS | `ssl-tls.md` |
| SQL injection | `sql-injection.md` |
| Row-level security | `row-level-security.md` |
| Encryption | `encryption.md` |
| Audit logging | `audit-logging.md` |
| GDPR compliance | `gdpr-compliance.md` |

### Databases
| Need | Reference |
|------|-----------|
| PostgreSQL | `postgresql.md` |
| MySQL | `mysql.md` |
| SQLite | `sqlite.md` |
| MongoDB (deprecated) | `mongodb.md` |
| CockroachDB | `cockroachdb.md` |
| PlanetScale | `planetscale.md` |
| Supabase | `supabase.md` |
| Neon | `neon.md` |
| Turso | `turso.md` |

### Extensions & Integrations
| Need | Reference |
|------|-----------|
| Extensions | `extensions.md` |
| Driver adapters | `driver-adapters.md` |
| Omit API | `omit-api.md` |
| Middleware (deprecated) | `middleware.md` |
| Soft delete | `soft-delete.md` |
| Read replicas | `read-replicas.md` |
| Multi-database | `multi-database.md` |
| Multi-schema | `multi-schema.md` |

### Framework Integrations
| Need | Reference |
|------|-----------|
| Next.js | `nextjs-integration.md` |
| Astro | `astro.md` |
| Nuxt | `nuxt.md` |
| SvelteKit | `sveltekit.md` |
| SolidStart | `solidstart.md` |
| Remix | `remix.md` |
| React Router | `react-router.md` |
| Hono | `hono.md` |
| Express | `express.md` |

### Auth Integrations
| Need | Reference |
|------|-----------|
| Clerk | `clerk.md` |
| Auth.js | `authjs.md` |
| Better Auth | `betterauth.md` |
| Permit.io | `permit-io.md` |

### Deployment
| Need | Reference |
|------|-----------|
| Deployment guide | `deployment.md` |
| Vercel | `vercel.md` |
| Netlify | `netlify.md` |
| Railway | `railway.md` |
| Render | `render.md` |
| Fly.io | `flyio.md` |
| AWS Lambda | `aws-lambda.md` |
| Cloudflare Workers | `cloudflare-workers.md` |
| Docker | `docker.md` |
| Heroku | `heroku.md` |
| Deno Deploy | `deno-deploy.md` |

### Tooling
| Need | Reference |
|------|-----------|
| VS Code | `vscode.md` |
| GitHub Copilot | `github-copilot.md` |
| Tabnine | `tabnine.md` |
| SafeQL | `safeql.md` |
| Prisma AI | `prisma-ai.md` |
| MCP Server | `mcp-server.md` |
| Turborepo | `turborepo.md` |
| pnpm workspaces | `pnpm-workspaces.md` |

### Monitoring
| Need | Reference |
|------|-----------|
| Error handling | `error-handling.md` |
| Error codes | `error-codes.md` |
| Logging | `logging.md` |
| OpenTelemetry | `opentelemetry.md` |
| DataDog | `datadog.md` |
| Studio | `studio.md` |
| Testing | `testing.md` |

### ORM Comparisons
| Need | Reference |
|------|-----------|
| vs TypeORM | `vs-typeorm.md` |
| vs Sequelize | `vs-sequelize.md` |
| vs Drizzle | `vs-drizzle.md` |
| vs Mongoose | `vs-mongoose.md` |
| vs Kysely | `vs-kysely.md` |

### Migration Guides
| Need | Reference |
|------|-----------|
| From TypeORM | `migrate-from-typeorm.md` |
| From Sequelize | `migrate-from-sequelize.md` |
| From Drizzle | `migrate-from-drizzle.md` |

---

## Best Practices

1. **Singleton in Next.js** - Cache PrismaClient in globalThis
2. **Output path required** - Never generate to node_modules
3. **Driver adapters** - Use native drivers for better performance
4. **Omit sensitive fields** - Configure global omit for passwords
5. **TypedSQL for complex** - Use for queries Prisma can't express
6. **Index verification** - Check query plans for N+1 issues

---

## Forbidden Patterns

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| Import from `@prisma/client` | v7 requires generated path | Import from `./generated/prisma/client` |
| `prisma-client-js` provider | Deprecated in v7 | Use `prisma-client` |
| No output path | Required in v7 | Set `output` in generator |
| MongoDB | Not supported in v7.0-7.3 | Stay on Prisma 6 |
| url in datasource | Deprecated | Use `prisma.config.ts` |
