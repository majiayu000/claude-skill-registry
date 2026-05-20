---
name: bc-security
description: Implement BigCommerce security — OAuth token management, API authentication, webhook verification, CSP, input validation, PCI compliance, and app security best practices. Use when hardening integrations or reviewing security posture.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# BigCommerce Security

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.bigcommerce.com security authentication` for auth security
2. Web-search `bigcommerce app security best practices` for app security
3. Web-search `bigcommerce pci compliance` for PCI guidance

## API Authentication Security

### Token Management

- **Never expose** API tokens in client-side code or public repositories
- Store tokens in environment variables or encrypted secret stores
- Use separate tokens for development and production
- Rotate tokens periodically
- Use minimum required OAuth scopes (principle of least privilege)

### Token Types

| Token Type | Security Level | Storage |
|------------|---------------|---------|
| API Account Token | Highest — full API access | Server-side only, encrypted |
| OAuth App Token | High — scoped access | Server-side, per-store |
| Storefront API Token | Medium — read-only storefront data | Client-side OK (limited scope) |
| Customer Impersonation Token | High — customer data access | Server-side only |

### Rate Limiting as Security

Rate limits prevent abuse:
- Monitor `X-Rate-Limit-Requests-Left` header
- Implement exponential backoff
- Never retry 401/403 responses (authentication/authorization failures)

## OAuth Security

### JWT Verification

Always verify JWTs in Load, Uninstall, and Remove User callbacks:
- Verify signature using your Client Secret (HMAC-SHA256)
- Check `iss` (issuer) matches BigCommerce
- Check `exp` (expiration) — reject expired tokens
- Check `aud` (audience) matches your Client ID
- Extract `store_hash` and `user` only after verification

### Callback URL Security

- Use HTTPS for all callback URLs
- Validate the `state` parameter in OAuth flows to prevent CSRF
- Don't accept arbitrary redirect URLs — whitelist allowed paths

### Token Storage

- Encrypt OAuth access tokens at rest in your database
- Associate tokens with store hash — verify on every API call
- Handle token revocation (when app is uninstalled)
- Don't log tokens in application logs

## Webhook Security

### Verification

BigCommerce doesn't sign webhook payloads with HMAC, so:
- Use custom headers for basic verification:
  ```json
  { "headers": { "X-Webhook-Secret": "your-shared-secret" } }
  ```
- Verify the header value in your handler
- Validate `store_id` matches expected stores

### Webhook Handler Security

- Respond with 200 OK quickly — don't process inline
- Validate payload structure before processing
- Use idempotency (check `hash` field) to prevent replay attacks
- Don't trust the `data.id` blindly — verify by fetching the resource via API
- Rate limit your webhook handler to prevent flood attacks

## Content Security Policy (CSP)

### For Embedded Apps

When your app loads in the BigCommerce admin iframe:
- Set `Content-Security-Policy: frame-ancestors 'self' *.bigcommerce.com`
- Or use `X-Frame-Options: ALLOW-FROM https://store-{hash}.mybigcommerce.com`
- Block framing from unauthorized domains

### For Stencil Themes

Add CSP headers via Script Manager or theme configuration to restrict:
- `script-src` — allowed script sources
- `style-src` — allowed style sources
- `img-src` — allowed image sources
- `connect-src` — allowed API endpoints

## Input Validation

### API Input

- Validate all data before sending to BigCommerce API
- Sanitize user input — escape HTML, validate types
- Validate email formats, phone numbers, postal codes
- Enforce maximum lengths for text fields

### Webhook Input

- Validate JSON structure of incoming payloads
- Verify resource IDs are numeric and within expected range
- Don't use webhook data directly — fetch fresh data via API

### Stencil Theme Input

- Escape all dynamic content in Handlebars templates (auto-escaping by default)
- Use `{{{raw_html}}}` triple-braces only for trusted content
- Sanitize any user-generated content before rendering

## PCI Compliance

### Reducing Scope

BigCommerce is PCI DSS Level 1 compliant as a platform:
- **Native/Embedded Checkout** — BigCommerce handles payment form rendering → you're out of PCI scope
- **Custom Checkout with tokenized payments** — use gateway JS SDKs (Stripe Elements, etc.) → minimal PCI scope
- **Custom Checkout with raw card data** — requires full PCI DSS compliance for your infrastructure

### Recommendations

- Use Embedded Checkout for headless — simplest PCI path
- Never log, store, or transmit raw card data
- Use tokenized payment methods in the Payments API
- Serve all pages over HTTPS

## App Marketplace Security Requirements

### For Marketplace Submission

- HTTPS for all endpoints
- Proper JWT verification on all callbacks
- Secure token storage (encrypted at rest)
- Handle uninstall callback (clean up data)
- No hardcoded credentials in source code
- OWASP Top 10 compliance

## Best Practices

- Store API tokens encrypted, never in code or logs
- Verify JWTs on every callback — check signature, expiry, audience
- Use custom webhook headers for verification
- Validate and sanitize all input — from users, webhooks, and APIs
- Use Embedded Checkout or tokenized payments to minimize PCI scope
- Set CSP headers for iframe embedding
- Implement rate limiting on your webhook handlers
- Rotate credentials periodically
- Use separate credentials per environment (dev/staging/production)
- Audit third-party dependencies for known vulnerabilities

Fetch the BigCommerce security documentation and app review requirements for exact JWT verification patterns, CSP configuration, and current security best practices before implementing.
