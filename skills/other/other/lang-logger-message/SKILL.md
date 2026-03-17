---
name: lang__logger_message
description: Adds structured, high-performance logging using LoggerMessage source generator. Use when adding logs to handlers, services, or middleware. Organizes logs by domain (Books, Users, etc.) in Infrastructure/Logging/Log.<Domain>.cs files.
---

All logging in BookStore MUST use the LoggerMessage source generator pattern for performance and consistency. Logs are organized by domain in separate partial classes.

## Structure

Logs are organized in `src/BookStore.ApiService/Infrastructure/Logging/Log.<Domain>.cs`:
- Each domain (Books, Users, etc.) is a nested partial class inside `Log`
- Use appropriate log levels: Information, Warning, Error, Debug
- Include relevant parameters for structured logging
- Use descriptive method names in past tense for completed actions

## Steps

1. **Identify Domain**
   - Determine which domain your logging belongs to (Books, Authors, Users, etc.)
   - Existing domains: Books, Authors, Publishers, Categories, Users, Email, Tenants, Notifications, Infrastructure, Maintenance, Seeding
   - Create new domain file if needed: `Log.<YourDomain>.cs`

2. **Add Log Method**
   - Open or create `Infrastructure/Logging/Log.<Domain>.cs`
   - Add a new partial method with `[LoggerMessage]` attribute
   - **Template**: See [templates/Log.Domain.cs](templates/Log.Domain.cs) for structure
   - Include all relevant parameters for context

3. **Choose Log Level**
   - `LogLevel.Information`: Success operations, normal flow
   - `LogLevel.Warning`: Validation failures, recoverable errors, suspicious activity
   - `LogLevel.Error`: Exceptions, failures requiring attention
   - `LogLevel.Debug`: Detailed diagnostic information

4. **Use in Code**
   - Inject `ILogger<YourClass>` in constructor
   - Call: `Log.<Domain>.<MethodName>(logger, params...)`
   - For errors: Exception parameter comes after logger, before other params

## Examples

**Information Level**:
```csharp
[LoggerMessage(
    Level = LogLevel.Information,
    Message = "Book created successfully: Id={BookId}, Title={Title}")]
public static partial void BookCreated(
    ILogger logger,
    Guid bookId,
    string title);
```

**Error Level with Exception**:
```csharp
[LoggerMessage(
    Level = LogLevel.Error,
    Message = "Failed to create book: Title={Title}")]
public static partial void BookCreationFailed(
    ILogger logger,
    Exception ex,
    string title);
```

**Usage in Handler**:
```csharp
public class CreateBookHandler(ILogger<CreateBookHandler> logger)
{
    public Task Handle(CreateBook command)
    {
        try
        {
            // ... create book logic ...
            Log.Books.BookCreated(logger, bookId, title);
        }
        catch (Exception ex)
        {
            Log.Books.BookCreationFailed(logger, ex, title);
            throw;
        }
    }
}
```

## Common Patterns

**Operation Flow**:
- Operation starting: `<Entity>Creating`, `<Entity>Updating`, `<Entity>Deleting`
- Operation success: `<Entity>Created`, `<Entity>Updated`, `<Entity>Deleted`
- Operation failure: `<Entity>CreationFailed`, `<Entity>UpdateFailed`, etc.

**Validation/Security**:
- Use `LogLevel.Warning` for validation failures, authentication issues
- Include enough context to debug without sensitive data

**Correlation**:
- Include CorrelationId when starting operations for request tracing
- Include entity IDs, versions, relevant metadata

## Related Skills

**Prerequisites**:
- Understanding of the domain you're logging for

**See Also**:
- `/wolverine__create_operation` - Uses logging in command handlers
- `/wolverine__update_operation` - Uses logging in update handlers
- `/wolverine__delete_operation` - Uses logging in delete handlers
- `docs/architecture.md` - System architecture and patterns
- Existing domain files in `src/BookStore.ApiService/Infrastructure/Logging/`
