<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: implementing-secret-detection
description: >-
  Detect and prevent secrets in source code using Gitleaks, TruffleHog, and
  detect-secrets. Configure pre-commit hooks, CI/CD scanning, and git history
  auditing to catch leaked credentials before they reach production.
domain: cybersecurity
subdomain: devsecops
tags:
  - secrets-detection
  - gitleaks
  - trufflehog
  - pre-commit
  - credential-leak
  - git-security
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1552.001"]
---

# Implementing Secret Detection

## Overview

Secrets leaked in source code are a leading cause of breaches. API keys, passwords,
tokens, and private keys committed to repositories remain in git history even after
deletion. This skill covers prevention (pre-commit hooks), detection (CI scanning),
and remediation (history rewriting, credential rotation).

Mode: `[MODE: BLUE]` — Preventive credential leak detection.

## Prerequisites

| Requirement | Details |
|---|---|
| Gitleaks v8+ (`brew install gitleaks` or Docker) | Required |
| TruffleHog v3+ (`brew install trufflehog`) | Required |
| pre-commit framework (`pip install pre-commit`) | Required |
| Git repository with full history access | Required |

## Key Concepts

### Pre-commit Hook Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

```bash
# Install hooks
pre-commit install

# Run against all files
pre-commit run gitleaks --all-files
```

### Gitleaks Configuration

```toml
# .gitleaks.toml
[allowlist]
  description = "Project allowlist"
  paths = [
    '''gitleaks\.toml''',
    '''(.*?)\.test\..*''',
    '''fixtures/''',
  ]

[[rules]]
  id = "custom-api-key"
  description = "Custom API key pattern"
  regex = '''(?i)my_service_api_key\s*=\s*['"][a-z0-9]{32}['"]'''
  tags = ["api-key", "custom"]

[rules.allowlist]
  commits = ["abc123def456"]
```

### Gitleaks in GitHub Actions

```yaml
name: Secret Detection
on: [pull_request, push]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
```

### TruffleHog Deep Scan

```bash
# Scan repo history for verified secrets
trufflehog git file://. --only-verified --json > trufflehog-results.json

# Scan GitHub org
trufflehog github --org=my-org --only-verified --json

# Scan specific branch
trufflehog git file://. --branch main --only-verified --json

# Scan S3 bucket
trufflehog s3 --bucket=my-bucket --only-verified --json
```

### Gitleaks Full History Scan

```bash
# Scan entire git history
gitleaks detect --source . --verbose --report-format json --report-path gitleaks-report.json

# Scan only staged changes
gitleaks protect --staged --verbose

# Scan specific commit range
gitleaks detect --source . --log-opts="--since='2024-01-01'" --report-format json
```

### Remediation When Secrets Found

```bash
# 1. ROTATE the credential IMMEDIATELY — this is step zero
# 2. Remove from git history using BFG
bfg --replace-text passwords.txt repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 3. Or use git-filter-repo
git filter-repo --invert-paths --path secrets.env

# 4. Force push cleaned history
git push --force --all
git push --force --tags

# 5. Update .gitignore and allowlist after rotation
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
```

## Workflow

### Step 1: Scan Repository

```bash
node scripts/agent.js --action scan --repo-dir . --output /tmp/secrets-scan.json
```

### Step 2: Scan Git History

```bash
node scripts/agent.js --action history --repo-dir . --output /tmp/secrets-history.json
```

### Step 3: Verify Pre-commit Hooks

```bash
node scripts/agent.js --action verify-hooks --repo-dir . --output /tmp/hooks-status.json
```

## Detection

```yaml
title: Secret Detection Detection
id: 16b0aaf2-9904-47d4-a626-bbf51fa44b44
status: experimental
description: Detects suspicious activity related to implementing secret detection techniques in devsecops context
logsource:
  category: process_creation
  product: linux
detection:
  selection:
    CommandLine: "*implementing*secret*"
  condition: selection
level: medium
tags:
  - attack.t1552.001
  - attack.execution
falsepositives:
  - CI/CD pipeline executing authorized security scanning tools
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Secret Detection Detection | linux/process_creation | Sigma rule (medium) |
| ATT&CK Coverage | MITRE ATT&CK | T1552.001 |

## Verification

- [ ] Pre-commit hooks installed and running gitleaks
- [ ] CI pipeline scans every PR for secrets
- [ ] Full git history scanned with no active secrets
- [ ] .gitleaks.toml configured with project-specific allowlist
- [ ] Remediation runbook documented (rotate → remove → prevent)
- [ ] TruffleHog verification mode confirms no verified secrets
- [ ] .secrets.baseline maintained and reviewed

## References

- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [TruffleHog Documentation](https://github.com/trufflesecurity/trufflehog)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
