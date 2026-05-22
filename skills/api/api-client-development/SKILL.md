---
name: api-client-development
description: Creating API clients with OpenAPI specs, authentication, and OAuth scopes for SCAPI and similar APIs
---

# API Client Development

This skill covers creating typed API clients using OpenAPI specifications, with proper authentication and OAuth scope handling. It builds on the patterns in [SDK Module Development](../sdk-module-development/SKILL.md).

## Overview

API clients in this project use:
- **openapi-fetch**: Type-safe HTTP client generated from OpenAPI specs
- **openapi-typescript**: Generates TypeScript types from OpenAPI specs
- **Middleware pattern**: Auth and logging injected via openapi-fetch middleware

## Creating a New API Client

### 1. Add the OpenAPI Spec

Place the spec in `packages/b2c-tooling-sdk/specs/`:

```
specs/
├── custom-apis-v1.yaml    # YAML or JSON
├── slas-admin-v1.yaml
└── ods-api-v1.json
```

### 2. Update Type Generation Script

In `packages/b2c-tooling-sdk/package.json`, add to the generate script:

```json
{
  "scripts": {
    "generate:types": "openapi-typescript specs/data-api.json -o src/clients/ocapi.generated.ts && openapi-typescript specs/newapi-v1.yaml -o src/clients/newapi.generated.ts"
  }
}
```

Run generation:

```bash
pnpm --filter @salesforce/b2c-tooling-sdk run generate:types
```

### 3. Create the Client Module

```typescript
// src/clients/newapi.ts
import createClient, {type Client} from 'openapi-fetch';
import type {AuthStrategy} from '../auth/types.js';
import type {paths, components} from './newapi.generated.js';
import {createAuthMiddleware, createLoggingMiddleware} from './middleware.js';

// Re-export generated types for consumers
export type {paths, components};

// Client type alias
export type NewApiClient = Client<paths>;

// Config interface
export interface NewApiClientConfig {
  hostname: string;
  // Add API-specific config here
}

// Factory function
export function createNewApiClient(
  config: NewApiClientConfig,
  auth: AuthStrategy
): NewApiClient {
  const client = createClient<paths>({
    baseUrl: `https://${config.hostname}/api/v1`,
  });

  // Middleware order: auth first (runs last), logging last (sees complete request)
  client.use(createAuthMiddleware(auth));
  client.use(createLoggingMiddleware('NEWAPI'));

  return client;
}
```

### 4. Export from Clients Barrel

```typescript
// src/clients/index.ts
export {createNewApiClient, type NewApiClient, type NewApiClientConfig} from './newapi.js';
export type {paths as NewApiPaths, components as NewApiComponents} from './newapi.js';
```

---

## SCAPI Client Pattern (OAuth Scope Injection)

SCAPI APIs require specific OAuth scopes. Instead of requiring CLI commands to manage scopes, **encapsulate scope logic in the client factory**.

### The Problem

Without encapsulation, CLI commands leak auth implementation details:

```typescript
// BAD: CLI command manages scopes
class MyCommand extends OAuthCommand {
  protected override loadConfiguration(): ResolvedConfig {
    const config = super.loadConfiguration();
    config.scopes = ['sfcc.custom-apis', `SALESFORCE_COMMERCE_API:${tenantId}`];
    return config;
  }
}
```

### The Solution

Use `OAuthStrategy.withAdditionalScopes()` in the client factory:

```typescript
// GOOD: Client encapsulates scope requirements
import {OAuthStrategy} from '../auth/oauth.js';
import type {AuthStrategy} from '../auth/types.js';

/** Default OAuth scopes required for this API */
export const MY_API_DEFAULT_SCOPES = ['sfcc.my-api'];

export interface MyApiClientConfig {
  shortCode: string;
  tenantId: string;           // Required for tenant-specific scope
  scopes?: string[];          // Optional override
}

