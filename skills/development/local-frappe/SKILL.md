---
name: local-frappe
description: Local Frappe development environment for testing APIs before production deployment. Use when developing or testing Python/API changes locally.
allowed-tools: Bash, Read, Grep, Edit, Write
user-invocable: true
---

# /local-frappe - Local Frappe Development

## CRITICAL: TEST LOCALLY FIRST - NO EXCEPTIONS

**NEVER deploy Frappe/Python changes directly to production.**

| Action | Time | When to Use |
|--------|------|-------------|
| Local test | **Seconds** | ALWAYS - every code change |
| Production deploy | 15-20 min | ONLY after local testing passes |

**The 15-20 minute production build/deploy cycle is UNACCEPTABLE for iterative development.**

## What This Command Does

Sets up and manages a local Frappe development environment for testing BEI custom APIs before deploying to production.

**MANDATORY:** Always test changes locally BEFORE pushing to production. The local environment matches production (Frappe v15, ERPNext v15, HRMS v15).

## Quick Start

```bash
cd docker-dev
dev.bat start     # Windows (first run takes 10-15 minutes)
./dev.sh start    # Linux/Mac
```

## Access

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Frappe web UI |
| http://localhost:8000/api/method/frappe.ping | API test endpoint |
| http://localhost:8000/api/method/hrms.api.hello.hello | BEI test API |
| localhost:3307 | MariaDB (user: root, pass: admin) |

**Login:** Administrator / admin

## Development Workflow

### Standard Workflow (Edit → Sync → Test)

```bash
# 1. Edit your API file locally
#    Example: hrms/api/employee_clearance.py

# 2. Sync to container and clear cache
dev.bat sync

# 3. Test your API
curl http://localhost:8000/api/method/hrms.api.employee_clearance.get_status

# 4. When ready, commit and push to production
git add .
git commit -m "feat: Add employee clearance API"
git push origin production
```

### Helper Commands

| Command | Description |
|---------|-------------|
| `dev.bat start` | Start all containers (first run: 10-15 min) |
| `dev.bat stop` | Stop all containers |
| `dev.bat restart` | Restart Frappe to pick up code changes |
| `dev.bat sync` | Copy API files and clear cache (quick reload) |
| `dev.bat shell` | Open bash shell in container |
| `dev.bat bench` | Run bench command (e.g., `dev.bat bench migrate`) |
| `dev.bat logs` | Follow Frappe logs |
| `dev.bat test` | Test hello API endpoint |
| `dev.bat migrate` | Run database migrations |
| `dev.bat status` | Show container status |
| `dev.bat reset` | Delete everything and start fresh (DESTRUCTIVE) |

## File Structure

```
docker-dev/
├── docker-compose.yml    # Container orchestration
├── dev.bat               # Windows helper script
└── dev.sh                # Linux/Mac helper script

hrms/api/                 # BEI custom API files (synced to container)
├── __init__.py           # API exports (CRITICAL - update when adding new APIs)
├── hello.py              # Test endpoint
├── employee_clearance.py # Clearance APIs
├── enrichment.py         # Data enrichment APIs
├── google_chat.py        # Google Chat integration
├── google_drive.py       # Google Drive integration
├── google_login.py       # Google OAuth
├── oauth_tokens.py       # OAuth token management
├── onboarding.py         # Employee onboarding
└── roster.py             # Shift roster APIs
```

## Adding a New API

### 1. Create your API file

```python
# hrms/api/my_new_api.py
import frappe

@frappe.whitelist(allow_guest=True)
def hello():
    """Test endpoint."""
    return {"message": "Hello from my new API!"}

@frappe.whitelist()
def get_data():
    """Requires authentication."""
    return {"user": frappe.session.user}
```

### 2. Update __init__.py

```python
# hrms/api/__init__.py
from hrms.api.my_new_api import (
    hello,
    get_data,
)
```

### 3. Sync and test

```bash
dev.bat sync
curl http://localhost:8000/api/method/hrms.api.my_new_api.hello
```

## Container Configuration

| Component | Value |
|-----------|-------|
| Frappe Image | `frappe/bench:v5.25.11` |
| Bench Location | `/workspace/frappe-bench` |
| API Mount | `/bei-api` (read-only from `hrms/api/`) |
| Site Name | `dev.localhost` |
| MariaDB Port | 3307 (external), 3306 (internal) |
| Web Port | 8000 |
| Socket.IO Port | 9000 |

## Volumes

| Volume | Purpose |
|--------|---------|
| `docker-dev_frappe-bench` | Frappe bench directory (apps, sites, etc.) |
| `docker-dev_mariadb-data` | Database data |

