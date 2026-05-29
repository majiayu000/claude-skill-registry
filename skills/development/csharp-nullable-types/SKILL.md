---
name: csharp-nullable-types
description: Use when C# nullable reference types, null safety patterns, and migration strategies. Use when ensuring null safety in C# code.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# C# Nullable Types

Master nullable reference types, null safety patterns, and migration strategies
in C# 8+. This skill covers nullable value types, nullable reference types,
null-safety annotations, operators, and best practices for writing null-safe code.

## Nullable Reference Types (C# 8+)

Nullable reference types provide compile-time null safety by distinguishing
between nullable and non-nullable reference types.

### Enabling Nullable Context

```csharp
// Project-wide in .csproj
<PropertyGroup>
    <Nullable>enable</Nullable>
</PropertyGroup>

// File-level directive
#nullable enable

public class User
{
    // Non-nullable - must be initialized
    public string Name { get; set; } = string.Empty;

    // Nullable - can be null
    public string? MiddleName { get; set; }

    // Non-nullable - must be set in constructor
    public string Email { get; set; }

    public User(string email)
    {
        Email = email;
    }
}

// Disable for legacy code
#nullable disable

public class LegacyClass
{
    public string Name { get; set; } // Warning suppressed
}

#nullable restore // Return to project default
```

### Non-nullable and Nullable References

```csharp
#nullable enable

public class PersonService
{
    // ✅ Non-nullable parameter and return type
    public string FormatName(string firstName, string lastName)
    {
        return $"{firstName} {lastName}";
    }

    // ✅ Nullable parameter
    public string FormatNameWithMiddle(string firstName, string? middleName, string lastName)
    {
        if (middleName != null)
        {
            return $"{firstName} {middleName} {lastName}";
        }
        return $"{firstName} {lastName}";
    }

    // ✅ Nullable return type
    public string? FindUserEmail(int userId)
    {
        var user = _repository.Find(userId);
        return user?.Email; // May return null
    }

    // ⚠️ Warning - possible null reference
    public string GetUpperName(string? name)
    {
        // CS8602: Possible null reference
        return name.ToUpper();
    }

    // ✅ Fixed with null check
    public string GetUpperNameSafe(string? name)
    {
        if (name == null)
        {
            throw new ArgumentNullException(nameof(name));
        }
        return name.ToUpper();
    }
}
```

## Nullable Value Types

Value types can be made nullable using Nullable&lt;T&gt; or the ? syntax.

### Nullable&lt;T&gt; and T?

```csharp
public class NullableValueTypes
{
    // Nullable value types
    public int? Age { get; set; }
    public DateTime? BirthDate { get; set; }
    public decimal? Salary { get; set; }
    public bool? IsActive { get; set; }

    // Equivalent to:
    public Nullable<int> AgeVerbose { get; set; }

    public void WorkWithNullables()
    {
        int? value = null;

        // HasValue and Value properties
        if (value.HasValue)
        {
            int actualValue = value.Value;
            Console.WriteLine(actualValue);
        }

        // GetValueOrDefault
        int result1 = value.GetValueOrDefault(); // 0
        int result2 = value.GetValueOrDefault(42); // 42

        // Null coalescing
        int result3 = value ?? 100; // 100
    }

    public int CalculateAge(DateTime? birthDate)
    {
        // ⚠️ Warning - possible null reference
        // return DateTime.Now.Year - birthDate.Value.Year;

        // ✅ Correct with null check
        if (!birthDate.HasValue)
        {
            throw new ArgumentException("Birth date is required", nameof(birthDate));
        }

        return DateTime.Now.Year - birthDate.Value.Year;
    }
}
```

### Nullable Value Type Operations

```csharp
public class NullableOperations
{
    public void ArithmeticOperations()
    {
        int? a = 5;
        int? b = 10;
        int? c = null;

        // Arithmetic with nullables
        int? sum = a + b; // 15
        int? nullSum = a + c; // null

        // Comparison
        bool? equal = a == b; // false
        bool? nullEqual = a == c; // null (neither true nor false)

        // Lifted operators
        int? result = (a > 0) ? a * 2 : null;
    }

    public decimal? CalculateDiscount(decimal? price, decimal? discountPercent)
    {
        // If either is null, result is null
        return price * (1 - discountPercent / 100);
    }

    public void BooleanLogic()
    {
        bool? a = true;
        bool? b = false;
        bool? c = null;

        // Three-valued logic
        bool? and1 = a & b;  // false
        bool? and2 = a & c;  // null
        bool? and3 = b & c;  // false (false & anything = false)

        bool? or1 = a | b;   // true
        bool? or2 = a | c;   // true (true | anything = true)
        bool? or3 = b | c;   // null
    }
}
```

