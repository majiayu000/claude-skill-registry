---
name: prepare-otterstack-deployment
description: Analyzes a codebase and prepares it for OtterStack deployment. Use when preparing docker-compose projects, checking OtterStack compatibility, scanning for environment variables, validating compose files, or setting up zero-downtime deployments. Triggers on "prepare for otterstack", "validate compose file", "check deployment readiness", or "scan env vars".
---

# Prepare OtterStack Deployment

Analyze a codebase and validate it's ready for OtterStack deployment by checking Docker Compose compatibility, scanning for environment variables, and detecting common failure patterns.

## Quick Start

Run these three checks to verify OtterStack readiness:

```bash
# 1. Scan for environment variables
grep -rE '\$\{[A-Z_]+\}|\$[A-Z_]+' docker-compose.yml

# 2. Check compose compatibility
grep -E "container_name:|env_file:" docker-compose.yml  # Should be empty

# 3. Validate syntax
docker compose config --quiet
```

If all checks pass → ready to deploy. If issues found → follow the detailed workflow below.

## Environment Variable Discovery

### Scan Application Code

Different languages use different patterns for environment variables:

**Node.js / TypeScript:**
```bash
grep -r "process\.env\." --include="*.js" --include="*.ts"
```

**Python:**
```bash
grep -r "os\.getenv\|os\.environ" --include="*.py"
```

**Ruby:**
```bash
grep -r "ENV\[" --include="*.rb"
```

**Go:**
```bash
grep -r "os\.Getenv" --include="*.go"
```

### Scan Docker Compose File

Find all variables referenced in compose file:

```bash
grep -oE '\$\{[A-Z_][A-Z0-9_]*\}' docker-compose.yml | sort -u
```

### Scan Dockerfile

Check for ARG and ENV declarations:

```bash
grep -E "^(ENV|ARG)\s+" Dockerfile
```

### Consolidate Results

For each variable found:
1. Determine if it's **required** (no default) or **optional** (has default)
2. Identify the **purpose** (database URL, API key, port, etc)
3. Flag **sensitive** variables (passwords, keys, tokens)
4. Note any **default values** from code

## Compose File Validation

### Critical OtterStack Requirements

#### ❌ 1. No Hardcoded Container Names

**Check:**
```bash
grep "container_name:" docker-compose.yml
```

**Why it fails**: OtterStack creates unique container names per deployment (e.g., `myapp-abc1234-web-1`). Hardcoded names prevent parallel deployments and zero-downtime updates.

**Fix**: Remove all `container_name:` directives.

**Before:**
```yaml
services:
  web:
    container_name: myapp-web  # ❌ Remove this
    image: myapp:latest
```

**After:**
```yaml
services:
  web:
    # ✅ Let Docker Compose generate names
    image: myapp:latest
```

#### ✅ 2. Use Environment Section (Not env_file)

**Check:**
```bash
grep "env_file:" docker-compose.yml
```

**Why it fails**: OtterStack passes `--env-file` to Docker Compose for variable substitution in the compose file itself. Variables must be in the `environment:` section to be injected into containers.

**Fix**: Move to `environment:` section with variable substitution.

**Before:**
```yaml
services:
  web:
    env_file: .env  # ❌ This doesn't work with OtterStack
```

**After:**
```yaml
services:
  web:
    environment:  # ✅ Use environment section
      DATABASE_URL: ${DATABASE_URL}
      SECRET_KEY: ${SECRET_KEY}
      LOG_LEVEL: ${LOG_LEVEL:-INFO}  # With default
```

#### ❌ 3. No Static Traefik Priority Labels

**Check:**
```bash
grep "traefik.http.routers.*.priority" docker-compose.yml
```

**Why it fails**: OtterStack manages Traefik priority labels automatically for zero-downtime deployments. Static priorities conflict with this mechanism.

**Fix**: Remove priority labels, keep other Traefik labels.

**Before:**
```yaml
labels:
  - "traefik.http.routers.myapp.rule=Host(`example.com`)"
  - "traefik.http.routers.myapp.priority=100"  # ❌ Remove this
```

