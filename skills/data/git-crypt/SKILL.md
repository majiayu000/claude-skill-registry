---
name: "git-crypt"
version: "1.0.0"
description: "Manage git-crypt encrypted repositories with seamless worktree support. Handles unlock/lock operations, key management, and the critical worktree smudge filter issue that causes encrypted file checkout failures."
category: security
tags:
  - git
  - encryption
  - security
  - worktree
  - secrets
author: Smith Horn
---

# git-crypt

Manage git-crypt encrypted repositories with seamless worktree support.

## Trigger Phrases

- "unlock git-crypt", "decrypt repo"
- "create worktree" (in git-crypt repos)
- "git-crypt status", "check encryption"
- "encrypted files", "git-crypt key"

## The Problem This Skill Solves

When creating git worktrees in repositories using git-crypt, you'll encounter this error:

```
git-crypt: Error: Unable to open key file - have you unlocked/initialized this repository yet?
error: external filter '"git-crypt" smudge' failed
fatal: .encrypted/file.md: smudge filter git-crypt failed
```

**Root cause**: Git worktrees don't inherit the git-crypt key configuration from the main repository's `.git/git-crypt/keys/` directory.

**This skill provides**: Automated workaround that copies keys and handles the smudge filter issue.

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `git-crypt status` | Check if repo uses git-crypt and current lock state |
| `git-crypt unlock <key-path>` | Unlock repo with symmetric key |
| `git-crypt lock` | Re-encrypt files (rarely needed) |

### Worktree Commands (This Skill's Value-Add)

```bash
# Create worktree with git-crypt support
./scripts/git-crypt-worktree.sh create <path> <branch>

# Fix existing worktree that failed checkout
./scripts/git-crypt-worktree.sh fix <worktree-path>

# Check worktree git-crypt status
./scripts/git-crypt-worktree.sh status <worktree-path>
```

---

## Prerequisites

1. **git-crypt installed**: `brew install git-crypt`
2. **Symmetric key file**: Stored securely (e.g., `~/.keys/project-git-crypt.key`)
3. **Main repo unlocked**: Always unlock main repo before creating worktrees

---

## Workflow: Creating Worktrees in git-crypt Repos

### Step 1: Ensure Clean Working Directory

```bash
# git-crypt unlock requires clean state
git stash push -m "WIP before git-crypt unlock"
```

### Step 2: Unlock Main Repository

```bash
git-crypt unlock ~/.keys/your-project.key
```

### Step 3: Create Worktree with Script

```bash
# Use the helper script (recommended)
./.claude/skills/git-crypt/scripts/git-crypt-worktree.sh create ../worktrees/feature-x feature/feature-x

# Or manually:
# 1. Temporarily disable smudge filter
git config --unset filter.git-crypt.smudge
git config --unset filter.git-crypt.clean
git config --unset filter.git-crypt.required
git config --unset diff.git-crypt.textconv

# 2. Create worktree
git worktree add ../worktrees/feature-x -b feature/feature-x

# 3. Re-enable smudge filter
git config filter.git-crypt.smudge '"git-crypt" smudge'
git config filter.git-crypt.clean '"git-crypt" clean'
git config filter.git-crypt.required true
git config diff.git-crypt.textconv '"git-crypt" diff'

# 4. Copy keys to worktree
mkdir -p .git/worktrees/feature-x/git-crypt/keys
cp .git/git-crypt/keys/default .git/worktrees/feature-x/git-crypt/keys/

# 5. Checkout files in worktree
cd ../worktrees/feature-x
git checkout HEAD -- .
```

### Step 4: Restore Stashed Changes

```bash
cd /path/to/main/repo
git stash pop
```

---

## Detecting git-crypt Repos

```bash
# Check if repo uses git-crypt
if [ -d ".git/git-crypt" ]; then
    echo "This repo uses git-crypt"
fi

# Check encryption status of specific file
git-crypt status docs/secrets.md

# Check all encrypted files
git-crypt status | grep "encrypted:"
```

---

## Key Management

### Symmetric Key Location Convention

Store keys outside the repository:

```
~/.keys/
├── skillsmith-git-crypt.key
├── other-project-git-crypt.key
└── README.md  # Document which key is for which repo
```

### Security Best Practices

1. **Never commit keys** to any repository
2. **Use restrictive permissions**: `chmod 600 ~/.keys/*.key`
3. **Back up keys securely** (password manager, encrypted drive)
4. **Document key locations** in team wiki (not in repo)

### Export Key for Team Members

```bash
# Export symmetric key (do this once, share securely)
git-crypt export-key /path/to/exported.key
```

---

## Troubleshooting

### "Working directory not clean" during unlock

```bash
git stash push -m "WIP"
git-crypt unlock ~/.keys/project.key
git stash pop
```

### Worktree shows files as "deleted"

This happens when git-crypt keys aren't in the worktree's git directory:

```bash
# Fix: Copy keys and re-checkout
./.claude/skills/git-crypt/scripts/git-crypt-worktree.sh fix ../worktrees/your-worktree
```

### "smudge filter git-crypt failed" during worktree creation

Use the helper script which temporarily disables the filter:

```bash
./.claude/skills/git-crypt/scripts/git-crypt-worktree.sh create ../worktrees/new-worktree -b branch-name
```

### Check if files are actually encrypted vs decrypted

```bash
# If this shows readable text, files are decrypted (good)
head -5 docs/encrypted-file.md

# If this shows binary garbage, files are still encrypted
# Run: git-crypt unlock <key-path>
```

---

## Integration with worktree-manager Skill

This skill complements the `worktree-manager` skill. When both are present:

1. **worktree-manager** handles branch management, cleanup, coordination
2. **git-crypt** handles encryption/decryption and key propagation

### Recommended Workflow

```bash
# 1. Unlock main repo (git-crypt skill)
git-crypt unlock ~/.keys/project.key

# 2. Create worktree with git-crypt support
./.claude/skills/git-crypt/scripts/git-crypt-worktree.sh create ../worktrees/feature -b feature/name

# 3. Use worktree-manager for coordination
# (worktree-manager handles sync, status, cleanup)
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GIT_CRYPT_KEY_PATH` | Path to symmetric key | None (must specify) |
| `GIT_CRYPT_WORKTREE_AUTO_FIX` | Auto-fix worktrees on creation | `true` |

---

## Files Managed by This Skill

| Path | Purpose |
|------|---------|
| `.git/git-crypt/keys/default` | Main repo decryption key (after unlock) |
| `.git/worktrees/*/git-crypt/keys/default` | Worktree-specific key copies |
| `.gitattributes` | Defines which files are encrypted |

---

## Related Documentation

- [git-crypt GitHub](https://github.com/AGWA/git-crypt)
- [Git Worktrees](https://git-scm.com/docs/git-worktree)
- [worktree-manager skill](../worktree-manager/SKILL.md)
