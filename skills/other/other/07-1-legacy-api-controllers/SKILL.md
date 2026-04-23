---
name: api-controller-generator
description: "Generates RESTful API Controllers with proper routing, versioning, authorization, and MediatR integration. Follows REST conventions and Clean Architecture patterns."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR, Asp.Versioning
---

# API Controller Generator

## Overview

This skill generates RESTful API Controllers following best practices:

- **MediatR integration** - Send commands/queries via ISender
- **API versioning** - URL segment versioning
- **Authorization** - Role and permission-based
- **Consistent responses** - Proper HTTP status codes
- **Request/Response DTOs** - Separate from domain

## Quick Reference

| HTTP Method | Action | Returns |
|-------------|--------|---------|
| `GET /{id}` | Get by ID | `200 OK` / `404 Not Found` |
| `GET /` | Get all/list | `200 OK` |
| `POST /` | Create | `201 Created` / `400 Bad Request` |
| `PUT /{id}` | Full update | `200 OK` / `404 Not Found` |
| `PATCH /{id}` | Partial update | `200 OK` / `404 Not Found` |
| `DELETE /{id}` | Delete | `204 No Content` / `404 Not Found` |

---

## Controller Structure

```
/API/Controllers/
├── {Feature}/
│   ├── {Entity}Controller.cs
│   ├── Request{Action}{Entity}.cs
│   └── ...
└── ...
```

---

## Template: Complete CRUD Controller

```csharp
// src/{name}.api/Controllers/{Feature}/{Entity}Controller.cs
using Asp.Versioning;
using MediatR;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using {name}.application.{feature}.Create{Entity};
using {name}.application.{feature}.Delete{Entity};
using {name}.application.{feature}.Get{Entity}ById;
using {name}.application.{feature}.Get{Entities};
using {name}.application.{feature}.Update{Entity};
using {name}.infrastructure.authorization;

namespace {name}.api.Controllers.{Feature};

[Authorize]
[ApiController]
[ApiVersion(ApiVersions.V1)]
[Route("api/v{version:apiVersion}/{entities}")]
public class {Entity}Controller : ControllerBase
{
    private readonly ISender _sender;

    public {Entity}Controller(ISender sender)
    {
        _sender = sender;
    }

    // ═══════════════════════════════════════════════════════════════
    // GET: api/v1/{entities}/{id}
    // ═══════════════════════════════════════════════════════════════
    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof({Entity}Response), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(
        Guid id,
        CancellationToken cancellationToken)
    {
        var query = new Get{Entity}ByIdQuery(id);

        var result = await _sender.Send(query, cancellationToken);

        if (result.IsFailure)
        {
            return NotFound(result.Error);
        }

        return Ok(result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // GET: api/v1/{entities}
    // ═══════════════════════════════════════════════════════════════
    [HttpGet]
    [ProducesResponseType(typeof(IReadOnlyList<{Entity}ListResponse>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetAll(CancellationToken cancellationToken)
    {
        var query = new GetAll{Entities}Query();

        var result = await _sender.Send(query, cancellationToken);

        return Ok(result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // GET: api/v1/{entities}/organization/{organizationId}
    // ═══════════════════════════════════════════════════════════════
    [HttpGet("organization/{organizationId:guid}")]
    [HasPermission(Permissions.{Entities}Read)]
    [ProducesResponseType(typeof(IReadOnlyList<{Entity}Response>), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetByOrganizationId(
        Guid organizationId,
        CancellationToken cancellationToken)
    {
        var query = new Get{Entities}ByOrganizationIdQuery(organizationId);

        var result = await _sender.Send(query, cancellationToken);

        return Ok(result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // POST: api/v1/{entities}
    // ═══════════════════════════════════════════════════════════════
    [HttpPost]
    [HasPermission(Permissions.{Entities}Write)]
    [ProducesResponseType(typeof(Guid), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create(
        [FromBody] RequestCreate{Entity} request,
        CancellationToken cancellationToken)
    {
        var command = new Create{Entity}Command(
            request.Name,
            request.Description,
            request.OrganizationId);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return BadRequest(result.Error);
        }

        return CreatedAtAction(
            nameof(GetById),
            new { id = result.Value },
            result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // PUT: api/v1/{entities}/{id}
    // ═══════════════════════════════════════════════════════════════
    [HttpPut("{id:guid}")]
    [HasPermission(Permissions.{Entities}Write)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Update(
        Guid id,
        [FromBody] RequestUpdate{Entity} request,
        CancellationToken cancellationToken)
    {
        var command = new Update{Entity}Command(
            id,
            request.Name,
            request.Description);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return result.Error.Code.Contains("NotFound")
                ? NotFound(result.Error)
                : BadRequest(result.Error);
        }

        return Ok();
    }

    // ═══════════════════════════════════════════════════════════════
    // PATCH: api/v1/{entities}/{id}
    // ═══════════════════════════════════════════════════════════════
    [HttpPatch("{id:guid}")]
    [HasPermission(Permissions.{Entities}Write)]
    [ProducesResponseType(StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> PartialUpdate(
        Guid id,
        [FromBody] RequestPatch{Entity} request,
        CancellationToken cancellationToken)
    {
        var command = new Patch{Entity}Command(id, request);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return result.Error.Code.Contains("NotFound")
                ? NotFound(result.Error)
                : BadRequest(result.Error);
        }

        return Ok();
    }

    // ═══════════════════════════════════════════════════════════════
    // DELETE: api/v1/{entities}/{id}
    // ═══════════════════════════════════════════════════════════════
    [HttpDelete("{id:guid}")]
    [HasPermission(Permissions.{Entities}Write)]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(
        Guid id,
        CancellationToken cancellationToken)
    {
        var command = new Delete{Entity}Command(id);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return result.Error.Code.Contains("NotFound")
                ? NotFound(result.Error)
                : BadRequest(result.Error);
        }

        return NoContent();
    }
}
```

