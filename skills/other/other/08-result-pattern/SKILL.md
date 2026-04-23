---
name: result-pattern
description: "Implements the Result pattern for explicit error handling without exceptions. Provides Result, Result<T>, and Error types for clean, predictable control flow in domain-driven applications."
version: 1.0.0
language: C#
framework: .NET 8+
pattern: Railway-Oriented Programming
---

# Result Pattern Implementation

## Overview

The Result pattern provides explicit error handling without exceptions:

- **No exceptions for business errors** - Exceptions for truly exceptional cases only
- **Explicit success/failure** - Compiler forces handling of both cases
- **Composable errors** - Chain operations, fail fast
- **Self-documenting** - Method signatures show possible outcomes

## Quick Reference

| Type | Purpose | Usage |
|------|---------|-------|
| `Result` | Operation without return value | Update, Delete operations |
| `Result<T>` | Operation with return value | Create, Get operations |
| `Error` | Error information | Code + Description |

---

## Implementation Structure

```
/Domain/Abstractions/
├── Result.cs           # Result and Result<T>
├── Error.cs            # Error record
└── ValidationResult.cs # Multiple errors support
```

---

## Template: Core Result Types

```csharp
// src/{name}.domain/Abstractions/Error.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Represents an error with a code and description
/// </summary>
public record Error(string Code, string Description)
{
    /// <summary>
    /// Represents no error (success state)
    /// </summary>
    public static readonly Error None = new(string.Empty, string.Empty);

    /// <summary>
    /// Represents a null value error
    /// </summary>
    public static readonly Error NullValue = new(
        "Error.NullValue",
        "A null value was provided");

    /// <summary>
    /// Creates an error from an exception
    /// </summary>
    public static Error FromException(Exception exception) => new(
        "Error.Exception",
        exception.Message);

    /// <summary>
    /// Implicit conversion to string (returns Code)
    /// </summary>
    public static implicit operator string(Error error) => error.Code;

    public override string ToString() => Code;
}
```

```csharp
// src/{name}.domain/Abstractions/Result.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Represents the outcome of an operation that doesn't return a value
/// </summary>
public class Result
{
    protected Result(bool isSuccess, Error error)
    {
        if (isSuccess && error != Error.None)
        {
            throw new InvalidOperationException(
                "Cannot create successful result with an error");
        }

        if (!isSuccess && error == Error.None)
        {
            throw new InvalidOperationException(
                "Cannot create failed result without an error");
        }

        IsSuccess = isSuccess;
        Error = error;
    }

    public bool IsSuccess { get; }

    public bool IsFailure => !IsSuccess;

    public Error Error { get; }

    // ═══════════════════════════════════════════════════════════════
    // FACTORY METHODS
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Creates a successful result
    /// </summary>
    public static Result Success() => new(true, Error.None);

    /// <summary>
    /// Creates a failed result with the specified error
    /// </summary>
    public static Result Failure(Error error) => new(false, error);

    /// <summary>
    /// Creates a successful result with a value
    /// </summary>
    public static Result<TValue> Success<TValue>(TValue value) =>
        new(value, true, Error.None);

    /// <summary>
    /// Creates a failed result with the specified error
    /// </summary>
    public static Result<TValue> Failure<TValue>(Error error) =>
        new(default, false, error);

    /// <summary>
    /// Creates a result based on a condition
    /// </summary>
    public static Result Create(bool condition, Error error) =>
        condition ? Success() : Failure(error);

    /// <summary>
    /// Creates a result based on a condition with a value
    /// </summary>
    public static Result<TValue> Create<TValue>(TValue? value, Error error) =>
        value is not null ? Success(value) : Failure<TValue>(error);
}

/// <summary>
/// Represents the outcome of an operation that returns a value
/// </summary>
public class Result<TValue> : Result
{
    private readonly TValue? _value;

    protected internal Result(TValue? value, bool isSuccess, Error error)
        : base(isSuccess, error)
    {
        _value = value;
    }

    /// <summary>
    /// Gets the value if successful, throws if failed
    /// </summary>
    public TValue Value => IsSuccess
        ? _value!
        : throw new InvalidOperationException(
            $"Cannot access value of a failed result. Error: {Error.Code}");

    /// <summary>
    /// Implicit conversion from value to successful Result
    /// </summary>
    public static implicit operator Result<TValue>(TValue? value) =>
        value is not null ? Success(value) : Failure<TValue>(Error.NullValue);

    /// <summary>
    /// Implicit conversion from Error to failed Result
    /// </summary>
    public static implicit operator Result<TValue>(Error error) =>
        Failure<TValue>(error);
}
```

---

## Template: Result Extensions (Functional Operations)

