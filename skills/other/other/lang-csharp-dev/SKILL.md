---
name: lang-csharp-dev
description: Foundational C# patterns covering LINQ, async/await, nullable types, records, and pattern matching. Use when writing C# code or needing guidance on C# features. This is the entry point for C# development.
---

# C# Development Skill

Comprehensive foundational patterns for modern C# development covering language features, best practices, and common idioms.

## Quick Reference

### Essential Patterns
```csharp
// Nullable reference types
string? nullableString = null;
string nonNullableString = "value";

// Records
public record Person(string Name, int Age);

// Pattern matching
var result = value switch
{
    null => "null",
    0 => "zero",
    > 0 => "positive",
    _ => "negative"
};

// LINQ method syntax
var results = collection
    .Where(x => x.IsActive)
    .Select(x => x.Name)
    .OrderBy(x => x)
    .ToList();

// Async/await
public async Task<string> GetDataAsync()
{
    return await httpClient.GetStringAsync(url);
}
```

### File Extensions
- `.cs` - C# source files
- `.csproj` - Project files
- `.sln` - Solution files
- `.cshtml` - Razor views
- `.razor` - Blazor components

## 1. Nullable Reference Types

### Overview
Nullable reference types help prevent null reference exceptions by making nullability explicit in the type system.

### Enabling Nullable Context
```csharp
// In .csproj
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>

// Or per-file
#nullable enable

// Disable warnings
#nullable disable
```

### Nullable Annotations
```csharp
// Nullable reference type
string? nullableString = null;

// Non-nullable reference type (default when nullable context enabled)
string nonNullableString = "value";

// Array of nullable strings
string?[] arrayOfNullableStrings = new string?[10];

// Nullable array of strings
string[]? nullableArrayOfStrings = null;

// Nullable array of nullable strings
string?[]? fullyNullable = null;
```

### Null-Forgiving Operator
```csharp
// When you know a value isn't null but compiler doesn't
string value = GetValue()!;

// Use sparingly - defeats purpose of nullable reference types
public void Process(string? input)
{
    // Bad - suppresses warning without checking
    Console.WriteLine(input!.Length);

    // Good - check first
    if (input is not null)
    {
        Console.WriteLine(input.Length);
    }
}
```

### Null Checking Patterns
```csharp
// Traditional null check
if (value != null)
{
    Console.WriteLine(value.Length);
}

// Pattern matching
if (value is not null)
{
    Console.WriteLine(value.Length);
}

// Null-conditional operator
Console.WriteLine(value?.Length);

// Null-coalescing operator
string result = value ?? "default";

// Null-coalescing assignment
value ??= "default";
```

### Method Annotations
```csharp
// Return nullable
public string? FindUser(int id)
{
    return users.FirstOrDefault(u => u.Id == id)?.Name;
}

// Accept nullable
public void UpdateName(string? newName)
{
    if (newName is null)
    {
        throw new ArgumentNullException(nameof(newName));
    }

    name = newName;
}

// Attributes for advanced scenarios
public bool TryGetValue(string key, [NotNullWhen(true)] out string? value)
{
    // Tells compiler that value is not null when method returns true
    return dictionary.TryGetValue(key, out value);
}

[return: NotNullIfNotNull(nameof(input))]
public string? Transform(string? input)
{
    // Return value nullability matches input nullability
    return input?.ToUpper();
}
```

### Generic Nullability
```csharp
// Nullable value type
public class Container<T>
{
    public T? Value { get; set; }  // Works for both reference and value types
}

// Constrain to non-nullable reference types
public class Container<T> where T : notnull
{
    public T Value { get; set; } = default!;
}

// Nullable reference type constraint
public class Container<T> where T : class?
{
    public T? Value { get; set; }
}
```

### Best Practices
```csharp
// DO: Enable nullable context globally
// In .csproj
<Nullable>enable</Nullable>

// DO: Check for null before use
public void Process(string? input)
{
    ArgumentNullException.ThrowIfNull(input);  // C# 11+
    // or
    if (input is null)
    {
        throw new ArgumentNullException(nameof(input));
    }

    Console.WriteLine(input.Length);
}

// DO: Use nullable return types when appropriate
public User? FindUser(int id) => users.FirstOrDefault(u => u.Id == id);

// DON'T: Overuse null-forgiving operator
// Bad
public void Bad(string? input)
{
    Console.WriteLine(input!.Length);
}

// Good
public void Good(string? input)
{
    if (input is not null)
    {
        Console.WriteLine(input.Length);
    }
}

// DO: Initialize non-nullable properties
public class User
{
    public string Name { get; set; } = string.Empty;  // Good
    public string Email { get; set; }  // Warning: non-nullable field must contain non-null value
}
```

## 2. LINQ (Language Integrated Query)

### Overview
LINQ provides a consistent model for querying data across different data sources using both query and method syntax.

### Query Syntax
```csharp
// Basic query
var results = from user in users
              where user.Age > 18
              select user.Name;

// Multiple from clauses (SelectMany)
var pairs = from user in users
            from order in user.Orders
            where order.Total > 100
            select new { user.Name, order.Id };

// Join
var results = from user in users
              join order in orders on user.Id equals order.UserId
              select new { user.Name, order.Total };

// Group join (left join)
var results = from user in users
              join order in orders on user.Id equals order.UserId into userOrders
              select new { user.Name, Orders = userOrders };

// Group by
var grouped = from user in users
              group user by user.Department into g
              select new { Department = g.Key, Count = g.Count() };

// Order by
var ordered = from user in users
              orderby user.LastName, user.FirstName descending
              select user;

// Let clause
var results = from user in users
              let fullName = $"{user.FirstName} {user.LastName}"
              where fullName.Length > 10
              select fullName;
```

### Method Syntax
```csharp
// Filtering
var adults = users.Where(u => u.Age >= 18);

// Projection
var names = users.Select(u => u.Name);
var dto = users.Select(u => new UserDto { Name = u.Name, Email = u.Email });

// Ordering
var sorted = users.OrderBy(u => u.LastName)
                  .ThenByDescending(u => u.FirstName);

// Grouping
var grouped = users.GroupBy(u => u.Department)
                   .Select(g => new { Department = g.Key, Count = g.Count() });

// Joining
var results = users.Join(
    orders,
    u => u.Id,
    o => o.UserId,
    (u, o) => new { u.Name, o.Total }
);

// SelectMany (flattening)
var allOrders = users.SelectMany(u => u.Orders);
var pairs = users.SelectMany(
    u => u.Orders,
    (u, o) => new { u.Name, o.Id }
);

// Aggregation
var total = orders.Sum(o => o.Total);
var average = orders.Average(o => o.Total);
var max = orders.Max(o => o.Total);
var count = orders.Count(o => o.IsCompleted);

// Quantifiers
var hasAny = orders.Any(o => o.Total > 1000);
var allCompleted = orders.All(o => o.IsCompleted);

// Element operations
var first = users.First(u => u.Id == 1);  // Throws if not found
var firstOrNull = users.FirstOrDefault(u => u.Id == 1);  // Returns null/default
var single = users.Single(u => u.Email == email);  // Throws if 0 or >1 matches
```

### Deferred vs. Immediate Execution
```csharp
// Deferred execution - query not executed until enumerated
IEnumerable<User> query = users.Where(u => u.Age > 18);

// Query executes here when enumerating
foreach (var user in query) { }

// Immediate execution - query executes immediately
List<User> list = users.Where(u => u.Age > 18).ToList();
User[] array = users.Where(u => u.Age > 18).ToArray();
Dictionary<int, User> dict = users.ToDictionary(u => u.Id);

// Aggregation methods execute immediately
int count = users.Count();
decimal total = orders.Sum(o => o.Total);
```

### Complex LINQ Patterns
```csharp
// Conditional where clauses
var query = users.AsQueryable();
if (!string.IsNullOrEmpty(searchTerm))
{
    query = query.Where(u => u.Name.Contains(searchTerm));
}
if (minAge.HasValue)
{
    query = query.Where(u => u.Age >= minAge.Value);
}
var results = query.ToList();

// Nested queries
var usersWithExpensiveOrders = users
    .Where(u => u.Orders.Any(o => o.Total > 1000))
    .Select(u => new
    {
        u.Name,
        ExpensiveOrders = u.Orders.Where(o => o.Total > 1000)
    });

// Distinct
var uniqueAges = users.Select(u => u.Age).Distinct();
var uniqueUsers = users.DistinctBy(u => u.Email);  // C# 11+

// Set operations
var union = list1.Union(list2);
var intersect = list1.Intersect(list2);
var except = list1.Except(list2);

// Partitioning
var page = users.Skip(pageSize * pageNumber).Take(pageSize);

// Zip
var pairs = list1.Zip(list2, (x, y) => new { x, y });

// Chunk (C# 11+)
var batches = users.Chunk(100);
foreach (var batch in batches)
{
    ProcessBatch(batch);
}
```

### LINQ to Objects Performance
```csharp
// DO: Use List<T> or array for known collections
List<User> users = GetUsers();
var results = users.Where(u => u.Age > 18);  // Fast iteration

// DO: Materialize once if reusing query results
var activeUsers = users.Where(u => u.IsActive).ToList();
var count = activeUsers.Count;
var first = activeUsers.First();

// DON'T: Materialize unnecessarily
// Bad - Count() can work on IEnumerable
var badCount = users.Where(u => u.IsActive).ToList().Count();

// Good
var goodCount = users.Count(u => u.IsActive);

// DO: Filter before projecting
// Good
var names = users.Where(u => u.Age > 18).Select(u => u.Name);

// Less efficient
var names2 = users.Select(u => u.Name).Where(n => users.First(u => u.Name == n).Age > 18);

// DO: Use appropriate methods
// Good - short circuits
bool hasAdmin = users.Any(u => u.Role == "Admin");

// Bad - checks entire collection
bool hasAdmin2 = users.Where(u => u.Role == "Admin").Count() > 0;
```

### Queryable vs. Enumerable
```csharp
// IEnumerable<T> - LINQ to Objects (in-memory)
IEnumerable<User> enumerable = users.Where(u => u.Age > 18);

// IQueryable<T> - LINQ provider translates to data source query
IQueryable<User> queryable = dbContext.Users.Where(u => u.Age > 18);

// AsQueryable converts IEnumerable to IQueryable (still executes in memory)
IQueryable<User> query = users.AsQueryable().Where(u => u.Age > 18);

// AsEnumerable forces remaining query to execute in memory
var results = dbContext.Users
    .Where(u => u.Age > 18)  // Translated to SQL
    .AsEnumerable()
    .Where(u => ComplexInMemoryCheck(u));  // Executes in memory
```

## 3. Async/Await Patterns

### Overview
Async/await enables non-blocking asynchronous operations while maintaining readable code.

### Basic Async/Await
```csharp
// Async method returning Task
public async Task ProcessDataAsync()
{
    await Task.Delay(1000);
    Console.WriteLine("Processed");
}

// Async method returning Task<T>
public async Task<string> GetDataAsync()
{
    var result = await httpClient.GetStringAsync(url);
    return result;
}

// Async void - only for event handlers
private async void Button_Click(object sender, EventArgs e)
{
    await ProcessDataAsync();
}
```

### Task Basics
```csharp
// Creating tasks
Task task = Task.Run(() => DoWork());
Task<int> taskWithResult = Task.Run(() => CalculateValue());

// Completing immediately
Task<string> completed = Task.FromResult("value");
Task failed = Task.FromException(new Exception("error"));
Task canceled = Task.FromCanceled(cancellationToken);

// Waiting (blocks current thread - avoid in async code)
task.Wait();
int result = taskWithResult.Result;

// Async waiting (doesn't block thread)
await task;
int result = await taskWithResult;
```

