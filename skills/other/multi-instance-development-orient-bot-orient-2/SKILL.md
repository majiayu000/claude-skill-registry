---
name: multi-instance-development
description: Run and troubleshoot multiple parallel Orient instances with isolated ports, databases, and Docker resources. Use for worktrees, port conflicts, and instance isolation.
---

# Multi-Instance Development Environment

**Purpose:** Manage multiple parallel instances of the Orient for simultaneous testing of different feature branches using isolated resources.

**When to use this skill:** When you need to run multiple bot instances simultaneously (main repo + worktrees), troubleshoot port conflicts, verify instance isolation, or understand the multi-instance architecture.

**Tags:** #development #worktrees #docker #ports #isolation #testing

---

## Overview

The multi-instance development system allows running multiple bot instances in parallel, each with:

- **Unique instance ID** (0-9): Auto-detected from worktree path
- **Isolated ports**: Formula-based offset calculation
- **Separate databases**: Instance-specific SQLite database files
- **Isolated storage**: Separate MinIO containers and S3 buckets
- **Independent networks**: Instance-specific Docker networks

### Key Benefits

- Test multiple features branches simultaneously
- No resource conflicts between instances
- WhatsApp session safety (disabled in worktrees)
- 100% backward compatible with main repo

---

## Architecture

### Instance ID Assignment

**Instance 0 (Main Repository)**

- Path: `/Users/*/code/*/orienter` (no `claude-worktrees` in path)
- Ports: Original values (80, 4098, etc.)
- WhatsApp: Enabled by default
- Use case: Primary development environment

**Instance 1-9 (Worktrees)**

- Path: `/Users/*/claude-worktrees/orienter/feature-name-*`
- Instance ID: Hash of worktree name modulo 9 + 1
- Ports: Offset by `instance_id * 1000`
- WhatsApp: Disabled by default
- Use case: Parallel feature testing

**Manual Override**

```bash
# Force specific instance ID
export AI_INSTANCE_ID=3
./run.sh dev
```

### Port Offset Formula

```
new_port = base_port + (instance_id * 1000)
```

**Port Allocation Table:**

| Service       | Base | Instance 0 | Instance 1 | Instance 2 | Instance 3 |
| ------------- | ---- | ---------- | ---------- | ---------- | ---------- |
| Nginx         | 80   | 80         | 1080       | 2080       | 3080       |
| Dashboard     | 4098 | 4098       | 5098       | 6098       | 7098       |
| OpenCode      | 4099 | 4099       | 5099       | 6099       | 7099       |
| Vite          | 5173 | 5173       | 6173       | 7173       | 8173       |
| MinIO API     | 9000 | 9000       | 10000      | 11000      | 12000      |
| MinIO Console | 9001 | 9001       | 10001      | 11001      | 12001      |

Note: WhatsApp is integrated into Dashboard (same port). Database is SQLite (file-based, no port).

### Resource Isolation

Each instance has:

- **Docker containers**: `orienter-{service}-{instance_id}` (nginx, minio)
- **Docker volumes**: `minio-data-{instance_id}`
- **Docker network**: `orienter-network-{instance_id}`
- **SQLite database**: `.dev-data/instance-{instance_id}/orient.db`
- **S3 bucket**: `orienter-data-{instance_id}`
- **Local directories**: `.dev-data/instance-{instance_id}`, `logs/instance-{instance_id}`

---

## Common Use Cases

### 1. Running Main + Worktree Simultaneously

**Scenario:** Test a feature branch while keeping main repo running.

```bash
# Terminal 1: Start main repo (Instance 0)
cd ~/code/genoox/orienter
./run.sh dev
# Access at: http://localhost:80

# Terminal 2: Start worktree (Instance 1)
cd ~/claude-worktrees/orienter/feature-auth-refactor-*
./run.sh dev
# Access at: http://localhost:1080

# Terminal 3: List all running instances
./run.sh instances
```

**Expected Result:**

- Both instances running without conflicts
- Separate dashboards accessible on different ports
- Independent databases and storage

### 2. Testing Multiple Feature Branches

**Scenario:** Compare behavior across 3 different implementations.

```bash
# Terminal 1: Feature A
cd ~/claude-worktrees/orienter/feature-a-*
./run.sh dev  # Instance 1: http://localhost:1080

# Terminal 2: Feature B
cd ~/claude-worktrees/orienter/feature-b-*
./run.sh dev  # Instance 2: http://localhost:2080

# Terminal 3: Feature C
cd ~/claude-worktrees/orienter/feature-c-*
./run.sh dev  # Instance 3: http://localhost:3080
```

### 3. Enabling WhatsApp in Worktree (Advanced)

