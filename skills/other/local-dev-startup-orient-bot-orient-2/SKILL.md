---
name: local-dev-startup
description: Start the website (Docusaurus) and dashboard (Vite) locally. Use when asked to "run the website", "start docs locally", "run the dashboard", "start dev servers", or any request to run local development services.
---

# Local Development Startup Guide

Comprehensive guide for starting and troubleshooting the Orient local development environment.

## Quick Start

```bash
# Start everything
./run.sh dev

# Stop everything
./run.sh dev stop
```

## Containerized Test Environment

For production-like testing with all services running in Docker containers:

```bash
# Start test environment
./run.sh test

# View container logs
./run.sh test logs

# Show container status
./run.sh test status

# Stop test environment
./run.sh test stop
```

### What `./run.sh test` Does

1. **Builds Docker images** for all services:
   - bot-slack
   - dashboard (includes WhatsApp integration)
   - opencode

2. **Starts containers** in dependency order:
   - MinIO (object storage)
   - Dashboard API (with WhatsApp routes)
   - OpenCode API
   - Bot services (Slack)
   - Nginx (reverse proxy)

3. **Creates SQLite database** and pushes schema

4. **Exposes services via Nginx** at port 80

### Test Environment Access Points

| Service       | URL                         |
| ------------- | --------------------------- |
| WhatsApp QR   | http://localhost/qr/        |
| Dashboard     | http://localhost/dashboard/ |
| OpenCode API  | http://localhost/opencode/  |
| MinIO Console | http://localhost:9001       |

### Test Environment vs Dev Mode

| Aspect     | `./run.sh dev`        | `./run.sh test`                |
| ---------- | --------------------- | ------------------------------ |
| Services   | Native processes      | Docker containers              |
| Hot reload | Yes (Vite HMR)        | No (requires rebuild)          |
| Frontend   | http://localhost:5173 | http://localhost/dashboard/    |
| Database   | SQLite (local file)   | SQLite (container volume)      |
| Use case   | Daily development     | Integration/production testing |

### Verifying Test Environment

```bash
# Check all containers are running
docker ps --filter "name=orienter"

# Check dashboard health
curl http://localhost/dashboard/api/health

# View container logs
./run.sh test logs

# Check specific container
docker logs orienter-dashboard
```

---

## What `./run.sh dev` Does

1. Checks for orphaned processes on required ports
2. Starts Docker infrastructure (MinIO, Nginx)
3. Creates SQLite database directory if needed
4. Pushes database schema with Drizzle
5. Seeds agent registry if empty
6. Starts Vite frontend dev server (port 5173)
7. Starts Dashboard API server with WhatsApp integration (port 4098)
8. Starts Slack bot

## Service Ports

| Service                   | Port | URL                   |
| ------------------------- | ---- | --------------------- |
| Dashboard Frontend (Vite) | 5173 | http://localhost:5173 |
| Dashboard API + WhatsApp  | 4098 | http://localhost:4098 |
| OpenCode                  | 4099 | http://localhost:4099 |
| MinIO Console             | 9001 | http://localhost:9001 |
| MinIO API                 | 9000 | http://localhost:9000 |
| Nginx                     | 80   | http://localhost:80   |

**Note:** WhatsApp functionality is integrated into the Dashboard service on port 4098.

## Common Startup Errors and Solutions

### 1. Database File Not Found

**Error:**

```
SQLITE_CANTOPEN: unable to open database file
```

**Cause:** Database directory doesn't exist.

**Solution:**

```bash
./run.sh dev stop
./run.sh dev
# Or manually:
mkdir -p .dev-data/instance-0
```

### 2. Missing Module Export (ESM Resolution)

**Error:**

```
SyntaxError: The requested module '@orientbot/database-services' does not provide an export named 'X'
```

**Cause:** Package dist files are stale or missing.

**Solution:** Rebuild packages in dependency order:

```bash
pnpm --filter @orientbot/core build
pnpm --filter @orientbot/database build
pnpm --filter @orientbot/database-services build
pnpm --filter @orientbot/integrations build
```

### 3. Missing Database Table

**Error:**

```
SqliteError: no such table: user_version_preferences
```

**Solution:**

1. Push schema: `pnpm --filter @orientbot/database run db:push:sqlite`
2. Or restart: `./run.sh dev stop && ./run.sh dev`

### 4. Container Name Conflict

