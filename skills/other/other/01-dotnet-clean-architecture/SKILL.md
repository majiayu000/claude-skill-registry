---
name: dotnet-clean-architecture
description: "Scaffolds a complete .NET solution following Clean Architecture principles with proper layer separation (API, Application, Domain, Infrastructure). Creates project structure, dependency injection setup, and cross-cutting concerns configuration."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR, FluentValidation, Entity Framework Core, Dapper
---

# .NET Clean Architecture Project Scaffolder

## Overview

This skill generates a complete .NET solution following Clean Architecture (also known as Onion Architecture or Hexagonal Architecture). The architecture enforces separation of concerns through distinct layers with unidirectional dependencies pointing inward.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  Controllers, Middleware, Request/Response DTOs             │
├─────────────────────────────────────────────────────────────┤
│                   Infrastructure Layer                       │
│  EF Core, Repositories, External Services, Authentication   │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│  Commands, Queries, Handlers, Validators, DTOs              │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                            │
│  Entities, Value Objects, Domain Events, Interfaces         │
└─────────────────────────────────────────────────────────────┘
```

**Dependency Rule**: Dependencies point inward. Domain has no dependencies. Application depends only on Domain. Infrastructure implements interfaces from Domain/Application.

## Quick Reference

| Task | Command/Action |
|------|----------------|
| Create solution | `dotnet new sln -n {SolutionName}` |
| Create Domain project | `dotnet new classlib -n {name}.domain` |
| Create Application project | `dotnet new classlib -n {name}.application` |
| Create Infrastructure project | `dotnet new classlib -n {name}.infrastructure` |
| Create API project | `dotnet new webapi -n {name}.api` |
| Add project to solution | `dotnet sln add src/{project}/{project}.csproj` |
| Add project reference | `dotnet add reference ../other/other.csproj` |

---

## Project Structure

```
{SolutionName}/
├── src/
│   ├── {name}.domain/
│   │   ├── Abstractions/
│   │   │   ├── Entity.cs
│   │   │   ├── IDomainEvent.cs
│   │   │   ├── IUnitOfWork.cs
│   │   │   └── Result.cs
│   │   ├── {Aggregate}/
│   │   │   ├── {Entity}.cs
│   │   │   ├── {Entity}Errors.cs
│   │   │   ├── I{Entity}Repository.cs
│   │   │   ├── ValueObjects/
│   │   │   └── Events/
│   │   └── {name}.domain.csproj
│   │
│   ├── {name}.application/
│   │   ├── Abstractions/
│   │   │   ├── Behaviors/
│   │   │   │   ├── LoggingBehavior.cs
│   │   │   │   └── ValidationBehavior.cs
│   │   │   ├── Messaging/
│   │   │   │   ├── ICommand.cs
│   │   │   │   ├── ICommandHandler.cs
│   │   │   │   ├── IQuery.cs
│   │   │   │   └── IQueryHandler.cs
│   │   │   ├── Authentication/
│   │   │   ├── Clock/
│   │   │   └── Data/
│   │   ├── {Feature}/
│   │   │   ├── Create{Entity}/
│   │   │   ├── Update{Entity}/
│   │   │   ├── Delete{Entity}/
│   │   │   └── Get{Entity}/
│   │   ├── DependencyInjection.cs
│   │   └── {name}.application.csproj
│   │
│   ├── {name}.infrastructure/
│   │   ├── Authentication/
│   │   ├── Authorization/
│   │   ├── Clock/
│   │   ├── Configurations/
│   │   ├── Repositories/
│   │   ├── Outbox/
│   │   ├── ApplicationDbContext.cs
│   │   ├── DependencyInjection.cs
│   │   └── {name}.infrastructure.csproj
│   │
│   └── {name}.api/
│       ├── Controllers/
│       ├── Middleware/
│       ├── Extensions/
│       ├── Program.cs
│       ├── appsettings.json
│       └── {name}.api.csproj
│
├── tests/
│   ├── {name}.domain.tests/
│   ├── {name}.application.tests/
│   └── {name}.api.tests/
│
└── {SolutionName}.sln
```

---

## Step 1: Create Solution and Projects

```bash
# Create solution
dotnet new sln -n {SolutionName}