**Warning:** Only enable if main repo WhatsApp is stopped.

```bash
# Stop main repo WhatsApp first
cd ~/code/genoox/orienter
./run.sh dev stop

# Enable WhatsApp in worktree
cd ~/claude-worktrees/orienter/test-feature-*
./run.sh dev --enable-whatsapp
# WhatsApp now runs on same port as Dashboard (Instance 1)
```

**Why disabled by default?**

- WhatsApp sessions are global per phone number
- Running two instances causes session conflicts
- Only one instance should connect to WhatsApp at a time

---

## How It Works

### 1. Instance Detection (`scripts/instance-env.sh`)

```bash
detect_instance_id() {
  # Priority 1: Explicit override
  if [ -n "$AI_INSTANCE_ID" ]; then echo "$AI_INSTANCE_ID"; return; fi

  # Priority 2: Detect from worktree path
  if [[ "$(pwd)" == *"/claude-worktrees/"* ]]; then
    local name=$(pwd | grep -oP 'claude-worktrees/[^/]+/\K[^/]+' | head -1)
    echo $(($(echo -n "$name" | cksum | cut -d' ' -f1) % 9 + 1))
    return
  fi

  # Priority 3: Default to instance 0
  echo "0"
}
```

### 2. Port Calculation

```bash
calculate_port() {
  local base_port=$1
  local instance_id=$2
  echo $(( base_port + (instance_id * 1000) ))
}
```

### 3. Environment Configuration

The system exports environment variables:

- **Ports**: `NGINX_PORT`, `DASHBOARD_PORT`, `OPENCODE_PORT`, `VITE_PORT`, etc.
- **Docker**: `COMPOSE_PROJECT_NAME`, container names with instance ID
- **Database**: `SQLITE_DB_PATH` includes instance ID
- **Storage**: `S3_BUCKET` includes instance ID
- **Directories**: `DATA_DIR`, `LOG_DIR`, `PID_DIR` are instance-specific

### 4. Docker Compose Templatization

```yaml
services:
  nginx:
    container_name: orienter-nginx-${AI_INSTANCE_ID:-0}
    ports:
      - '${NGINX_PORT:-80}:80'
    networks:
      - orienter-network

  minio:
    container_name: orienter-minio-${AI_INSTANCE_ID:-0}
    ports:
      - '${MINIO_API_PORT:-9000}:9000'
      - '${MINIO_CONSOLE_PORT:-9001}:9001'
    volumes:
      - minio-data:/data
```

### 5. Nginx Configuration Generation

Dynamic generation with `envsubst`:

```bash
# In scripts/dev.sh
envsubst '$VITE_PORT,$DASHBOARD_PORT,$OPENCODE_PORT' \
  < docker/nginx-local.template.conf \
  > docker/nginx-local.conf
```

---

## Troubleshooting

### Port Conflicts

**Symptom:** Error: "Address already in use" or "port is already allocated"

**Diagnosis:**

```bash
# Check what's using a port
lsof -ti :1080

# List all running instances
./run.sh instances

# Check for orphaned processes
docker ps -a --filter "name=orienter-"
```

**Solutions:**

1. **Stop conflicting instance:**

```bash
cd ~/claude-worktrees/orienter/other-feature
./run.sh dev stop
```

2. **Force kill port:**

```bash
lsof -ti :1080 | xargs kill -9
```

3. **Clean up Docker containers:**

```bash
docker ps -a --filter "name=orienter-" --format "{{.Names}}" | xargs docker rm -f
```

4. **Manual instance ID override:**

```bash
export AI_INSTANCE_ID=7  # Use different instance
./run.sh dev
```

### Database Issues

**Symptom:** SQLite database errors or missing tables

**Diagnosis:**

```bash
# Check if database file exists
ls -la .dev-data/instance-*/orient.db

# Check database size
du -h .dev-data/instance-*/orient.db
```

**Solutions:**

1. **Create database directory:**

```bash
source scripts/instance-env.sh
mkdir -p "$(dirname "$SQLITE_DB_PATH")"
```

2. **Reset database:**

```bash
rm .dev-data/instance-$AI_INSTANCE_ID/orient.db
./run.sh dev  # Will recreate on startup
```

### Container Isolation Issues

**Symptom:** Instances interfering with each other, or wrong data showing up

**Diagnosis:**

```bash
# List all containers with their networks
docker ps --format "table {{.Names}}\t{{.Networks}}\t{{.Ports}}"

# List volumes
docker volume ls | grep orienter
```

**Solutions:**

1. **Verify volume isolation:**

```bash
docker volume ls | grep minio-data
# Should show: minio-data-0, minio-data-1, etc.
```

