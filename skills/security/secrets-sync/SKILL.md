---
name: secrets-sync
description: "Two-way secret synchronization between master vault and projects. Detects new secrets, namespaces by project, and handles SOPS re-encryption. Use when user says 'sync secrets', 'pull secrets', 'push secrets', or 'secrets diff'."
allowed-tools: Bash, Read, Write, Edit
---

# Secrets Sync

You are an expert at synchronizing secrets between the central vault and project environments.

## When To Use

- User says "sync secrets" or "secrets sync"
- User says "pull secrets" (vault -> project)
- User says "push secrets" (project -> vault)
- User asks "what secrets am I missing?"
- User asks "secrets diff" or "compare secrets"

## Philosophy

- **Central vault is truth**: `~/github/oneshot/secrets/`
- **Projects consume**: Decrypt what they need
- **Namespacing prevents collision**: `PROJECT_KEY` format
- **Labels track origin**: SOPS comments show source

## Prerequisites

```bash
# Required
~/.age/key.txt              # Age private key
~/github/oneshot/secrets/   # Central vault
sops                        # SOPS CLI installed

# In project
.env or .env.example        # Project secrets source
```

## Workflows

### 1. Secrets Diff (Default)

Show what's different between project and vault:

```bash
# Extract project keys
grep -E '^[A-Z_][A-Z0-9_]*=' .env 2>/dev/null | cut -d= -f1 | sort > /tmp/project_keys.txt

# Extract vault keys (all encrypted files)
for file in ~/github/oneshot/secrets/*.encrypted; do
  sops -d "$file" 2>/dev/null | grep -E '^[A-Z_][A-Z0-9_]*=' | cut -d= -f1
done | sort | uniq > /tmp/vault_keys.txt

# Compare
echo "=== In Project, NOT in Vault (push candidates) ==="
comm -23 /tmp/project_keys.txt /tmp/vault_keys.txt

echo "=== In Vault, NOT in Project (pull candidates) ==="
comm -13 /tmp/project_keys.txt /tmp/vault_keys.txt

# Cleanup
rm -f /tmp/project_keys.txt /tmp/vault_keys.txt
```

### 2. Pull Secrets (Vault -> Project)

```bash
# Pull specific key from vault
sops -d ~/github/oneshot/secrets/secrets.env.encrypted | grep "^KEY_NAME=" >> .env

# Pull all matching project namespace
PROJECT=$(basename $(pwd) | tr '[:lower:]' '[:upper:]' | tr -d '-')
sops -d ~/github/oneshot/secrets/secrets.env.encrypted | grep "^${PROJECT}_" >> .env
```

### 3. Push Secrets (Project -> Vault)

This is the key workflow for two-way sync:

```bash
# 1. Detect project info
PROJECT_NAME=$(basename $(pwd) | tr '[:upper:]' '[:lower:]' | tr -d '-')
DATE=$(date +%Y-%m-%d)

# 2. Identify new secrets to push
# (secrets in .env not in vault)

# 3. For each new secret, namespace it
ORIGINAL_KEY="API_KEY"
ORIGINAL_VALUE="the_actual_value"
NAMESPACED_KEY="${PROJECT_NAME^^}_${ORIGINAL_KEY}"

# 4. Add to vault with label
# Open vault for editing:
sops ~/github/oneshot/secrets/secrets.env.encrypted

# In editor, add at appropriate location:
# [PROJECT:projectname] added YYYY-MM-DD by secrets-sync
# PROJECTNAME_API_KEY=value

# 5. Commit vault changes
cd ~/github/oneshot && git add secrets/ && \
  git commit -m "feat(secrets): add ${NAMESPACED_KEY} from ${PROJECT_NAME} sync"
```

## Label Format

All synced secrets MUST have a comment label on the line above:

```
# [PROJECT:projectname] added YYYY-MM-DD by secrets-sync
PROJECTNAME_KEY=value
```

Components:
- `PROJECT:name` - Lowercase project directory name
- `added YYYY-MM-DD` - Date secret was added
- `by secrets-sync` - Source attribution

## Namespace Convention

| Original | Project | Namespaced Result |
|----------|---------|-------------------|
| API_KEY | atlas | ATLAS_API_KEY |
| DB_PASSWORD | homelab | HOMELAB_DB_PASSWORD |
| SECRET | my-app | MYAPP_SECRET |

Rules:
1. Uppercase project name
2. Remove hyphens (my-app -> MYAPP)
3. Underscore separator
4. Original key appended

Skip namespacing if key already has project prefix.

## Sync Report Format

After sync operations, generate this report:

```markdown
## Secrets Sync Report

**Project**: myproject | **Date**: 2025-12-14
**Vault**: ~/github/oneshot/secrets/

### Pushed to Vault
| Key | Vault File | Status |
|-----|------------|--------|
| MYPROJECT_API_KEY | secrets.env.encrypted | Added |
| MYPROJECT_DB_URL | secrets.env.encrypted | Added |

### Available to Pull
| Key | Source File |
|-----|-------------|
| OPENROUTER_API_KEY | secrets.env.encrypted |
| CLOUDFLARE_API_TOKEN | homelab.env.encrypted |

### Conflicts (Manual Review Required)
| Key | Issue | Resolution |
|-----|-------|------------|
| API_KEY | Exists in both with different values | Namespace as MYPROJECT_API_KEY |

### Next Steps
1. Verify .env has correct values
2. Commit vault changes in oneshot repo
3. git push to sync with remote
```

## Vault Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `secrets.env.encrypted` | General API keys, DB creds | Default for most projects |
| `homelab.env.encrypted` | Homelab infrastructure | Docker/Traefik/NAS/etc |
| `*.encrypted` | Any new categorized secrets | As needed |

## Edge Cases

### No Age Key
```bash
if [ ! -f ~/.age/key.txt ]; then
    echo "ERROR: No Age key at ~/.age/key.txt"
    echo "Run: age-keygen -o ~/.age/key.txt"
    exit 1
fi
```

### No Project Secrets
```bash
if [ ! -f .env ] && [ ! -f .env.example ]; then
    echo "No .env or .env.example found"
    echo "Create one first with your project secrets"
    exit 1
fi
```

### Namespace Collision
If `MYPROJECT_API_KEY` already exists from a different project:
- Warn user
- Suggest alternative: `MYPROJECT_API_KEY_V2` or manual resolution

### Uncommitted Vault Changes
```bash
cd ~/github/oneshot
if [ -n "$(git status --porcelain secrets/)" ]; then
    echo "WARNING: Uncommitted changes in secrets/"
    git status secrets/
fi
```

## Anti-Patterns

- Pushing secrets without namespace prefix
- Pushing without project label comment
- Overwriting existing secrets without confirmation
- Syncing local-only secrets (DEBUG=true, LOCAL_PORT=3000)

## Related Skills

- `secrets-vault-manager`: Single secret operations, rotation, initial setup

## Keywords

sync secrets, pull secrets, push secrets, secrets diff, compare secrets, secret synchronization, vault sync, two-way sync
