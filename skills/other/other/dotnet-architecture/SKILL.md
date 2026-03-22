---
name: dotnet-architecture
description: "Guides implementation of Clean Architecture in .NET projects. Covers all layers: DTO, Domain (Models, Services, Enums), Infra.Interfaces (Repository, AppServices), Infra (Context, Repository, AppServices), and Application (DI/Startup). Use when creating entities, services, repositories, or restructuring architecture. Works with any project type (Web, Console, Mobile, Windows)."
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Task
---

# .NET Clean Architecture Guide

You are an expert assistant that helps developers implement Clean Architecture in .NET projects. You guide the user through ALL required layers. This guide is **agnostic to the presentation layer** — it works for Web API, Console, Mobile (MAUI), Windows (WPF/WinForms), Worker Services, etc.

## Input

The user will describe what to create or modify: `$ARGUMENTS`

Before generating code:
1. **Read the solution structure** — Identify all projects/layers
2. **Find an existing entity** — Use it as the primary reference to match patterns exactly (naming, namespaces, mapping approach, DI style)
3. **Read the DbContext** (if applicable) — Understand database provider, column naming conventions, and existing configurations
4. **Read the Startup/DI setup** — Find the centralized DI class (usually `Startup.cs`)
5. **Identify the mapping strategy** — AutoMapper profiles, manual mapping, or Mapster

---

## Architecture Overview

### Layer Structure & Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│  Presentation (Console, API, Mobile, Windows, Worker, etc.) │
│  Depends on: Application                                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│  Application — DI/IoC, Startup, cross-cutting concerns      │
│  Depends on: everything needed to wire up the application   │
└──────────────────────────────┬──────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│      Domain      │ │      Infra       │ │       DTO        │
│ Models, Services │ │ Context, Repos,  │ │ Data contracts,  │
│ Enums, Rules     │ │ AppServices      │ │ IOptions configs │
│                  │ │                  │ │                  │
│ Depends on:      │ │ Depends on:      │ │ Depends on:      │
│ Infra.Interfaces │ │ Domain,          │ │ nothing          │
│ DTO              │ │ Infra.Interfaces │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
          │                    │
          ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  Infra.Interfaces — Repository & AppService contracts       │
│  Depends on: nothing (may depend on DTO only)               │
│  Uses generics to avoid coupling to Domain models           │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Project | Responsibility | Dependencies |
|-------|---------|---------------|-------------|
| **DTO** | `{Project}.DTO` | Data Transfer Objects, public contracts, `IOptions<T>` configuration classes | **None** |
| **Infra.Interfaces** | `{Project}.Infra.Interfaces` | Repository and AppService interfaces using **generics** (`<TModel>`) | **None** (may depend on DTO) |
| **Domain** | `{Project}.Domain` | Models (rich entities), Enums, Services (business rules), Service interfaces | Infra.Interfaces, DTO |
| **Infra** | `{Project}.Infra` | DbContext, Repository implementations, AppService implementations (SNS, Rabbit, GitHub, Email, etc.) | Domain, Infra.Interfaces |
| **Application** | `{Project}.Application` | Centralized DI/IoC via `Startup.cs`, cross-cutting concerns | All layers as needed |
| **Presentation** | Varies | UI/entry point — **NOT covered by this skill** | Application |

### Key Rules

- **Domain NEVER depends on Infra** — only on Infra.Interfaces (abstractions)
- **Infra.Interfaces has NO dependencies** on Domain or Infra — uses generics for type parameters
- **DTO has ZERO dependencies** — pure data contracts
- **Application is the composition root** — it wires everything together in a `Startup` class
- **Domain Models are NOT immutable** — they are rich entities with public setters and behavior methods
- **All services MUST have interfaces** — Domain services define interfaces in `Domain/Interfaces/`
- **Model interfaces are exceptional** — only create `I{Entity}Model` when there's a specific need

---

## Step-by-Step Implementation

### Step 1: DTO

Create data transfer objects in the `{Project}.DTO` project root.

```csharp
namespace {Project}.DTO;

public class {Entity}Info
{
    public long Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
```

**Guidelines:**
- Create separate DTOs if insert/update shapes differ: `{Entity}InsertInfo` (no Id), `{Entity}UpdateInfo` (with Id)
- Use nullable types for optional fields (`DateTime?`, `long?`)
- Configuration classes for `IOptions<T>` also live here (e.g., `DatabaseSettings`, `OpenAISettings`)
- **No dependencies on any other project**
- Match the naming convention of existing DTOs

