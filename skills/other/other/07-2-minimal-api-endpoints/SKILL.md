---
name: minimal-api-endpoints
description: "Generates Minimal API endpoints following Microsoft's recommended approach. Creates fast, testable HTTP APIs with minimal code using MapGet/MapPost/MapPut/MapDelete. Preferred over controller-based APIs for new projects."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR, FluentValidation
source: Microsoft Learn - Minimal APIs
---

# Minimal API Endpoints Generator

## Overview

**Microsoft's recommended approach for new projects.** Minimal APIs provide a simplified, high-performance way to build HTTP APIs with less boilerplate than controllers.

### Benefits Over Controllers
- ✅ **Simpler syntax** - Less code, more productivity
- ✅ **Better performance** - Reduced overhead
- ✅ **Easier testing** - Testable handler methods
- ✅ **Modern approach** - Latest .NET features
- ✅ **Less ceremony** - No controller classes needed

## Quick Reference

| HTTP Method | Extension Method | Use Case |
|-------------|------------------|----------|
| `MapGet` | Read single/list | `app.MapGet("/users/{id}", ...)` |
| `MapPost` | Create | `app.MapPost("/users", ...)` |
| `MapPut` | Update (full) | `app.MapPut("/users/{id}", ...)` |
| `MapDelete` | Delete | `app.MapDelete("/users/{id}", ...)` |

---

## Endpoint Structure

```
/API/Endpoints/
├── {Feature}/
│   ├── {Feature}Endpoints.cs
│   └── Request{Action}{Entity}.cs
└── ...
```

---

## Template: Complete CRUD Endpoints

```csharp
// src/{name}.api/Endpoints/{Feature}/{Feature}Endpoints.cs
using {name}.application.{feature}.Create{Entity};
using {name}.application.{feature}.Delete{Entity};
using {name}.application.{feature}.Get{Entity}ById;
using {name}.application.{feature}.Get{Entities};
using {name}.application.{feature}.Update{Entity};
using {name}.infrastructure.authorization;
using MediatR;
using Microsoft.AspNetCore.Http.HttpResults;

namespace {name}.api.Endpoints.{Feature};

/// <summary>
/// Endpoints for {Entity} management
/// </summary>
public static class {Feature}Endpoints
{
    /// <summary>
    /// Maps all {Entity} endpoints
    /// </summary>
    public static RouteGroupBuilder Map{Feature}Endpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/{entities}")
            .WithTags("{Feature}")
            .RequireAuthorization();

        group.MapGet("/{id:guid}", GetById)
            .WithName("Get{Entity}ById")
            .WithSummary("Get {entity} by ID")
            .Produces<{Entity}Response>(StatusCodes.Status200OK)
            .Produces(StatusCodes.Status404NotFound);

        group.MapGet("/", GetAll)
            .WithName("GetAll{Entities}")
            .WithSummary("Get all {entities}")
            .Produces<IReadOnlyList<{Entity}ListResponse>>(StatusCodes.Status200OK);

        group.MapPost("/", Create)
            .WithName("Create{Entity}")
            .WithSummary("Create new {entity}")
            .RequireAuthorization(Permissions.{Entities}Write)
            .Produces<Guid>(StatusCodes.Status201Created)
            .Produces(StatusCodes.Status400BadRequest);

        group.MapPut("/{id:guid}", Update)
            .WithName("Update{Entity}")
            .WithSummary("Update existing {entity}")
            .RequireAuthorization(Permissions.{Entities}Write)
            .Produces(StatusCodes.Status204NoContent)
            .Produces(StatusCodes.Status404NotFound)
            .Produces(StatusCodes.Status400BadRequest);

        group.MapDelete("/{id:guid}", Delete)
            .WithName("Delete{Entity}")
            .WithSummary("Delete {entity}")
            .RequireAuthorization(Permissions.{Entities}Write)
            .Produces(StatusCodes.Status204NoContent)
            .Produces(StatusCodes.Status404NotFound);

        return group;
    }

    // ═══════════════════════════════════════════════════════════════
    // HANDLER METHODS
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Gets an {entity} by ID
    /// </summary>
    private static async Task<Results<Ok<{Entity}Response>, NotFound>> GetById(
        Guid id,
        ISender sender,
        CancellationToken cancellationToken)
    {
        var query = new Get{Entity}ByIdQuery(id);
        var result = await sender.Send(query, cancellationToken);

        return result.IsSuccess
            ? TypedResults.Ok(result.Value)
            : TypedResults.NotFound();
    }

    /// <summary>
    /// Gets all {entities}
    /// </summary>
    private static async Task<Ok<IReadOnlyList<{Entity}ListResponse>>> GetAll(
        ISender sender,
        CancellationToken cancellationToken)
    {
        var query = new GetAll{Entities}Query();
        var result = await sender.Send(query, cancellationToken);

        return TypedResults.Ok(result.Value);
    }

    /// <summary>
    /// Creates a new {entity}
    /// </summary>
    private static async Task<Results<Created<Guid>, BadRequest<Error>>> Create(
        RequestCreate{Entity} request,
        ISender sender,
        CancellationToken cancellationToken)
    {
        var command = new Create{Entity}Command(
            request.Name,
            request.Description);

        var result = await sender.Send(command, cancellationToken);

        return result.IsSuccess
            ? TypedResults.Created($"/api/{entities}/{result.Value}", result.Value)
            : TypedResults.BadRequest(result.Error);
    }

    /// <summary>
    /// Updates an existing {entity}
    /// </summary>
    private static async Task<Results<NoContent, NotFound, BadRequest<Error>>> Update(
        Guid id,
        RequestUpdate{Entity} request,
        ISender sender,
        CancellationToken cancellationToken)
    {
        var command = new Update{Entity}Command(id, request.Name, request.Description);
        var result = await sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return result.Error.Code.Contains("NotFound")
                ? TypedResults.NotFound()
                : TypedResults.BadRequest(result.Error);
        }

        return TypedResults.NoContent();
    }

    /// <summary>
    /// Deletes an {entity}
    /// </summary>
    private static async Task<Results<NoContent, NotFound>> Delete(
        Guid id,
        ISender sender,
        CancellationToken cancellationToken)
    {
        var command = new Delete{Entity}Command(id);
        var result = await sender.Send(command, cancellationToken);

        return result.IsSuccess
            ? TypedResults.NoContent()
            : TypedResults.NotFound();
    }
}
```

