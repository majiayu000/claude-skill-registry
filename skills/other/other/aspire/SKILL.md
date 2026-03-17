---
name: aspire
description: |
  Use when building cloud-native distributed applications with .NET Aspire. Covers the app host orchestration model, service defaults, built-in components (Redis, PostgreSQL, RabbitMQ), dashboard, health checks, and deployment to Azure Container Apps.
  USE FOR: orchestrating multi-service .NET applications, adding Redis/PostgreSQL/RabbitMQ with one line, built-in OpenTelemetry observability, local development dashboard for distributed apps, service discovery between projects
  DO NOT USE FOR: single-project monolithic applications without external dependencies, Kubernetes-native deployments with Helm (use standard containers), non-.NET polyglot microservices without .NET orchestration, Dapr sidecar architecture (use dapr)
license: MIT
metadata:
  displayName: ".NET Aspire"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: ".NET Aspire Documentation"
    url: "https://learn.microsoft.com/dotnet/aspire"
  - title: ".NET Aspire GitHub Repository"
    url: "https://github.com/dotnet/aspire"
---

# .NET Aspire

## Overview
.NET Aspire is an opinionated framework for building observable, production-ready, cloud-native distributed applications. It provides an app host project for orchestrating multi-service applications, service defaults for consistent configuration (OpenTelemetry, health checks, resilience), and pre-built components for common infrastructure like Redis, PostgreSQL, RabbitMQ, and Azure services. The Aspire dashboard provides real-time visibility into traces, logs, and metrics during local development.

## Project Structure
```
MyApp/
  MyApp.AppHost/           # Orchestration project (references all services)
  MyApp.ServiceDefaults/   # Shared configuration (telemetry, health checks)
  MyApp.Api/               # Web API project
  MyApp.Worker/            # Background worker project
  MyApp.Web/               # Frontend project
```

## Getting Started
```bash
dotnet new aspire-starter -n MyApp
# Creates AppHost, ServiceDefaults, Api, and Web projects
```

## App Host (Orchestration)
The AppHost project defines the distributed application topology: which services to run, what infrastructure they need, and how they connect.

```csharp
// MyApp.AppHost/Program.cs
var builder = DistributedApplication.CreateBuilder(args);

// Infrastructure resources
var cache = builder.AddRedis("cache")
    .WithRedisCommander();  // Adds Redis Commander UI

var postgres = builder.AddPostgres("postgres")
    .WithPgAdmin()          // Adds pgAdmin UI
    .WithDataVolume();      // Persists data across restarts

var db = postgres.AddDatabase("appdb");

var rabbit = builder.AddRabbitMQ("messaging")
    .WithManagementPlugin();  // Adds RabbitMQ management UI

// Application projects
var api = builder.AddProject<Projects.MyApp_Api>("api")
    .WithReference(db)
    .WithReference(cache)
    .WithReference(rabbit)
    .WithExternalHttpEndpoints();

builder.AddProject<Projects.MyApp_Worker>("worker")
    .WithReference(db)
    .WithReference(rabbit);

builder.AddProject<Projects.MyApp_Web>("web")
    .WithReference(api)
    .WithExternalHttpEndpoints();

builder.Build().Run();
```

## Service Defaults
Shared configuration that every service in the application uses.

