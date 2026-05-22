# Secrets Scan

Deep detection of hardcoded credentials and sensitive data in source code.

---
description: Detect API keys, passwords, tokens, and other secrets in code
version: 1.0.0
tags: [security, secrets, credentials, api-keys]
---

## Quick Start

```
/secrets-scan                    # Scan current directory
/secrets-scan --scope src/       # Scan specific path
/secrets-scan --entropy          # Include high-entropy detection
/secrets-scan --git-history      # Check git commit history
```

## What This Skill Detects

### High-Confidence Patterns

Patterns with very low false positive rates:

| Type | Pattern Example | Provider |
|------|-----------------|----------|
| AWS Access Key | `AKIA...` (20 chars) | AWS |
| AWS Secret Key | 40 char base64 | AWS |
| GitHub Token | `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_` | GitHub |
| GitLab Token | `glpat-...` | GitLab |
| Slack Token | `xoxb-`, `xoxp-`, `xoxa-` | Slack |
| Stripe Key | `sk_live_`, `rk_live_` | Stripe |
| Twilio | `SK...` (34 chars) | Twilio |
| SendGrid | `SG.` followed by base64 | SendGrid |
| Private Key | `-----BEGIN (RSA\|EC\|DSA)?PRIVATE KEY-----` | Various |
| Google API Key | `AIza...` (39 chars) | Google |

### Medium-Confidence Patterns

May require context validation:

| Type | Pattern | Notes |
|------|---------|-------|
| Generic API Key | `api[_-]?key.*=.*['"][a-zA-Z0-9]{16,}` | Variable names |
| Generic Secret | `secret.*=.*['"][^'"]+` | Context needed |
| Password | `password.*=.*['"][^'"]+` | May be config |
| Connection String | `://[^:]+:[^@]+@` | DB credentials |
| Bearer Token | `Bearer [a-zA-Z0-9_-]+` | In headers/code |

### High-Entropy Detection

Finds potential secrets via entropy analysis:

```
/secrets-scan --entropy
```

Detects strings with high randomness that may be:
- Base64-encoded secrets
- Hex-encoded tokens
- Custom API key formats

## Detection Patterns

### Cloud Provider Keys

```regex
# AWS
AKIA[0-9A-Z]{16}                           # Access Key ID
[A-Za-z0-9/+=]{40}                         # Secret Access Key (context needed)

# Azure
[a-zA-Z0-9+/=]{88}                         # Storage Account Key

# GCP
AIza[0-9A-Za-z_-]{35}                      # API Key
[0-9]+-[a-z0-9]{32}\.apps\.googleusercontent\.com  # OAuth Client
```

### Version Control Tokens

```regex
# GitHub
gh[pousr]_[A-Za-z0-9]{36,}                 # Personal/OAuth/User/Repo/App
github_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59} # Fine-grained PAT

# GitLab
glpat-[A-Za-z0-9-_]{20,}                   # Personal Access Token

# Bitbucket
[a-zA-Z0-9]{24}                            # App Password (context needed)
```

### Payment & Finance

```regex
# Stripe
sk_live_[a-zA-Z0-9]{24,}                   # Secret Key
rk_live_[a-zA-Z0-9]{24,}                   # Restricted Key
pk_live_[a-zA-Z0-9]{24,}                   # Publishable Key

# Square
sq0[a-z]{3}-[A-Za-z0-9_-]{22,}            # Access Token

# PayPal
access_token\$[a-zA-Z0-9-_.]+             # OAuth Token
```

### Communication Services

```regex
# Slack
xox[bpas]-[0-9]{10,}-[a-zA-Z0-9]{24,}     # Bot/User/App Token

# Twilio
SK[a-f0-9]{32}                             # API Key SID
[a-f0-9]{32}                               # Auth Token (context)

# SendGrid
SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}  # API Key
```

### Database Connection Strings

```regex
# PostgreSQL/MySQL
(postgres|mysql|mariadb)://[^:]+:[^@]+@[^/]+/\w+

# MongoDB
mongodb(\+srv)?://[^:]+:[^@]+@

# Redis
redis://:[^@]+@
```