---

## Template: Request DTOs

```csharp
// src/{name}.api/Endpoints/{Feature}/RequestCreate{Entity}.cs
namespace {name}.api.Endpoints.{Feature};

/// <summary>
/// Request to create a new {entity}
/// </summary>
public sealed record RequestCreate{Entity}(
    string Name,
    string? Description);

/// <summary>
/// Request to update an existing {entity}
/// </summary>
public sealed record RequestUpdate{Entity}(
    string Name,
    string? Description);
```

---

## Template: Program.cs Registration

```csharp
// src/{name}.api/Program.cs
using {name}.api.Endpoints.{Feature};
using {name}.application;
using {name}.infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add services
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
app.UseAuthentication();
app.UseAuthorization();

// Map endpoints
app.Map{Feature}Endpoints();
// Add more endpoint groups here

app.Run();
```

---

## Template: Complex Endpoints with MapGroup

```csharp
// src/{name}.api/Endpoints/{Feature}/{Feature}Endpoints.cs
public static class {Feature}Endpoints
{
    public static RouteGroupBuilder Map{Feature}Endpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/{entities}")
            .WithTags("{Feature}")
            .RequireAuthorization();

        // Standard CRUD
        group.MapGet("/{id:guid}", GetById);
        group.MapGet("/", GetAll);
        group.MapPost("/", Create);
        group.MapPut("/{id:guid}", Update);
        group.MapDelete("/{id:guid}", Delete);

        // Custom operations
        group.MapPost("/{id:guid}/activate", Activate)
            .WithName("Activate{Entity}")
            .RequireAuthorization(Permissions.{Entities}Write);

        group.MapPost("/{id:guid}/deactivate", Deactivate)
            .WithName("Deactivate{Entity}")
            .RequireAuthorization(Permissions.{Entities}Write);

        // Search
        group.MapGet("/search", Search)
            .WithName("Search{Entities}")
            .AllowAnonymous();

        // Related resources
        var childrenGroup = group.MapGroup("/{parentId:guid}/children")
            .WithTags("{Feature} - Children");

        childrenGroup.MapGet("/", GetChildren);
        childrenGroup.MapPost("/", AddChild);
        childrenGroup.MapDelete("/{childId:guid}", RemoveChild);

        return group;
    }

    private static async Task<Results<Ok, BadRequest<Error>>> Activate(
        Guid id,
        ISender sender,
        CancellationToken cancellationToken)
    {
        var command = new Activate{Entity}Command(id);
        var result = await sender.Send(command, cancellationToken);

        return result.IsSuccess
            ? TypedResults.Ok()
            : TypedResults.BadRequest(result.Error);
    }

    private static async Task<Ok<IReadOnlyList<{Entity}Response>>> Search(
        string? term,
        int pageNumber,
        int pageSize,
        ISender sender,
        CancellationToken cancellationToken)
    {
        var query = new Search{Entities}Query(term, pageNumber, pageSize);
        var result = await sender.Send(query, cancellationToken);

        return TypedResults.Ok(result.Value);
    }
}
```

---

## Template: Endpoint Filters (Validation)