### ConfigureAwait
```csharp
// Library code - don't capture synchronization context
public async Task<string> LibraryMethodAsync()
{
    var result = await httpClient.GetStringAsync(url)
        .ConfigureAwait(false);
    return result;
}

// UI/ASP.NET Core code - usually omit (capture context)
public async Task ButtonClickAsync()
{
    var data = await GetDataAsync();  // Returns to UI thread
    textBox.Text = data;  // Can update UI
}

// When to use ConfigureAwait(false)
// - Library code that doesn't need synchronization context
// - Improves performance by avoiding context capture
// - Prevents potential deadlocks

// When to omit ConfigureAwait or use ConfigureAwait(true)
// - UI code that needs to update controls
// - ASP.NET code that needs HttpContext
// - Code that depends on synchronization context
```

### Parallel Async Operations
```csharp
// Run tasks concurrently and wait for all
Task<string> task1 = GetDataAsync(url1);
Task<string> task2 = GetDataAsync(url2);
Task<string> task3 = GetDataAsync(url3);

await Task.WhenAll(task1, task2, task3);

string result1 = task1.Result;  // Already completed
string result2 = task2.Result;
string result3 = task3.Result;

// With results
var tasks = new[]
{
    GetDataAsync(url1),
    GetDataAsync(url2),
    GetDataAsync(url3)
};
string[] results = await Task.WhenAll(tasks);

// Wait for first to complete
Task<string> firstCompleted = await Task.WhenAny(task1, task2, task3);
string firstResult = await firstCompleted;

// Process as they complete
var tasks = urls.Select(url => GetDataAsync(url)).ToList();
while (tasks.Count > 0)
{
    Task<string> completedTask = await Task.WhenAny(tasks);
    tasks.Remove(completedTask);

    string result = await completedTask;
    ProcessResult(result);
}
```

### Cancellation
```csharp
// Creating cancellation token source
using var cts = new CancellationTokenSource();

// Cancel after timeout
cts.CancelAfter(TimeSpan.FromSeconds(30));

// Manual cancellation
cts.Cancel();

// Passing token to async method
await ProcessDataAsync(cts.Token);

// Implementing cancellation
public async Task ProcessDataAsync(CancellationToken cancellationToken)
{
    for (int i = 0; i < 1000; i++)
    {
        // Check for cancellation
        cancellationToken.ThrowIfCancellationRequested();

        // Or manual check
        if (cancellationToken.IsCancellationRequested)
        {
            // Cleanup
            return;
        }

        await ProcessItemAsync(i, cancellationToken);
    }
}

// Linking tokens
using var linkedCts = CancellationTokenSource
    .CreateLinkedTokenSource(token1, token2);
await ProcessAsync(linkedCts.Token);

// Registering callback
cancellationToken.Register(() =>
{
    Console.WriteLine("Cancellation requested");
});
```

### Error Handling
```csharp
// Try-catch with async
public async Task<string> GetDataWithErrorHandlingAsync()
{
    try
    {
        return await httpClient.GetStringAsync(url);
    }
    catch (HttpRequestException ex)
    {
        logger.LogError(ex, "HTTP request failed");
        throw;
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Unexpected error");
        return string.Empty;
    }
}

// Multiple tasks - exceptions aggregated
try
{
    await Task.WhenAll(task1, task2, task3);
}
catch (Exception ex)
{
    // Only first exception is caught
    logger.LogError(ex, "At least one task failed");
}

// To get all exceptions
var tasks = new[] { task1, task2, task3 };
try
{
    await Task.WhenAll(tasks);
}
catch
{
    foreach (var task in tasks)
    {
        if (task.IsFaulted)
        {
            logger.LogError(task.Exception, "Task failed");
        }
    }
}

// Handling faulted tasks
if (task.IsCompleted && !task.IsFaulted && !task.IsCanceled)
{
    var result = task.Result;
}
```

### Async Enumerable (IAsyncEnumerable)
```csharp
// Async iterator
public async IAsyncEnumerable<int> GenerateNumbersAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    for (int i = 0; i < 100; i++)
    {
        await Task.Delay(100, cancellationToken);
        yield return i;
    }
}

// Consuming async enumerable
await foreach (var number in GenerateNumbersAsync())
{
    Console.WriteLine(number);
}

// With cancellation
await foreach (var number in GenerateNumbersAsync(cancellationToken))
{
    Console.WriteLine(number);
}

// Real-world example - streaming API results
public async IAsyncEnumerable<User> StreamUsersAsync(
    [EnumeratorCancellation] CancellationToken cancellationToken = default)
{
    int page = 0;
    while (true)
    {
        var users = await GetPageAsync(page, cancellationToken);
        if (users.Count == 0)
            break;

        foreach (var user in users)
        {
            yield return user;
        }

        page++;
    }
}
```

### ValueTask
```csharp
// Use ValueTask when result is often available synchronously
public ValueTask<int> GetCachedValueAsync(string key)
{
    if (cache.TryGetValue(key, out int value))
    {
        return new ValueTask<int>(value);  // Synchronous completion
    }

    return new ValueTask<int>(FetchFromDatabaseAsync(key));  // Async completion
}

// Consuming ValueTask
int value = await GetCachedValueAsync("key");

// DO: Await ValueTask immediately
// Good
var result = await GetCachedValueAsync("key");

// DON'T: Store or await multiple times
// Bad
ValueTask<int> task = GetCachedValueAsync("key");
int result1 = await task;
int result2 = await task;  // May throw or return incorrect result

// DON'T: Use with Task.WhenAll
// Bad - convert to Task first
ValueTask<int> vt = GetCachedValueAsync("key");
await Task.WhenAll(vt.AsTask(), otherTask);
```

### Best Practices
```csharp
// DO: Use async all the way
// Good
public async Task<ActionResult> GetDataAsync()
{
    var data = await service.GetDataAsync();
    return Ok(data);
}

// Bad - sync over async (can cause deadlocks)
public ActionResult GetData()
{
    var data = service.GetDataAsync().Result;
    return Ok(data);
}

// DO: Suffix async methods with Async
public async Task<User> GetUserAsync(int id) { }

// DO: Return Task directly when possible
public Task<User> GetUserAsync(int id)
{
    return repository.GetByIdAsync(id);  // No await needed
}

// DON'T: Use async void except for event handlers
// Bad
public async void ProcessData()
{
    await DoWorkAsync();
}

// Good
public async Task ProcessDataAsync()
{
    await DoWorkAsync();
}

// DO: Use cancellation tokens
public async Task ProcessAsync(CancellationToken cancellationToken = default)
{
    await DoWorkAsync(cancellationToken);
}

// DO: ConfigureAwait(false) in library code
public async Task<string> LibraryMethodAsync()
{
    return await httpClient.GetStringAsync(url).ConfigureAwait(false);
}

// DON'T: Create unnecessary tasks
// Bad
public async Task<int> GetValueAsync()
{
    return await Task.Run(() => value);
}

// Good
public Task<int> GetValueAsync()
{
    return Task.FromResult(value);
}
```

## 4. Records and Init-Only Properties

### Overview
Records provide concise syntax for immutable reference types with value semantics. Init-only properties allow setting properties during object initialization but not after.

### Record Basics
```csharp
// Positional record
public record Person(string FirstName, string LastName, int Age);

// Usage
var person = new Person("John", "Doe", 30);
Console.WriteLine(person.FirstName);  // John

// Records are immutable by default - use 'with' for modifications
var older = person with { Age = 31 };

// Traditional property syntax
public record User
{
    public string Name { get; init; }
    public string Email { get; init; }
    public DateTime CreatedAt { get; init; }
}

// Mixed syntax
public record Product(string Name, decimal Price)
{
    public string Description { get; init; } = string.Empty;
    public bool IsAvailable { get; init; } = true;
}
```

### Record Value Semantics
```csharp
// Records use value-based equality
var person1 = new Person("John", "Doe", 30);
var person2 = new Person("John", "Doe", 30);

Console.WriteLine(person1 == person2);  // True
Console.WriteLine(person1.Equals(person2));  // True
Console.WriteLine(ReferenceEquals(person1, person2));  // False

// Automatic ToString implementation
Console.WriteLine(person1);  // Person { FirstName = John, LastName = Doe, Age = 30 }

// Automatic Deconstruction
var (firstName, lastName, age) = person1;

// GetHashCode based on values
var dict = new Dictionary<Person, string>();
dict[person1] = "Value";
Console.WriteLine(dict[person2]);  // Value (same key due to value equality)
```

### With-Expressions
```csharp
var original = new Person("John", "Doe", 30);

// Create modified copy
var modified = original with { Age = 31 };

// Multiple properties
var updated = original with
{
    LastName = "Smith",
    Age = 32
};

// Original unchanged
Console.WriteLine(original.Age);  // 30
Console.WriteLine(modified.Age);  // 31

// Chaining
var final = original
    .with { Age = 31 }
    .with { LastName = "Smith" };
```

### Record Inheritance
```csharp
// Base record
public record Person(string FirstName, string LastName);

// Derived record
public record Employee(string FirstName, string LastName, string Department)
    : Person(FirstName, LastName);

// Usage
Employee emp = new("John", "Doe", "IT");
Person person = emp;  // Upcasting

// With-expression preserves derived type
Employee updated = emp with { Department = "HR" };

// Equality respects hierarchy
Person p = new("John", "Doe");
Employee e = new("John", "Doe", "IT");
Console.WriteLine(p == e);  // False (different types)
```

### Record Structs (C# 10+)
```csharp
// Readonly record struct
public readonly record struct Point(int X, int Y);

// Mutable record struct
public record struct MutablePoint(int X, int Y);

// Usage
var p1 = new Point(1, 2);
// p1.X = 3;  // Error - readonly

var p2 = new MutablePoint(1, 2);
p2.X = 3;  // OK - mutable

// Value semantics still apply
var p3 = new Point(1, 2);
Console.WriteLine(p1 == p3);  // True
```

### Init-Only Properties
```csharp
// Init-only property
public class User
{
    public string Name { get; init; }
    public string Email { get; init; }
}

// Can set during initialization
var user = new User
{
    Name = "John",
    Email = "john@example.com"
};

// Cannot set after initialization
// user.Name = "Jane";  // Error

// With positional parameters
public class Product
{
    public Product(string name, decimal price)
    {
        Name = name;
        Price = price;
    }

    public string Name { get; init; }
    public decimal Price { get; init; }
    public string Description { get; init; } = string.Empty;
}

var product = new Product("Widget", 9.99m)
{
    Description = "A useful widget"
};
```

### Required Properties (C# 11+)
```csharp
// Required property must be set during initialization
public class User
{
    public required string Name { get; init; }
    public required string Email { get; init; }
    public string? PhoneNumber { get; init; }
}

// Must set required properties
var user = new User
{
    Name = "John",
    Email = "john@example.com"
    // PhoneNumber is optional
};

// With records
public record Person
{
    public required string FirstName { get; init; }
    public required string LastName { get; init; }
}

// SetsRequiredMembers attribute for constructors
public record Person
{
    public required string FirstName { get; init; }
    public required string LastName { get; init; }

    [SetsRequiredMembers]
    public Person(string firstName, string lastName)
    {
        FirstName = firstName;
        LastName = lastName;
    }
}

var person = new Person("John", "Doe");  // No initializer needed
```

### Record Patterns
```csharp
// DTOs
public record UserDto(int Id, string Name, string Email);

// Domain events
public record UserCreatedEvent(int UserId, DateTime CreatedAt);
public record UserUpdatedEvent(int UserId, DateTime UpdatedAt);

// API responses
public record ApiResponse<T>(bool Success, T? Data, string? Error);

// Configuration
public record DatabaseConfig
{
    public required string ConnectionString { get; init; }
    public int MaxRetries { get; init; } = 3;
    public TimeSpan Timeout { get; init; } = TimeSpan.FromSeconds(30);
}

// Immutable collections in records
public record ShoppingCart
{
    public ImmutableList<CartItem> Items { get; init; } = ImmutableList<CartItem>.Empty;

    public ShoppingCart AddItem(CartItem item)
    {
        return this with { Items = Items.Add(item) };
    }
}
```

