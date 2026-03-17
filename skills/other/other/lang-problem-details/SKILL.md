---
name: lang__problem_details
description: Adds RFC 7807 ProblemDetails error responses with typed error codes in handlers and endpoints. Use when implementing validation, error handling, or API responses. Returns standardized errors with HTTP status mapping.
---

All API errors MUST use the Result pattern with ProblemDetails responses. Errors are typed, include machine-readable error codes, and automatically map to appropriate HTTP status codes.

## Pattern Overview

**Result → Error → ProblemDetails → HTTP Response**

1. Create `Result.Failure(Error)` with error type and code
2. Call `.ToProblemDetails()` to convert to IResult
3. Framework automatically serializes to RFC 7807 format with status code

## Error Types & Status Codes

| Error Type | HTTP Status | Use When |
|------------|-------------|----------|
| `Error.Validation()` | 400 Bad Request | Input validation fails, business rules violated |
| `Error.NotFound()` | 404 Not Found | Resource doesn't exist |
| `Error.Conflict()` | 409 Conflict | Resource state conflict (already exists, already deleted) |
| `Error.Unauthorized()` | 401 Unauthorized | Authentication required or failed |
| `Error.Forbidden()` | 403 Forbidden | Authenticated but not authorized |
| `Error.InternalServerError()` | 500 Internal Server Error | Unexpected exceptions |

## Error Codes

Error codes follow pattern: `ERR_{DOMAIN}_{ERROR_NAME}`

**Existing domains**: Books, Authors, Publishers, Categories, Auth, Cart, Admin, Tenancy, Passkey

Error codes are defined in `src/BookStore.Shared/Models/ErrorCodes.cs`:

```csharp
public static class ErrorCodes
{
    public static class Books
    {
        public const string TitleRequired = "ERR_BOOK_TITLE_REQUIRED";
        public const string NotFound = "ERR_BOOK_NOT_FOUND";
        // ... more codes
    }
}
```

## Steps

1. **Identify Error Type**
   - Determine which Error factory method matches your scenario
   - Choose appropriate HTTP status code mapping

2. **Find or Add Error Code**
   - Check `ErrorCodes.<Domain>` for existing code
   - Add new code if needed following naming pattern
   - **Template**: See [templates/ErrorCodes.Domain.cs](templates/ErrorCodes.Domain.cs)

3. **Create Error Result**
   - Use `Result.Failure(Error.<Type>(code, message))`
   - Include helpful message for developers/UI
   - Return `.ToProblemDetails()`

4. **Add Logging** (Optional but Recommended)
   - Use `/lang__logger_message` for structured logging
   - Log before returning error for diagnostics

## Examples

**Validation Error (400)**:
```csharp
if (string.IsNullOrWhiteSpace(command.Title))
{
    Log.Books.TitleRequired(logger, command.Id);
    return Result.Failure(
        Error.Validation(
            ErrorCodes.Books.TitleRequired,
            "Book title is required"
        )).ToProblemDetails();
}
```

**Not Found Error (404)**:
```csharp
var book = await session.LoadAsync<BookDetails>(id);
if (book is null)
{
    Log.Books.BookNotFound(logger, id);
    return Result.Failure(
        Error.NotFound(
            ErrorCodes.Books.BookNotFound,
            "Book not found"
        )).ToProblemDetails();
}
```

**Conflict Error (409)**:
```csharp
if (aggregate.IsDeleted)
{
    return Result.Failure(
        Error.Conflict(
            ErrorCodes.Books.AlreadyDeleted,
            "Cannot update a deleted book"
        )).ToProblemDetails();
}
```

**Unauthorized Error (401)**:
```csharp
if (userId is null)
{
    return Result.Failure(
        Error.Unauthorized(
            ErrorCodes.Auth.InvalidToken,
            "User not authenticated"
        )).ToProblemDetails();
}
```

**From Aggregate (Business Logic)**:
```csharp
var eventResult = BookAggregate.CreateEvent(/* ... */);
if (eventResult.IsFailure)
{
    return eventResult.ToProblemDetails();
}

// Use the event
session.Events.StartStream<BookAggregate>(id, eventResult.Value);
```

**Internal Server Error (500)**:
```csharp
catch (Exception ex)
{
    Log.Books.UnexpectedError(logger, ex);
    return Result.Failure(
        Error.InternalServerError(
            ErrorCodes.Books.InternalError,
            $"An unexpected error occurred: {ex.Message}"
        )).ToProblemDetails();
}
```

## Response Format

ProblemDetails JSON response includes:

```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
  "title": "Bad Request",
  "status": 400,
  "detail": "Book title is required",
  "error": "ERR_BOOK_TITLE_REQUIRED"
}
```

- `type`: RFC 7231 reference
- `title`: Human-readable status name
- `status`: HTTP status code
- `detail`: Error message
- `error`: Machine-readable error code (in extensions)

## Common Patterns

**Multiple Validations**:
```csharp
// Check culture codes
if (!CultureValidator.IsValidCultureCode(command.Language))
{
    return Result.Failure(
        Error.Validation(
            ErrorCodes.Books.LanguageInvalid,
            "Invalid language code"
        )).ToProblemDetails();
}

// Check translations
if (!CultureValidator.ValidateTranslations(command.Translations, out var invalidCodes))
{
    return Result.Failure(
        Error.Validation(
            ErrorCodes.Books.TranslationLanguageInvalid,
            $"Invalid language codes: {string.Join(", ", invalidCodes)}"
        )).ToProblemDetails();
}
```

**Aggregate Validation**:
```csharp
// Let aggregate handle business rules
var eventResult = aggregate.UpdateEvent(command.Name);
if (eventResult.IsFailure)
{
    // Aggregate already created appropriate Error type
    return eventResult.ToProblemDetails();
}

session.Events.Append(id, eventResult.Value);
```

**Version Conflict**:
```csharp
var expectedVersion = ETagHelper.ParseETag(command.ETag);
if (expectedVersion.HasValue && aggregate.Version != expectedVersion.Value)
{
    return ETagHelper.PreconditionFailed(); // Returns 412 Precondition Failed
}
```

## Related Skills

**Prerequisites**:
- Understanding of Result pattern in `src/BookStore.Shared/Models/Result.cs`

**See Also**:
- `/lang__logger_message` - Add logging alongside error handling
- `/wolverine__create_operation` - Uses error handling in create handlers
- `/wolverine__update_operation` - Uses error handling in update handlers
- `/wolverine__delete_operation` - Uses error handling in delete handlers
- `src/BookStore.Shared/Models/Error.cs` - Error factory methods
- `src/BookStore.Shared/Models/ErrorCodes.cs` - All error codes
- `src/BookStore.ApiService/Infrastructure/Extensions/ResultExtensions.cs` - ToProblemDetails implementation
