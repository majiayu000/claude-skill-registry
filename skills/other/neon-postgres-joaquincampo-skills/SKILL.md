---
name: neon-postgres
description: |
  Neon serverless Postgres for Next.js/TypeScript applications. Covers core architecture (branches, compute endpoints, autoscaling, scale-to-zero), the @neondatabase/serverless driver (HTTP + WebSocket), Prisma ORM integration, neonctl CLI, Neon REST/Management API, MCP Server, connection pooling (PgBouncer), database branching workflows, migrations with Prisma Migrate, environment variable patterns, and pricing/limits.
  Use this skill whenever working with Neon Postgres, @neondatabase/serverless, neonctl, Neon branches, Neon connection pooling, serverless Postgres edge functions, Prisma with Neon, Neon MCP server, DATABASE_URL with -pooler, scale-to-zero Postgres, or any code importing from '@neondatabase/serverless'. Also triggers on: Neon project setup, Neon branching for preview environments, Neon schema diff, neon connection string, serverless database driver, CU-hours, Neon free tier, or Vercel + Neon integration.
---

# Neon Serverless Postgres - Complete Reference

This skill provides everything needed to work with Neon serverless Postgres in Next.js/TypeScript applications, with Prisma as the ORM layer.

## Quick Reference: Project Setup Checklist

```bash
# 1. Install dependencies (Prisma already in project)
npm install @prisma/client
npm install -D prisma

# 2. Set up environment variables (.env)
DATABASE_URL="postgresql://user:pass@ep-xyz-pooler.region.aws.neon.tech/dbname?sslmode=require"
DIRECT_URL="postgresql://user:pass@ep-xyz.region.aws.neon.tech/dbname?sslmode=require"

# 3. Configure prisma/schema.prisma with dual URLs (see references/prisma-integration.md)
# 4. Generate and run migrations
npx prisma migrate dev --name init
npx prisma generate

# 5. (Optional) Set up MCP server for AI-assisted DB management
npx neonctl init
```

**Rule**: Use `DATABASE_URL` (pooled, has `-pooler` in hostname) for app queries. Use `DIRECT_URL` (direct, no `-pooler`) for migrations.

For detailed information on each topic, see the reference files in the `references/` directory.
