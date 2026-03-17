---
description: Create a new .NET Aspire worker project with Kafka, RavenDB, and MinIO integration (project)
---
# Add Aspire Worker Project Skill

Create a new .NET Aspire worker project with messaging, database, and storage integration for NovaTune.

## Project Context

- Workers location: `src/NovaTuneApp/NovaTuneApp.Workers.{Name}/`
- AppHost: `src/NovaTuneApp/NovaTuneApp.AppHost/`
- Solution: `src/NovaTuneApp/NovaTuneApp.sln`
- Naming convention: `NovaTuneApp.Workers.{PurposeName}`

## Steps

### 1. Create Project Directory

```bash
mkdir -p src/NovaTuneApp/NovaTuneApp.Workers.Lifecycle
```

### 2. Create Project File

Location: `src/NovaTuneApp/NovaTuneApp.Workers.Lifecycle/NovaTuneApp.Workers.Lifecycle.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk.Worker">

    <PropertyGroup>
        <TargetFramework>net9.0</TargetFramework>
        <Nullable>enable</Nullable>
        <ImplicitUsings>enable</ImplicitUsings>
        <UserSecretsId>dotnet-NovaTuneApp.Workers.Lifecycle</UserSecretsId>
    </PropertyGroup>

    <ItemGroup>
        <ProjectReference Include="..\NovaTuneApp.ServiceDefaults\NovaTuneApp.ServiceDefaults.csproj" />
        <ProjectReference Include="..\NovaTuneApp.ApiService\NovaTuneApp.ApiService.csproj" />
    </ItemGroup>

    <ItemGroup>
        <!-- KafkaFlow for Kafka/Redpanda messaging -->
        <PackageReference Include="KafkaFlow" Version="3.1.0" />
        <PackageReference Include="KafkaFlow.Microsoft.DependencyInjection" Version="3.1.0" />
        <PackageReference Include="KafkaFlow.Serializer.JsonCore" Version="3.1.0" />
        <PackageReference Include="KafkaFlow.Admin" Version="3.1.0" />

        <!-- RavenDB -->
        <PackageReference Include="RavenDB.Client" Version="7.0.2" />

        <!-- MinIO -->
        <PackageReference Include="Minio" Version="6.0.3" />

        <!-- Health Checks -->
        <PackageReference Include="AspNetCore.HealthChecks.Kafka" Version="9.0.0" />
        <PackageReference Include="AspNetCore.HealthChecks.RavenDB" Version="9.0.0" />

        <!-- Serilog -->
        <PackageReference Include="Serilog.AspNetCore" Version="9.0.0" />
        <PackageReference Include="Serilog.Enrichers.Environment" Version="3.0.1" />
        <PackageReference Include="Serilog.Formatting.Compact" Version="3.0.0" />
    </ItemGroup>

</Project>
```

### 3. Create Program.cs

Location: `src/NovaTuneApp/NovaTuneApp.Workers.Lifecycle/Program.cs`