export function createMyApiClient(
  config: MyApiClientConfig,
  auth: AuthStrategy
): MyApiClient {
  const client = createClient<paths>({
    baseUrl: `https://${config.shortCode}.api.commercecloud.salesforce.com/my-api/v1`,
  });

  // Build required scopes: domain scope + tenant-specific scope
  const requiredScopes = config.scopes ?? [
    ...MY_API_DEFAULT_SCOPES,
    buildTenantScope(config.tenantId),
  ];

  // If OAuth strategy, add required scopes; otherwise use as-is (e.g., for testing)
  const scopedAuth = auth instanceof OAuthStrategy
    ? auth.withAdditionalScopes(requiredScopes)
    : auth;

  client.use(createAuthMiddleware(scopedAuth));
  client.use(createLoggingMiddleware('MY-API'));

  return client;
}
```

This pattern:
1. Keeps scope knowledge in the SDK, not the CLI
2. Allows scope override for special cases via `config.scopes`
3. Works with non-OAuth auth strategies (for testing/mocking)
4. CLI commands just pass the auth strategy through unchanged

---

## SCAPI Tenant ID Utilities

SCAPI APIs use an `organizationId` path parameter with the `f_ecom_` prefix, but OAuth scopes use the raw tenant ID. Use these utilities:

```typescript
// From @salesforce/b2c-tooling-sdk (or clients/custom-apis.ts)
import {toOrganizationId, toTenantId, buildTenantScope} from '@salesforce/b2c-tooling-sdk';

// Convert tenant ID to organization ID (adds f_ecom_ prefix)
toOrganizationId('zzxy_prd')        // Returns 'f_ecom_zzxy_prd'
toOrganizationId('f_ecom_zzxy_prd') // Returns 'f_ecom_zzxy_prd' (unchanged)

// Extract raw tenant ID (strips f_ecom_ prefix)
toTenantId('f_ecom_zzxy_prd')       // Returns 'zzxy_prd'
toTenantId('zzxy_prd')              // Returns 'zzxy_prd' (unchanged)

// Build tenant-specific OAuth scope
buildTenantScope('zzxy_prd')        // Returns 'SALESFORCE_COMMERCE_API:zzxy_prd'
buildTenantScope('f_ecom_zzxy_prd') // Returns 'SALESFORCE_COMMERCE_API:zzxy_prd'
```

### Constants

```typescript
/** Prefix required for SCAPI organizationId path parameter */
export const ORGANIZATION_ID_PREFIX = 'f_ecom_';

/** Prefix for tenant-specific SCAPI OAuth scopes */
export const SCAPI_TENANT_SCOPE_PREFIX = 'SALESFORCE_COMMERCE_API:';
```

---

## OAuthStrategy.withAdditionalScopes()

The `OAuthStrategy` class has a method for scope injection:

```typescript
// Creates a new OAuthStrategy with merged scopes
const scopedAuth = auth.withAdditionalScopes(['sfcc.custom-apis', 'SALESFORCE_COMMERCE_API:zzxy_prd']);
```

Key behaviors:
- Returns a **new** `OAuthStrategy` instance (immutable pattern)
- Merges scopes with deduplication (uses `Set`)
- The new strategy shares token cache with the original (keyed by clientId)
- If cached token doesn't have required scopes, it re-authenticates

---

## Complete SCAPI Client Example

Reference implementation: `packages/b2c-tooling-sdk/src/clients/custom-apis.ts`

```typescript
/*
 * Copyright (c) 2025, Salesforce, Inc.
 * SPDX-License-Identifier: Apache-2
 */
import createClient, {type Client} from 'openapi-fetch';
import type {AuthStrategy} from '../auth/types.js';
import {OAuthStrategy} from '../auth/oauth.js';
import type {paths, components} from './custom-apis.generated.js';
import {createAuthMiddleware, createLoggingMiddleware} from './middleware.js';

export type {paths, components};
export type CustomApisClient = Client<paths>;

/** Default OAuth scopes required for Custom APIs */
export const CUSTOM_APIS_DEFAULT_SCOPES = ['sfcc.custom-apis'];

export interface CustomApisClientConfig {
  shortCode: string;
  tenantId: string;
  scopes?: string[];
}

export function createCustomApisClient(
  config: CustomApisClientConfig,
  auth: AuthStrategy
): CustomApisClient {
  const client = createClient<paths>({
    baseUrl: `https://${config.shortCode}.api.commercecloud.salesforce.com/dx/custom-apis/v1`,
  });

  // Build required scopes: domain scope + tenant-specific scope
  const requiredScopes = config.scopes ?? [
    ...CUSTOM_APIS_DEFAULT_SCOPES,
    buildTenantScope(config.tenantId),
  ];

  // If OAuth strategy, add required scopes; otherwise use as-is
  const scopedAuth = auth instanceof OAuthStrategy
    ? auth.withAdditionalScopes(requiredScopes)
    : auth;

  client.use(createAuthMiddleware(scopedAuth));
  client.use(createLoggingMiddleware('CUSTOM-APIS'));

  return client;
}

