---
name: fabric-rest-api-perf-remediate
description: Diagnose and resolve Microsoft Fabric REST API performance issues including HTTP 429 throttling, long running operation (LRO) timeouts, pagination bottlenecks, and slow API response times. Use when remediate Fabric API latency, capacity throttling, retry-after handling, operation polling failures, bulk API call optimization, or automating Fabric REST API diagnostics with PowerShell. Covers api.fabric.microsoft.com endpoint performance, Entra ID token acquisition delays, and Fabric capacity SKU rate limits.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric REST API Performance remediate

Structured diagnostic workflows and automation scripts for identifying and resolving performance bottlenecks in Microsoft Fabric REST API integrations.

## When to Use This Skill

- API calls to `api.fabric.microsoft.com` are slow or timing out
- Receiving HTTP 429 (Too Many Requests) responses with Retry-After headers
- Long running operations (LRO) polling is inefficient or stalling
- Paginated API responses are taking too long to enumerate
- Bulk workspace or item operations exceed capacity throttle limits
- Entra ID token acquisition is adding unexpected latency
- Spark job submissions return HTTP 430 (TooManyRequestsForCapacity)
- Need to benchmark Fabric REST API throughput for a given capacity SKU

## Prerequisites

- PowerShell 7+ with `Invoke-RestMethod` support
- Microsoft Entra ID app registration with appropriate Fabric scopes
- A valid Bearer token or MSAL-based authentication flow
- Access to at least one Fabric workspace

## Diagnostic Decision Tree

Determine the root cause category before applying a fix:

```
API Call Slow or Failing?
├── HTTP 429 returned?
│   ├── YES → Throttling. See §1 Throttling Diagnosis
│   └── NO  → Continue
├── HTTP 430 returned?
│   ├── YES → Capacity exhausted. See §2 Capacity Limits
│   └── NO  → Continue
├── HTTP 202 + LRO stalling?
│   ├── YES → Polling issue. See §3 LRO Optimization
│   └── NO  → Continue
├── Large result sets slow?
│   ├── YES → Pagination. See §4 Pagination Tuning
│   └── NO  → Continue
├── Token acquisition slow?
│   ├── YES → Auth latency. See §5 Token Performance
│   └── NO  → General latency. See §6 Baseline Benchmarking
```

---

## §1 Throttling Diagnosis (HTTP 429)

Fabric throttles per-user, per-API within a time window. When exceeded, the API returns HTTP 429 with a `Retry-After` header (in seconds).

**Diagnosis Steps:**

1. Run the [throttle diagnostic script](./scripts/Test-FabricApiThrottle.ps1) to measure your current request rate against throttle limits
2. Capture `Retry-After` header values to understand cooldown periods
3. Review call patterns for burst behavior vs. steady-state

**Resolution Patterns:**

| Pattern | Description |
|---------|-------------|
| Exponential backoff | Respect `Retry-After`, then add jitter to avoid thundering herd |
| Request batching | Group related calls to reduce total API invocations |
| Caller isolation | Use separate service principals for independent workloads |
| Rate limiter | Implement a client-side token bucket before sending requests |

**Key Facts:**

- Every Fabric admin and core public API call is throttled
- Throttle window and limits are per-user, per-API (not published explicitly)
- The `Retry-After` value is in seconds (commonly 30-60s)

See [throttling-deep-dive.md](./references/throttling-deep-dive.md) for implementation patterns.

---

## §2 Capacity Rate Limits (HTTP 430)

Spark jobs and compute-bound operations have a separate throttle tied to the Fabric capacity SKU. When the max queue limit is reached, new jobs return HTTP 430.

**Capacity Queue Limits:**

| SKU | Queue Limit |
|-----|-------------|
| F2 / F4 | 4 |
| F8 | 8 |
| F16 | 16 |
| F32 | 32 |
| F64 (P1) | 64 |
| F128 (P2) | 128 |
| F256 (P3) | 256 |
| F512 (P4) | 512 |
| F1024 | 1024 |
| F2048 | 2048 |
| Trial | Not supported |

**Resolution:**

1. Cancel active Spark jobs via the Monitoring Hub
2. Upgrade to a larger capacity SKU
3. Enable optimistic job admission for higher concurrency
4. Implement client-side queue management before submitting jobs