```csharp
using Confluent.Kafka;
using KafkaFlow;
using KafkaFlow.Serializer;
using Microsoft.Extensions.Options;
using Minio;
using NovaTuneApp.ApiService.Infrastructure.Configuration;
using NovaTuneApp.Workers.Lifecycle.Handlers;
using NovaTuneApp.Workers.Lifecycle.Services;
using Raven.Client.Documents;
using Serilog;
using Serilog.Events;
using Serilog.Formatting.Compact;

// Bootstrap logging
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .WriteTo.Console(new RenderedCompactJsonFormatter())
    .CreateBootstrapLogger();

try
{
    var builder = Host.CreateApplicationBuilder(args);

    // Add service defaults (OpenTelemetry, health checks, etc.)
    builder.AddServiceDefaults();

    // Serilog
    builder.Services.AddSerilog((services, configuration) => configuration
        .ReadFrom.Configuration(builder.Configuration)
        .ReadFrom.Services(services)
        .MinimumLevel.Information()
        .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
        .MinimumLevel.Override("KafkaFlow", LogEventLevel.Information)
        .Enrich.FromLogContext()
        .Enrich.WithEnvironmentName()
        .Enrich.WithMachineName()
        .WriteTo.Console(new RenderedCompactJsonFormatter()));

    // Configuration
    builder.Services.Configure<NovaTuneOptions>(
        builder.Configuration.GetSection(NovaTuneOptions.SectionName));
    builder.Services.Configure<LifecycleOptions>(
        builder.Configuration.GetSection(LifecycleOptions.SectionName));

    var topicPrefix = builder.Configuration["NovaTune:TopicPrefix"] ?? "dev";
    var bootstrapServers = builder.Configuration.GetConnectionString("messaging")
        ?? "localhost:9092";

    // RavenDB
    var ravenConnectionString = builder.Configuration.GetConnectionString("novatune");
    string ravenDbUrl;
    string ravenDbDatabase;

    if (ravenConnectionString != null && ravenConnectionString.Contains(';'))
    {
        var parts = ravenConnectionString.Split(';')
            .Select(p => p.Split('=', 2))
            .Where(p => p.Length == 2)
            .ToDictionary(p => p[0], p => p[1]);

        ravenDbUrl = parts.GetValueOrDefault("URL") ?? "http://localhost:8080";
        ravenDbDatabase = parts.GetValueOrDefault("Database") ?? "NovaTune";
    }
    else
    {
        ravenDbUrl = ravenConnectionString ?? "http://localhost:8080";
        ravenDbDatabase = builder.Configuration["RavenDb:Database"] ?? "NovaTune";
    }

    builder.Services.AddSingleton<IDocumentStore>(sp =>
    {
        var store = new DocumentStore
        {
            Urls = [ravenDbUrl],
            Database = ravenDbDatabase
        };
        store.Initialize();
        return store;
    });

    // MinIO
    var minioEndpoint = builder.Configuration.GetConnectionString("storage")
        ?? "http://localhost:9000";
    var minioAccessKey = builder.Configuration["MinIO:AccessKey"] ?? "minioadmin";
    var minioSecretKey = builder.Configuration["MinIO:SecretKey"] ?? "minioadmin";
    var minioHost = minioEndpoint.Replace("http://", "").Replace("https://", "");
    var useSSL = minioEndpoint.StartsWith("https://");

    builder.Services.AddSingleton<IMinioClient>(_ =>
        new MinioClient()
            .WithEndpoint(minioHost)
            .WithCredentials(minioAccessKey, minioSecretKey)
            .WithSSL(useSSL)
            .Build());

    // Health Checks
    builder.Services.AddHealthChecks()
        .AddRavenDB(
            setup => setup.Urls = [ravenDbUrl],
            name: "ravendb",
            timeout: TimeSpan.FromSeconds(5))
        .AddKafka(
            new ProducerConfig { BootstrapServers = bootstrapServers },
            name: "kafka",
            timeout: TimeSpan.FromSeconds(5))
        .AddUrlGroup(
            new Uri($"{minioEndpoint}/minio/health/live"),
            name: "minio",
            timeout: TimeSpan.FromSeconds(5));

    // KafkaFlow Consumer (track deletions)
    builder.Services.AddKafka(kafka => kafka
        .UseMicrosoftLog()
        .AddCluster(cluster =>
        {
            cluster.WithBrokers([bootstrapServers]);

            cluster.AddConsumer(consumer => consumer
                .Topic($"{topicPrefix}-track-deletions")
                .WithGroupId($"{topicPrefix}-lifecycle-worker")
                .WithBufferSize(100)
                .WithWorkersCount(2)
                .WithAutoOffsetReset(KafkaFlow.AutoOffsetReset.Earliest)
                .AddMiddlewares(m => m
                    .AddDeserializer<JsonCoreDeserializer>()
                    .AddTypedHandlers(h => h.AddHandler<TrackDeletedHandler>())
                )
            );
        })
    );

    // Services
    builder.Services.AddTransient<TrackDeletedHandler>();
    builder.Services.AddScoped<IPhysicalDeletionService, PhysicalDeletionService>();

    // Background Services
    builder.Services.AddHostedService<KafkaFlowHostedService>();
    builder.Services.AddHostedService<PhysicalDeletionBackgroundService>();

    var host = builder.Build();
    await host.RunAsync();
}
catch (Exception ex)
{
    Log.Fatal(ex, "Lifecycle worker terminated unexpectedly");
}
finally
{
    Log.CloseAndFlush();
}
```