```csharp
// src/{name}.api/Endpoints/Filters/ValidationFilter.cs
using {name}.domain.abstractions;

namespace {name}.api.Endpoints.Filters;

/// <summary>
/// Endpoint filter for validation
/// </summary>
public class ValidationFilter<T> : IEndpointFilter where T : class
{
    private readonly IValidator<T> _validator;

    public ValidationFilter(IValidator<T> validator)
    {
        _validator = validator;
    }

    public async ValueTask<object?> InvokeAsync(
        EndpointFilterInvocationContext context,
        EndpointFilterDelegate next)
    {
        var request = context.Arguments.OfType<T>().FirstOrDefault();
        
        if (request is null)
        {
            return await next(context);
        }

        var validationResult = await _validator.ValidateAsync(request);

        if (!validationResult.IsValid)
        {
            return TypedResults.BadRequest(new Error(
                "Validation.Failed",
                string.Join(", ", validationResult.Errors.Select(e => e.ErrorMessage))));
        }

        return await next(context);
    }
}

// Usage in endpoint
group.MapPost("/", Create)
    .AddEndpointFilter<ValidationFilter<RequestCreate{Entity}>>();
```

---

## Template: Authorization

```csharp
// Multiple authorization options

// 1. Require authentication for all endpoints in group
var group = routes.MapGroup("/api/{entities}")
    .RequireAuthorization();

// 2. Specific permission on endpoint
group.MapPost("/", Create)
    .RequireAuthorization(Permissions.{Entities}Write);

// 3. Multiple policies
group.MapDelete("/{id:guid}", Delete)
    .RequireAuthorization(Permissions.{Entities}Write, Permissions.Admin);

// 4. Allow anonymous (override group auth)
group.MapGet("/public", GetPublicData)
    .AllowAnonymous();

// 5. Roles
group.MapPost("/admin/action", AdminAction)
    .RequireAuthorization(policy => policy.RequireRole("Admin", "SuperAdmin"));
```

---

## Template: API Versioning with MapGroup

```csharp
// src/{name}.api/Endpoints/{Feature}/{Feature}Endpoints.cs
public static class {Feature}Endpoints
{
    public static void Map{Feature}Endpoints(this IEndpointRouteBuilder routes)
    {
        // Version 1
        var v1 = routes.MapGroup("/api/v1/{entities}")
            .WithTags("{Feature} V1")
            .HasApiVersion(1.0);

        v1.MapGet("/{id:guid}", GetByIdV1);
        v1.MapPost("/", CreateV1);

        // Version 2 with breaking changes
        var v2 = routes.MapGroup("/api/v2/{entities}")
            .WithTags("{Feature} V2")
            .HasApiVersion(2.0);

        v2.MapGet("/{id:guid}", GetByIdV2);
        v2.MapPost("/", CreateV2);
    }
}
```

---

## TypedResults Pattern

Always use `TypedResults` for type-safe, testable responses:

```csharp
// ✅ CORRECT: TypedResults with union return type
private static async Task<Results<Ok<UserResponse>, NotFound>> GetUser(
    Guid id,
    ISender sender,
    CancellationToken cancellationToken)
{
    var result = await sender.Send(new GetUserQuery(id), cancellationToken);
    
    return result.IsSuccess
        ? TypedResults.Ok(result.Value)
        : TypedResults.NotFound();
}

// ❌ WRONG: Non-typed Results
private static async Task<IResult> GetUser(Guid id, ISender sender)
{
    var result = await sender.Send(new GetUserQuery(id));
    return result.IsSuccess ? Results.Ok(result.Value) : Results.NotFound();
}
```

### Benefits of TypedResults
- ✅ **Compile-time safety** - Catch errors at compile time
- ✅ **Better testing** - Assert on specific result types
- ✅ **OpenAPI metadata** - Automatic Swagger documentation
- ✅ **IntelliSense support** - Better IDE experience

---

## Testing Minimal API Endpoints

```csharp
// Unit test for endpoint handler
public class {Feature}EndpointsTests
{
    [Fact]
    public async Task GetById_ExistingId_ReturnsOk()
    {
        // Arrange
        var sender = Substitute.For<ISender>();
        var response = new {Entity}Response(Guid.NewGuid(), "Test");
        sender.Send(Arg.Any<Get{Entity}ByIdQuery>(), Arg.Any<CancellationToken>())
            .Returns(Result.Success(response));

        // Act
        var result = await {Feature}Endpoints.GetById(
            Guid.NewGuid(),
            sender,
            CancellationToken.None);

        // Assert - Type-safe assertion
        Assert.IsType<Ok<{Entity}Response>>(result.Result);
    }

    [Fact]
    public async Task GetById_NonExistingId_ReturnsNotFound()
    {
        // Arrange
        var sender = Substitute.For<ISender>();
        sender.Send(Arg.Any<Get{Entity}ByIdQuery>(), Arg.Any<CancellationToken>())
            .Returns(Result.Failure<{Entity}Response>({Entity}Errors.NotFound));

        // Act
        var result = await {Feature}Endpoints.GetById(
            Guid.NewGuid(),
            sender,
            CancellationToken.None);

        // Assert
        Assert.IsType<NotFound>(result.Result);
    }
}
```

