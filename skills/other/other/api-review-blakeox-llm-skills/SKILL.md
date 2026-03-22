---
name: api-review
description: Zero-assumption API design review. Uses the API as a consumer first, then audits contracts, error shapes, auth model, pagination, versioning, idempotency, and rate limiting. Every endpoint is guilty until proven correct.
user-invocable: true
argument-hint: "[API routes, controller files, or OpenAPI spec]"
---

Read `../_house-style/house-style.md` before starting.

## Anchor phrases

- An API you need source code to understand is a broken API.
- If the error message doesn't tell the consumer how to fix the problem, it's not an error message — it's a shrug.
- Consistency isn't a nice-to-have. Every inconsistency is a trap for the next developer.
- Returning 200 with an error body is not error handling — it's lying.

## Domain-specific examples

**Error handling — wrong way:**

"The error responses could be more consistent. Consider standardizing the error format across endpoints."

**Error handling — right way:**

"`POST /api/orders` returns `200 {error: 'invalid'}` on validation failure. `POST /api/users` returns `422 {errors: [{field: 'email', message: 'required'}]}`. `DELETE /api/items/:id` returns `500 Internal Server Error` with a raw stack trace when the ID doesn't exist. Three endpoints, three different error contracts. A consumer has to handle each one as a special case. Standardize on: `4xx` status code + `{error: {code: string, message: string, details?: object}}`. The code is machine-readable, the message is human-readable, details carries field-level info for validation errors."

**Auth gap — wrong way:**

"Make sure all endpoints require authentication."

**Auth gap — right way:**

"`GET /api/users/:id` has no auth middleware. Any unauthenticated request with a valid user ID returns the full user object including `email`, `phone`, `address`, and `payment_method_last4`. The endpoint is also enumerable — sequential IDs from 1 to N. An attacker can scrape your entire user directory with a for loop. This is an IDOR vulnerability and a data exposure incident waiting for someone to find it. Fix: add auth middleware to the router group, verify the requesting user owns the resource or has admin role."

## The audit

### 1. Use it as a consumer first
Read docs, look at types, trace a CRUD workflow. Document confusion and guessing.

### 2. Endpoint design
Method matches operation? Consistent naming? Request/response shapes consistent? Correct status codes?

### 3. Error handling
Consistent format? Machine-readable codes? Consumer can fix from error alone? Validation per-field? 500s leak internals?

### 4. Auth and authorization
Every endpoint protected? Right layer? IDOR check? Token validation? Rate limiting?

### 5. Data contracts
Types exported? Nullability explicit? Pagination consistent? Filters validated?

### 6. Idempotency and concurrency
Writes idempotent? Concurrent modification handling? Ordering dependencies?

### 7. Versioning
Versioned? Breaking change policy? Deprecation path?

### Adversarial testing
For every endpoint: empty body, huge strings, nested garbage, wrong types, SQL injection, XSS, path traversal, negative IDs, duplicate requests within 100ms. Document what the API does with each.

## Output format

### Consumer experience
One paragraph from the outside.

### API score

| Metric | Score (1-10) |
|---|---|
| Consistency | |
| Error handling | |
| Auth coverage | |
| Documentation | |
| Adversarial resilience | |
| **Overall** | |

### Critical findings
Security vulns, auth gaps, data exposure. Endpoint, trigger, fix.

### Endpoint audit
Per-endpoint: what it does, what's wrong, what's missing.

### Consistency issues
Different patterns across endpoints.

### Missing from API
What consumers need that doesn't exist.

### Devil's advocate
For harshest findings: internal-only API? Known consumers? Intentional tradeoffs?

### What I didn't test / Recommended changes (priority order)
