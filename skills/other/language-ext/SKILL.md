---
name: language-ext
description: |
  Use when applying comprehensive functional programming patterns in C# with language-ext, including Option, Either, Try, immutable collections, and monadic composition.
  USE FOR: Option<T> for null elimination, Either<L,R> for typed error handling, Try<T> for exception handling, immutable collections, monadic LINQ composition, Eff/Aff for effectful programming
  DO NOT USE FOR: lightweight Maybe only (use jflepp-maybe), F# language features (use fsharp), parser combinators (use pidgin), simple nullable handling without monadic composition
license: MIT
metadata:
  displayName: "language-ext"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility: claude, copilot, cursor
references:
  - title: "language-ext GitHub Repository"
    url: "https://github.com/louthy/language-ext"
  - title: "LanguageExt.Core NuGet Package"
    url: "https://www.nuget.org/packages/LanguageExt.Core"
  - title: "language-ext Wiki"
    url: "https://github.com/louthy/language-ext/wiki"
---

# language-ext

## Overview
language-ext is a comprehensive functional programming library for C# by Paul Louth. It brings Haskell/F#-inspired types and patterns to C#, including `Option<T>` (optional values), `Either<L, R>` (success/failure with typed errors), `Try<T>` (safe exception handling), `Validation<F, S>` (accumulating errors), immutable persistent collections (`Lst<T>`, `Map<K,V>`, `Set<T>`), and effectful computation types (`Eff<T>`, `Aff<T>`). All types support LINQ query syntax for monadic composition.

## NuGet Packages
- `LanguageExt.Core` -- core types (Option, Either, Try, collections)
- `LanguageExt.Transformers` -- monad transformers
- `LanguageExt.Sys` -- system effect types (console, file, etc.)

## Option<T>
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

// Creating options
Option<int> some = Some(42);
Option<int> none = None;

// From nullable
Option<string> fromNullable = Optional(GetNameOrNull());

// Map and Bind
Option<string> greeting = Some("Alice")
    .Map(name => $"Hello, {name}!");
// Some("Hello, Alice!")

Option<Address> address = FindUser(123)
    .Bind(user => user.Address is not null ? Some(user.Address) : None);

// Match
string result = FindUser(123).Match(
    Some: user => $"Found: {user.Name}",
    None: () => "User not found");

// IfNone for default values
string name = FindUser(123)
    .Map(u => u.Name)
    .IfNone("Unknown");

// LINQ syntax
var city =
    from user in FindUser(123)
    from addr in Optional(user.Address)
    from c in Optional(addr.City)
    select c;
```

## Either<L, R>
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

// L = error type (Left), R = success type (Right)
public Either<string, Customer> ValidateCustomer(CreateCustomerRequest request)
{
    if (string.IsNullOrWhiteSpace(request.Name))
        return Left("Name is required");
    if (!request.Email.Contains('@'))
        return Left("Invalid email address");
    if (request.Name.Length > 100)
        return Left("Name too long");

    return Right(new Customer(Guid.NewGuid(), request.Name, request.Email));
}

// Chaining with Bind
var result = ValidateCustomer(request)
    .Bind(c => SaveToDatabase(c))
    .Bind(c => SendWelcomeEmail(c))
    .Match(
        Right: customer => Results.Created($"/customers/{customer.Id}", customer),
        Left: error => Results.BadRequest(new { error }));

// LINQ syntax for Either
Either<string, OrderSummary> ProcessOrder(OrderRequest req) =>
    from customer in ValidateCustomer(req.Customer)
    from items in ValidateItems(req.Items)
    from total in CalculateTotal(items)
    select new OrderSummary(customer.Id, items, total);
```

## Validation<F, S> (Accumulating Errors)
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

// Unlike Either which short-circuits, Validation accumulates all errors
public Validation<Error, string> ValidateName(string name) =>
    string.IsNullOrWhiteSpace(name)
        ? Fail<Error, string>(Error.New("Name is required"))
        : Success<Error, string>(name);

public Validation<Error, string> ValidateEmail(string email) =>
    !email.Contains('@')
        ? Fail<Error, string>(Error.New("Invalid email"))
        : Success<Error, string>(email);

public Validation<Error, decimal> ValidateAmount(decimal amount) =>
    amount <= 0
        ? Fail<Error, decimal>(Error.New("Amount must be positive"))
        : Success<Error, decimal>(amount);

// Apply: accumulates ALL errors instead of stopping at first
var validated = (ValidateName(request.Name),
                 ValidateEmail(request.Email),
                 ValidateAmount(request.Amount))
    .Apply((name, email, amount) => new Customer(name, email, amount));

// validated might contain: Fail(["Name is required", "Invalid email"])
validated.Match(
    Succ: customer => Results.Ok(customer),
    Fail: errors => Results.BadRequest(errors.ToList()));
```

## Try<T>
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

// Safe exception handling
Try<int> safeParse = () => int.Parse("not a number");

int result = safeParse.Match(
    Succ: value => value,
    Fail: ex => -1);

// Chaining Try operations
Try<Customer> LoadCustomer(Guid id) =>
    Try(() => db.Customers.Find(id) ?? throw new KeyNotFoundException());

Try<Order> LoadLatestOrder(Customer customer) =>
    Try(() => db.Orders
        .Where(o => o.CustomerId == customer.Id)
        .OrderByDescending(o => o.CreatedAt)
        .First());

var orderTotal = LoadCustomer(customerId)
    .Bind(c => LoadLatestOrder(c))
    .Map(o => o.Total)
    .Match(
        Succ: total => $"Total: {total:C}",
        Fail: ex => $"Error: {ex.Message}");
```