### Best Practices
```csharp
// DO: Use records for DTOs and value objects
public record AddressDto(string Street, string City, string ZipCode);

// DO: Use records for immutable data
public record Configuration(string ApiKey, string BaseUrl);

// DON'T: Use records for entities with identity
// Bad - entities need reference equality
public record User(int Id, string Name);

// Good - use class for entities
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
}

// DO: Use init for immutability in classes
public class ValueObject
{
    public string Value { get; init; }
}

// DON'T: Mix mutable and immutable properties
// Bad
public record ConfusingRecord
{
    public string ImmutableProperty { get; init; }
    public string MutableProperty { get; set; }
}

// DO: Use required for mandatory properties
public record CreateUserRequest
{
    public required string Name { get; init; }
    public required string Email { get; init; }
    public string? PhoneNumber { get; init; }
}
```

## 5. Pattern Matching

### Overview
Pattern matching provides concise syntax for testing values against patterns and extracting information.

### Type Patterns
```csharp
// Basic type check
if (obj is string)
{
    string str = (string)obj;
}

// Type pattern with variable
if (obj is string str)
{
    Console.WriteLine(str.Length);
}

// Multiple type patterns
string result = obj switch
{
    string s => s,
    int i => i.ToString(),
    null => "null",
    _ => "unknown"
};
```

### Constant Patterns
```csharp
// Constant pattern
if (value is null)
{
    return;
}

if (value is 0)
{
    Console.WriteLine("Zero");
}

// Switch expression with constants
string description = value switch
{
    0 => "zero",
    1 => "one",
    2 => "two",
    _ => "other"
};
```

### Relational Patterns
```csharp
// Relational operators: <, <=, >, >=
string category = age switch
{
    < 13 => "child",
    < 20 => "teenager",
    < 65 => "adult",
    _ => "senior"
};

// Combining relational patterns
string grade = score switch
{
    >= 90 => "A",
    >= 80 => "B",
    >= 70 => "C",
    >= 60 => "D",
    _ => "F"
};

// With and/or patterns
bool isValid = value switch
{
    > 0 and < 100 => true,
    _ => false
};
```

### Logical Patterns
```csharp
// And pattern
if (obj is string s and { Length: > 0 })
{
    Console.WriteLine(s);
}

// Or pattern
if (value is 0 or 1 or 2)
{
    Console.WriteLine("Small number");
}

// Not pattern
if (value is not null)
{
    Process(value);
}

// Complex combinations
string result = value switch
{
    null or "" => "empty",
    { Length: > 0 and < 10 } => "short",
    { Length: >= 10 } => "long",
    _ => "unknown"
};
```

### Property Patterns
```csharp
// Property pattern
if (person is { Age: > 18 })
{
    Console.WriteLine("Adult");
}

// Multiple properties
if (person is { Age: > 18, IsActive: true })
{
    Process(person);
}

// Nested properties
if (order is { Customer: { IsVip: true }, Total: > 1000 })
{
    ApplyVipDiscount(order);
}

// Switch expression with properties
string description = person switch
{
    { Age: < 18 } => "minor",
    { Age: >= 18, IsStudent: true } => "student",
    { Age: >= 18, IsEmployed: true } => "employed",
    _ => "other"
};

// Extracting values
if (person is { Name: var name, Age: var age })
{
    Console.WriteLine($"{name} is {age} years old");
}
```

### Positional Patterns
```csharp
// Deconstruction pattern
if (point is (0, 0))
{
    Console.WriteLine("Origin");
}

// With variables
if (point is (var x, var y))
{
    Console.WriteLine($"X: {x}, Y: {y}");
}

// Switch expression
string quadrant = point switch
{
    (0, 0) => "origin",
    (var x, var y) when x > 0 && y > 0 => "quadrant I",
    (var x, var y) when x < 0 && y > 0 => "quadrant II",
    (var x, var y) when x < 0 && y < 0 => "quadrant III",
    (var x, var y) when x > 0 && y < 0 => "quadrant IV",
    _ => "on axis"
};

// Custom Deconstruct method
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }

    public void Deconstruct(out string name, out int age)
    {
        name = Name;
        age = Age;
    }
}

if (person is ("John", var age))
{
    Console.WriteLine($"John is {age} years old");
}
```

### List Patterns (C# 11+)
```csharp
// List pattern matching
int[] numbers = { 1, 2, 3 };

string result = numbers switch
{
    [] => "empty",
    [1] => "single one",
    [1, 2] => "one and two",
    [1, 2, 3] => "one, two, three",
    _ => "other"
};

// Discard pattern
if (numbers is [_, 2, _])
{
    Console.WriteLine("Middle element is 2");
}

// Slice pattern
string description = numbers switch
{
    [1, .. var rest] => $"starts with 1, {rest.Length} more",
    [.. var middle, 3] => $"ends with 3, {middle.Length} before",
    [1, .., 3] => "starts with 1 and ends with 3",
    _ => "other"
};

// Var pattern for slice
if (numbers is [var first, .. var middle, var last])
{
    Console.WriteLine($"First: {first}, Middle: [{string.Join(", ", middle)}], Last: {last}");
}
```

### When Clauses
```csharp
// When clause (case guard)
string category = value switch
{
    int i when i < 0 => "negative",
    int i when i == 0 => "zero",
    int i when i > 0 => "positive",
    _ => "not an integer"
};

// Complex conditions
string result = obj switch
{
    string s when s.StartsWith("A") => "starts with A",
    string s when s.Length > 10 => "long string",
    int i when i % 2 == 0 => "even number",
    _ => "other"
};

// With property patterns
string description = person switch
{
    { Age: var age } when age < 18 => "minor",
    { Age: var age, IsStudent: true } when age < 25 => "student",
    { IsEmployed: true } => "employed",
    _ => "other"
};
```

### Practical Examples
```csharp
// Parsing different input types
public static int ParseInput(object input)
{
    return input switch
    {
        int i => i,
        string s when int.TryParse(s, out int result) => result,
        string => 0,
        _ => throw new ArgumentException("Cannot parse input")
    };
}

// State machine
public State ProcessEvent(Event evt, State current)
{
    return (evt, current) switch
    {
        (StartEvent, IdleState) => new RunningState(),
        (StopEvent, RunningState) => new IdleState(),
        (PauseEvent, RunningState) => new PausedState(),
        (ResumeEvent, PausedState) => new RunningState(),
        _ => current
    };
}

// Visitor pattern
public decimal CalculatePrice(Product product)
{
    return product switch
    {
        Book { Pages: > 500 } => 29.99m,
        Book => 19.99m,
        Electronics { Warranty: true } => 599.99m,
        Electronics => 499.99m,
        Clothing { Size: "XL" or "XXL" } => 39.99m,
        Clothing => 29.99m,
        _ => 9.99m
    };
}

// Response handling
public async Task<string> HandleResponseAsync(HttpResponseMessage response)
{
    return response.StatusCode switch
    {
        HttpStatusCode.OK => await response.Content.ReadAsStringAsync(),
        HttpStatusCode.NotFound => "Resource not found",
        HttpStatusCode.Unauthorized => "Unauthorized access",
        >= HttpStatusCode.BadRequest and < HttpStatusCode.InternalServerError
            => "Client error",
        >= HttpStatusCode.InternalServerError
            => "Server error",
        _ => "Unknown error"
    };
}
```

### Best Practices
```csharp
// DO: Use switch expressions for multiple cases
// Good
string result = value switch
{
    1 => "one",
    2 => "two",
    _ => "other"
};

// Less readable
string result;
if (value == 1)
    result = "one";
else if (value == 2)
    result = "two";
else
    result = "other";

// DO: Use not pattern for null checks
if (value is not null)
{
    Process(value);
}

// DO: Use property patterns for complex checks
if (person is { Age: > 18, IsActive: true })
{
    Process(person);
}

// DON'T: Overuse when clauses - consider separate methods
// Bad
var result = value switch
{
    int i when ComplexCondition1(i) => "a",
    int i when ComplexCondition2(i) => "b",
    _ => "c"
};

// Better
if (value is int i && ComplexCondition1(i))
    return "a";
if (value is int j && ComplexCondition2(j))
    return "b";
return "c";

// DO: Exhaust all possibilities or use discard pattern
string result = value switch
{
    0 => "zero",
    > 0 => "positive",
    < 0 => "negative",
    // All cases covered, _ not needed
};
```

## 6. Delegates and Events

### Overview
Delegates are type-safe function pointers. Events provide a publish-subscribe mechanism built on delegates.

### Delegate Basics
```csharp
// Delegate declaration
public delegate void NotifyHandler(string message);
public delegate int Calculate(int x, int y);

// Using delegates
NotifyHandler handler = ShowMessage;
handler("Hello");  // Invokes ShowMessage("Hello")

void ShowMessage(string message)
{
    Console.WriteLine(message);
}

// Multi-cast delegates
NotifyHandler handler = ShowMessage;
handler += LogMessage;
handler += SendEmail;
handler("Event occurred");  // Calls all three methods

// Removing delegates
handler -= LogMessage;

// Return value with multi-cast (only last value returned)
Calculate calc = Add;
calc += Multiply;
int result = calc(5, 3);  // Returns Multiply result, Add result discarded
```

### Built-in Delegates
```csharp
// Action - no return value
Action action = () => Console.WriteLine("Action");
Action<string> actionWithParam = message => Console.WriteLine(message);
Action<int, string> actionMultiParam = (id, name) =>
    Console.WriteLine($"{id}: {name}");

action();
actionWithParam("Hello");
actionMultiParam(1, "John");

// Func - with return value
Func<int> func = () => 42;
Func<int, int> funcWithParam = x => x * 2;
Func<int, int, int> funcMultiParam = (x, y) => x + y;

int value = func();
int doubled = funcWithParam(5);
int sum = funcMultiParam(3, 4);

// Predicate - returns bool
Predicate<int> isEven = x => x % 2 == 0;
bool result = isEven(4);

// Comparison
Comparison<int> comparison = (x, y) => x.CompareTo(y);
```

### Events
```csharp
// Event declaration
public class Publisher
{
    // Event with EventHandler
    public event EventHandler? SomethingHappened;

    // Event with EventHandler<TEventArgs>
    public event EventHandler<DataEventArgs>? DataReceived;

    // Event with custom delegate
    public event NotifyHandler? Notification;

    protected virtual void OnSomethingHappened(EventArgs e)
    {
        SomethingHappened?.Invoke(this, e);
    }

    protected virtual void OnDataReceived(DataEventArgs e)
    {
        DataReceived?.Invoke(this, e);
    }

    public void DoSomething()
    {
        // Raise event
        OnSomethingHappened(EventArgs.Empty);
        OnDataReceived(new DataEventArgs { Data = "test" });
    }
}

// Custom EventArgs
public class DataEventArgs : EventArgs
{
    public string Data { get; set; } = string.Empty;
}

// Subscribing to events
var publisher = new Publisher();
publisher.SomethingHappened += OnSomethingHappened;
publisher.DataReceived += OnDataReceived;

void OnSomethingHappened(object? sender, EventArgs e)
{
    Console.WriteLine("Something happened");
}

void OnDataReceived(object? sender, DataEventArgs e)
{
    Console.WriteLine($"Data received: {e.Data}");
}

// Unsubscribing
publisher.SomethingHappened -= OnSomethingHappened;
```

### Lambda Expressions
```csharp
// Expression lambda
Func<int, int> square = x => x * x;

// Statement lambda
Func<int, int, int> divide = (x, y) =>
{
    if (y == 0)
        throw new DivideByZeroException();
    return x / y;
};

// Lambda with no parameters
Action greet = () => Console.WriteLine("Hello");

// Capturing variables (closure)
int factor = 10;
Func<int, int> multiply = x => x * factor;
int result = multiply(5);  // 50

factor = 20;
result = multiply(5);  // 100 (captures current value)

// Async lambda
Func<Task<string>> fetchData = async () =>
{
    await Task.Delay(1000);
    return "Data";
};
```

