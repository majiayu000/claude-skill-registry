---
name: setup-dev-environment
description: Set up or reset the local development environment with database, migrations, and dependencies
---

# Setup Dev Environment Skill

Use this skill when initializing or resetting the development environment.

---

## When to Use

- First time setting up the project after cloning
- After pulling major changes that affect dependencies or database schema
- When the local environment is in a broken state and needs a fresh start
- When switching between branches with different dependency requirements

## Prerequisites

- Docker and Docker Compose installed
- Go toolchain installed
- `.env` file configured (see README for required values)

## Initialization Options

### Option 1: Full Setup (with Node.js dependencies)

Use when you need to work with the tarkov.dev GraphQL schema or regenerate the client:

```bash
task init
```

This runs:
1. `deps:install:go` - Installs Go tools
2. `deps:install:node` - Installs Node.js tools
3. `migrate:up` - Applies all database migrations

### Option 2: Go-Only Setup (recommended for most development)

Use for general development when you don't need to update external schemas:

```bash
task init:go-only
```

This runs:
1. `deps:install:go` - Installs Go tools (golangci-lint, goose, genqlient)
2. `migrate:up` - Applies all database migrations

## What Gets Set Up

1. **Go Dependencies**: Linter, migration tool, GraphQL client generator
2. **Docker Services**: PostgreSQL database (and any other services in docker-compose.yml)
3. **Database Schema**: All migrations applied to create tables and indexes
4. **Environment**: Loads variables from `.env` file

## Verification

After initialization, verify the setup:

```bash
# Check Docker services are running
docker compose ps

# Run unit tests (no database needed)
task test:unit

# Run integration tests (uses database)
task test:integration
```

## Troubleshooting

**Database connection fails:**
- Ensure `.env` has correct `POSTGRES_*` values
- Check if port 5432 is already in use: `lsof -i :5432`
- View logs: `docker compose logs postgres`

**Migration errors:**
- Check if previous migrations ran: `docker compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"`
- Rollback and reapply: `task migrate:down && task migrate:up`

**Go dependencies fail to install:**
- Ensure Go is properly installed: `go version`
- Check GOPATH: `go env GOPATH`
- Manually install failing tool, e.g.: `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`

## Clean Reset

If you need to completely reset the environment:

```bash
# Stop and remove all containers and volumes
task compose:down
docker compose down -v

# Clean build artifacts
task clean

# Re-initialize
task init:go-only
```

## Next Steps

After setup, you can:
- Start the API: `task api:start`
- Start the importer: `task importer:start`
- Start the evaluator: `task evaluator:start`
- Run tests: `task test:unit` or `task test:integration`
