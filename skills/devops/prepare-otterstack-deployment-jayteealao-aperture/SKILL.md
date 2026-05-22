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

### Network Detection

Detect networks defined in the Docker Compose file to ensure proper container connectivity:

**Find network definitions:**
```bash
grep -A 5 "^networks:" docker-compose.yml
```

**Extract network names:**
```bash
# Get all network names from the networks section
grep -A 10 "^networks:" docker-compose.yml | grep -E "^  [a-z]" | awk '{print $1}' | sed 's/:$//'
```

**Identify default network:**
1. If networks section exists, use the first network listed as default
2. If no networks section, Docker Compose creates a default network named `{project}_default`
3. Recommend explicit network definition for clarity

**Check service network attachments:**
```bash
# Find services that specify networks
grep -B 5 "networks:" docker-compose.yml | grep -E "^  [a-z]" | awk '{print $1}' | sed 's/:$//'
```

**Network configuration requirements:**
- All services should attach to the same network for inter-service communication
- Network name should use variable substitution: `${NETWORK_NAME:-app-network}`
- Network should be defined explicitly at the bottom of compose file

**Example network configuration:**
```yaml
services:
  web:
    networks:
      - ${NETWORK_NAME:-app-network}

  api:
    networks:
      - ${NETWORK_NAME:-app-network}

networks:
  app-network:
    name: ${NETWORK_NAME:-app-network}
    external: false
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

### 6. Missing Network Definition

**Check:**
```bash
# Check if networks are defined
grep "^networks:" docker-compose.yml

# Check if services specify network
grep -A 2 "services:" docker-compose.yml | grep "networks:"
```

**Problem**: Services on different networks (or default networks) may have connectivity issues in complex deployments. OtterStack needs to know which network containers communicate on.

**Solution**: Define an explicit network and use variable substitution for flexibility.

**Before:**
```yaml
services:
  web:
    image: myapp:latest
    # No network specified - uses auto-generated default
```

**After:**
```yaml
services:
  web:
    image: myapp:latest
    networks:
      - ${NETWORK_NAME:-app-network}

networks:
  app-network:
    name: ${NETWORK_NAME:-app-network}
    external: false
```

## Traefik Exposure Detection

For services that need to be publicly accessible, detect existing Traefik configuration and prepare for enhanced labels:

### Scan for Traefik Labels

**Check for Traefik-enabled services:**
```bash
grep -B 5 "traefik.enable" docker-compose.yml | grep -E "^  [a-z].*:" | sed 's/:$//'
```

**Extract router names:**
```bash
grep "traefik.http.routers" docker-compose.yml | sed -E 's/.*traefik\.http\.routers\.([^.]+)\..*/\1/' | sort -u
```

**Identify exposed services:**
For each service with Traefik labels:
1. Extract service name from docker-compose.yml structure
2. Extract router name from labels
3. Check if domain variable is used (e.g., `${API_DOMAIN}`)
4. Note the exposed port from loadbalancer configuration

### Required Traefik Configuration

Services exposed via Traefik should have these labels at minimum:

```yaml
labels:
  - "traefik.enable=true"
  # Routing
  - "traefik.http.routers.{service}.rule=Host(`${SERVICE_DOMAIN}`)"
  - "traefik.http.routers.{service}.entrypoints=web,websecure"
  # TLS
  - "traefik.http.routers.{service}.tls=true"
  - "traefik.http.routers.{service}.tls.certresolver=myresolver"
  # Load balancer
  - "traefik.http.services.{service}.loadbalancer.server.port={PORT}"
  # CrowdSec middleware (security)
  - "traefik.http.routers.{service}.middlewares=crowdsec-{service}@docker"
  - "traefik.http.middlewares.crowdsec-{service}.plugin.crowdsec-bouncer.enabled=true"
  - "traefik.http.middlewares.crowdsec-{service}.plugin.crowdsec-bouncer.crowdseclapikey=${CROWDSEC_API_KEY}"
```

### Environment Variables for Exposure

For each exposed service, these environment variables are required:

1. **`${SERVICE}_DOMAIN`** - The domain name for the service (e.g., `API_DOMAIN=api.example.com`)
   - Type: String (domain format)
   - Validation: Must be a valid domain without protocol
   - Example: `aperture.example.com`, `api.myapp.io`

2. **`CROWDSEC_API_KEY`** - CrowdSec bouncer API key for security middleware
   - Type: String (sensitive)
   - Validation: Non-empty string
   - Shared across all exposed services
   - Obtain from: CrowdSec dashboard → Bouncers → Add bouncer

3. **`NETWORK_NAME`** - The Docker network name for Traefik communication
   - Type: String
   - Default: Detected from compose file or `app-network`
   - Traefik must be on the same network to route traffic

## Output Format

Generate a readiness report following this template:

```markdown
## OtterStack Readiness Report for [Project Name]

