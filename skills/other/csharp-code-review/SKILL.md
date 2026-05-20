---
name: csharp-code-review
description: Master C# and .NET code review patterns including async/await, LINQ optimization, dependency injection, Entity Framework, and null safety. Use PROACTIVELY when reviewing C#/.NET PRs.
---

# C#/.NET Code Review

Comprehensive code review checklist and patterns for C# and .NET applications, focusing on async patterns, LINQ, DI, EF Core, and modern C# features.

## When to Use This Skill

- Reviewing C# and .NET pull requests
- Establishing .NET code review standards
- Training reviewers on C#-specific issues
- Catching async/await bugs and EF Core issues
- Ensuring proper dependency injection patterns

## Quick Checklist

```markdown
## C#/.NET Review Checklist

- [ ] async/await all the way (no .Result or .Wait())
- [ ] IDisposable properly disposed (using statement)
- [ ] Null checks with null-conditional operators
- [ ] LINQ optimized (no multiple enumeration)
- [ ] EF Core: AsNoTracking for read-only, Include for eager loading
- [ ] DI lifetime scopes correct (Scoped vs Singleton)
- [ ] ConfigureAwait(false) in library code
- [ ] Proper exception handling with filters
```

## Review Severity Labels

```
🔴 [blocking]  - Must fix before merge (bugs, security, breaking)
🟡 [important] - Should fix, but discuss if you disagree
🟢 [nit]       - Nice to have, not blocking
💡 [suggestion]- Alternative approach to consider
```

---

## Async/Await Issues

### Blocking on Async - Deadlock Risk

```csharp
// ❌ Blocking on async - DEADLOCK RISK in ASP.NET!
public User GetUser(int id)
{
    return GetUserAsync(id).Result;  // Deadlock!
}

public User GetUserAlt(int id)
{
    return GetUserAsync(id).GetAwaiter().GetResult();  // Still bad!
}

// ✅ Async all the way
public async Task<User> GetUserAsync(int id)
{
    return await _repository.GetByIdAsync(id);
}
```

### async void - Unobserved Exceptions

```csharp
// ❌ async void - Exceptions cannot be caught!
public async void SaveData(Data data)
{
    await _repository.SaveAsync(data);  // If this throws, app may crash!
}

// ❌ Also problematic in event handlers
button.Click += async void (sender, e) =>
{
    await DoWorkAsync();  // Exception crashes app!
};

// ✅ async Task for async methods
public async Task SaveDataAsync(Data data)
{
    await _repository.SaveAsync(data);
}

// ✅ For event handlers, wrap in try-catch
button.Click += async (sender, e) =>
{
    try
    {
        await DoWorkAsync();
    }
    catch (Exception ex)
    {
        Logger.Error(ex);
    }
};
```

### Missing ConfigureAwait in Libraries

```csharp
// ❌ Missing ConfigureAwait in library code
// Can cause deadlocks when called from UI thread
public async Task<Data> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url);  // Captures context
    return await response.Content.ReadFromJsonAsync<Data>();
}

// ✅ ConfigureAwait(false) in library code
public async Task<Data> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url).ConfigureAwait(false);
    return await response.Content.ReadFromJsonAsync<Data>().ConfigureAwait(false);
}
```

### Sequential When Parallel Possible

```csharp
// ❌ Sequential when parallel is possible
public async Task<UserData> GetUserDataAsync(int userId)
{
    var profile = await GetProfileAsync(userId);
    var posts = await GetPostsAsync(userId);      // Waits for profile!
    var followers = await GetFollowersAsync(userId);  // Waits for posts!

    return new UserData(profile, posts, followers);
}

// ✅ Parallel execution with Task.WhenAll
public async Task<UserData> GetUserDataAsync(int userId)
{
    var profileTask = GetProfileAsync(userId);
    var postsTask = GetPostsAsync(userId);
    var followersTask = GetFollowersAsync(userId);

    await Task.WhenAll(profileTask, postsTask, followersTask);

    return new UserData(
        profileTask.Result,  // Safe - task completed
        postsTask.Result,
        followersTask.Result
    );
}
```