---

## OpenAPI / Swagger Documentation

```csharp
group.MapGet("/{id:guid}", GetById)
    .WithName("Get{Entity}ById")
    .WithSummary("Get {entity} by ID")
    .WithDescription("Retrieves a single {entity} by its unique identifier")
    .WithOpenApi()
    .Produces<{Entity}Response>(StatusCodes.Status200OK)
    .Produces(StatusCodes.Status404NotFound)
    .ProducesProblem(StatusCodes.Status400BadRequest);
```

---

## Organizing Endpoints

### Option 1: Static Class per Feature (Recommended)
```
/Endpoints/
├── Users/
│   ├── UsersEndpoints.cs
│   └── Requests.cs
├── Products/
│   ├── ProductsEndpoints.cs
│   └── Requests.cs
```

### Option 2: Extension Methods on IEndpointRouteBuilder
```csharp
public static class EndpointExtensions
{
    public static IEndpointRouteBuilder MapAllEndpoints(this IEndpointRouteBuilder routes)
    {
        routes.MapUsersEndpoints();
        routes.MapProductsEndpoints();
        routes.MapOrdersEndpoints();
        return routes;
    }
}

// In Program.cs
app.MapAllEndpoints();
```

---

## Critical Rules

1. **Use TypedResults** - Always prefer TypedResults over Results
2. **Static methods for handlers** - Easier to test
3. **MapGroup for organization** - Group related endpoints
4. **XML documentation** - Document all public methods
5. **Explicit return types** - Use Results<T1, T2, ...> union types
6. **CancellationToken always** - Pass through all async operations
7. **Route constraints** - Use `{id:guid}`, `{id:int}`, etc.
8. **Authorization by default** - RequireAuthorization on group
9. **WithName for link generation** - Named routes for CreatedAtRoute
10. **Organize by feature** - Not by HTTP verb

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Lambdas with business logic
app.MapPost("/users", async (CreateUserRequest request, IUserRepository repo) =>
{
    if (await repo.ExistsByEmail(request.Email))
        return Results.BadRequest("Email exists");
    
    var user = new User { Email = request.Email };
    repo.Add(user);
    await repo.SaveAsync();
    return Results.Created($"/users/{user.Id}", user);
});

// ✅ CORRECT: Handler method calls command via MediatR
app.MapPost("/users", Create);

private static async Task<Results<Created<Guid>, BadRequest<Error>>> Create(
    CreateUserRequest request,
    ISender sender,
    CancellationToken cancellationToken)
{
    var command = new CreateUserCommand(request.Email);
    var result = await sender.Send(command, cancellationToken);
    
    return result.IsSuccess
        ? TypedResults.Created($"/users/{result.Value}", result.Value)
        : TypedResults.BadRequest(result.Error);
}

// ❌ WRONG: Returning IResult (not type-safe)
private static async Task<IResult> GetUser(Guid id)

// ✅ CORRECT: Explicit return type with TypedResults
private static async Task<Results<Ok<UserResponse>, NotFound>> GetUser(Guid id)

// ❌ WRONG: Controllers in Minimal API project
public class UsersController : ControllerBase { }

// ✅ CORRECT: Static endpoint classes
public static class UsersEndpoints { }
```

---

## Related Skills

- `02-cqrs-command-generator` - Generate commands for endpoints
- `03-cqrs-query-generator` - Generate queries for endpoints
- `08-result-pattern` - Handle endpoint results
- `12-jwt-authentication` - Add authentication
- `13-permission-authorization` - Add authorization
- `01-dotnet-clean-architecture` - Overall architecture

---

## Migration from Controllers

If migrating from controllers:

```csharp
// Before: Controller
[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet("{id}")]
    public async Task<ActionResult<UserResponse>> GetById(Guid id)
    {
        // ...
    }
}

// After: Minimal API
public static class UsersEndpoints
{
    public static RouteGroupBuilder MapUsersEndpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/users");
        group.MapGet("/{id:guid}", GetById);
        return group;
    }

    private static async Task<Results<Ok<UserResponse>, NotFound>> GetById(
        Guid id,
        ISender sender,
        CancellationToken cancellationToken)
    {
        // ...
    }
}
```

---

**Minimal APIs are Microsoft's recommended approach. They provide better performance, simpler code, and easier testing than controllers.**