### Step 2: Infra.Interfaces — Repository

Create repository interfaces in `{Project}.Infra.Interfaces/Repository/` using **generics**.

```csharp
namespace {Project}.Infra.Interfaces.Repository;

public interface I{Entity}Repository<TModel> where TModel : class
{
    Task<TModel> GetByIdAsync(long id);
    Task<List<TModel>> ListAllAsync();
    Task<TModel> InsertAsync(TModel entity);
    Task<TModel> UpdateAsync(TModel entity);
    Task DeleteAsync(long id);
}
```

**Guidelines:**
- **Always use generics** (`<TModel>`) — the interface must NOT reference Domain models directly
- The generic constraint `where TModel : class` is sufficient
- Keep interfaces focused — don't add methods that only one implementation needs
- Add pagination signatures if the project uses them: `Task<(List<TModel> Items, int TotalCount)>`

### Step 3: Infra.Interfaces — AppService (if applicable)

Create AppService interfaces in `{Project}.Infra.Interfaces/AppServices/` for infrastructure services.

```csharp
namespace {Project}.Infra.Interfaces.AppServices;

public interface I{External}AppService<TModel> where TModel : class
{
    Task<TModel> GetDataAsync(string identifier);
    Task SendAsync(TModel data);
}
```

**Guidelines:**
- AppServices are for **external infrastructure concerns**: messaging (SNS, RabbitMQ), external APIs (GitHub, OpenAI), file storage (S3, Azure Blob), email, etc.
- Use generics to keep the interface decoupled from Domain
- If generics don't make sense for a specific service (e.g., `IEmailAppService`), it's acceptable to use primitive types or DTO types instead

### Step 4: Domain Model

Create rich domain entities in `{Project}.Domain/Models/`.

```csharp
namespace {Project}.Domain.Models;

public class {Entity}
{
    public long Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Business behavior methods
    public void UpdateName(string newName)
    {
        if (string.IsNullOrWhiteSpace(newName))
            throw new ArgumentException("Name cannot be empty.", nameof(newName));
        Name = newName;
    }
}
```

**Guidelines:**
- Models are **rich entities** with public setters — NOT immutable
- Business behavior methods belong on the model (validation, state transitions)
- Model interfaces (`I{Entity}`) are **exceptional** — only create when there's a specific need (e.g., multiple implementations, testing boundaries)
- Enums go in `{Project}.Domain/Enums/`
- Domain models must **NOT depend on infrastructure types** (no EF attributes, no Pgvector `Vector`, etc.) — use primitive types (`float[]`, `string`, `byte[]`) and let Infra handle conversion

### Step 5: Domain Service Interface

Create service interfaces in `{Project}.Domain/Interfaces/`.

```csharp
namespace {Project}.Domain.Interfaces;

public interface I{Entity}Service
{
    Task<{Entity}Info> GetByIdAsync(long id);
    Task<List<{Entity}Info>> ListAllAsync();
    Task<{Entity}Info> CreateAsync({Entity}Info dto);
    Task<{Entity}Info> UpdateAsync({Entity}Info dto);
    Task DeleteAsync(long id);
}
```

**Guidelines:**
- **All services MUST have interfaces**
- Services receive/return **DTOs** at their public API
- Internally they work with Domain Models
- Match the existing service interface patterns in the project

### Step 6: Domain Service Implementation

Create service implementations in `{Project}.Domain/Services/`.

```csharp
using {Project}.Domain.Interfaces;
using {Project}.Domain.Models;
using {Project}.DTO;
using {Project}.Infra.Interfaces.Repository;

namespace {Project}.Domain.Services;

public class {Entity}Service : I{Entity}Service
{
    private readonly I{Entity}Repository<{Entity}> _repository;

    public {Entity}Service(I{Entity}Repository<{Entity}> repository)
    {
        _repository = repository;
    }

    public async Task<{Entity}Info> GetByIdAsync(long id)
    {
        var entity = await _repository.GetByIdAsync(id);
        return MapToDto(entity);
    }

    public async Task<{Entity}Info> CreateAsync({Entity}Info dto)
    {
        var entity = MapToModel(dto);
        entity.CreatedAt = DateTime.UtcNow;
        var saved = await _repository.InsertAsync(entity);
        return MapToDto(saved);
    }

    // Manual mapping — or use AutoMapper/Mapster if project uses it
    private static {Entity}Info MapToDto({Entity} entity) => new()
    {
        Id = entity.Id,
        Name = entity.Name,
        CreatedAt = entity.CreatedAt
    };

    private static {Entity} MapToModel({Entity}Info dto) => new()
    {
        Id = dto.Id,
        Name = dto.Name
    };
}
```

