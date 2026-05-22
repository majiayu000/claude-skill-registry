---
name: tzurot-deployment
description: Railway deployment procedures for Tzurot v3. Use when deploying, running migrations, or debugging production. Covers service management, log analysis, and health checks.
lastUpdated: '2026-01-28'
---

# Deployment Skill - Tzurot v3

**Use this skill when:** Deploying to Railway, checking logs, managing env vars, debugging production, or verifying service health.

## Quick Reference

```bash
# Check service status (use --json for parsing)
railway status
railway status --json

# View logs
railway logs --service api-gateway -n 50

# Health check
curl https://api-gateway-development-83e8.up.railway.app/health

# Set env variable
railway variables --set "KEY=value" --service service-name
```

> **IMPORTANT**: Consult `docs/reference/RAILWAY_CLI_REFERENCE.md` for accurate Railway CLI 4.27.4 commands.

## Deployment Workflow

### Standard Process

1. **Merge PR to develop** (auto-deploys):

   ```bash
   gh pr merge <PR-number> --rebase
   ```

2. **Monitor deployment**:

   ```bash
   railway status --json
   railway logs --service api-gateway -n 100
   ```

3. **Verify health**:
   ```bash
   curl https://api-gateway-development-83e8.up.railway.app/health
   ```

### Rollback

```bash
# Revert last commit
git revert HEAD
git push origin develop
# Railway auto-deploys the revert
```

## Core Operations

### Viewing Logs

```bash
# Tail specific service
railway logs --service bot-client -n 50

# Search for errors
railway logs --service api-gateway | grep "ERROR"

# Trace request across services
railway logs | grep "requestId:abc123"
```

### Environment Variables

```bash
# Setup all variables from .env (recommended)
pnpm ops deploy:setup-vars --env dev --dry-run  # Preview first
pnpm ops deploy:setup-vars --env dev            # Apply to dev
pnpm ops deploy:setup-vars --env prod           # Apply to prod

# List all for a service (use --json for parsing)
railway variables --service api-gateway --environment development
railway variables --service api-gateway --json

# Set single variable
railway variables --set "OPENROUTER_API_KEY=sk-or-v1-..." --service ai-worker --environment development

# Delete variable - USE DASHBOARD (CLI cannot delete!)
# Go to: Railway Dashboard → Service → Variables → Delete
```

### Database Operations

> ⚠️ **CRITICAL: Prisma migrations use LOCAL folder, not remote state!**
>
> `prisma migrate deploy` applies migrations from your LOCAL `prisma/migrations/` folder.
> If you're on `develop` but production runs `main`, you may apply migrations that
> production code doesn't support yet!
>
> **Before running migrations:**
>
> 1. Checkout the branch that matches deployed code (`git checkout main`)
> 2. Verify migrations: `ls prisma/migrations/`
> 3. Ask: "Does production code support ALL these schema changes?"
>
> **See postmortem**: 2026-01-17 Wrong Branch Migration Deployment

```bash
# Check migration status (uses Railway CLI for auth)
pnpm ops db:status --env dev
pnpm ops db:status --env prod

# Run pending migrations
pnpm ops db:migrate --env dev
pnpm ops db:migrate --env prod --force  # Prod requires --force

# Inspect database tables/indexes
pnpm ops db:inspect --env dev

# Open Prisma Studio against Railway dev
pnpm ops run --env dev npx prisma studio
```

### Running Scripts Against Railway

Use `ops run` to execute **any script** with Railway database credentials:

```bash
# Generic pattern
pnpm ops run --env dev <command>

# Run a one-off script directly (no npm script needed)
pnpm ops run --env dev tsx scripts/src/db/backfill-local-embeddings.ts

# Run Prisma Studio against Railway
pnpm ops run --env dev npx prisma studio

# Shortcut from root
pnpm with-env dev tsx scripts/src/db/backfill-local-embeddings.ts
```

**How it works**: Fetches `DATABASE_PUBLIC_URL` from Railway and injects it as `DATABASE_URL`.

**When to use npm scripts vs direct execution:**

- One-off scripts → `tsx scripts/src/db/script.ts` (direct execution)
- Reusable scripts → `pnpm --filter pkg run script` (npm script)