```csharp
// src/{name}.domain/Abstractions/ResultExtensions.cs
namespace {name}.domain.abstractions;

public static class ResultExtensions
{
    // ═══════════════════════════════════════════════════════════════
    // MAP: Transform success value
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Transforms the value if successful, preserves error if failed
    /// </summary>
    public static Result<TOut> Map<TIn, TOut>(
        this Result<TIn> result,
        Func<TIn, TOut> mapper)
    {
        return result.IsSuccess
            ? Result.Success(mapper(result.Value))
            : Result.Failure<TOut>(result.Error);
    }

    /// <summary>
    /// Async version of Map
    /// </summary>
    public static async Task<Result<TOut>> Map<TIn, TOut>(
        this Task<Result<TIn>> resultTask,
        Func<TIn, TOut> mapper)
    {
        var result = await resultTask;
        return result.Map(mapper);
    }

    // ═══════════════════════════════════════════════════════════════
    // BIND: Chain operations that return Result
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Chains another Result-returning operation if successful
    /// </summary>
    public static Result<TOut> Bind<TIn, TOut>(
        this Result<TIn> result,
        Func<TIn, Result<TOut>> binder)
    {
        return result.IsSuccess
            ? binder(result.Value)
            : Result.Failure<TOut>(result.Error);
    }

    /// <summary>
    /// Async version of Bind
    /// </summary>
    public static async Task<Result<TOut>> Bind<TIn, TOut>(
        this Result<TIn> result,
        Func<TIn, Task<Result<TOut>>> binder)
    {
        return result.IsSuccess
            ? await binder(result.Value)
            : Result.Failure<TOut>(result.Error);
    }

    /// <summary>
    /// Async version of Bind for Task results
    /// </summary>
    public static async Task<Result<TOut>> Bind<TIn, TOut>(
        this Task<Result<TIn>> resultTask,
        Func<TIn, Result<TOut>> binder)
    {
        var result = await resultTask;
        return result.Bind(binder);
    }

    /// <summary>
    /// Fully async Bind
    /// </summary>
    public static async Task<Result<TOut>> Bind<TIn, TOut>(
        this Task<Result<TIn>> resultTask,
        Func<TIn, Task<Result<TOut>>> binder)
    {
        var result = await resultTask;
        return await result.Bind(binder);
    }

    // ═══════════════════════════════════════════════════════════════
    // TAP: Execute side effect without changing result
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Executes an action if successful, returns original result
    /// </summary>
    public static Result<T> Tap<T>(
        this Result<T> result,
        Action<T> action)
    {
        if (result.IsSuccess)
        {
            action(result.Value);
        }

        return result;
    }

    /// <summary>
    /// Async version of Tap
    /// </summary>
    public static async Task<Result<T>> Tap<T>(
        this Result<T> result,
        Func<T, Task> action)
    {
        if (result.IsSuccess)
        {
            await action(result.Value);
        }

        return result;
    }

    // ═══════════════════════════════════════════════════════════════
    // MATCH: Pattern match on result
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Executes success or failure function based on result state
    /// </summary>
    public static TOut Match<TIn, TOut>(
        this Result<TIn> result,
        Func<TIn, TOut> onSuccess,
        Func<Error, TOut> onFailure)
    {
        return result.IsSuccess
            ? onSuccess(result.Value)
            : onFailure(result.Error);
    }

    /// <summary>
    /// Async version of Match
    /// </summary>
    public static async Task<TOut> Match<TIn, TOut>(
        this Task<Result<TIn>> resultTask,
        Func<TIn, TOut> onSuccess,
        Func<Error, TOut> onFailure)
    {
        var result = await resultTask;
        return result.Match(onSuccess, onFailure);
    }

    // ═══════════════════════════════════════════════════════════════
    // ENSURE: Add validation to existing result
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Validates the value and fails if predicate returns false
    /// </summary>
    public static Result<T> Ensure<T>(
        this Result<T> result,
        Func<T, bool> predicate,
        Error error)
    {
        if (result.IsFailure)
        {
            return result;
        }

        return predicate(result.Value)
            ? result
            : Result.Failure<T>(error);
    }

    /// <summary>
    /// Async version of Ensure
    /// </summary>
    public static async Task<Result<T>> Ensure<T>(
        this Result<T> result,
        Func<T, Task<bool>> predicate,
        Error error)
    {
        if (result.IsFailure)
        {
            return result;
        }

        return await predicate(result.Value)
            ? result
            : Result.Failure<T>(error);
    }

    // ═══════════════════════════════════════════════════════════════
    // COMBINE: Combine multiple results
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Combines multiple results, returning first failure or success
    /// </summary>
    public static Result Combine(params Result[] results)
    {
        foreach (var result in results)
        {
            if (result.IsFailure)
            {
                return result;
            }
        }

        return Result.Success();
    }

    /// <summary>
    /// Combines multiple results with values
    /// </summary>
    public static Result<(T1, T2)> Combine<T1, T2>(
        Result<T1> result1,
        Result<T2> result2)
    {
        if (result1.IsFailure) return Result.Failure<(T1, T2)>(result1.Error);
        if (result2.IsFailure) return Result.Failure<(T1, T2)>(result2.Error);

        return Result.Success((result1.Value, result2.Value));
    }

    /// <summary>
    /// Combines three results with values
    /// </summary>
    public static Result<(T1, T2, T3)> Combine<T1, T2, T3>(
        Result<T1> result1,
        Result<T2> result2,
        Result<T3> result3)
    {
        if (result1.IsFailure) return Result.Failure<(T1, T2, T3)>(result1.Error);
        if (result2.IsFailure) return Result.Failure<(T1, T2, T3)>(result2.Error);
        if (result3.IsFailure) return Result.Failure<(T1, T2, T3)>(result3.Error);

        return Result.Success((result1.Value, result2.Value, result3.Value));
    }

    // ═══════════════════════════════════════════════════════════════
    // GET VALUE OR DEFAULT
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Returns the value if successful, or default value if failed
    /// </summary>
    public static T GetValueOrDefault<T>(
        this Result<T> result,
        T defaultValue = default!)
    {
        return result.IsSuccess ? result.Value : defaultValue;
    }

    /// <summary>
    /// Returns the value if successful, or result of factory if failed
    /// </summary>
    public static T GetValueOrDefault<T>(
        this Result<T> result,
        Func<T> defaultFactory)
    {
        return result.IsSuccess ? result.Value : defaultFactory();
    }
}
```