2. **Clean slate (nuclear option):**

```bash
# Stop all instances
./run.sh dev stop

# Remove all containers and volumes
docker compose -f docker/docker-compose.infra.yml down -v

# Restart
./run.sh dev
```

### WhatsApp Session Conflicts

**Symptom:** WhatsApp constantly disconnecting, or multiple QR codes appearing

**Diagnosis:**

```bash
# Check if multiple instances have WhatsApp enabled
ps aux | grep dashboard

# Check WhatsApp enabled status
source scripts/instance-env.sh
echo "WhatsApp enabled: $WHATSAPP_ENABLED"
```

**Solutions:**

1. **Ensure only one WhatsApp instance:**

```bash
# Stop all instances
./run.sh dev stop
cd ~/code/genoox/orienter
./run.sh dev stop

# Start only main repo
cd ~/code/genoox/orienter
./run.sh dev  # WhatsApp enabled by default
```

2. **If you need WhatsApp in worktree:**

```bash
# Stop main repo first
cd ~/code/genoox/orienter
./run.sh dev stop

# Start worktree with WhatsApp
cd ~/claude-worktrees/orienter/feature-*
./run.sh dev --enable-whatsapp
```

### Instance Detection Not Working

**Symptom:** Worktree shows as Instance 0, or ports aren't offset

**Diagnosis:**

```bash
# Check current path
pwd
# Should contain "/claude-worktrees/"

# Test detection
source scripts/instance-env.sh
echo "Detected instance: $AI_INSTANCE_ID"
```

**Solutions:**

1. **Verify worktree path:**

```bash
pwd | grep claude-worktrees
# Should return the path if in worktree
```

2. **Manual override:**

```bash
export AI_INSTANCE_ID=2
./run.sh dev
```

---

## Best Practices

### Development Workflow

1. **Main Repo = Production-like**
   - Keep main repo as Instance 0
   - Use for integration testing
   - Run with WhatsApp enabled

2. **Worktrees = Feature Testing**
   - Create worktrees for features
   - Each gets unique instance ID
   - WhatsApp disabled by default

3. **Resource Management**
   - Monitor RAM usage (~500MB per instance)
   - Don't exceed 9 instances simultaneously
   - Stop unused instances: `./run.sh dev stop`

### Testing Strategies

1. **Parallel Feature Comparison**

```bash
# Test 3 implementations side-by-side
./run.sh instances  # Check all running
open http://localhost:1080  # Feature A
open http://localhost:2080  # Feature B
open http://localhost:3080  # Feature C
```

2. **Database Migration Testing**

```bash
# Each instance has separate SQLite DB
# Test migrations independently:
cd ~/claude-worktrees/orienter/migration-test
./run.sh dev
# Run migrations (affects only Instance 1's DB)
```

### Cleanup Procedures

**Daily cleanup:**

```bash
# Stop all instances
./run.sh dev stop

# Check for orphans
./run.sh instances
docker ps | grep orienter
```

**Weekly cleanup:**

```bash
# Remove old volumes (optional)
docker volume ls | grep orienter
docker volume prune -f

# Clear logs
rm -rf logs/instance-*/*.log

# Clear old database files
rm -rf .dev-data/instance-*
```

---

## Monitoring & Debugging

### Check Instance Status

```bash
# List all running instances with ports
./run.sh instances

# Check specific instance
docker ps --filter "name=orienter-.*-1"

# View logs
tail -f logs/instance-1/dashboard-dev.log
```

### Verify Isolation

```bash
# Database isolation (SQLite - file-based)
ls -la .dev-data/instance-0/orient.db
ls -la .dev-data/instance-1/orient.db
# Should show different files

# Storage isolation
docker exec orienter-minio-0 mc ls local/
docker exec orienter-minio-1 mc ls local/
# Should show different buckets
```

### Performance Monitoring

```bash
# Check resource usage
docker stats --filter "name=orienter-"

# Check port availability
for port in 1080 5098 5099 6173 10000 10001; do
  lsof -ti :$port >/dev/null 2>&1 && echo "Port $port: IN USE" || echo "Port $port: FREE"
done
```

---

## Configuration Reference

### Environment Variables

Set in `scripts/instance-env.sh`, exported to all services:

**Instance Identification:**

- `AI_INSTANCE_ID` - Instance number (0-9)
- `COMPOSE_PROJECT_NAME` - Docker Compose project name

**Service Ports:**

- `NGINX_PORT` - Nginx reverse proxy port
- `DASHBOARD_PORT` - Dashboard API port (includes WhatsApp)
- `OPENCODE_PORT` - OpenCode server port
- `VITE_PORT` - Vite dev server port