**After:**
```yaml
labels:
  - "traefik.http.routers.myapp.rule=Host(`example.com`)"
  # ✅ OtterStack manages priorities automatically
```

#### ✅ 4. Health Checks Defined

**Check:**
```bash
grep -A5 "healthcheck:" docker-compose.yml
```

**Why it matters**: OtterStack waits for containers to be healthy before routing traffic. Without health checks, containers are immediately considered healthy (which may not be accurate).

**Best practice**: Define explicit health checks.

**Example:**
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/health"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 30s
```

**Critical**: Use `127.0.0.1` not `localhost` to avoid IPv6 issues (see Common Failures below).

#### ✅ 5. Syntax Validation

**Check:**
```bash
docker compose config --quiet
```

If this command fails, the compose file has syntax errors that must be fixed before deployment.

## Common Failure Detection

### 1. Native Module Bindings (Node.js)

**Check:**
```bash
grep -E "node-gyp|native|binding|better-sqlite3|bcrypt|sharp" package.json
```

**Problem**: Native modules compiled on your dev machine won't work in the production container due to different architectures.

**Solution**: Use multi-stage build and rebuild in production stage.

**Example fix in Dockerfile:**
```dockerfile
# Production stage
FROM node:20-slim

# Install build tools for native modules
RUN apt-get update && \
    apt-get install -y build-essential python3 && \
    apt-get clean

# Copy node_modules from builder
COPY --from=builder /build/node_modules ./node_modules

# Rebuild native modules for production architecture
RUN npm rebuild better-sqlite3

# Rest of dockerfile...
```

### 2. Database Path Permissions

**Check:**
```bash
grep -A2 "volumes:" docker-compose.yml | grep -E "\.db|/data"
```

**Problem**: Container user may not have write permissions to database directory.

**Solution**: Use named volumes OR ensure directory ownership in Dockerfile.

**Named volume approach (recommended):**
```yaml
volumes:
  - db-data:/app/data  # Named volume with correct permissions

volumes:
  db-data:
    name: myapp-db-data
```

**Dockerfile ownership approach:**
```dockerfile
# Create directories with correct ownership
RUN mkdir -p /app/data && chown -R app:app /app/data

# Switch to non-root user
USER app
```

### 3. Migration File Paths

**Check:**
```bash
grep "COPY.*migrations\|COPY.*prisma\|COPY.*db" Dockerfile
```

**Problem**: Migration files not copied to container or copied to wrong location.

**Solution**: Ensure migrations are copied to where your application expects them.

**Example**:
```dockerfile
# If your app looks for migrations relative to dist/index.js:
COPY src/migrations ./dist/migrations

# Not:
COPY src/migrations ./src/migrations  # ❌ Wrong location
```

### 4. IPv6/IPv4 Health Check Conflicts

**Check:**
```bash
grep -A3 "healthcheck:" docker-compose.yml | grep "localhost"
```

**Problem**: BusyBox `wget` and some `curl` versions try IPv6 (::1) first when resolving `localhost`, but app may only bind to IPv4 (0.0.0.0).

**Solution**: Use `127.0.0.1` instead of `localhost` in health checks.

**Before:**
```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://localhost:80/health"]  # ❌
```

**After:**
```yaml
healthcheck:
  test: ["CMD", "wget", "--spider", "http://127.0.0.1:80/health"]  # ✅
```

### 5. Missing Build Context

**Check:**
```bash
grep -A2 "build:" docker-compose.yml | grep -v "context:"
```

**Problem**: Build may fail or use wrong directory if context not explicit.

**Solution**: Always specify `context:` and `dockerfile:`.

**Before:**
```yaml
build: .  # ❌ Implicit context
```

**After:**
```yaml
build:  # ✅ Explicit context
  context: .
  dockerfile: Dockerfile
```

## Output Format

Generate a readiness report following this template:

```markdown
## OtterStack Readiness Report for [Project Name]

### ✅ Compatible Checks
- Docker Compose syntax validation passed
- Health checks defined for all services
- Uses environment: section for variables
- No hardcoded container names

