---
name: ln-770-crosscutting-setup
description: Coordinates logging, error handling, CORS, health checks, and API docs
---

# ln-770-crosscutting-setup

**Type:** L2 Domain Coordinator
**Category:** 7XX Project Bootstrap
**Parent:** ln-700-project-bootstrap

Coordinates cross-cutting concerns configuration for .NET and Python projects.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project root directory |
| **Output** | Configured logging, error handling, CORS, health checks, API docs |
| **Workers** | ln-771 to ln-775 |
| **Stacks** | .NET (ASP.NET Core), Python (FastAPI) |

---

## Phase 1: Detect Project Stack

Determine the technology stack by scanning project files.

**Detection Rules:**

| File Pattern | Stack | Framework |
|--------------|-------|-----------|
| `*.csproj` | .NET | ASP.NET Core |
| `pyproject.toml` or `requirements.txt` + FastAPI | Python | FastAPI |

**Actions:**
1. Glob for `*.csproj` files
2. If not found, Glob for `pyproject.toml` or `requirements.txt`
3. If Python, check for FastAPI in dependencies
4. Store detected stack in Context Store

**Context Store Initial:**
```json
{
  "STACK": ".NET" | "Python",
  "FRAMEWORK": "ASP.NET Core" | "FastAPI",
  "PROJECT_ROOT": "/path/to/project",
  "FRAMEWORK_VERSION": "8.0" | "0.109.0"
}
```

---

## Phase 2: Check Existing Configuration

Scan for already configured cross-cutting concerns.

**Detection Patterns:**

| Concern | .NET Pattern | Python Pattern |
|---------|--------------|----------------|
| Logging | `Serilog` in *.csproj, `UseSerilog` in Program.cs | `structlog` in requirements, logging config |
| Error Handling | `GlobalExceptionMiddleware`, `UseExceptionHandler` | `@app.exception_handler`, exception_handlers.py |
| CORS | `AddCors`, `UseCors` | `CORSMiddleware` |
| Health Checks | `AddHealthChecks`, `MapHealthChecks` | `/health` routes |
| API Docs | `AddSwaggerGen`, `UseSwagger` | FastAPI auto-generates |

**Actions:**
1. Grep for each pattern
2. Mark configured concerns as `skip: true`
3. Update Context Store with findings

**Context Store Updated:**
```json
{
  "concerns": {
    "logging": { "configured": false },
    "errorHandling": { "configured": false },
    "cors": { "configured": true, "skip": true },
    "healthChecks": { "configured": false },
    "apiDocs": { "configured": false }
  }
}
```

---

## Phase 3: Invoke Workers (Conditional)

Delegate to workers only for unconfigured concerns.

**Worker Invocation Order:**

| Order | Worker | Condition | Skill Call |
|-------|--------|-----------|------------|
| 1 | ln-771-logging-configurator | `logging.configured == false` | `/skill ln-771-logging-configurator` |
| 2 | ln-772-error-handler-setup | `errorHandling.configured == false` | `/skill ln-772-error-handler-setup` |
| 3 | ln-773-cors-configurator | `cors.configured == false` | `/skill ln-773-cors-configurator` |
| 4 | ln-774-healthcheck-setup | `healthChecks.configured == false` | `/skill ln-774-healthcheck-setup` |
| 5 | ln-775-api-docs-generator | `apiDocs.configured == false` | `/skill ln-775-api-docs-generator` |

**Pass Context Store to each worker.**

**Worker Response Format:**
```json
{
  "status": "success" | "skipped" | "error",
  "files_created": ["path/to/file.cs"],
  "packages_added": ["Serilog.AspNetCore"],
  "message": "Configured structured logging with Serilog"
}
```

---

## Phase 4: Generate Aggregation File

Create a single entry point for all cross-cutting services.

### .NET: Extensions/ServiceExtensions.cs

Generate based on configured workers:

```
// Structure only - actual code generated via MCP ref
public static class ServiceExtensions
{
    public static IServiceCollection AddCrosscuttingServices(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Calls added based on configured workers:
        // services.AddLogging(configuration);      // if ln-771 ran
        // services.AddCorsPolicy(configuration);   // if ln-773 ran
        // services.AddHealthChecks();              // if ln-774 ran
        // services.AddSwaggerServices();           // if ln-775 ran
        return services;
    }
}
```

### Python: middleware/__init__.py

Generate based on configured workers:

```
# Structure only - actual code generated via MCP ref
def configure_middleware(app):
    # Middleware added based on configured workers:
    # configure_logging(app)        # if ln-771 ran
    # configure_error_handlers(app) # if ln-772 ran
    # configure_cors(app)           # if ln-773 ran
    # configure_health_routes(app)  # if ln-774 ran
    pass
```

---

## Phase 5: Summary Report

Display summary of all configured concerns.

**Output Format:**

```
Cross-cutting Setup Complete
============================
Stack: .NET (ASP.NET Core 8.0)

Configured:
  ✓ Logging (Serilog) - Extensions/LoggingExtensions.cs
  ✓ Error Handling - Middleware/GlobalExceptionMiddleware.cs
  ✓ CORS - Extensions/CorsExtensions.cs
  ✓ Health Checks - Extensions/HealthCheckExtensions.cs
  ✓ API Docs (Swagger) - Extensions/SwaggerExtensions.cs

Skipped (already configured):
  - None

Entry Point: Extensions/ServiceExtensions.cs
  Add to Program.cs: builder.Services.AddCrosscuttingServices(builder.Configuration);

Packages to Install:
  dotnet add package Serilog.AspNetCore
  dotnet add package Swashbuckle.AspNetCore
```

---

## Workers

| Worker | Purpose | Stacks |
|--------|---------|--------|
| [ln-771-logging-configurator](../ln-771-logging-configurator/SKILL.md) | Structured logging | .NET (Serilog), Python (structlog) |
| [ln-772-error-handler-setup](../ln-772-error-handler-setup/SKILL.md) | Global exception middleware | .NET, Python |
| [ln-773-cors-configurator](../ln-773-cors-configurator/SKILL.md) | CORS policy configuration | .NET, Python |
| [ln-774-healthcheck-setup](../ln-774-healthcheck-setup/SKILL.md) | /health endpoints | .NET, Python |
| [ln-775-api-docs-generator](../ln-775-api-docs-generator/SKILL.md) | Swagger/OpenAPI | .NET (Swashbuckle), Python (FastAPI built-in) |

---

## Context Store Interface

Workers receive and return via Context Store:

**Input to Workers:**
```json
{
  "STACK": ".NET",
  "FRAMEWORK": "ASP.NET Core",
  "FRAMEWORK_VERSION": "8.0",
  "PROJECT_ROOT": "/path/to/project",
  "ENVIRONMENT": "Development"
}
```

**Output from Workers:**
```json
{
  "status": "success",
  "files_created": [],
  "packages_added": [],
  "registration_code": "services.AddLogging(configuration);"
}
```

---

## Idempotency

This skill is idempotent:
- Phase 2 detects existing configuration
- Workers skip if already configured
- Aggregation file preserves existing entries

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