**Note:** Volumes persist data across container restarts. To completely reset, use `docker compose down -v`.

## Troubleshooting

### Container won't start

```bash
# Check logs
dev.bat logs

# Or directly
docker logs frappe-dev
```

### API changes not visible

```bash
# Force sync and clear cache
dev.bat sync

# If still not working, restart Frappe
dev.bat restart
```

### Database connection errors

```bash
# Check MariaDB is healthy
docker ps

# Should show mariadb-dev as (healthy)
```

### Need fresh start

```bash
# WARNING: This deletes all data
dev.bat reset
# Or manually:
docker compose -f docker-dev/docker-compose.yml down -v
dev.bat start
```

### First run taking too long

First run downloads and installs:
- Frappe Framework (~3 min)
- ERPNext (~5 min)
- HRMS (~3 min)
- Site creation (~2 min)

Total: 10-15 minutes. Subsequent starts are fast (~30 seconds).

## Testing APIs

### Without authentication

```bash
# APIs with @frappe.whitelist(allow_guest=True)
curl http://localhost:8000/api/method/hrms.api.hello.hello
```

### With authentication

```bash
# Get session cookie first
curl -c cookies.txt -X POST http://localhost:8000/api/method/login \
  -d "usr=Administrator" -d "pwd=admin"

# Then use the cookie
curl -b cookies.txt http://localhost:8000/api/method/hrms.api.roster.get_roster
```

### Using bench execute

```bash
# Run Python code directly
dev.bat bench execute hrms.api.hello.hello

# With arguments
dev.bat bench execute "hrms.api.employee_clearance.get_status" --args '["HR-EMP-0001"]'
```

## When to Deploy to Production

After testing locally:

1. **Commit changes:**
   ```bash
   git add hrms/api/
   git commit -m "feat: Add employee clearance API"
   ```

2. **Push to production branch:**
   ```bash
   git push origin production
   ```

3. **Monitor GitHub Actions:** https://github.com/Bebang-Enterprise-Inc/hrms/actions

4. **Verify production:**
   ```bash
   curl https://hq.bebang.ph/api/method/hrms.api.hello.hello
   ```

See `/deploy-frappe` skill for full production deployment options.

## DO NOT DO

1. **NEVER edit files directly in the container** - Changes are lost on restart
2. **NEVER use `docker commit`** - Corrupts the Python environment
3. **NEVER push untested code to production** - Always test locally first
4. **NEVER skip updating `__init__.py`** - API won't be whitelisted
5. **NEVER assume production deploy will pick up code changes** - Use `no_cache=true` (see below)

---

## CRITICAL: Local vs Production Asset Handling

### Why Local Works But Production Breaks

**Local development** allows `bench build` because:
- Single container environment
- No persistent asset volumes (fresh start each time)
- Development mode reloads assets on change

**Production** prohibits `bench build` because:
- Multi-container architecture (frontend + backend)
- Persistent volumes don't auto-update
- Assets baked into Docker image at build time

### What This Means For You

| Action | Local | Production |
|--------|-------|------------|
| `bench build` | ✅ OK | ❌ NEVER |
| `bench migrate` | ✅ OK | ⚠️ Only via isolated container |
| Edit Python files | ✅ Sync + restart | ❌ Rebuild image |
| Edit CSS/JS | ✅ Sync + restart | ❌ Rebuild image |

### The Production Rule

**All code and asset changes MUST go through Docker image rebuild.**

When you push to production:
1. GitHub Actions rebuilds the entire Docker image
2. New CSS/JS hashes are baked into image
3. Assets volume should be deleted before deploy
4. Fresh containers get consistent assets

**Never "hot-fix" production by running bench commands.**

See `/deploy-frappe` for the full CSS 404 root cause analysis and fix.

## Testing Custom WWW Pages Locally

### Creating Custom Pages (like login)

1. Create your page file:
   ```
   hrms/www/bei-login.html  # The HTML template
   hrms/www/bei-login.py    # Optional Python context handler
   ```

2. If redirecting from an existing route, add to `hrms/hooks.py`:
   ```python
   website_redirects = [
       {"source": "/login", "target": "/bei-login", "redirect_http_status": 302},
   ]
   ```

3. Sync to container:
   ```bash
   dev.bat sync
   ```

4. Test locally:
   ```bash
   # Check redirect
   curl -sI http://localhost:8000/login | grep -i location

   # Check page renders
   curl -s http://localhost:8000/bei-login | grep -o "<title>.*</title>"
   ```

### Important: Production Deployment Uses Docker Cache

