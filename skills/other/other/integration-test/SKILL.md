---
name: integration-test
description: Write end-to-end integration tests that exercise full request-to-response flows (Priya Sharma's workflow)
disable-model-invocation: true
---

Write integration tests for: $ARGUMENTS

Integration tests differ from unit tests — they exercise the FULL path from HTTP request through auth, service, external resource, and back.

## Step 1 — Identify Integration Scenarios
Map complete user workflows:
- Full request lifecycle: HTTP → Auth → Service → External Resource → Response
- Multi-step workflows: Set state → verify → set all → verify all
- Error recovery: Resource disconnect mid-operation → verify state consistency
- Auth flows: No key → rejected, wrong key → rejected, correct key → success
- Rate limiting: Within limit → success, exceed limit → 429 → wait → success

## Step 2 — Write Integration Test Fixtures
Create a fixture that uses the REAL DI chain — no dependency overrides:
```
// Full integration fixture — uses REAL DI chain, no overrides
fixture integration_client() {
    // Initialize mock implementation, service, and app
    // NO DI overrides — tests the real dependency chain
    client = new TestHTTPClient(app, propagate_errors: false)
    yield client
}
```

## Step 3 — Write Integration Tests

### Workflow tests (multi-step):
Test complete user workflows that exercise multiple endpoints in sequence.
Verify state persists between requests and final state is consistent.

### Error recovery tests:
Test that errors leave the system in a consistent state.
Verify rollback behavior on partial failures.

### Cross-cutting tests:
- Health endpoint returns correct status based on resource connection state
- Audit log produced for every state-changing operation

## Step 4 — Organize
Place integration tests in the integration test file (see test file mapping in project config).

## Step 5 — Verify
Run the test command (see project config) — full suite still passes.

## Rules
- Integration tests use the REAL DI chain — minimal or no dependency overrides
- Test multi-step workflows, not individual operations
- Verify side effects (audit logs, state persistence) across steps
- Keep integration tests independent — each test resets state