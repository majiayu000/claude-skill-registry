---
name: live-service-e2e-testing
description: |-
  Use when building real-service end-to-end tests with fixtures, cleanup, rate limits, and evidence.
  Triggers:
practices:
- tdd
- bdd-gherkin
- sre
hexagonal_role: supporting
consumes:
- service-contract
- environment-contract
- test-plan
produces:
- real-service-e2e-suite
- evidence-packet
- cleanup-report
context_rel:
- kind: customer-of
  with: test
skill_api_version: 1
user-invocable: false
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: topic
metadata:
  tier: execution
  stability: stable
  dependencies:
  - test
  - validation
  - standards
output_contract: "Real-service E2E suite with env contract, isolation plan, cleanup proof, rate-limit policy, and redacted evidence packet."
---

# Testing Real-Service E2E No Mocks

Use this skill when a test must prove behavior against the actual external service, account, tenant, database, queue, browser, payment gateway, cloud API, or deployed environment. The goal is production-representative confidence without borrowing production risk.

## Non-Negotiables

- No mocks, stubs, fakes, simulators, local emulators, contract-only assertions, or recorded replays may substitute for the real service behavior under test.
- Never use a production tenant, customer account, live money path, or shared mutable environment unless the user explicitly authorizes that exact target.
- Missing secrets, quota, sandbox access, or network access is a blocker to report, not a reason to fake success.
- Tests must be independently repeatable: each run owns its data, names, resources, and cleanup.
- Evidence must be sufficient for a reviewer to see what service was exercised, what was asserted, and what cleanup happened, without exposing secrets or sensitive payloads.

## Build Workflow

1. Define the real-service boundary.
   Name every service, account, region, project, tenant, endpoint, webhook, queue, or browser surface that the test will touch. Mark anything that is not real-service traffic as support code only.

2. Establish account and environment isolation.
   Use a sandbox or dedicated test account. Require explicit environment variables for credentials and base URLs. Prefix all remote resources with a unique run id, and attach tags or metadata when the service supports them.

3. Design fixtures as real service state.
   Create fixtures through public APIs, CLIs, admin endpoints, or UI flows that a real client could use. Keep fixtures minimal, deterministic, and unique per run. Avoid pre-existing shared fixtures unless they are immutable and documented.

4. Register cleanup before creation.
   Add cleanup handlers before creating remote resources. Cleanup must delete, cancel, archive, refund in sandbox, revoke, or expire every resource created by the run. Only clean resources that carry the run id or explicit ownership marker.

5. Respect rate limits and cost.
   Add bounded concurrency, backoff, jitter, retry caps, and per-suite budgets. Treat 429, quota, and cost-limit responses as test signals with useful diagnostics, not as infinite retry triggers.

6. Assert through observable service behavior.
   Verify results with independent reads, callbacks, webhooks, logs, UI state, or service-side records. Use polling only for documented eventual consistency, with deadlines and clear failure messages.

7. Capture evidence.
   Save redacted request ids, resource ids, URLs, timestamps, screenshots when useful, service responses, cleanup logs, and the exact env contract used. Never store raw tokens, customer data, or irreversible secret material.

8. Gate execution deliberately.
   Real-service tests should require an explicit opt-in such as `REAL_SERVICE_E2E=1` plus service-specific credentials. Local default behavior may skip with a clear reason; CI jobs configured for this suite should fail when required env is absent.

## Test Harness Shape

- Put service credentials and base URLs behind named env vars.
- Fail fast when the target account does not match the expected sandbox marker.
- Generate a `run_id` once per suite and include it in every remote resource name or tag.
- Keep resource creation and cleanup in helper functions that return concrete resource ids.
- Prefer narrow scenario tests over broad journeys that make cleanup ambiguous.
- Emit a redacted evidence artifact at the end of the run, even when assertions fail.
- If cleanup fails, preserve enough evidence to repair manually and make the failure visible.

## Review Checklist

- The suite cannot pass without reaching the real service.
- Every external resource has a unique owner marker and cleanup path.
- Required env vars, account ids, sandbox names, and rate-limit assumptions are documented in the test code or adjacent README.
- Assertions verify service-observable outcomes rather than only local return values.
- Retries are bounded and tied to documented eventual consistency or transient service errors.
- Evidence includes run id, service request/resource ids, assertion summary, and cleanup result.

