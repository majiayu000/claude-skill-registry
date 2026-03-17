---
name: api-design
description: Use when designing or modifying REST API endpoints, controller structure, route patterns, request/response DTOs. Triggers on keywords like "API endpoint", "REST", "controller", "route", "HTTP", "request body", "response".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
infer: true
---

# REST API Design

Expert API design agent for EasyPlatform following platform patterns and REST best practices.

## Controller Pattern

```csharp
[ApiController]
[Route("api/[controller]")]
[PlatformAuthorize]  // Require authentication
public class EmployeeController : PlatformBaseController
{
    // GET api/employee - List with filtering
    [HttpGet]
    public async Task<IActionResult> GetList([FromQuery] GetEmployeeListQuery query)
        => Ok(await Cqrs.SendAsync(query));

    // GET api/employee/{id} - Single by ID
    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(string id)
        => Ok(await Cqrs.SendAsync(new GetEmployeeByIdQuery { Id = id }));

    // POST api/employee - Create/Update
    [HttpPost]
    [PlatformAuthorize(Roles = "Admin,Manager")]
    public async Task<IActionResult> Save([FromBody] SaveEmployeeCommand command)
        => Ok(await Cqrs.SendAsync(command));

    // DELETE api/employee/{id} - Delete
    [HttpDelete("{id}")]
    [PlatformAuthorize(Roles = "Admin")]
    public async Task<IActionResult> Delete(string id)
        => Ok(await Cqrs.SendAsync(new DeleteEmployeeCommand { Id = id }));

    // POST api/employee/search - Complex search
    [HttpPost("search")]
    public async Task<IActionResult> Search([FromBody] SearchEmployeesQuery query)
        => Ok(await Cqrs.SendAsync(query));

    // POST api/employee/{id}/action - Custom action
    [HttpPost("{id}/activate")]
    public async Task<IActionResult> Activate(string id)
        => Ok(await Cqrs.SendAsync(new ActivateEmployeeCommand { Id = id }));
}
```

## Route Naming Conventions

| Action          | HTTP Method | Route Pattern                   | Example                            |
| --------------- | ----------- | ------------------------------- | ---------------------------------- |
| List            | GET         | `/api/{resource}`               | `GET /api/employees`               |
| Get by ID       | GET         | `/api/{resource}/{id}`          | `GET /api/employees/123`           |
| Create/Update   | POST        | `/api/{resource}`               | `POST /api/employees`              |
| Delete          | DELETE      | `/api/{resource}/{id}`          | `DELETE /api/employees/123`        |
| Complex Search  | POST        | `/api/{resource}/search`        | `POST /api/employees/search`       |
| Custom Action   | POST        | `/api/{resource}/{id}/{action}` | `POST /api/employees/123/activate` |
| Nested Resource | GET         | `/api/{parent}/{id}/{child}`    | `GET /api/departments/1/employees` |

## Request/Response DTOs

### Query DTO (GET requests)

```csharp
// Simple query params - use record
public record GetEmployeeListQuery : PlatformCqrsPagedQuery<GetEmployeeListQueryResult, EmployeeDto>
{
    public List<EmploymentStatus>? Statuses { get; init; }
    public string? SearchText { get; init; }
    public string? DepartmentId { get; init; }
}
```

### Command DTO (POST/PUT/DELETE)

```csharp
public sealed class SaveEmployeeCommand : PlatformCqrsCommand<SaveEmployeeCommandResult>
{
    public string? Id { get; set; }  // Null for create
    public string FirstName { get; set; } = string.Empty;
    public string LastName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;

    public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
    {
        return base.Validate()
            .And(_ => FirstName.IsNotNullOrEmpty(), "FirstName is required")
            .And(_ => Email.IsNotNullOrEmpty(), "Email is required")
            .And(_ => Email.Contains("@"), "Invalid email format");
    }
}
```

### Response DTO

```csharp
// For single entity
public sealed class SaveEmployeeCommandResult : PlatformCqrsCommandResult
{
    public EmployeeDto Entity { get; set; } = null!;
}

// For paged list
public sealed class GetEmployeeListQueryResult : PlatformCqrsPagedQueryResult<EmployeeDto>
{
    public Dictionary<EmploymentStatus, int> StatusCounts { get; set; } = new();

    public GetEmployeeListQueryResult(List<Employee> items, int total, GetEmployeeListQuery req, Dictionary<EmploymentStatus, int> counts)
        : base(items.SelectList(e => new EmployeeDto(e)), total, req)
    {
        StatusCounts = counts;
    }
}
```

## Authorization Patterns

```csharp
// Controller level - all endpoints
[PlatformAuthorize]
public class SecureController : PlatformBaseController { }

// Endpoint level - specific roles
[HttpPost]
[PlatformAuthorize(Roles = "Admin,Manager")]
public async Task<IActionResult> AdminOnly() { }

// Handler level - business validation
protected override async Task<PlatformValidationResult<T>> ValidateRequestAsync(...)
{
    return await validation
        .And(_ => RequestContext.HasRole("Admin") || RequestContext.UserId() == req.TargetUserId,
            "Can only modify own data or be Admin");
}
```

## File Upload Endpoints

```csharp
[HttpPost("upload")]
[RequestSizeLimit(50 * 1024 * 1024)]  // 50MB
public async Task<IActionResult> Upload([FromForm] UploadCommand command)
    => Ok(await Cqrs.SendAsync(command));

public sealed class UploadCommand : PlatformCqrsCommand<UploadCommandResult>
{
    [FromForm]
    public IFormFile File { get; set; } = null!;

    [FromForm]
    public string? Description { get; set; }
}
```

## Error Response Format

```csharp
// Platform handles errors automatically with standard format
{
    "type": "validation",
    "title": "Validation Error",
    "status": 400,
    "errors": {
        "email": ["Email is required", "Invalid email format"],
        "firstName": ["FirstName is required"]
    }
}

// Business errors
{
    "type": "business",
    "title": "Business Rule Violation",
    "status": 422,
    "detail": "Employee is already assigned to this department"
}
```

## API Design Checklist

- [ ] RESTful route naming (plural nouns, lowercase)?
- [ ] Appropriate HTTP methods?
- [ ] Proper authorization attributes?
- [ ] Validation in Command/Query Validate()?
- [ ] Consistent response format?
- [ ] Paging for list endpoints?
- [ ] Error handling follows platform patterns?

## Anti-Patterns

- **Verbs in URLs**: Use `/employees/123/activate` not `/activateEmployee`
- **Missing Authorization**: Always add `[PlatformAuthorize]`
- **Validation in Controller**: Move to Command/Query `Validate()`
- **Business Logic in Controller**: Keep controllers thin, logic in handlers
- **Inconsistent Naming**: Follow `{Resource}Controller` pattern