**Error:**

```
Conflict. The container name "/orienter-minio-0" is already in use
```

**Solution:**

```bash
./run.sh dev stop
docker rm orienter-minio-0 2>/dev/null
./run.sh dev
```

### 5. Port Already in Use

**Error:**

```
EADDRINUSE: address already in use :::4098
```

**Solution:**

```bash
# Find what's using the port
lsof -i :4098

# Kill the process or stop dev mode
./run.sh dev stop
```

## Package Build Order

When ESM errors occur, rebuild in this order:

```bash
pnpm --filter @orientbot/core build
pnpm --filter @orientbot/database build
pnpm --filter @orientbot/database-services build
pnpm --filter @orientbot/integrations build
```

## Database Management

### Database Location

SQLite database file: `.dev-data/instance-N/orient.db`

### Pushing Schema

```bash
# Push schema changes
pnpm --filter @orientbot/database run db:push:sqlite

# Or via run.sh (done automatically)
./run.sh dev
```

### Inspecting Database

```bash
# Using sqlite3 CLI
sqlite3 .dev-data/instance-0/orient.db ".tables"
sqlite3 .dev-data/instance-0/orient.db "SELECT * FROM agents;"

# Using Drizzle Studio
pnpm db:studio
```

## Verification Checklist

```bash
# 1. API Health (includes WhatsApp status)
curl http://localhost:4098/health

# 2. Frontend Loading
curl -s http://localhost:5173 | head -5

# 3. Database Connectivity
sqlite3 .dev-data/instance-0/orient.db "SELECT COUNT(*) FROM agents;"

# 4. Check Running Processes
ps aux | grep -E "tsx|vite" | grep -v grep

# 5. WhatsApp QR Status
curl http://localhost:4098/qr/status
```

## Environment Configuration

### `.env`

```bash
DATABASE_TYPE=sqlite
SQLITE_DB_PATH=.dev-data/instance-0/orient.db
DASHBOARD_JWT_SECRET=your-secret-here
ORIENT_MASTER_KEY=your-master-key
```

## Troubleshooting Commands

```bash
# View dashboard logs
tail -f logs/instance-0/dashboard-dev.log

# Check Docker containers
docker ps

# Check database tables
sqlite3 .dev-data/instance-0/orient.db ".tables"

# Check for errors
grep -i error logs/instance-0/*.log | tail -20
```

## Blank Page / Loading Issues via Nginx (Port 80)

### Symptoms

- Blank page or stuck on "Loading your workspace..." when accessing http://localhost:80
- No JavaScript console errors visible
- Network requests return 200/304 successfully
- React app intermittently fails to mount (`#root` element is empty)
- Direct access to http://localhost:5173 works perfectly

### Root Causes

**1. ES Module Execution Issues Through Proxy**
When Vite dev server runs behind Nginx proxy, ES modules can intermittently fail to execute:

- Module scripts load (network shows 200/304) but don't run
- No JavaScript errors - silent failure
- Issue is timing/race-condition related with Nginx proxying

**2. Browser Extension Interference**
Extensions like MetaMask use SES (Secure EcmaScript) lockdown which can block:

- Vite's hot module replacement (HMR)
- React prototype modifications
- Look for "SES Removing unpermitted intrinsics" in console

### Diagnosis

```javascript
// In browser console on http://localhost:80/
document.getElementById('root')?.children?.length; // 0 = React not mounted
```

### Solution: Use Direct Vite Access (Strongly Recommended)

**For ALL daily development, use http://localhost:5173 directly:**

```
http://localhost:5173/
```

Benefits:

- 100% reliable React mounting
- Faster hot reload (no Nginx proxy overhead)
- No browser extension conflicts
- Full API access (Vite proxies /api/ requests to port 4098)

**Use http://localhost:80 (Nginx) ONLY when testing:**

- Production-like routing scenarios
- Auth flows requiring specific hostnames
- Multi-service integration testing
- Always test in incognito mode to avoid extension conflicts

## Creating Dashboard Users

When database is recreated, users are lost:

```bash
cd packages/dashboard
HASH=$(npx tsx -e "import bcrypt from 'bcryptjs'; bcrypt.hash('password', 10).then(h => console.log(h));")
sqlite3 ../.dev-data/instance-0/orient.db "
INSERT INTO dashboard_users (username, password_hash) VALUES ('username', '$HASH');
"
```