### ⚠️  Issues Found

1. **Container name conflict** (docker-compose.yml:15)
   - Found: `container_name: myapp-web`
   - Fix: Remove this line

2. **Health check IPv6 issue** (docker-compose.yml:23)
   - Found: `test: ["CMD", "curl", "http://localhost:8080/health"]`
   - Fix: Change to `http://127.0.0.1:8080/health`

3. **Native module needs rebuild** (package.json)
   - Found: better-sqlite3 in dependencies
   - Fix: Add `RUN npm rebuild better-sqlite3` to Dockerfile

### Environment Variables

**Required (no defaults):**
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Application secret for sessions
- `API_TOKEN` - External service authentication

**Optional (with defaults):**
- `LOG_LEVEL` - Logging level (default: INFO)
- `PORT` - Application port (default: 8080)
- `NODE_ENV` - Environment mode (default: production)

**Sensitive (never commit):**
- `DATABASE_URL` contains password
- `SECRET_KEY` is cryptographic secret
- `API_TOKEN` is authentication credential

### Recommended Fixes

#### 1. Update docker-compose.yml

```yaml
# Remove line 15:
- container_name: myapp-web

# Update health check (line 23):
healthcheck:
  test: ["CMD", "curl", "-f", "http://127.0.0.1:8080/health"]
  interval: 10s
  start_period: 30s
```

#### 2. Update Dockerfile

Add after installing dependencies:
```dockerfile
# Rebuild native modules for production container
RUN npm rebuild better-sqlite3
```

#### 3. Set Environment Variables

On OtterStack server:
```bash
otterstack env set myapp DATABASE_URL "postgresql://user:pass@host/db"
otterstack env set myapp SECRET_KEY "your-secret-key-here"
otterstack env set myapp API_TOKEN "your-api-token"
```

### Next Steps

1. **Apply fixes above** to docker-compose.yml and Dockerfile
2. **Commit and push changes** to git repository
3. **Set environment variables** on OtterStack server
4. **Deploy**: `otterstack deploy myapp`

### Ready to Deploy?

- [ ] All issues fixed
- [ ] Changes committed and pushed
- [ ] Environment variables set on server
- [ ] Docker Compose validation passes locally

Once all boxes are checked, proceed with deployment.
```

## Success Criteria

You're ready to deploy when:

✅ **Compose file passes all checks:**
- No `container_name:` directives
- Uses `environment:` section (not `env_file:`)
- No static Traefik priorities
- Health checks use `127.0.0.1` not `localhost`
- `docker compose config --quiet` succeeds

✅ **Common failures addressed:**
- Native modules have rebuild step in Dockerfile
- Migration files copied to correct paths
- Database directories have proper permissions

✅ **Environment variables documented:**
- All required variables identified
- Sensitive variables flagged
- Default values noted

✅ **Fixes committed:**
- Changes pushed to git repository
- Ready for OtterStack to pull latest commit

## Example: Preparing Aperture

**Scan Results:**
```bash
# Environment variables found
grep -rE '\$\{[A-Z_]+\}' docker-compose.yml
# Found: DATABASE_URL, SECRET_KEY, API_TOKEN, LOG_LEVEL, PORT

# Compatibility checks
grep "container_name:" docker-compose.yml
# Found: container_name: aperture-gateway (line 12)
# Found: container_name: aperture-web (line 45)

grep "env_file:" docker-compose.yml
# No issues - uses environment: section ✅

# Common failures
grep -E "better-sqlite3" package.json
# Found: better-sqlite3 in dependencies

grep "COPY.*migrations" Dockerfile
# Found: COPY src/migrations ./src/migrations
# Issue: App looks in ./dist/migrations at runtime
```

**Fixes Applied:**
1. Removed both `container_name:` directives
2. Added `RUN npm rebuild better-sqlite3` to Dockerfile
3. Changed migrations path to `COPY src/migrations ./dist/migrations`
4. Updated health check to use `127.0.0.1` instead of `localhost`

**Result**: Successful deployment after applying these fixes.
