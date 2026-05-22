---
name: vault
description: Encrypted secrets vault for AI coding agents. Store API keys, passwords, and tokens with `age` (public-key encryption) and `sops` (encrypted YAML secrets files). Never plaintext.
---

# vault

Keep your secrets encrypted. API keys, passwords, tokens -- locked in a vault that only you can open. Your AI agent gets secrets when it needs them, then forgets them.

**Script:** `./scripts/vault.sh`
**Setup:** `./scripts/setup.sh` (run once, takes 30 seconds)

---

## Setup

```bash
cd /path/to/skills/vault
./scripts/setup.sh
```

- **Claude Code:** copy this skill folder into `.claude/skills/vault/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, verification, troubleshooting), see [references/installation-guide.md](references/installation-guide.md).

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the vault skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Why this matters

Right now, your secrets probably live in a `.env` file. Plain text. Anyone who can see your files -- a colleague, a stolen laptop, a backup that leaks, an AI agent that goes rogue -- reads every secret you have.

This vault encrypts them. Even if someone copies your entire hard drive, they can't read your secrets without your encryption key. And your AI agent only sees secrets for the instant it needs them -- they never sit in memory or get written to a file.

**Before (plaintext .env):**
```text
OPENAI_API_KEY=sk-abc123-real-key-here     <- anyone can read this
DATABASE_URL=postgres://admin:password@...  <- sitting in plain text
STRIPE_SECRET=sk_live_...                   <- one leak away from disaster
```

**After (encrypted vault):**
```text
OPENAI_API_KEY: ENC[AES256_GCM,data:8f3k2...]   <- gibberish without your key
DATABASE_URL: ENC[AES256_GCM,data:j4m9x...]      <- encrypted at rest
STRIPE_SECRET: ENC[AES256_GCM,data:p2w7n...]     <- safe even if file leaks
```

The flow: `secret -> encrypt -> vault -> agent needs it -> decrypt to memory -> use -> forget`

---

## Quick Start

Three steps. That's it.

### 1. Run setup

```bash
cd path/to/this/skill
./scripts/setup.sh
```

This installs the encryption tools (if needed), creates your vault, and generates your encryption key. One command, done.

### 2. Add a secret

```bash
./scripts/vault.sh set MY_API_KEY "sk-your-actual-key"
```

### 3. Get it back

```bash
./scripts/vault.sh get MY_API_KEY
```

Your vault is working. Secrets are encrypted on disk, decrypted only when you ask for them.

---

## Commands

```bash
VAULT="./scripts/vault.sh"

# Store a secret
$VAULT set API_KEY "sk-abc123"

# Retrieve a secret (outputs to stdout, no trailing newline)
$VAULT get API_KEY

# List all secret names (not their values)
$VAULT list

# Export all secrets to your current shell
eval "$($VAULT source)"

# Run a command with secrets injected as env vars
$VAULT exec node server.js

# Check that vault works
$VAULT verify

# Full health check (tools, permissions, encryption test)
$VAULT doctor

# First-time setup
$VAULT setup

