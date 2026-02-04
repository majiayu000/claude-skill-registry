---
name: aspire
description: Aspire orchestration for cloud-native distributed applications in any language (C#, Python, Node.js, Go). Handles dependency management, local dev with Docker, Azure deployment, service discovery, and observability dashboards. Use when setting up microservices, containerized apps, or polyglot distributed systems.
version: 1.0.0
source_urls:
  - https://learn.microsoft.com/dotnet/aspire/get-started/aspire-overview
  - https://learn.microsoft.com/dotnet/aspire/fundamentals/setup-tooling
  - https://github.com/dotnet/aspire
  - https://learn.microsoft.com/dotnet/aspire/database/postgresql-component
  - https://learn.microsoft.com/dotnet/aspire/caching/stackexchange-redis-component
  - https://learn.microsoft.com/dotnet/aspire/deployment/azure/aca-deployment
  - https://learn.microsoft.com/dotnet/aspire/service-discovery/overview
  - https://learn.microsoft.com/dotnet/aspire/fundamentals/dashboard
activation_keywords:
  - aspire
  - distributed app
  - microservices
  - service discovery
  - apphost
  - cloud-native
  - orchestration
auto_activate: true
token_budget: 1800
---

# Aspire Orchestration

## Overview

Code-first orchestration for polyglot distributed apps. AppHost defines topology, `aspire run` orchestrates locally, `azd deploy` deploys to Azure.

**Auto-activates** on keywords: aspire, microservices, distributed app, service discovery, orchestration

## Quick Start

```bash
# Install .NET 8+ and Aspire workload
# See: https://learn.microsoft.com/dotnet/aspire/fundamentals/setup-tooling
dotnet workload update
dotnet workload install aspire

# Create AppHost (orchestrates services in ANY language)
dotnet new aspire-apphost -n MyApp

# Basic AppHost - orchestrate Python, Node.js, .NET services
var builder = DistributedApplication.CreateBuilder(args);
var redis = builder.AddRedis("cache");

// Python service
var pythonApi = builder.AddExecutable("python-api", "python", ".").WithArgs("app.py").WithReference(redis);

// Node.js service
var nodeApi = builder.AddExecutable("node-api", "node", ".").WithArgs("server.js").WithReference(redis);

// .NET service
var dotnetApi = builder.AddProject<Projects.Api>("api").WithReference(redis);

builder.Build().Run();

# Run (orchestrates ALL languages)
aspire run  # Dashboard opens at http://localhost:15888
```

## Core Workflows

### Project Setup

```bash
dotnet new aspire-apphost -n MyApp
dotnet new webapi -n MyApp.Api
dotnet add MyApp.AppHost reference MyApp.Api
```

**AppHost**: Resource topology in `Program.cs`
**ServiceDefaults**: Shared config (logging, telemetry, resilience)
**Services**: Your apps (APIs, workers, web apps)

### Dependency Configuration

```csharp
// PostgreSQL
var postgres = builder.AddPostgres("db").AddDatabase("mydb");
var api = builder.AddProject<Projects.Api>("api").WithReference(postgres);

// Redis
var redis = builder.AddRedis("cache").WithRedisCommander();
var api = builder.AddProject<Projects.Api>("api").WithReference(redis);

// RabbitMQ
var rabbitmq = builder.AddRabbitMQ("messaging");
var worker = builder.AddProject<Projects.Worker>("worker").WithReference(rabbitmq);

// Access in code (connection strings auto-injected)
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("cache");
});
```

### Local Development

```bash
aspire run  # Starts all services
```

**Dashboard** (localhost:15888): Resources, logs, traces, metrics
**Hot Reload**: Auto-rebuild on code changes
**Debugging**: Attach to individual services via IDE

### Cloud Deployment

See [Azure deployment guide](https://learn.microsoft.com/dotnet/aspire/deployment/azure/aca-deployment).

```bash
azd init  # Initialize Azure Developer CLI
azd up    # Deploy (generates Bicep → Azure Container Apps)
azd deploy -e production  # Deploy to specific environment
```

**Generates:** Bicep → Container Apps + networking + managed identities

## Navigation Guide

**When setting up projects:**
- examples.md lines 8-31 → Minimal project
- examples.md lines 518-608 → Add Python service
- examples.md lines 610-669 → Add Node.js service
- examples.md lines 671-768 → Add Go service

**When adding infrastructure:**
- reference.md lines 47-148 → Database APIs (PostgreSQL, Redis, MongoDB)
- examples.md lines 39-95 → Redis integration
- examples.md lines 102-176 → PostgreSQL integration

**When deploying:**
- commands.md lines 215-288 → Full azd workflow
- examples.md lines 387-515 → Azure deployment walkthrough
- patterns.md lines 5-42 → HA configuration

**When debugging:**
- troubleshooting.md lines 5-112 → Orchestration failures
- troubleshooting.md lines 291-397 → Connection issues
- commands.md lines 131-179 → Debug commands

## Quick Reference

**Essential commands:** See commands.md for complete reference

**Polyglot patterns:**
```csharp
builder.AddProject<Projects.Api>("api");  // .NET
builder.AddExecutable("python-api", "python", ".").WithArgs("app.py");  // Python
builder.AddExecutable("node-api", "node", ".").WithArgs("server.js");  // Node.js
builder.AddExecutable("go-svc", "go", ".").WithArgs("run", "main.go");  // Go
```

**Service discovery:** `.WithReference(redis)` in AppHost → `GetConnectionString("cache")` in service

## Integration with Amplihack

**Command**: `/ultrathink "Setup Aspire for microservices"`
- prompt-writer clarifies requirements → architect uses reference.md for API design
- builder uses examples.md for implementation → reviewer checks patterns.md for best practices
- tester uses troubleshooting.md for validation

**Agent-Skill mapping**:
- architect → reference.md (API design)
- builder → examples.md (implementation)
- reviewer → patterns.md (best practices)
- tester → troubleshooting.md (validation)
- all agents → commands.md (CLI operations)

