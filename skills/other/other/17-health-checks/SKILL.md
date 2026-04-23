---
name: health-checks
description: "Configures health checks for database, external services, and custom application checks. Provides liveness and readiness endpoints for container orchestration."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: AspNetCore.HealthChecks.NpgSql, AspNetCore.HealthChecks.UI.Client
---

# Health Checks Configuration

## Overview

Health checks monitor application dependencies:

- **Liveness** - Is the app running?
- **Readiness** - Is the app ready to serve traffic?
- **Database checks** - PostgreSQL connectivity
- **External service checks** - APIs, caches, queues
- **Custom checks** - Business logic validation

## Quick Reference

| Check Type | Purpose |
|------------|---------|
| `AddNpgSql` | PostgreSQL database |
| `AddUrlGroup` | External HTTP endpoints |
| `AddRedis` | Redis cache |
| `AddRabbitMQ` | RabbitMQ message broker |
| Custom | Application-specific checks |

---

## Template: Health Check Registration

```csharp
// src/{name}.infrastructure/HealthChecks/HealthCheckExtensions.cs
using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace {name}.infrastructure.healthchecks;

public static class HealthCheckExtensions
{
    public static IServiceCollection AddHealthChecks(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddHealthChecks()
            // ═══════════════════════════════════════════════════════════════
            // DATABASE
            // ═══════════════════════════════════════════════════════════════
            .AddNpgSql(
                configuration.GetConnectionString("Database")!,
                name: "postgresql",
                failureStatus: HealthStatus.Unhealthy,
                tags: new[] { "db", "sql", "postgresql", "ready" })

            // ═══════════════════════════════════════════════════════════════
            // EXTERNAL SERVICES
            // ═══════════════════════════════════════════════════════════════
            .AddUrlGroup(
                new Uri(configuration["AuthService:BaseUrl"]!),
                name: "auth-service",
                failureStatus: HealthStatus.Degraded,
                tags: new[] { "external", "auth", "ready" })

            // ═══════════════════════════════════════════════════════════════
            // REDIS (if used)
            // ═══════════════════════════════════════════════════════════════
            // .AddRedis(
            //     configuration.GetConnectionString("Redis")!,
            //     name: "redis",
            //     tags: new[] { "cache", "redis", "ready" })

            // ═══════════════════════════════════════════════════════════════
            // CUSTOM CHECKS
            // ═══════════════════════════════════════════════════════════════
            .AddCheck<DatabaseMigrationHealthCheck>(
                "database-migrations",
                tags: new[] { "db", "migrations", "ready" });

        return services;
    }
}
```

---

## Template: Custom Health Check

```csharp
// src/{name}.infrastructure/HealthChecks/DatabaseMigrationHealthCheck.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace {name}.infrastructure.healthchecks;

internal sealed class DatabaseMigrationHealthCheck : IHealthCheck
{
    private readonly ApplicationDbContext _dbContext;

    public DatabaseMigrationHealthCheck(ApplicationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var pendingMigrations = await _dbContext.Database
                .GetPendingMigrationsAsync(cancellationToken);

            var pending = pendingMigrations.ToList();

            if (pending.Any())
            {
                return HealthCheckResult.Degraded(
                    $"Pending migrations: {string.Join(", ", pending)}",
                    data: new Dictionary<string, object>
                    {
                        { "pending_count", pending.Count },
                        { "migrations", pending }
                    });
            }

            return HealthCheckResult.Healthy("All migrations applied");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy(
                "Failed to check migrations",
                exception: ex);
        }
    }
}
```

---

## Template: Program.cs Configuration

```csharp
// src/{name}.api/Program.cs
using HealthChecks.UI.Client;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;

var app = builder.Build();

// ═══════════════════════════════════════════════════════════════
// LIVENESS: Is the app running?
// ═══════════════════════════════════════════════════════════════
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false,  // No checks, just confirms app is running
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

// ═══════════════════════════════════════════════════════════════
// READINESS: Is the app ready to serve traffic?
// ═══════════════════════════════════════════════════════════════
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready"),
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

// ═══════════════════════════════════════════════════════════════
// FULL: All health checks
// ═══════════════════════════════════════════════════════════════
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});
```

---

## Kubernetes Configuration

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: api
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
```

---

## Related Skills

- `dotnet-clean-architecture` - Infrastructure layer setup
- `jwt-authentication` - Auth service health check
