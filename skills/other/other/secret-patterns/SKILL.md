---
name: secret-patterns
description: 30+ service-specific secret detection regex patterns, entropy-based detection, PEM/JWT/Base64 identification, and false positive filtering.
---

# Secret Detection Patterns

Patterns for finding leaked credentials in codebases, git history, and CI logs.

## AWS Credentials

```bash
# Access Key ID: always starts with AKIA (long-term) or ASIA (session)
AKIA[0-9A-Z]{16}
ASIA[0-9A-Z]{16}

# Secret Access Key: 40-char base64-ish string after aws_secret
aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}

# ripgrep one-liner
rg --no-heading -n '(AKIA|ASIA)[0-9A-Z]{16}' .
```

## GitHub Tokens

```bash
# Personal access tokens (classic and fine-grained)
ghp_[A-Za-z0-9]{36}
github_pat_[A-Za-z0-9_]{82}

# OAuth / app tokens
gho_[A-Za-z0-9]{36}
ghs_[A-Za-z0-9]{36}
ghu_[A-Za-z0-9]{36}
ghr_[A-Za-z0-9]{36}

rg --no-heading -n 'gh[pousr]_[A-Za-z0-9]{36}' .
```

## Stripe Keys

```bash
# Live secret (never commit)
sk_live_[A-Za-z0-9]{24,}

# Test secret (flag but lower severity)
sk_test_[A-Za-z0-9]{24,}

# Publishable keys (public, lower severity)
pk_live_[A-Za-z0-9]{24,}
pk_test_[A-Za-z0-9]{24,}

rg --no-heading -n 'sk_(live|test)_[A-Za-z0-9]{24,}' .
```

## OpenAI / Anthropic Keys

```bash
# OpenAI
sk-proj-[A-Za-z0-9\-_]{50,}
sk-[A-Za-z0-9]{48}

# Anthropic
sk-ant-[A-Za-z0-9\-_]{90,}

rg --no-heading -n '(sk-proj-|sk-ant-)' .
```

## JWT Tokens

```bash
# Three base64url segments separated by dots
eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+

# Decode header to verify (Python)
import base64, json
header = token.split('.')[0] + '=='
print(json.loads(base64.urlsafe_b64decode(header)))
```

## PEM Private Keys

```bash
# RSA, EC, OpenSSH private keys
-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----

rg --no-heading -n '\-\-\-\-\-BEGIN.+PRIVATE KEY' .

# Also catch generic PEM blocks
-----BEGIN CERTIFICATE-----
-----BEGIN PGP PRIVATE KEY BLOCK-----
```

## Slack Tokens

```bash
xoxb-[0-9]{11,}-[0-9]{11,}-[A-Za-z0-9]{24}   # Bot token
xoxp-[0-9]{11,}-[0-9]{11,}-[A-Za-z0-9]{32}   # User token
xoxe\.[A-Za-z0-9\-_]{80,}                      # Enterprise grid
xoxs-[A-Za-z0-9\-]{80,}                        # SCIM token

rg --no-heading -n 'xox[bpse][-.]' .
```

## Database Connection Strings

```bash
# PostgreSQL
postgres(ql)?://[^:]+:[^@]+@[^/]+/\S+
postgresql\+asyncpg://[^:]+:[^@]+@

# MongoDB
mongodb(\+srv)?://[^:]+:[^@]+@

# MySQL / MariaDB
mysql://[^:]+:[^@]+@

rg --no-heading -n '(postgres|mongodb|mysql)://\S+:\S+@' .
```

## NPM, SendGrid, Twilio, Mailgun

```bash
# NPM publish token
npm_[A-Za-z0-9]{36}

# SendGrid
SG\.[A-Za-z0-9\-_]{22}\.[A-Za-z0-9\-_]{43}

# Twilio account SID + auth token
AC[0-9a-f]{32}                           # Account SID
SK[0-9a-f]{32}                           # API Key SID

# Mailgun API key
key-[A-Za-z0-9]{32}

rg --no-heading -n '(npm_[A-Za-z0-9]{36}|SG\.[A-Za-z0-9_-]{22}\.)' .
```

## SSH Private Keys

```bash
-----BEGIN OPENSSH PRIVATE KEY-----
-----BEGIN RSA PRIVATE KEY-----
-----BEGIN EC PRIVATE KEY-----
-----BEGIN DSA PRIVATE KEY-----
```

## Google Service Account JSON

```typescript
// Detect the "type": "service_account" JSON pattern
rg --no-heading -n '"type"\s*:\s*"service_account"' .

// Or the private_key field
rg --no-heading -n '"private_key"\s*:\s*"-----BEGIN' .
```

## High-Entropy String Detection (Shannon Entropy)

```python
import math
from collections import Counter

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = Counter(s)
    length = len(s)
    return -sum((c / length) * math.log2(c / length) for c in freq.values())

def is_high_entropy_secret(value: str, threshold: float = 4.5) -> bool:
    # Ignore short strings and common words
    if len(value) < 20:
        return False
    return shannon_entropy(value) > threshold

# Example usage
candidates = [
    "AKIAIOSFODNN7EXAMPLE",          # entropy ~4.1 (low, example key)
    "wJalrXUtnFEMI/K7MDENG/bPxRfi",  # entropy ~4.7 (real secret)
    "my-password-123",               # entropy ~3.8 (low)
]
for c in candidates:
    print(f"{c[:20]}... entropy={shannon_entropy(c):.2f} secret={is_high_entropy_secret(c)}")
```

## False Positive Filtering Rules

```python
FALSE_POSITIVE_PATHS = [
    r'test[s]?/',
    r'__tests__/',
    r'spec/',
    r'fixtures/',
    r'examples/',
    r'docs/',
    r'\.md$',
    r'CHANGELOG',
    r'README',
]

FALSE_POSITIVE_VALUES = [
    'example',
    'placeholder',
    'your_key_here',
    'INSERT_KEY',
    'REPLACE_ME',
    'xxxx',
    '1234',
    'test',
    'dummy',
    'fake',
]

def is_false_positive(path: str, value: str) -> bool:
    import re
    for pattern in FALSE_POSITIVE_PATHS:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    lower = value.lower()
    return any(fp in lower for fp in FALSE_POSITIVE_VALUES)
```

## Pre-commit Hook Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.63.5
    hooks:
      - id: trufflehog
        entry: trufflehog git file://. --since-commit HEAD --only-verified --fail
```

```bash
# Manual scan of full git history
gitleaks detect --source . --log-opts="--all"

# TruffleHog targeted scan
trufflehog git https://github.com/org/repo --only-verified

# ripgrep composite scan (fast, no install)
rg --no-heading -n \
  '(AKIA|ASIA|ghp_|sk_live_|sk-proj-|sk-ant-|xoxb-|npm_|SG\.|-----BEGIN.+PRIVATE)' \
  --glob '!{node_modules,dist,.git}' .
```

**Key rule**: Any match outside `test/`, `docs/`, or `examples/` with entropy > 4.5 is a confirmed finding. Rotate immediately.