**Infrastructure Ports:**

- `MINIO_API_PORT` - MinIO S3 API port
- `MINIO_CONSOLE_PORT` - MinIO web console port

**Database Configuration:**

- `SQLITE_DB_PATH` - SQLite database file path (instance-specific)

**Storage Configuration:**

- `S3_BUCKET` - MinIO bucket name (includes instance ID)
- `AWS_ENDPOINT_URL` - MinIO endpoint URL

**Directories:**

- `DATA_DIR` - Instance data directory
- `LOG_DIR` - Instance logs directory
- `PID_DIR` - Process ID files directory

**Feature Flags:**

- `WHATSAPP_ENABLED` - WhatsApp integration enabled (true/false)

### Command Reference

**Instance Management:**

```bash
./run.sh instances           # List all running instances
./run.sh dev                 # Start instance (auto-detect ID)
./run.sh dev stop            # Stop current instance
./run.sh dev status          # Show instance status
./run.sh dev logs            # View instance logs
./run.sh dev --enable-whatsapp  # Enable WhatsApp in worktree
```

**Testing:**

```bash
./scripts/run-all-tests.sh          # Run all multi-instance tests
./scripts/test-instance-env.sh      # Unit tests
./scripts/test-config-templates.sh  # Template tests
./scripts/test-integration.sh       # Integration tests
```

**Debugging:**

```bash
source scripts/instance-env.sh      # Load instance environment
display_instance_info               # Show instance configuration
docker ps --filter "name=orienter-" # List containers
docker logs orienter-nginx-1        # View container logs
```

---

## Advanced Topics

### Custom Instance ID Assignment

For complex scenarios, you can manually assign instance IDs:

```bash
# In worktree .env file
echo "AI_INSTANCE_ID=5" >> .env

# Or via environment
export AI_INSTANCE_ID=5
./run.sh dev
```

### Port Collision Resolution

If two worktrees get the same hash (rare), manually override:

```bash
# Worktree 1
cd ~/claude-worktrees/orienter/feature-a
export AI_INSTANCE_ID=1
./run.sh dev

# Worktree 2 (collision detected)
cd ~/claude-worktrees/orienter/feature-b
export AI_INSTANCE_ID=2
./run.sh dev
```

### Production Considerations

**This feature is development-only:**

- Production deploys still use single instance (instance 0)
- Multi-instance is NOT for production horizontal scaling
- Use for local testing only

---

## Related Skills

- `worktree-operations` - Creating and managing git worktrees
- `docker-development` - Local Docker development workflow
- `testing-strategy` - Testing in the monorepo
- `production-debugging` - Production environment debugging

---

## Implementation Files

**Core:**

- `scripts/instance-env.sh` - Instance detection and configuration
- `scripts/dev.sh` - Development script integration
- `docker/docker-compose.infra.yml` - Templatized infrastructure (nginx, minio)
- `docker/nginx-local.template.conf` - Dynamic Nginx config

**Testing:**

- `tests/scripts/instance-env.test.ts` - TypeScript unit tests
- `scripts/test-*.sh` - Bash integration tests
- `scripts/run-all-tests.sh` - Test runner

---

## Migration History

### 2026-01-26: SQLite Migration (v2.0.0)

**Breaking Changes:**

- **Database**: Migrated from PostgreSQL to SQLite (file-based)
- **WhatsApp**: Integrated into Dashboard (single `DASHBOARD_PORT` instead of separate `WHATSAPP_PORT`)
- **Docker**: Removed PostgreSQL container from all compose files

**Removed Environment Variables:**

- `POSTGRES_PORT` - No longer needed (SQLite is file-based)
- `POSTGRES_DB` - No longer needed
- `POSTGRES_USER` - No longer needed
- `POSTGRES_PASSWORD` - No longer needed
- `DATABASE_URL` - Replaced with `SQLITE_DB_PATH`
- `WHATSAPP_PORT` - WhatsApp now uses `DASHBOARD_PORT`

**New Environment Variables:**

- `SQLITE_DB_PATH` - Path to SQLite database file
- `DATABASE_TYPE=sqlite` - Database type indicator

**Migration Steps:**

1. Update `.env` to remove PostgreSQL variables
2. Run `./run.sh dev stop` to stop any running instances
3. Remove old PostgreSQL data: `docker volume rm` any postgres volumes
4. Start fresh with `./run.sh dev`

---

**Last Updated:** 2026-01-26
**Feature Version:** 2.0.0
**Architecture:** SQLite database, unified Dashboard+WhatsApp server
**Minimum Requirements:** Docker, Bash 4.0+, ~500MB RAM per instance
