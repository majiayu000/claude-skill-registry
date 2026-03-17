---
name: api-client
description: REST API client builder with authentication, error handling, retry logic, and request management. Supports OAuth, JWT, API keys. Use when building API integrations, creating API clients, or working with REST services.
---

# API Client Builder

## Overview

Build robust REST API clients with authentication, comprehensive error handling, automatic retries, and request/response management.

## Quick Start

### Basic API Client

```javascript
const client = new APIClient({
  baseURL: 'https://api.example.com',
  apiKey: process.env.API_KEY
});

const response = await client.get('/users');
console.log(response.data);
```

## Features

- ✓ Multiple authentication methods (API key, OAuth, JWT)
- ✓ Automatic retry with exponential backoff
- ✓ Request/response logging
- ✓ Error classification and handling
- ✓ Rate limiting support
- ✓ Request timeout configuration

## Workflow

### Step 1: Configure Client

Create client with base configuration:

```javascript
const client = new APIClient({
  baseURL: 'https://api.example.com',
  timeout: 5000,
  retries: 3
});
```

### Step 2: Add Authentication

See [references/authentication-guide.md](references/authentication-guide.md) for all methods.

**API Key**:
```javascript
client.setAuth({
  type: 'apiKey',
  key: process.env.API_KEY
});
```

**OAuth 2.0**:
```javascript
client.setAuth({
  type: 'oauth',
  clientId: process.env.CLIENT_ID,
  clientSecret: process.env.CLIENT_SECRET
});
```

### Step 3: Make Requests

```javascript
// GET request
const users = await client.get('/users');

// POST request
const newUser = await client.post('/users', {
  name: 'John Doe',
  email: 'john@example.com'
});

// PUT request
const updated = await client.put('/users/123', {
  name: 'Jane Doe'
});

// DELETE request
await client.delete('/users/123');
```

### Step 4: Handle Errors

```javascript
try {
  const response = await client.get('/users');
  console.log(response.data);
} catch (error) {
  if (error.status === 401) {
    console.error('Authentication failed');
  } else if (error.status === 429) {
    console.error('Rate limit exceeded');
  } else {
    console.error('Request failed:', error.message);
  }
}
```

## Configuration

### Complete Configuration Options

```javascript
const client = new APIClient({
  // Base configuration
  baseURL: 'https://api.example.com',
  timeout: 5000,                  // Request timeout (ms)

  // Retry configuration
  retries: 3,                     // Number of retries
  retryDelay: 1000,               // Initial retry delay (ms)
  retryMult iplier: 2,              // Exponential backoff multiplier

  // Authentication (see references/authentication-guide.md)
  auth: {
    type: 'apiKey',
    key: process.env.API_KEY
  },

  // Headers
  headers: {
    'Content-Type': 'application/json',
    'Custom-Header': 'value'
  },

  // Logging
  logging: true,                  // Enable request/response logging
  logLevel: 'info'               // debug, info, warn, error
});
```

See [templates/api-config-template.json](templates/api-config-template.json) for complete configuration template.

## Authentication Methods

### Method 1: API Key

```javascript
client.setAuth({
  type: 'apiKey',
  key: process.env.API_KEY,
  header: 'X-API-Key'  // Optional, default: 'Authorization'
});
```

### Method 2: OAuth 2.0

See [references/authentication-guide.md#oauth](references/authentication-guide.md#oauth) for complete OAuth flow.

### Method 3: JWT

See [references/authentication-guide.md#jwt](references/authentication-guide.md#jwt) for JWT implementation.

## Error Handling

### Error Classification

Errors are classified into categories for appropriate handling:

| Status Code | Category | Retry? | Action |
|-------------|----------|--------|--------|
| 400 | Client Error | No | Fix request |
| 401 | Auth Error | No | Refresh token |
| 403 | Permission | No | Check permissions |
| 404 | Not Found | No | Check endpoint |
| 429 | Rate Limit | Yes | Wait and retry |
| 500 | Server Error | Yes | Retry |
| 503 | Unavailable | Yes | Retry |

See [references/error-handling.md](references/error-handling.md) for complete error handling strategies.

## Validation

Validate API configuration before using:

```bash
python scripts/validate-config.py config.json
```

## Templates

Copy templates from `templates/` directory:
- `api-config-template.json` - Complete configuration
- `error-handler-template.js` - Error handling code
- `retry-logic-template.js` - Retry implementation

## References

- [Authentication Guide](references/authentication-guide.md) - All auth methods
- [Error Handling](references/error-handling.md) - Comprehensive error strategies
- [Rate Limiting](references/rate-limiting.md) - Handle rate limits
- [Testing](references/testing-apis.md) - Test API clients

---

**Version**: 1.0
**Last Updated**: October 25, 2025
**Example Type**: Complex skill (full structure)