### Event Patterns
```csharp
// Standard event pattern
public class Button
{
    public event EventHandler? Click;

    protected virtual void OnClick(EventArgs e)
    {
        Click?.Invoke(this, e);
    }

    public void PerformClick()
    {
        OnClick(EventArgs.Empty);
    }
}

// Weak event pattern (prevents memory leaks)
public class WeakEventManager
{
    private readonly List<WeakReference<EventHandler>> handlers = new();

    public void AddHandler(EventHandler handler)
    {
        handlers.Add(new WeakReference<EventHandler>(handler));
    }

    public void RemoveHandler(EventHandler handler)
    {
        handlers.RemoveAll(wr =>
        {
            if (!wr.TryGetTarget(out var target))
                return true;  // Remove dead reference
            return target == handler;
        });
    }

    public void Raise(object? sender, EventArgs e)
    {
        foreach (var wr in handlers.ToList())
        {
            if (wr.TryGetTarget(out var handler))
            {
                handler(sender, e);
            }
            else
            {
                handlers.Remove(wr);  // Cleanup
            }
        }
    }
}

// Custom add/remove
public class CustomEvents
{
    private EventHandler? _changed;

    public event EventHandler? Changed
    {
        add
        {
            Console.WriteLine("Handler added");
            _changed += value;
        }
        remove
        {
            Console.WriteLine("Handler removed");
            _changed -= value;
        }
    }
}
```

### Practical Examples
```csharp
// Observer pattern
public class StockMonitor
{
    public event EventHandler<StockChangedEventArgs>? StockChanged;

    private decimal _price;
    public decimal Price
    {
        get => _price;
        set
        {
            if (_price != value)
            {
                var oldPrice = _price;
                _price = value;
                OnStockChanged(new StockChangedEventArgs
                {
                    OldPrice = oldPrice,
                    NewPrice = value
                });
            }
        }
    }

    protected virtual void OnStockChanged(StockChangedEventArgs e)
    {
        StockChanged?.Invoke(this, e);
    }
}

public class StockChangedEventArgs : EventArgs
{
    public decimal OldPrice { get; set; }
    public decimal NewPrice { get; set; }
}

// Usage
var monitor = new StockMonitor();
monitor.StockChanged += (sender, e) =>
{
    Console.WriteLine($"Price changed from {e.OldPrice} to {e.NewPrice}");
};
monitor.Price = 100.50m;

// Progress reporting
public class FileProcessor
{
    public event EventHandler<ProgressEventArgs>? ProgressChanged;

    public async Task ProcessFilesAsync(string[] files)
    {
        for (int i = 0; i < files.Length; i++)
        {
            await ProcessFileAsync(files[i]);

            OnProgressChanged(new ProgressEventArgs
            {
                Percentage = (i + 1) * 100 / files.Length,
                Message = $"Processed {files[i]}"
            });
        }
    }

    protected virtual void OnProgressChanged(ProgressEventArgs e)
    {
        ProgressChanged?.Invoke(this, e);
    }
}

public class ProgressEventArgs : EventArgs
{
    public int Percentage { get; set; }
    public string Message { get; set; } = string.Empty;
}

// Callback pattern
public class DataLoader
{
    public async Task LoadDataAsync(
        Func<string, Task> onProgress,
        Func<Exception, Task<bool>> onError)
    {
        try
        {
            await onProgress("Starting...");
            // Load data
            await onProgress("Completed");
        }
        catch (Exception ex)
        {
            bool retry = await onError(ex);
            if (retry)
            {
                await LoadDataAsync(onProgress, onError);
            }
        }
    }
}
```

### Best Practices
```csharp
// DO: Use EventHandler<T> for events
public event EventHandler<DataEventArgs>? DataReceived;

// DON'T: Use custom delegates unless necessary
// Avoid
public delegate void DataHandler(string data);
public event DataHandler? DataReceived;

// DO: Follow event naming conventions
protected virtual void OnDataReceived(DataEventArgs e)
{
    DataReceived?.Invoke(this, e);
}

// DO: Check for null before invoking
// Good - null conditional
SomethingHappened?.Invoke(this, EventArgs.Empty);

// Old way
var handler = SomethingHappened;
if (handler != null)
{
    handler(this, EventArgs.Empty);
}

// DO: Unsubscribe from events to prevent memory leaks
publisher.DataReceived -= OnDataReceived;

// DO: Use weak references for long-lived publishers
// See WeakEventManager example above

// DON'T: Return values from multi-cast delegates
// Bad - only last value returned
public delegate int Calculate(int x);
Calculate calc = x => x * 2;
calc += x => x + 1;
int result = calc(5);  // Only returns 6, ignores 10

// DO: Use Action/Func for callbacks
public void ProcessData(Action<string> callback)
{
    callback("Processing...");
}

// DON'T: Raise events outside of the class
// Events can only be raised by the declaring class
```

## 7. Generics

### Overview
Generics enable type-safe code reuse without boxing/unboxing or type casting.

### Generic Classes
```csharp
// Generic class
public class Container<T>
{
    private T _value;

    public Container(T value)
    {
        _value = value;
    }

    public T GetValue() => _value;
    public void SetValue(T value) => _value = value;
}

// Usage
var intContainer = new Container<int>(42);
var stringContainer = new Container<string>("hello");

// Multiple type parameters
public class Pair<TFirst, TSecond>
{
    public TFirst First { get; set; }
    public TSecond Second { get; set; }
}

var pair = new Pair<int, string> { First = 1, Second = "one" };
```

### Generic Methods
```csharp
// Generic method
public T GetDefault<T>()
{
    return default(T);
}

// Type inference
int defaultInt = GetDefault<int>();  // Explicit
int inferredInt = GetDefault();  // Inferred from return type

// Generic method with constraints
public T Max<T>(T a, T b) where T : IComparable<T>
{
    return a.CompareTo(b) > 0 ? a : b;
}

int maxInt = Max(5, 10);
string maxString = Max("apple", "banana");

// Multiple type parameters
public TResult Convert<TSource, TResult>(TSource source, Func<TSource, TResult> converter)
{
    return converter(source);
}

string result = Convert(42, i => i.ToString());
```

### Generic Constraints
```csharp
// Class constraint
public class Repository<T> where T : class
{
    public T? FindById(int id) => null;
}

// Struct constraint
public class Calculator<T> where T : struct
{
    public T Add(T a, T b) => default;
}

// Interface constraint
public class Sorter<T> where T : IComparable<T>
{
    public List<T> Sort(List<T> items)
    {
        return items.OrderBy(x => x).ToList();
    }
}

// Base class constraint
public class Manager<T> where T : BaseEntity
{
    public void Save(T entity)
    {
        entity.UpdatedAt = DateTime.UtcNow;
    }
}

// Constructor constraint
public class Factory<T> where T : new()
{
    public T Create()
    {
        return new T();
    }
}

// Multiple constraints
public class AdvancedRepository<T>
    where T : BaseEntity, IValidatable, new()
{
    public T Create()
    {
        var entity = new T();
        entity.Validate();
        return entity;
    }
}

// Constraint on multiple type parameters
public class Converter<TInput, TOutput>
    where TInput : class
    where TOutput : class, new()
{
    public TOutput Convert(TInput input)
    {
        return new TOutput();
    }
}

// Notnull constraint (C# 8+)
public class Container<T> where T : notnull
{
    private Dictionary<string, T> _items = new();
}
```

### Covariance and Contravariance
```csharp
// Covariance (out) - can return more derived type
public interface IProducer<out T>
{
    T Produce();
    // T Consume(T item);  // Error - T in input position
}

IProducer<string> stringProducer = GetProducer();
IProducer<object> objectProducer = stringProducer;  // OK - string is object

// Contravariance (in) - can accept more general type
public interface IConsumer<in T>
{
    void Consume(T item);
    // T Produce();  // Error - T in output position
}

IConsumer<object> objectConsumer = GetConsumer();
IConsumer<string> stringConsumer = objectConsumer;  // OK - object accepts string

// Real-world example
IEnumerable<string> strings = new List<string> { "a", "b" };
IEnumerable<object> objects = strings;  // OK - IEnumerable<out T> is covariant

Action<object> objectAction = obj => Console.WriteLine(obj);
Action<string> stringAction = objectAction;  // OK - Action<in T> is contravariant
```

### Generic Collections
```csharp
// List<T>
List<int> numbers = new() { 1, 2, 3 };
List<string> names = ["Alice", "Bob"];  // C# 12 collection expression

// Dictionary<TKey, TValue>
Dictionary<string, int> ages = new()
{
    ["Alice"] = 30,
    ["Bob"] = 25
};

// HashSet<T>
HashSet<string> uniqueNames = new() { "Alice", "Bob", "Alice" };

// Queue<T>
Queue<int> queue = new();
queue.Enqueue(1);
int item = queue.Dequeue();

// Stack<T>
Stack<int> stack = new();
stack.Push(1);
int top = stack.Pop();

// LinkedList<T>
LinkedList<string> list = new();
list.AddFirst("first");
list.AddLast("last");

// SortedSet<T>
SortedSet<int> sorted = new() { 3, 1, 2 };  // Maintains order

// SortedDictionary<TKey, TValue>
SortedDictionary<string, int> sortedDict = new()
{
    ["z"] = 1,
    ["a"] = 2
};
```

### Generic Interfaces
```csharp
// IEnumerable<T>
public class CustomCollection<T> : IEnumerable<T>
{
    private List<T> _items = new();

    public IEnumerator<T> GetEnumerator()
    {
        return _items.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
}

// IComparer<T>
public class DescendingComparer<T> : IComparer<T> where T : IComparable<T>
{
    public int Compare(T? x, T? y)
    {
        if (x == null || y == null)
            return 0;
        return y.CompareTo(x);  // Reversed
    }
}

List<int> numbers = new() { 3, 1, 2 };
numbers.Sort(new DescendingComparer<int>());

// IEqualityComparer<T>
public class CaseInsensitiveComparer : IEqualityComparer<string>
{
    public bool Equals(string? x, string? y)
    {
        return string.Equals(x, y, StringComparison.OrdinalIgnoreCase);
    }

    public int GetHashCode(string obj)
    {
        return obj.ToLowerInvariant().GetHashCode();
    }
}

var dict = new Dictionary<string, int>(new CaseInsensitiveComparer());
dict["KEY"] = 1;
Console.WriteLine(dict["key"]);  // 1
```

### Advanced Generic Patterns
```csharp
// Generic factory
public interface IFactory<T>
{
    T Create();
}

public class DefaultFactory<T> : IFactory<T> where T : new()
{
    public T Create() => new T();
}

// Generic builder
public class Builder<T> where T : class, new()
{
    private readonly T _instance = new();
    private readonly List<Action<T>> _actions = new();

    public Builder<T> With(Action<T> action)
    {
        _actions.Add(action);
        return this;
    }

    public T Build()
    {
        foreach (var action in _actions)
        {
            action(_instance);
        }
        return _instance;
    }
}

var user = new Builder<User>()
    .With(u => u.Name = "John")
    .With(u => u.Email = "john@example.com")
    .Build();

// Generic repository pattern
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}

public class Repository<T> : IRepository<T> where T : class
{
    private readonly DbContext _context;

    public Repository(DbContext context)
    {
        _context = context;
    }

    public async Task<T?> GetByIdAsync(int id)
    {
        return await _context.Set<T>().FindAsync(id);
    }

    public async Task<IEnumerable<T>> GetAllAsync()
    {
        return await _context.Set<T>().ToListAsync();
    }

    // ... other methods
}

// Type recursion
public class TreeNode<T> where T : TreeNode<T>
{
    public List<T> Children { get; set; } = new();
}

public class BinaryNode : TreeNode<BinaryNode>
{
    public BinaryNode? Left { get; set; }
    public BinaryNode? Right { get; set; }
}
```