---

## Template: Request DTOs

```csharp
// src/{name}.api/Controllers/{Feature}/RequestCreate{Entity}.cs
namespace {name}.api.Controllers.{Feature};

public sealed class RequestCreate{Entity}
{
    public required string Name { get; init; }
    public string? Description { get; init; }
    public Guid OrganizationId { get; init; }
}

// src/{name}.api/Controllers/{Feature}/RequestUpdate{Entity}.cs
public sealed class RequestUpdate{Entity}
{
    public required string Name { get; init; }
    public string? Description { get; init; }
}

// src/{name}.api/Controllers/{Feature}/RequestPatch{Entity}.cs
public sealed class RequestPatch{Entity}
{
    public string? Name { get; init; }
    public string? Description { get; init; }
    public bool? IsActive { get; init; }
}
```

---

## Template: Controller with Complex Operations

```csharp
// src/{name}.api/Controllers/{Feature}/{Entity}Controller.cs
[Authorize]
[ApiController]
[ApiVersion(ApiVersions.V1)]
[Route("api/v{version:apiVersion}/{entities}")]
public class {Entity}Controller : ControllerBase
{
    private readonly ISender _sender;
    private readonly IConfiguration _configuration;

    public {Entity}Controller(ISender sender, IConfiguration configuration)
    {
        _sender = sender;
        _configuration = configuration;
    }

    // ═══════════════════════════════════════════════════════════════
    // POST: api/v1/{entities}/batch
    // ═══════════════════════════════════════════════════════════════
    [HttpPost("batch")]
    [HasPermission(Permissions.{Entities}Write)]
    public async Task<IActionResult> CreateBatch(
        [FromBody] RequestCreateBatch{Entity} request,
        CancellationToken cancellationToken)
    {
        var command = new CreateBatch{Entity}Command(request);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return BadRequest(result.Error);
        }

        return Ok(result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // POST: api/v1/{entities}/{id}/activate
    // ═══════════════════════════════════════════════════════════════
    [HttpPost("{id:guid}/activate")]
    [HasPermission(Permissions.{Entities}Write)]
    public async Task<IActionResult> Activate(
        Guid id,
        CancellationToken cancellationToken)
    {
        var command = new Activate{Entity}Command(id);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return BadRequest(result.Error);
        }

        return Ok();
    }

    // ═══════════════════════════════════════════════════════════════
    // POST: api/v1/{entities}/{id}/deactivate
    // ═══════════════════════════════════════════════════════════════
    [HttpPost("{id:guid}/deactivate")]
    [HasPermission(Permissions.{Entities}Write)]
    public async Task<IActionResult> Deactivate(
        Guid id,
        CancellationToken cancellationToken)
    {
        var command = new Deactivate{Entity}Command(id);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return BadRequest(result.Error);
        }

        return Ok();
    }

    // ═══════════════════════════════════════════════════════════════
    // GET: api/v1/{entities}/search
    // ═══════════════════════════════════════════════════════════════
    [HttpGet("search")]
    public async Task<IActionResult> Search(
        [FromQuery] string? term,
        [FromQuery] int pageNumber = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken cancellationToken = default)
    {
        var query = new Search{Entities}Query(term, pageNumber, pageSize);

        var result = await _sender.Send(query, cancellationToken);

        return Ok(result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // POST: api/v1/{entities}/{parentId}/children
    // ═══════════════════════════════════════════════════════════════
    [HttpPost("{parentId:guid}/children")]
    [HasPermission(Permissions.{Entities}Write)]
    public async Task<IActionResult> AddChild(
        Guid parentId,
        [FromBody] RequestAddChild request,
        CancellationToken cancellationToken)
    {
        var command = new AddChildCommand(parentId, request.Name, request.SortOrder);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return BadRequest(result.Error);
        }

        return Created($"api/v1/{entities}/{parentId}/children/{result.Value}", result.Value);
    }

    // ═══════════════════════════════════════════════════════════════
    // DELETE: api/v1/{entities}/{parentId}/children/{childId}
    // ═══════════════════════════════════════════════════════════════
    [HttpDelete("{parentId:guid}/children/{childId:guid}")]
    [HasPermission(Permissions.{Entities}Write)]
    public async Task<IActionResult> RemoveChild(
        Guid parentId,
        Guid childId,
        CancellationToken cancellationToken)
    {
        var command = new RemoveChildCommand(parentId, childId);

        var result = await _sender.Send(command, cancellationToken);

        if (result.IsFailure)
        {
            return BadRequest(result.Error);
        }

        return NoContent();
    }
}
```

