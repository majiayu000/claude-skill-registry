---
name: error-handling-vassovass-scl-v3
description: Centralized error handling system for StepLeague using AppError class,
  error codes, and reporting. Use when implementing error handling, catching exceptions,
  or displaying error messages to users. Key
---

---
name: error-handling
description: Centralized error handling system for StepLeague using AppError class, error codes, and reporting. Use when implementing error handling, catching exceptions, or displaying error messages to users. Keywords: error, exception, AppError, ErrorCode, catch, try, toast, logging.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.1"
  project: "stepleague"
---

# Error Handling Skill

## Overview

StepLeague uses a centralized error handling system in `src/lib/errors.ts`.

**Key Components:**
- `AppError` - Typed error class with codes and context
- `ErrorCode` - Enum of all error types
- `normalizeError()` - Convert any error to AppError
- `reportError()` / `reportErrorClient()` - Log and report errors

---

## Throwing Errors

### Use AppError with Specific Codes

```typescript
import { AppError, ErrorCode } from "@/lib/errors";

throw new AppError({
  code: ErrorCode.UPLOAD_TOO_LARGE,
  message: "File exceeds 5MB limit",
  context: { fileSize: file.size, maxSize: MAX_SIZE },
  recoverable: true, // Can user retry?
});
```

### AppError Options

| Option | Type | Description |
|--------|------|-------------|
| `code` | `ErrorCode` | **Required.** Error type for programmatic handling |
| `message` | `string` | **Required.** Human-readable description |
| `context` | `object` | Additional debug info |
| `cause` | `Error` | Original error that caused this |
| `recoverable` | `boolean` | Can user retry? Default: `true` |

---

## Available Error Codes

### Upload/Attachment Errors
- `UPLOAD_FAILED` - General upload failure
- `UPLOAD_TOO_LARGE` - File size limit exceeded
- `UPLOAD_INVALID_TYPE` - Wrong file type
- `UPLOAD_INVALID_FORMAT` - Invalid file format
- `UPLOAD_PROCESSING_FAILED` - Image processing failed
- `UPLOAD_STORAGE_ERROR` - Storage service error
- `ATTACHMENT_NOT_FOUND` - Attachment doesn't exist
- `ATTACHMENT_FETCH_FAILED` - Failed to retrieve attachment
- `ATTACHMENT_DELETE_FAILED` - Failed to delete attachment

### API Errors
- `API_REQUEST_FAILED` - General API failure
- `API_FETCH_FAILED` - Network fetch failed
- `API_VALIDATION_ERROR` - Request validation failed
- `API_UNAUTHORIZED` - Not authenticated (401)
- `API_FORBIDDEN` - Not authorized (403)
- `API_NOT_FOUND` - Resource not found (404)

### Database Errors
- `DB_INSERT_FAILED` - Insert operation failed
- `DB_UPDATE_FAILED` - Update operation failed
- `DB_DELETE_FAILED` - Delete operation failed
- `DB_QUERY_FAILED` - Select query failed

### Menu Errors
- `MENU_NOT_FOUND` - Menu doesn't exist
- `MENU_CREATE_FAILED` - Failed to create menu
- `MENU_ITEM_NOT_FOUND` - Menu item doesn't exist
- `MENU_ITEM_CREATE_FAILED` - Failed to create item
- `MENU_ITEM_UPDATE_FAILED` - Failed to update item
- `MENU_ITEM_DELETE_FAILED` - Failed to delete item
- `MENU_BATCH_UPDATE_FAILED` - Failed to reorder items
- `MENU_INVALID_HIERARCHY` - Invalid parent/child structure

### Form/Validation Errors
- `VALIDATION_FAILED` - General validation failure
- `REQUIRED_FIELD_MISSING` - Required field is empty

### Network Errors
- `NETWORK_ERROR` - No network connection
- `TIMEOUT_ERROR` - Request timed out
- `REQUEST_TIMEOUT` - Operation timed out
- `RATE_LIMIT_EXCEEDED` - Too many requests

### Fallback
- `UNKNOWN_ERROR` - Catch-all for unexpected errors

