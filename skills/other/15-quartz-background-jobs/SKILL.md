---
name: quartz-background-jobs
description: "Generates scheduled background jobs using Quartz.NET. Includes job definitions, triggers, cron scheduling, dependency injection, and persistent job store configuration."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Quartz, Quartz.Extensions.Hosting
---

# Background Job Generator (Quartz)

## Overview

Quartz.NET is a full-featured job scheduling library:

- **Job scheduling** - Run tasks at specific times or intervals
- **Cron expressions** - Complex scheduling patterns
- **Persistence** - Jobs survive application restarts
- **Dependency injection** - Full DI support
- **Clustering** - Distributed job execution

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `IJob` | Job interface to implement |
| `IConfigureOptions<QuartzOptions>` | Job registration |
| `JobKey` | Unique job identifier |
| `TriggerBuilder` | Defines when job runs |
| `CronScheduleBuilder` | Cron-based scheduling |
| `SimpleScheduleBuilder` | Interval-based scheduling |

---

## Job Structure

```
/Infrastructure/
├── BackgroundJobs/
│   ├── {JobName}Job.cs
│   ├── {JobName}JobSetup.cs
│   └── ...
└── DependencyInjection.cs
```

---

## Template: Simple Interval Job

```csharp
// src/{name}.infrastructure/BackgroundJobs/ProcessPendingOrdersJob.cs
using Microsoft.Extensions.Logging;
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

/// <summary>
/// Processes pending orders every 5 minutes
/// </summary>
[DisallowConcurrentExecution]  // Prevent overlapping executions
public sealed class ProcessPendingOrdersJob : IJob
{
    private readonly IOrderRepository _orderRepository;
    private readonly IOrderProcessor _orderProcessor;
    private readonly ILogger<ProcessPendingOrdersJob> _logger;

    public ProcessPendingOrdersJob(
        IOrderRepository orderRepository,
        IOrderProcessor orderProcessor,
        ILogger<ProcessPendingOrdersJob> logger)
    {
        _orderRepository = orderRepository;
        _orderProcessor = orderProcessor;
        _logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        _logger.LogInformation("Starting pending orders processing...");

        try
        {
            var pendingOrders = await _orderRepository
                .GetPendingOrdersAsync(context.CancellationToken);

            _logger.LogInformation(
                "Found {Count} pending orders to process",
                pendingOrders.Count);

            foreach (var order in pendingOrders)
            {
                try
                {
                    await _orderProcessor.ProcessAsync(order, context.CancellationToken);
                    
                    _logger.LogInformation(
                        "Processed order {OrderId}",
                        order.Id);
                }
                catch (Exception ex)
                {
                    _logger.LogError(
                        ex,
                        "Failed to process order {OrderId}",
                        order.Id);
                }
            }

            _logger.LogInformation("Completed pending orders processing");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error in pending orders processing job");
            throw;  // Quartz will handle retry based on configuration
        }
    }
}
```

---

## Template: Job Setup (IConfigureOptions)

```csharp
// src/{name}.infrastructure/BackgroundJobs/ProcessPendingOrdersJobSetup.cs
using Microsoft.Extensions.Options;
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

internal sealed class ProcessPendingOrdersJobSetup 
    : IConfigureOptions<QuartzOptions>
{
    public void Configure(QuartzOptions options)
    {
        var jobKey = JobKey.Create(nameof(ProcessPendingOrdersJob));

        options
            .AddJob<ProcessPendingOrdersJob>(jobBuilder =>
                jobBuilder
                    .WithIdentity(jobKey)
                    .WithDescription("Processes pending orders"))
            .AddTrigger(triggerBuilder =>
                triggerBuilder
                    .ForJob(jobKey)
                    .WithIdentity($"{nameof(ProcessPendingOrdersJob)}-trigger")
                    .WithSimpleSchedule(schedule =>
                        schedule
                            .WithIntervalInMinutes(5)
                            .RepeatForever())
                    .StartNow());
    }
}
```

---

## Template: Cron Scheduled Job

