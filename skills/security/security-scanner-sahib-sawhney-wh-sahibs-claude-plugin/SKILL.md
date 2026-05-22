---
name: dapr-security-scanner
description: Scans DAPR projects for security issues including plain-text secrets, missing ACLs, insecure configurations, and security best practice violations. Automatically triggers on component file modifications.
---

# DAPR Security Scanner

Proactively scan DAPR configurations for security vulnerabilities and best practice violations.

## When to Activate

This skill should be invoked:
- When component YAML files are created or modified
- When the user asks about security concerns
- Before deployment to production
- During code review of DAPR configurations

## Security Checks

### 1. Plain-Text Secrets Detection

Scan for hardcoded credentials in component files:

```yaml
# BAD - Plain text secret
- name: connectionString
  value: "Server=myserver;Password=secret123"

# GOOD - Using secret reference
- name: connectionString
  secretKeyRef:
    name: db-secrets
    key: connectionString
```

**Check for:**
- `password`, `secret`, `key`, `token`, `credential` in value fields
- Connection strings with embedded passwords
- API keys in plain text
- Base64-encoded secrets (still exposed)

### 2. Missing Secret Store References

Verify sensitive fields use `secretKeyRef`:

```yaml
# Required for these field patterns:
- *password*
- *secret*
- *key* (except keyName for crypto)
- *token*
- *credential*
- connectionString
- accessKey
- apiKey
```

### 3. Component Scope Validation

Check that sensitive components have scopes defined:

```yaml
# Components requiring scopes:
- secretstores.* - MUST have scopes
- state.* with sensitive data - SHOULD have scopes
- pubsub.* - SHOULD have scopes
- bindings.* with write access - SHOULD have scopes
```

### 4. Managed Identity Recommendations

Flag connection string usage when managed identity is available:

```yaml
# Azure components should prefer:
- azureClientId (for managed identity)
# Over:
- connectionString
- accountKey
```

### 5. ACL Configuration

Verify access control is properly configured:
- Check for `accessControl` in Configuration resources
- Verify `defaultAction: deny` is set
- Ensure service-specific policies exist

### 6. mTLS Configuration

Check mutual TLS settings:
```yaml
spec:
  mtls:
    enabled: true  # Should be true for production
```

### 7. Resiliency Policy Validation

Verify resiliency policies exist for production:
- Check for Resiliency resource
- Verify circuit breakers for external services
- Check retry policies have reasonable limits

## Scanning Commands

### Scan Single File
```bash
python scripts/security-scan.py path/to/component.yaml
```

### Scan All Components
```bash
python scripts/security-scan.py components/
```

### Generate Report
```bash
python scripts/security-scan.py --report security-report.json
```

## Severity Levels

| Severity | Description | Examples |
|----------|-------------|----------|
| CRITICAL | Immediate security risk | Plain-text passwords, exposed API keys |
| HIGH | Significant vulnerability | Missing scopes on secret stores, no mTLS |
| MEDIUM | Security improvement needed | No resiliency policies, missing ACLs |
| LOW | Best practice recommendation | Using connection strings vs managed identity |

## Report Format

```json
{
  "scan_time": "2024-01-01T12:00:00Z",
  "files_scanned": 5,
  "issues": [
    {
      "severity": "CRITICAL",
      "file": "components/statestore.yaml",
      "line": 15,
      "message": "Plain-text password detected in 'redisPassword'",
      "recommendation": "Use secretKeyRef instead of value"
    }
  ],
  "summary": {
    "critical": 1,
    "high": 0,
    "medium": 2,
    "low": 3
  }
}
```

## Auto-Fix Capabilities

For common issues, suggest automatic fixes:

### Convert Plain-Text to SecretKeyRef
```yaml
# Before
- name: password
  value: "mysecret"

# After (suggested)
- name: password
  secretKeyRef:
    name: app-secrets
    key: password
```

### Add Missing Scopes
```yaml
# Before
spec:
  type: secretstores.azure.keyvault
  ...

# After (suggested)
spec:
  type: secretstores.azure.keyvault
  ...
scopes:
  - app-id-1
```

## Integration with CI/CD

The security scanner can be integrated into CI/CD pipelines:

```yaml
# GitHub Actions example
- name: DAPR Security Scan
  run: python scripts/security-scan.py components/ --fail-on critical
```

Exit codes:
- 0: No issues or only LOW severity
- 1: MEDIUM or higher issues found
- 2: CRITICAL issues found
