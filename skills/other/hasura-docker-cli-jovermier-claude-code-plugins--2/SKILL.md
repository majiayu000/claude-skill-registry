---
name: hasura-docker-cli
description: Activate when using Hasura CLI commands in a self-hosted Docker environment, including migrations, metadata management, and console access via docker exec.
updated: 2025-01-13
---

# Hasura Docker CLI Skill

This skill guides you through using Hasura CLI in a self-hosted Docker Compose environment where the Hasura CLI runs inside a container.

## When This Skill Activates

Claude automatically uses this skill when you:

- Need to run Hasura CLI commands in self-hosted Docker environment
- Want to access Hasura console for schema changes
- Are managing database migrations via Hasura CLI
- Need to apply or rollback migrations
- Want to export or apply Hasura metadata
- Are troubleshooting Hasura configuration issues

## Self-Hosted Docker Architecture

In a self-hosted setup, the Hasura CLI runs inside a Docker container rather than on your host machine.

```
Self-Hosted Docker Stack:
┌──────────────────────────────────────────────────┐
│ console service (hasura/graphql-engine)          │
│ • Runs hasura-cli console command               │
│ • Port 9695: Hasura Console UI                  │
│ • Has hasura-cli installed                      │
│ • Working dir: /app (mounted nhost/ directory)  │
└──────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────┐
│ graphql service (hasura/graphql-engine)         │
│ • Main Hasura GraphQL Engine                    │
│ • Port 8080: GraphQL API                        │
└──────────────────────────────────────────────────┘
```

## CRITICAL: Use Docker Exec for CLI Commands

**❌ TRADITIONAL HASURA CLI DOES NOT WORK DIRECTLY:**

```bash
# ❌ These fail because CLI is inside container
hasura-cli migrate status
hasura-cli metadata export
```

**✅ INSTEAD, USE DOCKER EXEC:**

```bash
# ✅ Correct way to access Hasura CLI in Docker
docker exec {console-container-name} hasura-cli [command]

# Example:
docker exec backend-console-1 hasura-cli version
docker exec backend-console-1 hasura-cli migrate status
```

## Finding Your Console Container Name

```bash
# List all containers to find the console
docker ps | grep console

# Common naming patterns:
# - backend-console-1
# - nhost-console-1
# - hasura-console-1
# - {project}-console-1
```

## Hasura Console Access

### Method 1: Web Browser (Recommended)

The Hasura Console is typically already running when your Docker stack is up:

```bash
# Console URL (configure in docker-compose.yaml)
http://localhost:9695

# Or via environment variable:
https://${CONSOLE_URL}
```

**Docker Compose Configuration:**

```yaml
services:
  console:
    image: hasura/graphql-engine:{version}
    entrypoint: ["hasura-cli"]
    command: ["console", "--no-browser", "--endpoint=http://graphql:8080"]
    ports:
      - "9695:9695"
    volumes:
      - ./nhost:/app  # Mount nhost directory
    working_dir: /app
```

This means:
- ✅ Console is always running when Docker stack is up
- ✅ Automatically tracks schema changes as migrations
- ✅ Accessible via browser at port 9695

### Method 2: Direct CLI Access

```bash
# Access the console container shell
docker exec -it {console-container-name} bash

# Inside container, run hasura-cli commands directly
hasura-cli migrate status
hasura-cli metadata export
```

## Common Hasura CLI Commands

All commands must be prefixed with `docker exec {container-name}`:

### Migration Management

```bash
# Set your container name as environment variable for convenience
export CONSOLE_CONTAINER={your-console-container-name}
export HASURA_ADMIN_SECRET={your-admin-secret}

# Check migration status
docker exec $CONSOLE_CONTAINER hasura-cli migrate status \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Apply pending migrations
docker exec $CONSOLE_CONTAINER hasura-cli migrate apply \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Create new migration
docker exec $CONSOLE_CONTAINER hasura-cli migrate create "add_users_table" \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Rollback last migration
docker exec $CONSOLE_CONTAINER hasura-cli migrate apply \
  --down 1 \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Rollback to specific version
docker exec $CONSOLE_CONTAINER hasura-cli migrate apply \
  --version {timestamp} \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET
```

### Metadata Management

```bash
# Export metadata
docker exec $CONSOLE_CONTAINER hasura-cli metadata export \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Apply metadata
docker exec $CONSOLE_CONTAINER hasura-cli metadata apply \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Reload metadata (refresh GraphQL schema)
docker exec $CONSOLE_CONTAINER hasura-cli metadata reload \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Check metadata inconsistencies
docker exec $CONSOLE_CONTAINER hasura-cli metadata inconsistency list \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET
```

### Seed Data Management

```bash
# Apply seed data
docker exec $CONSOLE_CONTAINER hasura-cli seed apply \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET

# Apply specific seed file
docker exec $CONSOLE_CONTAINER hasura-cli seed apply \
  --file seeds/default/1234_initial_data.sql \
  --database-name default \
  --endpoint http://graphql:8080 \
  --admin-secret $HASURA_ADMIN_SECRET
```

## Environment Variables

The Hasura CLI typically needs these environment variables:

```bash
# Inside the console container (configured in docker-compose.yaml)
HASURA_GRAPHQL_ADMIN_SECRET=${GRAPHQL_ADMIN_SECRET}
HASURA_GRAPHQL_DATABASE_URL=postgres://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}
```

## Working Directory

The console container should mount your project directory:

```yaml
# In docker-compose.yaml
volumes:
  - ./nhost:/app
working_dir: /app
```

This means the CLI can find:
- `/app/config.yaml` - Hasura config
- `/app/migrations/` - Migration files
- `/app/metadata/` - Metadata files
- `/app/seeds/` - Seed files

## Simplified Helper Aliases (Optional)

