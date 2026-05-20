---
name: secrets-detection-rules
description: Эксперт по обнаружению секретов. Используй для создания правил детекции API keys, tokens и credentials в коде.
---

# Secrets Detection Rules Expert

Expert in pattern matching, regex optimization, false positive reduction, and comprehensive coverage for detecting sensitive credentials in source code.

## Core Principles

```yaml
detection_philosophy:
  precision_over_recall:
    principle: "Minimize false positives"
    reason: "Too many alerts = alert fatigue = ignored alerts"

  layered_detection:
    levels:
      - "High confidence: Known patterns"
      - "Medium confidence: Entropy + context"
      - "Low confidence: Heuristics"

  entropy_analysis:
    purpose: "Detect random strings that might be secrets"
    threshold: "Shannon entropy > 4.2"
    context: "Combined with naming patterns"

  contextual_validation:
    factors:
      - "Variable/key name"
      - "File location"
      - "Surrounding code"
      - "String format"
```

## Rule Categories

### AWS Credentials

```yaml
aws_rules:
  access_key_id:
    pattern: "AKIA[0-9A-Z]{16}"
    confidence: "high"
    description: "AWS Access Key ID"
    example: "AKIAIOSFODNN7EXAMPLE"

  secret_access_key:
    pattern: "[A-Za-z0-9/+=]{40}"
    context_required:
      - "aws_secret"
      - "secret_access_key"
      - "AWS_SECRET"
    confidence: "high"
    description: "AWS Secret Access Key"

  session_token:
    pattern: "FwoGZXIvYXdzE[A-Za-z0-9/+=]+"
    confidence: "high"
    description: "AWS Session Token"
```

### API Keys & Tokens

```yaml
api_key_rules:
  generic_api_key:
    patterns:
      - name: "api_key variable"
        regex: '(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?'
        confidence: "medium"

      - name: "bearer token"
        regex: '(?i)bearer\s+[a-zA-Z0-9_-]{20,}'
        confidence: "high"

      - name: "authorization header"
        regex: '(?i)authorization\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?'
        confidence: "medium"

  service_specific:
    github:
      patterns:
        - "ghp_[a-zA-Z0-9]{36}"  # Personal access token
        - "gho_[a-zA-Z0-9]{36}"  # OAuth access token
        - "ghu_[a-zA-Z0-9]{36}"  # User-to-server token
        - "ghs_[a-zA-Z0-9]{36}"  # Server-to-server token
      confidence: "high"

    slack:
      patterns:
        - "xoxb-[0-9]{10,}-[0-9]{10,}-[a-zA-Z0-9]{24}"  # Bot token
        - "xoxp-[0-9]{10,}-[0-9]{10,}-[a-zA-Z0-9]{24}"  # User token
        - "xoxa-[0-9]{10,}-[0-9]{10,}-[a-zA-Z0-9]{24}"  # App token
        - "xoxr-[0-9]{10,}-[0-9]{10,}-[a-zA-Z0-9]{24}"  # Refresh token
      confidence: "high"

    stripe:
      patterns:
        - "sk_live_[a-zA-Z0-9]{24,}"  # Live secret key
        - "sk_test_[a-zA-Z0-9]{24,}"  # Test secret key
        - "rk_live_[a-zA-Z0-9]{24,}"  # Restricted key
        - "pk_live_[a-zA-Z0-9]{24,}"  # Publishable key (lower risk)
      confidence: "high"

    google:
      patterns:
        - "AIza[0-9A-Za-z_-]{35}"  # API key
        - "[0-9]+-[a-z0-9_]{32}\\.apps\\.googleusercontent\\.com"  # OAuth client
      confidence: "high"

    twilio:
      patterns:
        - "SK[a-f0-9]{32}"  # API key
        - "AC[a-f0-9]{32}"  # Account SID
      confidence: "high"

    sendgrid:
      pattern: "SG\\.[a-zA-Z0-9_-]{22}\\.[a-zA-Z0-9_-]{43}"
      confidence: "high"

    mailchimp:
      pattern: "[a-f0-9]{32}-us[0-9]{1,2}"
      confidence: "high"
```

