---
name: developing-csharp
description: Use when working with .cs files, .NET projects, implementing C# features, advising on C#/.NET architecture and patterns, or answering questions about C#/.NET development. Covers async patterns, dependency injection, LINQ, and testing conventions.
---

# C# Development

Apply these patterns when working with C# code. When both developing-csharp and testing-xunit apply, testing-xunit takes precedence in test files.

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes, Structs | PascalCase | `UserService` |
| Interfaces | IPascalCase | `IUserRepository` |
| Methods, Properties | PascalCase | `GetUserById` |
| Private fields | _camelCase | `_userRepository` |
| Parameters, locals | camelCase | `userId` |
| Async methods | PascalCase + Async | `GetUserByIdAsync` |

## Project Structure

```
src/
├── MyApp.Api/Controllers/
├── MyApp.Core/Entities/, Interfaces/, Services/
├── MyApp.Infrastructure/Repositories/, Data/
tests/
├── MyApp.UnitTests/
├── MyApp.IntegrationTests/
```

## Dependency Injection

Register services in Program.cs:

```csharp
builder.Services.AddScoped<IUserRepository, UserRepository>();
builder.Services.AddSingleton<ICacheService, RedisCacheService>();
builder.Services.AddTransient<IEmailSender, SmtpEmailSender>();
```

| Lifetime | Use For |
|----------|---------|
| Singleton | Shared state, caches, configuration |
| Scoped | Per-request state, DbContext, repositories |
| Transient | Stateless services, lightweight operations |

Inject via constructor:

```csharp
public class UserService : IUserService
{
    private readonly IUserRepository _userRepository;
    private readonly ILogger<UserService> _logger;

    public UserService(IUserRepository userRepository, ILogger<UserService> logger)
    {
        _userRepository = userRepository;
        _logger = logger;
    }
}
```

## Async/Await

Always use `Async` suffix. Always await or return the task. Use `ConfigureAwait(false)` in libraries. Support `CancellationToken`.

```csharp
public async Task<User> GetUserAsync(int id, CancellationToken ct = default)
{
    return await _context.Users.FirstOrDefaultAsync(u => u.Id == id, ct);
}
```

Do not use `async void` except for event handlers. Do not block with `.Result` or `.Wait()`. Do not ignore tasks with `_ = ProcessAsync()`.

## LINQ

Prefer method syntax:

```csharp
var activeUsers = users
    .Where(u => u.IsActive)
    .OrderBy(u => u.LastName)
    .Select(u => new UserDto(u.Id, u.FullName))
    .ToList();
```

Materialize once to avoid multiple enumeration:

```csharp
var activeUsers = users.Where(u => u.IsActive).ToList();
var count = activeUsers.Count;
var first = activeUsers.First();
```

## Error Handling

Use custom exception hierarchy:

```csharp
public class DomainException : Exception { }
public class NotFoundException : DomainException { }
public class ValidationException : DomainException
{
    public IReadOnlyList<string> Errors { get; }
}
```

Result pattern alternative:

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    public static Result<T> Success(T value) => new(value);
    public static Result<T> Failure(string error) => new(error);
}
```

## Testing with xUnit

```csharp
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepo;
    private readonly UserService _sut;

    public UserServiceTests()
    {
        _mockRepo = new Mock<IUserRepository>();
        _sut = new UserService(_mockRepo.Object);
    }

    [Fact]
    public async Task GetByIdAsync_WithValidId_ReturnsUser()
    {
        var expectedUser = new User { Id = 1, Name = "John" };
        _mockRepo.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(expectedUser);

        var result = await _sut.GetByIdAsync(1);

        Assert.NotNull(result);
        Assert.Equal("John", result.Name);
    }
}
```

## Entity Framework

```csharp
public class AppDbContext : DbContext
{
    public DbSet<User> Users => Set<User>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }
}
```

Avoid the repository pattern with Entity Framework.

## Requirements

1. Use `var` for obvious types
2. Prefer `readonly` fields
3. Use `record` for DTOs: `public record UserDto(int Id, string Name);`
4. Use nullable reference types and null-coalescing operators
5. Use `using` statements for disposable resources
6. Use `""` not `string.Empty`
7. Use collection expressions (C# 12+): `int[] numbers = [1, 2, 3];`