```csharp
// src/{name}.infrastructure/BackgroundJobs/DailyReportJob.cs
using Microsoft.Extensions.Logging;
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

/// <summary>
/// Generates daily reports at 6:00 AM every day
/// </summary>
[DisallowConcurrentExecution]
public sealed class DailyReportJob : IJob
{
    private readonly IReportService _reportService;
    private readonly IEmailService _emailService;
    private readonly ILogger<DailyReportJob> _logger;

    public DailyReportJob(
        IReportService reportService,
        IEmailService emailService,
        ILogger<DailyReportJob> logger)
    {
        _reportService = reportService;
        _emailService = emailService;
        _logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        _logger.LogInformation("Starting daily report generation...");

        var reportDate = DateTime.UtcNow.Date.AddDays(-1);

        var report = await _reportService.GenerateDailyReportAsync(
            reportDate,
            context.CancellationToken);

        await _emailService.SendReportAsync(
            report,
            context.CancellationToken);

        _logger.LogInformation(
            "Daily report for {Date} sent successfully",
            reportDate.ToShortDateString());
    }
}
```

```csharp
// src/{name}.infrastructure/BackgroundJobs/DailyReportJobSetup.cs
using Microsoft.Extensions.Options;
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

internal sealed class DailyReportJobSetup : IConfigureOptions<QuartzOptions>
{
    public void Configure(QuartzOptions options)
    {
        var jobKey = JobKey.Create(nameof(DailyReportJob));

        options
            .AddJob<DailyReportJob>(jobBuilder =>
                jobBuilder
                    .WithIdentity(jobKey)
                    .WithDescription("Daily report generation"))
            .AddTrigger(triggerBuilder =>
                triggerBuilder
                    .ForJob(jobKey)
                    .WithIdentity($"{nameof(DailyReportJob)}-trigger")
                    .WithCronSchedule(
                        "0 0 6 * * ?",  // 6:00 AM every day
                        builder => builder.InTimeZone(TimeZoneInfo.Utc))
                    .WithDescription("Fires at 6:00 AM UTC daily"));
    }
}
```

---

## Cron Expression Reference

| Expression | Description |
|------------|-------------|
| `0 0 * * * ?` | Every hour at minute 0 |
| `0 0/15 * * * ?` | Every 15 minutes |
| `0 0 6 * * ?` | Daily at 6:00 AM |
| `0 0 6 ? * MON-FRI` | Weekdays at 6:00 AM |
| `0 0 0 1 * ?` | First day of month at midnight |
| `0 0 0 L * ?` | Last day of month at midnight |
| `0 0 12 ? * SUN` | Every Sunday at noon |

**Format**: `seconds minutes hours day-of-month month day-of-week [year]`

| Field | Values |
|-------|--------|
| Seconds | 0-59 |
| Minutes | 0-59 |
| Hours | 0-23 |
| Day-of-month | 1-31, L (last), W (weekday) |
| Month | 1-12 or JAN-DEC |
| Day-of-week | 1-7 or SUN-SAT, L (last) |
| Year | Optional, 1970-2099 |

**Special Characters**:
- `*` - All values
- `?` - No specific value (day-of-month/day-of-week)
- `-` - Range (e.g., `MON-FRI`)
- `,` - List (e.g., `MON,WED,FRI`)
- `/` - Increment (e.g., `0/15` = every 15)
- `L` - Last (e.g., last day of month)
- `W` - Nearest weekday
- `#` - Nth day (e.g., `2#3` = third Monday)

---

## Template: Job with Data Map

```csharp
// src/{name}.infrastructure/BackgroundJobs/SendScheduledEmailJob.cs
using Microsoft.Extensions.Logging;
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

/// <summary>
/// Sends a scheduled email using data from JobDataMap
/// </summary>
public sealed class SendScheduledEmailJob : IJob
{
    public const string EmailIdKey = "EmailId";
    public const string RecipientKey = "Recipient";

    private readonly IEmailService _emailService;
    private readonly ILogger<SendScheduledEmailJob> _logger;

    public SendScheduledEmailJob(
        IEmailService emailService,
        ILogger<SendScheduledEmailJob> logger)
    {
        _emailService = emailService;
        _logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        // Get data from job data map
        var dataMap = context.MergedJobDataMap;
        
        var emailId = dataMap.GetGuid(EmailIdKey);
        var recipient = dataMap.GetString(RecipientKey);

        _logger.LogInformation(
            "Sending scheduled email {EmailId} to {Recipient}",
            emailId,
            recipient);

        await _emailService.SendScheduledEmailAsync(
            emailId,
            context.CancellationToken);
    }
}

// Scheduling the job with data
public class EmailScheduler
{
    private readonly ISchedulerFactory _schedulerFactory;

    public async Task ScheduleEmailAsync(
        Guid emailId,
        string recipient,
        DateTime sendAt)
    {
        var scheduler = await _schedulerFactory.GetScheduler();

        var jobKey = new JobKey($"email-{emailId}", "scheduled-emails");

        var job = JobBuilder.Create<SendScheduledEmailJob>()
            .WithIdentity(jobKey)
            .UsingJobData(SendScheduledEmailJob.EmailIdKey, emailId.ToString())
            .UsingJobData(SendScheduledEmailJob.RecipientKey, recipient)
            .Build();

        var trigger = TriggerBuilder.Create()
            .WithIdentity($"email-{emailId}-trigger", "scheduled-emails")
            .StartAt(sendAt)
            .Build();

        await scheduler.ScheduleJob(job, trigger);
    }
}
```

