---
name: dapr-middleware-validator
description: Automatically validate DAPR HTTP middleware configuration files. Checks for correct middleware types, proper secret references, pipeline ordering, and security best practices. Use when configuring OAuth2, Bearer tokens, OPA policies, rate limiting, or other middleware.
allowed-tools: Read, Grep, Glob
---

# DAPR Middleware Configuration Validator

This skill validates DAPR HTTP middleware components for security and correctness.

## When to Use

Claude automatically uses this skill when:
- A middleware YAML file is created or modified
- User configures OAuth2, Bearer, OPA, or rate limiting
- Pipeline configuration is being set up
- Before deploying middleware-protected APIs

## Middleware Types

### Authentication Middleware
| Type | Component Type | Purpose |
|------|---------------|---------|
| OAuth2 | `middleware.http.oauth2` | Authorization Code flow |
| OAuth2 CC | `middleware.http.oauth2clientcredentials` | Service-to-service auth |
| Bearer | `middleware.http.bearer` | JWT/OIDC token validation |

### Authorization Middleware
| Type | Component Type | Purpose |
|------|---------------|---------|
| OPA | `middleware.http.opa` | Policy-based authorization |

### Traffic Control Middleware
| Type | Component Type | Purpose |
|------|---------------|---------|
| Rate Limit | `middleware.http.ratelimit` | Request throttling |
| Sentinel | `middleware.http.sentinel` | Circuit breaker/flow control |

### Request Processing Middleware
| Type | Component Type | Purpose |
|------|---------------|---------|
| Router Alias | `middleware.http.routeralias` | Route rewriting |
| Router Checker | `middleware.http.routerchecker` | Route validation |
| WASM | `middleware.http.wasm` | Custom WebAssembly logic |
| Uppercase | `middleware.http.uppercase` | Testing only |

## Validation Rules

### OAuth2 Middleware Validation

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: oauth2
spec:
  type: middleware.http.oauth2
  version: v1
  metadata:
  - name: clientId
    secretKeyRef:           # REQUIRED: Use secretKeyRef
      name: oauth-secrets
      key: client-id
  - name: clientSecret
    secretKeyRef:           # REQUIRED: Use secretKeyRef
      name: oauth-secrets
      key: client-secret
  - name: scopes
    value: "openid profile" # REQUIRED
  - name: authURL
    value: "https://..."    # REQUIRED: Must be HTTPS
  - name: tokenURL
    value: "https://..."    # REQUIRED: Must be HTTPS
  - name: redirectURL
    value: "..."            # REQUIRED
  - name: forceHTTPS
    value: "true"           # RECOMMENDED for production
```

**Checks performed:**
- [ ] `clientId` uses `secretKeyRef` (not plain value)
- [ ] `clientSecret` uses `secretKeyRef` (not plain value)
- [ ] `authURL` uses HTTPS protocol
- [ ] `tokenURL` uses HTTPS protocol
- [ ] `forceHTTPS` is "true" for production

### Bearer Token Validation

```yaml
spec:
  type: middleware.http.bearer
  metadata:
  - name: audience
    value: "api://..."      # REQUIRED
  - name: issuer
    value: "https://..."    # REQUIRED: Must be HTTPS
```

**Checks performed:**
- [ ] `audience` is specified
- [ ] `issuer` uses HTTPS protocol
- [ ] Issuer matches known providers or is valid URL

### OPA Middleware Validation

```yaml
spec:
  type: middleware.http.opa
  metadata:
  - name: defaultStatus
    value: "403"            # RECOMMENDED: 403 for authz failures
  - name: rego
    value: |
      package http
      default allow = false  # REQUIRED: Default deny
```

**Checks performed:**
- [ ] Rego policy has `default allow = false`
- [ ] Policy uses `package http`
- [ ] `includedHeaders` contains Authorization if JWT checking
- [ ] No hardcoded secrets in policy

### Rate Limit Validation

```yaml
spec:
  type: middleware.http.ratelimit
  metadata:
  - name: maxRequestsPerSecond
    value: "100"            # REQUIRED: Reasonable limit
```

**Checks performed:**
- [ ] `maxRequestsPerSecond` is specified
- [ ] Value is reasonable (not 0, not extremely high)

### Sentinel Validation

```yaml
spec:
  type: middleware.http.sentinel
  metadata:
  - name: appName
    value: "my-service"     # REQUIRED
  - name: flowRules
    value: |                # At least one rule type required
      [...]
```

**Checks performed:**
- [ ] `appName` is specified
- [ ] At least one rule type is defined (flowRules, circuitBreakerRules, etc.)
- [ ] Resource paths in rules are valid format
- [ ] Threshold values are reasonable

### WASM Validation

```yaml
spec:
  type: middleware.http.wasm
  metadata:
  - name: url
    value: "file://..."     # REQUIRED
