---
name: optional
description: |
  Use when implementing the Optional/Maybe pattern in C# to eliminate null reference exceptions and make value absence explicit in the type system.
  USE FOR: Optional<T> type implementation, null elimination patterns, monadic optional chaining, safe value access patterns, API design with explicit optionality
  DO NOT USE FOR: full FP library with Either/Try/collections (use language-ext), lightweight Maybe with NuGet package (use jflepp-maybe), F# Option type (use fsharp)
license: MIT
metadata:
  displayName: "Optional Pattern"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "Optional GitHub Repository"
    url: "https://github.com/nlkl/Optional"
  - title: "Optional NuGet Package"
    url: "https://www.nuget.org/packages/Optional"
---

# Optional Pattern in C#

## Overview
The Optional (or Maybe) pattern represents values that may or may not be present, replacing null with an explicit type-safe container. Instead of returning `null` and hoping callers check for it, methods return `Optional<T>` which forces consumers to handle both the "has value" and "no value" cases. This eliminates null reference exceptions, makes APIs self-documenting, and enables monadic composition through Map, Bind, and Match operations. The pattern can be implemented as a lightweight struct or used via libraries like the `Optional` NuGet package.

## NuGet Packages
- `Optional` -- Nils Luck's Optional<T> library with Map/FlatMap/Filter
- `JFlepp.Maybe` -- lightweight alternative (see jflepp-maybe skill)
- `LanguageExt.Core` -- comprehensive FP library with Option<T> (see language-ext skill)

## Implementing Optional<T>
```csharp
public readonly struct Optional<T> : IEquatable<Optional<T>>
{
    private readonly T _value;
    private readonly bool _hasValue;

    private Optional(T value)
    {
        _value = value;
        _hasValue = true;
    }

    public static Optional<T> Some(T value) =>
        value is null
            ? throw new ArgumentNullException(nameof(value))
            : new Optional<T>(value);

    public static Optional<T> None => default;

    public bool HasValue => _hasValue;

    public TResult Match<TResult>(Func<T, TResult> some, Func<TResult> none) =>
        _hasValue ? some(_value) : none();

    public void Match(Action<T> some, Action none)
    {
        if (_hasValue) some(_value);
        else none();
    }

    public Optional<TResult> Map<TResult>(Func<T, TResult> mapper) =>
        _hasValue ? Optional<TResult>.Some(mapper(_value)) : Optional<TResult>.None;

    public Optional<TResult> Bind<TResult>(Func<T, Optional<TResult>> binder) =>
        _hasValue ? binder(_value) : Optional<TResult>.None;

    public Optional<T> Filter(Func<T, bool> predicate) =>
        _hasValue && predicate(_value) ? this : None;

    public T OrElse(T defaultValue) =>
        _hasValue ? _value : defaultValue;

    public T OrElse(Func<T> defaultFactory) =>
        _hasValue ? _value : defaultFactory();

    public T OrThrow(Func<Exception> exceptionFactory) =>
        _hasValue ? _value : throw exceptionFactory();

    // Equality
    public bool Equals(Optional<T> other) =>
        _hasValue == other._hasValue &&
        (!_hasValue || EqualityComparer<T>.Default.Equals(_value, other._value));

    public override bool Equals(object? obj) =>
        obj is Optional<T> other && Equals(other);

    public override int GetHashCode() =>
        _hasValue ? EqualityComparer<T>.Default.GetHashCode(_value!) : 0;

    public static bool operator ==(Optional<T> left, Optional<T> right) => left.Equals(right);
    public static bool operator !=(Optional<T> left, Optional<T> right) => !left.Equals(right);

    public override string ToString() =>
        _hasValue ? $"Some({_value})" : "None";
}
```

## LINQ Support
```csharp
// Enable LINQ query syntax by implementing Select and SelectMany
public static class OptionalLinqExtensions
{
    public static Optional<TResult> Select<T, TResult>(
        this Optional<T> source, Func<T, TResult> selector) =>
        source.Map(selector);

    public static Optional<TResult> SelectMany<T, TIntermediate, TResult>(
        this Optional<T> source,
        Func<T, Optional<TIntermediate>> bind,
        Func<T, TIntermediate, TResult> project) =>
        source.Bind(a => bind(a).Map(b => project(a, b)));

    public static Optional<T> Where<T>(
        this Optional<T> source, Func<T, bool> predicate) =>
        source.Filter(predicate);
}

// LINQ usage
Optional<string> city =
    from user in FindUser(userId)
    from address in GetAddress(user)
    from cityName in GetCity(address)
    where cityName.Length > 0
    select cityName.ToUpperInvariant();
```

## Conversion Extensions
```csharp
public static class OptionalConversions
{
    // From nullable reference types
    public static Optional<T> ToOptional<T>(this T? value) where T : class =>
        value is not null ? Optional<T>.Some(value) : Optional<T>.None;

    // From nullable value types
    public static Optional<T> ToOptional<T>(this T? value) where T : struct =>
        value.HasValue ? Optional<T>.Some(value.Value) : Optional<T>.None;

    // From dictionary lookups
    public static Optional<TValue> TryGet<TKey, TValue>(
        this IDictionary<TKey, TValue> dict, TKey key) =>
        dict.TryGetValue(key, out var value)
            ? Optional<TValue>.Some(value)
            : Optional<TValue>.None;

    // From parsing
    public static Optional<int> TryParseInt(string input) =>
        int.TryParse(input, out var result)
            ? Optional<int>.Some(result)
            : Optional<int>.None;

    public static Optional<Guid> TryParseGuid(string input) =>
        Guid.TryParse(input, out var result)
            ? Optional<Guid>.Some(result)
            : Optional<Guid>.None;

    // To nullable
    public static T? ToNullable<T>(this Optional<T> optional) where T : class =>
        optional.Match(some: v => v, none: () => null!);
}
```

