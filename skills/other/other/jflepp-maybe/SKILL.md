---
name: jflepp-maybe
description: |
  Use when handling optional values with JFlepp.Maybe, a lightweight Maybe/Option monad library for C#.
  USE FOR: optional value handling with Maybe<T>, null elimination, monadic chaining of optional values, LINQ query syntax over optional values
  DO NOT USE FOR: full functional programming library (use language-ext), complex error handling with error types (use Result/Either), parser combinators (use pidgin)
license: MIT
metadata:
  displayName: "JFlepp.Maybe"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "JFlepp.Maybe GitHub Repository"
    url: "https://github.com/fl3pp/JFlepp.Maybe"
  - title: "JFlepp.Maybe NuGet Package"
    url: "https://www.nuget.org/packages/JFlepp.Maybe"
---

# JFlepp.Maybe

## Overview
JFlepp.Maybe is a lightweight .NET library providing a `Maybe<T>` type for representing optional values without using null. It implements the Maybe monad with `Select` (map), `SelectMany` (bind), and `Where` (filter) operations, enabling LINQ query syntax over optional values. The library is intentionally minimal, focusing on correct optional value semantics with a small API surface.

## NuGet Package
- `JFlepp.Maybe` -- core Maybe<T> type

## Basic Usage
```csharp
using JFlepp.Maybe;

// Creating Maybe values
Maybe<int> someValue = Maybe.Some(42);
Maybe<int> noValue = Maybe.None<int>();

// Check for value
if (someValue.HasValue)
{
    Console.WriteLine($"Value: {someValue.Value}");
}

// Match to handle both cases
string result = someValue.Match(
    some: value => $"Found: {value}",
    none: () => "Not found");

// OrElse for default values
int withDefault = noValue.OrElse(0); // 0
int withLazy = noValue.OrElse(() => ComputeExpensiveDefault()); // lazy evaluation
```

## Map and Bind
```csharp
using JFlepp.Maybe;

// Map: transform the inner value if present
Maybe<string> maybeName = Maybe.Some("Alice");
Maybe<int> nameLength = maybeName.Select(name => name.Length);
// nameLength = Some(5)

Maybe<string> noName = Maybe.None<string>();
Maybe<int> noLength = noName.Select(name => name.Length);
// noLength = None

// Bind (SelectMany): chain operations that return Maybe
Maybe<User> FindUser(int id) =>
    users.ContainsKey(id)
        ? Maybe.Some(users[id])
        : Maybe.None<User>();

Maybe<Address> GetAddress(User user) =>
    user.Address is not null
        ? Maybe.Some(user.Address)
        : Maybe.None<Address>();

Maybe<string> GetCity(Address address) =>
    !string.IsNullOrEmpty(address.City)
        ? Maybe.Some(address.City)
        : Maybe.None<string>();

// Chain with SelectMany
Maybe<string> userCity = FindUser(123)
    .SelectMany(user => GetAddress(user))
    .SelectMany(address => GetCity(address));
```

## LINQ Query Syntax
```csharp
using JFlepp.Maybe;

// LINQ query syntax for readable chaining
Maybe<string> cityName =
    from user in FindUser(123)
    from address in GetAddress(user)
    from city in GetCity(address)
    select city.ToUpperInvariant();

// With intermediate transformations
Maybe<OrderSummary> summary =
    from customer in FindCustomer(customerId)
    from order in GetLatestOrder(customer.Id)
    from total in CalculateTotal(order)
    where total > 0
    select new OrderSummary(customer.Name, order.Id, total);
```

## Where (Filter)
```csharp
using JFlepp.Maybe;

// Filter: keep value only if predicate is true
Maybe<int> positive = Maybe.Some(42).Where(x => x > 0); // Some(42)
Maybe<int> filtered = Maybe.Some(-5).Where(x => x > 0);  // None

// Combining filter with map
Maybe<string> validEmail = Maybe.Some("user@example.com")
    .Where(e => e.Contains('@'))
    .Select(e => e.ToLowerInvariant());
```