### Best Practices
```csharp
// DO: Use meaningful type parameter names
public class Dictionary<TKey, TValue>  // Good
public class Dictionary<K, V>  // Less clear

// DO: Use single letter for simple cases
public T Identity<T>(T value) => value;

// DO: Constrain type parameters when needed
public void Sort<T>(List<T> items) where T : IComparable<T>
{
    items.Sort();
}

// DON'T: Overuse constraints
// Bad - unnecessary constraint
public T Clone<T>(T item) where T : class, ICloneable
{
    return (T)item.Clone();
}

// DO: Use generic collections over non-generic
List<int> numbers = new();  // Good
ArrayList numbers2 = new();  // Bad - uses boxing

// DO: Consider covariance/contravariance for interfaces
public interface IReader<out T>  // Can return derived types
{
    T Read();
}

// DON'T: Use generics when not needed
// Bad - not reusable
public class IntContainer
{
    public int Value { get; set; }
}

// Good - reusable
public class Container<T>
{
    public T Value { get; set; }
}
```

## 8. Extension Methods

### Overview
Extension methods add functionality to existing types without modifying them or creating derived types.

### Basic Extension Methods
```csharp
// Extension method class (must be static)
public static class StringExtensions
{
    // Extension method (must be static with this parameter)
    public static bool IsNullOrEmpty(this string? value)
    {
        return string.IsNullOrEmpty(value);
    }

    public static string Truncate(this string value, int maxLength)
    {
        if (value.Length <= maxLength)
            return value;
        return value.Substring(0, maxLength) + "...";
    }
}

// Usage
string text = "Hello, World!";
bool isEmpty = text.IsNullOrEmpty();  // false
string truncated = text.Truncate(5);  // "Hello..."

// Null reference
string? nullText = null;
bool isNull = nullText.IsNullOrEmpty();  // true
```

### Extension Methods for Collections
```csharp
public static class EnumerableExtensions
{
    public static bool IsNullOrEmpty<T>(this IEnumerable<T>? source)
    {
        return source == null || !source.Any();
    }

    public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> source)
        where T : class
    {
        return source.Where(x => x != null)!;
    }

    public static void ForEach<T>(this IEnumerable<T> source, Action<T> action)
    {
        foreach (var item in source)
        {
            action(item);
        }
    }

    public static Dictionary<TKey, TValue> ToDictionarySafe<TSource, TKey, TValue>(
        this IEnumerable<TSource> source,
        Func<TSource, TKey> keySelector,
        Func<TSource, TValue> valueSelector)
        where TKey : notnull
    {
        var dict = new Dictionary<TKey, TValue>();
        foreach (var item in source)
        {
            var key = keySelector(item);
            if (!dict.ContainsKey(key))
            {
                dict[key] = valueSelector(item);
            }
        }
        return dict;
    }

    public static IEnumerable<TResult> SelectMany<TSource, TResult>(
        this IEnumerable<TSource> source,
        Func<TSource, IEnumerable<TResult>?> selector)
    {
        foreach (var item in source)
        {
            var results = selector(item);
            if (results != null)
            {
                foreach (var result in results)
                {
                    yield return result;
                }
            }
        }
    }
}

// Usage
List<int>? numbers = GetNumbers();
bool isEmpty = numbers.IsNullOrEmpty();

List<string?> names = GetNames();
var nonNullNames = names.WhereNotNull();

numbers?.ForEach(n => Console.WriteLine(n));
```

### Extension Methods for Specific Types
```csharp
public static class DateTimeExtensions
{
    public static bool IsWeekend(this DateTime date)
    {
        return date.DayOfWeek == DayOfWeek.Saturday ||
               date.DayOfWeek == DayOfWeek.Sunday;
    }

    public static DateTime StartOfDay(this DateTime date)
    {
        return date.Date;
    }

    public static DateTime EndOfDay(this DateTime date)
    {
        return date.Date.AddDays(1).AddTicks(-1);
    }

    public static int Age(this DateTime birthDate)
    {
        var today = DateTime.Today;
        var age = today.Year - birthDate.Year;
        if (birthDate.Date > today.AddYears(-age))
            age--;
        return age;
    }
}

// Usage
DateTime date = DateTime.Now;
bool isWeekend = date.IsWeekend();
DateTime start = date.StartOfDay();
int age = new DateTime(1990, 1, 1).Age();

public static class IntExtensions
{
    public static bool IsEven(this int value) => value % 2 == 0;
    public static bool IsOdd(this int value) => value % 2 != 0;
    public static bool IsPrime(this int value)
    {
        if (value <= 1) return false;
        if (value == 2) return true;
        if (value % 2 == 0) return false;

        for (int i = 3; i * i <= value; i += 2)
        {
            if (value % i == 0) return false;
        }
        return true;
    }
}

// Usage
bool even = 42.IsEven();
bool prime = 17.IsPrime();
```

### Extension Methods for Custom Types
```csharp
public class User
{
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}

public static class UserExtensions
{
    public static bool IsNew(this User user)
    {
        return user.CreatedAt > DateTime.UtcNow.AddDays(-30);
    }

    public static string GetDisplayName(this User user)
    {
        return string.IsNullOrEmpty(user.Name) ? user.Email : user.Name;
    }

    public static UserDto ToDto(this User user)
    {
        return new UserDto
        {
            Name = user.Name,
            Email = user.Email
        };
    }
}

// Usage
User user = GetUser();
bool isNew = user.IsNew();
string display = user.GetDisplayName();
UserDto dto = user.ToDto();
```

### Fluent Interface Extensions
```csharp
public static class FluentExtensions
{
    public static T Also<T>(this T obj, Action<T> action)
    {
        action(obj);
        return obj;
    }

    public static TResult Let<T, TResult>(this T obj, Func<T, TResult> func)
    {
        return func(obj);
    }

    public static T? TakeIf<T>(this T obj, Func<T, bool> predicate)
    {
        return predicate(obj) ? obj : default;
    }
}

// Usage
var user = new User()
    .Also(u => u.Name = "John")
    .Also(u => u.Email = "john@example.com");

int length = "Hello"
    .Let(s => s.ToUpper())
    .Let(s => s.Length);

string? value = "test"
    .TakeIf(s => s.Length > 5);  // null

public static class BuilderExtensions
{
    public static StringBuilder AppendLineIf(
        this StringBuilder builder,
        bool condition,
        string value)
    {
        if (condition)
            builder.AppendLine(value);
        return builder;
    }

    public static StringBuilder AppendJoin<T>(
        this StringBuilder builder,
        string separator,
        IEnumerable<T> values)
    {
        builder.Append(string.Join(separator, values));
        return builder;
    }
}

// Usage
var sb = new StringBuilder()
    .AppendLine("Header")
    .AppendLineIf(includeDetails, "Details")
    .AppendJoin(", ", numbers);
```

### LINQ-Style Extensions
```csharp
public static class QueryableExtensions
{
    public static IQueryable<T> WhereIf<T>(
        this IQueryable<T> query,
        bool condition,
        Expression<Func<T, bool>> predicate)
    {
        return condition ? query.Where(predicate) : query;
    }

    public static IQueryable<T> Page<T>(
        this IQueryable<T> query,
        int page,
        int pageSize)
    {
        return query.Skip((page - 1) * pageSize).Take(pageSize);
    }

    public static async Task<PagedResult<T>> ToPagedResultAsync<T>(
        this IQueryable<T> query,
        int page,
        int pageSize)
    {
        var total = await query.CountAsync();
        var items = await query.Page(page, pageSize).ToListAsync();

        return new PagedResult<T>
        {
            Items = items,
            TotalCount = total,
            Page = page,
            PageSize = pageSize
        };
    }
}

// Usage
var query = context.Users.AsQueryable()
    .WhereIf(!string.IsNullOrEmpty(searchTerm), u => u.Name.Contains(searchTerm))
    .WhereIf(minAge.HasValue, u => u.Age >= minAge.Value);

var paged = query.Page(pageNumber, pageSize);
var result = await query.ToPagedResultAsync(pageNumber, pageSize);
```

### Extension Methods for Async
```csharp
public static class TaskExtensions
{
    public static async Task<TResult> Then<T, TResult>(
        this Task<T> task,
        Func<T, TResult> func)
    {
        var result = await task;
        return func(result);
    }

    public static async Task<TResult> ThenAsync<T, TResult>(
        this Task<T> task,
        Func<T, Task<TResult>> func)
    {
        var result = await task;
        return await func(result);
    }

    public static async Task<T> WithTimeout<T>(
        this Task<T> task,
        TimeSpan timeout)
    {
        var completedTask = await Task.WhenAny(task, Task.Delay(timeout));
        if (completedTask == task)
        {
            return await task;
        }
        throw new TimeoutException();
    }

    public static async Task<T> WithRetry<T>(
        this Func<Task<T>> taskFactory,
        int retryCount,
        TimeSpan delay)
    {
        for (int i = 0; i < retryCount; i++)
        {
            try
            {
                return await taskFactory();
            }
            catch when (i < retryCount - 1)
            {
                await Task.Delay(delay);
            }
        }
        return await taskFactory();
    }
}

// Usage
var result = await GetDataAsync()
    .Then(data => data.ToUpper())
    .ThenAsync(async upper => await ProcessAsync(upper))
    .WithTimeout(TimeSpan.FromSeconds(30));

var data = await new Func<Task<string>>(() => FetchDataAsync())
    .WithRetry(3, TimeSpan.FromSeconds(1));
```

### Best Practices
```csharp
// DO: Use clear, descriptive names
public static bool IsValidEmail(this string email) { }  // Good
public static bool Valid(this string s) { }  // Bad

// DO: Keep extension methods simple
public static string Truncate(this string value, int length)
{
    return value.Length <= length ? value : value.Substring(0, length);
}

// DON'T: Add extension methods to object
// Bad - affects everything
public static void DoSomething(this object obj) { }

// DO: Group related extensions in same class
public static class StringExtensions
{
    public static bool IsNullOrEmpty(this string? value) { }
    public static string Truncate(this string value, int length) { }
    public static bool IsValidEmail(this string email) { }
}

// DON'T: Override existing methods
// Bad - confusing
public static int Length(this string value) => value.Length * 2;

// DO: Handle null appropriately
public static bool IsNullOrEmpty(this string? value)
{
    return string.IsNullOrEmpty(value);
}

// DON'T: Modify state unexpectedly
// Bad - side effect
public static string Uppercase(this StringBuilder sb)
{
    sb.Clear();
    sb.Append("MODIFIED");
    return sb.ToString();
}

// DO: Return new instances for value types
public static DateTime AddBusinessDays(this DateTime date, int days)
{
    return date.AddDays(days);  // Returns new DateTime
}

// DO: Document extension methods
/// <summary>
/// Truncates the string to the specified length.
/// </summary>
/// <param name="value">The string to truncate.</param>
/// <param name="maxLength">The maximum length.</param>
/// <returns>The truncated string.</returns>
public static string Truncate(this string value, int maxLength) { }
```

## 9. Properties and Indexers

### Overview
Properties provide a flexible mechanism to read, write, or compute values. Indexers allow instances to be indexed like arrays.

### Auto-Implemented Properties
```csharp
// Auto-property
public class User
{
    public string Name { get; set; }
    public int Age { get; set; }
}

// With default value
public class Product
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; } = 0m;
    public bool IsAvailable { get; set; } = true;
}

// Init-only property
public class ImmutableUser
{
    public string Name { get; init; }
    public string Email { get; init; }
}

var user = new ImmutableUser
{
    Name = "John",
    Email = "john@example.com"
};
// user.Name = "Jane";  // Error - init-only

// Required property (C# 11+)
public class RequiredUser
{
    public required string Name { get; init; }
    public required string Email { get; init; }
}

// Must initialize required properties
var user2 = new RequiredUser
{
    Name = "John",
    Email = "john@example.com"
};
```