# Create projects
dotnet new classlib -n {name}.domain -o src/{name}.domain
dotnet new classlib -n {name}.application -o src/{name}.application
dotnet new classlib -n {name}.infrastructure -o src/{name}.infrastructure
dotnet new webapi -n {name}.api -o src/{name}.api

# Add projects to solution
dotnet sln add src/{name}.domain/{name}.domain.csproj
dotnet sln add src/{name}.application/{name}.application.csproj
dotnet sln add src/{name}.infrastructure/{name}.infrastructure.csproj
dotnet sln add src/{name}.api/{name}.api.csproj

# Add project references
cd src/{name}.application
dotnet add reference ../{name}.domain/{name}.domain.csproj

cd ../{name}.infrastructure
dotnet add reference ../{name}.domain/{name}.domain.csproj
dotnet add reference ../{name}.application/{name}.application.csproj

cd ../{name}.api
dotnet add reference ../{name}.application/{name}.application.csproj
dotnet add reference ../{name}.infrastructure/{name}.infrastructure.csproj
```

---

## Step 2: Domain Layer Setup

### Entity Base Class

```csharp
// src/{name}.domain/Abstractions/Entity.cs
namespace {name}.domain.abstractions;

public abstract class Entity
{
    private readonly List<IDomainEvent> _domainEvents = new();

    protected Entity(Guid id)
    {
        Id = id;
    }

    protected Entity() { } // EF Core

    public Guid Id { get; init; }

    public IReadOnlyList<IDomainEvent> GetDomainEvents() => _domainEvents.ToList();

    public void ClearDomainEvents() => _domainEvents.Clear();

    protected void RaiseDomainEvent(IDomainEvent domainEvent) => _domainEvents.Add(domainEvent);
}
```

### Domain Event Interface

```csharp
// src/{name}.domain/Abstractions/IDomainEvent.cs
using MediatR;

namespace {name}.domain.abstractions;

public interface IDomainEvent : INotification
{
}
```

### Unit of Work Interface

```csharp
// src/{name}.domain/Abstractions/IUnitOfWork.cs
namespace {name}.domain.abstractions;

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
```

### Result Pattern (see result-pattern skill for full implementation)

```csharp
// src/{name}.domain/Abstractions/Result.cs
namespace {name}.domain.abstractions;

public class Result
{
    protected Result(bool isSuccess, Error error)
    {
        if (isSuccess && error != Error.None)
            throw new InvalidOperationException();
        if (!isSuccess && error == Error.None)
            throw new InvalidOperationException();

        IsSuccess = isSuccess;
        Error = error;
    }

    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public Error Error { get; }

    public static Result Success() => new(true, Error.None);
    public static Result Failure(Error error) => new(false, error);
    public static Result<TValue> Success<TValue>(TValue value) => new(value, true, Error.None);
    public static Result<TValue> Failure<TValue>(Error error) => new(default, false, error);
}

public class Result<TValue> : Result
{
    private readonly TValue? _value;

    protected internal Result(TValue? value, bool isSuccess, Error error)
        : base(isSuccess, error)
    {
        _value = value;
    }

    public TValue Value => IsSuccess
        ? _value!
        : throw new InvalidOperationException("Cannot access value of a failed result");

    public static implicit operator Result<TValue>(TValue? value) =>
        value is not null ? Success(value) : Failure<TValue>(Error.NullValue);
}