## Converting from Nullable Types
```csharp
using JFlepp.Maybe;

// Extension methods for nullable conversion
public static class MaybeExtensions
{
    public static Maybe<T> ToMaybe<T>(this T? value) where T : class
        => value is not null ? Maybe.Some(value) : Maybe.None<T>();

    public static Maybe<T> ToMaybe<T>(this T? value) where T : struct
        => value.HasValue ? Maybe.Some(value.Value) : Maybe.None<T>();
}

// Usage with nullable returns
string? nullableName = GetNameOrNull();
Maybe<string> maybeName = nullableName.ToMaybe();

int? nullableAge = GetAgeOrNull();
Maybe<int> maybeAge = nullableAge.ToMaybe();

// Converting Dictionary lookups
public static Maybe<TValue> TryGetMaybe<TKey, TValue>(
    this IDictionary<TKey, TValue> dictionary, TKey key)
    => dictionary.TryGetValue(key, out var value)
        ? Maybe.Some(value)
        : Maybe.None<TValue>();

Maybe<Customer> customer = customerDictionary.TryGetMaybe("cust-123");
```

## Practical Repository Example
```csharp
using JFlepp.Maybe;

public interface ICustomerRepository
{
    Maybe<Customer> FindById(Guid id);
    Maybe<Customer> FindByEmail(string email);
}

public class CustomerRepository : ICustomerRepository
{
    private readonly AppDbContext _db;

    public CustomerRepository(AppDbContext db) => _db = db;

    public Maybe<Customer> FindById(Guid id)
    {
        var customer = _db.Customers.Find(id);
        return customer is not null
            ? Maybe.Some(customer)
            : Maybe.None<Customer>();
    }

    public Maybe<Customer> FindByEmail(string email)
    {
        var customer = _db.Customers.FirstOrDefault(c => c.Email == email);
        return customer is not null
            ? Maybe.Some(customer)
            : Maybe.None<Customer>();
    }
}

// Usage in a service
public class CustomerService
{
    private readonly ICustomerRepository _repository;

    public CustomerService(ICustomerRepository repository)
        => _repository = repository;

    public string GetCustomerGreeting(Guid id) =>
        _repository.FindById(id)
            .Select(c => $"Hello, {c.Name}!")
            .OrElse("Customer not found");

    public Maybe<decimal> GetCustomerBalance(Guid id) =>
        _repository.FindById(id)
            .Select(c => c.Balance)
            .Where(balance => balance >= 0);
}
```

## API Endpoint Integration
```csharp
app.MapGet("/customers/{id:guid}", (Guid id, ICustomerRepository repo) =>
{
    return repo.FindById(id)
        .Match<IResult>(
            some: customer => Results.Ok(customer),
            none: () => Results.NotFound());
});

app.MapGet("/customers/{id:guid}/address/city", (Guid id, ICustomerRepository repo) =>
{
    var city =
        from customer in repo.FindById(id)
        from address in GetAddress(customer)
        from cityName in GetCity(address)
        select cityName;

    return city.Match<IResult>(
        some: c => Results.Ok(new { city = c }),
        none: () => Results.NotFound());
});
```

## Maybe vs Alternatives

| Feature | JFlepp.Maybe | language-ext Option | C# Nullable |
|---------|-------------|-------------------|-------------|
| Type | `Maybe<T>` | `Option<T>` | `T?` |
| LINQ support | Yes | Yes | No |
| Value type | Class-based | Struct-based | Compiler feature |
| API surface | Minimal | Extensive | N/A |
| Library size | Tiny | Large (full FP) | Built-in |
| Match method | Yes | Yes | No (manual null check) |
| Best for | Lightweight optional | Full FP ecosystem | Simple null safety |

## Best Practices
- Use `Maybe.Some(value)` for present values and `Maybe.None<T>()` for absent values; never pass null where a `Maybe<T>` is expected.
- Use `Select` (map) to transform the inner value and `SelectMany` (bind) to chain operations that themselves return `Maybe<T>`.
- Prefer LINQ query syntax (`from ... in ... select`) when chaining more than two `SelectMany` operations for improved readability.
- Use `OrElse` with a default value at the boundary of your application (e.g., in API endpoints or UI code) to convert from `Maybe<T>` to a concrete value.
- Use `Where` to filter optional values based on a predicate, converting `Some` to `None` when the condition is not met.
- Write extension methods to convert between nullable types (`T?`) and `Maybe<T>` for interop with existing APIs that return null.
- Return `Maybe<T>` from repository and service methods instead of nullable types to make the possibility of absence explicit in the type signature.
- Use `Match` with both `some` and `none` handlers to ensure both cases are handled explicitly, preventing accidental null-like access patterns.
- Avoid calling `.Value` directly without checking `.HasValue` first; prefer `Match`, `Select`, or `OrElse` for safe access.
- Keep the `JFlepp.Maybe` library for simple optional value scenarios; if you need `Either`, `Try`, or full monadic composition, consider language-ext instead.
