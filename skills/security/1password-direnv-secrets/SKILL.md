---
name: 1password-direnv-secrets
description: Configures 1Password CLI with direnv for fast, secure credential loading. Activates for: 1Password + direnv setup, slow secrets (>2 sec), .env.op files, op:// references, AWS credentials via env vars, --reveal flag issues, repeated biometric prompts, creating 1Password items programmatically, op item get errors. Not for: 1Password GUI usage, SSH keys (use 1Password SSH agent).
---

# 1Password CLI Secret Management

Secure credential management using 1Password CLI with zero plaintext secrets on disk.

## Quick Reference

| Use Case                    | Approach              | Details                                                           |
|-----------------------------|-----------------------|-------------------------------------------------------------------|
| All secrets (AWS, DB, APIs) | direnv + `op run`     | [Core Pattern](#core-pattern-direnv--op-run)                      |
| CI/CD automation            | Service account token | [Session Management](references/session-management.md)            |
| Creating items for users    | `op item create`      | [Programmatic Creation](references/programmatic-item-creation.md) |

**Key insight:** Secrets load once on `cd` and all subprocesses inherit them (standard Unix `fork()` behavior). One `op` call, no re-fetching.

---

## Core Pattern: direnv + op run

**Use `op run --env-file` NOT multiple `op read` calls.**

| Approach           | CLI Invocations | Load Time  |
|--------------------|-----------------|------------|
| Multiple `op read` | N per secret    | ~5 seconds |
| Single `op run`    | 1               | ~1 second  |

### Setup

**1. `.env.op`** (safe to commit - contains only `op://` references):

```bash
AWS_ACCESS_KEY_ID="op://Vault/Item/Access Key ID"
AWS_SECRET_ACCESS_KEY="op://Vault/Item/Secret Access Key"
DB_PASSWORD="op://Vault/Item/password"
```

**2. `.envrc`** (safe to commit - no secrets, just loader command):

```bash
direnv_load op run --env-file=.env.op --no-masking \
  --account=yourcompany.1password.com -- direnv dump
```

**3. Enable:** `direnv allow`

### Global Helper

Add to `~/.config/direnv/direnvrc`:

```bash
use_1password() {
  local env_file="${1:-.env.op}" account="${2:-yourcompany.1password.com}"
  [[ -f "$env_file" ]] && direnv_load op run --env-file="$env_file" \
    --no-masking --account="$account" -- direnv dump
}
```

Then `.envrc` becomes: `use 1password`

---

## Critical: The --reveal Flag

**Concealed fields require `--reveal` to get actual values.**

```bash
# WRONG - returns placeholder text, NOT the secret!
op item get "Item" --fields "Secret Access Key"
# Output: [use 'op item get xxx --reveal' to reveal]

# CORRECT - returns actual secret value
op item get "Item" --fields "Secret Access Key" --reveal
```

**Common symptom:** `SignatureDoesNotMatch` errors from AWS indicate the secret wasn't retrieved properly.

---

## Reducing Biometric Prompts

| Scenario             | Solution                   | Prompts              |
|----------------------|----------------------------|----------------------|
| Dev entering project | direnv + `op run`          | 1 on directory entry |
| CI/CD pipeline       | `OP_SERVICE_ACCOUNT_TOKEN` | 0                    |

**Key insight:** Sessions last 10 minutes with auto-refresh on each use. Keep 1Password desktop app unlocked and integrated with CLI.

> **Detailed strategies:** [references/session-management.md](references/session-management.md)

---

## Discovery Commands

```bash
op account list                                    # Find accounts
op vault list --account mycompany.1password.com    # Find vaults
op item list --account mycompany.1password.com     # Find items
```

> **Full reference:** [references/discovery-commands.md](references/discovery-commands.md) - field inspection, search patterns, debugging

---

## Creating Items Programmatically

For Claude Code workflows where Claude sets up infrastructure without handling raw secrets:

```bash
# Create item with placeholder values
op item create --category "API Credential" \
  --title "AWS Service-Name" \
  --vault "Private" \
  --account mycompany.1password.com \
  "Access Key ID[text]=REPLACE_ME" \
  "Secret Access Key[concealed]=REPLACE_ME"
```

User populates via 1Password app, then Claude continues with configuration.

> **Full pattern:** [references/programmatic-item-creation.md](references/programmatic-item-creation.md)

---

## What's Safe to Commit?

| File      | Safe? | Why                                                    |
|-----------|-------|--------------------------------------------------------|
| `.env.op` | Yes   | Contains only `op://` pointers                         |
| `.envrc`  | Yes   | No secrets - just loader command delegating to .env.op |
| `.env`    | Never | Contains actual secrets                                |

> The account name (e.g., `yourcompany.1password.com`) isn't sensitive - it's just an identifier. For team projects, everyone uses the same account anyway.

---

## Troubleshooting

| Error                         | Fix                                         |
|-------------------------------|---------------------------------------------|
| `SignatureDoesNotMatch` (AWS) | Add `--reveal` for concealed fields         |
| `op: command not found`       | `brew install --cask 1password-cli`         |
| `could not find item`         | Names are case-sensitive; verify exact name |

> **Full troubleshooting:** [references/session-management.md#troubleshooting-excessive-prompts](references/session-management.md#troubleshooting-excessive-prompts)

---

## Prerequisites

```bash
# Install 1Password CLI (v2.18.0+ for service accounts)
brew install --cask 1password-cli

# Install direnv (for env var approach)
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# Sign in and integrate with desktop app
op signin --account=yourcompany.1password.com

# Verify integration
op whoami
```

**Required:** 1Password desktop app with CLI integration enabled (Settings → Developer → CLI Integration).

---

## Detailed References

- [Session Management](references/session-management.md) - Minimizing prompts, service accounts, CI/CD
- [Discovery Commands](references/discovery-commands.md) - Finding accounts, vaults, items, fields
- [Programmatic Item Creation](references/programmatic-item-creation.md) - Claude Code workflow patterns
