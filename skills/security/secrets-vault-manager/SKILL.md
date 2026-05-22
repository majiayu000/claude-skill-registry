---
name: secrets-vault-manager
description: "Handle SOPS + Age secrets for ONE_SHOT projects. Manages encrypted secrets, decryption, and secret rotation. Use when user mentions 'secrets', 'API keys', 'environment variables', '.env', or 'SOPS'."
allowed-tools: Bash, Read, Write, Edit
---

# Secrets Vault Manager

You are an expert at managing secrets with SOPS + Age encryption.

## When To Use

- Project needs API keys / secrets
- User mentions "Set up secrets-vault"
- User asks to "Decrypt / refresh secrets"
- User wants to "Add a new secret"

## Philosophy

One Age key in 1Password → ALL secrets.

## Setup (One-Time)

```bash
# Install
sudo apt install age sops  # Ubuntu
brew install age sops      # Mac

# Generate key
mkdir -p ~/.age
age-keygen -o ~/.age/key.txt
# Save public key (age1...) to 1Password

# Secrets are in the oneshot repo
# If not cloned: git clone git@github.com:Khamel83/oneshot.git ~/github/oneshot
```

## Create .sops.yaml

```yaml
creation_rules:
  - path_regex: .*\.encrypted$
    age: 'age1your_public_key_here'
```

## Daily Usage

```bash
# Decrypt to project
sops --decrypt ~/github/oneshot/secrets/secrets.env.encrypted > .env
source .env

# Update secrets
sops ~/github/oneshot/secrets/secrets.env.encrypted
# Edit, save, auto-encrypted
cd ~/github/oneshot && git add . && git commit -m "Update secrets" && git push
```

## Common Operations

### Decrypt for Local Use

```bash
sops --decrypt ~/github/oneshot/secrets/secrets.env.encrypted > .env
```

Verify `.env` is gitignored!

### Add New Secret

```bash
sops ~/github/oneshot/secrets/secrets.env.encrypted
# Add: NEW_SECRET=value
# Save and exit
cd ~/github/oneshot && git add . && git commit -m "Add NEW_SECRET" && git push
```

### Refresh Secrets

```bash
sops --decrypt ~/github/oneshot/secrets/secrets.env.encrypted > .env
```

### Per-Project SOPS (Alternative)

If not using central vault:

```bash
mkdir -p .sops
age-keygen -o .sops/key.txt

cat > .sops.yaml << 'EOF'
creation_rules:
  - path_regex: \.encrypted$
    age: 'age1your_key'
EOF

sops secrets.env.encrypted
sops --decrypt secrets.env.encrypted > .env
```

## .gitignore Template

```gitignore
# Secrets (NEVER commit)
.env
.env.local
secrets.env
*.key
key.txt
.age/

# Allow examples
!.env.example

# SOPS encrypted ARE safe
!*.encrypted
```

## Document in README

Add to project README:

```markdown
## Secrets

This project uses SOPS + Age for secrets management.

\`\`\`bash
# Decrypt secrets (requires Age key)
sops --decrypt ~/github/oneshot/secrets/secrets.env.encrypted > .env
source .env
\`\`\`
```

## Outputs

- `.env` created or refreshed (gitignored)
- Documentation updated: README "Secrets" section
- `secrets.env.encrypted` updated in vault when adding new secrets

## Anti-Patterns

- Ever committing `.env` or raw secrets
- Decrypting into tracked files
- Sharing Age private key outside 1Password
- Storing secrets in code or comments

## Related Skills

- `secrets-sync`: Two-way sync between vault and projects, namespacing, project labels

## Keywords

secrets, API keys, environment variables, .env, SOPS, Age, encrypt, decrypt, vault
