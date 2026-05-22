---
name: devops-local-dev
description: Manages the Bestays Docker Compose development environment including service orchestration, Makefile workflows, logs monitoring, and hot-reload development. This skill should be used when starting/stopping development services, checking logs, troubleshooting Docker issues, or managing the local development workflow.
---

# Devops Local Dev

## Overview

Manage the Bestays Docker Compose development environment with 4 core services (PostgreSQL, FastAPI, SvelteKit, Redis) using Makefile commands for orchestration, monitoring, and troubleshooting.

## When to Use This Skill

Use this skill when:

- Starting a new development session (`make dev`, `make up`)
- Stopping or restarting services (`make down`, `make restart`)
- Checking service logs (`make logs`, `make logs-server`, `make logs-frontend`)
- Troubleshooting service health or connectivity issues
- Accessing service shells (`make shell-server`, `make shell-db`)
- Resetting the development environment (`make reset`)
- Understanding the Docker Compose architecture

## Docker Compose Architecture

### Services Overview

| Service      | Container Name       | Host Port   | Purpose                                 |
| ------------ | -------------------- | ----------- | --------------------------------------- |
| **postgres** | bestays-db-dev       | 5433 → 5432 | PostgreSQL 16-alpine with pgvector      |
| **server**   | bestays-server-dev   | 8011 → 8011 | FastAPI backend with hot-reload         |
| **frontend** | bestays-dev-frontend | 5183 → 5183 | SvelteKit 5 with Vite HMR               |
| **redis**    | bestays-redis-dev    | 6379 → 6379 | Redis 7-alpine for caching/sessions     |
| **pgadmin**  | bestays-pgadmin-dev  | 5050 → 80   | Database UI (optional, --profile tools) |

**Access URLs:**

- Backend API: http://localhost:8011
- API Docs: http://localhost:8011/docs
- Frontend: http://localhost:5183
- Database: localhost:5433 (PostgreSQL client)
- pgAdmin: http://localhost:5050 (when started with `make pgadmin`)

### Persistent Volumes

| Volume                  | Purpose            | Survives `make down`? |
| ----------------------- | ------------------ | --------------------- |
| `postgres_data`         | Database data      | ✅ Yes                |
| `redis_data`            | Redis persistence  | ✅ Yes                |
| `server_venv`           | Python virtual env | ✅ Yes                |
| `frontend_node_modules` | Node dependencies  | ✅ Yes                |
| `pgadmin_data`          | pgAdmin config     | ✅ Yes                |

**Note:** Use `make reset` to delete all volumes and start fresh.

### Network

All services communicate via `bestays-network` (bridge network).

- Services use **internal names** to communicate (e.g., `postgres:5432`, `redis:6379`)
- Host machine uses **localhost** with mapped ports (e.g., `localhost:5433`)

## Development Workflow

### Starting a Session

**Recommended (with validation):**

```bash
make dev
```

This command:

1. Detects and stops existing containers
2. Runs preflight validation (checks dependencies, configs)
3. Starts all Docker services
4. Waits for health checks
5. Verifies service health

**Quick start (no validation):**

```bash
make up
```

**With pgAdmin (database UI):**

```bash
make pgadmin
```

### Monitoring Services

**Follow all logs (recommended during development):**

```bash
make logs
```

**Service-specific logs:**

```bash
make logs-server     # Backend FastAPI logs
make logs-frontend   # Frontend SvelteKit/Vite logs
make logs-db         # PostgreSQL logs
```

**Check service status:**

```bash
make status          # Docker Compose status
make check           # Health check all services
make dev-status      # Comprehensive status + validation
```

### Hot-Reload Development

**Backend (FastAPI):**

- Auto-reloads on `.py` file changes in `apps/server/`
- Restart time: ~1-2 seconds
- Watch logs: `make logs-server`

**Frontend (SvelteKit):**

- Vite HMR on `.svelte`, `.ts`, `.js`, `.css` changes in `apps/frontend/`
- Reload time: ~100-500ms (instant in browser)
- Watch logs: `make logs-frontend`

**Restart after major changes:**

```bash
make restart-server     # Restart backend only
make restart-frontend   # Restart frontend only
make restart            # Restart all services
```

### Shell Access

**Backend shell (Python environment):**

```bash
make shell-server
# Inside container: python, pytest, alembic commands
```

**Frontend shell:**

```bash
make shell-frontend
# Inside container: npm, node commands
```

**Database shell (psql):**

```bash
make shell-db
# PostgreSQL shell connected to bestays_dev
```

### Stopping Services

**Preserve data (recommended):**

```bash
make down           # or make dev-stop
```

Stops containers, keeps volumes intact.

**Full reset (delete all data):**

```bash
make reset
```

Stops containers, deletes volumes, restarts fresh.

## Makefile Commands

The project uses a Makefile for Docker Compose orchestration. Run `make help` to see all available commands.

### Common Commands

**Session Management:**

```bash
make dev          # Smart start with validation
make up           # Start all services
make down         # Stop services (preserve data)
make restart      # Restart all services
make reset        # Full reset (delete volumes)
```