## Null Safety Annotations

Attributes that provide additional null-safety information to the compiler.

### Common Annotations

```csharp
using System.Diagnostics.CodeAnalysis;

public class AnnotationExamples
{
    // [NotNull] - Parameter won't be null when method returns normally
    public void ProcessUser([NotNull] User? user)
    {
        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        // Compiler knows user is not null here
        Console.WriteLine(user.Name);
    }

    // [MaybeNull] - Return value may be null even if type is non-nullable
    [return: MaybeNull]
    public T GetValueOrDefault<T>(string key)
    {
        if (_dictionary.TryGetValue(key, out var value))
        {
            return value;
        }
        return default; // May be null for reference types
    }

    // [NotNullWhen] - Parameter is not null when method returns specified bool
    public bool TryGetUser(int id, [NotNullWhen(true)] out User? user)
    {
        user = _repository.Find(id);
        return user != null;
    }

    public void UseUser(int id)
    {
        if (TryGetUser(id, out var user))
        {
            // Compiler knows user is not null here
            Console.WriteLine(user.Name);
        }
    }

    // [NotNullIfNotNull] - Return value is not null if parameter
    // is not null
    [return: NotNullIfNotNull(nameof(value))]
    public string? ProcessString(string? value)
    {
        return value?.Trim().ToUpperInvariant();
    }

    // [DoesNotReturn] - Method never returns normally
    [DoesNotReturn]
    public void ThrowError(string message)
    {
        throw new InvalidOperationException(message);
    }

    public void ValidateUser(User? user)
    {
        if (user == null)
        {
            ThrowError("User is required");
        }

        // Compiler knows this is unreachable if user is null
        Console.WriteLine(user.Name);
    }
}
```

### MemberNotNull Annotation

```csharp
public class InitializationExample
{
    private string _name;
    private string _email;

    public InitializationExample()
    {
        Initialize("Default", "default@example.com");
    }

    // Tells compiler these members are initialized
    [MemberNotNull(nameof(_name), nameof(_email))]
    private void Initialize(string name, string email)
    {
        _name = name;
        _email = email;
    }

    [MemberNotNull(nameof(_name), nameof(_email))]
    public void Reset()
    {
        _name = string.Empty;
        _email = string.Empty;
    }
}
```

## Null-Forgiving Operator

The null-forgiving operator (!) suppresses nullable warnings when you know
better than the compiler.

### Using the ! Operator

```csharp
public class NullForgivingExamples
{
    private User? _currentUser;

    public void Initialize()
    {
        _currentUser = LoadUser();
    }

    public void ProcessCurrentUser()
    {
        // ⚠️ Warning: Possible null reference
        // Console.WriteLine(_currentUser.Name);

        // ✅ Use ! when you know it's not null
        Console.WriteLine(_currentUser!.Name);
    }

    // ⚠️ Use sparingly and carefully
    public string GetUserName()
    {
        // Only use ! if you're absolutely sure
        return _currentUser!.Name;
    }

    // ✅ Better: check explicitly
    public string GetUserNameSafe()
    {
        if (_currentUser == null)
        {
            throw new InvalidOperationException("User not initialized");
        }

        return _currentUser.Name;
    }

    // Common pattern with dictionary
    public void DictionaryPattern()
    {
        var dict = new Dictionary<string, User>();
        dict["key"] = new User("test@example.com");

        // You know key exists
        var user = dict["key"];
        Console.WriteLine(user.Email); // No warning needed

        // But with TryGetValue
        if (dict.TryGetValue("key", out var foundUser))
        {
            // foundUser is User?, but you know it's not null here
            Console.WriteLine(foundUser!.Email); // Or better: check in if
        }
    }
}
```

### When NOT to Use the Null-Forgiving Operator

