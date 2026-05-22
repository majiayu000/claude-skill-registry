---
name: ln-771-logging-configurator
description: Configures structured logging (Serilog/.NET, structlog/Python)
---

# ln-771-logging-configurator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-770-crosscutting-setup

Configures structured JSON logging for .NET and Python projects.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Context Store from ln-770 |
| **Output** | Logging configuration files |
| **Stacks** | .NET (Serilog), Python (structlog) |

---

## Phase 1: Receive Context

Accept Context Store from coordinator.

**Required Context:**
- `STACK`: .NET or Python
- `FRAMEWORK`: ASP.NET Core or FastAPI
- `FRAMEWORK_VERSION`: Version number
- `PROJECT_ROOT`: Project directory path
- `ENVIRONMENT`: Development or Production

**Validation:**
- If `STACK` not provided, detect from project files
- If version not provided, use latest stable

---

## Phase 2: Research Current Best Practices

Use MCP tools to get up-to-date documentation.

**For .NET (Serilog):**
```
MCP ref: "Serilog ASP.NET Core structured logging configuration"
Context7: /serilog/serilog-aspnetcore
```

**For Python (structlog):**
```
MCP ref: "structlog Python structured logging configuration"
Context7: /hynek/structlog
```

**Key Patterns to Research:**
1. Request logging middleware
2. Log enrichment (correlation ID, user context)
3. Log level configuration by environment
4. Sink configuration (Console, File, Seq, Elastic)

---

## Phase 3: Decision Points

Ask user for configuration preferences.

### Q1: Log Format

| Option | When to Use |
|--------|-------------|
| **JSON** (Recommended for Production) | Machine-readable, log aggregation systems |
| **Pretty/Colored** (Recommended for Development) | Human-readable, local debugging |

### Q2: Enrichment Fields

| Field | Description | Default |
|-------|-------------|---------|
| `correlationId` | Request tracking across services | ✓ Yes |
| `userId` | Authenticated user identifier | ✓ Yes |
| `requestPath` | HTTP request path | ✓ Yes |
| `responseTime` | Request duration in ms | ✓ Yes |
| `machineName` | Server hostname | Optional |
| `threadId` | Thread identifier | Optional |

### Q3: Log Sinks

| Sink | Use Case |
|------|----------|
| **Console** | Always enabled |
| **File** | Local persistence, log rotation |
| **Seq** | Structured log server |
| **Elasticsearch** | Log aggregation at scale |

### Q4: Log Levels by Environment

| Level | Development | Production |
|-------|-------------|------------|
| Default | Debug | Information |
| Microsoft.* | Information | Warning |
| System.* | Information | Warning |
| Application | Debug | Information |

---

## Phase 4: Generate Configuration

Generate files based on stack and decisions.

### .NET Output Files

| File | Purpose |
|------|---------|
| `Extensions/LoggingExtensions.cs` | Service registration |
| `appsettings.json` (update) | Serilog configuration |
| `appsettings.Development.json` (update) | Dev overrides |

**Generation Process:**
1. Use MCP ref to get current Serilog API
2. Generate LoggingExtensions.cs with:
   - UseSerilog configuration
   - Request logging middleware
   - Enrichment configuration
3. Update appsettings.json with Serilog section

**Packages to Add:**
- `Serilog.AspNetCore`
- `Serilog.Sinks.Console`
- `Serilog.Sinks.File` (if File sink selected)
- `Serilog.Enrichers.Environment` (if machineName selected)

### Python Output Files

| File | Purpose |
|------|---------|
| `core/logging_config.py` | structlog configuration |
| `middleware/logging_middleware.py` | Request logging |

**Generation Process:**
1. Use MCP ref to get current structlog API
2. Generate logging_config.py with:
   - Processor chain configuration
   - Renderer selection (JSON/Console)
   - Log level configuration
3. Generate logging_middleware.py for FastAPI

**Packages to Add:**
- `structlog`
- `python-json-logger` (if JSON format)

---

## Phase 5: Validate

Verify the configuration works.

**Validation Steps:**

1. **Check imports:** Ensure all packages are available
   - .NET: `dotnet list package | grep Serilog`
   - Python: `pip list | grep structlog`

2. **Syntax check:**
   - .NET: `dotnet build --no-restore`
   - Python: `python -m py_compile core/logging_config.py`

3. **Test log output:**
   - Start application
   - Make test request
   - Verify log format matches configuration

**Expected Log Format:**
```json
{
  "timestamp": "2026-01-10T12:00:00.000Z",
  "level": "info",
  "message": "Request completed",
  "correlationId": "abc-123",
  "requestPath": "/api/health",
  "responseTime": 45,
  "statusCode": 200
}
```

---

## Return to Coordinator

Return result to ln-770:

```json
{
  "status": "success",
  "files_created": [
    "Extensions/LoggingExtensions.cs",
    "appsettings.json"
  ],
  "packages_added": [
    "Serilog.AspNetCore",
    "Serilog.Sinks.Console"
  ],
  "registration_code": "services.AddLoggingServices(configuration);",
  "message": "Configured structured logging with Serilog"
}
```

---

## Idempotency

This skill is idempotent:
- Phase 1: Check if logging already configured (Grep for Serilog/structlog)
- If configured: Return `{ "status": "skipped", "message": "Logging already configured" }`
- If not: Proceed with configuration

---

## Reference Links

- [Serilog.AspNetCore](https://github.com/serilog/serilog-aspnetcore)
- [structlog Documentation](https://www.structlog.org/)
- [ASP.NET Core Logging](https://learn.microsoft.com/aspnet/core/fundamentals/logging/)

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