public record Error(string Code, string Description)
{
    public static readonly Error None = new(string.Empty, string.Empty);
    public static readonly Error NullValue = new("Error.NullValue", "A null value was provided");
}
```

---

## Step 3: Application Layer Setup

### Package References

```xml
<!-- {name}.application.csproj -->
<ItemGroup>
    <PackageReference Include="FluentValidation" Version="11.*" />
    <PackageReference Include="FluentValidation.DependencyInjectionExtensions" Version="11.*" />
    <PackageReference Include="MediatR" Version="12.*" />
    <PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="8.*" />
</ItemGroup>
```

### CQRS Abstractions

```csharp
// src/{name}.application/Abstractions/Messaging/ICommand.cs
using MediatR;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.messaging;

public interface ICommand : IRequest<Result> { }

public interface ICommand<TResponse> : IRequest<Result<TResponse>> { }
```

```csharp
// src/{name}.application/Abstractions/Messaging/ICommandHandler.cs
using MediatR;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.messaging;

public interface ICommandHandler<TCommand> : IRequestHandler<TCommand, Result>
    where TCommand : ICommand { }

public interface ICommandHandler<TCommand, TResponse> : IRequestHandler<TCommand, Result<TResponse>>
    where TCommand : ICommand<TResponse> { }
```

```csharp
// src/{name}.application/Abstractions/Messaging/IQuery.cs
using MediatR;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.messaging;

public interface IQuery<TResponse> : IRequest<Result<TResponse>> { }
```

```csharp
// src/{name}.application/Abstractions/Messaging/IQueryHandler.cs
using MediatR;
using {name}.domain.abstractions;

namespace {name}.application.abstractions.messaging;

public interface IQueryHandler<TQuery, TResponse> : IRequestHandler<TQuery, Result<TResponse>>
    where TQuery : IQuery<TResponse> { }
```

### Dependency Injection

```csharp
// src/{name}.application/DependencyInjection.cs
using FluentValidation;
using Microsoft.Extensions.DependencyInjection;
using {name}.application.abstractions.behaviors;

namespace {name}.application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddMediatR(configuration =>
        {
            configuration.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly);
            configuration.AddOpenBehavior(typeof(LoggingBehavior<,>));
            configuration.AddOpenBehavior(typeof(ValidationBehavior<,>));
        });

        services.AddValidatorsFromAssembly(typeof(DependencyInjection).Assembly);

        return services;
    }
}
```

---

## Step 4: Infrastructure Layer Setup

### Package References

```xml
<!-- {name}.infrastructure.csproj -->
<ItemGroup>
    <PackageReference Include="Dapper" Version="2.*" />
    <PackageReference Include="EFCore.NamingConventions" Version="8.*" />
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.*" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.*" />
    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.*" />
    <PackageReference Include="Quartz.Extensions.Hosting" Version="3.*" />
</ItemGroup>
```

### Application DbContext

```csharp
// src/{name}.infrastructure/ApplicationDbContext.cs
using Microsoft.EntityFrameworkCore;
using {name}.application.abstractions.clock;
using {name}.domain.abstractions;

namespace {name}.infrastructure;

public sealed class ApplicationDbContext : DbContext, IUnitOfWork
{
    private readonly IDateTimeProvider _dateTimeProvider;

    public ApplicationDbContext(
        DbContextOptions<ApplicationDbContext> options,
        IDateTimeProvider dateTimeProvider)
        : base(options)
    {
        _dateTimeProvider = dateTimeProvider;
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Add domain events to outbox before saving
        AddDomainEventsAsOutboxMessages();
        return await base.SaveChangesAsync(cancellationToken);
    }

