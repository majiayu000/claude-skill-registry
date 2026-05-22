---
name: secrets-hunter
description: Hunt for hardcoded secrets, API keys, tokens, credentials, private keys, and sensitive configuration. Use when auditing code for credential exposure or before committing code.
---

# Secrets Hunter

## Purpose

Find hardcoded secrets, API keys, tokens, passwords, private keys, and sensitive configuration that should not be in source code.

## Focus Areas

- **API Keys**: Cloud providers, third-party services
- **Passwords/Credentials**: Database passwords, admin credentials
- **Private Keys**: SSH, SSL/TLS, signing keys
- **Tokens**: JWT secrets, OAuth tokens, session secrets
- **Connection Strings**: Database URLs with credentials
- **Webhook Secrets**: GitHub, Stripe, payment processors

## High-Value Targets

### Cloud Provider Keys
```
AWS:           AKIA[0-9A-Z]{16}
GCP:           AIza[0-9A-Za-z\\-_]{35}
Azure:         [a-zA-Z0-9+/]{86}==
DigitalOcean:  dop_v1_[a-f0-9]{64}
```

### Service API Keys
```
Stripe:        sk_live_[0-9a-zA-Z]{24}
GitHub:        ghp_[0-9a-zA-Z]{36}
Slack:         xox[baprs]-[0-9a-zA-Z-]{10,}
SendGrid:      SG\.[a-zA-Z0-9]{22}\.[a-zA-Z0-9]{43}
Twilio:        SK[0-9a-fA-F]{32}
```

### Private Keys
```
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----
-----BEGIN EC PRIVATE KEY-----
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

### Common Patterns
```
password\s*[=:]\s*["'][^"']+["']
api_key\s*[=:]\s*["'][^"']+["']
secret\s*[=:]\s*["'][^"']+["']
token\s*[=:]\s*["'][^"']+["']
```

## Output Format

```yaml
findings:
  - title: "Hardcoded AWS Access Key in config"
    severity: critical
    attack_scenario: "Attacker uses exposed AWS key for unauthorized cloud access"
    preconditions: "Key must still be active"
    reachability: public  # If in public repo
    impact: "Full AWS account compromise, data breach, resource abuse"
    confidence: high
    cwe_id: "CWE-798"
    affected_assets:
      - "src/config/aws.rs:15"
      - "AKIAIOSFODNN7EXAMPLE"
```

## Search Locations

### High Priority Files
```
.env, .env.*, *.env
config.*, settings.*
docker-compose.yml
Dockerfile
*.properties
application.yml, application.yaml
secrets.*, credentials.*
```

### Code Patterns
```
const API_KEY = "..."
let password = "..."
"Authorization": "Bearer ..."
connection_string = "postgres://user:pass@..."
```

### Git History
```
# Secrets often removed but remain in history
git log -p --all -S 'password'
git log -p --all -S 'api_key'
```

## False Positive Indicators

```
- Example/placeholder values: "your-api-key-here", "xxx", "changeme"
- Test credentials: "test", "development", "localhost"
- Environment variable references: process.env.API_KEY, os.getenv()
- Documentation strings explaining format
```

## Severity Guidelines

| Secret Type | Severity |
|-------------|----------|
| Cloud provider keys (AWS, GCP) | Critical |
| Production database credentials | Critical |
| Private signing keys | Critical |
| Payment processor keys (Stripe live) | Critical |
| OAuth client secrets | High |
| API keys with write access | High |
| Read-only API keys | Medium |
| Internal service tokens | Medium |
| Test/development credentials | Low |

## KYCo Integration

Register secret exposure findings:

### 1. Check Active Project
```bash
kyco project list
```

### 2. Register Finding
```bash
kyco finding create \
  --title "Hardcoded AWS Access Key in config" \
  --project PROJECT_ID \
  --severity critical \
  --cwe CWE-798 \
  --attack-scenario "Attacker uses exposed AWS key for unauthorized cloud access" \
  --impact "Full AWS account compromise, data breach" \
  --assets "src/config/aws.rs:15"
```

### 3. Use TruffleHog/Gitleaks Integration
```bash
# Run trufflehog and export
trufflehog git file://. --json > trufflehog-results.json

# Run gitleaks
gitleaks detect --source . --report-path gitleaks-report.json

# Import into KYCo (manual conversion may be needed)
kyco finding import gitleaks-report.json --project PROJECT_ID
```

### Common CWE IDs for Secrets
- CWE-798: Use of Hard-coded Credentials
- CWE-321: Use of Hard-coded Cryptographic Key
- CWE-312: Cleartext Storage of Sensitive Information
- CWE-319: Cleartext Transmission of Sensitive Information