---

## Template: Job with Retry Logic

```csharp
// src/{name}.infrastructure/BackgroundJobs/SyncExternalDataJob.cs
using Microsoft.Extensions.Logging;
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

/// <summary>
/// Syncs data from external API with retry support
/// </summary>
[DisallowConcurrentExecution]
[PersistJobDataAfterExecution]  // Persist data map changes
public sealed class SyncExternalDataJob : IJob
{
    private const int MaxRetries = 3;
    private const string RetryCountKey = "RetryCount";

    private readonly IExternalApiClient _apiClient;
    private readonly IDataSyncService _syncService;
    private readonly ILogger<SyncExternalDataJob> _logger;

    public SyncExternalDataJob(
        IExternalApiClient apiClient,
        IDataSyncService syncService,
        ILogger<SyncExternalDataJob> logger)
    {
        _apiClient = apiClient;
        _syncService = syncService;
        _logger = logger;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        var retryCount = context.MergedJobDataMap.GetInt(RetryCountKey);

        try
        {
            _logger.LogInformation(
                "Starting external data sync (attempt {Attempt})",
                retryCount + 1);

            var data = await _apiClient.FetchDataAsync(context.CancellationToken);
            await _syncService.SyncAsync(data, context.CancellationToken);

            // Reset retry count on success
            context.JobDetail.JobDataMap.Put(RetryCountKey, 0);

            _logger.LogInformation("External data sync completed successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(
                ex,
                "External data sync failed (attempt {Attempt} of {MaxRetries})",
                retryCount + 1,
                MaxRetries);

            if (retryCount < MaxRetries - 1)
            {
                // Increment retry count
                context.JobDetail.JobDataMap.Put(RetryCountKey, retryCount + 1);

                // Throw to trigger Quartz retry
                throw new JobExecutionException(ex, refireImmediately: false);
            }
            else
            {
                // Max retries reached, log and don't retry
                _logger.LogCritical(
                    "External data sync failed after {MaxRetries} attempts. Manual intervention required.",
                    MaxRetries);

                context.JobDetail.JobDataMap.Put(RetryCountKey, 0);
            }
        }
    }
}
```

---

## Template: Quartz Registration

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
using Quartz;
using Microsoft.Extensions.DependencyInjection;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // ... other registrations

        AddBackgroundJobs(services, configuration);

        return services;
    }

    private static void AddBackgroundJobs(
        IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddQuartz(configure =>
        {
            // ═══════════════════════════════════════════════════════════════
            // IN-MEMORY STORE (Development)
            // ═══════════════════════════════════════════════════════════════
            configure.UseInMemoryStore();

            // ═══════════════════════════════════════════════════════════════
            // PERSISTENT STORE (Production - uncomment for production)
            // ═══════════════════════════════════════════════════════════════
            // configure.UsePersistentStore(store =>
            // {
            //     store.UsePostgres(configuration.GetConnectionString("Database")!);
            //     store.UseJsonSerializer();
            //     store.PerformSchemaValidation = true;
            // });

            // ═══════════════════════════════════════════════════════════════
            // CLUSTERING (Multi-instance - uncomment for distributed)
            // ═══════════════════════════════════════════════════════════════
            // configure.UsePersistentStore(store =>
            // {
            //     store.UsePostgres(configuration.GetConnectionString("Database")!);
            //     store.UseJsonSerializer();
            //     store.UseClustering(cluster =>
            //     {
            //         cluster.CheckinMisfireThreshold = TimeSpan.FromSeconds(20);
            //         cluster.CheckinInterval = TimeSpan.FromSeconds(10);
            //     });
            // });
        });

        // Register hosted service
        services.AddQuartzHostedService(options =>
        {
            options.WaitForJobsToComplete = true;
            options.AwaitApplicationStarted = true;
        });

        // Register job setups
        services.ConfigureOptions<ProcessPendingOrdersJobSetup>();
        services.ConfigureOptions<DailyReportJobSetup>();
        services.ConfigureOptions<SyncExternalDataJobSetup>();
    }
}
```

---

## Template: Job Scheduler Service

```csharp
// src/{name}.infrastructure/BackgroundJobs/JobSchedulerService.cs
using Quartz;

