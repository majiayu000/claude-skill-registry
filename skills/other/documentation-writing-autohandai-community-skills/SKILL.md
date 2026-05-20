---
name: documentation-writing
description: Technical documentation best practices and API documentation
license: MIT
compatibility: typedoc 0.25+, jsdoc 4+, markdown
allowed-tools: read_file write_file apply_patch search_with_context
---

# Documentation Writing

## Core Principles

1. **Audience-focused** - Know who you're writing for
2. **Task-oriented** - Help users accomplish goals
3. **Scannable** - Use headers, lists, and code blocks
4. **Accurate** - Keep in sync with code
5. **Complete** - Cover common use cases and edge cases

## README Structure

```markdown
# Project Name

Brief description (1-2 sentences).

## Features

- Feature 1
- Feature 2

## Installation

```bash
npm install package-name
```

## Quick Start

```typescript
import { thing } from 'package-name';
// Minimal working example
```

## Usage

### Basic Usage
Detailed examples with explanations.

### Advanced Usage
Complex scenarios and configuration.

## API Reference

Link to detailed docs or inline reference.

## Contributing

How to contribute to the project.

## License

MIT
```

## JSDoc/TSDoc Comments

### Functions
```typescript
/**
 * Calculates the total price including tax.
 *
 * @param basePrice - The price before tax
 * @param taxRate - Tax rate as a decimal (e.g., 0.08 for 8%)
 * @returns The total price with tax applied
 *
 * @example
 * ```ts
 * const total = calculateTotal(100, 0.08);
 * // Returns: 108
 * ```
 *
 * @throws {RangeError} If taxRate is negative
 */
function calculateTotal(basePrice: number, taxRate: number): number {
  if (taxRate < 0) throw new RangeError('Tax rate cannot be negative');
  return basePrice * (1 + taxRate);
}
```

### Classes
```typescript
/**
 * Manages user authentication and session state.
 *
 * @remarks
 * This class handles OAuth2 authentication flows and maintains
 * session tokens in secure storage.
 *
 * @example
 * ```ts
 * const auth = new AuthManager({ clientId: 'xxx' });
 * await auth.login();
 * const user = auth.getCurrentUser();
 * ```
 */
class AuthManager {
  /**
   * Creates a new AuthManager instance.
   * @param config - Authentication configuration options
   */
  constructor(config: AuthConfig) {}

  /**
   * Initiates the login flow.
   * @returns Promise that resolves when authentication completes
   */
  async login(): Promise<void> {}
}
```

### Interfaces
```typescript
/**
 * Configuration options for the API client.
 */
interface ApiClientConfig {
  /**
   * Base URL for all API requests.
   * @example "https://api.example.com/v1"
   */
  baseUrl: string;

  /**
   * Request timeout in milliseconds.
   * @default 30000
   */
  timeout?: number;

  /**
   * Custom headers to include in all requests.
   */
  headers?: Record<string, string>;
}
```

## API Documentation

### OpenAPI/Swagger
```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0
  description: API for managing users

paths:
  /users:
    get:
      summary: List all users
      description: Returns a paginated list of users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    $ref: '#/components/schemas/Pagination'
```

### Endpoint Documentation
```markdown
## Create User

Creates a new user account.

### Request

`POST /api/v1/users`

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

#### Body

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| name | string | Yes | 2-100 characters |
| role | string | No | "user" or "admin" (default: "user") |

### Response

#### Success (201 Created)

```json
{
  "success": true,
  "data": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2025-01-02T12:00:00Z"
  }
}
```

#### Error (400 Bad Request)

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": {
      "email": "Invalid email format"
    }
  }
}
```
```

## Code Examples

### Good Example
```typescript
// ✅ Shows real use case with context
import { createClient } from 'my-api';

const client = createClient({
  apiKey: process.env.API_KEY,
  region: 'us-east-1',
});

// Fetch user with error handling
try {
  const user = await client.users.get('user_123');
  console.log(`Found user: ${user.name}`);
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    console.log('User does not exist');
  } else {
    throw error; // Re-throw unexpected errors
  }
}
```

### Bad Example
```typescript
// ❌ Too abstract, no context
const client = new Client(options);
const result = client.doThing(data);
```

## Changelog Format

```markdown
# Changelog

## [1.2.0] - 2025-01-02

### Added
- New `exportToPDF()` method for reports (#123)
- Support for custom themes

### Changed
- Improved performance of data loading by 40%
- Updated minimum Node.js version to 18

### Fixed
- Fixed memory leak in long-running processes (#456)
- Corrected timezone handling for scheduled tasks

### Deprecated
- `legacyExport()` - use `exportToPDF()` instead

### Security
- Updated dependencies to patch CVE-2025-XXXX
```

## Best Practices

1. **Write for scanning** - Use headers, bullets, tables
2. **Show, don't tell** - Include working code examples
3. **Keep examples minimal** - Show the concept, not everything
4. **Update with code** - Docs rot faster than code
5. **Test your examples** - Ensure they actually work
6. **Link liberally** - Connect related concepts
7. **Use consistent terminology** - Define terms once
8. **Include troubleshooting** - Common errors and solutions
