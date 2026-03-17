---
name: core-error-handling
description: Core error types and HTTP status code mapping patterns
---

# Core Error Usage Guide

## Overview

All modules **MUST** use core errors from `@zerobias-org/types-core-js` instead of generic TypeScript `Error` class. This guide provides the correct constructor patterns for each error type.

## 🚨 CRITICAL RULES

1. **NEVER use generic `Error` class** - Always use core errors
2. **Import from `@zerobias-org/types-core-js`** - All core errors are available from the main package
3. **Follow exact constructor signatures** - Each error has specific required and optional parameters
4. **Timestamp is usually optional** - Most errors auto-generate timestamps if not provided

## Common Core Errors and Constructor Patterns

### Authentication Errors

#### InvalidCredentialsError
Use for authentication failures (401 errors):
```typescript
import { InvalidCredentialsError } from '@zerobias-org/types-core-js';

// Basic usage (timestamp auto-generated)
throw new InvalidCredentialsError();

// With custom timestamp
throw new InvalidCredentialsError(new Date());
```

#### UnauthorizedError  
Use for authorization failures (403 errors):
```typescript
import { UnauthorizedError } from '@zerobias-org/types-core-js';

// Basic usage (timestamp auto-generated)
throw new UnauthorizedError();

// With custom timestamp
throw new UnauthorizedError(new Date());
```

### Input/Validation Errors

#### InvalidInputError
Use for bad request data (400/422 errors):
```typescript
import { InvalidInputError } from '@zerobias-org/types-core-js';

// Required: type and value
throw new InvalidInputError('username', 'invalid@value');

// With examples
throw new InvalidInputError('email', 'notanemail', ['user@example.com', 'admin@domain.com']);

// With custom timestamp
throw new InvalidInputError('id', '123abc', [], new Date());
```

### Resource Errors

#### NoSuchObjectError
Use for resource not found (404 errors):
```typescript
import { NoSuchObjectError } from '@zerobias-org/types-core-js';

// Required: type and id
throw new NoSuchObjectError('user', 'john_doe');
throw new NoSuchObjectError('organization', '12345');

// With custom timestamp
throw new NoSuchObjectError('repository', 'my-repo', new Date());
```

### Rate Limiting Errors

#### RateLimitExceededError
Use for rate limit exceeded (429 errors):
```typescript
import { RateLimitExceededError } from '@zerobias-org/types-core-js';

// Basic usage
throw new RateLimitExceededError();

// With call details
throw new RateLimitExceededError(new Date(), 100, '1 hour');

// With custom timestamp only
throw new RateLimitExceededError(new Date());
```

### Generic Errors

#### UnexpectedError
Use for server errors (500+ errors) and unexpected cases:
```typescript
import { UnexpectedError } from '@zerobias-org/types-core-js';

// Required: message
throw new UnexpectedError('Database connection failed');

// With custom status code
throw new UnexpectedError('Service unavailable', 503);

// With custom status code and timestamp
throw new UnexpectedError('Internal error', 500, new Date());
```

## HTTP Status Code to Core Error Mapping

| Status Code | Core Error | Constructor Example |
|-------------|------------|-------------------|
| 400 | `InvalidInputError` | `new InvalidInputError('field', 'value')` |
| 401 | `InvalidCredentialsError` | `new InvalidCredentialsError()` |
| 403 | `UnauthorizedError` | `new UnauthorizedError()` |
| 404 | `NoSuchObjectError` | `new NoSuchObjectError('type', 'id')` |
| 422 | `InvalidInputError` | `new InvalidInputError('field', 'value')` |
| 429 | `RateLimitExceededError` | `new RateLimitExceededError()` |
| 500+ | `UnexpectedError` | `new UnexpectedError('message')` |

## Error Handling Pattern for HTTP Clients

```typescript
import {
  InvalidCredentialsError,
  UnauthorizedError,
  NoSuchObjectError,
  InvalidInputError,
  RateLimitExceededError,
  UnexpectedError,
} from '@zerobias-org/types-core-js';

private handleApiError(error: any): never {
  const status = error.status || error.response?.status || 500;
  const message = error.message || 'Unknown error';
  
  switch (status) {
    case 401:
      throw new InvalidCredentialsError();
    
    case 403:
      if (message.toLowerCase().includes('rate limit')) {
        throw new RateLimitExceededError();
      }
      throw new UnauthorizedError();
    
    case 404:
      throw new NoSuchObjectError('resource', 'unknown');
    
    case 400:
    case 422:
      throw new InvalidInputError('request', message);
    
    case 429:
      throw new RateLimitExceededError();
    
    default:
      if (status >= 500) {
        throw new UnexpectedError(`Server error: ${message}`, status);
      }
      throw new UnexpectedError(`API error: ${message}`, status);
  }
}
```

## Additional Core Errors Available

### Complete Error Constructor Patterns

