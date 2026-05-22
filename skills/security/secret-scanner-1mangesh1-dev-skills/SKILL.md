---
name: secret-scanner
description: This skill should be used when the user asks to "scan for secrets", "find API keys", "detect credentials", "check for hardcoded passwords", "find leaked tokens", "scan for sensitive keys", "check git history for secrets", "audit repository for credentials", or mentions secret detection, credential scanning, API key exposure, token leakage, password detection, or security key auditing.
license: MIT
metadata:
  author: 1mangesh1
  version: "1.0.0"
  tags:
    - security
    - secrets
    - credentials
    - api-keys
    - tokens
    - passwords
    - git-security
    - pre-commit
    - cicd
---

# Secret Scanner

A comprehensive secret detection skill for AI agents. Detects API keys, tokens, passwords, private keys, and credentials across 50+ services. Features entropy-based detection, git history scanning, and CI/CD integration.

## Capabilities

1. **Secret Detection** - Find hardcoded secrets using 200+ regex patterns
2. **Entropy Analysis** - Detect high-entropy strings that may be secrets
3. **Provider Coverage** - AWS, GCP, Azure, GitHub, Stripe, and 50+ more
4. **Git History Scan** - Scan entire commit history for leaked secrets
5. **File Type Support** - Code, configs, env files, JSON, YAML, and more
6. **Risk Scoring** - Score findings by severity and exposure context
7. **False Positive Filtering** - Smart exclusions for test data and examples
8. **Remediation Guidance** - Step-by-step secret rotation instructions
9. **CI/CD Integration** - Pre-commit hooks and GitHub Actions
10. **Allowlist Support** - Configure known-safe patterns to skip

## Usage

```
/secret-scanner [command] [path] [options]
```

### Commands

- `scan <path>` - Scan files or directories for secrets
- `scan-git <path>` - Scan git history for leaked secrets
- `audit <path>` - Full security audit with report generation
- `verify <secret>` - Check if a specific string matches secret patterns
- `providers` - List all supported secret providers
- `report` - Generate report from existing findings

### Options

- `--format <type>` - Output format: json, markdown, sarif (default: markdown)
- `--output <file>` - Write results to file
- `--severity <level>` - Minimum severity: low, medium, high, critical
- `--include <patterns>` - File patterns to include
- `--exclude <patterns>` - File patterns to exclude
- `--entropy <threshold>` - Entropy threshold (default: 4.5)
- `--no-entropy` - Disable entropy-based detection
- `--allowlist <file>` - Path to allowlist configuration
- `--git-depth <n>` - Number of commits to scan (default: all)

## Workflow

When invoked, follow this workflow:

### Step 1: Determine Scan Scope

Ask the user to specify:
- Target path (file, directory, or repository)
- Scan type (current files, git history, or both)
- Whether to include entropy-based detection

### Step 2: File Discovery

Use Glob to find relevant files:

```
# Source code
**/*.{py,js,ts,tsx,jsx,java,go,rb,php,cs,swift,kt,rs,c,cpp,h}

# Configuration
**/*.{env,json,yaml,yml,xml,toml,ini,conf,cfg,properties}

# Infrastructure
**/*.{tf,tfvars,hcl,dockerfile,docker-compose*}

# Shell scripts
**/*.{sh,bash,zsh,ps1,bat,cmd}

# Certificates and keys
**/*.{pem,key,p12,pfx,jks,keystore}
```

### Step 3: Pattern Matching

Apply detection patterns from `references/secret-patterns.md`:

#### Critical Severity
```python
# AWS Access Keys
AKIA[0-9A-Z]{16}

# AWS Secret Keys
(?i)aws.{0,20}['"][0-9a-zA-Z/+]{40}['"]

# GitHub Tokens
gh[pousr]_[A-Za-z0-9_]{36,255}

# Private Keys
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
```

#### High Severity
```python
# Generic API Keys
(?i)(api[_-]?key|apikey)['"]?\s*[:=]\s*['"][a-zA-Z0-9_\-]{20,}['"]

# Generic Tokens
(?i)(token|bearer|auth)['"]?\s*[:=]\s*['"][a-zA-Z0-9_\-\.]{20,}['"]

# Passwords
(?i)(password|passwd|pwd)['"]?\s*[:=]\s*['"][^'"]{8,}['"]
```

### Step 4: Entropy Analysis

For strings not matching known patterns, calculate Shannon entropy:

```python
def calculate_entropy(string):
    """Calculate Shannon entropy of a string."""
    from collections import Counter
    import math

    if not string:
        return 0

    counts = Counter(string)
    length = len(string)

    entropy = -sum(
        (count / length) * math.log2(count / length)
        for count in counts.values()
    )

    return entropy

# Flag strings with entropy > 4.5 and length >= 20
```

### Step 5: Context Analysis

For each potential secret:
1. Check surrounding context (variable names, comments)
2. Verify it's not in a test/example file
3. Check against allowlist
4. Determine exposure context (public repo, .env, etc.)

### Step 6: Calculate Risk Score

Apply formula from `references/risk-scoring.md`:

```
Risk = (Sensitivity × 0.40) + (Exposure × 0.30) +
       (Verifiability × 0.15) + (Scope × 0.15)
```

### Step 7: Generate Output

Format findings following `examples/sample-finding.json`:

```json
{
  "id": "S-20260204-0001",
  "file": "config/settings.py",
  "line": 42,
  "secret_type": "aws_access_key",
  "provider": "AWS",
  "value_preview": "AKIA...XXXX",
  "confidence": 0.98,
  "risk_score": 95,
  "severity": "critical",
  "context": "AWS_ACCESS_KEY = 'AKIA[REDACTED]'",
  "remediation": [...],
  "verified": false
}
```

## Supported Providers

### Cloud Providers

| Provider | Secret Types | Pattern Count |
|----------|--------------|---------------|
| AWS | Access Keys, Secret Keys, Session Tokens | 8 |
| GCP | API Keys, Service Account Keys, OAuth | 6 |
| Azure | Storage Keys, Connection Strings, SAS Tokens | 7 |
| DigitalOcean | API Tokens, Spaces Keys | 3 |
| Heroku | API Keys, OAuth Tokens | 2 |
| Alibaba Cloud | Access Keys, Secret Keys | 3 |

### Code Platforms

| Provider | Secret Types | Pattern Count |
|----------|--------------|---------------|
| GitHub | Personal Access Tokens, App Tokens, OAuth | 5 |
| GitLab | Personal Tokens, Pipeline Tokens, Runner Tokens | 4 |
| Bitbucket | App Passwords, OAuth, Repository Tokens | 3 |
| npm | Auth Tokens, Publish Tokens | 2 |
| PyPI | API Tokens | 1 |

### Payment Services

| Provider | Secret Types | Pattern Count |
|----------|--------------|---------------|
| Stripe | Secret Keys, Publishable Keys, Restricted Keys | 4 |
| PayPal | Client Secrets, Access Tokens | 2 |
| Square | Access Tokens, Application IDs | 2 |
| Braintree | Access Tokens, Merchant IDs | 2 |

### Communication Services

| Provider | Secret Types | Pattern Count |
|----------|--------------|---------------|
| Twilio | Account SID, Auth Token, API Key | 4 |
| SendGrid | API Keys | 2 |
| Mailchimp | API Keys | 1 |
| Slack | Bot Tokens, User Tokens, Webhooks | 4 |
| Discord | Bot Tokens, Webhooks | 2 |

### Database Services

| Provider | Secret Types | Pattern Count |
|----------|--------------|---------------|
| MongoDB | Connection Strings | 2 |
| PostgreSQL | Connection Strings | 2 |
| MySQL | Connection Strings | 2 |
| Redis | Connection Strings, Auth Tokens | 2 |

### Other Services

| Provider | Secret Types | Pattern Count |
|----------|--------------|---------------|
| OpenAI | API Keys | 2 |
| Anthropic | API Keys | 1 |
| Firebase | API Keys, Admin SDK Keys | 3 |
| Cloudflare | API Keys, API Tokens | 2 |
| Datadog | API Keys, App Keys | 2 |
| New Relic | License Keys, API Keys | 2 |
| Auth0 | Client Secrets, API Tokens | 2 |
| Okta | API Tokens | 1 |
| JWT | Tokens (signature analysis) | 1 |

Full pattern list: `references/secret-patterns.md`

## Git History Scanning

### Scan Modes

1. **Full History** - Scan all commits
2. **Depth Limited** - Scan last N commits
3. **Branch Specific** - Scan specific branch
4. **Diff Mode** - Only scan changed lines

### Usage

```bash
# Scan entire history
/secret-scanner scan-git ./repo

# Scan last 100 commits
/secret-scanner scan-git ./repo --git-depth 100

# Scan specific branch
/secret-scanner scan-git ./repo --branch feature/auth
```

### Git-Specific Findings

```json
{
  "commit": "abc123",
  "author": "developer@example.com",
  "date": "2026-01-15T10:30:00Z",
  "message": "Add API configuration",
  "file": "config.py",
  "secret_type": "stripe_secret_key",
  "still_present": false,
  "removed_in": "def456"
}
```

## Entropy-Based Detection

### How It Works

1. Extract string literals and values from files
2. Calculate Shannon entropy for each string
3. Flag high-entropy strings (> 4.5) that are:
   - At least 20 characters long
   - Contain mixed character classes
   - In security-sensitive contexts

### Entropy Thresholds

| Threshold | Detection Level | False Positive Rate |
|-----------|-----------------|---------------------|
| 3.5 | Aggressive | High |
| 4.0 | Moderate | Medium |
| 4.5 | Balanced (default) | Low |
| 5.0 | Conservative | Very Low |

### Context Boosting

Entropy findings are boosted if found in:
- Variable names containing: key, secret, token, password, auth
- Files: `.env`, `secrets.*`, `credentials.*`
- Config sections: `[credentials]`, `[auth]`

## False Positive Handling

### Built-in Exclusions