**After testing locally, you MUST use `no_cache=true` when deploying:**
```bash
gh workflow run "Build and Deploy Frappe HRMS" --repo Bebang-Enterprise-Inc/hrms -f no_cache=true -f run_migrate=true
```

**Why:** Docker cache doesn't detect when git repo contents change. Without `no_cache=true`, the build serves cached layers from previous builds.

**How to verify fresh build:** Check GitHub Actions build time:
- ~2 min = CACHED (old code)
- ~5-10 min = FRESH (new code)

## Running bei-tasks Frontend Locally (Added 2026-01-24)

For full-stack local development, run both Frappe AND bei-tasks locally:

### 1. Start Local Frappe

```bash
cd F:\Dropbox\Projects\BEI-ERP\docker-dev
powershell -Command "docker compose up -d"
# Wait for Frappe to start (~30 seconds if already initialized)
```

### 2. Generate API Keys (First Time Only)

```bash
# Login to get session cookie
curl -c cookies.txt -X POST "http://localhost:8000/api/method/login" \
  -d "usr=Administrator&pwd=admin"

# Generate API keys
curl -b cookies.txt -X POST \
  "http://localhost:8000/api/method/frappe.core.doctype.user.user.generate_keys?user=Administrator"
# Returns: {"message":{"api_key":"xxx","api_secret":"yyy"}}
```

### 3. Configure bei-tasks for Local Frappe

Create/update `F:\Dropbox\Projects\bei-tasks\.env.development.local`:

```env
# Local Development Environment
NEXT_PUBLIC_FRAPPE_URL=http://localhost:8000

# Local Frappe API credentials (from step 2)
FRAPPE_API_KEY=your-api-key
FRAPPE_API_SECRET=your-api-secret

# App Configuration
NEXT_PUBLIC_APP_NAME=BEI Tasks (LOCAL)
```

### 4. Start Local bei-tasks

```bash
cd F:\Dropbox\Projects\bei-tasks
npm run dev
# Frontend runs at http://localhost:3000
```

### 5. Test the Connection

```bash
# Test Frappe API directly
curl -H "Authorization: token api-key:api-secret" \
  "http://localhost:8000/api/method/hrms.api.onboarding.get_session?token=test"

# Expected: {"message":{"success":false,"error":"Session not found",...}}
```

### Local Development Stack

| Component | URL | Purpose |
|-----------|-----|---------|
| Frappe Backend | http://localhost:8000 | API + Admin UI |
| bei-tasks Frontend | http://localhost:3000 | React/Next.js app |
| MariaDB | localhost:3307 | Database |
| Socket.IO | localhost:9000 | Realtime |

### Syncing Code Changes

```bash
# After editing hrms/api/*.py files:
cd F:\Dropbox\Projects\BEI-ERP\docker-dev

# Sync files and clear cache
powershell -Command "docker exec frappe-dev bash -c 'cp -f /bei-api/*.py /workspace/frappe-bench/apps/hrms/hrms/api/ && cd /workspace/frappe-bench && bench --site dev.localhost clear-cache'"

# If whitelist decorators changed, restart Frappe
powershell -Command "docker restart frappe-dev"
```

### Important Notes

1. **Authentication Required:** Local APIs need authentication (no `allow_guest=True`)
2. **Session Cookie OR Token Auth:** Use either method for local testing
3. **Different Site:** Local uses `dev.localhost`, production uses `hq.bebang.ph`
4. **No Test Data:** Local DB is empty - create test data as needed

## Related Skills

- `/deploy-frappe` - Production deployment (ONLY after local testing)
- `/frappe-sql-bulk` - Bulk data operations
- `/frappe-doctype` - DocType development

---

## Production Testing Infrastructure (Added 2026-01-23)

### CRITICAL: Database Architecture Discovery

**The Frappe system at `hq.bebang.ph` uses a LOCAL Docker database via Docker Swarm (migrated 2026-01-29).**

| Component | Service Name | Purpose |
|-----------|--------------|---------|
| Backend | `frappe_backend` | Frappe/ERPNext/HRMS (Gunicorn) |
| Database | `frappe_db` | MariaDB (LOCAL) |
| Frontend | `frappe_frontend` | Nginx proxy |
| WebSocket | `frappe_websocket` | Socket.IO |
| Queue | `frappe_queue-short`, `frappe_queue-long` | Background workers |
| Scheduler | `frappe_scheduler` | Cron jobs |

**Note:** Production now uses Docker Swarm (9 services). Container names changed from `frappe_docker-backend-1` to dynamic names under `frappe_backend.1.xxxx`.

