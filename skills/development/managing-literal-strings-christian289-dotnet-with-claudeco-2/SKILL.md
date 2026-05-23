---
name: managing-literal-strings
description: "Manages literal strings by pre-defining them as const string in C#. Use when organizing string constants, log messages, exception messages, or UI texts across the codebase."
---

# Literal String Handling

A guide on handling literal strings in C# code.

## Project Structure

The templates folder contains a Console Application example (use latest .NET per version mapping).

```
templates/
└── LiteralStringSample/                ← Console Application
    ├── Constants/
    │   ├── Messages.cs                 ← General message constants
    │   └── LogMessages.cs              ← Log message constants
    ├── Program.cs                      ← Top-Level Statement entry point
    ├── GlobalUsings.cs
    └── LiteralStringSample.csproj
```

## Rule

**Literal strings should preferably be pre-defined as `const string`**

## Examples

### Good Example

```csharp
// Good example
const string ErrorMessage = "An error has occurred.";

if (condition)
    throw new Exception(ErrorMessage);
```

### Bad Example

```csharp
// Bad example
if (condition)
    throw new Exception("An error has occurred.");
```

## Constants Class Structure

Manage by separating into static classes by message type:

```csharp
// Constants/Messages.cs
namespace LiteralStringSample.Constants;

public static class Messages
{
    // Error messages
    public const string ErrorOccurred = "An error has occurred.";

    public const string InvalidInput = "Invalid input.";

    // Success messages
    public const string OperationSuccess = "Operation completed successfully.";
}
```

```csharp
// Constants/LogMessages.cs
namespace LiteralStringSample.Constants;

public static class LogMessages
{
    // Information logs
    public const string ApplicationStarted = "Application started.";

    // Format strings
    public const string UserLoggedIn = "User logged in: {0}";
}
```

## Usage Example

```csharp
using LiteralStringSample.Constants;

try
{
    if (string.IsNullOrEmpty(input))
    {
        throw new ArgumentException(Messages.InvalidInput);
    }

    Console.WriteLine(Messages.OperationSuccess);
}
catch (Exception)
{
    Console.WriteLine(Messages.ErrorOccurred);
}

// Using format strings
Console.WriteLine(string.Format(LogMessages.UserLoggedIn, userName));
```

## Reasons

1. **Maintainability**: Only one place to modify when changing messages
2. **Reusability**: Same messages can be used in multiple places
3. **Type safety**: Typos can be caught at compile time
4. **Performance**: Eliminates string literal duplication
5. **Consistency**: Messages can be managed in pairs (e.g., Korean/English)