### Database Credentials

```yaml
database_rules:
  connection_strings:
    postgresql:
      pattern: 'postgres(?:ql)?://[^:]+:[^@]+@[^/]+/[^\s"\''`]+'
      confidence: "high"
      example: "postgresql://user:password@localhost:5432/db"

    mysql:
      pattern: 'mysql://[^:]+:[^@]+@[^/]+/[^\s"\''`]+'
      confidence: "high"

    mongodb:
      pattern: 'mongodb(?:\+srv)?://[^:]+:[^@]+@[^\s"\''`]+'
      confidence: "high"
      example: "mongodb+srv://user:pass@cluster.mongodb.net/db"

    redis:
      pattern: 'redis://[^:]*:[^@]+@[^\s"\''`]+'
      confidence: "high"

  password_patterns:
    variable_assignment:
      patterns:
        - '(?i)(password|passwd|pwd)\s*[:=]\s*["\''`]([^"\''`\s]{8,})["\''`]'
        - '(?i)db_pass(?:word)?\s*[:=]\s*["\''`]([^"\''`\s]{8,})["\''`]'
      exclude:
        - "password123"
        - "changeme"
        - "example"
        - "${.*}"
```

### Private Keys

```yaml
private_key_rules:
  rsa:
    pattern: "-----BEGIN RSA PRIVATE KEY-----"
    confidence: "high"
    multiline: true

  openssh:
    pattern: "-----BEGIN OPENSSH PRIVATE KEY-----"
    confidence: "high"
    multiline: true

  ec:
    pattern: "-----BEGIN EC PRIVATE KEY-----"
    confidence: "high"
    multiline: true

  pgp:
    pattern: "-----BEGIN PGP PRIVATE KEY BLOCK-----"
    confidence: "high"
    multiline: true

  generic:
    pattern: "-----BEGIN PRIVATE KEY-----"
    confidence: "high"
    multiline: true
```

### JWT Tokens

```yaml
jwt_rules:
  jwt_token:
    pattern: "eyJ[a-zA-Z0-9_-]*\\.eyJ[a-zA-Z0-9_-]*\\.[a-zA-Z0-9_-]*"
    confidence: "medium"
    validation:
      - "Decode header to verify structure"
      - "Check payload for sensitive claims"
      - "Verify not expired test token"

  jwt_context:
    high_confidence:
      - "In Authorization header"
      - "Named as 'token' or 'jwt'"
      - "In API response"
    low_confidence:
      - "In test files"
      - "In documentation"
      - "Expired payload"
```

## Entropy Analysis

```python
# Shannon entropy calculation
import math
from collections import Counter

def calculate_entropy(s: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0.0

    length = len(s)
    frequencies = Counter(s)

    entropy = 0.0
    for count in frequencies.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy

def is_high_entropy(s: str, threshold: float = 4.2) -> bool:
    """Check if string has high entropy (likely a secret)."""
    # Minimum length check
    if len(s) < 16:
        return False

    # Calculate entropy
    entropy = calculate_entropy(s)

    return entropy >= threshold

# Entropy thresholds by type
ENTROPY_THRESHOLDS = {
    "api_key": 4.2,
    "password": 3.5,
    "token": 4.5,
    "hash": 4.8
}
```

## False Positive Reduction

```yaml
whitelist_patterns:
  placeholders:
    patterns:
      - "YOUR_.*_HERE"
      - "REPLACE_.*"
      - "INSERT_.*"
      - "xxx+"
      - "\\*+"
      - "<.*>"
      - "\\$\\{.*\\}"
      - "\\{\\{.*\\}\\}"
    action: "ignore"

  test_values:
    patterns:
      - "test.*"
      - "fake.*"
      - "dummy.*"
      - "example.*"
      - "sample.*"
      - "mock.*"
    action: "ignore"

  common_false_positives:
    patterns:
      - "0{16,}"  # All zeros
      - "1{16,}"  # All ones
      - "abcd.*"  # Sequential
      - "password123"
      - "changeme"
      - "secret123"
    action: "ignore"

path_exclusions:
  directories:
    - "node_modules/"
    - "vendor/"
    - ".git/"
    - "__pycache__/"
    - "build/"
    - "dist/"
    - "coverage/"

  file_patterns:
    - "*.min.js"
    - "*.min.css"
    - "*.map"
    - "*.lock"
    - "package-lock.json"
    - "yarn.lock"

  documentation:
    - "*.md"
    - "*.rst"
    - "*.txt"
    - "docs/"
    - "examples/"

context_validation:
  safe_patterns:
    - "process.env.*"
    - "os.environ.*"
    - "System.getenv.*"
    - "ENV['.*']"
    - "config.get.*"

  suspicious_patterns:
    - "hardcoded"
    - "= \"[^\"]{20,}\""
    - "= '[^']{20,}'"
```

## Rule Configuration

```yaml
# .secrets-detection.yml
version: "1.0"

rules:
  - id: "aws-access-key"
    pattern: "AKIA[0-9A-Z]{16}"
    severity: "critical"
    enabled: true

  - id: "generic-api-key"
    pattern: '(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})["\']?'
    severity: "high"
    enabled: true
    entropy_check: true
    entropy_threshold: 4.2

  - id: "private-key"
    pattern: "-----BEGIN .* PRIVATE KEY-----"
    severity: "critical"
    enabled: true
    multiline: true

exclude:
  paths:
    - "test/"
    - "spec/"
    - "*.test.*"
    - "*.spec.*"
    - "fixtures/"
    - "mocks/"

  patterns:
    - "EXAMPLE_.*"
    - ".*_PLACEHOLDER"
    - "\\$\\{.*\\}"

report:
  format: "json"
  output: "secrets-report.json"
  fail_on: "critical"

performance:
  max_file_size: "10MB"
  timeout_per_file: "30s"
  parallel_files: 4
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/secrets-scan.yml
name: Secrets Detection

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Detect secrets
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Trufflehog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --only-verified

      - name: Upload results
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: secrets-report
          path: secrets-report.json
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
        name: Detect secrets
        entry: gitleaks protect --verbose --redact
        language: golang
        pass_filenames: false

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

## Performance Optimization

```yaml
optimization_strategies:
  regex:
    use_atomic_groups: true
    avoid_backtracking: true
    possessive_quantifiers: true
    example:
      bad: "(a+)+"
      good: "(?>a+)"

  scanning:
    progressive:
      - "Phase 1: High confidence patterns"
      - "Phase 2: Medium confidence + entropy"
      - "Phase 3: Low confidence heuristics"

    early_exit:
      - "Skip binary files"
      - "Skip files > 10MB"
      - "Skip whitelisted paths"

  caching:
    - "Cache compiled regexes"
    - "Cache file hashes"
    - "Incremental scanning"

resource_limits:
  max_file_size: "10MB"
  timeout_per_file: "30s"
  max_line_length: "10000"
  parallel_workers: 4
```

## Remediation

```yaml
remediation_steps:
  immediate:
    - "Revoke compromised credential"
    - "Rotate the secret"
    - "Remove from git history"
    - "Audit access logs"

  git_history_cleanup:
    commands:
      - "git filter-branch --force --index-filter"
      - "BFG Repo-Cleaner for large repos"
      - "git-filter-repo for complex cases"
    warning: "Requires force push, coordinate with team"

  prevention:
    - "Use environment variables"
    - "Use secrets management (Vault, AWS Secrets Manager)"
    - "Enable pre-commit hooks"
    - "Implement CI/CD scanning"
    - "Regular rotation schedule"
```

## Лучшие практики

1. **Precision over recall** — меньше ложных срабатываний
2. **Layered detection** — комбинируй паттерны и энтропию
3. **Context matters** — учитывай окружение и naming
4. **Whitelist carefully** — документируй исключения
5. **Scan early** — pre-commit hooks + CI/CD
6. **Rotate on detection** — compromised = revoked