Create shell aliases for convenience:

```bash
# Add to ~/.bashrc or ~/.zshrc
export CONSOLE_CONTAINER={your-container-name}
export HASURA_ADMIN_SECRET=${GRAPHQL_ADMIN_SECRET}

alias hasura='docker exec $CONSOLE_CONTAINER hasura-cli'

# Then use like:
hasura migrate status --database-name default
hasura metadata export
```

## Complete Migration Workflow

**Scenario: Add a new database table**

```bash
# 1. Open Hasura Console in browser
open http://localhost:9695

# 2. Make schema changes via UI
#    - Go to DATA tab
#    - Click "Create Table"
#    - Define columns, constraints, relationships
#    - Save

# 3. Console automatically creates migration files in:
#    nhost/migrations/default/{timestamp}_{operation}/
#    ├── up.sql    (forward migration)
#    └── down.sql  (rollback migration)

# 4. Check migration status
docker exec $CONSOLE_CONTAINER hasura-cli migrate status \
  --database-name default \
  --endpoint http://graphql:8080

# 5. If needed, manually apply migrations
docker exec $CONSOLE_CONTAINER hasura-cli migrate apply \
  --database-name default \
  --endpoint http://graphql:8080

# 6. Export metadata to sync permissions
docker exec $CONSOLE_CONTAINER hasura-cli metadata export \
  --endpoint http://graphql:8080

# 7. Reload Hasura metadata
docker exec $CONSOLE_CONTAINER hasura-cli metadata reload \
  --endpoint http://graphql:8080

# 8. Commit migration files
git add nhost/migrations/
git add nhost/metadata/
git commit -m "feat(db): add users table"
```

## Troubleshooting

### Issue: Cannot connect to Hasura

**Symptoms:**
- `docker exec` commands fail
- "No such container" error

**Solutions:**

```bash
# 1. Check if console container is running
docker ps | grep console

# 2. If not running, start Docker stack
docker compose up -d

# 3. Wait for services to be healthy
docker compose ps

# 4. Check console logs
docker logs {console-container-name}
```

### Issue: Admin secret authentication failed

**Symptoms:**
- "admin secret not provided" error
- "access denied" messages

**Solutions:**

```bash
# 1. Check admin secret in .env file
grep HASURA_ADMIN_SECRET .env

# 2. Pass admin secret explicitly
docker exec $CONSOLE_CONTAINER hasura-cli migrate status \
  --admin-secret "your-actual-secret-here" \
  --database-name default

# 3. Or set environment variable
export HASURA_GRAPHQL_ADMIN_SECRET=$(grep HASURA_ADMIN_SECRET .env | cut -d '=' -f2)
```

### Issue: Migration files not found

**Symptoms:**
- "no migrations found" error
- Migration commands don't see files

**Solutions:**

```bash
# 1. Verify migration files exist
ls -la nhost/migrations/default/

# 2. Check docker volume mount
docker inspect {console-container-name} | grep -A 10 Mounts

# 3. Verify working directory in container
docker exec $CONSOLE_CONTAINER pwd
# Should output: /app

# 4. List files in container
docker exec $CONSOLE_CONTAINER ls -la /app/migrations/default/
```

### Issue: Console not accessible in browser

**Symptoms:**
- Cannot access http://localhost:9695
- Console URL returns 404 or connection refused

**Solutions:**

```bash
# 1. Check if console service is running
docker ps | grep console

# 2. Check console service health
docker compose ps console

# 3. Check console logs for errors
docker logs {console-container-name} -f

# 4. Verify port mapping
docker port {console-container-name}

# 5. Try accessing via environment URL
echo "https://${CONSOLE_URL}"
```

## Key Differences from Managed Services

| Feature           | Managed (Nhost Cloud/Hasura Cloud) | Self-Hosted Docker                     |
| ----------------- | ----------------------------------- | -------------------------------------- |
| Console access    | `nhost dev hasura`                  | Browser: `http://localhost:9695`       |
| CLI commands      | `hasura-cli [cmd]`                  | `docker exec {container} hasura-cli`   |
| Migration apply   | Auto-applied                        | Manual via CLI or auto on startup      |
| Console startup   | On-demand                           | Always running with Docker stack        |
| Endpoint          | Managed by service                  | `http://graphql:8080` (internal)       |
| Admin secret      | Auto-configured                     | From `.env` file                       |
| Working directory | Auto-detected                       | `/app` in container                    |

## Best Practices

1. **Use Console UI for schema changes** - Automatically creates migration files
2. **Commit migration files immediately** - Track schema changes in version control
3. **Test migrations in development first** - Before applying to production
4. **Always export metadata after schema changes** - Keep metadata in sync
5. **Use explicit database-name flag** - `--database-name default` for clarity
6. **Keep admin secret secure** - Never commit to version control
7. **Back up database before rollbacks** - Prevent data loss

## Quick Reference

| Task              | Command                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| Check CLI version | `docker exec $CONSOLE_CONTAINER hasura-cli version`                                                           |
| Migration status  | `docker exec $CONSOLE_CONTAINER hasura-cli migrate status --database-name default`                            |
| Apply migrations  | `docker exec $CONSOLE_CONTAINER hasura-cli migrate apply --database-name default`                             |
| Export metadata   | `docker exec $CONSOLE_CONTAINER hasura-cli metadata export`                                                   |
| Reload metadata   | `docker exec $CONSOLE_CONTAINER hasura-cli metadata reload`                                                   |
| Access console    | Open browser to `http://localhost:9695` or `https://${CONSOLE_URL}`                                           |

---

**Remember**: In self-hosted Docker environments, the Hasura CLI runs inside a container. Always use `docker exec {container-name} hasura-cli` to run CLI commands, and access the console via web browser.
