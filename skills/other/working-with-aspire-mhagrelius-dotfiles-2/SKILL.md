---
name: working-with-aspire
description: Use when building distributed apps with Aspire; orchestrating .NET, JavaScript, Python, or polyglot services; when environment variables or service discovery aren't working; when migrating from .NET Aspire 9 to 13+ or Community Toolkit; when seeing AddNpmApp deprecated errors; when OTEL not appearing in dashboard; when ports change on restart breaking OAuth; when configuring MCP server for AI assistants; when debugging Aspire apps and need to check resource status or logs
---

# Working with .NET Aspire 13

## For AI Assistants: Use MCP Tools

**CRITICAL:** When helping users debug Aspire applications, use the Aspire MCP tools instead of curl, external HTTP calls, or suggesting manual dashboard inspection.

| Task | MCP Tool | NOT This |
|------|----------|----------|
| Check resource status | `list_resources` | ❌ curl to dashboard API |
| Get service logs | `list_console_logs` | ❌ curl, docker logs |
| View traces | `list_traces` | ❌ curl to OTLP endpoint |
| Find errors in traces | `list_trace_structured_logs` | ❌ manual dashboard search |
| List available AppHosts | `list_apphosts` | ❌ file system search |

If MCP is not configured, guide the user to run `aspire mcp init` in their AppHost directory.

## Quick Reference

| Task | Reference File |
|------|----------------|
| AppHost patterns, resources, lifecycle | `app-host.md` |
| Azure integrations (databases, messaging, AI) | `azure-integrations.md` |
| Database integrations (Postgres, SQL, Mongo) | `database-integrations.md` |
| Caching (Redis, Valkey, Garnet) | `caching-integrations.md` |
| Messaging (Kafka, RabbitMQ, NATS) | `messaging-integrations.md` |
| Polyglot (Node.js, Python, Go, Rust, Java) | `polyglot-integrations.md` |
| Deployment, CLI, and aspire do pipelines | `deployment-cli.md` |
| Testing with Aspire | `testing.md` |
| Errors and troubleshooting | `diagnostics.md` |
| MCP integration for AI assistants | `mcp-integration.md` |
| VS Code extension | `vs-code-extension.md` |
| Certificate trust configuration | `certificate-config.md` |
| Migration from 9.x to 13.x | `aspire-13-migration.md` |

## Common Mistakes

### ❌ Wrong: Using non-existent or deprecated APIs

| Wrong | Correct | Why |
|-------|---------|-----|
| `AddPythonUvicornApp` | `AddUvicornApp` | Method is just `AddUvicornApp` |
| `AddNpmApp` | `AddViteApp` or `AddJavaScriptApp` | `AddNpmApp` removed in 13.0 |
| `AddPythonApp` for FastAPI | `AddUvicornApp` | Use AddUvicornApp for ASGI (FastAPI, Starlette) |
| `Aspire.Hosting.NodeJs` | `Aspire.Hosting.JavaScript` | Package renamed in 13.0 |

### ❌ Wrong: Putting secrets in appsettings.json

```csharp
// WRONG - secrets exposed in source control
// appsettings.json: { "Parameters": { "api-key": "secret123" } }

// CORRECT - use user-secrets for development
// dotnet user-secrets set "Parameters:api-key" "secret123"
```

## Aspire 13 Breaking Changes

**Critical:** Migration from Aspire 9.x requires attention. See `aspire-13-migration.md` for full details.

### JavaScript/Node.js Changes (13.0)
```csharp
// BEFORE (9.x) - REMOVED IN 13.0
builder.AddNpmApp("frontend", "../app", scriptName: "dev", args: ["--no-open"])

// AFTER (13.0) - Use AddJavaScriptApp or AddViteApp
builder.AddJavaScriptApp("frontend", "../app")
    .WithRunScript("dev")
    .WithArgs("--no-open");

// For Vite/React specifically:
builder.AddViteApp("frontend", "../app")
    .WithHttpEndpoint(env: "PORT");

// Package renamed: Aspire.Hosting.NodeJs → Aspire.Hosting.JavaScript
```

### Azure Redis Changes (13.1)
```csharp
// BEFORE (13.0) - DEPRECATED
builder.AddAzureRedisEnterprise("cache")

// AFTER (13.1)
builder.AddAzureManagedRedis("cache")
```

### Network Context Changes (13.0)
```csharp
// BEFORE (9.x) - containerHostName parameter removed
await resource.ProcessArgumentValuesAsync(
    executionContext, processValue, logger,
    containerHostName: "localhost", cancellationToken);

// AFTER (13.0) - Use NetworkIdentifier
await resource.ProcessArgumentValuesAsync(
    executionContext, processValue, logger, cancellationToken);

// Get endpoints with network context
var endpoint = api.GetEndpoint("http", KnownNetworkIdentifiers.DefaultAspireContainerNetwork);
```