### Properties with Backing Fields
```csharp
// Private backing field
public class User
{
    private string _name = string.Empty;

    public string Name
    {
        get => _name;
        set => _name = value ?? throw new ArgumentNullException(nameof(value));
    }
}

// Validation
public class Product
{
    private decimal _price;

    public decimal Price
    {
        get => _price;
        set
        {
            if (value < 0)
                throw new ArgumentException("Price cannot be negative");
            _price = value;
        }
    }
}

// Computed property
public class Rectangle
{
    public double Width { get; set; }
    public double Height { get; set; }

    public double Area => Width * Height;  // Expression-bodied

    public double Perimeter
    {
        get { return 2 * (Width + Height); }
    }
}

// Lazy initialization
public class DataService
{
    private HttpClient? _httpClient;

    public HttpClient HttpClient
    {
        get
        {
            if (_httpClient == null)
            {
                _httpClient = new HttpClient();
            }
            return _httpClient;
        }
    }

    // Or with Lazy<T>
    private readonly Lazy<HttpClient> _lazyClient = new(() => new HttpClient());
    public HttpClient Client => _lazyClient.Value;
}
```

### Property Accessors
```csharp
// Different access levels
public class User
{
    public string Name { get; set; }
    public string Email { get; private set; }  // Public get, private set
    public DateTime CreatedAt { get; init; }  // Public get, init-only set
    private string Password { get; set; }  // Private get and set
}

// Get-only property
public class Constants
{
    public string AppName => "MyApp";  // Cannot be set
    public int MaxRetries { get; } = 3;  // Can only be set in constructor

    public Constants()
    {
        MaxRetries = 5;  // OK in constructor
    }
}

// Set-only property (rare)
public class Logger
{
    private string _logPath = string.Empty;

    public string LogPath
    {
        set => _logPath = value;
    }
}
```

### Expression-Bodied Members
```csharp
public class Person
{
    private string _firstName = string.Empty;
    private string _lastName = string.Empty;

    // Expression-bodied property
    public string FullName => $"{_firstName} {_lastName}";

    // Expression-bodied getter and setter
    public string FirstName
    {
        get => _firstName;
        set => _firstName = value ?? throw new ArgumentNullException(nameof(value));
    }

    // Expression-bodied method
    public string GetGreeting() => $"Hello, {FullName}!";

    // Expression-bodied constructor
    public Person(string firstName, string lastName) =>
        (_firstName, _lastName) = (firstName, lastName);
}
```

### Indexers
```csharp
// Basic indexer
public class StringCollection
{
    private readonly List<string> _items = new();

    public string this[int index]
    {
        get => _items[index];
        set => _items[index] = value;
    }

    public int Count => _items.Count;
    public void Add(string item) => _items.Add(item);
}

// Usage
var collection = new StringCollection();
collection.Add("first");
collection.Add("second");
string item = collection[0];  // "first"
collection[1] = "modified";

// Multiple parameters
public class Matrix
{
    private readonly double[,] _data;

    public Matrix(int rows, int cols)
    {
        _data = new double[rows, cols];
    }

    public double this[int row, int col]
    {
        get => _data[row, col];
        set => _data[row, col] = value;
    }
}

// Usage
var matrix = new Matrix(3, 3);
matrix[0, 0] = 1.0;
double value = matrix[0, 0];

// String indexer
public class Configuration
{
    private readonly Dictionary<string, string> _settings = new();

    public string? this[string key]
    {
        get => _settings.TryGetValue(key, out var value) ? value : null;
        set
        {
            if (value != null)
                _settings[key] = value;
            else
                _settings.Remove(key);
        }
    }
}

// Usage
var config = new Configuration();
config["apiKey"] = "secret";
string? key = config["apiKey"];

// Read-only indexer
public class ReadOnlyCollection<T>
{
    private readonly List<T> _items;

    public ReadOnlyCollection(List<T> items)
    {
        _items = items;
    }

    public T this[int index] => _items[index];  // Get only

    public int Count => _items.Count;
}
```

### Advanced Property Patterns
```csharp
// Lazy property
public class Report
{
    private string? _cachedContent;

    public string Content
    {
        get
        {
            if (_cachedContent == null)
            {
                _cachedContent = GenerateContent();
            }
            return _cachedContent;
        }
    }

    private string GenerateContent()
    {
        // Expensive operation
        return "Report content";
    }

    public void InvalidateCache()
    {
        _cachedContent = null;
    }
}

// Property with notification
public class ObservableUser : INotifyPropertyChanged
{
    private string _name = string.Empty;

    public string Name
    {
        get => _name;
        set
        {
            if (_name != value)
            {
                _name = value;
                OnPropertyChanged();
            }
        }
    }

    public event PropertyChangedEventHandler? PropertyChanged;

    protected virtual void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

// Dependency property pattern (similar to WPF)
public class DependencyObject
{
    private readonly Dictionary<string, object?> _properties = new();

    protected T? GetValue<T>(string propertyName)
    {
        return _properties.TryGetValue(propertyName, out var value) && value is T typed
            ? typed
            : default;
    }

    protected void SetValue<T>(string propertyName, T value)
    {
        _properties[propertyName] = value;
        OnPropertyChanged(propertyName);
    }

    protected virtual void OnPropertyChanged(string propertyName) { }
}

public class CustomControl : DependencyObject
{
    public string Text
    {
        get => GetValue<string>(nameof(Text)) ?? string.Empty;
        set => SetValue(nameof(Text), value);
    }
}
```

### Best Practices
```csharp
// DO: Use auto-properties when no validation needed
public class User
{
    public string Name { get; set; } = string.Empty;
    public int Age { get; set; }
}

// DO: Use init for immutability
public record Product(string Name, decimal Price)
{
    public string Description { get; init; } = string.Empty;
}

// DO: Validate in property setters
public class Product
{
    private decimal _price;

    public decimal Price
    {
        get => _price;
        set
        {
            if (value < 0)
                throw new ArgumentException("Price cannot be negative");
            _price = value;
        }
    }
}

// DON'T: Perform expensive operations in getters
// Bad
public string Data
{
    get
    {
        return File.ReadAllText("data.txt");  // Expensive!
    }
}

// Good - cache or use method
private string? _cachedData;
public string Data => _cachedData ??= File.ReadAllText("data.txt");

// Or
public string GetData() => File.ReadAllText("data.txt");

// DO: Use expression-bodied properties for simple computed values
public string FullName => $"{FirstName} {LastName}";

// DON'T: Return arrays from properties
// Bad - caller can modify array
public int[] Numbers { get; set; }

// Good - use IReadOnlyCollection or return copy
public IReadOnlyList<int> Numbers { get; }
public int[] GetNumbers() => _numbers.ToArray();

// DO: Use private setters for internal state
public class User
{
    public string Name { get; set; }
    public DateTime CreatedAt { get; private set; }

    public User(string name)
    {
        Name = name;
        CreatedAt = DateTime.UtcNow;
    }
}

// DO: Use required for mandatory initialization (C# 11+)
public class Config
{
    public required string ApiKey { get; init; }
    public required string BaseUrl { get; init; }
}
```

## 10. Exception Handling

### Overview
Exception handling provides a structured way to handle runtime errors and exceptional conditions.

### Basic Exception Handling
```csharp
// Try-catch
try
{
    int result = Divide(10, 0);
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Cannot divide by zero: {ex.Message}");
}

// Multiple catch blocks
try
{
    ProcessData();
}
catch (FileNotFoundException ex)
{
    Console.WriteLine($"File not found: {ex.Message}");
}
catch (UnauthorizedAccessException ex)
{
    Console.WriteLine($"Access denied: {ex.Message}");
}
catch (Exception ex)
{
    Console.WriteLine($"Unexpected error: {ex.Message}");
}

// Catch with when clause
try
{
    await httpClient.GetAsync(url);
}
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    Console.WriteLine("Resource not found");
}
catch (HttpRequestException ex) when (ex.StatusCode == HttpStatusCode.Unauthorized)
{
    Console.WriteLine("Unauthorized access");
}
catch (HttpRequestException ex)
{
    Console.WriteLine($"HTTP error: {ex.Message}");
}

// Finally block
FileStream? file = null;
try
{
    file = File.OpenRead("data.txt");
    // Process file
}
catch (IOException ex)
{
    Console.WriteLine($"IO error: {ex.Message}");
}
finally
{
    file?.Close();  // Always executed
}

// Using statement (automatic disposal)
try
{
    using var file = File.OpenRead("data.txt");
    // Process file
}  // Automatically disposed
catch (IOException ex)
{
    Console.WriteLine($"IO error: {ex.Message}");
}
```

### Throwing Exceptions
```csharp
// Throw exception
public void ValidateAge(int age)
{
    if (age < 0)
    {
        throw new ArgumentException("Age cannot be negative", nameof(age));
    }
}

// Throw with inner exception
try
{
    ProcessData();
}
catch (Exception ex)
{
    throw new ApplicationException("Failed to process data", ex);
}

// Rethrow
try
{
    ProcessData();
}
catch (Exception ex)
{
    LogError(ex);
    throw;  // Preserves stack trace
}

// DON'T: throw ex (loses stack trace)
try
{
    ProcessData();
}
catch (Exception ex)
{
    LogError(ex);
    throw ex;  // Bad - resets stack trace
}

// Throw expressions (C# 7+)
public string GetName(string? input)
{
    return input ?? throw new ArgumentNullException(nameof(input));
}

public User GetUser(int id) =>
    users.Find(u => u.Id == id) ?? throw new KeyNotFoundException($"User {id} not found");
```

### Standard Exception Types
```csharp
// ArgumentException - invalid argument
public void SetAge(int age)
{
    if (age < 0 || age > 150)
        throw new ArgumentException("Age must be between 0 and 150", nameof(age));
}

// ArgumentNullException - null argument
public void ProcessUser(User user)
{
    ArgumentNullException.ThrowIfNull(user);  // C# 11+
    // or
    if (user == null)
        throw new ArgumentNullException(nameof(user));
}

// ArgumentOutOfRangeException - argument out of valid range
public void SetPercentage(int value)
{
    if (value < 0 || value > 100)
        throw new ArgumentOutOfRangeException(nameof(value), value,
            "Percentage must be between 0 and 100");
}

// InvalidOperationException - invalid state for operation
public void Start()
{
    if (_isRunning)
        throw new InvalidOperationException("Already running");
    _isRunning = true;
}

// NotSupportedException - operation not supported
public override void Write(byte[] buffer, int offset, int count)
{
    throw new NotSupportedException("Stream does not support writing");
}

// NotImplementedException - not yet implemented
public virtual void Process()
{
    throw new NotImplementedException("Subclasses must implement this method");
}

// KeyNotFoundException - dictionary key not found
public string GetValue(string key)
{
    if (!_dict.ContainsKey(key))
        throw new KeyNotFoundException($"Key '{key}' not found");
    return _dict[key];
}
```

### Custom Exceptions
```csharp
// Custom exception
public class ValidationException : Exception
{
    public ValidationException()
    {
    }

    public ValidationException(string message)
        : base(message)
    {
    }

    public ValidationException(string message, Exception innerException)
        : base(message, innerException)
    {
    }
}

// With additional properties
public class ApiException : Exception
{
    public int StatusCode { get; }
    public string? ResponseBody { get; }

    public ApiException(int statusCode, string message, string? responseBody = null)
        : base(message)
    {
        StatusCode = statusCode;
        ResponseBody = responseBody;
    }
}

// Usage
try
{
    var response = await httpClient.GetAsync(url);
    if (!response.IsSuccessStatusCode)
    {
        var body = await response.Content.ReadAsStringAsync();
        throw new ApiException((int)response.StatusCode,
            "API request failed", body);
    }
}
catch (ApiException ex)
{
    Console.WriteLine($"Status: {ex.StatusCode}, Body: {ex.ResponseBody}");
}
```