---

## §3 Long Running Operation (LRO) Optimization

Many Fabric APIs return HTTP 202 Accepted with three critical headers:

- `Location` — polling URL (Get Operation State endpoint)
- `x-ms-operation-id` — operation GUID for constructing polling URLs
- `Retry-After` — seconds to wait before first poll

**Common Performance Issues:**

| Issue | Symptom | Fix |
|-------|---------|-----|
| Aggressive polling | Hundreds of GET calls, wastes quota | Honor `Retry-After`, use exponential backoff |
| Ignoring Location header | Building URLs manually, missing result endpoint | Use Location header directly; it transitions from State to Result when complete |
| Not checking for result | Polling succeeds but result never fetched | After `Succeeded` status, call Get Operation Result |
| Missing failure handling | Stuck in infinite poll loop | Check for `Failed` and `Skipped` statuses |

**LRO Status Values:** `Succeeded`, `Failed`, `Skipped`, `Completed`

Run the [LRO polling benchmark script](./scripts/Measure-FabricLroPolling.ps1) to profile your polling efficiency.

See [lro-patterns.md](./references/lro-patterns.md) for complete polling implementation patterns.

---

## §4 Pagination Tuning

Fabric paginated APIs return `continuationToken` and `continuationUri` in response bodies. Performance degrades when consuming large result sets sequentially.

**Optimization Strategies:**

1. Use `continuationUri` directly rather than rebuilding URLs with `continuationToken`
2. Process pages concurrently when downstream logic allows
3. Implement early termination when the target item is found
4. Cache intermediate results for retry resilience

**Template:** Use the [pagination walker template](./templates/Invoke-FabricPaginatedApi.ps1) for efficient enumeration.

---

## §5 Token Acquisition Performance

Slow Entra ID token acquisition adds latency to every API call chain.

**Diagnosis:**

1. Measure token acquisition time separately from API call time
2. Check if tokens are being acquired per-request instead of cached
3. Verify token lifetime and refresh logic

**Optimization:**

| Technique | Impact |
|-----------|--------|
| Token caching | Eliminate redundant auth round-trips |
| MSAL token cache serialization | Persist tokens across process restarts |
| Certificate-based auth | Faster than client secret for service principals |
| Reduce scope requests | Request only needed scopes per call |

---

## §6 Baseline Benchmarking

Before remediate, establish a performance baseline.

Run the [baseline benchmark script](./scripts/Measure-FabricApiBaseline.ps1) to capture:

- Token acquisition latency (ms)
- Simple GET endpoint response time (ms)
- Paginated enumeration throughput (items/sec)
- LRO polling round-trip time (ms)

Compare results against expected ranges in the [baseline reference](./references/baseline-expectations.md).

---

## Quick Reference: HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 201 | Created (LRO complete) | Fetch result |
| 202 | Accepted (LRO started) | Begin polling via Location header |
| 400 | Bad request | Validate request body/parameters |
| 401 | Unauthorized | Refresh token, check scopes |
| 403 | Forbidden | Verify workspace/item permissions |
| 404 | Not found | Confirm workspace/item IDs |
| 429 | Throttled | Wait `Retry-After` seconds, then retry |
| 430 | Capacity exhausted | Reduce concurrent jobs or scale SKU |

---

## remediate

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| All calls slow (>2s) | Token not cached | Implement MSAL token caching |
| Intermittent 429s | Burst pattern | Add rate limiter with token bucket |
| LRO never completes | Operation failed silently | Check for `Failed` status in poll response |
| Pagination returns duplicates | Stale continuationToken | Always use fresh `continuationUri` from latest response |
| 430 on Spark submit | Capacity queue full | Check Monitoring Hub, scale SKU, or wait |
| Token acquisition >3s | Network/DNS issue | Test connectivity to `login.microsoftonline.com` |

## References

- [Throttling Deep Dive](./references/throttling-deep-dive.md) — retry patterns, jitter, token bucket implementation
- [LRO Patterns](./references/lro-patterns.md) — polling state machines, cancellation, parallel LRO management
- [Baseline Expectations](./references/baseline-expectations.md) — expected latency ranges by operation type
- [Fabric REST API Scopes](./references/fabric-api-scopes.md) — scope reference for Entra ID app registration