---

## Template: Validation Result (Multiple Errors)

```csharp
// src/{name}.domain/Abstractions/ValidationResult.cs
namespace {name}.domain.abstractions;

/// <summary>
/// Result that can contain multiple validation errors
/// </summary>
public sealed class ValidationResult : Result, IValidationResult
{
    private ValidationResult(Error[] errors)
        : base(false, IValidationResult.ValidationError)
    {
        Errors = errors;
    }

    public Error[] Errors { get; }

    public static ValidationResult WithErrors(Error[] errors) => new(errors);
}

/// <summary>
/// Validation result with a value
/// </summary>
public sealed class ValidationResult<TValue> : Result<TValue>, IValidationResult
{
    private ValidationResult(Error[] errors)
        : base(default, false, IValidationResult.ValidationError)
    {
        Errors = errors;
    }

    public Error[] Errors { get; }

    public static ValidationResult<TValue> WithErrors(Error[] errors) => new(errors);
}

/// <summary>
/// Marker interface for validation results
/// </summary>
public interface IValidationResult
{
    public static readonly Error ValidationError = new(
        "Validation.Error",
        "One or more validation errors occurred");

    Error[] Errors { get; }
}
```

---

## Usage Examples

### Basic Usage in Domain Entity

```csharp
public sealed class User : Entity
{
    public static Result<User> Create(string email, string name)
    {
        // Validate email
        var emailResult = Email.Create(email);
        if (emailResult.IsFailure)
        {
            return Result.Failure<User>(emailResult.Error);
        }

        // Validate name
        if (string.IsNullOrWhiteSpace(name))
        {
            return Result.Failure<User>(UserErrors.NameRequired);
        }

        if (name.Length > 100)
        {
            return Result.Failure<User>(UserErrors.NameTooLong);
        }

        var user = new User(Guid.NewGuid(), emailResult.Value, name);

        return Result.Success(user);
    }

    public Result UpdateName(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return Result.Failure(UserErrors.NameRequired);
        }

        Name = name;
        return Result.Success();
    }
}
```

### Usage in Command Handler

```csharp
internal sealed class CreateUserCommandHandler
    : ICommandHandler<CreateUserCommand, Guid>
{
    private readonly IUserRepository _userRepository;
    private readonly IUnitOfWork _unitOfWork;

    public async Task<Result<Guid>> Handle(
        CreateUserCommand request,
        CancellationToken cancellationToken)
    {
        // Check if user exists
        var existingUser = await _userRepository
            .GetByEmailAsync(request.Email, cancellationToken);

        if (existingUser is not null)
        {
            return Result.Failure<Guid>(UserErrors.EmailAlreadyExists);
        }

        // Create user using factory method
        var userResult = User.Create(request.Email, request.Name);

        if (userResult.IsFailure)
        {
            return Result.Failure<Guid>(userResult.Error);
        }

        _userRepository.Add(userResult.Value);

        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return userResult.Value.Id;
    }
}
```

