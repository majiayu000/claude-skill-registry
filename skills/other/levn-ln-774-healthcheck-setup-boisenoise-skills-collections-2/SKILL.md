---
name: ln-774-healthcheck-setup
description: Configures health check endpoints for Kubernetes readiness/liveness/startup
---

# ln-774-healthcheck-setup

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-770-crosscutting-setup

Configures health check endpoints for Kubernetes probes and monitoring.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Context Store from ln-770 |
| **Output** | Health check endpoints and Kubernetes probe configuration |
| **Stacks** | .NET (AspNetCore.Diagnostics.HealthChecks), Python (FastAPI routes) |

---

## Phase 1: Receive Context + Identify Dependencies

Accept Context Store and scan for dependencies to monitor.

**Required Context:**
- `STACK`: .NET or Python
- `PROJECT_ROOT`: Project directory path

**Idempotency Check:**
- .NET: Grep for `AddHealthChecks` or `MapHealthChecks`
- Python: Grep for `/health` route
- If found: Return `{ "status": "skipped" }`

**Dependency Detection:**

| Dependency | .NET Detection | Python Detection |
|------------|----------------|------------------|
| PostgreSQL | `Npgsql` in csproj | `psycopg2` or `asyncpg` in requirements |
| MySQL | `MySql.Data` in csproj | `mysql-connector-python` in requirements |
| Redis | `StackExchange.Redis` in csproj | `redis` in requirements |
| RabbitMQ | `RabbitMQ.Client` in csproj | `pika` or `aio-pika` in requirements |
| MongoDB | `MongoDB.Driver` in csproj | `pymongo` in requirements |

---

## Phase 2: Design Health Check Strategy

Define three types of health endpoints per Kubernetes best practices.

### Endpoint Types

| Endpoint | Probe Type | Purpose | Checks |
|----------|------------|---------|--------|
| `/health/live` | Liveness | Is app alive? | App responds (no dependency checks) |
| `/health/ready` | Readiness | Can app serve traffic? | All dependencies healthy |
| `/health/startup` | Startup (K8s 1.16+) | Is app initialized? | Initial warmup complete |

### When Each Probe Fails

| Probe | Failure Action | Kubernetes Behavior |
|-------|----------------|---------------------|
| Liveness | Container restart | kubelet restarts container |
| Readiness | Remove from service | Traffic stopped, no restart |
| Startup | Delay other probes | Liveness/Readiness paused |

---

## Phase 3: Research Health Check Patterns

Use MCP tools for current documentation.

**For .NET:**
```
MCP ref: "ASP.NET Core health checks Kubernetes probes"
Context7: /dotnet/aspnetcore
```

**For Python:**
```
MCP ref: "FastAPI health check endpoint Kubernetes"
Context7: /tiangolo/fastapi
```

**Key Patterns to Research:**
1. Database health checks (connection pool)
2. Redis connectivity check
3. Custom health check implementation
4. Health check response writer customization

---

## Phase 4: Configure Kubernetes Probes

Determine probe timing based on application characteristics.

### Probe Configuration

| Parameter | Liveness | Readiness | Startup |
|-----------|----------|-----------|---------|
| `initialDelaySeconds` | 10 | 5 | 0 |
| `periodSeconds` | 10 | 5 | 5 |
| `timeoutSeconds` | 5 | 3 | 3 |
| `failureThreshold` | 3 | 3 | 30 |
| `successThreshold` | 1 | 1 | 1 |

**Startup Probe Calculation:**
```
Max startup time = initialDelaySeconds + (periodSeconds × failureThreshold)
Default: 0 + (5 × 30) = 150 seconds
```

---

## Phase 5: Generate Implementation

### .NET Output Files

| File | Purpose |
|------|---------|
| `Extensions/HealthCheckExtensions.cs` | Health check registration |
| `HealthChecks/StartupHealthCheck.cs` | Custom startup check |

**Generation Process:**
1. Use MCP ref for current ASP.NET Core health checks API
2. Generate HealthCheckExtensions with:
   - AddHealthChecks registration
   - Database health check (if detected)
   - Redis health check (if detected)
   - Custom StartupHealthCheck
3. Configure three endpoints with proper tags

**Packages to Add:**
- `AspNetCore.HealthChecks.NpgSql` (if PostgreSQL)
- `AspNetCore.HealthChecks.Redis` (if Redis)
- `AspNetCore.HealthChecks.MySql` (if MySQL)

**Registration Code:**
```csharp
builder.Services.AddHealthCheckServices(builder.Configuration);
// ...
app.MapHealthCheckEndpoints();
```

### Python Output Files

| File | Purpose |
|------|---------|
| `routes/health.py` | Health check router |
| `services/health_checker.py` | Dependency health checks |

**Generation Process:**
1. Use MCP ref for FastAPI health patterns
2. Generate health router with:
   - /health/live endpoint (simple)
   - /health/ready endpoint (with dependency checks)
   - /health/startup endpoint
3. Generate health_checker service for dependency verification

**Registration Code:**
```python
from routes.health import health_router
app.include_router(health_router)
```

### Kubernetes Manifest Snippet

Generate for inclusion in deployment.yaml:

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/ready
    port: 5000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

startupProbe:
  httpGet:
    path: /health/startup
    port: 5000
  periodSeconds: 5
  failureThreshold: 30
```

---

## Phase 6: Validate

**Validation Steps:**

1. **Syntax check:**
   - .NET: `dotnet build --no-restore`
   - Python: `python -m py_compile routes/health.py`

2. **Endpoint test:**
   ```bash
   curl http://localhost:5000/health/live
   curl http://localhost:5000/health/ready
   curl http://localhost:5000/health/startup
   ```

3. **Verify response format:**
   ```json
   {
     "status": "Healthy",
     "checks": {
       "database": { "status": "Healthy", "duration": "00:00:00.0234" },
       "redis": { "status": "Healthy", "duration": "00:00:00.0012" }
     },
     "totalDuration": "00:00:00.0250"
   }
   ```

4. **Dependency failure test:**
   - Stop database
   - Verify `/health/ready` returns 503
   - Verify `/health/live` still returns 200

---

## Return to Coordinator

```json
{
  "status": "success",
  "files_created": [
    "Extensions/HealthCheckExtensions.cs",
    "HealthChecks/StartupHealthCheck.cs"
  ],
  "packages_added": [
    "AspNetCore.HealthChecks.NpgSql"
  ],
  "registration_code": "builder.Services.AddHealthCheckServices(configuration);",
  "message": "Configured health checks with liveness, readiness, and startup probes"
}
```

---

## Reference Links

- [ASP.NET Core Health Checks](https://learn.microsoft.com/aspnet/core/host-and-deploy/health-checks)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [AWS EKS Health Check Best Practices](https://docs.aws.amazon.com/eks/latest/best-practices/application.html)

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
