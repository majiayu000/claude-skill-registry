---
name: aspnet-core
description: |
  Builds REST APIs, SignalR hubs, and ASP.NET Core Web API applications.
  Use when: Creating controllers, configuring middleware, setting up dependency injection, implementing background services, or working with the API layer.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# ASP.NET Core Skill

ASP.NET Core Web API patterns for VanDaemon's backend. This project uses .NET 10 with thin controllers, singleton services, SignalR for real-time updates, and JSON file persistence. Controllers delegate to application services; business logic never lives in controllers.

## Quick Start

### Minimal Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class TanksController : ControllerBase
{
    private readonly ITankService _tankService;

    public TanksController(ITankService tankService)
    {
        _tankService = tankService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<Tank>>> GetAll(CancellationToken ct)
    {
        var tanks = await _tankService.GetAllTanksAsync(ct);
        return Ok(tanks);
    }

    [HttpPost("{id}/state")]
    public async Task<IActionResult> SetState(Guid id, [FromBody] object state, CancellationToken ct)
    {
        await _tankService.UpdateTankAsync(id, state, ct);
        return NoContent();
    }
}
```

### Service Registration

```csharp
// Program.cs - Register as singletons (VanDaemon pattern)
builder.Services.AddSingleton<ITankService, TankService>();
builder.Services.AddSingleton<IControlService, ControlService>();
builder.Services.AddSingleton<JsonFileStore>();

// SignalR
builder.Services.AddSignalR();

// After app.Build()
app.MapHub<TelemetryHub>("/hubs/telemetry");
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Thin Controllers | Delegate to services immediately | `return Ok(await _service.GetAsync(ct))` |
| CancellationToken | Accept in all async endpoints | `Task<T> Method(CancellationToken ct)` |
| ActionResult<T> | Return type for typed responses | `ActionResult<List<Tank>>` |
| Background Services | Inherit `BackgroundService` | `TelemetryBackgroundService` |
| Health Checks | Map `/health` endpoint | `app.MapGet("/health", ...)` |

## Common Patterns

### Background Service with Scope

```csharp
public class TelemetryBackgroundService : BackgroundService
{
    private readonly IServiceProvider _provider;

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            using var scope = _provider.CreateScope();
            var tankService = scope.ServiceProvider.GetRequiredService<ITankService>();
            await tankService.RefreshAllAsync(ct);
            await Task.Delay(TimeSpan.FromSeconds(5), ct);
        }
    }
}
```

### Health Endpoint

```csharp
app.MapGet("/health", () => Results.Ok(new
{
    status = "healthy",
    timestamp = DateTime.UtcNow
}));
```

## WARNING: Common Anti-Patterns

See [patterns](references/patterns.md) for detailed anti-pattern documentation including:
- Business logic in controllers
- Missing CancellationToken
- Blocking calls in async context
- Incorrect service lifetimes

## See Also

- [patterns](references/patterns.md) - Controller patterns, DI, anti-patterns
- [workflows](references/workflows.md) - Adding endpoints, services, SignalR

## Related Skills

- See the **csharp** skill for language patterns and async/await
- See the **signalr** skill for real-time hub implementation
- See the **serilog** skill for structured logging
- See the **docker** skill for containerized deployment
- See the **xunit** skill for controller testing