```

**Checks performed:**
- [ ] `url` is specified with valid scheme (file://, http://, https://)
- [ ] HTTPS used for remote WASM binaries
- [ ] Path exists for file:// URLs (if verifiable)

### Router Alias Validation

```yaml
spec:
  type: middleware.http.routeralias
  metadata:
  - name: routes
    value: |                # REQUIRED
      {"/api": "/v1.0/invoke/..."}
```

**Checks performed:**
- [ ] `routes` is valid JSON or YAML
- [ ] Target paths are valid Dapr API paths

### Router Checker Validation

```yaml
spec:
  type: middleware.http.routerchecker
  metadata:
  - name: rule
    value: "^[A-Za-z0-9/._-]+$"  # REQUIRED: Valid regex
```

**Checks performed:**
- [ ] `rule` is valid regex pattern
- [ ] Pattern is security-appropriate (blocks common attacks)

## Pipeline Order Validation

Correct middleware ordering:

```yaml
spec:
  httpPipeline:
    handlers:
    - name: routerchecker     # 1. Block invalid requests first
      type: middleware.http.routerchecker
    - name: ratelimit         # 2. Rate limit before auth
      type: middleware.http.ratelimit
    - name: bearer-auth       # 3. Authenticate
      type: middleware.http.bearer
    - name: opa-authz         # 4. Authorize (after auth)
      type: middleware.http.opa
    - name: routeralias       # 5. Transform routes last
      type: middleware.http.routeralias
```

**Order checks:**
- [ ] Rate limiting comes before authentication
- [ ] Authorization comes after authentication
- [ ] Route validation comes before other middleware
- [ ] Route aliasing comes after security middleware

## Security Checks

### Critical Security Issues
1. **Plain-text credentials** - clientId/clientSecret not in secretKeyRef
2. **HTTP URLs** - Auth/token URLs using HTTP instead of HTTPS
3. **Default allow** - OPA policy without explicit default deny
4. **No rate limiting** - APIs without request throttling

### Warnings
1. **Missing forceHTTPS** - OAuth2 without HTTPS enforcement
2. **High rate limits** - Very permissive request limits
3. **Overly permissive OPA** - Policies with broad allow rules
4. **Missing headers** - OPA not checking Authorization header

## Output Format

```
DAPR Middleware Validation Report
==================================

✓ components/oauth2-auth.yaml - Valid
  - Type: middleware.http.oauth2
  - Credentials use secretKeyRef: Yes
  - HTTPS enforced: Yes

⚠ components/ratelimit.yaml - Warning
  - Type: middleware.http.ratelimit
  - Warning: Rate limit of 10000 RPS is very high
  - Recommendation: Consider lower limit for public APIs

✗ components/bearer-auth.yaml - Invalid
  - Type: middleware.http.bearer
  - Error: Missing required field 'audience'
  - Error: 'issuer' uses HTTP instead of HTTPS

Pipeline Analysis:
✗ Rate limiting should come BEFORE authentication middleware
  Current order: [bearer-auth, ratelimit]
  Recommended:   [ratelimit, bearer-auth]

Security Summary:
- Critical: 1 (plain-text credentials)
- Warnings: 2
- Valid: 3
```

## Common Issues and Fixes

### Plain-Text Credentials
```yaml
# BAD (security risk)
- name: clientSecret
  value: "my-secret-key"

# GOOD (use secret reference)
- name: clientSecret
  secretKeyRef:
    name: oauth-secrets
    key: client-secret
```

### HTTP Instead of HTTPS
```yaml
# BAD (insecure)
- name: tokenURL
  value: "http://auth.example.com/token"

# GOOD
- name: tokenURL
  value: "https://auth.example.com/token"
```

### Default Allow in OPA
```rego
# BAD (insecure - allows everything by default)
package http
default allow = true

# GOOD (secure - denies by default)
package http
default allow = false
allow { ... specific conditions ... }
```

### Wrong Pipeline Order
```yaml
# BAD (auth before rate limit allows DoS via auth endpoints)
handlers:
- name: oauth2
  type: middleware.http.oauth2
- name: ratelimit
  type: middleware.http.ratelimit

# GOOD (rate limit protects auth endpoints)
handlers:
- name: ratelimit
  type: middleware.http.ratelimit
- name: oauth2
  type: middleware.http.oauth2
```

## Integration Points

This skill integrates with:
- `middleware-expert` agent for detailed configuration help
- `security-scanner` skill for broader security analysis
- `/dapr:middleware` command to generate valid configs
- `/dapr:security` command for pre-deployment checks