### ✅ Compatible Checks
- Docker Compose syntax validation passed
- Health checks defined for all services
- Uses environment: section for variables
- No hardcoded container names

### 🌐 Networks Detected

**Default network:** `app-network`

**All networks:**
- `app-network` (default)
- `traefik-network` (external, for Traefik communication)

**Service attachments:**
- `web` → app-network, traefik-network
- `api` → app-network, traefik-network
- `db` → app-network (internal only)

**Recommendations:**
- Add `NETWORK_NAME` environment variable for flexibility
- Ensure Traefik is on `traefik-network` for routing

### 🔒 Traefik Exposure

**Exposed services:**

1. **API Service** (`api`)
   - Router: `aperture-api`
   - Port: 8080
   - Domain variable: `API_DOMAIN`
   - CrowdSec: Enabled

2. **Web Service** (`web`)
   - Router: `aperture-web`
   - Port: 3000
   - Domain variable: `WEB_DOMAIN`
   - CrowdSec: Enabled

**Required for exposure:**
- `API_DOMAIN` - Domain for API service (e.g., api.example.com)
- `WEB_DOMAIN` - Domain for web service (e.g., app.example.com)
- `CROWDSEC_API_KEY` - CrowdSec bouncer key (shared)
- `NETWORK_NAME` - Network for Traefik communication

**Traefik configuration:**
- TLS enabled with Let's Encrypt (certresolver: myresolver)
- HTTP and HTTPS entrypoints
- CrowdSec bouncer middleware for DDoS protection

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

## Integration with /deploy-otterstack

This skill is automatically invoked during **Phase 2: Preparation** of the `/deploy-otterstack` command.

### Integration Points

When invoked from the deployment orchestration command, this skill:
- Performs comprehensive readiness analysis of the project
- Identifies blocking issues that must be fixed before deployment
- Scans for all required and optional environment variables
- Detects common failure patterns proactively
- Outputs a structured readiness report for the command to parse

### Context Passing

The orchestration command uses the following outputs from this skill:

**Blocking Issues**:
- Critical OtterStack compatibility problems (container names, env_file usage, etc.)
- Required environment variables that are missing
- Common failure patterns detected (native modules, permissions, migrations, etc.)

**Environment Variables**:
- **Required** - Variables without defaults that must be set
- **Optional** - Variables with defaults in the compose file
- **Detected** - Variables already found in codebase or .env files
- **Sensitive** - Variables containing secrets (passwords, keys, tokens)

**Readiness Status**:
- `ready: true/false` - Whether project can proceed to deployment
- `blocking_issue_count` - Number of critical issues found
- `warning_count` - Number of non-critical warnings

### Workflow in Orchestration

```
/deploy-otterstack invoked
    ↓
Invoke prepare-otterstack-deployment skill
    ↓
Generate readiness report
    ↓
If blocking issues found:
  - Show user the issues and fixes
  - Prompt: Review / Continue anyway / Cancel
  - If Cancel: Exit deployment
  - If Continue: Proceed with warnings
    ↓
Pass required_env_vars[] to Setup phase
    ↓
Setup phase uses this to configure environment
```

### Output Format for Orchestration

The command parses these sections from the skill's output:

1. **Compatible Checks** - What passed validation
2. **Issues Found** - Blocking problems with file locations and fixes
3. **Environment Variables** - Required/optional/sensitive vars
4. **Recommended Fixes** - Step-by-step fix instructions
5. **Next Steps** - What to do before deployment

### Auto-Fix Capabilities

Some issues can be automatically identified and fixed by the orchestration command:

| Issue Type | Auto-Fixable | Action |
|------------|--------------|--------|
| Missing env vars | Partial | Prompt user during env scan |
| container_name present | No | User must edit compose file |
| env_file present | No | User must migrate to environment: section |
| Static Traefik priorities | No | User must remove priority labels |
| Health check uses localhost | No | User must change to 127.0.0.1 |
| Native modules need rebuild | No | User must update Dockerfile |
| IPv6/IPv4 conflicts | No | User must update health checks |

### Related Commands

- `/deploy-otterstack` - Full orchestration command that uses this skill in Phase 2