---

## Catching & Reporting Errors

### Standard Pattern

```typescript
import { normalizeError, reportErrorClient, ErrorCode } from "@/lib/errors";
import { toast } from "@/hooks/use-toast";

try {
  await doSomething();
} catch (err) {
  // 1. Normalize to AppError
  const appError = normalizeError(err, ErrorCode.API_REQUEST_FAILED);

  // 2. Report (logs to console, future: Sentry)
  reportErrorClient(appError);

  // 3. Show user-friendly message
  toast({
    title: "Error",
    description: appError.toUserMessage(),
    variant: "destructive",
  });
}
```

### User-Friendly Messages

`appError.toUserMessage()` converts technical errors to friendly text:

| Code | User Message |
|------|-------------|
| `UPLOAD_TOO_LARGE` | "The file is too large. Please choose a smaller file." |
| `NETWORK_ERROR` | "Connection lost. Please check your internet and try again." |
| `API_UNAUTHORIZED` | "Please sign in to continue." |
| `API_FORBIDDEN` | "You don't have permission to do this." |

---

## Creating Errors from API Responses

```typescript
import { errorFromResponse } from "@/lib/errors";

const response = await fetch("/api/something");

if (!response.ok) {
  const appError = await errorFromResponse(response, "Failed to save");
  throw appError;
}
```

This automatically:
- Extracts error message from JSON body
- Maps HTTP status to ErrorCode
- Sets `recoverable` based on status (5xx = retryable)

---

## Server-Side Error Reporting

```typescript
import { reportError } from "@/lib/errors";

// In API route
try {
  await doServerThing();
} catch (error) {
  await reportError(error, user?.id, requestId);
  return serverError("Operation failed");
}
```

Server-side reporting uses `@/lib/server/logger` for Vercel logs.

---

## Best Practices

### 1. Always Normalize Unknown Errors

```typescript
// ✅ Normalize any caught error
const appError = normalizeError(err, ErrorCode.UNKNOWN_ERROR);

// ❌ Don't assume error type
console.log(err.message); // May not be an Error!
```

### 2. Provide Context for Debugging

```typescript
throw new AppError({
  code: ErrorCode.UPLOAD_FAILED,
  message: "Failed to upload image",
  context: {
    filename: file.name,
    size: file.size,
    type: file.type,
    userId: user.id,
  },
});
```

### 3. Chain Errors with Cause

```typescript
try {
  await uploadToStorage(file);
} catch (cause) {
  throw new AppError({
    code: ErrorCode.UPLOAD_STORAGE_ERROR,
    message: "Storage upload failed",
    cause: cause instanceof Error ? cause : undefined,
  });
}
```

### 4. Use recoverable Flag

```typescript
// User can retry
throw new AppError({
  code: ErrorCode.NETWORK_ERROR,
  message: "Request failed",
  recoverable: true, // Show "Try Again" button
});

// User cannot recover
throw new AppError({
  code: ErrorCode.API_FORBIDDEN,
  message: "Access denied",
  recoverable: false, // Show "Contact Support"
});
```

---

## Adding New Error Codes

When adding new features that need specific error handling:

1. **Add to ErrorCode enum** in `src/lib/errors.ts`:

```typescript
export enum ErrorCode {
  // ... existing codes

  // New feature errors
  MY_FEATURE_FAILED = 'MY_FEATURE_FAILED',
  MY_FEATURE_INVALID = 'MY_FEATURE_INVALID',
}
```

2. **Add user-friendly message** in `toUserMessage()`:

```typescript
const friendlyMessages: Partial<Record<ErrorCode, string>> = {
  // ... existing messages
  [ErrorCode.MY_FEATURE_FAILED]: 'Unable to complete operation. Please try again.',
};
```

---

## Reference Files

| File | Purpose |
|------|---------|
| `src/lib/errors.ts` | AppError class, ErrorCode enum, utilities |
| `src/lib/server/logger.ts` | Server-side logging |

---

## Related Skills

- `api-handler` - Uses error handling for API routes
- `architecture-philosophy` - Error handling is key defensive pattern
