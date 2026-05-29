---
name: serilog
description: |
  Implements structured logging and configures Serilog sinks for VanDaemon.
  Use when: Adding logging to services, configuring log sinks, debugging with structured data, setting up log enrichment.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Serilog Skill

VanDaemon uses Serilog 8.x for structured logging with console and file sinks. Logs use semantic message templates with named properties for queryability. The API layer configures Serilog in `Program.cs` with rolling file output to `logs/vandaemon-{Date}.txt`.

## Quick Start

### Basic Structured Logging

```csharp
// Inject ILogger<T> via constructor
private readonly ILogger<TankService> _logger;

public TankService(ILogger<TankService> logger)
{
    _logger = logger;
}

// Use semantic message templates - property names in braces
_logger.LogInformation("Tank {TankId} updated to {Level}%", tankId, level);
_logger.LogWarning("Tank {TankName} below threshold: {CurrentLevel}% < {Threshold}%", 
    tank.Name, tank.CurrentLevel, tank.AlertLevel);
```

### Exception Logging

```csharp
try
{
    await plugin.SetStateAsync(controlId, state, ct);
}
catch (Exception ex)
{
    // Exception as FIRST parameter, then message template
    _logger.LogError(ex, "Failed to set state for control {ControlId}", controlId);
    throw;
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Message Template | Named placeholders for structured data | `"Processing {TankId}"` |
| Log Level | Severity filtering | `LogInformation`, `LogWarning`, `LogError` |
| Enrichment | Automatic context properties | `Enrich.FromLogContext()` |
| Sink | Output destination | Console, File, Seq |

## Common Patterns

### Service Layer Logging

**When:** Logging business operations with context

```csharp
public async Task<Tank> UpdateTankAsync(Tank tank, CancellationToken ct)
{
    _logger.LogDebug("Updating tank {TankId}: {TankName}", tank.Id, tank.Name);
    
    // Business logic...
    
    _logger.LogInformation("Tank {TankId} saved successfully", tank.Id);
    return tank;
}
```

### Plugin Lifecycle Logging

**When:** Tracking plugin initialization and disposal

```csharp
public async Task InitializeAsync(Dictionary<string, object> config, CancellationToken ct)
{
    _logger.LogInformation("Initializing {PluginName} v{Version}", Name, Version);
    
    if (!config.TryGetValue("MqttBroker", out var broker))
    {
        _logger.LogWarning("{PluginName} missing MqttBroker config, using default", Name);
    }
}
```

## See Also

- [patterns](references/patterns.md) - Structured logging patterns and enrichment
- [workflows](references/workflows.md) - Configuration and debugging workflows

## Related Skills

- See the **aspnet-core** skill for middleware logging configuration
- See the **dotnet** skill for DI registration patterns
- See the **docker** skill for viewing container logs