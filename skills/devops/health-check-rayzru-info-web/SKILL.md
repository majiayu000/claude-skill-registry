---
name: health-check
description: Verify development environment health (Docker, API, auth, database)
context: fork
allowed-tools:
  - Bash
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
---

# Health Check

Verifies development environment is healthy and ready for work.

**Token Efficiency**: Quick environment validation (30% savings: 1,500 → 1,050 tokens)

## Usage

Invoke with: `/health-check [scope]`

**Examples**:
- `/health-check` - Full health check (all services)
- `/health-check docker` - Check Docker containers only
- `/health-check api` - Check API endpoints only
- `/health-check auth` - Check authentication only

## Prerequisites

- Docker Desktop running (for Docker checks)
- Application running on localhost:3000
- PostgreSQL database available

## Workflow

### Step 1: Determine Check Scope

**If user provided scope**:
- `docker` → Check Docker containers only
- `api` → Check API endpoints only
- `auth` → Check authentication only
- `db` → Check database only
- `frontend` → Check frontend only

**If no scope provided**:
- Run full health check (all services)

### Step 2: Check Docker Containers

**List running containers**:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**Expected containers**:
- `info-web-postgres` - PostgreSQL database
- `info-web-app` (optional) - Next.js app if running in Docker

**Health indicators**:
- ✅ Container status: "Up" (healthy)
- ❌ Container status: "Restarting" or "Exited" (unhealthy)

**Check PostgreSQL container specifically**:

```bash
# Verify postgres container is running
docker ps --filter "name=postgres" --format "{{.Status}}"

# Check postgres logs for errors
docker logs info-web-postgres --tail 20 | grep -i error || echo "No errors"
```

**If PostgreSQL not running**:
- Return error: "PostgreSQL container not running"
- Recommend: `docker-compose up -d postgres` or `docker start info-web-postgres`

### Step 3: Check Database Connectivity

**Test database connection**:

```bash
# Try to connect to postgres and run simple query
docker exec info-web-postgres psql -U postgres -d info-web -c "SELECT 1;" 2>&1
```

**Expected output**: `1` (successful query)

**If connection fails**:
- Check if database exists
- Check credentials match DATABASE_URL
- Check if postgres is accepting connections

**Check database schema**:

```bash
# List tables to verify migrations ran
docker exec info-web-postgres psql -U postgres -d info-web -c "\dt" 2>&1
```

**Expected tables** (based on Drizzle schema):
- `users`
- `shifts`
- `schedules`
- Other application tables

**If no tables found**:
- Warn: "Database empty. Run migrations: `npm run db:push`"

### Step 4: Check API Endpoints

**Test Next.js API health**:

```bash
# Check if Next.js is responding
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/

# Check tRPC API
curl -s http://localhost:3000/api/trpc/healthcheck || echo "Health endpoint not available"
```

**Expected responses**:
- Frontend (/) → 200 OK
- API health → 200 OK or endpoint not implemented (404)

**If Next.js not responding**:
- Check if process running: `lsof -i :3000`
- Check package.json for dev script
- Recommend: `npm run dev` or `docker-compose up`

**Test critical API endpoints**:

```bash
# Test NextAuth providers endpoint
curl -s http://localhost:3000/api/auth/providers | jq . || echo "Auth providers not available"

# Expected: JSON with credentials provider
```

**If auth providers fail**:
- Check NEXTAUTH_SECRET env var
- Check NextAuth configuration
- Verify auth route handlers exist

### Step 5: Check Authentication

**Navigate to login page**:

```javascript
mcp__playwright__browser_navigate({
  url: "http://localhost:3000/auth/sign-in"
})

mcp__playwright__browser_snapshot()
```

**Check for**:
- ✅ Login form renders (email input, password input, submit button)
- ✅ No console errors (check separately with debug-console if needed)
- ❌ 500 error page
- ❌ "Service unavailable" message

**Attempt test login** (optional, only if --verify-auth flag):

```javascript
// Only run if user requested auth verification
// Uses same flow as /auth-verify Skill
```

### Step 6: Check Environment Variables

**Verify critical env vars are set**:

```bash
# Check if .env file exists
test -f .env && echo "✓ .env file found" || echo "✗ .env file missing"

# Check critical variables (without printing values)
grep -q "DATABASE_URL" .env && echo "✓ DATABASE_URL set" || echo "✗ DATABASE_URL missing"
grep -q "NEXTAUTH_SECRET" .env && echo "✓ NEXTAUTH_SECRET set" || echo "✗ NEXTAUTH_SECRET missing"
grep -q "NEXTAUTH_URL" .env && echo "✓ NEXTAUTH_URL set" || echo "✗ NEXTAUTH_URL missing"
```

