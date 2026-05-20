---
name: endpoint-check
description: Check endpoint security configuration for web properties
user-invocable: true
---

You are helping the team check endpoint security configuration for Jocko Fuel web properties.

Follow these steps:

### Step 1: Identify Endpoints

Ask the user which endpoints to check, or default to known properties:
- **Primary storefront**: jockofuel.com
- **Wholesale store**: jocko-fuel-wholesale.myshopify.com
- **MCP servers**: Horizon FastMCP endpoints
- **Custom domains**: Any additional web properties
- **Cloud functions**: GCP Cloud Run / Cloud Functions endpoints

### Step 2: Check TLS Configuration

Delegate to the `endpoint-security-auditor` agent to verify:
- Certificate validity and expiration dates
- TLS version support (require TLS 1.2+, flag TLS 1.0/1.1)
- Cipher suite strength (flag weak ciphers)
- Certificate chain completeness
- HSTS configuration and preload status

### Step 3: Audit Security Headers

Check HTTP response headers on each endpoint:
- **Content-Security-Policy** (CSP)
- **Strict-Transport-Security** (HSTS)
- **X-Content-Type-Options**: nosniff
- **X-Frame-Options**: DENY or SAMEORIGIN
- **Referrer-Policy**
- **Permissions-Policy**

Grade each endpoint: A (all headers), B (most headers), C (some headers), F (missing critical headers).

### Step 4: Check DNS Security

Delegate to the `endpoint-security-auditor` agent to verify:
- SPF records for email domains
- DKIM signing configuration
- DMARC policy and reporting
- DNSSEC status (if applicable)

### Step 5: Deliver Report

Present findings per endpoint with:
- TLS grade (A+ through F)
- Security header grade
- DNS security status
- Specific items to fix, ordered by priority

### Error Handling

- If an endpoint is unreachable, note it and recommend investigating uptime
- If headers are managed by a CDN or WAF, note the configuration layer
- If DNS records are managed externally, provide the expected settings