#### ParameterRequiredError
For missing required parameters:
```typescript
// Required: parameter name
throw new ParameterRequiredError('apiKey');
throw new ParameterRequiredError('organizationId');
```

#### NotFoundError
Alternative to NoSuchObjectError:
```typescript
// Required: message
throw new NotFoundError('Resource not found');
throw new NotFoundError('User does not exist');
```

#### TimeoutError
For timeout scenarios:
```typescript
// Required: message, timeout in ms
throw new TimeoutError('Request timed out', 30000);
throw new TimeoutError('Connection timeout', 5000);
```

#### ConflictError
For conflict scenarios (409):
```typescript
// Required: message
throw new ConflictError('Resource already exists');
throw new ConflictError('Duplicate email address');

// With details
throw new ConflictError('Username taken', { username: 'john_doe' });
```

#### ForbiddenError
For forbidden access:
```typescript
// No parameters - auto timestamp
throw new ForbiddenError();

// With custom timestamp
throw new ForbiddenError(new Date());
```

#### NotConnectedError
For connection state errors:
```typescript
// No parameters required
throw new NotConnectedError();

// With custom timestamp
throw new NotConnectedError(new Date());
```

#### IllegalArgumentError
For programming errors:
```typescript
// Required: argument name, value, reason
throw new IllegalArgumentError('pageSize', -1, 'Must be positive');
throw new IllegalArgumentError('email', 'invalid', 'Not a valid email format');
```

#### InvalidStateError
For invalid state transitions:
```typescript
// Required: current state, attempted action
throw new InvalidStateError('disconnected', 'send');
throw new InvalidStateError('pending', 'approve');
```

## Best Practices

1. **Choose the most specific error type** - Don't always default to UnexpectedError
2. **Provide meaningful context** - Use appropriate `type` and `id` values for NoSuchObjectError
3. **Include examples for validation errors** - Help users understand expected input format
4. **Let timestamps auto-generate** - Only provide custom timestamps when necessary
5. **Handle rate limits appropriately** - Check error messages for rate limit indicators
6. **Map HTTP status codes correctly** - Use the mapping table above as reference

## Import Statement

```typescript
import {
  InvalidCredentialsError,
  UnauthorizedError,
  NoSuchObjectError,
  InvalidInputError,
  RateLimitExceededError,
  UnexpectedError,
  // Add other errors as needed
} from '@zerobias-org/types-core-js';
```

## Complete Error Handling Utility Function

Create in `src/util.ts`:

```typescript
import {
  InvalidCredentialsError,
  UnauthorizedError,
  NoSuchObjectError,
  InvalidInputError,
  RateLimitExceededError,
  UnexpectedError,
  ConflictError,
  TimeoutError,
  ForbiddenError
} from '@zerobias-org/types-core-js';

export function handleAxiosError(error: any): never {
  // Log for debugging
  console.error('API Error:', error.message || error);

  // Extract status code
  const status = error.response?.status || error.status || 500;
  const data = error.response?.data || {};
  const message = data.message || data.error || error.message || 'Unknown error';

  // Extract resource type from URL if possible
  const urlMatch = error.config?.url?.match(/\/(\w+)\/[\w-]+$/);
  const resourceType = urlMatch ? urlMatch[1] : 'resource';

  // Extract resource ID from URL if possible
  const idMatch = error.config?.url?.match(/\/([\w-]+)$/);
  const resourceId = idMatch ? idMatch[1] : 'unknown';

  switch (status) {
    case 401:
      throw new InvalidCredentialsError();

    case 403:
      // Check if it's actually a rate limit
      if (message.toLowerCase().includes('rate') ||
          message.toLowerCase().includes('limit')) {
        throw new RateLimitExceededError();
      }
      throw new ForbiddenError();

    case 404:
      throw new NoSuchObjectError(resourceType, resourceId);

    case 400:
    case 422:
      // Extract field name if available
      const field = data.field || data.parameter || 'request';
      const value = data.value || message;
      throw new InvalidInputError(field, value);

    case 409:
      throw new ConflictError(message);

    case 429:
      const retryAfter = error.response?.headers['retry-after'];
      throw new RateLimitExceededError(new Date(), undefined, retryAfter);

    case 408:
    case 504:
      throw new TimeoutError(message, 30000);

    default:
      if (status >= 500) {
        throw new UnexpectedError(`Server error: ${message}`, status);
      }
      throw new UnexpectedError(`API error: ${message}`, status);
  }
}
```

## Usage in HTTP Client

```typescript
// In src/ServiceClient.ts
import axios, { AxiosInstance } from 'axios';
import { handleAxiosError } from './util';

export class ServiceClient {
  private httpClient: AxiosInstance;

  constructor() {
    this.httpClient = axios.create({
      timeout: 30000
    });

    // Add error interceptor
    this.httpClient.interceptors.response.use(
      response => response,
      error => handleAxiosError(error)
    );
  }

  // All requests automatically get error handling
  async get(path: string): Promise<any> {
    return this.httpClient.get(path);
  }
}
```
