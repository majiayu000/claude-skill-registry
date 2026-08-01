---
name: 1password-direnv-secrets
description: 'Configures 1Password CLI with direnv for fast secret loading using op-run
  pattern. Activates for: 1Password + direnv setup, slow secrets (>2 sec), environment
  variables from 1Password, .env.op files,'
---

---
name: 1password-direnv-secrets
description: Configures 1Password CLI with direnv for fast secret loading using op-run pattern. Activates for: 1Password + direnv setup, slow secrets (>2 sec), environment variables from 1Password, .env.op files, op:// references, or migrating from multiple op-read calls to single op-run.
---

# 1Password + direnv Secret Management

## Core Pattern

**Use `op run --env-file` NOT multiple `op read` calls.**

| Approach           | CLI Invocations | Load Time  |
| ------------------ | --------------- | ---------- |
| Multiple `op read` | N per secret    | ~5 seconds |
| Single `op run`    | 1               | ~1 second  |

## Prerequisites

```bash
brew install --cask 1password-cli && brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
op signin --account=yourcompany.1password.com
```

## Implementation

**1. `.env.op`** (commit this - op:// refs are NOT secrets):

```bash
AWS_ACCESS_KEY_ID="op://Vault/Item/AWS Access Key ID"
AWS_SECRET_ACCESS_KEY="op://Vault/Item/AWS Secret Access Key"
DB_PASSWORD="op://Vault/Item/Database Password"
DB_PORT="3306"  # Static values work too
```

**2. `.envrc`** (gitignored):

```bash
direnv_load op run --env-file=.env.op --no-masking \
  --account=yourcompany.1password.com -- direnv dump
```

**3. `.gitignore`**: Add `.envrc` and `.direnv/`

**4. Enable**: `direnv allow`

## Global Helper (Optional)

Add to `~/.config/direnv/direnvrc`:

```bash
use_1password() {
  local env_file="${1:-.env.op}" account="${2:-yourcompany.1password.com}"
  [[ -f "$env_file" ]] && direnv_load op run --env-file="$env_file" \
    --no-masking --account="$account" -- direnv dump
}
```

Then `.envrc` becomes: `use 1password`

## What's Safe to Commit?

| File      | Safe? | Why                             |
| --------- | ----- | ------------------------------- |
| `.env.op` | Yes   | Contains only `op://` pointers  |
| `.envrc`  | No    | Has account name (gitignore it) |
| `.env`    | Never | Contains actual secrets         |

**Secret lifecycle**: 1Password (encrypted) → resolved on-demand → memory only → cleared on exit

## Troubleshooting

| Error                             | Fix                                       |
| --------------------------------- | ----------------------------------------- |
| `op: command not found`           | `brew install --cask 1password-cli`       |
| `direnv: error .envrc is blocked` | `direnv allow`                            |
| `could not find item`             | Check vault/item names match exactly      |
| Secrets not loading               | Test: `op read "op://Vault/Item/Field"`   |
| Slow loading (>2 sec)             | Ensure using `op run`, not multiple reads |

## Alternative: `op inject` (Single File)

```bash
# .envrc - no separate .env.op needed
export AWS_KEY="op://Vault/Item/Field"
source <(printenv | grep "op://" | op inject --account=yourcompany.1password.com)
```

Simpler but refs briefly visible in env before resolution.
