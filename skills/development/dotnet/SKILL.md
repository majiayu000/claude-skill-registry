---
name: dotnet
description: Guidelines for .NET backend development with C#, ASP.NET Core, and Entity Framework Core
---

# .NET Development Guidelines

You are an expert in .NET backend development with deep knowledge of C#, ASP.NET Core, Entity Framework Core, and modern .NET practices.

## Code Style and Structure

- Write concise, idiomatic C# code with accurate examples
- Follow .NET conventions and best practices
- Use object-oriented programming with proper encapsulation
- Prefer LINQ for collection operations
- Structure code according to Clean Architecture principles

## Project Structure

```
src/
  Domain/           # Entities, value objects, domain logic
  Application/      # Use cases, DTOs, interfaces
  Infrastructure/   # Data access, external services
  WebApi/          # Controllers, middleware, configuration
tests/
  UnitTests/
  IntegrationTests/
```

## RESTful API Design

- Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Return appropriate status codes
- Use plural nouns for resource endpoints
- Implement proper pagination for collections
- Use query parameters for filtering and sorting
- Version APIs (URL path or header)

```csharp
[ApiController]
[Route("api/v1/[controller]")]
public class UsersController : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers([FromQuery] PaginationParams pagination)

    [HttpGet("{id}")]
    public async Task<ActionResult<UserDto>> GetUser(int id)

    [HttpPost]
    public async Task<ActionResult<UserDto>> CreateUser(CreateUserDto dto)
}
```

## Async/Await Patterns

- Use `async/await` for all I/O-bound operations
- Suffix async methods with `Async`
- Don't block on async code (avoid `.Result` and `.Wait()`)
- Use `CancellationToken` for cancellation support
- Prefer `ValueTask` for frequently-called methods

## Entity Framework Core

### Configuration
- Use Fluent API for entity configuration
- Configure relationships explicitly
- Use migrations for schema changes
- Enable nullable reference types

### Best Practices
- Use `AsNoTracking()` for read-only queries
- Implement the Repository pattern for data access
- Use Include/ThenInclude for eager loading
- Avoid N+1 query problems
- Use projections for optimized queries

```csharp
public async Task<IEnumerable<UserDto>> GetUsersAsync()
{
    return await _context.Users
        .AsNoTracking()
        .Select(u => new UserDto
        {
            Id = u.Id,
            Name = u.Name
        })
        .ToListAsync();
}
```

## Dependency Injection

- Use constructor injection
- Register services in `Program.cs`
- Use appropriate lifetimes (Scoped, Transient, Singleton)
- Create interfaces for service abstractions
- Use Options pattern for configuration

```csharp
builder.Services.AddScoped<IUserService, UserService>();
builder.Services.Configure<JwtSettings>(builder.Configuration.GetSection("Jwt"));
```

## Caching

- Use IMemoryCache for in-memory caching
- Use IDistributedCache for distributed scenarios
- Implement cache invalidation strategies
- Use response caching for HTTP responses
- Consider Redis for production caching

## Validation

- Use FluentValidation for complex validation
- Use Data Annotations for simple validation
- Validate early in the request pipeline
- Return detailed validation errors
- Implement model state validation

## Error Handling

- Use global exception handling middleware
- Create custom exception types
- Return consistent error responses
- Log exceptions with context
- Don't expose internal details

## Security

### Authentication
- Use JWT tokens for API authentication
- Implement refresh token rotation
- Store tokens securely
- Use ASP.NET Core Identity when appropriate

### Authorization
- Use policy-based authorization
- Implement resource-based authorization
- Apply `[Authorize]` attributes appropriately
- Use claims for fine-grained permissions

## Testing

- Write unit tests with xUnit
- Use Moq for mocking dependencies
- Write integration tests with WebApplicationFactory
- Test API endpoints end-to-end
- Use in-memory database for testing

## Documentation

- Use Swagger/OpenAPI for API documentation
- Document all endpoints with XML comments
- Include request/response examples
- Generate client SDKs from OpenAPI spec