    private void AddDomainEventsAsOutboxMessages()
    {
        // See outbox-pattern skill for implementation
    }
}
```

### Dependency Injection

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using {name}.application.abstractions.clock;
using {name}.application.abstractions.data;
using {name}.domain.abstractions;
using {name}.infrastructure.clock;

namespace {name}.infrastructure;

public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddTransient<IDateTimeProvider, DateTimeProvider>();

        AddPersistence(services, configuration);
        AddAuthentication(services, configuration);
        AddAuthorization(services);
        AddHealthChecks(services, configuration);

        return services;
    }

    private static void AddPersistence(IServiceCollection services, IConfiguration configuration)
    {
        var connectionString = configuration.GetConnectionString("Database")
            ?? throw new ArgumentNullException(nameof(configuration));

        services.AddDbContext<ApplicationDbContext>(options =>
        {
            options.UseNpgsql(connectionString)
                   .UseSnakeCaseNamingConvention();
        });

        services.AddScoped<IUnitOfWork>(sp => sp.GetRequiredService<ApplicationDbContext>());

        services.AddSingleton<ISqlConnectionFactory>(_ => new SqlConnectionFactory(connectionString));

        // Register repositories here
        // services.AddScoped<I{Entity}Repository, {Entity}Repository>();
    }

    private static void AddAuthentication(IServiceCollection services, IConfiguration configuration)
    {
        // See jwt-authentication skill
    }

    private static void AddAuthorization(IServiceCollection services)
    {
        // See permission-authorization skill
    }

    private static void AddHealthChecks(IServiceCollection services, IConfiguration configuration)
    {
        services.AddHealthChecks()
            .AddNpgSql(configuration.GetConnectionString("Database")!);
    }
}
```

---

## Step 5: API Layer Setup

### Program.cs

```csharp
// src/{name}.api/Program.cs
using HealthChecks.UI.Client;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Serilog;
using {name}.application;
using {name}.infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseSerilogRequestLogging();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();
app.MapHealthChecks("health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});

app.Run();
```

### appsettings.json

```json
{
  "ConnectionStrings": {
    "Database": "Host=localhost;Port=5432;Database={name}-db;Username=postgres;Password=postgres"
  },
  "Serilog": {
    "Using": ["Serilog.Sinks.Console"],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning"
      }
    },
    "WriteTo": [{ "Name": "Console" }],
    "Enrich": ["FromLogContext", "WithMachineName", "WithThreadId"]
  },
  "Authentication": {
    "Audience": "{name}",
    "Issuer": "{name}-auth",
    "SecretKey": "your-secret-key-at-least-32-characters-long"
  }
}
```

---

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Solution | PascalCase | `HumanPwr` |
| Projects | lowercase with dots | `humanpwr.domain` |
| Namespaces | lowercase | `humanpwr.domain.users` |
| Classes | PascalCase | `UserRepository` |
| Interfaces | IPascalCase | `IUserRepository` |
| Commands | {Action}{Entity}Command | `CreateUserCommand` |
| Queries | Get{Entity}Query | `GetUserByIdQuery` |
| Handlers | {Command/Query}Handler | `CreateUserCommandHandler` |
| Responses | {Entity}Response | `UserResponse` |
| Domain Events | {Entity}{Action}DomainEvent | `UserCreatedDomainEvent` |
| Errors | {Entity}Errors | `UserErrors` |

---

## Critical Rules

1. **Domain has ZERO dependencies** on other layers or external packages (except MediatR for IDomainEvent)
2. **Application depends only on Domain** - no infrastructure concerns
3. **Infrastructure implements interfaces** defined in Domain/Application
4. **API only references Application and Infrastructure** - never Domain directly for services
5. **Use Result pattern** instead of exceptions for business logic errors
6. **Commands modify state**, Queries read state (CQRS)
7. **One handler per Command/Query** - no shared handlers
8. **Repositories are per aggregate root** - not per entity
9. **Domain events are raised in domain**, handled in application layer
10. **Always use CancellationToken** in async operations

---

## Related Skills

- `cqrs-command-generator` - Generate Commands with handlers
- `cqrs-query-generator` - Generate Queries with handlers
- `domain-entity-generator` - Generate Domain entities
- `repository-pattern` - Generate Repositories
- `ef-core-configuration` - Generate EF configurations
- `result-pattern` - Implement Result pattern
- `pipeline-behaviors` - Create MediatR behaviors