### Exception Filters
```csharp
// When clause for conditional catching
try
{
    ProcessData();
}
catch (Exception ex) when (ex.Message.Contains("timeout"))
{
    Console.WriteLine("Operation timed out");
}
catch (Exception ex) when (LogException(ex))
{
    // Never executes - LogException returns false
    // But exception is logged as side effect
}

private bool LogException(Exception ex)
{
    logger.LogError(ex, "Exception occurred");
    return false;  // Continue exception propagation
}

// Retry with filter
int retries = 3;
for (int i = 0; i < retries; i++)
{
    try
    {
        await ProcessAsync();
        break;
    }
    catch (HttpRequestException ex) when (i < retries - 1)
    {
        await Task.Delay(1000);
    }
}
```

### Async Exception Handling
```csharp
// Async exception handling
public async Task ProcessDataAsync()
{
    try
    {
        await FetchDataAsync();
    }
    catch (HttpRequestException ex)
    {
        logger.LogError(ex, "HTTP request failed");
        throw;
    }
}

// Multiple async operations
try
{
    await Task.WhenAll(
        ProcessAsync(1),
        ProcessAsync(2),
        ProcessAsync(3)
    );
}
catch (Exception ex)
{
    // Only first exception caught
    logger.LogError(ex, "At least one operation failed");
}

// Handling all exceptions
var tasks = new[]
{
    ProcessAsync(1),
    ProcessAsync(2),
    ProcessAsync(3)
};

try
{
    await Task.WhenAll(tasks);
}
catch
{
    foreach (var task in tasks.Where(t => t.IsFaulted))
    {
        foreach (var ex in task.Exception?.InnerExceptions ?? Enumerable.Empty<Exception>())
        {
            logger.LogError(ex, "Task failed");
        }
    }
}

// ConfigureAwait with exception handling
try
{
    var result = await GetDataAsync().ConfigureAwait(false);
}
catch (Exception ex)
{
    // Exception still caught properly
    logger.LogError(ex, "Operation failed");
}
```

### Best Practices
```csharp
// DO: Catch specific exceptions
// Good
try
{
    ProcessData();
}
catch (FileNotFoundException ex)
{
    Console.WriteLine("File not found");
}
catch (UnauthorizedAccessException ex)
{
    Console.WriteLine("Access denied");
}

// Bad - catches everything
try
{
    ProcessData();
}
catch (Exception ex)
{
    Console.WriteLine("Error occurred");
}

// DO: Use using for disposable resources
// Good
using var file = File.OpenRead("data.txt");
ProcessFile(file);

// Bad - manual disposal
FileStream file = null;
try
{
    file = File.OpenRead("data.txt");
    ProcessFile(file);
}
finally
{
    file?.Dispose();
}

// DON'T: Use exceptions for control flow
// Bad
try
{
    var user = users.First(u => u.Id == id);
}
catch (InvalidOperationException)
{
    return null;
}

// Good
var user = users.FirstOrDefault(u => u.Id == id);

// DO: Include relevant information in exceptions
// Good
throw new ValidationException($"Invalid email format: {email}");

// Bad
throw new ValidationException("Invalid input");

// DO: Document exceptions
/// <summary>
/// Gets a user by ID.
/// </summary>
/// <param name="id">The user ID.</param>
/// <returns>The user.</returns>
/// <exception cref="ArgumentException">Thrown when id is invalid.</exception>
/// <exception cref="KeyNotFoundException">Thrown when user not found.</exception>
public User GetUser(int id)
{
    if (id <= 0)
        throw new ArgumentException("Invalid ID", nameof(id));

    return users[id] ?? throw new KeyNotFoundException($"User {id} not found");
}

// DON'T: Catch and ignore exceptions
// Bad
try
{
    ProcessData();
}
catch
{
    // Silently ignored - very bad!
}

// Good - at minimum, log the exception
try
{
    ProcessData();
}
catch (Exception ex)
{
    logger.LogError(ex, "Failed to process data");
    throw;
}

// DO: Use ArgumentNullException.ThrowIfNull (C# 11+)
public void Process(string value)
{
    ArgumentNullException.ThrowIfNull(value);
    // Process value
}

// DO: Preserve stack trace when rethrowing
try
{
    ProcessData();
}
catch (Exception ex)
{
    LogError(ex);
    throw;  // Good - preserves stack trace
}
```

## 11. Metaprogramming

C# provides multiple metaprogramming mechanisms: attributes for declarative metadata, reflection for runtime introspection, and source generators for compile-time code generation.

### Attributes

```csharp
// Built-in attributes
[Obsolete("Use NewMethod instead", error: false)]
public void OldMethod() { }

[Conditional("DEBUG")]
public void DebugOnlyMethod() { }

[Serializable]
public class DataClass { }

// Parameter attributes
public void Process([Required] string input, [Range(1, 100)] int value) { }

// Method attributes
[MethodImpl(MethodImplOptions.AggressiveInlining)]
public int FastMethod() => 42;

// Assembly attributes (in AssemblyInfo.cs or project file)
[assembly: InternalsVisibleTo("MyApp.Tests")]

// Custom attribute definition
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method, AllowMultiple = true)]
public class AuthorizeAttribute : Attribute
{
    public string[] Roles { get; set; } = Array.Empty<string>();
    public string Policy { get; set; } = string.Empty;

    public AuthorizeAttribute() { }
    public AuthorizeAttribute(params string[] roles) => Roles = roles;
}

// Usage
[Authorize("Admin", "Manager")]
public class AdminController { }
```

### Reflection

```csharp
// Get type information
Type type = typeof(User);
Type runtimeType = user.GetType();

// Get members
PropertyInfo[] properties = type.GetProperties();
MethodInfo[] methods = type.GetMethods(BindingFlags.Public | BindingFlags.Instance);
FieldInfo[] fields = type.GetFields(BindingFlags.NonPublic | BindingFlags.Instance);

// Get and set property values
PropertyInfo nameProp = type.GetProperty("Name")!;
string name = (string)nameProp.GetValue(user)!;
nameProp.SetValue(user, "New Name");

// Invoke methods dynamically
MethodInfo method = type.GetMethod("ProcessData")!;
object? result = method.Invoke(user, new object[] { "arg1", 42 });

// Create instance dynamically
object instance = Activator.CreateInstance(type)!;
User typedInstance = (User)Activator.CreateInstance(typeof(User), "Name", 30)!;

// Generic method invocation
MethodInfo genericMethod = type.GetMethod("GenericMethod")!;
MethodInfo constructed = genericMethod.MakeGenericMethod(typeof(string));
constructed.Invoke(instance, null);

// Read attributes
var authorizeAttr = type.GetCustomAttribute<AuthorizeAttribute>();
var allAuthorize = type.GetCustomAttributes<AuthorizeAttribute>();
bool hasAttr = type.IsDefined(typeof(SerializableAttribute));
```

### Source Generators (Compile-time)

```csharp
// Source generator definition (in separate analyzer project)
[Generator]
public class AutoNotifyGenerator : IIncrementalGenerator
{
    public void Initialize(IncrementalGeneratorInitializationContext context)
    {
        // Find classes with [AutoNotify] attribute
        var classDeclarations = context.SyntaxProvider
            .ForAttributeWithMetadataName(
                "AutoNotifyAttribute",
                predicate: static (s, _) => s is ClassDeclarationSyntax,
                transform: static (ctx, _) => GetClassInfo(ctx));

        context.RegisterSourceOutput(classDeclarations, static (spc, source) =>
        {
            spc.AddSource($"{source.Name}.g.cs", GenerateCode(source));
        });
    }
}

// Usage in consuming project
[AutoNotify]
public partial class ViewModel
{
    private string _name = "";
    private int _age;
}

// Generated code (automatic)
public partial class ViewModel : INotifyPropertyChanged
{
    public event PropertyChangedEventHandler? PropertyChanged;

    public string Name
    {
        get => _name;
        set { _name = value; OnPropertyChanged(); }
    }

    public int Age
    {
        get => _age;
        set { _age = value; OnPropertyChanged(); }
    }

    protected void OnPropertyChanged([CallerMemberName] string? name = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}
```

### Expression Trees

```csharp
// Build expressions programmatically
ParameterExpression param = Expression.Parameter(typeof(User), "u");
MemberExpression property = Expression.Property(param, "Age");
ConstantExpression constant = Expression.Constant(18);
BinaryExpression comparison = Expression.GreaterThan(property, constant);

// Compile to delegate
Expression<Func<User, bool>> lambda = Expression.Lambda<Func<User, bool>>(comparison, param);
Func<User, bool> compiled = lambda.Compile();

// Use like regular delegate
bool isAdult = compiled(user);

// Parse existing expressions
Expression<Func<User, bool>> expr = u => u.Age > 18;
var visitor = new CustomExpressionVisitor();
visitor.Visit(expr);
```

### See Also

- `patterns-metaprogramming-dev` - Cross-language metaprogramming patterns

---

## 12. Build and Dependencies

.NET uses the SDK-style project system with `csproj` files, NuGet for package management, and MSBuild for building.

### Project File (csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <LangVersion>latest</LangVersion>

    <!-- Output settings -->
    <OutputType>Exe</OutputType>
    <AssemblyName>MyApp</AssemblyName>
    <RootNamespace>MyApp</RootNamespace>

    <!-- Package metadata (for libraries) -->
    <PackageId>MyCompany.MyLibrary</PackageId>
    <Version>1.0.0</Version>
    <Authors>Your Name</Authors>
    <Description>A useful library</Description>
    <PackageTags>utility;helper</PackageTags>
    <RepositoryUrl>https://github.com/user/repo</RepositoryUrl>
    <PackageLicenseExpression>MIT</PackageLicenseExpression>
  </PropertyGroup>

  <!-- Dependencies -->
  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Serilog" Version="3.1.1" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
  </ItemGroup>

  <!-- Project references -->
  <ItemGroup>
    <ProjectReference Include="..\MyLibrary\MyLibrary.csproj" />
  </ItemGroup>

  <!-- Conditional references -->
  <ItemGroup Condition="'$(Configuration)' == 'Debug'">
    <PackageReference Include="Microsoft.Extensions.Logging.Debug" Version="8.0.0" />
  </ItemGroup>

</Project>
```

### dotnet CLI Commands

```bash
# Create projects
dotnet new console -n MyApp           # Console app
dotnet new classlib -n MyLib          # Class library
dotnet new webapi -n MyApi            # Web API
dotnet new sln -n MySolution          # Solution file
dotnet sln add MyApp/MyApp.csproj     # Add project to solution

# Package management
dotnet add package Newtonsoft.Json    # Add package
dotnet add package Serilog --version 3.1.1  # Specific version
dotnet remove package Newtonsoft.Json # Remove package
dotnet list package                   # List packages
dotnet list package --outdated        # Check for updates
dotnet restore                        # Restore packages

# Build and run
dotnet build                          # Build project
dotnet build -c Release              # Release build
dotnet run                            # Build and run
dotnet run --project MyApp            # Run specific project
dotnet watch run                      # Run with hot reload

# Testing
dotnet test                           # Run tests
dotnet test --filter "Category=Unit" # Filter tests
dotnet test --collect:"XPlat Code Coverage"  # With coverage

# Publishing
dotnet publish -c Release             # Publish for deployment
dotnet publish -c Release -r win-x64 --self-contained  # Self-contained
dotnet publish -c Release -r linux-x64 -p:PublishSingleFile=true  # Single file