// Tenant ID utilities
export const ORGANIZATION_ID_PREFIX = 'f_ecom_';
export const SCAPI_TENANT_SCOPE_PREFIX = 'SALESFORCE_COMMERCE_API:';

export function toOrganizationId(tenantId: string): string {
  return tenantId.startsWith(ORGANIZATION_ID_PREFIX)
    ? tenantId
    : `${ORGANIZATION_ID_PREFIX}${tenantId}`;
}

export function toTenantId(value: string): string {
  return value.startsWith(ORGANIZATION_ID_PREFIX)
    ? value.slice(ORGANIZATION_ID_PREFIX.length)
    : value;
}

export function buildTenantScope(tenantId: string): string {
  return `${SCAPI_TENANT_SCOPE_PREFIX}${toTenantId(tenantId)}`;
}
```

---

## CLI Command Integration

With scope encapsulation in the client, CLI commands become simple:

```typescript
// packages/b2c-cli/src/commands/scapi/custom/status.ts
import {OAuthCommand} from '@salesforce/b2c-tooling-sdk/cli';
import {createCustomApisClient, toOrganizationId} from '@salesforce/b2c-tooling-sdk';

export default class ScapiCustomStatus extends OAuthCommand<typeof ScapiCustomStatus> {
  static flags = {
    ...OAuthCommand.baseFlags,
    'tenant-id': Flags.string({
      description: 'Organization/tenant ID',
      env: 'SFCC_TENANT_ID',
      required: true,
    }),
  };

  async run() {
    this.requireOAuthCredentials();

    const {'tenant-id': tenantId} = this.flags;
    const {shortCode} = this.resolvedConfig;

    // Auth strategy from base class - no scope configuration needed!
    const oauthStrategy = this.getOAuthStrategy();

    // Client handles scope injection internally
    const client = createCustomApisClient({shortCode, tenantId}, oauthStrategy);

    const {data, error} = await client.GET('/organizations/{organizationId}/endpoints', {
      params: {
        path: {organizationId: toOrganizationId(tenantId)},
      },
    });

    // Handle response...
  }
}
```

---

## Testing API Clients

Use MSW (Mock Service Worker) to mock API responses:

```typescript
import {http, HttpResponse} from 'msw';
import {setupServer} from 'msw/node';
import {createCustomApisClient} from '@salesforce/b2c-tooling-sdk';

const mockAuth: AuthStrategy = {
  async fetch(url, init) {
    return fetch(url, init);
  },
  async getAuthorizationHeader() {
    return 'Bearer mock-token';
  },
};

const server = setupServer(
  http.get('https://test.api.commercecloud.salesforce.com/dx/custom-apis/v1/organizations/*/endpoints', () => {
    return HttpResponse.json({
      data: [{apiName: 'test', status: 'active'}],
      total: 1,
      limit: 10,
    });
  })
);

beforeAll(() => server.listen());
afterAll(() => server.close());

it('fetches endpoints', async () => {
  const client = createCustomApisClient(
    {shortCode: 'test', tenantId: 'zzxy_prd'},
    mockAuth
  );

  const {data} = await client.GET('/organizations/{organizationId}/endpoints', {
    params: {path: {organizationId: 'f_ecom_zzxy_prd'}},
  });

  expect(data?.data).toHaveLength(1);
});
```

---

## Checklist: New SCAPI Client

1. Add OpenAPI spec to `specs/`
2. Update `generate:types` script in `package.json`
3. Run `pnpm --filter @salesforce/b2c-tooling-sdk run generate:types`
4. Create client module with:
   - Config interface including `tenantId`
   - Default scopes constant
   - Factory function with scope injection pattern
   - Tenant ID utilities (or import from existing)
5. Export from `src/clients/index.ts`
6. Add to main `src/index.ts` if needed
7. Write tests with MSW mocks
8. Build: `pnpm --filter @salesforce/b2c-tooling-sdk run build`
9. Test: `pnpm --filter @salesforce/b2c-tooling-sdk run test`
