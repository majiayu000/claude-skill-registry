---
name: acp-conformance
description: Validate an ACP implementation against the protocol specification — schema validation, flow testing, error handling, idempotency, security checks, and production readiness. Use when preparing for launch or certifying compliance.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
disable-model-invocation: true
---

# ACP Conformance & Production Readiness

## Before writing code

**Fetch live docs**:
1. Fetch `https://developers.openai.com/commerce/guides/production/` for OpenAI's production readiness checklist
2. Web-search `site:github.com agentic-commerce-protocol spec openapi` for the latest OpenAPI specs to validate against
3. Web-search `site:github.com agentic-commerce-protocol spec json-schema` for JSON schemas
4. Fetch `https://developers.openai.com/commerce/guides/get-started/` for onboarding requirements

## Conformance Test Categories

### 1. Schema Validation

- Validate all request/response payloads against the ACP JSON schemas
- Ensure monetary amounts are integers in minor currency units (no floats)
- Verify all required fields are present
- Check field types match the spec (string, integer, enum values)

### 2. Checkout Flow Tests

- **Create** → verify 201 response with valid CheckoutSession
- **Update** → verify status transitions are valid
- **Retrieve** → verify GET returns current state
- **Complete** → verify payment processing and `completed` status
- **Cancel** → verify session termination
- **Full flow** → create → update → complete end-to-end

### 3. State Machine Compliance

- Verify only valid status transitions occur
- Test `not_ready_for_payment` → `ready_for_payment` when all data provided
- Test `authentication_required` → `completed` after 3DS
- Verify `canceled` is terminal (no transitions out)
- Test concurrent requests on same session

### 4. Idempotency Tests

- Same `Idempotency-Key` + same body = identical response with `Idempotent-Replayed: true`
- Same key + different body = 422 `idempotency_conflict`
- Concurrent duplicate = 409 `idempotency_in_flight` with `Retry-After`
- Keys retained minimum 24 hours
- 5xx responses are NOT cached

### 5. Header Validation

- `Authorization: Bearer <token>` required on all requests
- `API-Version` required and matches spec version
- `Idempotency-Key` required on all POST
- Missing required headers → appropriate error response

### 6. Error Response Format

- All errors use flat `{type, code, message, param}` structure
- `param` uses JSONPath (RFC 9535) syntax
- Correct HTTP status codes for each error type
- `type` is one of: `invalid_request`, `processing_error`, `service_unavailable`

### 7. Webhook Signature Verification

- All webhooks signed with HMAC-SHA256
- Signature in correct header
- Timing-safe comparison on receiving end
- Invalid signatures rejected

### 8. Security Checks

- TLS 1.2+ enforced
- No raw card data in logs
- SPTs properly scoped (amount, merchant, session, expiration)
- Bearer tokens validated on every request
- IP allowlisting configured (if applicable)

### 9. Extension Compliance

- Capability negotiation works correctly
- Unsupported extensions gracefully ignored
- Extension pruning works when parent capability absent
- Discount codes properly validated and errors returned

### Production Readiness Checklist

- [ ] All 5 checkout operations implemented and tested
- [ ] Idempotency handling complete
- [ ] Webhook signing and delivery implemented
- [ ] Error responses match spec format
- [ ] 3D Secure flow handled
- [ ] Monitoring and logging in place
- [ ] Rate limiting configured
- [ ] PCI compliance verified (if handling delegate payment)
- [ ] Load testing completed
- [ ] Onboarding with OpenAI/agent platform complete

Fetch the OpenAI production readiness guide and latest OpenAPI specs for the most current conformance requirements before testing.