```csharp
// MyApp.ServiceDefaults/Extensions.cs
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using OpenTelemetry;
using OpenTelemetry.Metrics;
using OpenTelemetry.Trace;

public static class Extensions
{
    public static IHostApplicationBuilder AddServiceDefaults(
        this IHostApplicationBuilder builder)
    {
        builder.ConfigureOpenTelemetry();
        builder.AddDefaultHealthChecks();
        builder.Services.AddServiceDiscovery();

        builder.Services.ConfigureHttpClientDefaults(http =>
        {
            http.AddStandardResilienceHandler();
            http.AddServiceDiscovery();
        });

        return builder;
    }

    public static IHostApplicationBuilder ConfigureOpenTelemetry(
        this IHostApplicationBuilder builder)
    {
        builder.Logging.AddOpenTelemetry(logging =>
        {
            logging.IncludeFormattedMessage = true;
            logging.IncludeScopes = true;
        });

        builder.Services.AddOpenTelemetry()
            .WithMetrics(metrics =>
            {
                metrics
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddRuntimeInstrumentation();
            })
            .WithTracing(tracing =>
            {
                tracing
                    .AddAspNetCoreInstrumentation()
                    .AddHttpClientInstrumentation()
                    .AddEntityFrameworkCoreInstrumentation();
            });

        builder.AddOpenTelemetryExporters();
        return builder;
    }

    public static IHostApplicationBuilder AddDefaultHealthChecks(
        this IHostApplicationBuilder builder)
    {
        builder.Services.AddHealthChecks()
            .AddCheck("self", () => HealthCheckResult.Healthy(), ["live"]);

        return builder;
    }

    public static WebApplication MapDefaultEndpoints(this WebApplication app)
    {
        app.MapHealthChecks("/health");
        app.MapHealthChecks("/alive", new HealthCheckOptions
        {
            Predicate = r => r.Tags.Contains("live")
        });

        return app;
    }
}
```

## Service Project Configuration
```csharp
// MyApp.Api/Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

// Aspire component for PostgreSQL with EF Core
builder.AddNpgsqlDbContext<AppDbContext>("appdb");

// Aspire component for Redis caching
builder.AddRedisDistributedCache("cache");

// Aspire component for RabbitMQ
builder.AddRabbitMQClient("messaging");

builder.Services.AddControllers();

var app = builder.Build();

app.MapDefaultEndpoints();
app.MapControllers();
app.Run();
```

## Built-in Components

| Component | NuGet Package | AddXxx Method |
|-----------|--------------|---------------|
| PostgreSQL (EF Core) | `Aspire.Npgsql.EntityFrameworkCore` | `AddNpgsqlDbContext<T>` |
| PostgreSQL (Npgsql) | `Aspire.Npgsql` | `AddNpgsqlDataSource` |
| Redis (Caching) | `Aspire.StackExchange.Redis.DistributedCaching` | `AddRedisDistributedCache` |
| Redis (Output Cache) | `Aspire.StackExchange.Redis.OutputCaching` | `AddRedisOutputCache` |
| RabbitMQ | `Aspire.RabbitMQ.Client` | `AddRabbitMQClient` |
| Azure Blob Storage | `Aspire.Azure.Storage.Blobs` | `AddAzureBlobClient` |
| Azure Service Bus | `Aspire.Azure.Messaging.ServiceBus` | `AddAzureServiceBusClient` |
| Azure Key Vault | `Aspire.Azure.Security.KeyVault` | `AddAzureKeyVaultClient` |
| MongoDB | `Aspire.MongoDB.Driver` | `AddMongoDBClient` |
| Seq (Logging) | `Aspire.Seq` | `AddSeqEndpoint` |

## Using Aspire Components in Services
```csharp
// PostgreSQL with Entity Framework Core
var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();
builder.AddNpgsqlDbContext<CatalogDbContext>("catalogdb");

var app = builder.Build();

app.MapGet("/products", async (CatalogDbContext db) =>
    await db.Products.ToListAsync());

app.MapPost("/products", async (Product product, CatalogDbContext db) =>
{
    db.Products.Add(product);
    await db.SaveChangesAsync();
    return Results.Created($"/products/{product.Id}", product);
});

// Redis distributed caching
app.MapGet("/products/{id}", async (
    int id, CatalogDbContext db, IDistributedCache cache) =>
{
    var cacheKey = $"product:{id}";
    var cached = await cache.GetStringAsync(cacheKey);
    if (cached is not null)
        return Results.Ok(JsonSerializer.Deserialize<Product>(cached));

    var product = await db.Products.FindAsync(id);
    if (product is null) return Results.NotFound();

    await cache.SetStringAsync(cacheKey,
        JsonSerializer.Serialize(product),
        new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5)
        });

    return Results.Ok(product);
});
```