1. **Test Files** - `*_test.*`, `*_spec.*`, `test_*.*`, `__tests__/*`
2. **Example Files** - `example.*`, `sample.*`, `demo.*`
3. **Documentation** - `*.md`, `*.rst`, `docs/*`
4. **Mock Data** - Files containing "mock", "fake", "dummy"
5. **Known Safe Patterns**:
   - `AKIAIOSFODNN7EXAMPLE` (AWS example key)
   - `sk_test_*` (Stripe test keys)
   - `pk_test_*` (Stripe test publishable keys)
   - `xoxb-PLACEHOLDER-EXAMPLE-TOKEN` (Slack example)

### Allowlist Configuration

Create `.secret-scanner-allowlist.yaml`:

```yaml
# Allowlist configuration
patterns:
  # Regex patterns to ignore
  - "EXAMPLE_[A-Z_]+"
  - "test_api_key_\\d+"

paths:
  # Files/directories to skip
  - "test/"
  - "fixtures/"
  - "*.example"

hashes:
  # SHA256 hashes of known false positives
  - "abc123..."

comments:
  # Inline comments that suppress warnings
  - "# secret-scanner:ignore"
  - "// nosecret"
```

## Risk Scoring

### Severity Levels

| Score | Severity | Response | Examples |
|-------|----------|----------|----------|
| 90-100 | **Critical** | Immediate | AWS keys, private keys, prod DB passwords |
| 70-89 | **High** | Within 4 hours | API keys, OAuth tokens, service accounts |
| 50-69 | **Medium** | Within 24 hours | Test API keys, internal tokens |
| 25-49 | **Low** | Within 1 week | Entropy matches, partial credentials |
| 0-24 | **Info** | Review | Possible false positives |

### Factor Weights

- **Sensitivity (40%)**: Type of secret and potential damage
- **Exposure (30%)**: Where the secret was found
- **Verifiability (15%)**: Can the secret be validated as real
- **Scope (15%)**: Blast radius if exploited

Full methodology: `references/risk-scoring.md`

## Remediation Workflow

### Step 1: Immediate Actions

1. **Revoke the secret** - Invalidate immediately in provider console
2. **Rotate credentials** - Generate new secret
3. **Update applications** - Deploy new credentials
4. **Audit access logs** - Check for unauthorized usage

### Step 2: Clean Up

1. **Remove from code** - Delete the hardcoded secret
2. **Clean git history** - Use BFG or git filter-branch
3. **Force push** - Update all branches
4. **Invalidate caches** - Clear CI/CD caches

### Step 3: Prevention

1. **Add to .gitignore** - Prevent future commits
2. **Install pre-commit hook** - Block commits with secrets
3. **Use secrets manager** - AWS Secrets Manager, HashiCorp Vault
4. **Environment variables** - Store secrets in environment

Provider-specific instructions: `references/remediation.md`

## CI/CD Integration

### Pre-Commit Hook

```bash
# Install the pre-commit hook
cp scripts/pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Pre-commit Framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: secret-scanner
        name: Secret Scanner
        entry: python scripts/detect-secrets.py
        language: python
        types: [file]
        pass_filenames: true
```

### GitHub Actions

```yaml
# .github/workflows/secret-scan.yml
name: Secret Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git scanning
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run Secret Scan
        run: |
          python scripts/detect-secrets.py . --format sarif --output results.sarif
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: results.sarif
```

### Environment Variables

```bash
# Configure behavior
export SECRET_SCANNER_SEVERITY=high      # Minimum severity to report
export SECRET_SCANNER_ENTROPY=4.5        # Entropy threshold
export SECRET_SCANNER_BLOCK=true         # Block on findings
export SECRET_SCANNER_ALLOWLIST=.secret-scanner-allowlist.yaml
```

## Output Formats

### JSON (findings.json)

Structured array with all findings and metadata.

### Markdown (report.md)

Human-readable report with:
- Executive summary
- Findings by severity
- Provider breakdown
- Remediation checklist

### SARIF

Static Analysis Results Interchange Format for GitHub Security tab integration.

## Security Guardrails

1. **Never output full secrets** - Show only prefix/suffix with masking
2. **Secure temporary files** - Use scratchpad, clean up after
3. **No secret logging** - Redact from all log output
4. **Verification is optional** - Don't auto-verify against live APIs
5. **Respect allowlists** - Honor configured exclusions

## References

- `references/secret-patterns.md` - All detection patterns
- `references/provider-patterns.md` - Provider-specific patterns
- `references/entropy-detection.md` - Entropy analysis methodology
- `references/risk-scoring.md` - Risk scoring methodology
- `references/remediation.md` - Secret rotation guides
- `references/allowlist-config.md` - Allowlist configuration

## Examples

- `examples/sample-finding.json` - Example finding output
- `examples/sample-report.md` - Example audit report
- `examples/allowlist.yaml` - Example allowlist configuration

## Scripts

- `scripts/detect-secrets.py` - Main secret detection script
- `scripts/scan-git-history.py` - Git history scanner
- `scripts/entropy-analyzer.py` - Entropy-based detection
- `scripts/generate-report.py` - Report generation
- `scripts/pre-commit-hook.sh` - Git pre-commit hook
