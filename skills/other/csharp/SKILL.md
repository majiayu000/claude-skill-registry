---
name: csharp
description: |
  Writes C# code following VanDaemon conventions and clean architecture patterns
  Use when: Creating services, entities, controllers, or plugins in the VanDaemon codebase
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# C# Skill

Generates C# code following VanDaemon's clean architecture with nullable reference types, async patterns, and structured logging. All services are singletons with constructor injection. Entities live in Core, services in Application, controllers in Api.

## Quick Start

### Creating a Service

```csharp
// Application/Interfaces/IFuelService.cs
public interface IFuelService
{
    Task<IReadOnlyList<FuelReading>> GetAllReadingsAsync(CancellationToken cancellationToken = default);
    Task<FuelReading?> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
}

// Application/Services/FuelService.cs
public class FuelService : IFuelService
{
    private readonly ILogger<FuelService> _logger;
    private readonly JsonFileStore _fileStore;

    public FuelService(ILogger<FuelService> logger, JsonFileStore fileStore)
    {
        _logger = logger;
        _fileStore = fileStore;
    }

    public async Task<IReadOnlyList<FuelReading>> GetAllReadingsAsync(CancellationToken cancellationToken = default)
    {
        var readings = await _fileStore.LoadAsync<List<FuelReading>>("fuel.json", cancellationToken);
        return readings?.AsReadOnly() ?? new List<FuelReading>().AsReadOnly();
    }
}
```

### Creating an Entity

```csharp
// Core/Entities/FuelReading.cs
public class FuelReading
{
    public Guid Id { get; set; }
    public double Level { get; set; }
    public DateTime Timestamp { get; set; }
    public bool IsActive { get; set; } = true;  // Soft delete pattern
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Nullable types | All reference types nullable-aware | `Tank?`, `string?` |
| CancellationToken | Required on all async methods | `Task<T> MethodAsync(CancellationToken ct = default)` |
| Soft deletes | Never remove, set `IsActive = false` | `entity.IsActive = false;` |
| Structured logging | Named placeholders | `_logger.LogInformation("Tank {TankId} at {Level}%", id, level)` |
| Private fields | Underscore prefix | `private readonly ILogger _logger;` |

## Common Patterns

### Plugin Implementation

**When:** Adding hardware integration

```csharp
public class MyPlugin : ISensorPlugin, IDisposable
{
    private readonly ILogger<MyPlugin> _logger;
    private readonly Dictionary<string, double> _values = new();
    private bool _disposed;

    public string Name => "My Plugin";
    public string Version => "1.0.0";

    public async Task InitializeAsync(Dictionary<string, object> config, CancellationToken ct = default)
    {
        _logger.LogInformation("Initializing {PluginName}", Name);
        // Setup from config dictionary
    }

    public Task<double> ReadValueAsync(string sensorId, CancellationToken ct = default)
        => Task.FromResult(_values.GetValueOrDefault(sensorId, 0.0));

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;
        // Cleanup
    }
}
```

### SignalR Broadcast

**When:** Pushing real-time updates to clients

```csharp
await _hubContext.Clients.Group("tanks").SendAsync(
    "TankLevelUpdated", tankId, currentLevel, tankName, cancellationToken);
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **dotnet** skill for build commands and project structure
- See the **aspnet-core** skill for controllers and middleware
- See the **xunit** skill for testing patterns
- See the **serilog** skill for logging configuration