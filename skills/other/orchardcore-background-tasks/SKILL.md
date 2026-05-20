---
name: orchardcore-background-tasks
description: Skill for creating background tasks and scheduled jobs in Orchard Core. Covers IBackgroundTask implementation, scheduling configuration, and background service patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Background Tasks - Prompt Templates

## Create Background Tasks

You are an Orchard Core expert. Generate background task implementations for Orchard Core.

### Guidelines

- Background tasks implement `IBackgroundTask` and run on a schedule.
- Tasks are registered in `Startup.cs` using `AddBackgroundTask<T>()`.
- The schedule is configured using `SetSchedule()` with cron expressions or `TimeSpan`.
- Background tasks run in the context of the tenant's service scope.
- Use `ILogger` for logging task execution and errors.
- Tasks should be idempotent and handle concurrent execution gracefully.
- Always seal classes.

### Basic Background Task

```csharp
using Microsoft.Extensions.Logging;
using OrchardCore.BackgroundTasks;

[BackgroundTask(
    Schedule = "*/15 * * * *",
    Description = "{{TaskDescription}}")]
public sealed class {{TaskName}} : IBackgroundTask
{
    private readonly ILogger<{{TaskName}}> _logger;

    public {{TaskName}}(ILogger<{{TaskName}}> logger)
    {
        _logger = logger;
    }

    public Task DoWorkAsync(IServiceProvider serviceProvider, CancellationToken cancellationToken)
    {
        _logger.LogInformation("Running {{TaskName}}...");

        // Task logic here

        return Task.CompletedTask;
    }
}
```

### Background Task with Service Dependencies

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using OrchardCore.BackgroundTasks;
using OrchardCore.ContentManagement;

[BackgroundTask(
    Schedule = "0 */6 * * *",
    Description = "{{TaskDescription}}")]
public sealed class {{TaskName}} : IBackgroundTask
{
    private readonly ILogger<{{TaskName}}> _logger;

    public {{TaskName}}(ILogger<{{TaskName}}> logger)
    {
        _logger = logger;
    }

    public async Task DoWorkAsync(IServiceProvider serviceProvider, CancellationToken cancellationToken)
    {
        // Resolve services from the service provider
        var contentManager = serviceProvider.GetRequiredService<IContentManager>();
        var session = serviceProvider.GetRequiredService<YesSql.ISession>();

        _logger.LogInformation("Running {{TaskName}}...");

        // Example: query and process content items
        var items = await session
            .Query<ContentItem, ContentItemIndex>(x =>
                x.ContentType == "{{ContentType}}" && x.Published)
            .ListAsync();

        foreach (var item in items)
        {
            if (cancellationToken.IsCancellationRequested)
            {
                break;
            }

            // Process item
        }

        _logger.LogInformation("{{TaskName}} completed. Processed {Count} items.", items.Count());
    }
}
```

### Registering a Background Task

```csharp
using OrchardCore.BackgroundTasks;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddBackgroundTask<{{TaskName}}>();
    }
}
```

### Enabling Background Tasks Feature

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.BackgroundTasks"
      ],
      "disable": []
    }
  ]
}
```

### Common Cron Schedule Expressions

- `* * * * *` — Every minute.
- `*/5 * * * *` — Every 5 minutes.
- `*/15 * * * *` — Every 15 minutes.
- `0 * * * *` — Every hour.
- `0 */6 * * *` — Every 6 hours.
- `0 0 * * *` — Daily at midnight.
- `0 0 * * 0` — Weekly on Sunday at midnight.
- `0 0 1 * *` — Monthly on the 1st at midnight.