**Guidelines:**
- Services contain **business rules** that are not specific to a single domain entity
- Entity-specific behavior belongs on the Model itself
- Services depend on **Infra.Interfaces** (repository/AppService abstractions), never on Infra directly
- Match the mapping strategy used by the project (manual, AutoMapper, Mapster)

### Step 7: Infra — DbContext Configuration

Add `DbSet` and configure the entity in `OnModelCreating`.

```csharp
// Add DbSet
public DbSet<{Entity}> {Entity}s { get; set; }

// Inside OnModelCreating:
modelBuilder.Entity<{Entity}>(entity =>
{
    entity.ToTable("{table_name}");
    entity.HasKey(e => e.Id);

    entity.Property(e => e.Id)
        .HasColumnName("id")
        .UseIdentityAlwaysColumn();

    entity.Property(e => e.Name)
        .HasColumnName("name")
        .HasMaxLength(240)
        .IsRequired();

    entity.Property(e => e.CreatedAt)
        .HasColumnName("created_at")
        .HasColumnType("timestamp with time zone")
        .HasDefaultValueSql("now()");
});
```

**Conventions to detect and match:**
- Table naming: `snake_case` vs `PascalCase` vs plural vs singular
- Column naming: `snake_case` (`created_at`) vs `PascalCase` (`CreatedAt`)
- Primary key: auto-increment, identity, sequences, or GUID
- Timestamps: `timestamp with time zone` (PostgreSQL) vs `datetime2` (SQL Server)
- FK behavior: `DeleteBehavior.Cascade` vs `ClientSetNull` vs `Restrict`
- Use `ValueConverter` when Domain model types differ from database types (e.g., `float[]` → pgvector `Vector`)

### Step 8: Infra — Repository Implementation

```csharp
using {Project}.Domain.Models;
using {Project}.Infra.Context;
using {Project}.Infra.Interfaces.Repository;
using Microsoft.EntityFrameworkCore;

namespace {Project}.Infra.Repository;

public class {Entity}Repository : I{Entity}Repository<{Entity}>
{
    private readonly {DbContextType} _context;

    public {Entity}Repository({DbContextType} context)
    {
        _context = context;
    }

    public async Task<{Entity}> GetByIdAsync(long id)
    {
        return await _context.{Entity}s
            .AsNoTracking()
            .FirstOrDefaultAsync(e => e.Id == id)
            ?? throw new KeyNotFoundException($"{Entity} {id} not found.");
    }

    public async Task<List<{Entity}>> ListAllAsync()
    {
        return await _context.{Entity}s
            .AsNoTracking()
            .OrderBy(e => e.Name)
            .ToListAsync();
    }

    public async Task<{Entity}> InsertAsync({Entity} entity)
    {
        _context.{Entity}s.Add(entity);
        await _context.SaveChangesAsync();
        return entity;
    }

    public async Task<{Entity}> UpdateAsync({Entity} entity)
    {
        var existing = await _context.{Entity}s.FindAsync(entity.Id)
            ?? throw new KeyNotFoundException($"{Entity} {entity.Id} not found.");

        _context.Entry(existing).CurrentValues.SetValues(entity);
        await _context.SaveChangesAsync();
        return existing;
    }

    public async Task DeleteAsync(long id)
    {
        var entity = await _context.{Entity}s.FindAsync(id)
            ?? throw new KeyNotFoundException($"{Entity} {id} not found.");

        _context.{Entity}s.Remove(entity);
        await _context.SaveChangesAsync();
    }
}
```

### Step 9: Infra — AppService Implementation (if applicable)

```csharp
using {Project}.Domain.Models;
using {Project}.Infra.Interfaces.AppServices;

namespace {Project}.Infra.AppServices;

public class {External}AppService : I{External}AppService<{Model}>
{
    private readonly HttpClient _httpClient;

    public {External}AppService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    // Implementation that calls external service
}
```

