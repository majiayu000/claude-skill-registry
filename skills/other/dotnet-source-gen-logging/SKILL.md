---
name: dotnet-source-gen-logging
description: Converts logging to use the LoggerMessage source generator for high-performance, AOT-compatible logging. Use when the user wants to optimize logging or organize log messages.
license: MIT
metadata:
  author: Im5tu
  version: "1.0"
  repositoryUrl: https://github.com/im5tu/dotnet-skills
allowed-tools: Bash(dotnet:*) Read Glob Grep AskUserQuestion
---

Convert existing logging calls to use the `LoggerMessage` source generator for high-performance, AOT-compatible logging with no boxing overhead and compile-time template parsing.

## When to Use

- Optimizing logging performance in hot paths
- Preparing for Native AOT deployment
- Organizing scattered log messages into logical groupings
- Standardizing EventIds across the codebase

## Steps

1. **Find ILogger usages and logging calls**
   - Search for `ILogger` field/parameter declarations
   - Find all logging calls: `LogInformation`, `LogWarning`, `LogError`, `LogDebug`, `LogTrace`, `LogCritical`
   - Note the log message templates and parameters

2. **Organize into logical groupings by domain**
   - Group related log messages by their functional area, eg:
     - `LoggingValidationExtensions` - validation-related logs
     - `LoggingAuthenticationExtensions` - auth-related logs
     - `LoggingDatabaseExtensions` - database-related logs
     - `LoggingHttpExtensions` - HTTP-related logs
     - `LoggingCacheExtensions` - caching-related logs
     - `LoggingMessagingExtensions` - messaging/queue-related logs

3. **Create partial static classes with extension methods**
   ```csharp
   public static partial class LoggingValidationExtensions
   {
       [LoggerMessage(
           EventId = 1001,
           Level = LogLevel.Warning,
           Message = "Validation failed for {EntityType}: {Errors}")]
       public static partial void ValidationFailed(
           this ILogger logger, string entityType, string errors);
   }
   ```

4. **Use EventId ranges per category**
   - 1000-1999: Validation
   - 2000-2999: Authentication
   - 3000-3999: Database
   - 4000-4999: HTTP
   - 5000-5999: Cache
   - 6000-6999: Messaging
   - 7000-7999: General/Application

5. **Replace inline logging calls with extension method calls**
   - Before: `_logger.LogWarning("Validation failed for {entityType}: {errors}", type, errs)`
   - After: `_logger.ValidationFailed(type, errs)`

6. **Verify with build**
   ```bash
   dotnet build
   ```

7. **If build fails**, review errors:
   - Missing `using` statements for the extension class namespace
   - Parameter type mismatches
   - Duplicate EventIds

8. **Report results**:
   - List all created extension classes
   - Show count of converted log messages per category
   - Confirm build status

## Key Notes

- **Requires .NET 6+** - the source generator is built into the SDK
- **Avoids boxing** - value types are not boxed when passed to the generated methods
- **Template parsed once** - message template is parsed at compile time, not runtime
- **Use PascalCase for placeholders** - `{EntityType}` not `{entityType}` (matching is case-insensitive, but PascalCase is the recommended convention)
- **Extension methods** - allows fluent `logger.MethodName()` syntax
- **Partial classes** - required for source generator to emit the implementation

## Example Conversion

Before:
```csharp
_logger.LogInformation("User {UserId} logged in from {IpAddress}", userId, ip);
_logger.LogWarning("Failed login attempt for {Username}", username);
```

After:
```csharp
// In LoggingAuthenticationExtensions.cs
public static partial class LoggingAuthenticationExtensions
{
    [LoggerMessage(
        EventId = 2001,
        Level = LogLevel.Information,
        Message = "User {UserId} logged in from {IpAddress}")]
    public static partial void UserLoggedIn(
        this ILogger logger, string userId, string ipAddress);

    [LoggerMessage(
        EventId = 2002,
        Level = LogLevel.Warning,
        Message = "Failed login attempt for {Username}")]
    public static partial void FailedLoginAttempt(
        this ILogger logger, string username);
}

// Usage
_logger.UserLoggedIn(userId, ip);
_logger.FailedLoginAttempt(username);
```