### Using ValueTask Incorrectly

```csharp
// ❌ Awaiting ValueTask multiple times
public async Task ProcessAsync()
{
    ValueTask<int> valueTask = GetValueAsync();

    var result1 = await valueTask;
    var result2 = await valueTask;  // WRONG! Can't await twice!
}

// ✅ Await once or convert to Task
public async Task ProcessAsync()
{
    // Option 1: Await once
    var result = await GetValueAsync();

    // Option 2: Convert to Task if multiple awaits needed
    var task = GetValueAsync().AsTask();
    var result1 = await task;
    var result2 = await task;  // OK now
}
```

---

## LINQ Issues

### Multiple Enumeration

```csharp
// ❌ Multiple enumeration - performance problem
public void ProcessUsers(IEnumerable<User> users)
{
    if (!users.Any()) return;           // First enumeration

    var count = users.Count();          // Second enumeration

    foreach (var user in users) { }     // Third enumeration!
}

// ✅ Materialize once
public void ProcessUsers(IEnumerable<User> users)
{
    var userList = users.ToList();  // Materialize once

    if (userList.Count == 0) return;

    foreach (var user in userList) { }
}
```

### N+1 Query Problem

```csharp
// ❌ N+1 queries - one query per order!
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    var customer = await _context.Customers
        .FirstAsync(c => c.Id == order.CustomerId);  // Query per order!
    order.CustomerName = customer.Name;
}

// ✅ Eager loading with Include
var orders = await _context.Orders
    .Include(o => o.Customer)  // Single query with JOIN
    .ToListAsync();

foreach (var order in orders)
{
    order.CustomerName = order.Customer.Name;  // Already loaded!
}
```

### Loading Too Much Data

```csharp
// ❌ Loading entire entity for few fields
var users = await _context.Users
    .Where(u => u.Active)
    .ToListAsync();  // Loads ALL columns

var names = users.Select(u => u.Name).ToList();

// ✅ Project to only needed fields
var names = await _context.Users
    .Where(u => u.Active)
    .Select(u => u.Name)  // Only fetch Name column
    .ToListAsync();
```

### Deferred Execution Surprise

```csharp
// ❌ Deferred execution in returned IEnumerable
public IEnumerable<User> GetActiveUsers()
{
    using var context = new AppDbContext();
    return context.Users.Where(u => u.Active);  // Not materialized!
}  // Context disposed before enumeration!

// ✅ Materialize before returning
public IEnumerable<User> GetActiveUsers()
{
    using var context = new AppDbContext();
    return context.Users.Where(u => u.Active).ToList();  // Materialized
}

// ✅ Or use async pattern
public async Task<List<User>> GetActiveUsersAsync()
{
    await using var context = new AppDbContext();
    return await context.Users.Where(u => u.Active).ToListAsync();
}
```

### Client vs Server Evaluation

```csharp
// ❌ Forces client evaluation - loads all data then filters
var users = await _context.Users
    .Where(u => MyCustomMethod(u.Name))  // Can't translate to SQL!
    .ToListAsync();

// ✅ Use SQL-translatable expressions
var users = await _context.Users
    .Where(u => u.Name.StartsWith("A"))  // Translates to SQL LIKE
    .ToListAsync();

// If custom logic needed, filter on server first
var users = await _context.Users
    .Where(u => u.Active)  // Server-side filter
    .ToListAsync();

var filtered = users.Where(u => MyCustomMethod(u.Name));  // Client-side
```

---

## Dependency Injection Issues

### Captive Dependency