**Examples of AppServices:**
- `GitHubAppService` — calls GitHub API via Octokit
- `OpenAIAppService` — calls OpenAI API for completions/embeddings
- `SnsAppService` — publishes messages to AWS SNS
- `RabbitAppService` — publishes/consumes RabbitMQ messages
- `EmailAppService` — sends emails via SMTP/SendGrid
- `StorageAppService` — uploads/downloads from S3/Azure Blob

### Step 10: Migration (if applicable)

```bash
dotnet ef migrations add Add{Entity}Table --project {InfraProject} --startup-project {StartupProject}
dotnet ef database update --project {InfraProject} --startup-project {StartupProject}
```

### Step 11: DI Registration — Application/Startup.cs

All DI registration is **centralized** in the `Startup` class.

```csharp
using {Project}.Domain.Interfaces;
using {Project}.Domain.Models;
using {Project}.Domain.Services;
using {Project}.Infra.Context;
using {Project}.Infra.Interfaces.Repository;
using {Project}.Infra.Repository;
using {Project}.Infra.AppServices;
using {Project}.Infra.Interfaces.AppServices;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace {Project}.Application;

public static class Startup
{
    public static IServiceCollection ConfigureServices(
        this IServiceCollection services,
        Action<{Settings}> configureSettings)
    {
        var settings = new {Settings}();
        configureSettings(settings);

        // IOptions configuration
        services.Configure<{SubSettings}>(opt => { /* ... */ });

        // DbContext
        services.AddDbContext<{DbContext}>(options =>
            options.UseNpgsql(settings.Database.ConnectionString));

        // Repositories
        services.AddScoped<I{Entity}Repository<{Entity}>, {Entity}Repository>();

        // AppServices
        services.AddHttpClient<I{External}AppService<{Model}>, {External}AppService>();

        // Domain Services
        services.AddScoped<I{Entity}Service, {Entity}Service>();

        return services;
    }
}
```

**Guidelines:**
- **One centralized `Startup` class** — all registrations in one place
- Match the lifetime used by the project: `AddScoped` (per-request), `AddTransient` (per-resolve), `AddSingleton` (app lifetime)
- Use `AddHttpClient<>` for services that need `HttpClient` (OpenAI, GitHub, etc.)
- AutoMapper: `services.AddAutoMapper(typeof(Startup).Assembly)` if used

---

## Checklist

| # | Layer | Action | Description |
|---|-------|--------|-------------|
| 1 | DTO | Create | `{Entity}Info.cs` (and Insert/Update variants if needed) |
| 2 | Infra.Interfaces | Create | `I{Entity}Repository<TModel>` in `Repository/` |
| 3 | Infra.Interfaces | Create | `I{External}AppService<TModel>` in `AppServices/` (if applicable) |
| 4 | Domain | Create | `{Entity}.cs` model in `Models/` |
| 5 | Domain | Create | `I{Entity}Service.cs` interface in `Interfaces/` |
| 6 | Domain | Create | `{Entity}Service.cs` implementation in `Services/` |
| 7 | Infra | Modify | DbContext — add `DbSet` and `OnModelCreating` configuration |
| 8 | Infra | Create | `{Entity}Repository.cs` in `Repository/` |
| 9 | Infra | Create | `{External}AppService.cs` in `AppServices/` (if applicable) |
| 10 | Infra | Run | `dotnet ef migrations add` (if applicable) |
| 11 | Application | Modify | `Startup.cs` — register repositories, AppServices, services |

---

## Response Guidelines

1. **Read existing files first** — Find an existing complete entity and use it as the reference for all layers
2. **Follow the order** — DTO → Infra.Interfaces → Domain → Infra → Application
3. **Match all conventions** exactly — naming, namespaces, folder structure, code style
4. **Run migrations** after modifying DbContext
5. **Detect and match** the database provider conventions (column naming, timestamps, key generation)
6. **Adapt mapping strategy** — AutoMapper, manual mapping, or whatever the project uses
7. **Match DI patterns** — registration style and service lifetimes
8. **Never touch the presentation layer** — this skill is agnostic to UI/entry point
9. **Keep Infra.Interfaces decoupled** — always use generics, never reference Domain models
10. **Domain models use primitive types** — infrastructure-specific types (Vector, BsonDocument, etc.) are converted in Infra via ValueConverters or mapping