---

## Template: Controller with Role-Based Authorization

```csharp
// src/{name}.api/Controllers/{Feature}/{Entity}Controller.cs
[Authorize]
[ApiController]
[ApiVersion(ApiVersions.V1)]
[Route("api/v{version:apiVersion}/{entities}")]
public class {Entity}Controller : ControllerBase
{
    private readonly ISender _sender;

    public {Entity}Controller(ISender sender)
    {
        _sender = sender;
    }

    // Public endpoint (no specific role required, just authenticated)
    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetById(Guid id, CancellationToken ct)
    {
        // ...
    }

    // Multiple roles allowed
    [HttpPost]
    [Authorize(Roles = Roles.SuperAdmin + "," + Roles.Manager)]
    public async Task<IActionResult> Create(
        [FromBody] RequestCreate{Entity} request,
        CancellationToken ct)
    {
        // ...
    }

    // Only super admin
    [HttpDelete("{id:guid}")]
    [Authorize(Roles = Roles.SuperAdmin)]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct)
    {
        // ...
    }

    // Permission-based (custom attribute)
    [HttpPut("{id:guid}")]
    [HasPermission(Permissions.{Entities}Write)]
    public async Task<IActionResult> Update(
        Guid id,
        [FromBody] RequestUpdate{Entity} request,
        CancellationToken ct)
    {
        // ...
    }

    // Anonymous endpoint
    [HttpGet("public")]
    [AllowAnonymous]
    public async Task<IActionResult> GetPublicData(CancellationToken ct)
    {
        // ...
    }
}
```

---

## API Versioning Setup

```csharp
// src/{name}.api/ApiVersions.cs
namespace {name}.api;

public static class ApiVersions
{
    public const string V1 = "1.0";
    public const string V2 = "2.0";
}

// src/{name}.infrastructure/DependencyInjection.cs
private static void AddApiVersioning(IServiceCollection services)
{
    services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1);
        options.ReportApiVersions = true;
        options.ApiVersionReader = new UrlSegmentApiVersionReader();
        options.AssumeDefaultVersionWhenUnspecified = true;
    })
    .AddMvc();
}
```

---

## Permission-Based Authorization

```csharp
// src/{name}.infrastructure/Authorization/Permissions.cs
namespace {name}.infrastructure.authorization;

public static class Permissions
{
    // Organizations
    public const string OrganizationsRead = "organizations:read";
    public const string OrganizationsWrite = "organizations:write";

    // Users
    public const string UsersRead = "users:read";
    public const string UsersWrite = "users:write";

    // {Entities}
    public const string {Entities}Read = "{entities}:read";
    public const string {Entities}Write = "{entities}:write";
}

// src/{name}.infrastructure/Authorization/Roles.cs
namespace {name}.infrastructure.authorization;

public static class Roles
{
    public const string SuperAdmin = "SuperAdmin";
    public const string Admin = "Admin";
    public const string Manager = "Manager";
    public const string Consultant = "Consultant";
    public const string Associate = "Associate";
}

// src/{name}.infrastructure/Authorization/HasPermissionAttribute.cs
using Microsoft.AspNetCore.Authorization;

namespace {name}.infrastructure.authorization;

public sealed class HasPermissionAttribute : AuthorizeAttribute
{
    public HasPermissionAttribute(string permission) : base(permission)
    {
    }
}
```