namespace {name}.infrastructure.backgroundjobs;

/// <summary>
/// Service for dynamically scheduling jobs at runtime
/// </summary>
public interface IJobSchedulerService
{
    Task ScheduleJobAsync<TJob>(DateTime runAt, JobDataMap? data = null) 
        where TJob : IJob;
    Task ScheduleJobAsync<TJob>(TimeSpan delay, JobDataMap? data = null) 
        where TJob : IJob;
    Task CancelJobAsync(string jobName, string groupName);
    Task<bool> IsJobScheduledAsync(string jobName, string groupName);
}

internal sealed class JobSchedulerService : IJobSchedulerService
{
    private readonly ISchedulerFactory _schedulerFactory;

    public JobSchedulerService(ISchedulerFactory schedulerFactory)
    {
        _schedulerFactory = schedulerFactory;
    }

    public async Task ScheduleJobAsync<TJob>(DateTime runAt, JobDataMap? data = null) 
        where TJob : IJob
    {
        var scheduler = await _schedulerFactory.GetScheduler();
        var jobName = $"{typeof(TJob).Name}-{Guid.NewGuid()}";

        var jobBuilder = JobBuilder.Create<TJob>()
            .WithIdentity(jobName, "dynamic-jobs");

        if (data is not null)
        {
            jobBuilder.UsingJobData(data);
        }

        var job = jobBuilder.Build();

        var trigger = TriggerBuilder.Create()
            .WithIdentity($"{jobName}-trigger", "dynamic-jobs")
            .StartAt(runAt)
            .Build();

        await scheduler.ScheduleJob(job, trigger);
    }

    public async Task ScheduleJobAsync<TJob>(TimeSpan delay, JobDataMap? data = null) 
        where TJob : IJob
    {
        await ScheduleJobAsync<TJob>(DateTime.UtcNow.Add(delay), data);
    }

    public async Task CancelJobAsync(string jobName, string groupName)
    {
        var scheduler = await _schedulerFactory.GetScheduler();
        await scheduler.DeleteJob(new JobKey(jobName, groupName));
    }

    public async Task<bool> IsJobScheduledAsync(string jobName, string groupName)
    {
        var scheduler = await _schedulerFactory.GetScheduler();
        return await scheduler.CheckExists(new JobKey(jobName, groupName));
    }
}
```

---

## Critical Rules

1. **Use [DisallowConcurrentExecution]** - Prevent overlapping runs
2. **Handle exceptions properly** - Log and decide retry strategy
3. **Use CancellationToken** - From `context.CancellationToken`
4. **Keep jobs focused** - One responsibility per job
5. **Use persistent store for production** - Jobs survive restarts
6. **Time zones matter** - Specify timezone for cron triggers
7. **Monitor job execution** - Log start/end and duration
8. **Don't block the thread** - Use async/await
9. **Inject scoped services** - Each execution gets new scope
10. **Test job logic separately** - Extract logic to testable services

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Long-running synchronous code
public Task Execute(IJobExecutionContext context)
{
    Thread.Sleep(60000);  // Don't block!
    return Task.CompletedTask;
}

// ✅ CORRECT: Async operations
public async Task Execute(IJobExecutionContext context)
{
    await Task.Delay(60000, context.CancellationToken);
}

// ❌ WRONG: Swallowing exceptions silently
public async Task Execute(IJobExecutionContext context)
{
    try { await DoWork(); }
    catch { }  // Silent failure, no logging!
}

// ✅ CORRECT: Log and handle exceptions
public async Task Execute(IJobExecutionContext context)
{
    try { await DoWork(); }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Job failed");
        throw;  // Let Quartz handle retry
    }
}

// ❌ WRONG: Ignoring cancellation
public async Task Execute(IJobExecutionContext context)
{
    foreach (var item in items)
    {
        await ProcessItem(item);  // Ignores shutdown signal
    }
}

// ✅ CORRECT: Respect cancellation
public async Task Execute(IJobExecutionContext context)
{
    foreach (var item in items)
    {
        context.CancellationToken.ThrowIfCancellationRequested();
        await ProcessItem(item, context.CancellationToken);
    }
}
```

---

## Related Skills

- `outbox-pattern` - Outbox processor job
- `email-service` - Scheduled email jobs
- `dotnet-clean-architecture` - Infrastructure layer setup
