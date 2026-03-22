---
name: api-testing-patterns
description: API-specific testing patterns covering functional, security, performance, contract, and integration dimensions. Use when writing API tests, reviewing API test coverage, or assessing API test quality. Do NOT use for API design decisions -- use api-design-patterns instead. Do NOT use for general testing principles -- use testing-principles instead.
durability: encoded-preference
---

# API Testing Patterns

## Core Principle

Every API endpoint must be validated across six dimensions: functional, security, performance, contract, error handling, and integration. Missing any dimension is a coverage gap.

## API Test Coverage Dimensions

| Dimension | What to Test | When to Flag Missing |
|-----------|-------------|---------------------|
| Functional | Request/response correctness, status codes, payload shape, field validation | Any new or modified endpoint without functional tests |
| Security | Authentication, authorization, input sanitization, abuse resistance | Any public-facing or auth-dependent endpoint without security tests |
| Performance | Response time SLAs, concurrency behavior, degradation under load | Any endpoint serving user-facing traffic without performance assertions |
| Contract | Schema compatibility, backward compatibility, consumer expectations | Any endpoint consumed by other services without contract tests |
| Error handling | Error response format, edge cases, failure modes | Any endpoint without negative test cases |
| Integration | Service-to-service communication, fallback behavior, timeout handling | Any endpoint calling external services without integration tests |

## Functional Testing

- Verify sensitive fields are never leaked in responses (passwords, internal IDs, tokens)
- Test pagination, filtering, and sorting parameters when applicable
- Test idempotency: calling the same mutation twice should not produce duplicate side effects

## Contract Testing

- Consumer-driven contracts: consumers define expectations, providers verify compliance
- Backward compatibility: adding fields is safe; removing or renaming fields breaks consumers
- Contract tests run in CI on every change to API response structures

### Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Testing contracts only on the provider side | Consumer-driven: let consumers define what they need |
| Skipping contract tests for "internal" APIs | Internal APIs have consumers too -- they need contracts |
| Manual schema comparison | Automate schema validation in CI |

## API Security Testing (OWASP API Security Top 10)

Test every API against these vulnerability categories. This list is distinct from the general OWASP Top 10 covered by `security-patterns`.

| # | Vulnerability | What to Test |
|---|--------------|-------------|
| API1 | Broken Object Level Authorization | Access resource IDs belonging to other users; verify 403 |
| API2 | Broken Authentication | Token expiry, invalid tokens, missing tokens, brute force resistance |
| API3 | Broken Object Property Level Authorization | Attempt to read/write properties beyond the caller's permission scope |
| API4 | Unrestricted Resource Consumption | Rate limiting enforcement, payload size limits, query complexity limits |
| API5 | Broken Function Level Authorization | Call admin endpoints as regular user; verify 403 |
| API6 | Unrestricted Access to Sensitive Business Flows | Automate purchase/signup/voting flows; verify abuse controls exist |
| API7 | Server Side Request Forgery | Pass internal URLs in request fields; verify the server rejects or sanitizes |
| API8 | Security Misconfiguration | Verify CORS, HTTP headers, debug endpoints disabled, default credentials removed |
| API9 | Improper Inventory Management | Verify deprecated/shadow API versions return 404 or redirect |
| API10 | Unsafe Consumption of APIs | When the API calls third-party APIs, verify input from those APIs is validated |

### Security Test Principles

For general security testing patterns, see security-patterns skill. The following are API-testing-specific:

- Always test authentication bypass: requests without tokens must return 401
- Always test authorization escalation: requests for other users' resources must return 403
- Verify rate limiting returns 429 with Retry-After header under burst load
- Verify error responses do not leak stack traces, internal paths, or query details

## Performance Threshold Categories

Define thresholds per endpoint, not globally. Different endpoints have different SLA expectations.

| Category | Notes |
|----------|-------|
| Response time (p95) | Define per endpoint based on SLA |
| Throughput | Test at multiples of normal traffic; verify no error rate increase |
| Error rate under load | Track 4xx and 5xx separately |
| Concurrent connections | Verify graceful degradation at pool exhaustion, not crashes |
| Payload size | Test with maximum expected payload; verify no timeout or memory issues |

## Error Handling and Edge Case Testing

Every API endpoint must have negative test cases covering:

| Category | Test Cases |
|----------|-----------|
| Malformed input | Invalid JSON, wrong content-type, truncated payloads |
| Missing required fields | Each required field omitted individually |
| Type violations | String where number expected, array where object expected |
| Boundary values | Empty strings, zero, negative numbers, max-length strings, Unicode, special characters |
| Duplicate operations | Creating the same resource twice (idempotency verification) |
| Concurrent modifications | Simultaneous updates to the same resource (conflict detection) |
| Timeout and cancellation | Slow upstream dependencies, client disconnect during processing |

## Integration Testing for Microservice Communication

| Pattern | What to Test |
|---------|-------------|
| Synchronous calls | Request/response between services, timeout handling, retry behavior |
| Asynchronous messaging | Message publishing, consumption, ordering, dead-letter handling |
| Circuit breaker | Verify circuit opens after failure threshold, half-open recovery, fallback responses |
| Service discovery | Verify correct routing when instances scale up/down |
| Distributed transactions | Saga completion, compensation on failure, idempotency of each step |

### Integration Test Principles

- Test with real service instances where feasible; use contract stubs for services you do not own
- Verify timeout and retry configuration: ensure retries use exponential backoff with jitter
- Test failure propagation: when a downstream service fails, verify the upstream returns an appropriate error (not 500 with a raw exception)
- Test data consistency: after a multi-service operation, verify all services have consistent state
- Isolate integration tests from unit/functional tests -- they have different reliability characteristics and execution times