**Monitoring:**

```bash
make logs              # Follow all logs
make logs-server       # Backend logs only
make logs-frontend     # Frontend logs only
make status            # Service status
make check             # Health check
```

**Shell Access:**

```bash
make shell-server      # Backend container shell
make shell-frontend    # Frontend container shell
make shell-db          # PostgreSQL shell
```

**Development:**

```bash
make build            # Rebuild containers
make test-server      # Run backend tests
make migrate          # Run database migrations
```

**Guidelines:**

- Use `make dev` for validated startup (runs preflight checks)
- Use `make up` for quick restart (no validation)
- Use `make logs` during active development
- Use `make reset` only when you need a completely fresh start (deletes all data)

## Troubleshooting

### Services Won't Start

**Check if ports are already in use:**

```bash
lsof -i :5433  # PostgreSQL
lsof -i :8011  # Backend
lsof -i :5183  # Frontend
lsof -i :6379  # Redis
```

**Solution:** Stop conflicting processes or change ports in `docker-compose.dev.yml`

### Backend Not Hot-Reloading

**Verify volume mount:**

```bash
make shell-server
ls -la /app
# Should show your source code
```

**Check logs for reload confirmation:**

```bash
make logs-server
# Look for "Uvicorn running on..." and "Watching for changes..."
```

### Frontend Not Hot-Reloading

**Check Vite startup:**

```bash
make logs-frontend
# Look for "VITE ready in X ms" and HMR connection
```

**Verify browser connection:**

- Open browser console
- Look for Vite HMR websocket connection
- Should see: `[vite] connected.`

### Database Connection Errors

**Check database health:**

```bash
make check
```

**Verify connection string (from backend container):**

```bash
make shell-server
echo $DATABASE_URL
# Should be: postgresql+asyncpg://bestays_user:bestays_password@postgres:5432/bestays_dev
```

**Common issue:** Backend tries to connect before PostgreSQL is ready

- **Solution:** Restart backend: `make restart-server`
- Health checks should prevent this, but can happen on slow systems

### Cannot Access Services from Host

**Check if services are running:**

```bash
make status
```

**Verify port mappings:**

```bash
docker ps --filter "name=bestays"
# Should show: 0.0.0.0:8011->8011/tcp
```

**Test connectivity:**

```bash
curl http://localhost:8011/api/health   # Backend
curl http://localhost:5183              # Frontend
```

### Full Reset Required

If nothing works, nuclear option:

```bash
make reset
```

This will:

1. Stop all services
2. Delete all volumes (database data, dependencies)
3. Start fresh

**Note:** You will lose local database data. Consider backing up first (see devops-database skill).

## Environment Variables

**Required variables (set in `.env` file):**

```bash
# Database
POSTGRES_USER=bestays_user
POSTGRES_PASSWORD=bestays_password
POSTGRES_DB=bestays_dev

# Backend
CLERK_SECRET_KEY=sk_test_...
CLERK_WEBHOOK_SECRET=whsec_...
OPENROUTER_API_KEY=sk-or-v1-...

# Frontend
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
```

**Location:** Copy `.env.example` to `.env` and configure.

**Validation:** Run `make dev-validate` to check environment configuration.

## Common Development Patterns

### TDD Workflow

```bash
# Terminal 1: Watch backend logs
make logs-server

# Terminal 2: Run tests on changes
make test-server

# Edit code → Tests auto-run → Check logs → Repeat
```

### Frontend Component Development

```bash
# Terminal 1: Watch frontend logs
make logs-frontend

# Terminal 2: Browser with DevTools open
# Edit .svelte files → Vite HMR → Instant browser update
```

### API Development

```bash
# Start services
make dev

# Access interactive API docs
open http://localhost:8011/docs

# Make changes to Python code → Auto-reload → Refresh docs → Test
```

### Full-Stack Feature Development

```bash
# Terminal 1: All logs
make logs

# Terminal 2: Available for commands
make shell-server     # Backend work
make shell-frontend   # Frontend work
make migrate          # Database changes
```

## Related Skills

- **devops-database** - Database migrations, Alembic, PostgreSQL management

## Key Files

- `docker-compose.dev.yml` - Service definitions
- `Makefile` - Command shortcuts (run `make help`)
- `.env` - Environment variables (copy from `.env.example`)

## Integration with Claude Code

When implementing features, Claude Code will:

1. **Start session:** `make dev`
2. **Watch logs:** `make logs` (or service-specific)
3. **Run tests:** `make test-server`
4. **Restart services if needed:** `make restart-server`
5. **Health check before testing:** `make check`
6. **End session (preserves data):** `make down`

**Why Docker for Development?**

1. **Dev/Prod Parity** - Same PostgreSQL version, same environment
2. **Easy Resets** - `make reset` gives fresh start
3. **Isolated Dependencies** - No conflicts with host machine
4. **Hot-Reload** - Code changes reflect immediately
5. **Unified Logs** - All service logs in one place
6. **Session Management** - Easy restart between development sessions