### Private Keys

```regex
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

### JWT & Session

```regex
eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+   # JWT
```

## Scan Options

### Basic Scan
```
/secrets-scan
```
Scans for high-confidence patterns only.

### With Entropy Analysis
```
/secrets-scan --entropy
```
Adds high-entropy string detection (more findings, some false positives).

### Specific Scope
```
/secrets-scan --scope src/api/
/secrets-scan --scope "*.ts"
```

### Git History Scan
```
/secrets-scan --git-history
/secrets-scan --git-history --since "2024-01-01"
```
Scans commit history for secrets that were committed and later removed.

### Exclude Patterns
```
/secrets-scan --exclude "*.test.ts" --exclude "fixtures/"
```

## Output Format

### Finding Report

```
SECRETS SCAN RESULTS
====================

High-Confidence Findings: 2
Medium-Confidence Findings: 5
Entropy Findings: 3

[!] CRITICAL: AWS Access Key
    File: src/config/aws.ts:15
    Pattern: AKIAIOSFODNN7EXAMPLE
    Action: Rotate immediately, check CloudTrail

[!] CRITICAL: GitHub Token
    File: .env.example:8
    Pattern: ghp_xxxx...xxxx (redacted)
    Action: Revoke token, remove from history

[H] HIGH: Database Password
    File: docker-compose.yml:23
    Pattern: password: supersecret
    Action: Use environment variable

[M] MEDIUM: Possible API Key
    File: src/services/api.ts:44
    Pattern: apiKey = "a1b2c3..."
    Context: May be test value
```

### Summary Statistics

```
Files scanned: 342
Patterns checked: 127
Time elapsed: 2.3s

By Severity:
  Critical: 2
  High: 5
  Medium: 8

By Type:
  Cloud credentials: 2
  API keys: 4
  Passwords: 3
  Private keys: 1
  Other: 5
```

## False Positive Handling

### Common False Positives

1. **Example/placeholder values**
   - `AKIAIOSFODNN7EXAMPLE` (AWS example)
   - `sk_test_...` (Stripe test key)
   - `your-api-key-here`

2. **Test fixtures**
   - Mock credentials in test files
   - Fixture data

3. **Documentation**
   - README examples
   - API documentation

### Ignore File

Create `.secrets-scan-ignore`:

```
# Ignore test fixtures
**/fixtures/**
**/__mocks__/**
*.test.ts
*.spec.js

# Ignore documentation
docs/**
*.md

# Ignore specific false positives
src/constants.ts:EXAMPLE_KEY

# Inline ignore comment
# secrets-scan-ignore: test fixture
```

### Inline Ignore

```javascript
// secrets-scan-ignore: example value
const EXAMPLE_KEY = "AKIAIOSFODNN7EXAMPLE";
```

## Remediation Steps

### When Secrets Are Found

1. **Immediate Actions**
   - Rotate the credential immediately
   - Check access logs for unauthorized use
   - Remove from code/config

2. **Clean Git History**
   ```bash
   # Remove secret from history
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/file' \
     --prune-empty --tag-name-filter cat -- --all

   # Or use BFG Repo Cleaner
   bfg --replace-text secrets.txt repo.git
   ```

3. **Prevent Future Commits**
   - Add pre-commit hooks
   - Configure secret scanning in CI

### Prevention

```bash
# Install pre-commit hook
npx husky add .husky/pre-commit "npx secrets-scan --staged"
```

## Integration

### CI/CD Pipeline

```yaml
# GitHub Actions
- name: Secrets Scan
  run: |
    /secrets-scan --fail-on-findings
    exit $?

# Exit codes:
# 0 = No findings
# 1 = Findings detected
# 2 = Error during scan
```

### Pre-Commit Hook

```bash
#!/bin/sh
# .husky/pre-commit
files=$(git diff --cached --name-only)
/secrets-scan --files "$files"
```

## Related Skills

- `/security-scan` - Full security analysis
- `/config-scan` - Configuration security
- `/dependency-scan` - Package vulnerabilities
