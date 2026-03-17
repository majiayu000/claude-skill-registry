---
name: extensions-service-discovery
description: |
  Use when resolving service endpoints dynamically with Microsoft.Extensions.ServiceDiscovery. Covers configuration-based, DNS-based, and Aspire-integrated service resolution for HttpClient, endpoint selection strategies, and health-aware routing.
  USE FOR: resolving service URLs from configuration or DNS instead of hardcoding, service discovery in .NET Aspire applications, load-balanced HttpClient endpoint resolution, adding service discovery to IHttpClientFactory, health-aware service routing
  DO NOT USE FOR: Dapr service invocation (use dapr), direct DNS resolution without HttpClient (use System.Net.Dns), API gateway routing (use YARP or Azure API Management), Kubernetes service mesh features (use Istio or Linkerd)
license: MIT
metadata:
  displayName: "Service Discovery"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "Service Discovery in .NET Documentation"
    url: "https://learn.microsoft.com/dotnet/core/extensions/service-discovery"
  - title: "Microsoft.Extensions.ServiceDiscovery NuGet Package"
    url: "https://www.nuget.org/packages/Microsoft.Extensions.ServiceDiscovery"
  - title: ".NET Aspire GitHub Repository"
    url: "https://github.com/dotnet/aspire"
---

# Service Discovery

## Overview
Microsoft.Extensions.ServiceDiscovery provides a pluggable service endpoint resolution system for .NET applications. It resolves logical service names (like `https+http://catalog-api`) to actual network endpoints using configuration, DNS, or container orchestration. It integrates directly with `IHttpClientFactory` and is the built-in service discovery mechanism for .NET Aspire, but can also be used standalone in any .NET application.

## NuGet Packages
```bash
dotnet add package Microsoft.Extensions.ServiceDiscovery
dotnet add package Microsoft.Extensions.ServiceDiscovery.Dns      # DNS SRV resolution
dotnet add package Microsoft.Extensions.ServiceDiscovery.Yarp     # YARP integration
```

## Basic Setup
```csharp
var builder = WebApplication.CreateBuilder(args);

// Add service discovery
builder.Services.AddServiceDiscovery();

// Apply to all HttpClient instances by default
builder.Services.ConfigureHttpClientDefaults(http =>
{
    http.AddServiceDiscovery();
});

var app = builder.Build();
app.Run();
```

## Configuration-Based Resolution
Define service endpoints in `appsettings.json`.

```json
{
  "Services": {
    "catalog-api": {
      "https": ["https://catalog1.example.com", "https://catalog2.example.com"],
      "http": ["http://catalog1.example.com:8080"]
    },
    "payment-service": {
      "https": ["https://payments.internal:5001"]
    },
    "identity-server": {
      "default": ["https://identity.example.com"]
    }
  }
}
```

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddServiceDiscovery();

builder.Services.ConfigureHttpClientDefaults(http =>
{
    http.AddServiceDiscovery();
});

// Named HttpClient uses service discovery automatically
builder.Services.AddHttpClient("catalog", client =>
{
    // Resolved from Services:catalog-api in config
    client.BaseAddress = new Uri("https+http://catalog-api");
});

var app = builder.Build();

app.MapGet("/products", async (IHttpClientFactory factory) =>
{
    var client = factory.CreateClient("catalog");
    var products = await client.GetFromJsonAsync<List<Product>>("/api/products");
    return Results.Ok(products);
});
```

## Typed HttpClient with Service Discovery
```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddServiceDiscovery();
builder.Services.ConfigureHttpClientDefaults(http =>
{
    http.AddServiceDiscovery();
});

builder.Services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = new Uri("https+http://catalog-api");
});

builder.Services.AddHttpClient<PaymentClient>(client =>
{
    client.BaseAddress = new Uri("https://payment-service");
});

var app = builder.Build();

app.MapPost("/orders", async (Order order, CatalogClient catalog, PaymentClient payments) =>
{
    var product = await catalog.GetProductAsync(order.ProductId);
    var result = await payments.ProcessAsync(order.Total);
    return Results.Created($"/orders/{order.Id}", order);
});

app.Run();

public class CatalogClient(HttpClient httpClient)
{
    public async Task<Product?> GetProductAsync(string productId) =>
        await httpClient.GetFromJsonAsync<Product>($"/api/products/{productId}");

    public async Task<List<Product>> SearchAsync(string query) =>
        await httpClient.GetFromJsonAsync<List<Product>>(
            $"/api/products?q={Uri.EscapeDataString(query)}") ?? [];
}

public class PaymentClient(HttpClient httpClient)
{
    public async Task<PaymentResult> ProcessAsync(decimal amount) =>
        await httpClient.PostAsJsonAsync("/api/payments", new { amount })
            .ContinueWith(t => t.Result.Content.ReadFromJsonAsync<PaymentResult>())
            .Unwrap() ?? throw new InvalidOperationException("Payment failed");
}
```

## URI Scheme Conventions

| Scheme | Behavior |
|--------|----------|
| `https://service-name` | Resolves HTTPS endpoints only |
| `http://service-name` | Resolves HTTP endpoints only |
| `https+http://service-name` | Prefers HTTPS, falls back to HTTP |
| `http+https://service-name` | Prefers HTTP, falls back to HTTPS |

