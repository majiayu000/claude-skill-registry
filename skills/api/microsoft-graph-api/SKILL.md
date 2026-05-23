---
name: "microsoft-graph-api"
description: "Comprehensive Microsoft Graph API reference for M365 service integration"
---

# Microsoft Graph API Skill

Comprehensive reference for Microsoft Graph API integration including endpoints, authentication, rate limiting, and best practices.

## ⚠️ Staleness Warning

Microsoft Graph APIs evolve frequently. Permissions, endpoints, and authentication flows may change.

**Refresh triggers:**
- Microsoft Graph API version updates
- MSAL library major releases
- Azure AD → Microsoft Entra ID migration
- New Graph scopes or permissions

**Last validated:** February 2026 (Graph v1.0, MSAL 2.x)

**Check current state:** [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer), [Graph API Reference](https://learn.microsoft.com/graph/api/overview)

---

## API Quick Reference

### Base URLs

| Environment | URL |
|-------------|-----|
| **Production (v1.0)** | `https://graph.microsoft.com/v1.0` |
| **Beta** | `https://graph.microsoft.com/beta` |
| **China (21Vianet)** | `https://microsoftgraph.chinacloudapi.cn/v1.0` |

> **Best Practice**: Use v1.0 for production. Beta endpoints can change without notice.

### Authentication

| Method | Header | Use Case |
|--------|--------|----------|
| **Delegated (user)** | `Authorization: Bearer {token}` | Interactive apps — acts on behalf of signed-in user |
| **Application** | `Authorization: Bearer {token}` | Background services — acts as the app itself |

**Token Acquisition (VS Code Extension)**:
```typescript
// Progressive scope acquisition — request minimal scopes initially
const INITIAL_SCOPES = ['User.Read'];
const FULL_SCOPES = [
    'User.Read',
    'Calendars.Read',
    'Mail.Read',
    'Presence.Read',
    'People.Read',
    'Group.Read.All'
];

async function getGraphToken(): Promise<string | null> {
    const session = await vscode.authentication.getSession(
        'microsoft',
        FULL_SCOPES,
        { createIfNone: false }
    );
    return session?.accessToken ?? null;
}
```

---

## Permissions (Scopes) Reference

### Common Delegated Scopes

| Scope | Purpose |
|-------|---------|
| `User.Read` | Read signed-in user profile |
| `User.ReadBasic.All` | Read basic profile of all users |
| `Mail.Read` | Read user mail |
| `Mail.Send` | Send mail as the user |
| `Calendars.Read` | Read user calendar events |
| `Calendars.ReadWrite` | Create/update calendar events |
| `Presence.Read` | Read user presence status |
| `People.Read` | Read user's relevant people |
| `Group.Read.All` | Read all groups |
| `Sites.Read.All` | Read SharePoint sites |
| `Files.Read.All` | Read all files user can access |
| `Tasks.Read` | Read user's tasks (To Do) |
| `Tasks.ReadWrite` | Create/update tasks (Planner/To Do) |

### Common Application Scopes

| Scope | Purpose |
|-------|---------|
| `User.Read.All` | Read all user profiles (app-only) |
| `Group.Read.All` | Read all groups (app-only) |
| `Mail.Read` | Read all users' mail (requires admin consent) |
| `AuditLog.Read.All` | Read audit logs |
| `Reports.Read.All` | Read M365 usage reports |
| `ServiceHealth.Read.All` | Read M365 service health |

> **Principle of Least Privilege**: Request only the scopes your app actually needs. Start with `User.Read` and add incrementally.

---

## Key Endpoints by Service

### Users

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get current user | GET | `/me` |
| Get user by ID/UPN | GET | `/users/{id-or-upn}` |
| List users | GET | `/users` |
| Get user photo | GET | `/me/photo/$value` |
| Get manager | GET | `/me/manager` |
| Get direct reports | GET | `/me/directReports` |

### Mail

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List messages | GET | `/me/messages` |
| Get message | GET | `/me/messages/{message-id}` |
| Send mail | POST | `/me/sendMail` |
| List mail folders | GET | `/me/mailFolders` |

### Calendar

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List events | GET | `/me/calendar/events` |
| Calendar view | GET | `/me/calendarView?startDateTime={start}&endDateTime={end}` |
| Create event | POST | `/me/calendar/events` |
| Get event | GET | `/me/events/{event-id}` |

### Presence

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Get my presence | GET | `/me/presence` |
| Get user presence | GET | `/users/{id}/presence` |
| Get presence for multiple | POST | `/communications/getPresencesByUserId` |

### People & Insights

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List relevant people | GET | `/me/people` |
| Get trending docs | GET | `/me/insights/trending` |
| Get used docs | GET | `/me/insights/used` |
| Get shared docs | GET | `/me/insights/shared` |

### SharePoint & OneDrive

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List sites | GET | `/sites` |
| Get site by path | GET | `/sites/{hostname}:/{server-relative-path}` |
| List drives | GET | `/me/drives` |
| List drive items | GET | `/me/drive/root/children` |
| Search files | GET | `/me/drive/root/search(q='{query}')` |
| Upload file | PUT | `/me/drive/items/{parent-id}:/{filename}:/content` |

### Planner (Task Management)

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List plans for group | GET | `/groups/{group-id}/planner/plans` |
| List tasks in plan | GET | `/planner/plans/{plan-id}/tasks` |
| Create task | POST | `/planner/tasks` |
| Update task | PATCH | `/planner/tasks/{task-id}` |
| Get user tasks | GET | `/me/planner/tasks` |

> **Note**: Planner only supports **delegated** permissions. Application permissions are not available.

### To Do

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List task lists | GET | `/me/todo/lists` |
| Create task list | POST | `/me/todo/lists` |
| List tasks | GET | `/me/todo/lists/{list-id}/tasks` |
| Create task | POST | `/me/todo/lists/{list-id}/tasks` |
| Update task | PATCH | `/me/todo/lists/{list-id}/tasks/{task-id}` |

### Groups & Teams

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List groups | GET | `/groups` |
| Get group | GET | `/groups/{group-id}` |
| List group members | GET | `/groups/{group-id}/members` |
| List joined teams | GET | `/me/joinedTeams` |
| Get team channels | GET | `/teams/{team-id}/channels` |
| Post channel message | POST | `/teams/{team-id}/channels/{channel-id}/messages` |

### Service Health & Communications (FishbowlGovernance pattern)

| Operation | Method | Endpoint | Scope |
|-----------|--------|----------|-------|
| List health overviews | GET | `/admin/serviceAnnouncement/healthOverviews` | ServiceHealth.Read.All |
| List active issues | GET | `/admin/serviceAnnouncement/issues` | ServiceHealth.Read.All |
| Get issue detail | GET | `/admin/serviceAnnouncement/issues/{id}` | ServiceHealth.Read.All |
| List message center | GET | `/admin/serviceAnnouncement/messages` | ServiceMessage.Read.All |

**Rate limit**: 1,500 requests / 10 minutes

### Audit Logs (FishbowlGovernance pattern)

| Operation | Method | Endpoint | Scope |
|-----------|--------|----------|-------|
| List directory audits | GET | `/auditLogs/directoryAudits` | AuditLog.Read.All |
| List sign-in logs | GET | `/auditLogs/signIns` | AuditLog.Read.All |
| List provisioning logs | GET | `/auditLogs/provisioning` | AuditLog.Read.All |

**Rate limit**: Security endpoints = 150 requests / 10 minutes

### Sensitivity Labels (Information Protection)

| Operation | Method | Endpoint | Scope |
|-----------|--------|----------|-------|
| List labels | GET | `/informationProtection/policy/labels` | InformationProtectionPolicy.Read |
| Evaluate classification | POST | `/informationProtection/policy/labels/evaluateClassificationResults` | InformationProtectionPolicy.Read |
| Extract label | POST | `/informationProtection/policy/labels/extractLabel` | InformationProtectionPolicy.Read |

---

## Critical Patterns

### Custom Error Types

```typescript
export class GraphRateLimitError extends Error {
  public readonly retryAfter: number;

  constructor(retryAfter: number, message = '') {
    super(`Rate limited. Retry after ${retryAfter}s. ${message}`);
    this.name = 'GraphRateLimitError';
    this.retryAfter = retryAfter;
  }
}

export class GraphApiError extends Error {
  public readonly statusCode: number;
  public readonly errorCode: string;

  constructor(statusCode: number, errorCode: string, message: string) {
    super(`Graph API ${statusCode} (${errorCode}): ${message}`);
    this.name = 'GraphApiError';
    this.statusCode = statusCode;
    this.errorCode = errorCode;
  }
}
```

### API Client Pattern (with retry + timeout)

```typescript
const GRAPH_ENDPOINT = 'https://graph.microsoft.com/v1.0';
const DEFAULT_TIMEOUT_MS = 30000;
const DEFAULT_MAX_RETRIES = 3;

async function graphRequest<T>(
  method: 'GET' | 'POST' | 'PATCH' | 'DELETE',
  endpoint: string,
  options: RequestInit = {},
  config: { timeoutMs?: number; maxRetries?: number; throwOnError?: boolean } = {}
): Promise<T | null> {
    const token = await getGraphToken();
    if (!token) return null;

    const { timeoutMs = DEFAULT_TIMEOUT_MS, maxRetries = DEFAULT_MAX_RETRIES, throwOnError = false } = config;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
            const response = await fetch(`${GRAPH_ENDPOINT}${endpoint}`, {
                method,
                ...options,
                signal: controller.signal,
                headers: { 'Authorization': `Bearer ${token}`, ...options.headers }
            });
            clearTimeout(timeoutId);

            // Handle 429 rate limiting
            if (response.status === 429) {
                const retryAfter = parseInt(response.headers.get('Retry-After') || '10');
                if (attempt < maxRetries) {
                    await new Promise(r => setTimeout(r, retryAfter * 1000));
                    continue;
                }
                if (throwOnError) throw new GraphRateLimitError(retryAfter);
                return null;
            }

            // Handle 5xx with exponential backoff
            if (response.status >= 500 && attempt < maxRetries) {
                await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
                continue;
            }

            if (!response.ok) {
                if (throwOnError) {
                    const err = await response.json().catch(() => ({}));
                    throw new GraphApiError(response.status, err?.error?.code || 'Unknown', err?.error?.message || response.statusText);
                }
                return null;
            }

            return response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            if (error instanceof Error && error.name === 'AbortError' && attempt < maxRetries) {
                await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
                continue;
            }
            throw error;
        }
    }
    return null;
}
```

### OData Query Parameters

Graph supports standard OData query parameters:

| Parameter | Example | Purpose |
|-----------|---------|---------|
| `$select` | `?$select=id,displayName,mail` | Return only specified properties |
| `$filter` | `?$filter=department eq 'Engineering'` | Filter results server-side |
| `$orderby` | `?$orderby=displayName` | Sort results |
| `$top` | `?$top=10` | Limit result count |
| `$skip` | `?$skip=20` | Skip N results (not all APIs) |
| `$expand` | `?$expand=manager` | Include related resources inline |
| `$count` | `?$count=true` | Include total count in response |
| `$search` | `?$search="displayName:Fabio"` | Full-text search |

**Combining parameters**:
```http
GET /users?$select=id,displayName,department&$filter=department eq 'Analytics'&$top=25&$orderby=displayName
```

> **Not all endpoints support all parameters.** Check specific endpoint docs.

### Pagination

Graph uses `@odata.nextLink` for pagination:

```typescript
async function graphFetchAll<T>(path: string): Promise<T[]> {
    const token = await getGraphToken();
    if (!token) return [];
    
    const results: T[] = [];
    let url: string | null = `${GRAPH_ENDPOINT}${path}`;

    while (url) {
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        results.push(...(data.value || []));
        url = data['@odata.nextLink'] || null;
    }

    return results;
}
```

### JSON Batching

Combine up to **20 requests** in a single HTTP call:

```typescript
interface BatchRequest {
    id: string;
    method: 'GET' | 'POST' | 'PATCH' | 'DELETE';
    url: string;
    body?: unknown;
}

async function graphBatch<T>(requests: BatchRequest[]): Promise<Map<string, T>> {
    if (requests.length > 20) {
        console.warn('Batch limit is 20, use graphBatchAll() for unlimited');
        requests = requests.slice(0, 20);
    }

    const response = await graphPost<{ responses: Array<{ id: string; status: number; body: T }> }>(
        '/$batch',
        { requests }
    );

    const results = new Map<string, T>();
    for (const resp of response?.responses || []) {
        if (resp.status >= 200 && resp.status < 300) {
            results.set(resp.id, resp.body);
        }
    }
    return results;
}

// Auto-chunk unlimited requests into batches of 20
async function graphBatchAll<T>(requests: BatchRequest[]): Promise<Map<string, T>> {
    const allResults = new Map<string, T>();
    for (let i = 0; i < requests.length; i += 20) {
        const chunk = requests.slice(i, i + 20);
        const chunkResults = await graphBatch<T>(chunk);
        for (const [id, body] of chunkResults) {
            allResults.set(id, body);
        }
    }
    return allResults;
}
```

### Helper: Build Batch Request

```typescript
function buildBatchRequest(
    method: 'GET' | 'POST' | 'PATCH' | 'DELETE',
    url: string,
    body?: unknown,
    requestId?: string
): BatchRequest {
    return {
        id: requestId || Math.random().toString(36).substring(2, 10),
        method,
        url,
        body,
    };
}
```

---

## Rate Limits & Throttling

### Service-Specific Limits

| Service | Per App per Tenant | Notes |
|---------|-------------------|-------|
| **Outlook (Mail/Calendar)** | 10,000 requests / 10 min | Standard throttling |
| **Teams** | Varies by endpoint | Channel messages more restrictive |
| **SharePoint/OneDrive** | Based on concurrent calls | Use batching |
| **Directory (Users/Groups)** | 10,000 requests / 10 min | Standard throttling |
| **Service Health** | 1,500 requests / 10 min | Lower limit - cache results |
| **Security (Alerts/Incidents)** | 150 requests / 10 min | Much lower - batch carefully |
| **Audit Logs** | 1,000 requests / 10 min | Lower limit - paginate wisely |

### Throttled Response

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
```

### Best Practices for Avoiding Throttling

1. Use `$select` to request only needed properties
2. Use `$filter` server-side instead of fetching all and filtering locally
3. Use JSON batching to reduce request count
4. Implement exponential backoff with jitter
5. Cache responses where data doesn't change frequently

---

## Token Lifetime

| Token | Default Lifetime |
|-------|-----------------|
| Access token | 60-90 minutes |
| Refresh token | Up to 90 days |
| ID token | 60 minutes |

> **Always use MSAL** rather than raw OAuth. MSAL handles caching, refresh, and retry automatically.

---

## SDKs & Client Libraries

| Language | Package | Notes |
|----------|---------|-------|
| **TypeScript/JS** | `@microsoft/microsoft-graph-client` | Official SDK |
| **Python** | `msgraph-sdk-python` | Official SDK |
| **PowerShell** | `Microsoft.Graph` | `Install-Module Microsoft.Graph` |
| **.NET** | `Microsoft.Graph` | NuGet package |

---

## Alex-Specific Integration Points

| Feature | Endpoint | Alex Usage |
|---------|----------|------------|
| Calendar context | `/me/calendarView` | Meeting prep, scheduling awareness |
| Email context | `/me/messages` | Communication context |
| **Send email** | `/me/sendMail` | Proactive notifications, weekly reports |
| Presence | `/me/presence` | Availability in status |
| People | `/me/people` | Org context, relevant contacts |
| OneDrive | `/me/drive` | Knowledge file sync |
| **OneDrive upload** | `/me/drive/root:/{path}:/content` | File archival, exports |
| **Service Health** | `/admin/serviceAnnouncement/healthOverviews` | Alex-aware service status |
| **Service Issues** | `/admin/serviceAnnouncement/issues` | Proactive troubleshooting |
| **Sensitivity Labels** | `/me/informationProtection/sensitivityLabels` | Document classification |

---

## Synapses

```
→ [enterprise-integration skill] AUTH_PATTERNS_AND_SCOPES (strong, bidirectional)
→ [vscode-extension-patterns skill] VSCODE_AUTH_SESSION_API (strong, outbound)
→ [alex-core] ENTERPRISE_MODE_GATING (strong, inbound)
→ [localization skill] USER_PREFERRED_LANGUAGE_FROM_GRAPH (moderate, outbound)
→ [GI-heir-promotion-pattern-graph-api-2026-02-12] PROMOTION_CASE_STUDY (strong, origin)
→ [FishbowlGovernance DK-MICROSOFT-GRAPH.md] HEIR_SOURCE_KNOWLEDGE (strong, inbound)
→ [error-handling-patterns] CUSTOM_ERROR_TYPES (moderate, outbound)
→ [api-design patterns] BATCH_AUTO_CHUNKING_PATTERN (strong, outbound)
```

### Session 2026-02-12: Heir Promotion
- Promoted from FishbowlGovernance heir's production Graph integration
- Added: Service Health, Email, OneDrive modules
- Added: graphBatchAll() auto-chunking pattern
- Blocker discovered: Admin consent required for Microsoft tenants

---

## References

- [Microsoft Graph Overview](https://learn.microsoft.com/graph/overview)
- [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- [Graph API Reference (v1.0)](https://learn.microsoft.com/graph/api/overview?view=graph-rest-1.0)
- [Permissions Reference](https://learn.microsoft.com/graph/permissions-reference)
- [Graph API Throttling](https://learn.microsoft.com/graph/throttling)
- [MSAL Overview](https://learn.microsoft.com/entra/msal/overview)
- [JSON Batching](https://learn.microsoft.com/graph/json-batching)