## Service Discovery and HTTP Clients
```csharp
// In the API project, call another service by name
var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();

builder.Services.AddHttpClient<CatalogClient>(client =>
{
    // "catalog-api" is resolved via service discovery from the AppHost
    client.BaseAddress = new Uri("https+http://catalog-api");
});

var app = builder.Build();

app.MapGet("/orders/{id}/details", async (int id, CatalogClient catalog) =>
{
    var products = await catalog.GetProductsForOrderAsync(id);
    return Results.Ok(products);
});

public class CatalogClient(HttpClient httpClient)
{
    public async Task<List<Product>> GetProductsForOrderAsync(int orderId) =>
        await httpClient.GetFromJsonAsync<List<Product>>(
            $"/api/orders/{orderId}/products") ?? [];
}
```

## Custom Resources
```csharp
// Add a container resource for services not built into Aspire
var elasticsearch = builder.AddContainer("elasticsearch", "elasticsearch", "8.12.0")
    .WithHttpEndpoint(port: 9200, targetPort: 9200)
    .WithEnvironment("discovery.type", "single-node")
    .WithEnvironment("xpack.security.enabled", "false")
    .WithVolume("es-data", "/usr/share/elasticsearch/data");

builder.AddProject<Projects.MyApp_Api>("api")
    .WithReference(elasticsearch);
```

## Environment and Parameters
```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Parameters (prompted at deploy time or from config)
var adminPassword = builder.AddParameter("admin-password", secret: true);

var postgres = builder.AddPostgres("postgres", password: adminPassword);

// Connection strings from configuration
var apiKey = builder.AddParameter("api-key", secret: true);

builder.AddProject<Projects.MyApp_Api>("api")
    .WithEnvironment("ApiKey", apiKey);
```

## Deployment to Azure Container Apps
```bash
# Install the azd CLI
winget install microsoft.azd

# Initialize and deploy
azd init
azd up
```

```csharp
// AppHost with Azure-specific resources
var builder = DistributedApplication.CreateBuilder(args);

var insights = builder.AddAzureApplicationInsights("insights");
var storage = builder.AddAzureStorage("storage");
var blobs = storage.AddBlobs("blobs");

builder.AddProject<Projects.MyApp_Api>("api")
    .WithReference(insights)
    .WithReference(blobs);
```

## Best Practices
- Use the AppHost project solely for orchestration (defining resources, references, and endpoints); never put business logic, controllers, or domain code in the AppHost.
- Call `builder.AddServiceDefaults()` as the first line in every service project's `Program.cs` to ensure consistent OpenTelemetry, health checks, resilience, and service discovery configuration.
- Use `WithDataVolume()` on database resources (PostgreSQL, Redis) during development to persist data across container restarts rather than re-seeding on every startup.
- Prefer Aspire's `AddNpgsqlDbContext<T>("name")` over manual `DbContext` configuration because it automatically wires connection strings from service discovery, configures health checks, and adds OpenTelemetry instrumentation.
- Use `WithExternalHttpEndpoints()` only on services that need external access (API gateways, frontend); internal services should only be reachable through service discovery.
- Reference services by name (`https+http://catalog-api`) in `HttpClient.BaseAddress` and let Aspire's service discovery resolve the actual endpoint, rather than hardcoding `localhost:PORT` URLs.
- Use `builder.AddParameter("key", secret: true)` for sensitive values (API keys, passwords) instead of hardcoding them; Aspire prompts for these during `azd up` and stores them securely.
- Add `WithManagementPlugin()`, `WithPgAdmin()`, or `WithRedisCommander()` during development to get admin UIs for infrastructure resources; these are automatically excluded in production deployments.
- Run `azd init` and `azd up` for deploying to Azure Container Apps rather than manually building Docker images and configuring infrastructure.
- Open the Aspire Dashboard (automatically launched during `dotnet run` on the AppHost) to inspect distributed traces, structured logs, and metrics across all services during local development.