**Common Mistake:** AWS SSM commands often connect to the RDS database (`frappe-hrms-db.ctmwomgscn66.ap-southeast-1.rds.amazonaws.com`), but the live Frappe instance uses the local Docker database. This causes "no employees found" issues when testing.

### Production Test Accounts

| Employee ID | Email | Password | Role |
|-------------|-------|----------|------|
| TEST-STAFF-001 | test.staff@bebang.ph | BeiTest2026! | Store Staff |
| TEST-SUPERVISOR-001 | test.supervisor@bebang.ph | BeiTest2026! | Store Supervisor |
| TEST-AREA-001 | test.area@bebang.ph | BeiTest2026! | Area Supervisor |
| TEST-HR-001 | test.hr@bebang.ph | BeiTest2026! | HR User |

### Inserting Test Data into Production

```bash
# 1. Get AWS credentials
export AWS_ACCESS_KEY_ID=$(doppler secrets get AWS_ACCESS_KEY_ID --project bei-erp --config dev --plain)
export AWS_SECRET_ACCESS_KEY=$(doppler secrets get AWS_SECRET_ACCESS_KEY --project bei-erp --config dev --plain)
export AWS_DEFAULT_REGION=ap-southeast-1

# 2. Run SQL on the CORRECT database (via Swarm backend container)
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker exec $(docker ps -qf name=frappe_backend) bench --site hq.bebang.ph mariadb --execute \"INSERT INTO tabEmployee (name, employee_name, first_name, status, gender, date_of_birth, date_of_joining, company, user_id, creation, modified, owner, modified_by) VALUES ('TEST-STAFF-001', 'Test Staff', 'Test', 'Active', 'Male', '1990-01-01', '2024-01-01', 'Bebang Enterprise Inc.', 'test.staff@bebang.ph', NOW(), NOW(), 'Administrator', 'Administrator');\""
  ]'

# 3. Verify
aws ssm send-command \
  --instance-ids "i-026b7477d27bd46d6" \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=[
    "docker exec $(docker ps -qf name=frappe_backend) bench --site hq.bebang.ph mariadb --execute \"SELECT name, employee_name, user_id FROM tabEmployee WHERE name LIKE 'TEST-%';\""
  ]'
```

### API Credentials for bei-tasks

| Environment | Key | Secret | Source |
|-------------|-----|--------|--------|
| Production (Vercel) | `4a17c23aca83560` | `38ecc0e1054b1d2` | Doppler bei-erp |
| Local (.env.local) | Same | Same | Doppler bei-erp |

**IMPORTANT:** HR API routes use token auth (not session cookies) for Employee lookups because regular Frappe users don't have Employee read permission.

### Verifying API Connection

```bash
# Test from production
curl -X POST https://hq.bebang.ph/api/resource/Employee \
  -H "Authorization: token 4a17c23aca83560:38ecc0e1054b1d2" \
  -H "Content-Type: application/json" \
  -d '{"filters": [["user_id", "=", "test.staff@bebang.ph"]]}'

# Expected: Returns employee record
```

### Troubleshooting Production Tests

1. **"No employee found" but employee exists:**
   - Check you're querying the Docker database, not RDS
   - Use `bench --site hq.bebang.ph mariadb` not direct RDS connection

2. **API returns 401:**
   - Verify Vercel env vars match Doppler
   - Redeploy after env var changes

3. **Container not found:**
   - Production now uses Docker Swarm (migrated 2026-01-29)
   - Service names: `frappe_backend`, `frappe_frontend`, etc.
   - Container names are dynamic: `frappe_backend.1.xxxxx`
   - Use `docker service ls` to verify services
   - Use `docker ps -qf name=frappe_backend` to get container ID

4. **HR pages show "Failed to get employee data":**
   - HR APIs need token auth, not session auth
   - Check `app/api/hr/*/route.ts` uses `Authorization: token` header

5. **Code deployed but changes not visible:**
   - Docker build caching issue - use `no_cache=true` when deploying
   - See `/deploy-frappe` for details on when to use no_cache
   - Verify with: `curl https://hq.bebang.ph/api/method/hrms.api.hello.hello`
   - Response should include `build_version` field showing deployment timestamp

### Deployment Verification Endpoint

The hello API includes deployment info for verification:

```bash
curl -s https://hq.bebang.ph/api/method/hrms.api.hello.hello | python -m json.tool
```

Expected response:
```json
{
    "message": {
        "message": "Hello from Frappe HRMS!",
        "timestamp": "2026-01-29 10:04:11.569399",
        "build_version": "2026-01-29T12:16:00+08:00",
        "deployment": "docker-swarm"
    }
}
```

If `build_version` doesn't update after deployment, rebuild with `no_cache=true`.