### Service Restart

```bash
# Use redeploy (railway restart doesn't exist)
railway redeploy --service bot-client --yes
```

## Troubleshooting

| Symptom            | Check                           | Solution                      |
| ------------------ | ------------------------------- | ----------------------------- |
| Service crashed    | `railway logs -n 100`           | Check for missing env vars    |
| Slow responses     | `railway logs \| grep duration` | Check DB/Redis connection     |
| Bot not responding | `bot-client` logs               | Verify DISCORD_TOKEN          |
| Migration failed   | `pnpm ops db:status --env dev`  | Apply with `db:migrate --env` |

### Service Won't Start

1. Check logs: `railway logs --service <name> -n 100`
2. Verify env vars: `railway variables --service <name>`
3. Check DATABASE_URL and REDIS_URL are set

### Discord Bot Not Responding

1. Check bot-client logs
2. Verify health endpoint
3. Verify DISCORD_TOKEN is set
4. Check bot permissions in Discord server

## Docker Build Architecture

### Turbo Prune Pattern

All service Dockerfiles use `turbo prune` for automatic dependency handling:

```dockerfile
# Stage 1: Prune monorepo to only needed packages
FROM node:25-slim AS pruner
RUN npm install -g turbo pnpm
COPY . .
RUN turbo prune @tzurot/service-name --docker

# Stage 2: Install dependencies from pruned workspace
FROM node:25-slim AS installer
COPY --from=pruner /app/out/json/ .
COPY prisma ./prisma
RUN pnpm install --frozen-lockfile

# Stage 3: Build with pruned source
FROM installer AS builder
COPY --from=pruner /app/out/full/ .
COPY tsconfig.json ./
RUN npx prisma generate  # MUST be after COPY, not in installer!
RUN pnpm turbo run build --filter=@tzurot/service-name...
```

**Why turbo prune?**

- Automatically includes transitive workspace dependencies
- No need to manually update Dockerfiles when adding new packages
- Better Docker layer caching (package.json files copied separately)

**Critical ordering requirements:**

1. **tsconfig.json**: Must be copied in builder stage (turbo prune doesn't include root configs)
2. **prisma generate**: Must run in builder stage AFTER `COPY --from=pruner`. If run in installer stage, the subsequent COPY overwrites the generated client!

### Adding New Workspace Packages

When creating a new package in `packages/`:

1. **Build step**: Automatically included via `turbo prune`
2. **Runtime copy**: Still requires manual `COPY --from=builder` for `dist/` folder

```dockerfile
# If the new package is used at runtime, add to runner stage:
COPY --from=builder /app/packages/new-package/dist ./packages/new-package/dist
```

**Note**: The build will succeed automatically (turbo prune includes dependencies), but if the package's compiled output is needed at runtime, you must add the COPY line.

## Railway Patterns

### Private Networking

```typescript
// ✅ Use Railway-provided URLs
const GATEWAY_URL = process.env.GATEWAY_URL; // Internal

// ❌ Don't use public URLs for internal calls
const GATEWAY_URL = 'https://api-gateway-xxx.up.railway.app';
```

### Connection Retry on Startup

```typescript
for (let attempt = 1; attempt <= 5; attempt++) {
  try {
    await prisma.$connect();
    break;
  } catch {
    await new Promise(r => setTimeout(r, 2000 * attempt));
  }
}
```

## Deployment Checklist

**Before**:

- [ ] Tests passing (`pnpm test`)
- [ ] Linting passing (`pnpm lint`)
- [ ] PR merged to `develop`

**After**:

- [ ] Services show "Running" status
- [ ] Health endpoint returns 200
- [ ] No ERROR logs in first 5 minutes
- [ ] Bot responds to test command

## Related Skills

- **tzurot-observability** - Log analysis and correlation IDs
- **tzurot-security** - Secret management
- **tzurot-git-workflow** - Deployment triggers

## References

- Railway CLI: `docs/reference/RAILWAY_CLI_REFERENCE.md`
- Railway Operations: `docs/reference/deployment/RAILWAY_OPERATIONS.md`
- Railway docs: https://docs.railway.com/