# Help for any command
$VAULT get --help
$VAULT set --help
$VAULT exec --help
$VAULT doctor --help
```

Every command has `--help`. When something goes wrong, error messages tell you what happened and what to do.

---

## For AI agents

This is the pattern for injecting secrets into AI agent workflows.

### Pattern 1: Variable assignment

```bash
# Agent needs one secret for a specific command
export TOKEN=$(./scripts/vault.sh get MY_API_KEY)
curl -H "Authorization: Bearer $TOKEN" https://api.example.com
unset TOKEN
```

### Pattern 2: Source all secrets

```bash
# Load everything into the current shell
eval "$(./scripts/vault.sh source)"
# Now all secrets are available as env vars
echo $MY_API_KEY  # available
echo $DATABASE_URL  # available
```

### Pattern 3: Scoped execution

```bash
# Run a command with secrets -- they don't leak to the parent shell
./scripts/vault.sh exec python my_script.py
# Secrets are gone after the command finishes
```

**Pattern 3 is the safest.** Secrets exist only for the duration of the command. They don't linger in your shell's environment. Prefer this when possible.

### Agent safety rules

- Never write secrets to files that get committed to git
- Never include secrets in prompts or logs
- Prefer `vault.sh exec` over `eval "$(vault.sh source)"` when possible
- After using `eval source`, clean up with `unset` for sensitive vars

---

## Configuration

All paths are configurable via environment variables:

| Variable | Default | What it controls |
|----------|---------|-----------------|
| `VAULT_DIR` | `~/.shit` | Where the vault lives |
| `VAULT_FILE` | `$VAULT_DIR/vault.enc.yaml` | The encrypted secrets file |
| `SOPS_AGE_KEY_FILE` | `$VAULT_DIR/.age-identity` | Your encryption key |

**Customize the vault path.** The default (`~/.shit`) is intentionally misleading -- it's an extra layer of obscurity on top of the real encryption. Pick something that makes sense for your setup. Some options:

```bash
# In your shell profile (~/.zshrc or ~/.bashrc):
export VAULT_DIR="$HOME/.config/vault"     # conventional
export VAULT_DIR="$HOME/.cache/.internal"   # hidden in cache
export VAULT_DIR="$HOME/.local/secrets"     # descriptive
```

Then re-run setup: `VAULT_DIR="$HOME/.config/vault" ./scripts/setup.sh`

---

## How it works (under the hood)

Two tools do the heavy lifting:

- **age** -- Modern encryption. Creates a key pair (public + private). Your secrets are encrypted with the public key and can only be decrypted with the private key. No passwords to remember.
- **sops** -- Wraps age to encrypt individual fields in a YAML file. Each secret value is encrypted separately, but key names stay visible (so you can see what's in the vault without decrypting).

The vault directory looks like this:

```text
~/.shit/                    chmod 700 (only you can access)
  .age-identity             Your encryption key (chmod 600)
  vault.enc.yaml            Your encrypted secrets
  .sops.yaml                Config telling sops which key to use
```

**Key security facts:**
- Secrets are encrypted with X25519 (the elliptic-curve key-exchange algorithm Signal uses)
- Decrypted values only exist in memory -- stdout, pipes, env vars
- Nothing writes plaintext to disk, ever
- The `vault.sh` script validates all input to prevent injection attacks
- File permissions are checked and auto-fixed on every operation

---

## What this protects against (and what it doesn't)

**Protected:**
- Casual file browsing (encrypted, not readable)
- Accidental git commits (encrypted file is safe to commit, though not recommended)
- Laptop theft (encrypted without the key is useless)
- AI agent data exfiltration (secrets aren't in plaintext files)
- Plaintext exposure in logs or backups

**NOT protected:**
- Someone with access to your logged-in user account (they can run vault.sh)
- Physical access to your unlocked computer
- Malware running as your user (it can read the key file)
- Key compromise (if someone gets `.age-identity`, they get everything)

**Bottom line:** This is dramatically better than `.env` files. It's not a replacement for a dedicated secrets manager in production infrastructure (use HashiCorp Vault, AWS Secrets Manager, etc. for that). It's for your development machine, your personal API keys, your local credentials.

---

## Error Handling

| Problem | Solution |
|---------|----------|
| `sops not found` | `brew install sops` (Mac) or see [sops install guide](https://github.com/getsops/sops#install) |
| `age not found` | `brew install age` (Mac) or see [age install guide](https://github.com/FiloSottile/age#installation) |
| `jq not found` | `brew install jq` (Mac) or `sudo apt install jq` (Linux) |
| `Age identity not found` | Run `./scripts/setup.sh` to create it |
| `Vault decrypted but no secrets found` | Normal for a fresh vault -- add a secret with `vault.sh set` |
| `Failed to set key` | Check that key name uses only letters, digits, and underscores |
| `Key not found` | Run `vault.sh list` to see available keys |
| `Permission denied` | Run `vault.sh doctor` to check and fix permissions |
| Everything broken | Run `vault.sh doctor` -- it checks everything and tells you what's wrong |

---

## Anti-Patterns

| Do NOT | Do instead |
|--------|------------|
| Store secrets in `.env` plaintext files | Store secrets with `./scripts/vault.sh set ...` |
| Leave secrets exported in shell for long sessions | Prefer `./scripts/vault.sh exec <command>` for scoped access |
| Print secrets to logs or command history | Use env vars and avoid echoing secret values |
| Commit decrypted outputs or temp files | Keep secrets encrypted at rest and out of git |
| Skip `vault.sh doctor` when setup fails | Run `vault.sh doctor` first, then fix reported issues |

---

## Bundled Resources Index

| Path | What | When to load |
|------|------|-------------|
| `./references/installation-guide.md` | Detailed install walkthrough for Claude Code and Codex CLI | First-time setup or environment repair |
| `./scripts/vault.sh` | Vault CLI -- the main interface | Always |
| `./scripts/setup.sh` | First-time setup script | Initial setup only |
