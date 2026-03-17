---
name: integration-development
description: Guide for creating new OAuth-based integrations in the Orient codebase. Use when adding external service integrations (APIs like Linear, GitHub, Slack, Notion, etc.), implementing OAuth flows, or creating catalog-based integration manifests. Covers the full integration lifecycle from manifest definition to tool implementation.
---

# Integration Development

This skill provides guidance for creating OAuth-based integrations in Orient.

## Integration Architecture

Orient uses a **catalog-based architecture** for integrations:

```
packages/integrations/src/
├── catalog/                    # Integration definitions
│   ├── linear/
│   │   ├── INTEGRATION.yaml    # Manifest
│   │   ├── oauth-config.ts     # OAuth configuration
│   │   ├── tools.ts            # API client and tools
│   │   └── index.ts            # Exports
│   └── github/
│       └── ...
├── types/
│   └── integration.ts          # IntegrationManifest types
└── index.ts                    # Package exports
```

## Quick Start

1. Create directory: `packages/integrations/src/catalog/<integration-name>/`
2. Create `INTEGRATION.yaml` manifest
3. Create `oauth-config.ts` for OAuth flow
4. Create `tools.ts` for API client
5. Create `index.ts` for exports
6. Update package.json exports

## File Templates

### INTEGRATION.yaml

See `references/manifest-template.md` for the complete template.

Key fields:

- `name`: lowercase identifier (e.g., `linear`, `github`)
- `title`: display name
- `description`: 50+ character description
- `version`: semver (e.g., `1.0.0`)
- `oauth`: authorization and token URLs, scopes
- `requiredSecrets`: CLIENT_ID, CLIENT_SECRET, etc.
- `tools`: available API operations
- `status`: `stable`, `beta`, or `experimental`

### oauth-config.ts

Required exports:

- Scope constants (e.g., `LINEAR_SCOPES`)
- Default scopes array
- Config interface
- `getAuthUrl()` - generate authorization URL
- `exchangeCode()` - exchange code for tokens
- `getUserInfo()` - fetch user profile
- `getConfigFromEnv()` - load config from environment

### tools.ts

Required exports:

- Type definitions for API responses
- Client class with API methods
- Factory function (e.g., `createLinearClient()`)

## OAuth Flow Patterns

### Standard OAuth 2.0

Most services use standard OAuth 2.0:

```typescript
// 1. Generate auth URL with state
const authUrl = getAuthUrl(config, scopes, state);

// 2. User authorizes in browser, redirected with code

// 3. Exchange code for tokens
const tokens = await exchangeCode(config, code);

// 4. Use access token for API calls
const client = createClient(tokens.accessToken);
```

### OAuth 2.0 with PKCE

Some services require PKCE (Proof Key for Code Exchange):

```typescript
// 1. Generate code verifier and challenge
const codeVerifier = crypto.randomBytes(32).toString('base64url');
const codeChallenge = crypto.createHash('sha256').update(codeVerifier).digest('base64url');

// 2. Include challenge in auth URL
const authUrl = `${baseUrl}?code_challenge=${codeChallenge}&code_challenge_method=S256`;

// 3. Include verifier in token exchange
const tokens = await exchangeCode(config, code, codeVerifier);
```

## API Client Patterns

### GraphQL APIs (Linear, GitHub GraphQL)

```typescript
private async query<T>(query: string, variables?: Record<string, unknown>): Promise<T> {
  const response = await fetch(this.apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${this.accessToken}`,
    },
    body: JSON.stringify({ query, variables }),
  });

  const result = await response.json();
  if (result.errors?.length > 0) {
    throw new Error(`GraphQL error: ${result.errors[0].message}`);
  }
  return result.data;
}
```

### REST APIs (GitHub REST, Slack)

```typescript
private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${this.apiUrl}${endpoint}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${this.accessToken}`,
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: response.statusText }));
    throw new Error(`API error: ${error.message}`);
  }

  return response.json();
}
```

## Logging Pattern

Always use the service logger:

```typescript
import { createServiceLogger } from '@orientbot/core';

const logger = createServiceLogger('integration-name');

async function someOperation() {
  const op = logger.startOperation('operationName', { param1: value1 });

  try {
    const result = await doWork();
    op.success('Operation completed', { resultCount: result.length });
    return result;
  } catch (error) {
    op.failure(error instanceof Error ? error : String(error));
    throw error;
  }
}
```

## Type Transformation

Transform API responses to camelCase:

```typescript
// API returns snake_case
const apiResponse = {
  created_at: '2024-01-15',
  pull_request: { html_url: '...' },
};

// Transform to camelCase
const result = {
  createdAt: apiResponse.created_at,
  pullRequest: { htmlUrl: apiResponse.pull_request.html_url },
};
```

## Required Secrets

Define all required secrets in the manifest:

```yaml
requiredSecrets:
  - name: SERVICE_CLIENT_ID
    description: OAuth Client ID from developer settings
    category: oauth
    required: true
  - name: SERVICE_CLIENT_SECRET
    description: OAuth Client Secret
    category: oauth
    required: true
  - name: SERVICE_WEBHOOK_SECRET
    description: Webhook signing secret (optional)
    category: webhook
    required: false
```

## Webhook Support

For integrations that support webhooks:

```yaml
webhooks:
  events:
    - push
    - pull_request
    - issues
  signatureHeader: X-Hub-Signature-256
  signatureAlgorithm: hmac-sha256
```

## Testing Integrations

1. **OAuth flow**: Test with real credentials in development
2. **API calls**: Mock API responses in unit tests
3. **Token refresh**: Test expiration handling
4. **Error handling**: Test API error responses

## Common Pitfalls

1. **Missing scopes**: Always request all needed scopes upfront
2. **Token expiration**: Handle refresh tokens if provided
3. **Rate limiting**: Implement backoff for API errors
4. **Pagination**: Handle paginated API responses
5. **Error messages**: Parse API error details for useful messages

## References

- `references/manifest-template.md` - Full INTEGRATION.yaml template
- `references/oauth-providers.md` - OAuth configuration for common providers