### 4. Add to Solution

```bash
cd src/NovaTuneApp
dotnet sln add NovaTuneApp.Workers.Lifecycle/NovaTuneApp.Workers.Lifecycle.csproj
```

### 5. Register in AppHost

Location: `src/NovaTuneApp/NovaTuneApp.AppHost/AppHost.cs`

Add project reference to `NovaTuneApp.AppHost.csproj`:

```xml
<ProjectReference Include="..\NovaTuneApp.Workers.Lifecycle\NovaTuneApp.Workers.Lifecycle.csproj"/>
```

Add to AppHost.cs (in the non-testing block):

```csharp
// Lifecycle Worker - handles physical deletion of soft-deleted tracks
builder.AddProject<Projects.NovaTuneApp_Workers_Lifecycle>("lifecycle-worker")
    .WithReference(messaging)
    .WaitFor(messaging)
    .WithReference(database)
    .WaitFor(database)
    .WithReference(storage.GetEndpoint("api"))
    .WaitFor(storage)
    .WithEnvironment("NovaTune__TopicPrefix", "dev");
```

### 6. Create Configuration Class

Location: `src/NovaTuneApp/NovaTuneApp.Workers.Lifecycle/Configuration/LifecycleOptions.cs`

```csharp
namespace NovaTuneApp.Workers.Lifecycle.Configuration;

public class LifecycleOptions
{
    public const string SectionName = "Lifecycle";

    /// <summary>
    /// Interval between physical deletion polling.
    /// Default: 5 minutes.
    /// </summary>
    public TimeSpan PollingInterval { get; set; } = TimeSpan.FromMinutes(5);

    /// <summary>
    /// Maximum tracks to process per cycle.
    /// Default: 50.
    /// </summary>
    public int BatchSize { get; set; } = 50;

    /// <summary>
    /// Whether physical deletion is enabled.
    /// Default: true.
    /// </summary>
    public bool Enabled { get; set; } = true;
}
```

### 7. Create appsettings.json

Location: `src/NovaTuneApp/NovaTuneApp.Workers.Lifecycle/appsettings.json`

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.Hosting.Lifetime": "Information"
    }
  },
  "NovaTune": {
    "TopicPrefix": "dev"
  },
  "Lifecycle": {
    "PollingInterval": "00:05:00",
    "BatchSize": 50,
    "Enabled": true
  }
}
```

## Project Structure

```
NovaTuneApp.Workers.Lifecycle/
├── Configuration/
│   └── LifecycleOptions.cs
├── Handlers/
│   └── TrackDeletedHandler.cs
├── Services/
│   ├── IPhysicalDeletionService.cs
│   └── PhysicalDeletionService.cs
├── Program.cs
├── appsettings.json
├── appsettings.Development.json
└── NovaTuneApp.Workers.Lifecycle.csproj
```

## Dependencies Pattern

Workers typically depend on:

| Dependency | Purpose |
|------------|---------|
| `NovaTuneApp.ServiceDefaults` | OpenTelemetry, health checks, service discovery |
| `NovaTuneApp.ApiService` | Shared models, configuration, services |
| `KafkaFlow` | Kafka/Redpanda messaging |
| `RavenDB.Client` | Document database |
| `Minio` | Object storage |
| `Serilog` | Structured logging |

## Verification

After creating the project:

```bash
# Build solution
dotnet build src/NovaTuneApp/NovaTuneApp.sln

# Run the worker standalone
dotnet run --project src/NovaTuneApp/NovaTuneApp.Workers.Lifecycle

# Run with Aspire orchestration
dotnet run --project src/NovaTuneApp/NovaTuneApp.AppHost
```