---

## Global Error Handling

```csharp
// src/{name}.api/Middleware/ExceptionHandlingMiddleware.cs
using {name}.application.exceptions;
using Microsoft.AspNetCore.Mvc;

namespace {name}.api.Middleware;

public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(
        RequestDelegate next,
        ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception exception)
        {
            _logger.LogError(exception, "Exception occurred: {Message}", exception.Message);

            var problemDetails = CreateProblemDetails(exception);

            context.Response.StatusCode = problemDetails.Status ?? 500;
            await context.Response.WriteAsJsonAsync(problemDetails);
        }
    }

    private static ProblemDetails CreateProblemDetails(Exception exception)
    {
        return exception switch
        {
            ValidationException validationException => new ProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Validation Error",
                Detail = "One or more validation errors occurred.",
                Extensions = { ["errors"] = validationException.Errors }
            },
            ConcurrencyException => new ProblemDetails
            {
                Status = StatusCodes.Status409Conflict,
                Title = "Concurrency Error",
                Detail = "The record was modified by another user."
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Server Error",
                Detail = "An unexpected error occurred."
            }
        };
    }
}

// Extension method
public static class ExceptionHandlingMiddlewareExtensions
{
    public static IApplicationBuilder UseCustomExceptionHandler(
        this IApplicationBuilder app)
    {
        return app.UseMiddleware<ExceptionHandlingMiddleware>();
    }
}
```

---

## REST Conventions

| Operation | HTTP Method | URL | Success Code | Failure Codes |
|-----------|-------------|-----|--------------|---------------|
| Get one | GET | `/{entities}/{id}` | 200 | 404 |
| Get all | GET | `/{entities}` | 200 | - |
| Get filtered | GET | `/{entities}?filter=x` | 200 | - |
| Get children | GET | `/{entities}/{id}/children` | 200 | 404 |
| Create | POST | `/{entities}` | 201 | 400 |
| Full update | PUT | `/{entities}/{id}` | 200 | 400, 404 |
| Partial update | PATCH | `/{entities}/{id}` | 200 | 400, 404 |
| Delete | DELETE | `/{entities}/{id}` | 204 | 400, 404 |
| Action | POST | `/{entities}/{id}/action` | 200 | 400, 404 |

---

## Critical Rules

1. **Inject ISender, not IMediator** - Only send, don't publish
2. **Use CancellationToken** - Pass to all async operations
3. **Return appropriate status codes** - 201 for create, 204 for delete
4. **Use CreatedAtAction for POST** - Returns location header
5. **DTOs in API layer** - Don't expose application layer DTOs directly
6. **Route constraints** - `{id:guid}` for type safety
7. **Authorize by default** - `[Authorize]` on controller
8. **API versioning** - Support multiple versions
9. **ProducesResponseType** - Document possible responses
10. **Don't catch exceptions** - Let middleware handle

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Business logic in controller
[HttpPost]
public async Task<IActionResult> Create([FromBody] Request request)
{
    if (await _repository.ExistsAsync(request.Name))
        return BadRequest("Already exists");  // Logic belongs in handler!
    
    var entity = new Entity { Name = request.Name };
    _repository.Add(entity);
    await _unitOfWork.SaveChangesAsync();
    return Ok(entity.Id);
}

// ✅ CORRECT: Controller only orchestrates
[HttpPost]
public async Task<IActionResult> Create([FromBody] Request request, CancellationToken ct)
{
    var command = new CreateCommand(request.Name);
    var result = await _sender.Send(command, ct);
    
    return result.IsFailure 
        ? BadRequest(result.Error) 
        : CreatedAtAction(nameof(GetById), new { id = result.Value }, result.Value);
}

// ❌ WRONG: Returning domain entities
[HttpGet("{id}")]
public async Task<User> GetById(Guid id)  // Exposes domain!

// ✅ CORRECT: Return DTOs
[HttpGet("{id}")]
public async Task<IActionResult> GetById(Guid id, CancellationToken ct)
{
    var result = await _sender.Send(new GetQuery(id), ct);
    return result.IsFailure ? NotFound(result.Error) : Ok(result.Value);
}

// ❌ WRONG: Catching and wrapping exceptions
try { ... }
catch (Exception ex)
{
    return StatusCode(500, ex.Message);
}

// ✅ CORRECT: Let middleware handle exceptions
// No try-catch, middleware handles it globally
```

---

## Related Skills

- `cqrs-command-generator` - Generate commands for controllers
- `cqrs-query-generator` - Generate queries for controllers
- `dotnet-clean-architecture` - Overall project structure
- `result-pattern` - Handle command/query results
