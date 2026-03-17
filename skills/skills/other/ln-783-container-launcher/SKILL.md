---
name: ln-783-container-launcher
description: Builds and launches Docker containers with health verification using best practices
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-783-container-launcher

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-780-bootstrap-verifier

---

## Purpose

Builds Docker images, launches containers, and performs comprehensive health verification using Docker native health checks and retry strategies.

**Scope:**
- Detect and validate docker-compose.yml configuration
- Build Docker images
- Launch containers with proper startup order
- Verify container health using native health checks
- Provide access URLs and cleanup instructions

**Out of Scope:**
- Building application code (handled by ln-781)
- Running tests (handled by ln-782)
- Container orchestration beyond single host (Kubernetes, Swarm)

---

## When to Use

| Scenario | Use This Skill |
|----------|---------------|
| Called by ln-780 orchestrator | Yes |
| Standalone container launch | Yes |
| Development environment setup | Yes |
| Production deployment | No, use proper CI/CD |

---

## Workflow

### Step 1: Pre-flight Checks

Verify Docker environment readiness.

| Check | Failure Action |
|-------|---------------|
| Docker daemon running | Report error with installation instructions |
| Docker Compose available | Report error, suggest installation |
| Compose file exists | Report error, list expected locations |
| Required ports free | Report conflict, suggest alternatives |
| Sufficient disk space | Warn if low space (<2GB free) |

### Step 2: Parse Compose Configuration

Extract service information from docker-compose.yml.

| Information | Purpose |
|-------------|---------|
| Service names | Track which containers to monitor |
| Exposed ports | Know which ports to check |
| Health check definitions | Use native health checks if defined |
| Dependencies (depends_on) | Understand startup order |
| Volume mounts | Verify paths exist |

### Step 3: Build Images

Build all images defined in compose file.

| Aspect | Strategy |
|--------|----------|
| Build context | Use paths from compose file |
| Build args | Pass through from compose configuration |
| Cache | Use Docker layer cache for speed |
| Failure | Report build errors with full log |

### Step 4: Launch Containers

Start containers with proper orchestration.

| Aspect | Strategy |
|--------|----------|
| Startup order | Respect depends_on and healthcheck conditions |
| Detached mode | Run in background |
| Network | Use compose-defined networks |
| Volumes | Mount all defined volumes |

### Step 5: Health Verification

Verify all containers are healthy using appropriate strategy.

**Strategy Selection:**

| Condition | Strategy |
|-----------|----------|
| Service has `healthcheck:` in compose | Use native Docker health status |
| Service has `depends_on: condition: service_healthy` | Wait for Docker health status |
| No healthcheck defined | Use external HTTP probe with retry |

**Retry Configuration:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max attempts | 10 | Allow slow-starting services |
| Initial delay | 5s | Give containers time to start |
| Backoff | Exponential (5, 10, 20, 40s) | Avoid overwhelming services |
| Max total wait | 120s | Reasonable upper limit |

**Health Check Methods:**

| Method | When to Use |
|--------|------------|
| Docker health status | When container has healthcheck defined |
| HTTP GET to exposed port | For web services without healthcheck |
| Container exec | For services without exposed ports |
| TCP port check | For databases and message queues |

### Step 6: Report Results

Return structured results to orchestrator.

**Result Structure:**

| Field | Description |
|-------|-------------|
| containers | Array of container status objects |
| healthChecks | Array of health check results |
| accessUrls | Map of service name to access URL |
| overallStatus | healthy / unhealthy / partial |
| startupDuration | Time from launch to all healthy |

**Container Status Object:**

| Field | Description |
|-------|-------------|
| name | Container name |
| service | Service name from compose |
| status | running / exited / restarting |
| health | healthy / unhealthy / starting / none |
| port | Exposed port (if any) |
| startedAt | Container start timestamp |

**Health Check Result:**

| Field | Description |
|-------|-------------|
| url | Checked URL or endpoint |
| status | HTTP status code or check result |
| responseTime | Time to respond in ms |
| healthy | Boolean health status |

---

## Error Handling

| Error Type | Action |
|------------|--------|
| Docker daemon not running | Report with start instructions |
| Port already in use | Report conflict, suggest docker compose down first |
| Image build failed | Report with build logs |
| Container exited | Report with container logs |
| Health check timeout | Report with last known status and logs |
| Network unreachable | Check Docker network configuration |

---

## Options

| Option | Default | Description |
|--------|---------|-------------|
| keepRunning | true | Leave containers running after verification |
| stopAfter | false | Stop containers after successful verification |
| healthTimeout | 120 | Max seconds to wait for healthy status |
| showLogs | true | Show container logs on failure |
| buildFirst | true | Build images before starting |
| pullLatest | false | Pull base images before build |

---

## Cleanup Instructions

Provide user with cleanup commands in report.

| Action | Description |
|--------|-------------|
| Stop containers | Stop running containers, preserve data |
| Remove containers and networks | Clean up containers but keep volumes |
| Remove everything | Full cleanup including volumes and images |

---

## Critical Rules

1. **Use native health checks when available** - more reliable than external probes
2. **Implement retry with backoff** - services need time to initialize
3. **Always collect logs on failure** - essential for debugging
4. **Parse compose file for ports** - do not hardcode port numbers
5. **Respect depends_on order** - critical for database-dependent services

---

## Definition of Done

- [ ] Docker environment verified
- [ ] All images built successfully
- [ ] All containers running
- [ ] All health checks passing
- [ ] Access URLs provided
- [ ] Results returned to orchestrator

---

## Reference Files

- Parent: `../ln-780-bootstrap-verifier/SKILL.md`

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
