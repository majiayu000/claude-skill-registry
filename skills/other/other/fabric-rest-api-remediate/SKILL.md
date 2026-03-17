---
name: fabric-rest-api-remediate
description: Diagnose and resolve Microsoft Fabric REST API errors including HTTP 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Throttling, and 5xx server errors. Use when debugging Fabric API authentication failures, Entra ID token issues, insufficient scopes, throttling/rate limiting, long running operation (LRO) polling failures, pagination problems, service principal configuration, or capacity API errors. Covers PowerShell and C# remediate workflows against api.fabric.microsoft.com.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric REST API remediate

Structured diagnostic workflows for identifying and resolving errors when calling Microsoft Fabric REST APIs (`https://api.fabric.microsoft.com/v1/`).

## When to Use This Skill

- Fabric REST API returns an HTTP error (401, 403, 404, 429, 5xx)
- Authentication or token acquisition fails with MSAL
- Service principal or managed identity calls are rejected
- API calls are being throttled (HTTP 429)
- Long running operations (LRO) fail or time out during polling
- Pagination with `continuationToken` stops working or returns incomplete results
- Capacity API operations fail (create, update, resume, suspend)
- Need to implement retry logic with exponential backoff for Fabric APIs
- Debugging `errorCode` values in Fabric API error responses

## Prerequisites

- Microsoft Entra ID app registration with appropriate Fabric API permissions
- PowerShell 7+ with `Az.Accounts` module or MSAL.PS for token acquisition
- Access to a Microsoft Fabric workspace (Contributor or higher)
- Tenant setting **Service principals can use Fabric APIs** enabled (if using service principals)

## Quick Diagnostic: Identify Your Error

Start here. Match your HTTP status code to the appropriate workflow.