```csharp
// ❌ Captive dependency - Scoped injected into Singleton
services.AddSingleton<MySingleton>();
services.AddScoped<MyScopedService>();

public class MySingleton
{
    private readonly MyScopedService _scoped;  // WRONG! Scoped in Singleton!

    public MySingleton(MyScopedService scoped)
    {
        _scoped = scoped;  // This instance lives forever, never refreshed!
    }
}

// ✅ Use IServiceScopeFactory for scoped in singletons
public class MySingleton
{
    private readonly IServiceScopeFactory _scopeFactory;

    public MySingleton(IServiceScopeFactory scopeFactory)
    {
        _scopeFactory = scopeFactory;
    }

    public void DoWork()
    {
        using var scope = _scopeFactory.CreateScope();
        var scoped = scope.ServiceProvider.GetRequiredService<MyScopedService>();
        scoped.Process();
    }
}
```

### Concrete Dependencies

```csharp
// ❌ Depending on concrete implementation
public class OrderService
{
    private readonly SqlOrderRepository _repository;  // Concrete type!

    public OrderService(SqlOrderRepository repository)
    {
        _repository = repository;
    }
}

// ✅ Depend on abstraction
public class OrderService
{
    private readonly IOrderRepository _repository;

    public OrderService(IOrderRepository repository)
    {
        _repository = repository;
    }
}
```

### Service Locator Anti-Pattern

```csharp
// ❌ Service locator - hides dependencies
public class OrderProcessor
{
    public void Process(Order order)
    {
        var logger = ServiceLocator.Get<ILogger>();  // Hidden dependency!
        var repository = ServiceLocator.Get<IOrderRepository>();
        // ...
    }
}

// ✅ Constructor injection - explicit dependencies
public class OrderProcessor
{
    private readonly ILogger _logger;
    private readonly IOrderRepository _repository;

    public OrderProcessor(ILogger logger, IOrderRepository repository)
    {
        _logger = logger;
        _repository = repository;
    }

    public void Process(Order order)
    {
        // Dependencies are clear and testable
    }
}
```

---

## Null Safety

### Null-Conditional Operators

```csharp
// ❌ Multiple null checks
if (user != null && user.Address != null && user.Address.City != null)
{
    var city = user.Address.City;
}

// ✅ Null-conditional operator
var city = user?.Address?.City;
```

### Null-Coalescing Operators

```csharp
// ❌ Verbose null check
string name;
if (user.Name != null)
{
    name = user.Name;
}
else
{
    name = "Unknown";
}

// ✅ Null-coalescing
var name = user.Name ?? "Unknown";

// ✅ Null-coalescing assignment
user.Name ??= "Unknown";  // Only assigns if null
```

### ArgumentNullException

```csharp
// ❌ Verbose null check
public void Process(User user)
{
    if (user == null)
    {
        throw new ArgumentNullException(nameof(user));
    }
}

// ✅ Use ThrowIfNull (C# 10+)
public void Process(User user)
{
    ArgumentNullException.ThrowIfNull(user);
}
```

### Null-Forgiving Without Validation

```csharp
// ❌ Null-forgiving without validation
public string GetName(User? user)
{
    return user!.Name;  // Could throw NullReferenceException!
}

// ✅ Validate before using
public string GetName(User? user)
{
    ArgumentNullException.ThrowIfNull(user);
    return user.Name;  // TypeScript knows it's not null now
}
```

---

## Resource Management

### Missing Disposal

```csharp
// ❌ Resource not disposed
public string ReadFile(string path)
{
    var reader = new StreamReader(path);
    return reader.ReadToEnd();  // StreamReader never closed!
}

// ✅ Using statement
public string ReadFile(string path)
{
    using var reader = new StreamReader(path);
    return reader.ReadToEnd();
}  // Automatically disposed
```

### HttpClient Misuse

```csharp
// ❌ Creating HttpClient per request - socket exhaustion!
public async Task<string> GetDataAsync(string url)
{
    using var client = new HttpClient();  // Creates new socket each time!
    return await client.GetStringAsync(url);
}

// ✅ Use IHttpClientFactory
public class MyService
{
    private readonly HttpClient _client;

    public MyService(IHttpClientFactory factory)
    {
        _client = factory.CreateClient("MyApi");
    }

    public async Task<string> GetDataAsync(string url)
    {
        return await _client.GetStringAsync(url);
    }
}
```

