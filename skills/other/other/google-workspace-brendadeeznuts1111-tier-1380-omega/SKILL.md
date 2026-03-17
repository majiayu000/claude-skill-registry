---
name: google-workspace
description: |
  Build integrations with Google Workspace APIs (Gmail, Calendar, Drive, Sheets, Docs, Chat, Meet, Forms, Tasks, Admin SDK). Covers OAuth 2.0, service accounts, rate limits, batch operations, and Cloudflare Workers patterns.

  Use when building MCP servers, automation tools, or integrations with any Google Workspace API, or troubleshooting OAuth errors, rate limit 429 errors, scope issues, or API-specific gotchas.
user-invocable: true
---

# Google Workspace APIs

**Status**: Production Ready
**Last Updated**: 2026-01-09
**Dependencies**: Cloudflare Workers (recommended), Google Cloud Project
**Skill Version**: 1.0.0

---

## Quick Reference

| API | Common Use Cases | Reference |
|-----|------------------|-----------|
| Gmail | Email automation, inbox management | [gmail-api.md](references/gmail-api.md) |
| Calendar | Event management, scheduling | [calendar-api.md](references/calendar-api.md) |
| Drive | File storage, sharing | [drive-api.md](references/drive-api.md) |
| Sheets | Spreadsheet data, reporting | [sheets-api.md](references/sheets-api.md) |
| Docs | Document generation | [docs-api.md](references/docs-api.md) |
| Chat | Bots, webhooks, spaces | [chat-api.md](references/chat-api.md) |
| Meet | Video conferencing | [meet-api.md](references/meet-api.md) |
| Forms | Form responses, creation | [forms-api.md](references/forms-api.md) |
| Tasks | Task management | [tasks-api.md](references/tasks-api.md) |
| Admin SDK | User/group management | [admin-sdk.md](references/admin-sdk.md) |
| People | Contacts management | [people-api.md](references/people-api.md) |

---

## Shared Authentication Patterns

All Google Workspace APIs use the same authentication mechanisms. Choose based on your use case.

### Option 1: OAuth 2.0 (User Context)

Best for: Acting on behalf of a user, accessing user-specific data.

```typescript
// Authorization URL
const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth')
authUrl.searchParams.set('client_id', env.GOOGLE_CLIENT_ID)
authUrl.searchParams.set('redirect_uri', `${env.BASE_URL}/callback`)
authUrl.searchParams.set('response_type', 'code')
authUrl.searchParams.set('scope', SCOPES.join(' '))
authUrl.searchParams.set('access_type', 'offline')  // For refresh tokens
authUrl.searchParams.set('prompt', 'consent')       // Force consent for refresh token

// Token exchange
async function exchangeCode(code: string): Promise<TokenResponse> {
  const response = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      code,
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      redirect_uri: `${env.BASE_URL}/callback`,
      grant_type: 'authorization_code',
    }),
  })
  return response.json()
}

// Refresh token
async function refreshToken(refresh_token: string): Promise<TokenResponse> {
  const response = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      refresh_token,
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      grant_type: 'refresh_token',
    }),
  })
  return response.json()
}
```

**Critical:**
- Always request `access_type=offline` for refresh tokens
- Use `prompt=consent` to ensure refresh token is returned
- Store refresh tokens securely (Cloudflare KV or D1)
- Access tokens expire in ~1 hour

### Option 2: Service Account (Server-to-Server)

Best for: Backend automation, no user interaction, domain-wide delegation.

```typescript
import { SignJWT } from 'jose'

async function getServiceAccountToken(
  serviceAccount: ServiceAccountKey,
  scopes: string[]
): Promise<string> {
  const now = Math.floor(Date.now() / 1000)

  // Create JWT
  const jwt = await new SignJWT({
    iss: serviceAccount.client_email,
    scope: scopes.join(' '),
    aud: 'https://oauth2.googleapis.com/token',
    iat: now,
    exp: now + 3600,
  })
    .setProtectedHeader({ alg: 'RS256', typ: 'JWT' })
    .sign(await importPKCS8(serviceAccount.private_key, 'RS256'))

  // Exchange JWT for access token
  const response = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
      assertion: jwt,
    }),
  })

  const data = await response.json()
  return data.access_token
}
```

**Domain-Wide Delegation** (impersonate users):
```typescript
const jwt = await new SignJWT({
  iss: serviceAccount.client_email,
  sub: 'user@domain.com',  // User to impersonate
  scope: scopes.join(' '),
  aud: 'https://oauth2.googleapis.com/token',
  iat: now,
  exp: now + 3600,
})
```

**Setup Required:**
1. Create service account in Google Cloud Console
2. Download JSON key file
3. Enable domain-wide delegation in Admin Console (if impersonating)
4. Store key as Cloudflare secret (JSON stringified)

---

## Common Rate Limits

All Google Workspace APIs enforce quotas. These are approximate - check each API's specific limits.

### Per-User Limits (OAuth)

| API | Reads | Writes | Notes |
|-----|-------|--------|-------|
| Gmail | 250/user/sec | 250/user/sec | Aggregate across all methods |
| Calendar | 500/user/100sec | 500/user/100sec | Per calendar |
| Drive | 1000/user/100sec | 1000/user/100sec | |
| Sheets | 100/user/100sec | 100/user/100sec | Lower than others |

### Per-Project Limits

