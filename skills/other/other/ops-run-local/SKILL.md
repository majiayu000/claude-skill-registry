---
name: ops-run-local
description: Manage the local development environment for Expo + serverless backend projects. Supports start, stop, restart, and status for the full stack or individual services.
allowed-tools:
  - Bash
  - Read
---

# Ops: Run Local

Manage the local development environment.

**Argument**: `$ARGUMENTS` — `start`, `stop`, `restart`, `status`, `start-frontend`, `start-backend` (default: `start`)

## Path Convention

- **Frontend**: Current project directory (`.`)
- **Backend**: `${BACKEND_DIR:-../backend-v2}` — set `BACKEND_DIR` in `.claude/settings.local.json` if your backend is elsewhere

## Prerequisites (run before any operation)

1. Verify backend directory exists:
   ```bash
   BACKEND_DIR="${BACKEND_DIR:-../backend-v2}"
   test -d "$BACKEND_DIR" && echo "Backend dir OK: $BACKEND_DIR" || echo "ERROR: Backend dir not found at $BACKEND_DIR — set BACKEND_DIR"
   ```
2. Check port availability:
   ```bash
   lsof -i :8081 2>/dev/null | grep LISTEN
   lsof -i :3000 2>/dev/null | grep LISTEN
   ```
3. Verify bun is installed:
   ```bash
   which bun && bun --version
   ```

## Discovery

Read the frontend `package.json` to find available start scripts (e.g., `start:local`, `start:dev`, `start:staging`). Read the backend `package.json` to find backend start scripts (e.g., `start:local`, `start:dev`).

## Operations

### start (full stack)

Start both backend and frontend for local development.

1. **Start backend** (background):
   ```bash
   cd "${BACKEND_DIR:-../backend-v2}" && IS_OFFLINE=true bun run start:local
   ```
   Run this in the background using the Bash tool with `run_in_background: true`.

2. **Wait for backend** (up to 30 seconds):
   ```bash
   for i in $(seq 1 30); do
     curl -sf http://localhost:3000/graphql -X POST \
       -H "Content-Type: application/json" \
       -d '{"query":"{ __typename }"}' > /dev/null 2>&1 && echo "Backend ready" && break
     sleep 1
   done
   ```

3. **Start frontend** (background):
   ```bash
   bun run start:local
   ```
   Run this in the background using the Bash tool with `run_in_background: true`.

4. **Verify frontend** (up to 60 seconds — Metro bundler can be slow):
   ```bash
   for i in $(seq 1 60); do
     curl -sf http://localhost:8081 > /dev/null 2>&1 && echo "Frontend ready" && break
     sleep 1
   done
   ```

5. Report status table.

### start-frontend (frontend only, pointing at remote backend)

Use when the backend is already deployed and you only need the frontend.

1. ```bash
   bun run start:dev
   ```
   Run in background.

2. Verify:
   ```bash
   for i in $(seq 1 60); do
     curl -sf http://localhost:8081 > /dev/null 2>&1 && echo "Frontend ready" && break
     sleep 1
   done
   ```

### start-backend (backend only)

1. Check AWS credentials (discover profile from backend `package.json` `aws:signin:*` scripts):
   ```bash
   aws sts get-caller-identity --profile {aws-profile} 2>/dev/null
   ```
   If expired, run the backend's `aws:signin:{env}` script.

2. Start:
   ```bash
   cd "${BACKEND_DIR:-../backend-v2}" && IS_OFFLINE=true bun run start:local
   ```
   Run in background.

3. Verify:
   ```bash
   for i in $(seq 1 30); do
     curl -sf http://localhost:3000/graphql -X POST \
       -H "Content-Type: application/json" \
       -d '{"query":"{ __typename }"}' > /dev/null 2>&1 && echo "Backend ready" && break
     sleep 1
   done
   ```

### stop

Kill all local services.

```bash
# Kill frontend (Metro bundler)
lsof -ti :8081 | xargs kill -9 2>/dev/null || echo "No frontend process on :8081"

# Kill backend (Serverless Offline)
lsof -ti :3000 | xargs kill -9 2>/dev/null || echo "No backend process on :3000"

# Stop Docker if running
cd "${BACKEND_DIR:-../backend-v2}" && docker compose down 2>/dev/null || true
```

### restart

1. Run **stop** (above).
2. Wait 2 seconds: `sleep 2`
3. Run **start** (above).
4. Verify both services respond.

### status

Check what is currently running and responsive.

```bash
echo "=== Port Check ==="
echo -n "Frontend :8081 — "; lsof -i :8081 2>/dev/null | grep LISTEN > /dev/null && echo "LISTENING" || echo "NOT LISTENING"
echo -n "Backend  :3000 — "; lsof -i :3000 2>/dev/null | grep LISTEN > /dev/null && echo "LISTENING" || echo "NOT LISTENING"

echo ""
echo "=== Health Check ==="
echo -n "Frontend :8081 — "; curl -sf -o /dev/null -w "%{http_code}" http://localhost:8081 2>/dev/null || echo "UNREACHABLE"
echo -n "Backend  :3000 — "; curl -sf -o /dev/null -w "%{http_code}" http://localhost:3000/graphql -X POST -H "Content-Type: application/json" -d '{"query":"{ __typename }"}' 2>/dev/null || echo "UNREACHABLE"

echo ""
echo "=== Docker ==="
docker compose -f "${BACKEND_DIR:-../backend-v2}/compose.yaml" ps 2>/dev/null || echo "No Docker services running"
```

Report results as a table:

| Service | Port | Listening | Responsive |
|---------|------|-----------|------------|
| Frontend (Metro) | 8081 | YES/NO | YES/NO |
| Backend (Serverless Offline) | 3000 | YES/NO | YES/NO |
