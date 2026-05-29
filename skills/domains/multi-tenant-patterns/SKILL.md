# Multi-Tenant Patterns Skill

> Header-based multi-tenant authentication patterns.

---

## Request Headers

```
x-n8n-url: https://n8n.example.com
x-n8n-key: n8n_api_key_here
x-instance-id: optional-instance-id
x-session-id: optional-session-id
```

## Auth Flow

```
1. Request arrives with headers
2. Extract n8n credentials from headers
3. Validate credentials against n8n instance
4. Create or resume session
5. Execute MCP tool with tenant context
6. Return response
```

## Session Management

```typescript
interface Session {
  id: string;
  n8nUrl: string;
  n8nApiKey: string;
  instanceId?: string;
  createdAt: Date;
  lastUsedAt: Date;
}
```

## Rate Limiting Per Tenant

```typescript
const key = `rate:${apiKey}:${hour}`;
const count = await kv.get(key) || 0;
if (count >= limit) {
  throw new RateLimitError();
}
await kv.put(key, count + 1, { expirationTtl: 3600 });
```