| API | Daily Quota | Per-Minute | Notes |
|-----|-------------|------------|-------|
| Gmail | 1B units | Varies | Unit-based (send = 100 units) |
| Calendar | 1M queries | 500/sec | |
| Drive | 1B queries | 1000/sec | |
| Sheets | Unlimited | 500/user/100sec | |

### Handling Rate Limits

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 5
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error: any) {
      const status = error.status || error.code

      if (status === 429 || status === 503) {
        // Rate limited or service unavailable
        const retryAfter = error.headers?.get('Retry-After') || Math.pow(2, i)
        await new Promise(r => setTimeout(r, retryAfter * 1000))
        continue
      }

      if (status === 403 && error.message?.includes('rateLimitExceeded')) {
        // Quota exceeded - exponential backoff
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000))
        continue
      }

      throw error
    }
  }
  throw new Error('Max retries exceeded')
}
```

---

## Batch Requests

Most Google APIs support batching multiple requests into one HTTP call.

```typescript
async function batchRequest(
  accessToken: string,
  requests: BatchRequestItem[]
): Promise<BatchResponse[]> {
  const boundary = 'batch_boundary'

  let body = ''
  requests.forEach((req, i) => {
    body += `--${boundary}\r\n`
    body += 'Content-Type: application/http\r\n'
    body += `Content-ID: <item${i}>\r\n\r\n`
    body += `${req.method} ${req.path} HTTP/1.1\r\n`
    body += 'Content-Type: application/json\r\n\r\n'
    if (req.body) body += JSON.stringify(req.body)
    body += '\r\n'
  })
  body += `--${boundary}--`

  const response = await fetch('https://www.googleapis.com/batch/v1', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': `multipart/mixed; boundary=${boundary}`,
    },
    body,
  })

  // Parse multipart response...
  return parseBatchResponse(await response.text())
}
```

**Limits:**
- Max 100 requests per batch (most APIs)
- Max 1000 requests per batch (some APIs like Drive)
- Each request in batch counts toward quota

---

## Cloudflare Workers Configuration

```jsonc
// wrangler.jsonc
{
  "name": "google-workspace-mcp",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-03",
  "compatibility_flags": ["nodejs_compat"],

  // Store OAuth tokens
  "kv_namespaces": [
    { "binding": "TOKENS", "id": "xxx" }
  ],

  // Or use D1 for structured storage
  "d1_databases": [
    { "binding": "DB", "database_name": "workspace-mcp", "database_id": "xxx" }
  ]
}
```

**Secrets to set:**
```bash
echo "your-client-id" | npx wrangler secret put GOOGLE_CLIENT_ID
echo "your-client-secret" | npx wrangler secret put GOOGLE_CLIENT_SECRET
# For service accounts:
cat service-account.json | npx wrangler secret put GOOGLE_SERVICE_ACCOUNT
```

---

## Common Errors

### Error: "invalid_grant" on Token Refresh
**Cause**: Refresh token revoked or expired (6 months of inactivity)
**Fix**: Re-authenticate user, request new refresh token

### Error: "access_denied" on OAuth
**Cause**: App not verified, or user not in test users list
**Fix**: Add user to OAuth consent screen test users, or complete app verification

### Error: "insufficientPermissions" (403)
**Cause**: Missing required scope
**Fix**: Check scopes in authorization URL, re-authenticate with correct scopes

### Error: "rateLimitExceeded" (403)
**Cause**: Quota exceeded
**Fix**: Implement exponential backoff, reduce request frequency, request quota increase

### Error: "notFound" (404) on Known Resource
**Cause**: Using wrong API version, or resource in trash
**Fix**: Check API version in URL, check trash for deleted items

---

## API-Specific Guides

Detailed patterns for each API are in the `references/` directory. Load these when working with specific APIs.

### Gmail API
See [references/gmail-api.md](references/gmail-api.md)
- Message CRUD, labels, threads
- MIME handling, attachments
- Push notifications (Pub/Sub)

### Calendar API
See [references/calendar-api.md](references/calendar-api.md)
- Events CRUD, recurring events
- Free/busy queries
- Calendar sharing

### Drive API
See [references/drive-api.md](references/drive-api.md)
- File upload/download
- Permissions, sharing
- Search queries

### Sheets API
See [references/sheets-api.md](references/sheets-api.md)
- Reading/writing cells
- A1 notation, ranges
- Batch updates

### Chat API
See [references/chat-api.md](references/chat-api.md)
- Bots, webhooks
- Cards v2, interactive forms
- Spaces, members, reactions

*(Additional API references added as MCP servers are built)*

---

## Package Versions (Verified 2026-01-09)

```json
{
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20260109.0",
    "wrangler": "^4.58.0",
    "jose": "^6.1.3"
  }
}
```

---

## Official Documentation

- **Google Workspace APIs**: https://developers.google.com/workspace
- **OAuth 2.0**: https://developers.google.com/identity/protocols/oauth2
- **Service Accounts**: https://cloud.google.com/iam/docs/service-accounts
- **API Explorer**: https://developers.google.com/apis-explorer
- **Quotas Dashboard**: https://console.cloud.google.com/iam-admin/quotas

---

## Skill Roadmap

APIs documented as MCP servers are built:

- [ ] Gmail API
- [ ] Calendar API
- [ ] Drive API
- [ ] Sheets API
- [ ] Docs API
- [x] Chat API (migrated from google-chat-api skill)
- [ ] Meet API
- [ ] Forms API
- [ ] Tasks API
- [ ] Admin SDK
- [ ] People API