```csharp
public class BadNullForgiving
{
    // ❌ BAD - Hiding real problems
    public void ProcessData(string? input)
    {
        var result = input!.ToUpper(); // Will crash if input is null
    }

    // ✅ GOOD - Proper null handling
    public void ProcessDataSafe(string? input)
    {
        if (input == null)
        {
            throw new ArgumentNullException(nameof(input));
        }

        var result = input.ToUpper();
    }

    // ❌ BAD - False confidence
    public User GetUser(int id)
    {
        return _repository.Find(id)!; // May actually be null!
    }

    // ✅ GOOD - Handle null case
    public User GetUserSafe(int id)
    {
        return _repository.Find(id)
            ?? throw new KeyNotFoundException($"User {id} not found");
    }
}
```

## Null-Conditional Operators

Safe navigation operators for accessing members that might be null.

### ?. and ?[] Operators

```csharp
public class NullConditionalExamples
{
    public void SafeNavigation()
    {
        User? user = GetUser();

        // ✅ Null-conditional member access
        string? name = user?.Name; // null if user is null

        // ✅ Chaining null-conditional operators
        string? city = user?.Address?.City;

        // ✅ Null-conditional indexing
        char? firstChar = user?.Name?[0];

        // ✅ Combining with method calls
        int? nameLength = user?.Name?.Length;

        // ✅ With null coalescing
        string displayName = user?.Name ?? "Guest";

        // ✅ Null-conditional with invocation
        int? result = user?.CalculateAge();
    }

    public void ArrayAndCollectionAccess()
    {
        int[]? numbers = GetNumbers();

        // ✅ Null-conditional array access
        int? first = numbers?[0];

        // ✅ Null-conditional with LINQ
        int? max = numbers?.Max();

        // ✅ Dictionary access
        Dictionary<string, User>? users = GetUsers();
        User? user = users?["key"];
    }

    public void InvocationExamples()
    {
        Action? callback = GetCallback();

        // ✅ Null-conditional invocation
        callback?.Invoke();

        // Equivalent to:
        if (callback != null)
        {
            callback.Invoke();
        }

        // ✅ With events
        EventHandler? handler = SomeEvent;
        handler?.Invoke(this, EventArgs.Empty);
    }
}
```

## Null-Coalescing Operators

The ?? and ??= operators provide default values for null expressions.

### ?? Operator

```csharp
public class NullCoalescingExamples
{
    public void BasicCoalescing()
    {
        string? name = GetName();

        // ✅ Provide default if null
        string displayName = name ?? "Unknown";

        // ✅ Chain multiple coalescing
        string result = GetPrimaryName()
            ?? GetSecondaryName()
            ?? GetDefaultName()
            ?? "Fallback";

        // ✅ With value types
        int? nullableValue = GetValue();
        int value = nullableValue ?? 0;

        // ✅ Combine with null-conditional
        int length = user?.Name?.Length ?? 0;
    }

    public User GetUserOrDefault(int id)
    {
        // ✅ Return default if null
        return _repository.Find(id) ?? new User("guest@example.com");
    }

    public string GetConfigValue(string key, string defaultValue)
    {
        // ✅ Configuration pattern
        return _config[key] ?? defaultValue;
    }
}
```

### ??= Operator (Null-Coalescing Assignment)

```csharp
public class NullCoalescingAssignment
{
    private User? _cachedUser;
    private List<string>? _items;

    public User GetUser(int id)
    {
        // ✅ Lazy initialization pattern
        _cachedUser ??= LoadUser(id);
        return _cachedUser;
    }

    public void EnsureListInitialized()
    {
        // ✅ Ensure collection is initialized
        _items ??= new List<string>();
        _items.Add("item");
    }

    public void UpdateNameIfNull(User user)
    {
        // ✅ Set only if currently null
        user.MiddleName ??= "N/A";
    }

    // Before C# 8, you would write:
    public void OldWay()
    {
        if (_items == null)
        {
            _items = new List<string>();
        }

        // Or:
        _items = _items ?? new List<string>();
    }
}
```

## Pattern Matching with Null

C# 9+ pattern matching enhancements for null checking.

### Null Pattern Matching

