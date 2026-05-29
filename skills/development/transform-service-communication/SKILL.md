---
name: transform-service-communication
description: Transforms direct service calls to use ServiceClient with config-driven URLs following ModuleImplementationGuide.md Section 5.3. Replaces hardcoded URLs with config values, uses ServiceClient from @coder/shared, adds circuit breakers and retry logic, implements service-to-service JWT auth, adds correlation ID logging, and handles service failures gracefully. Use when refactoring service calls, removing hardcoded URLs, or implementing service-to-service auth.
---

# Transform Service Communication

Transforms direct service calls to use ServiceClient with config-driven URLs.

## Core Principle

**ALL service URLs MUST come from config, never hardcoded.**

Reference: ModuleImplementationGuide.md Section 5.3, .cursorrules (Service Communication)

## ServiceClient Pattern

Reference: containers/shared/src/services/ServiceClient.ts

### Basic Usage

```typescript
import { ServiceClient } from '@coder/shared';
import { loadConfig } from '../config';

const config = loadConfig();

// ✅ Correct: Create client with config URL
const authClient = new ServiceClient({
  baseURL: config.services.auth.url, // From config!
  timeout: 5000,
  retries: 3,
  circuitBreaker: {
    enabled: true,
    threshold: 5,
    timeout: 30000,
  },
});

// Make request
const user = await authClient.get('/api/v1/users/123', {
  headers: {
    'X-Tenant-ID': tenantId,
    'Authorization': `Bearer ${serviceToken}`,
  },
});
```

### ❌ Wrong Patterns

```typescript
// ❌ Hardcoded URL
const response = await fetch('http://localhost:3021/api/users/123');

// ❌ Direct import from another module
import { UserService } from '../services/user.service';

// ❌ Hardcoded port
const response = await axios.get('http://localhost:3021/api/users/123');
```

## Service-to-Service Authentication

Always include JWT token and tenant ID:

```typescript
import { ServiceClient } from '@coder/shared';
import { getServiceToken } from '@coder/shared'; // Helper to get service JWT

const client = new ServiceClient({
  baseURL: config.services.auth.url,
  timeout: 5000,
});

// Get service token for authentication
const serviceToken = await getServiceToken();

const response = await client.get('/api/v1/users/123', {
  headers: {
    'X-Tenant-ID': tenantId, // ✅ Always include tenantId
    'Authorization': `Bearer ${serviceToken}`, // ✅ Service-to-service JWT
    'X-Request-ID': requestId, // ✅ Correlation ID
  },
});
```

## Circuit Breaker

ServiceClient includes built-in circuit breaker:

```typescript
const client = new ServiceClient({
  baseURL: config.services.auth.url,
  timeout: 5000,
  retries: 3,
  circuitBreaker: {
    enabled: true,
    threshold: 5, // Open after 5 failures
    timeout: 30000, // Wait 30s before retry
  },
});

try {
  const response = await client.get('/api/v1/users/123');
} catch (error) {
  // Circuit breaker will prevent requests if service is down
  if (error.message.includes('Circuit breaker is OPEN')) {
    // Handle gracefully - return cached data or default
    return getCachedUser(id);
  }
  throw error;
}
```

## Retry Logic

ServiceClient includes exponential backoff retry:

```typescript
const client = new ServiceClient({
  baseURL: config.services.auth.url,
  timeout: 5000,
  retries: 3, // Retry up to 3 times
});

// Automatically retries on network errors or 5xx errors
// Uses exponential backoff: 1s, 2s, 4s, 8s (max 10s)
const response = await client.get('/api/v1/users/123');
```

## Error Handling

Handle service failures gracefully:

```typescript
import { AppError } from '@coder/shared';
import { log } from '../utils/logger';

async function getUser(tenantId: string, userId: string) {
  try {
    const client = new ServiceClient({
      baseURL: config.services.user_management.url,
    });
    
    const serviceToken = await getServiceToken();
    const user = await client.get(`/api/v1/users/${userId}`, {
      headers: {
        'X-Tenant-ID': tenantId,
        'Authorization': `Bearer ${serviceToken}`,
      },
    });
    
    return user;
  } catch (error: any) {
    log.error('Failed to get user from user-management service', error, {
      tenantId,
      userId,
    });
    
    // Handle circuit breaker
    if (error.message?.includes('Circuit breaker is OPEN')) {
      throw new AppError(
        'User service temporarily unavailable',
        503,
        'SERVICE_UNAVAILABLE'
      );
    }
    
    // Handle 404
    if (error.response?.status === 404) {
      throw new AppError('User not found', 404, 'NOT_FOUND');
    }
    
    // Re-throw other errors
    throw error;
  }
}
```

## Configuration Pattern

Add service URLs to config/default.yaml:

```yaml
services:
  auth:
    url: ${AUTH_URL:-http://localhost:3021}
  user_management:
    url: ${USER_MANAGEMENT_URL:-http://localhost:3022}
  logging:
    url: ${LOGGING_URL:-http://localhost:3014}
  notification:
    url: ${NOTIFICATION_MANAGER_URL:-http://localhost:3001}
```

## Service Client Factory

Create reusable client instances:

```typescript
// src/services/clients.ts
import { ServiceClient } from '@coder/shared';
import { getConfig } from '../config';

let authClient: ServiceClient | null = null;
let userManagementClient: ServiceClient | null = null;

export function getAuthClient(): ServiceClient {
  if (!authClient) {
    const config = getConfig();
    authClient = new ServiceClient({
      baseURL: config.services.auth.url,
      timeout: 5000,
      retries: 3,
      circuitBreaker: {
        enabled: true,
        threshold: 5,
        timeout: 30000,
      },
    });
  }
  return authClient;
}

export function getUserManagementClient(): ServiceClient {
  if (!userManagementClient) {
    const config = getConfig();
    userManagementClient = new ServiceClient({
      baseURL: config.services.user_management.url,
      timeout: 5000,
      retries: 3,
      circuitBreaker: {
        enabled: true,
        threshold: 5,
        timeout: 30000,
      },
    });
  }
  return userManagementClient;
}
```

## Usage in Services

```typescript
import { getAuthClient } from './clients';
import { getServiceToken } from '@coder/shared';

class MyService {
  async validateUser(tenantId: string, userId: string) {
    const client = getAuthClient();
    const serviceToken = await getServiceToken();
    
    try {
      const user = await client.get(`/api/v1/users/${userId}`, {
        headers: {
          'X-Tenant-ID': tenantId,
          'Authorization': `Bearer ${serviceToken}`,
        },
      });
      
      return user;
    } catch (error: any) {
      if (error.response?.status === 404) {
        throw new AppError('User not found', 404, 'NOT_FOUND');
      }
      throw error;
    }
  }
}
```

## Transformation Checklist

When transforming old code:

- [ ] Replace hardcoded URLs with config.services.{name}.url
- [ ] Use ServiceClient from @coder/shared
- [ ] Include X-Tenant-ID header in all requests
- [ ] Include Authorization header with service token
- [ ] Add correlation ID (X-Request-ID) for logging
- [ ] Configure circuit breaker (enabled by default)
- [ ] Configure retry logic (default: 3 retries)
- [ ] Handle errors gracefully (circuit breaker, 404, etc.)
- [ ] Log service calls with context

## Common Mistakes

1. **Hardcoded URLs**
   - Always use config.services.{name}.url

2. **Missing tenant ID**
   - Always include X-Tenant-ID header

3. **Missing service token**
   - Always include Authorization header

4. **No error handling**
   - Handle circuit breaker and service failures

5. **Direct imports**
   - Never import from another module's src/ folder