## Immutable Collections
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

// Lst<T>: immutable linked list
Lst<int> numbers = List(1, 2, 3, 4, 5);
Lst<int> withSix = numbers.Add(6); // numbers is unchanged

// Map<K, V>: immutable dictionary
Map<string, int> scores = Map(
    ("alice", 95),
    ("bob", 87),
    ("charlie", 92));

Option<int> bobScore = scores.Find("bob"); // Some(87)
Map<string, int> updated = scores.AddOrUpdate("bob", 90);

// Set<T>: immutable set
Set<string> tags = Set("dotnet", "csharp", "functional");
Set<string> moreTags = tags.Add("fp"); // tags is unchanged
bool hasCsharp = tags.Contains("csharp"); // true

// Seq<T>: lazy immutable sequence
Seq<int> lazy = Seq(1, 2, 3, 4, 5)
    .Filter(x => x % 2 == 0)
    .Map(x => x * x);
```

## Pattern Matching Helpers
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

// Fluent matching
string message = match(FindUser(123),
    Some: user => $"Welcome back, {user.Name}",
    None: () => "Please sign in");

// Working with tuples
var (name, age) = match(FindUser(123),
    Some: user => (user.Name, user.Age),
    None: () => ("Unknown", 0));

// ifSome / ifNone side effects
FindUser(123)
    .IfSome(user => logger.LogInformation("User found: {Name}", user.Name))
    .IfNone(() => logger.LogWarning("User not found"));
```

## Practical Service Layer Example
```csharp
using LanguageExt;
using static LanguageExt.Prelude;

public class OrderService
{
    private readonly IOrderRepository _orders;
    private readonly ICustomerRepository _customers;
    private readonly IPaymentGateway _payments;

    public OrderService(IOrderRepository orders, ICustomerRepository customers,
        IPaymentGateway payments)
    {
        _orders = orders;
        _customers = customers;
        _payments = payments;
    }

    public Either<OrderError, OrderConfirmation> PlaceOrder(PlaceOrderRequest request) =>
        from customer in _customers.FindById(request.CustomerId)
            .ToEither(OrderError.CustomerNotFound)
        from validItems in ValidateItems(request.Items)
        from total in Right<OrderError, decimal>(validItems.Sum(i => i.Total))
        from payment in _payments.Charge(customer, total)
            .MapLeft(e => OrderError.PaymentFailed(e.Message))
        from order in _orders.Create(customer.Id, validItems, total, payment.TransactionId)
            .MapLeft(e => OrderError.DatabaseError(e.Message))
        select new OrderConfirmation(order.Id, total, payment.TransactionId);
}

public abstract record OrderError
{
    public sealed record CustomerNotFoundError() : OrderError;
    public sealed record InvalidItemsError(string Message) : OrderError;
    public sealed record PaymentFailedError(string Message) : OrderError;
    public sealed record DatabaseErrorRecord(string Message) : OrderError;

    public static readonly OrderError CustomerNotFound = new CustomerNotFoundError();
    public static OrderError PaymentFailed(string msg) => new PaymentFailedError(msg);
    public static OrderError DatabaseError(string msg) => new DatabaseErrorRecord(msg);
}
```

## language-ext Types Overview

| Type | Purpose | Short-circuits? |
|------|---------|----------------|
| `Option<T>` | Optional values (replaces null) | N/A (None propagates) |
| `Either<L, R>` | Success (R) or typed error (L) | Yes (Left stops chain) |
| `Validation<F, S>` | Success or accumulated errors | No (collects all errors) |
| `Try<T>` | Exception-safe computation | Yes (exception stops chain) |
| `TryAsync<T>` | Async exception-safe computation | Yes |
| `Eff<T>` / `Aff<T>` | Side-effectful computation | Yes |
| `Lst<T>` | Immutable linked list | N/A |
| `Map<K,V>` | Immutable dictionary | N/A |
| `Set<T>` | Immutable set | N/A |

## Best Practices
- Use `Option<T>` instead of nullable returns for all methods that may not produce a value; convert at system boundaries using `Optional()` for nullable-to-Option bridging.
- Use `Either<L, R>` for operations that can fail with domain-specific errors; define error types as discriminated unions (sealed record hierarchies) for exhaustive matching.
- Use `Validation<F, S>` when you need to accumulate all validation errors (e.g., form validation) rather than stopping at the first failure as `Either` does.
- Prefer LINQ query syntax (`from ... in ... select`) for chaining more than two monadic operations; it reads like sequential code while maintaining functional composition.
- Use `Prelude` static imports (`using static LanguageExt.Prelude`) for ergonomic access to `Some`, `None`, `Left`, `Right`, `Try`, `List`, `Map`, and `Set` factory methods.
- Use language-ext immutable collections (`Lst<T>`, `Map<K,V>`, `Set<T>`) for domain models that must be thread-safe and mutation-free.
- Convert between `Option` and `Either` at service boundaries using `ToEither(errorValue)` when you need to add error context to an absent value.
- Use `Try<T>` and `TryAsync<T>` at infrastructure boundaries (file I/O, HTTP calls) to convert exceptions into monadic values that compose safely.
- Avoid mixing null-returning APIs with language-ext types in the same layer; establish a boundary where nullables are converted to `Option<T>`.
- Use `Match` with explicit handlers for all cases to ensure complete handling; avoid `IfSome`/`IfNone` in business logic where both paths need to produce a value.