```csharp
public class PatternMatchingExamples
{
    public void IsPatterns()
    {
        object? obj = GetObject();

        // ✅ Check for null
        if (obj is null)
        {
            Console.WriteLine("Object is null");
        }

        // ✅ Check for not null
        if (obj is not null)
        {
            Console.WriteLine("Object is not null");
        }

        // ✅ Type pattern with null check
        if (obj is string s)
        {
            // s is not null here
            Console.WriteLine(s.ToUpper());
        }

        // ✅ Property pattern
        if (obj is User { Name: not null } user)
        {
            Console.WriteLine(user.Name);
        }
    }

    public string GetDescription(User? user) => user switch
    {
        null => "No user",
        { Name: null } => "User without name",
        { Name: var name } => $"User: {name}"
    };

    public void RecursivePatterns()
    {
        Order? order = GetOrder();

        // ✅ Complex pattern matching
        var status = order switch
        {
            null => "No order",
            { Customer: null } => "Order without customer",
            { Customer.Address: null } => "Customer without address",
            { Customer.Address.City: var city } => $"Shipping to {city}",
        };
    }
}
```

## Migration Strategies

Gradually migrate existing code to nullable reference types.

### Incremental Migration

```csharp
// Step 1: Enable nullable in .csproj with warnings as errors
<PropertyGroup>
    <Nullable>enable</Nullable>
    <WarningsAsErrors>nullable</WarningsAsErrors>
</PropertyGroup>

// Step 2: Migrate file by file
#nullable enable

public class MigratedClass
{
    // Fix all warnings in this file
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
}

// Step 3: Use #nullable disable for legacy code
#nullable disable

public class LegacyClass
{
    // No nullable warnings here
    public string Name { get; set; }
}

#nullable restore
```

### Migration Patterns

```csharp
public class MigrationPatterns
{
    // Before: Everything nullable by default
    #nullable disable
    public string GetUserName(User user)
    {
        return user.Name;
    }
    #nullable restore

    // After: Explicit nullability
    #nullable enable
    public string GetUserNameNullable(User? user)
    {
        if (user == null)
        {
            throw new ArgumentNullException(nameof(user));
        }

        return user.Name ?? throw new InvalidOperationException("Name is required");
    }

    // Pattern: Make optional parameters explicit
    // Before
    #nullable disable
    public void ProcessData(string data, string format)
    {
        format = format ?? "json";
    }
    #nullable restore

    // After
    #nullable enable
    public void ProcessDataNullable(string data, string? format = null)
    {
        format ??= "json";
    }

    // Pattern: Use nullable return types
    // Before
    #nullable disable
    public User FindUser(int id)
    {
        return _repository.Find(id); // May return null
    }
    #nullable restore

    // After
    #nullable enable
    public User? FindUserNullable(int id)
    {
        return _repository.Find(id);
    }
}
```

## Compiler Warnings and Strictness

Understanding and configuring nullable warning levels.

### Warning Levels

```csharp
// In .csproj
<PropertyGroup>
    <Nullable>enable</Nullable>

    <!-- Treat nullable warnings as errors -->
    <WarningsAsErrors>CS8600;CS8601;CS8602;CS8603;CS8604</WarningsAsErrors>

    <!-- Or treat all nullable warnings as errors -->
    <WarningsAsErrors>nullable</WarningsAsErrors>
</PropertyGroup>

// Common warnings:
// CS8600: Converting null literal or possible null value to non-nullable type
// CS8601: Possible null reference assignment
// CS8602: Dereference of a possibly null reference
// CS8603: Possible null reference return
// CS8604: Possible null reference argument

#nullable enable

public class WarningExamples
{
    // CS8618: Non-nullable property must contain non-null value when exiting constructor
    public string Name { get; set; } = string.Empty;

    // CS8603: Possible null reference return
    public string GetName(User? user)
    {
        return user?.Name ?? string.Empty; // Fix
    }

    // CS8602: Dereference of possibly null reference
    public int GetLength(string? value)
    {
        return value?.Length ?? 0; // Fix
    }

    // Suppress specific warning
    #pragma warning disable CS8602
    public void LegacyCode(string? value)
    {
        Console.WriteLine(value.Length); // Warning suppressed
    }
    #pragma warning restore CS8602
}
```

