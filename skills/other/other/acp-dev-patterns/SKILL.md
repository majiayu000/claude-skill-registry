---
name: acp-dev-patterns
description: Cross-cutting ACP development patterns — idempotency, error handling, 3D Secure flows, request signing, rate limiting, monitoring, and security best practices. Use when designing architecture or solving production concerns.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Development Patterns

## Before writing code

**Fetch live docs**:
- Checkout spec: Fetch `https://developers.openai.com/commerce/specs/checkout/` for error codes and idempotency rules
- Production guide: Fetch `https://developers.openai.com/commerce/guides/production/` for operational requirements
- Stripe integration: Web-search `site:docs.stripe.com agentic-commerce` for PSP-side patterns
- Changelog: Web-search `site:github.com agentic-commerce-protocol CHANGELOG` for latest changes

## Pattern: Idempotency

Every POST request MUST include `Idempotency-Key` (UUID v4, max 255 chars).

**Server-side implementation**:
- Store key → response mapping for minimum 24 hours
- Same key + identical body = replay original response, add `Idempotent-Replayed: true` header
- Same key + different body = 422 `idempotency_conflict`
- Key in flight = 409 `idempotency_in_flight` with `Retry-After` header
- 5xx responses are NOT cached — retries treated as fresh requests

**Client-side implementation**:
- Generate UUID v4 for each logical operation
- Reuse the same key when retrying a failed request
- Generate a new key for a genuinely new operation
- Handle 409 by waiting per `Retry-After` then retrying

## Pattern: Error Handling

ACP uses a flat error structure:
```
{type, code, message, param}
```

- `type`: `invalid_request` | `processing_error` | `service_unavailable`
- `code`: Well-known identifier (e.g., `idempotency_conflict`, `invalid_card`, `rate_limit_exceeded`)
- `message`: Human-readable description
- `param`: JSONPath (RFC 9535) to the offending field

**Retry strategy**:
- `429 rate_limit_exceeded` — Exponential backoff with jitter
- `409 idempotency_in_flight` — Wait per `Retry-After` header
- `5xx` — Retry with same idempotency key, exponential backoff
- `4xx` (except 429) — Do not retry, fix the request

## Pattern: 3D Secure Authentication

When `complete` returns `authentication_required`:

1. Extract 3DS challenge from the response
2. Present challenge to the buyer (redirect or modal)
3. Buyer completes authentication
4. Call `complete` again with `authentication_result`:
   - `three_ds_cryptogram`
   - `electronic_commerce_indicator`
   - `transaction_id`
   - `version`
5. Merchant processes the authenticated payment

Handle authentication timeouts and failures gracefully.

## Pattern: Request Signing

For request integrity verification:
- **Signature header**: Base64-encoded signature over canonical JSON body
- **Timestamp header**: RFC 3339 for freshness validation
- **Algorithm**: HMAC (Base64-encoded HMAC signature over canonical JSON body)
- **Verification**: Reconstruct canonical JSON, verify signature, check timestamp within clock-skew window

## Pattern: Webhook Delivery

Merchant → Agent webhook best practices:
- Sign EVERY event with HMAC-SHA256
- Include event ID for consumer-side deduplication
- Implement exponential backoff for failed deliveries
- Set reasonable timeouts (5-30 seconds)
- Log delivery attempts and responses
- Queue events if the webhook endpoint is down
- Verify the receiving endpoint uses HTTPS

## Pattern: API Versioning

- Always send `API-Version: YYYY-MM-DD` header
- Pin to a specific version in your code
- Test against new versions before upgrading
- Handle version-specific response shape differences
- Log the version used for debugging

## Pattern: Rate Limiting

- Implement server-side rate limiting per API key
- Return 429 with `Retry-After` header when exceeded
- Client-side: Honor `Retry-After`, add jitter to prevent thundering herd
- Monitor rate limit proximity and alert before hitting limits

## Pattern: Monetary Amount Safety

- ALL amounts as integers in minor currency units
- `$19.99` = `1999` (cents)
- Never use floating-point for money
- Validate on input and output
- Use language-specific money libraries (e.g., `decimal` in Python, `BigInt` in JS)

## Pattern: Monitoring & Observability

- Log every checkout operation with session ID and status
- Track conversion funnel: create → update → complete → order
- Alert on error rate spikes (especially 5xx)
- Monitor idempotency key reuse patterns
- Track payment success/failure rates
- Dashboard SPT provisioning and consumption
- Monitor webhook delivery success rates

## Pattern: Security Checklist

- TLS 1.2+ on all endpoints
- Bearer token rotation strategy
- No PCI data in logs (redact card numbers, CVCs)
- IP allowlisting for agent platform connections
- Request signing for integrity verification
- HMAC verification on all incoming webhooks
- Rate limiting to prevent abuse
- Input validation on all fields
- CORS configuration (if browser-facing)

Fetch the latest spec and production guide for current error codes, header requirements, and security recommendations before implementing.