---

## Modern C# Features

### Pattern Matching

```csharp
// ❌ Type checking with casting
if (shape.GetType() == typeof(Circle))
{
    var circle = (Circle)shape;
    return circle.Radius * circle.Radius * Math.PI;
}

// ✅ Pattern matching
if (shape is Circle circle)
{
    return circle.Radius * circle.Radius * Math.PI;
}

// ✅ Switch expression
var area = shape switch
{
    Circle c => c.Radius * c.Radius * Math.PI,
    Rectangle r => r.Width * r.Height,
    Triangle t => t.Base * t.Height / 2,
    _ => throw new ArgumentException("Unknown shape")
};
```

### Records for DTOs

```csharp
// ❌ Verbose DTO class
public class UserDto
{
    public int Id { get; init; }
    public string Name { get; init; }
    public string Email { get; init; }

    // Need to implement Equals, GetHashCode, ToString...
}

// ✅ Record (C# 9+)
public record UserDto(int Id, string Name, string Email);

// Immutable with value equality built-in
// Easy with-expression: var updated = dto with { Name = "New Name" };
```

### Primary Constructors (C# 12)

```csharp
// ❌ Verbose class with constructor
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly ILogger<UserService> _logger;

    public UserService(IUserRepository repository, ILogger<UserService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
}

// ✅ Primary constructor (C# 12)
public class UserService(IUserRepository repository, ILogger<UserService> logger)
{
    public async Task<User> GetUserAsync(int id)
    {
        logger.LogInformation("Getting user {Id}", id);
        return await repository.GetByIdAsync(id);
    }
}
```

---

## EF Core Best Practices

### AsNoTracking for Read-Only

```csharp
// ❌ Tracking when not needed
var users = await _context.Users
    .Where(u => u.Active)
    .ToListAsync();  // Tracking enabled - overhead

// ✅ AsNoTracking for read-only queries
var users = await _context.Users
    .AsNoTracking()  // No change tracking overhead
    .Where(u => u.Active)
    .ToListAsync();
```

### Explicit Loading When Needed

```csharp
// ✅ Load related data only when needed
var order = await _context.Orders.FindAsync(orderId);

if (needsCustomerInfo)
{
    await _context.Entry(order)
        .Reference(o => o.Customer)
        .LoadAsync();
}
```

---

## Common Pitfalls

| Pitfall              | Problem               | Solution                    |
| -------------------- | --------------------- | --------------------------- |
| `.Result` on async   | Deadlock              | `await` all the way         |
| `async void`         | Unobserved exceptions | Use `async Task`            |
| Multiple enumeration | Performance           | Materialize with `ToList()` |
| N+1 queries          | Many DB roundtrips    | Use `Include()`             |
| Captive dependency   | Stale scoped services | Use `IServiceScopeFactory`  |
| Missing `using`      | Resource leak         | Always dispose IDisposable  |
| New `HttpClient`     | Socket exhaustion     | Use `IHttpClientFactory`    |

## Best Practices Summary

1. **Async All The Way** - Never block on async
2. **async Task** - Never `async void` except event handlers
3. **ConfigureAwait(false)** - In library code
4. **Materialize Once** - `ToList()` before multiple operations
5. **Include() Eagerly** - Avoid N+1 queries
6. **AsNoTracking()** - For read-only queries
7. **Dispose Resources** - `using` for IDisposable
8. **Use Modern C#** - Records, pattern matching, primary constructors


## Parent Hub
- [_backend-mastery](../_backend-mastery/SKILL.md)


## Part of Workflow
This skill is utilized in the following sequential workflows:
- [_workflow-feature-lifecycle](../_workflow-feature-lifecycle/SKILL.md)