### Publishing API Changes (13.0)
```csharp
// BEFORE (9.x)
public class MyPublisher : IDistributedApplicationPublisher { }

// AFTER (13.0) - Use aspire do pipelines instead
// IDistributedApplicationPublisher is deprecated
```

## Aspire 13.0+ New Features

### Certificate Trust Automation
```csharp
// Automatic - no configuration needed
var pythonApi = builder.AddUvicornApp("api", "./api", "main:app");
var nodeApi = builder.AddJavaScriptApp("frontend", "./frontend");
// Both automatically trust development certificates
```

### MCP Integration for AI Assistants
```bash
# Initialize MCP for Claude Code, GitHub Copilot, etc.
aspire mcp init
```

### aspire do Pipeline System
```bash
aspire do build           # Build container images
aspire do push            # Push to registry
aspire do deploy          # Full deployment
aspire do diagnostics     # Show available steps
```

### aspire init (Aspirify Existing Projects)
```bash
aspire init               # Interactive setup
aspire init --single-file # Create .cs AppHost without .csproj
```

### Single-File AppHost
```csharp
// apphost.cs - no project file needed
#:package Aspire.Hosting@*
#:package Aspire.Hosting.Redis@*

var builder = DistributedApplication.CreateBuilder(args);
var cache = builder.AddRedis("cache");
builder.Build().Run();
```

## Common Patterns

### FastAPI + React (Vite) Full Stack
```csharp
// Required packages:
// dotnet add package Aspire.Hosting.Python
// dotnet add package Aspire.Hosting.JavaScript  (NOT NodeJs!)
// dotnet add package Aspire.Hosting.PostgreSQL

var builder = DistributedApplication.CreateBuilder(args);

// Database
var db = builder.AddPostgres("db")
    .AddDatabase("appdata")
    .WithDataVolume();

// FastAPI backend - use AddUvicornApp (NOT AddPythonApp!)
var api = builder.AddUvicornApp("api", "../api", "main:app")
    .WithHttpEndpoint(port: 8000, env: "PORT")
    .WithReference(db)
    .WaitFor(db);

// React frontend - use AddViteApp (NOT AddNpmApp!)
builder.AddViteApp("frontend", "../frontend")
    .WithHttpEndpoint(env: "PORT")
    .WithExternalHttpEndpoints()
    .WithReference(api);

builder.Build().Run();
```

Frontend reads API URL from env: `process.env.services__api__http__0`

### Basic AppHost Structure
```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Database
var db = builder.AddPostgres("db")
    .AddDatabase("appdata")
    .WithDataVolume();

// API with database reference
var api = builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WaitFor(db);

// Frontend with API reference
builder.AddViteApp("frontend", "../frontend")
    .WithHttpEndpoint(env: "PORT")
    .WithReference(api);

builder.Build().Run();
```

### Service Discovery Pattern
```csharp
// Producer exposes endpoint
var api = builder.AddProject<Projects.Api>("api")
    .WithHttpEndpoint(port: 5000, name: "api");

// Consumer references it (gets services__api__api__0 env var)
builder.AddProject<Projects.Web>("web")
    .WithReference(api);
```

### Health Checks and Wait
```csharp
var db = builder.AddPostgres("db");
var cache = builder.AddRedis("cache");

builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WithReference(cache)
    .WaitFor(db)           // Wait for running
    .WaitForHealthy(cache); // Wait for healthy (requires health check)
```

## When to Read Specific Files

**Read `app-host.md` when:**
- Setting up new AppHost project
- Understanding resource lifecycle events
- Configuring endpoints and networking
- Using parameters and secrets

**Read `azure-integrations.md` when:**
- Using Azure services (Cosmos, Service Bus, Storage)
- Running Azure emulators locally
- Using `RunAsEmulator()` or `RunAsContainer()`
- Customizing Bicep output

**Read `polyglot-integrations.md` when:**
- Adding Node.js, Python, Go, Rust, or Java apps
- Frontend frameworks (Vite, Angular, React)
- Container-based polyglot services
- Migrating from AddNpmApp to AddJavaScriptApp

**Read `deployment-cli.md` when:**
- Using `aspire deploy`, `aspire publish`, or `aspire do`
- Using `aspire init` to Aspirify existing projects
- Setting up CI/CD pipelines
- Understanding manifest format

**Read `mcp-integration.md` when:**
- Setting up AI assistant integration
- Configuring Claude Code, GitHub Copilot, or Cursor
- Excluding resources from MCP access

**Read `vs-code-extension.md` when:**
- Using Aspire in VS Code
- Debugging polyglot applications
- Creating new Aspire projects in VS Code

**Read `certificate-config.md` when:**
- Configuring HTTPS for polyglot apps
- Custom certificate authorities
- Certificate trust issues between services

**Read `aspire-13-migration.md` when:**
- Upgrading from Aspire 9.x
- Seeing deprecated API warnings
- Container networking issues after upgrade

**Read `diagnostics.md` when:**
- Seeing ASPIRE* compiler errors
- Debugging service discovery issues
- Troubleshooting container startup