## Nullable in Generic Constraints

Handling nullability in generic type parameters.

### Generic Nullable Constraints

```csharp
#nullable enable

public class GenericNullability
{
    // T? is nullable for both reference and value types
    public T? FindOrDefault<T>(int id)
    {
        var result = _repository.Find<T>(id);
        return result; // May be null
    }

    // where T : class - T is a reference type
    public T Create<T>(string name) where T : class, new()
    {
        var instance = new T();
        return instance; // Never null
    }

    // where T : class? - T is a nullable reference type
    public void Process<T>(T? value) where T : class
    {
        if (value == null)
        {
            return;
        }

        // value is not null here
        Console.WriteLine(value.ToString());
    }

    // where T : struct - T is a non-nullable value type
    public T GetValue<T>() where T : struct
    {
        return default; // Returns default value, never null
    }

    // where T : notnull - T cannot be nullable
    public void RequireNonNull<T>(T value) where T : notnull
    {
        // value is guaranteed not to be null
        Console.WriteLine(value.ToString());
    }
}
```

### Nullable Generic Patterns

```csharp
public class Repository<T> where T : class
{
    private readonly Dictionary<int, T> _cache = new();

    // Return nullable when not found
    public T? Find(int id)
    {
        _cache.TryGetValue(id, out var result);
        return result;
    }

    // Throw when not found
    public T Get(int id)
    {
        return _cache[id]; // Throws if not found
    }

    // Try pattern
    public bool TryGet(int id, [NotNullWhen(true)] out T? result)
    {
        return _cache.TryGetValue(id, out result);
    }
}

public class NullableGenericList<T>
{
    private readonly List<T> _items = new();

    // First or null
    public T? FirstOrDefault()
    {
        return _items.Count > 0 ? _items[0] : default;
    }

    // Find with predicate
    public T? Find(Predicate<T> predicate)
    {
        foreach (var item in _items)
        {
            if (predicate(item))
            {
                return item;
            }
        }
        return default;
    }
}
```

## Best Practices

1. **Enable Nullable Globally**: Use `<Nullable>enable</Nullable>` in .csproj
2. **Explicit Nullability**: Make nullability intentions clear in APIs
3. **Validate at Boundaries**: Check for null at public API boundaries
4. **Use Null-Conditional Operators**: Prefer ?. over explicit null checks
5. **Avoid Null-Forgiving**: Use ! sparingly and only when truly necessary
6. **Return Non-Nullable**: Prefer non-nullable return types when possible
7. **Use Annotations**: Apply [NotNull], [MaybeNull] etc. appropriately
8. **Constructor Initialization**: Initialize non-nullable properties in constructors
9. **Throw on Invalid State**: Throw exceptions for unexpected nulls
10. **Gradual Migration**: Migrate file-by-file with #nullable directives

## Common Pitfalls

1. **Overusing !**: Suppressing warnings instead of fixing root cause
2. **Not Initializing**: Forgetting to initialize non-nullable properties
3. **Silent Failures**: Not handling null cases in public APIs
4. **Mixing Contexts**: Inconsistent nullable/disable throughout codebase
5. **Ignoring Warnings**: Treating warnings as noise instead of issues
6. **Null Return Types**: Returning null without nullable return type
7. **Unchecked Parameters**: Not validating nullable parameters
8. **Generic Confusion**: Misunderstanding T? in generic methods
9. **Legacy Assumptions**: Assuming all references can be null
10. **False Confidence**: Trusting ! operator without verification

## When to Use

Use this skill when:

- Writing null-safe C# code
- Migrating to nullable reference types
- Preventing NullReferenceExceptions
- Designing clear APIs with explicit nullability
- Working with optional values
- Implementing defensive programming
- Refactoring legacy code
- Setting up new C# projects
- Enforcing null safety at compile time
- Working with generic nullable types

## Resources

- [Nullable Reference Types](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references)
- [Nullable Reference Types Migration](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-migration-strategies)
- [Nullable Attributes](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/attributes/nullable-analysis)
- [Nullable Warning Codes](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/nullable-warnings)
- [Tutorial: Update Code with Nullable Reference Types](https://learn.microsoft.com/en-us/dotnet/csharp/tutorials/nullable-reference-types)