## Repository Pattern with Optional
```csharp
public interface IUserRepository
{
    Optional<User> FindById(Guid id);
    Optional<User> FindByEmail(string email);
    IReadOnlyList<User> FindAll();
}

public class UserRepository : IUserRepository
{
    private readonly AppDbContext _db;

    public UserRepository(AppDbContext db) => _db = db;

    public Optional<User> FindById(Guid id) =>
        _db.Users.Find(id).ToOptional();

    public Optional<User> FindByEmail(string email) =>
        _db.Users.FirstOrDefault(u => u.Email == email).ToOptional();

    public IReadOnlyList<User> FindAll() =>
        _db.Users.AsNoTracking().ToList();
}
```

## Service Layer with Optional Chaining
```csharp
public class UserService
{
    private readonly IUserRepository _users;
    private readonly IOrderRepository _orders;

    public UserService(IUserRepository users, IOrderRepository orders)
    {
        _users = users;
        _orders = orders;
    }

    public Optional<UserProfile> GetProfile(Guid userId) =>
        _users.FindById(userId)
            .Map(user => new UserProfile(
                user.Id,
                user.Name,
                user.Email,
                user.CreatedAt));

    public Optional<OrderSummary> GetLatestOrder(Guid userId) =>
        from user in _users.FindById(userId)
        from order in _orders.FindLatestByCustomer(user.Id)
        select new OrderSummary(order.Id, order.Total, order.Status);

    public string GetDisplayName(Guid userId) =>
        _users.FindById(userId)
            .Map(u => u.DisplayName)
            .Filter(name => !string.IsNullOrWhiteSpace(name))
            .OrElse("Anonymous User");
}
```

## API Endpoint Integration
```csharp
app.MapGet("/users/{id:guid}", (Guid id, IUserRepository repo) =>
    repo.FindById(id).Match<IResult>(
        some: user => Results.Ok(new UserDto(user.Id, user.Name, user.Email)),
        none: () => Results.NotFound()));

app.MapGet("/users/{id:guid}/orders/latest", (Guid id, UserService service) =>
    service.GetLatestOrder(id).Match<IResult>(
        some: order => Results.Ok(order),
        none: () => Results.NotFound()));

// Multiple optional lookups
app.MapGet("/users/{userId:guid}/orders/{orderId:guid}",
    (Guid userId, Guid orderId, IUserRepository users, IOrderRepository orders) =>
{
    var result =
        from user in users.FindById(userId)
        from order in orders.FindById(orderId)
        where order.CustomerId == user.Id
        select new { user.Name, order.Id, order.Total };

    return result.Match<IResult>(
        some: r => Results.Ok(r),
        none: () => Results.NotFound());
});
```

## Optional vs Nullable vs Exception

| Approach | Represents Absence | Forces Handling | Composable | Error Info |
|----------|-------------------|----------------|------------|------------|
| `Optional<T>` | Type-safe, explicit | Yes (Match) | Yes (Map/Bind) | None (value absent) |
| `T?` (nullable) | Compiler warning | Partial (NRT warnings) | No | None |
| `null` | Runtime error risk | No | No | NullReferenceException |
| Exception | Thrown at runtime | Via try/catch | No | Stack trace |
| `Either<L,R>` | Left value | Yes (Match) | Yes (Map/Bind) | Typed error |

## Using the Optional NuGet Package
```csharp
// dotnet add package Optional
using Optional;
using Optional.Unsafe;

// Creating values
Option<string> some = "hello".Some();
Option<string> none = Option.None<string>();

// From nullable
Option<string> fromNull = nullableString.SomeNotNull();

// Map, FlatMap, Filter
var result = some
    .Map(s => s.ToUpper())
    .Filter(s => s.Length > 3)
    .FlatMap(s => TryParseSomething(s));

// Match
string output = result.Match(
    some: value => $"Got: {value}",
    none: () => "Nothing");

// WithException for converting to Either-like
Option<string, FormatException> parsed = input
    .SomeWhen(s => !string.IsNullOrEmpty(s), () => new FormatException("Empty input"))
    .FlatMap(s => s.SomeWhen(
        x => x.All(char.IsLetterOrDigit),
        () => new FormatException("Invalid characters")));
```

## Best Practices
- Return `Optional<T>` from methods that may not find a value (repository lookups, dictionary gets, parsing) to make absence explicit in the return type.
- Implement `Optional<T>` as a `readonly struct` to avoid heap allocations and make the None case zero-cost.
- Use `Match` with both `some` and `none` handlers as the primary way to extract values, ensuring both cases are always handled.
- Use `Map` for transforming the inner value and `Bind` (or `FlatMap`) for chaining operations that themselves return Optional; never nest Map calls.
- Use `Filter` to convert Some to None based on a condition, which is cleaner than matching and re-wrapping.
- Convert nullable types to Optional at system boundaries (database results, API responses) and work with Optional internally throughout the application.
- Use LINQ query syntax for chains of more than two Bind operations to maintain readability.
- Use `OrElse` with a default value only at the edges of the system (API responses, UI rendering); keep Optional propagating through the core logic.
- Avoid calling `.Value` or similar unsafe accessors; always use `Match`, `Map`, or `OrElse` for safe access.
- Choose between `Optional` (self-implemented or NuGet), `JFlepp.Maybe`, and `language-ext` based on your needs: custom struct for zero-dependency, JFlepp for minimal library, language-ext for full FP ecosystem.