**Critical environment variables**:
- `DATABASE_URL` - PostgreSQL connection string
- `NEXTAUTH_SECRET` - NextAuth secret for JWT signing
- `NEXTAUTH_URL` - Application URL (http://localhost:3000)
- `NODE_ENV` - development/production

**If critical vars missing**:
- Warn which vars are missing
- Recommend: "Copy .env.example to .env and fill in values"

### Step 7: Check Node.js and Dependencies

**Verify Node.js version**:

```bash
node --version
```

**Expected**: v18+ or v20+ (Next.js 16 requirement)

**If wrong Node version**:
- Warn: "Node.js version mismatch. Expected v18+, found [version]"
- Recommend: Use nvm to switch versions

**Check if node_modules exists**:

```bash
test -d node_modules && echo "✓ Dependencies installed" || echo "✗ node_modules missing"
```

**If node_modules missing**:
- Recommend: `npm install` or `pnpm install`

**Check for package.json**:

```bash
test -f package.json && echo "✓ package.json found" || echo "✗ Not a Node.js project"
```

### Step 8: Check Running Processes

**Check if Next.js dev server is running**:

```bash
# Check port 3000
lsof -i :3000 -t || echo "Nothing running on port 3000"

# Get process details if running
lsof -i :3000 | grep LISTEN
```

**If port 3000 occupied by wrong process**:
- Identify process: `lsof -i :3000`
- Recommend killing process or using different port

**If Next.js not running**:
- Recommend: `npm run dev`

### Step 9: Generate Health Report

**Aggregate all checks**:

```markdown
## Development Environment Health Report

**Date**: [timestamp]
**Scope**: [full | docker | api | auth | db]

### Status Summary
- Docker: ✅ Healthy | ⚠️ Warning | ❌ Unhealthy
- Database: ✅ Connected | ❌ Connection failed
- API: ✅ Responding | ❌ Not responding
- Auth: ✅ Working | ❌ Not configured
- Frontend: ✅ Running | ❌ Not running
- Environment: ✅ Configured | ⚠️ Missing vars

### Docker Containers
- **postgres**: ✅ Up (healthy)
- **app**: ✅ Up (if running in Docker)

### Database
- **Connection**: ✅ Connected
- **Schema**: ✅ Tables exist ([count] tables)
- **Migrations**: ✅ Up to date | ⚠️ Pending migrations

### API Endpoints
- **GET /**: ✅ 200 OK
- **GET /api/auth/providers**: ✅ 200 OK
- **tRPC Health**: ✅ Available | ⚠️ Not implemented

### Authentication
- **Login page**: ✅ Renders correctly
- **NextAuth config**: ✅ Configured
- **Test login**: ✅ Successful | ⚠️ Not tested

### Environment Variables
- **DATABASE_URL**: ✅ Set
- **NEXTAUTH_SECRET**: ✅ Set
- **NEXTAUTH_URL**: ✅ Set
- **NODE_ENV**: ✅ development

### Node.js Environment
- **Node version**: v20.10.0 ✅
- **Dependencies**: ✅ Installed (node_modules present)
- **Dev server**: ✅ Running on port 3000

### Issues Found
[None | List of issues]

### Recommendations
[None | List of recommended actions]
```

### Step 10: Return Health Status

**Return structured result**:

```json
{
  "healthy": true,
  "scope": "full",
  "docker": {
    "status": "healthy",
    "containers_running": 2,
    "postgres_healthy": true
  },
  "database": {
    "status": "healthy",
    "connection": "success",
    "tables_count": 8,
    "migrations": "up_to_date"
  },
  "api": {
    "status": "healthy",
    "frontend_responding": true,
    "auth_providers_available": true
  },
  "auth": {
    "status": "healthy",
    "login_page_renders": true,
    "nextauth_configured": true
  },
  "environment": {
    "status": "healthy",
    "node_version": "v20.10.0",
    "dependencies_installed": true,
    "env_vars_complete": true
  },
  "issues": [],
  "recommendations": []
}
```

**If unhealthy**:

```json
{
  "healthy": false,
  "issues": [
    {
      "severity": "critical",
      "component": "database",
      "message": "PostgreSQL container not running",
      "recommendation": "Run: docker-compose up -d postgres"
    },
    {
      "severity": "warning",
      "component": "environment",
      "message": "NEXTAUTH_SECRET not set",
      "recommendation": "Add NEXTAUTH_SECRET to .env file"
    }
  ],
  "recommendations": [
    "Start PostgreSQL: docker-compose up -d postgres",
    "Configure environment: cp .env.example .env",
    "Install dependencies: npm install"
  ]
}
```

## Success Criteria

- [x] All services checked based on scope
- [x] Docker containers verified
- [x] Database connectivity tested
- [x] API endpoints responding
- [x] Authentication configured
- [x] Environment variables validated
- [x] Issues identified with severity
- [x] Recommendations provided
- [x] Health report generated

## Health Check Scopes

### Full Check (default)
- Docker containers
- Database connectivity
- API endpoints
- Authentication
- Environment variables
- Node.js environment

**Use when**: Starting work, after system restart, troubleshooting

### Docker Only
- Container status
- PostgreSQL health
- Container logs

**Use when**: Docker issues suspected, container not starting

### API Only
- Frontend responding
- tRPC endpoints
- NextAuth providers

**Use when**: API not working, debugging API issues

### Auth Only
- Login page renders
- NextAuth configuration
- Test authentication

**Use when**: Auth issues, can't log in

### Database Only
- Connection test
- Schema validation
- Migration status

**Use when**: Database errors, migration issues

## Error Handling

### Error 1: Docker Not Running

**Symptom**: `docker ps` fails with "Cannot connect to Docker daemon"
**Cause**: Docker Desktop not running
**Solution**:
```bash
# macOS
open /Applications/Docker.app

# Linux
sudo systemctl start docker

# Windows
# Start Docker Desktop from Start menu
```

### Error 2: PostgreSQL Container Not Found

**Symptom**: No container named "postgres" or "info-web-postgres"
**Cause**: Container not created or wrong name
**Solution**:
```bash
# List all containers (including stopped)
docker ps -a | grep postgres

# Start postgres container
docker-compose up -d postgres

# Or create new container
docker run --name info-web-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
```

### Error 3: Database Connection Failed

**Symptom**: `psql` connection refused or authentication failed
**Cause**: Wrong credentials or DATABASE_URL
**Solution**:
```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Expected: postgresql://user:password@localhost:5432/database

# Test connection manually
psql "postgresql://postgres:postgres@localhost:5432/info-web"

# If fails, check postgres logs
docker logs info-web-postgres
```

### Error 4: Port 3000 Already in Use

**Symptom**: `lsof -i :3000` shows process, but not Next.js
**Cause**: Another app using port 3000
**Solution**:
```bash
# Kill process on port 3000
kill -9 $(lsof -t -i:3000)

# Or use different port
PORT=3001 npm run dev
```

### Error 5: Node.js Version Mismatch

**Symptom**: Node.js version < 18
**Cause**: Old Node.js version
**Solution**:
```bash
# Install nvm if not installed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js 20
nvm install 20
nvm use 20

# Verify version
node --version
```

## Examples

### Example 1: Healthy Environment

**User**: `/health-check`

**Output**:
```markdown
## Development Environment Health Report

**Date**: 2026-01-09 10:45:00
**Scope**: full

### Status Summary
- Docker: ✅ Healthy (2 containers running)
- Database: ✅ Connected (8 tables, migrations up to date)
- API: ✅ Responding (200 OK)
- Auth: ✅ Working (login page renders)
- Frontend: ✅ Running (port 3000)
- Environment: ✅ Configured (all vars set)

### Issues Found
None

### Recommendations
Environment is healthy and ready for development! 🎉
```

**JSON output**:
```json
{
  "healthy": true,
  "scope": "full",
  "docker": { "status": "healthy", "containers_running": 2 },
  "database": { "status": "healthy", "connection": "success", "tables_count": 8 },
  "api": { "status": "healthy", "frontend_responding": true },
  "auth": { "status": "healthy", "login_page_renders": true },
  "environment": { "status": "healthy", "node_version": "v20.10.0" },
  "issues": [],
  "recommendations": ["Environment is healthy and ready for development!"]
}
```

### Example 2: PostgreSQL Not Running

**User**: `/health-check docker`

**Output**:
```markdown
## Development Environment Health Report

**Date**: 2026-01-09 10:50:00
**Scope**: docker

### Status Summary
- Docker: ❌ Unhealthy (postgres container not running)

### Docker Containers
- **postgres**: ❌ Not running (exited)

### Issues Found
1. **Critical**: PostgreSQL container not running
   - Container status: Exited (exit code 1)
   - Last error: "database system was shut down"

### Recommendations
1. Start PostgreSQL container:
   ```bash
   docker-compose up -d postgres
   ```
2. Check container logs if still fails:
   ```bash
   docker logs info-web-postgres
   ```
```

### Example 3: Environment Variables Missing

**User**: `/health-check`

**Output**:
```markdown
## Development Environment Health Report

### Status Summary
- Environment: ⚠️ Warning (missing critical variables)

### Environment Variables
- **DATABASE_URL**: ❌ Missing
- **NEXTAUTH_SECRET**: ❌ Missing
- **NEXTAUTH_URL**: ✅ Set
- **NODE_ENV**: ✅ development

### Issues Found
1. **Critical**: DATABASE_URL not set
   - Application cannot connect to database
2. **Critical**: NEXTAUTH_SECRET not set
   - Authentication will not work

### Recommendations
1. Copy environment template:
   ```bash
   cp .env.example .env
   ```
2. Fill in missing values:
   - DATABASE_URL=postgresql://postgres:postgres@localhost:5432/info-web
   - NEXTAUTH_SECRET=[generate with: openssl rand -base64 32]
3. Restart development server after updating .env
```

### Example 4: Multiple Issues

**User**: `/health-check`

**Output**:
```markdown
## Development Environment Health Report

### Status Summary
- Docker: ❌ Unhealthy (postgres not running)
- Database: ❌ Connection failed
- API: ❌ Not responding (port 3000)
- Environment: ⚠️ Warning (missing vars)

### Issues Found
1. **Critical**: PostgreSQL container not running
   - Cannot connect to database
2. **Critical**: Next.js dev server not running
   - Port 3000 not responding
3. **Warning**: NEXTAUTH_SECRET not set
   - Auth may not work properly

### Recommendations
**Fix in this order**:
1. Start PostgreSQL:
   ```bash
   docker-compose up -d postgres
   ```
2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add NEXTAUTH_SECRET
   ```
3. Install dependencies (if needed):
   ```bash
   npm install
   ```
4. Start development server:
   ```bash
   npm run dev
   ```
5. Re-run health check to verify:
   ```bash
   /health-check
   ```
```

## Integration with Development Workflow

**Morning startup routine**:
```bash
# 1. Start Docker
open /Applications/Docker.app

# 2. Run health check
/health-check

# 3. If issues found, follow recommendations
# 4. Once healthy, start working
```

**Troubleshooting workflow**:
```bash
# App not working, don't know why
/health-check

# Check issues found
# Follow recommendations in order
# Re-run after each fix

# When all green, continue work
```

**Before asking for help**:
```bash
# Run health check first
/health-check

# Include health report output when asking for help
# Shows exactly what's broken
```

## When to Use This Skill

**Use /health-check when**:
- ✅ Starting work (verify environment ready)
- ✅ After system restart (check services came up)
- ✅ App not working (systematic diagnosis)
- ✅ After pulling code (verify dependencies/migrations)
- ✅ Before committing (ensure tests can run)
- ✅ Helping teammate (verify their environment)

**Don't use when**:
- ❌ In CI/CD pipeline (use proper health check endpoints)
- ❌ Production debugging (use monitoring tools)
- ❌ Performance profiling (use dedicated profilers)

## Token Efficiency

**Baseline (manual environment check)**:
- Check Docker: 200 tokens
- Check database: 300 tokens
- Check API: 200 tokens
- Check auth: 200 tokens
- Check env vars: 200 tokens
- Check Node.js: 200 tokens
- Write report: 200 tokens
- **Total**: ~1,500 tokens

**With health-check Skill**:
- Skill invocation: 150 tokens
- Run all checks: 500 tokens
- Aggregate results: 200 tokens
- Generate report: 200 tokens
- **Total**: ~1,050 tokens

**Savings**: 450 tokens (30% reduction)

**Projected usage**: 5x per week
**Weekly savings**: 2,250 tokens
**Annual savings**: 117,000 tokens (~$0.29/year)

**Note**: Lower frequency than other Skills, but critical for productivity (saves debugging time)

## Related Documentation

- [Docker Docs](https://docs.docker.com/) - Container management
- [Next.js Deployment](https://nextjs.org/docs/deployment) - Environment configuration
- [TOKEN_EFFICIENCY.md](../../guidelines/TOKEN_EFFICIENCY.md) - Token optimization patterns

---

**Skill Version**: 1.0
**Created**: 2026-01-09
**Last Updated**: 2026-01-09
**Requires**: Claude Code v2.1.0+, Docker Desktop, Chrome DevTools MCP (optional)