# NuGet publishing
dotnet pack -c Release                # Create NuGet package
dotnet nuget push MyLib.1.0.0.nupkg --api-key KEY --source https://api.nuget.org/v3/index.json
```

### NuGet Configuration (nuget.config)

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
    <add key="private" value="https://pkgs.mycompany.com/v3/index.json" />
  </packageSources>

  <packageSourceCredentials>
    <private>
      <add key="Username" value="user" />
      <add key="ClearTextPassword" value="password" />
    </private>
  </packageSourceCredentials>

  <packageSourceMapping>
    <packageSource key="nuget.org">
      <package pattern="*" />
    </packageSource>
    <packageSource key="private">
      <package pattern="MyCompany.*" />
    </packageSource>
  </packageSourceMapping>
</configuration>
```

### Directory.Build.props (Shared Settings)

```xml
<!-- Directory.Build.props - applies to all projects in directory tree -->
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>

    <!-- Versioning -->
    <Version>1.0.0</Version>
    <Company>MyCompany</Company>
    <Copyright>Copyright © 2024 MyCompany</Copyright>
  </PropertyGroup>

  <!-- Shared analyzers -->
  <ItemGroup>
    <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
  </ItemGroup>
</Project>
```

### Global.json (SDK Version)

```json
{
  "sdk": {
    "version": "8.0.100",
    "rollForward": "latestMinor",
    "allowPrerelease": false
  }
}
```

---

## 13. Testing

.NET has multiple testing frameworks. xUnit is the most popular, with NUnit and MSTest as alternatives. Moq and NSubstitute provide mocking, while FluentAssertions improves readability.

### xUnit

```csharp
// xUnit test class (no attribute needed)
public class CalculatorTests
{
    private readonly Calculator _calculator = new();

    [Fact]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        int a = 2, b = 3;

        // Act
        int result = _calculator.Add(a, b);

        // Assert
        Assert.Equal(5, result);
    }

    [Theory]
    [InlineData(1, 1, 2)]
    [InlineData(2, 3, 5)]
    [InlineData(-1, 1, 0)]
    public void Add_MultipleInputs_ReturnsCorrectSum(int a, int b, int expected)
    {
        Assert.Equal(expected, _calculator.Add(a, b));
    }

    [Theory]
    [MemberData(nameof(TestData))]
    public void Add_FromMemberData_Works(int a, int b, int expected)
    {
        Assert.Equal(expected, _calculator.Add(a, b));
    }

    public static IEnumerable<object[]> TestData =>
        new List<object[]>
        {
            new object[] { 1, 1, 2 },
            new object[] { 5, 5, 10 }
        };

    [Fact]
    public void Divide_ByZero_ThrowsException()
    {
        Assert.Throws<DivideByZeroException>(() => _calculator.Divide(1, 0));
    }

    [Fact]
    public async Task FetchData_ValidUrl_ReturnsData()
    {
        var result = await _calculator.FetchDataAsync("https://api.example.com");
        Assert.NotNull(result);
        Assert.NotEmpty(result);
    }
}

// Test fixtures (shared setup)
public class DatabaseTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public DatabaseTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void Query_ReturnsData()
    {
        var result = _fixture.Database.Query("SELECT 1");
        Assert.NotNull(result);
    }
}

public class DatabaseFixture : IDisposable
{
    public Database Database { get; }

    public DatabaseFixture()
    {
        Database = new Database();
        Database.Initialize();
    }

    public void Dispose() => Database.Dispose();
}
```

### NUnit

```csharp
[TestFixture]
public class CalculatorTests
{
    private Calculator _calculator = null!;

    [SetUp]
    public void Setup()
    {
        _calculator = new Calculator();
    }

    [TearDown]
    public void TearDown()
    {
        // Cleanup
    }

    [Test]
    public void Add_TwoNumbers_ReturnsSum()
    {
        Assert.That(_calculator.Add(2, 3), Is.EqualTo(5));
    }

    [TestCase(1, 1, ExpectedResult = 2)]
    [TestCase(2, 3, ExpectedResult = 5)]
    public int Add_ReturnsSum(int a, int b)
    {
        return _calculator.Add(a, b);
    }

    [Test]
    public void Divide_ByZero_Throws()
    {
        Assert.Throws<DivideByZeroException>(() => _calculator.Divide(1, 0));
    }

    [Test]
    [Category("Integration")]
    [Ignore("Requires database")]
    public void Integration_Test() { }
}
```

### MSTest

```csharp
[TestClass]
public class CalculatorTests
{
    private Calculator _calculator = null!;

    [TestInitialize]
    public void Setup()
    {
        _calculator = new Calculator();
    }

    [TestMethod]
    public void Add_TwoNumbers_ReturnsSum()
    {
        Assert.AreEqual(5, _calculator.Add(2, 3));
    }

    [DataTestMethod]
    [DataRow(1, 1, 2)]
    [DataRow(2, 3, 5)]
    public void Add_MultipleInputs(int a, int b, int expected)
    {
        Assert.AreEqual(expected, _calculator.Add(a, b));
    }

    [TestMethod]
    [ExpectedException(typeof(DivideByZeroException))]
    public void Divide_ByZero_Throws()
    {
        _calculator.Divide(1, 0);
    }
}
```

### Moq (Mocking)

```csharp
// Interface to mock
public interface IUserRepository
{
    User? GetById(int id);
    Task<User?> GetByIdAsync(int id);
    void Save(User user);
}

// Test with Moq
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _mockRepo;
    private readonly UserService _service;

    public UserServiceTests()
    {
        _mockRepo = new Mock<IUserRepository>();
        _service = new UserService(_mockRepo.Object);
    }

    [Fact]
    public void GetUser_ValidId_ReturnsUser()
    {
        // Setup
        var user = new User { Id = 1, Name = "John" };
        _mockRepo.Setup(r => r.GetById(1)).Returns(user);

        // Act
        var result = _service.GetUser(1);

        // Assert
        Assert.Equal("John", result?.Name);
        _mockRepo.Verify(r => r.GetById(1), Times.Once);
    }

    [Fact]
    public async Task GetUserAsync_ReturnsUser()
    {
        var user = new User { Id = 1, Name = "John" };
        _mockRepo.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(user);

        var result = await _service.GetUserAsync(1);

        Assert.NotNull(result);
    }

    [Fact]
    public void SaveUser_CallsRepository()
    {
        var user = new User { Name = "John" };

        _service.SaveUser(user);

        _mockRepo.Verify(r => r.Save(It.Is<User>(u => u.Name == "John")), Times.Once);
    }

    [Fact]
    public void GetUser_WhenNotFound_ReturnsNull()
    {
        _mockRepo.Setup(r => r.GetById(It.IsAny<int>())).Returns((User?)null);

        var result = _service.GetUser(999);

        Assert.Null(result);
    }

    [Fact]
    public void SequencedReturns()
    {
        _mockRepo.SetupSequence(r => r.GetById(It.IsAny<int>()))
            .Returns(new User { Name = "First" })
            .Returns(new User { Name = "Second" })
            .Throws<InvalidOperationException>();
    }
}
```

### FluentAssertions

```csharp
using FluentAssertions;

[Fact]
public void User_ShouldHaveCorrectProperties()
{
    var user = new User { Name = "John", Age = 30 };

    user.Name.Should().Be("John");
    user.Age.Should().BeGreaterThan(18).And.BeLessThan(100);
    user.Email.Should().BeNullOrEmpty();
}

[Fact]
public void Collection_Assertions()
{
    var numbers = new[] { 1, 2, 3, 4, 5 };

    numbers.Should().HaveCount(5);
    numbers.Should().Contain(3);
    numbers.Should().BeInAscendingOrder();
    numbers.Should().OnlyContain(n => n > 0);
}

[Fact]
public void Exception_Assertions()
{
    Action act = () => throw new InvalidOperationException("Test error");

    act.Should().Throw<InvalidOperationException>()
       .WithMessage("*error*");
}

[Fact]
public async Task Async_Assertions()
{
    Func<Task> act = async () => await FailingMethodAsync();

    await act.Should().ThrowAsync<HttpRequestException>();
}

[Fact]
public void Object_Comparison()
{
    var user1 = new User { Name = "John", Age = 30 };
    var user2 = new User { Name = "John", Age = 30 };

    user1.Should().BeEquivalentTo(user2);  // Deep comparison
    user1.Should().BeEquivalentTo(user2, options =>
        options.Excluding(u => u.CreatedAt));  // Exclude property
}

[Fact]
public void Execution_Time()
{
    Action act = () => Thread.Sleep(100);

    act.ExecutionTime().Should().BeLessThan(200.Milliseconds());
}
```

### Running Tests

```bash
# Run all tests
dotnet test

# Run with verbosity
dotnet test --logger "console;verbosity=detailed"

# Filter tests
dotnet test --filter "FullyQualifiedName~CalculatorTests"
dotnet test --filter "Category=Unit"
dotnet test --filter "TestCategory!=Integration"

# Code coverage
dotnet test --collect:"XPlat Code Coverage"
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=opencover

# Generate report
reportgenerator -reports:coverage.xml -targetdir:coveragereport
```

### Test Organization

```
MyApp.sln
├── src/
│   ├── MyApp/
│   │   └── MyApp.csproj
│   └── MyApp.Core/
│       └── MyApp.Core.csproj
└── tests/
    ├── MyApp.Tests/              # Unit tests
    │   └── MyApp.Tests.csproj
    ├── MyApp.IntegrationTests/   # Integration tests
    │   └── MyApp.IntegrationTests.csproj
    └── MyApp.Tests.Common/       # Shared test utilities
        └── MyApp.Tests.Common.csproj
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Async/await, channels, threads
- `patterns-serialization-dev` - JSON, validation, struct tags
- `patterns-metaprogramming-dev` - Decorators, macros, annotations

---

## Skill Routing

### When to Use This Skill
- Writing C# code in any .NET application
- Working with modern C# language features (C# 8+)
- Implementing LINQ queries
- Asynchronous programming with async/await
- Creating immutable data structures with records
- Pattern matching scenarios
- Generic programming
- Extension methods for code reusability

### Related Skills
- **lang-dotnet-web-dev** - ASP.NET Core, Blazor, Web APIs
- **lang-dotnet-data-dev** - Entity Framework Core, Dapper, ADO.NET
- **lang-xaml-dev** - WPF, UWP, MAUI
- **testing-dotnet-dev** - xUnit, NUnit, MSTest
- **lang-fsharp-dev** - F# functional programming

### Complementary Skills
- **git-workflow** - Version control and collaboration
- **docker-dev** - Containerization
- **azure-dev** - Azure services and deployment
- **api-design** - RESTful API design principles

## Additional Resources

### Official Documentation
- C# Language Reference: https://docs.microsoft.com/en-us/dotnet/csharp/
- .NET API Browser: https://docs.microsoft.com/en-us/dotnet/api/
- C# Programming Guide: https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/

### Learning Resources
- What's New in C#: https://docs.microsoft.com/en-us/dotnet/csharp/whats-new/
- C# Coding Conventions: https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions
- Async Best Practices: https://docs.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming

### Tools
- Visual Studio: https://visualstudio.microsoft.com/
- Visual Studio Code: https://code.visualstudio.com/
- JetBrains Rider: https://www.jetbrains.com/rider/
- LINQPad: https://www.linqpad.net/

## Summary

This skill covers foundational C# programming patterns and language features essential for modern C# development. Key areas include:

1. **Nullable Reference Types** - Prevent null reference exceptions with compile-time null safety
2. **LINQ** - Query and manipulate collections with both query and method syntax
3. **Async/Await** - Write efficient asynchronous code with Task-based patterns
4. **Records** - Create immutable value types with concise syntax
5. **Pattern Matching** - Express complex conditional logic clearly
6. **Delegates and Events** - Implement callbacks and event-driven patterns
7. **Generics** - Write reusable, type-safe code
8. **Extension Methods** - Add functionality to existing types
9. **Properties and Indexers** - Encapsulate data access
10. **Exception Handling** - Handle errors gracefully and reliably

Apply these patterns consistently for maintainable, robust C# applications. For specialized scenarios (web development, data access, UI), refer to the related skills listed above.
