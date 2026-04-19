---
name: secret-scanner
description: "Pre-push API key and credential scanner - blocks git push if secrets found"
version: 1.0.0
category: security
tags: [secrets, api-keys, pre-push, git-hooks, security]
---

# Secret Scanner

Scans your codebase for leaked API keys, tokens, and credentials. Blocks git push if secrets are found.

## Usage

```bash
# Scan current directory
vibeco secrets

# Scan specific path
vibeco secrets /path/to/project
```

## Detected Secrets (22 patterns)

| Provider | Pattern | Example |
|----------|---------|---------|
| OpenAI | `sk-proj-...`, `sk-...` | `sk-proj-abc123...` |
| Anthropic | `sk-ant-...` | `sk-ant-api03-...` |
| AWS | `AKIA...` | `AKIAIOSFODNN7EXAMPLE` |
| GitHub | `ghp_...`, `gho_...`, `github_pat_...` | `ghp_xxxxxxxxxxxx` |
| Stripe | `sk_live_...`, `pk_live_...` | `sk_live_4eC39H...` |
| Google | `AIza...` | `AIzaSyDaGm...` |
| Slack | `xoxb-...`, `xoxp-...` | `xoxb-123-456-abc` |
| SendGrid | `SG....` | `SG.xxx.yyy` |
| npm | `npm_...` | `npm_xxxxxxxxxxxxx` |
| PyPI | `pypi-...` | `pypi-AgEIcHl...` |
| Database URLs | `postgres://`, `mongodb://`, `mysql://`, `redis://` | With embedded passwords |
| Private Keys | `PRIVATE KEY-----` | PEM format |

## Auto-Setup: Git Pre-Push Hook

Add to your project's `.git/hooks/pre-push`:

```bash
#!/bin/bash
vibeco secrets "$(git rev-parse --show-toplevel)" || exit 1
```

Make it executable:
```bash
chmod +x .git/hooks/pre-push
```

Now every `git push` will scan for secrets first. If any are found, push is blocked.

## How It Works

1. Walks all source files (skips node_modules, dist, .git, lock files)
2. Matches 22 regex patterns for known API key formats
3. Skips comments and regex definition lines (avoids false positives)
4. If secrets found: prints masked values, exits with code 1 (blocks push)
5. If clean: prints success, exits with code 0

## What to Do If Secrets Are Found

1. **Remove** the secret from source code
2. **Move** to `.env` file (add `.env` to `.gitignore`)
3. **Use** environment variables: `process.env.API_KEY`
4. **If already pushed**: rotate the credential immediately (it's compromised)

## Scanned File Types

`.ts .tsx .js .jsx .mjs .cjs .py .go .java .rb .php .rs .swift .kt .json .yml .yaml .toml .env .cfg .conf .ini .sh .bash .zsh .xml .properties .gradle`