```csharp
// Prefer HTTPS, fall back to HTTP
builder.Services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = new Uri("https+http://catalog-api");
});

// HTTPS only (fails if no HTTPS endpoint available)
builder.Services.AddHttpClient<SecureClient>(client =>
{
    client.BaseAddress = new Uri("https://secure-service");
});
```

## DNS-Based Resolution
Resolve service endpoints using DNS SRV and A/AAAA records.

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddServiceDiscovery()
    .AddDnsSrvServiceEndpointProvider();  // Add DNS SRV resolution

builder.Services.ConfigureHttpClientDefaults(http =>
{
    http.AddServiceDiscovery();
});

// DNS SRV record: _http._tcp.catalog-api.example.com -> catalog1:8080, catalog2:8080
builder.Services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = new Uri("http://catalog-api.example.com");
});
```

## Per-Client Service Discovery
Apply service discovery selectively rather than globally.

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddServiceDiscovery();

// Only this client uses service discovery
builder.Services.AddHttpClient<InternalServiceClient>(client =>
{
    client.BaseAddress = new Uri("https+http://internal-api");
})
.AddServiceDiscovery();

// This client uses a static URL (no service discovery)
builder.Services.AddHttpClient<ExternalApiClient>(client =>
{
    client.BaseAddress = new Uri("https://api.external-vendor.com");
});
```

## Integration with Resilience
Combine service discovery with `Microsoft.Extensions.Http.Resilience` for retries, circuit breakers, and timeouts.

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddServiceDiscovery();

builder.Services.AddHttpClient<CatalogClient>(client =>
{
    client.BaseAddress = new Uri("https+http://catalog-api");
})
.AddServiceDiscovery()
.AddStandardResilienceHandler(options =>
{
    options.Retry.MaxRetryAttempts = 3;
    options.Retry.Delay = TimeSpan.FromMilliseconds(500);
    options.CircuitBreaker.SamplingDuration = TimeSpan.FromSeconds(10);
    options.AttemptTimeout.Timeout = TimeSpan.FromSeconds(5);
    options.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(30);
});
```

## Aspire Integration
In .NET Aspire, service discovery is configured automatically by the AppHost.

```csharp
// AppHost/Program.cs
var builder = DistributedApplication.CreateBuilder(args);

var catalogApi = builder.AddProject<Projects.CatalogApi>("catalog-api");

builder.AddProject<Projects.WebFrontend>("web")
    .WithReference(catalogApi);  // Automatically configures service discovery

// CatalogApi/Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();  // Includes AddServiceDiscovery()

// WebFrontend/Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.AddServiceDefaults();

builder.Services.AddHttpClient<CatalogClient>(client =>
{
    // "catalog-api" is resolved automatically from Aspire's service discovery
    client.BaseAddress = new Uri("https+http://catalog-api");
});
```

## Environment Variable Configuration
Service discovery can also read endpoints from environment variables (set by Aspire or container orchestrators).

```bash
# Environment variable format
services__catalog-api__https__0=https://catalog1.example.com
services__catalog-api__https__1=https://catalog2.example.com
services__catalog-api__http__0=http://catalog1.example.com:8080
```

## Best Practices
- Use `https+http://` as the default URI scheme for internal services to prefer HTTPS when available while gracefully falling back to HTTP during local development where TLS certificates may not be configured.
- Apply `AddServiceDiscovery()` to `ConfigureHttpClientDefaults` to enable service discovery globally rather than adding it to each client individually, reducing boilerplate and preventing missed clients.
- Define service endpoints in `appsettings.json` under the `Services` key for development and testing environments, and use environment variables (`services__name__scheme__index`) for production deployments set by orchestrators.
- Combine service discovery with `AddStandardResilienceHandler()` from `Microsoft.Extensions.Http.Resilience` to get retries, circuit breakers, and timeouts on resolved endpoints rather than implementing retry logic manually.
- Use typed `HttpClient` classes (e.g., `CatalogClient`, `PaymentClient`) with constructor-injected `HttpClient` rather than `IHttpClientFactory.CreateClient("name")` to get compile-time safety and encapsulated API logic.
- Use `AddDnsSrvServiceEndpointProvider()` for Kubernetes or Consul environments where services are registered via DNS SRV records rather than duplicating endpoints in configuration files.
- Separate internal services (using service discovery) from external APIs (using static URLs) by applying `AddServiceDiscovery()` per-client rather than globally when your application calls both internal and third-party APIs.
- Let .NET Aspire handle service discovery configuration automatically via `WithReference()` in the AppHost rather than manually configuring endpoints in `appsettings.json` for Aspire-orchestrated applications.
- Keep service names consistent across AppHost references, configuration keys, and `HttpClient.BaseAddress` URIs (e.g., always use `catalog-api`, not `CatalogAPI` or `catalog_api`) to prevent resolution failures.
- Test service discovery in isolation by mocking `IServiceEndpointProvider` or overriding configuration values in test fixtures to point at test servers, rather than relying on real service infrastructure during unit tests.