| HTTP Status | Error Category | Jump To |
|-------------|---------------|---------|
| 401 | Authentication / Token | [Authentication Failures](#workflow-1-authentication-failures-401) |
| 403 | Permissions / Authorization | [Permission Denied](#workflow-2-permission-denied-403) |
| 404 | Resource Not Found | [Resource Not Found](#workflow-3-resource-not-found-404) |
| 429 | Throttling / Rate Limit | [Throttling](#workflow-4-throttling-429) |
| 430 | Spark Compute Limit | [Capacity Limits](#workflow-5-capacity-and-spark-limits-430) |
| 500/502/503 | Server Error | [Server Errors](#workflow-6-server-errors-5xx) |
| 202 then failure | LRO Polling Issue | [LRO remediate](#workflow-7-long-running-operation-failures) |

## Understanding Fabric Error Responses

Every Fabric API error returns an `ErrorResponse` object. Always capture the `requestId` for support escalation.

```json
{
  "errorCode": "TokenExpired",
  "message": "The access token has expired.",
  "moreDetails": [],
  "relatedResource": {
    "resourceId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "resourceType": "workspace"
  },
  "requestId": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
}
```

Key rules for error handling:
1. Parse `errorCode` for programmatic logic (stable, contract-based)
2. Never parse `message` programmatically (may change over time)
3. Always log `requestId` for support cases
4. Check `relatedResource` to identify which resource caused the error

---

## Workflow 1: Authentication Failures (401)

A 401 means the request failed during authentication or access token validation.

**Step 1 — Check the `errorCode` in the response body**

| errorCode | Root Cause | Fix |
|-----------|-----------|-----|
| `TokenExpired` | Access token has expired | Acquire a fresh token and retry |
| `InsufficientScopes` | Token missing required scopes | Request correct scopes in MSAL call |

**Step 2 — Validate your token**

Run the [diagnostic script](./scripts/Test-FabricApiConnection.ps1) to test connectivity:

```powershell
./scripts/Test-FabricApiConnection.ps1 -TestEndpoint "workspaces"
```

Or decode and inspect your token manually:

```powershell
# Decode JWT token payload (PowerShell)
$token = "<your-access-token>"
$payload = $token.Split('.')[1]
$padding = 4 - ($payload.Length % 4)
if ($padding -lt 4) { $payload += '=' * $padding }
$decoded = [System.Text.Encoding]::UTF8.GetString(
    [System.Convert]::FromBase64String($payload)
) | ConvertFrom-Json
# Check expiration
$expiry = [DateTimeOffset]::FromUnixTimeSeconds($decoded.exp).LocalDateTime
Write-Host "Token expires: $expiry"
Write-Host "Scopes (scp): $($decoded.scp)"
Write-Host "Audience (aud): $($decoded.aud)"
```

**Step 3 — Verify scopes match the API**

Fabric REST APIs use scopes in the format `https://api.fabric.microsoft.com/<Scope>`. Common scopes:

| Scope | Purpose |
|-------|---------|
| `Workspace.ReadWrite.All` | Full workspace CRUD |
| `Item.ReadWrite.All` | Full item CRUD |
| `Item.Read.All` | Read-only item access |
| `Item.Execute.All` | Execute items (notebooks, pipelines) |
| `<ItemType>.ReadWrite.All` | Item-specific CRUD (e.g., `Notebook.ReadWrite.All`) |

**Step 4 — If using service principal or managed identity**

Confirm the **Service principals can use Fabric APIs** tenant setting is enabled. Not all APIs support service principals — check the individual API reference page for identity support.

See [authentication-guide.md](./references/authentication-guide.md) for detailed token acquisition examples in PowerShell and C#.

---

## Workflow 2: Permission Denied (403)

A 403 means the caller is authenticated but lacks permissions on the target resource.

**Step 1 — Check the `errorCode`**

| errorCode | Root Cause | Fix |
|-----------|-----------|-----|
| `InsufficientPrivileges` | Missing workspace/item permissions | Request access from workspace admin |

**Step 2 — Verify workspace role**

The calling identity needs at least **Contributor** role for write operations and **Viewer** for read operations.

**Step 3 — Check for API-specific requirements**

Some APIs require Fabric Admin permissions. Admin APIs are under `/v1/admin/` paths. Confirm the calling identity has the Fabric Administrator role if targeting admin endpoints.

**Step 4 — Service principal considerations**

If the API call relies on downstream items that don't support service principals, the call fails even if the top-level API does. For example, calling `Items - Create Item` to create a data warehouse will fail because data warehouses don't support service principal identity.

---

## Workflow 3: Resource Not Found (404)

A 404 means the specified resource doesn't exist or isn't accessible to the caller.

**Step 1 — Check the `errorCode`**

| errorCode | Root Cause | Fix |
|-----------|-----------|-----|
| `WorkspaceNotFound` | Invalid workspace ID | Verify the workspace GUID |
| `EntityNotFound` | Invalid resource ID | Check `relatedResource` in error for details |

**Step 2 — Validate your IDs**

```powershell
# List all accessible workspaces to find correct ID
$headers = @{ Authorization = "Bearer $token" }
$response = Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/workspaces" `
    -Headers $headers
$response.value | Select-Object id, displayName | Format-Table
```

**Step 3 — Check URL construction**

Fabric API base: `https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items`

Common mistakes: mixing up `workspaceId` with `itemId`, using display names instead of GUIDs, or targeting the wrong API version.

---

## Workflow 4: Throttling (429)

A 429 means rate limits have been exceeded. Fabric throttles per caller identity per API within one-minute windows.

**Step 1 — Read the `Retry-After` header**

The response includes a `Retry-After` header indicating seconds to wait. Always use this value rather than hardcoded delays.

**Step 2 — Implement bounded retry with exponential backoff**

Use the [retry helper script](./scripts/Invoke-FabricApiWithRetry.ps1):

```powershell
./scripts/Invoke-FabricApiWithRetry.ps1 `
    -Uri "https://api.fabric.microsoft.com/v1/workspaces" `
    -Token $token `
    -MaxRetries 5
```

**Step 3 — Reduce throttling likelihood**

| Strategy | How |
|----------|-----|
| Use batch/bulk operations | Prefer `List Items` over individual `Get Item` calls |
| Cache metadata | Store workspace/item IDs locally, refresh periodically |
| Spread requests | Add jitter between calls; avoid burst patterns |
| Use pagination efficiently | Follow `continuationToken` to completion in a single pass |

See [error-codes-reference.md](./references/error-codes-reference.md) for the complete error code table.

---

## Workflow 5: Capacity and Spark Limits (430)

HTTP 430 is Fabric-specific for Spark compute limits.

**Error message**: `[TooManyRequestsForCapacity] This spark job can't be run because you have hit a spark compute or API rate limit.`

**Resolution options**:
1. Cancel an active Spark job via the Monitoring Hub
2. Upgrade to a larger capacity SKU (queue limits scale with SKU size)
3. Wait and retry later

| Fabric SKU | Queue Limit |
|------------|-------------|
| F2 | 4 |
| F8 | 8 |
| F64 / P1 | 64 |
| F128 / P2 | 128 |
| F256 / P3 | 256 |
| Trial | No queueing |

---

## Workflow 6: Server Errors (5xx)

**Step 1 — Capture the `requestId`** from the response body or header. This is essential for Microsoft Support escalation.

**Step 2 — Retry with backoff**. Transient 500/502/503 errors often resolve on retry.

**Step 3 — Check Fabric service health** at [Microsoft 365 Service Health](https://admin.microsoft.com/Adminportal/Home#/servicehealth) or [Azure Status](https://status.azure.com/).

**Step 4 — If persistent**, open a support ticket including the `requestId`, timestamp, and full request/response details.

---

## Workflow 7: Long Running Operation Failures

Fabric uses LRO (Long Running Operations) for time-consuming tasks. An LRO returns HTTP 202 with polling headers.

**Step 1 — Capture response headers after 202**

| Header | Purpose |
|--------|---------|
| `Location` | URL to poll for operation status |
| `x-ms-operation-id` | Operation ID for constructing status URL |
| `Retry-After` | Seconds to wait before first poll |

**Step 2 — Poll the operation status**

Two approaches:
1. Use the `Location` header URL directly (preferred)
2. Construct: `GET https://api.fabric.microsoft.com/v1/operations/{operationId}`

**Step 3 — Handle terminal states**

| Status | Meaning | Action |
|--------|---------|--------|
| `Running` | Still in progress | Continue polling |
| `Succeeded` | Completed successfully | Fetch result if available |
| `Failed` | Operation failed | Check error details in response |

**Step 4 — Get the result**

If the operation has a result, append `/result` to the operation URL:
`GET https://api.fabric.microsoft.com/v1/operations/{operationId}/result`

See [long-running-operations.md](./references/long-running-operations.md) for complete polling implementation patterns.

---

## Workflow 8: Pagination Issues

Fabric uses `continuationToken` / `continuationUri` for paginated responses.

**Step 1 — Follow the token to completion**

```powershell
$allItems = @()
$uri = "https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items"
do {
    $response = Invoke-RestMethod -Uri $uri -Headers $headers
    $allItems += $response.value
    $uri = $response.continuationUri
} while ($uri)
```

**Step 2 — Common pitfalls**

| Problem | Cause | Fix |
|---------|-------|-----|
| Missing items | Stopped before token was null | Loop until `continuationToken` is null or absent |
| URL encoding errors | Token not URL-encoded | Use `continuationUri` directly (pre-encoded) |
| Stale token | Token expired mid-pagination | Refresh the bearer token between pages |

---

## remediate Decision Tree

```
API call fails
├── Got HTTP response?
│   ├── 401 → Check token expiry and scopes
│   ├── 403 → Check workspace role and API identity support
│   ├── 404 → Verify workspace/item GUIDs
│   ├── 429 → Honor Retry-After, implement backoff
│   ├── 430 → Spark capacity limit, scale up or wait
│   ├── 5xx → Retry with backoff, check service health
│   └── 202 → LRO started, poll Location header
├── Network error / timeout?
│   ├── Check DNS resolution for api.fabric.microsoft.com
│   ├── Verify no proxy/firewall blocking HTTPS
│   └── Test with: Invoke-RestMethod -Uri "https://api.fabric.microsoft.com/v1/"
└── Token acquisition failed?
    ├── Check Entra app registration exists
    ├── Verify redirect URI matches
    ├── Confirm API permissions granted and admin-consented
    └── See authentication-guide.md
```

## References

- [Error Codes Reference](./references/error-codes-reference.md) — Complete Fabric API error code table
- [Authentication Guide](./references/authentication-guide.md) — Token acquisition patterns for PowerShell and C#
- [Long Running Operations](./references/long-running-operations.md) — LRO polling implementation patterns
- [Test-FabricApiConnection.ps1](./scripts/Test-FabricApiConnection.ps1) — Diagnostic connectivity test
- [Invoke-FabricApiWithRetry.ps1](./scripts/Invoke-FabricApiWithRetry.ps1) — Retry logic with exponential backoff
- [Fabric-Api-ErrorHandler.template.ps1](./templates/Fabric-Api-ErrorHandler.template.ps1) — Starter error handling scaffold