### Chaining with Bind

```csharp
public async Task<Result<OrderConfirmation>> PlaceOrder(
    Guid userId,
    CreateOrderRequest request,
    CancellationToken ct)
{
    return await GetUser(userId, ct)
        .Bind(user => ValidateUserCanOrder(user))
        .Bind(user => CreateOrder(user, request))
        .Bind(order => ProcessPayment(order, ct))
        .Bind(order => SendConfirmation(order, ct));
}
```

### Using Match in Controller

```csharp
[HttpPost]
public async Task<IActionResult> Create(
    [FromBody] CreateUserRequest request,
    CancellationToken ct)
{
    var command = new CreateUserCommand(request.Email, request.Name);

    var result = await _sender.Send(command, ct);

    return result.Match(
        onSuccess: id => CreatedAtAction(nameof(GetById), new { id }, id),
        onFailure: error => error.Code switch
        {
            "User.EmailExists" => Conflict(error),
            "User.NotFound" => NotFound(error),
            _ => BadRequest(error)
        });
}
```

### Combining Multiple Results

```csharp
public Result<Order> CreateOrder(
    CreateOrderRequest request)
{
    // Validate all fields
    var customerResult = CustomerId.Create(request.CustomerId);
    var addressResult = Address.Create(request.Street, request.City);
    var amountResult = Money.Create(request.Amount);

    // Combine - returns first failure
    var combinedResult = ResultExtensions.Combine(
        customerResult,
        addressResult,
        amountResult);

    if (combinedResult.IsFailure)
    {
        return Result.Failure<Order>(combinedResult.Error);
    }

    var (customerId, address, amount) = combinedResult.Value;

    return Order.Create(customerId, address, amount);
}
```

---

## Domain Errors Pattern

```csharp
// src/{name}.domain/Users/UserErrors.cs
namespace {name}.domain.users;

public static class UserErrors
{
    public static readonly Error NotFound = new(
        "User.NotFound",
        "The user with the specified ID was not found");

    public static readonly Error EmailAlreadyExists = new(
        "User.EmailExists",
        "A user with this email already exists");

    public static readonly Error NameRequired = new(
        "User.NameRequired",
        "User name is required");

    public static readonly Error NameTooLong = new(
        "User.NameTooLong",
        "User name cannot exceed 100 characters");

    public static readonly Error InvalidCredentials = new(
        "User.InvalidCredentials",
        "The provided credentials are invalid");

    public static readonly Error AccountLocked = new(
        "User.AccountLocked",
        "The user account is locked");

    // Parameterized errors
    public static Error NotFoundById(Guid id) => new(
        "User.NotFound",
        $"The user with ID '{id}' was not found");

    public static Error Unauthorized(string resource) => new(
        "User.Unauthorized",
        $"User is not authorized to access '{resource}'");
}
```

---

## Critical Rules

1. **Never throw for business errors** - Return `Result.Failure`
2. **Always check IsSuccess/IsFailure** - Before accessing Value
3. **Use factory methods** - `Result.Success()`, `Result.Failure()`
4. **Errors are immutable** - `record Error(...)` 
5. **Error codes are unique** - Follow `{Entity}.{ErrorType}` pattern
6. **Chain with Bind** - For sequential operations
7. **Use Match in controllers** - Clean response mapping
8. **Value objects validate in Create** - Return Result from factories
9. **Combine for multiple validations** - Returns first failure
10. **Keep Result in domain** - Don't leak to API layer directly

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Throwing for business errors
if (user is null)
    throw new NotFoundException("User not found");

// ✅ CORRECT: Return Result
if (user is null)
    return Result.Failure<User>(UserErrors.NotFound);

// ❌ WRONG: Accessing Value without checking
var user = result.Value;  // Throws if failed!

// ✅ CORRECT: Check first
if (result.IsFailure)
    return Result.Failure(result.Error);
var user = result.Value;

// ❌ WRONG: Ignoring Result
await CreateUserAsync(request);  // Ignores possible failure

// ✅ CORRECT: Handle the result
var result = await CreateUserAsync(request);
if (result.IsFailure)
    // Handle error

// ❌ WRONG: Using exceptions as control flow
try { return Success(Process()); }
catch (ValidationException ex) { return Failure(ex.Error); }

// ✅ CORRECT: Design to return Result
var validationResult = Validate(input);
if (validationResult.IsFailure)
    return validationResult;
return Success(Process(input));
```

---

## Related Skills

- `domain-entity-generator` - Use Result in factory methods
- `cqrs-command-generator` - Commands return Result
- `cqrs-query-generator` - Queries return Result
- `pipeline-behaviors` - Validation behavior uses Result
