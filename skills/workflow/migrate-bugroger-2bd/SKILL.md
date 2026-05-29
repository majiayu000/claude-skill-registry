---
name: migrate
description: Migrate from combined repo to engine+vault setup. Use when you have an existing 2bd repo with personal content mixed in, and want to separate it into engine (git) and vault (OneDrive).
argument-hint: "--vault=/path/to/new/vault"
---

# Migrate Action

This action helps existing 2bd users migrate from a combined repository to the separated engine+vault architecture.

## Overview

**Before:** Single repo with engine code + personal content
**After:**
- Engine repo (here) — clean, shareable, git-tracked
- Vault (OneDrive) — personal content, no git

---

## Workflow

### 1. Get Vault Path

Check for `--vault=` argument, otherwise ask:

"Where should I create your vault? This should be a folder that syncs with OneDrive/iCloud/Dropbox.

Example: `~/OneDrive/2bd-vault`"

Store as `$VAULT`.

### 2. Validate Path

- Ensure parent directory exists
- Warn if path is inside a git repo: "This path is inside a git repository. Vaults should NOT be in git repos."
- If path already exists with files: "This folder already has files. Choose a different path or empty it first."

### 3. Create Vault from Scaffold

```bash
mkdir -p "$VAULT"
cp -r scaffold/* "$VAULT/"
```

### 4. Copy Personal Content

Copy existing personal content from this repo to the vault:

**Captive notes:**
```bash
cp 00_Brain/Captive/*.md "$VAULT/00_Brain/Captive/" 2>/dev/null || true
cp -r 00_Brain/Captive/Flash/* "$VAULT/00_Brain/Captive/Flash/" 2>/dev/null || true
```

**Periodic archives:**
```bash
cp 00_Brain/Periodic/Daily/*.md "$VAULT/00_Brain/Periodic/Daily/" 2>/dev/null || true
cp 00_Brain/Periodic/Weekly/*.md "$VAULT/00_Brain/Periodic/Weekly/" 2>/dev/null || true
cp 00_Brain/Periodic/Monthly/*.md "$VAULT/00_Brain/Periodic/Monthly/" 2>/dev/null || true
cp 00_Brain/Periodic/Quarterly/*.md "$VAULT/00_Brain/Periodic/Quarterly/" 2>/dev/null || true
cp 00_Brain/Periodic/Yearly/*.md "$VAULT/00_Brain/Periodic/Yearly/" 2>/dev/null || true
```

**Semantic & Synthetic:**
```bash
cp -r 00_Brain/Semantic/* "$VAULT/00_Brain/Semantic/" 2>/dev/null || true
cp -r 00_Brain/Synthetic/* "$VAULT/00_Brain/Synthetic/" 2>/dev/null || true
```

**Directives:**
```bash
cp -r 00_Brain/Systemic/Directives/*.md "$VAULT/00_Brain/Systemic/Directives/" 2>/dev/null || true
```

**Projects:**
```bash
cp 01_Projects/*.md "$VAULT/01_Projects/" 2>/dev/null || true
```

**Areas:**
```bash
cp 02_Areas/People/*.md "$VAULT/02_Areas/People/" 2>/dev/null || true
cp 02_Areas/Insights/*.md "$VAULT/02_Areas/Insights/" 2>/dev/null || true
```

**Archives:**
```bash
cp -r 04_Archives/* "$VAULT/04_Archives/" 2>/dev/null || true
```

### 5. Write Engine Config

Write `.claude/config.md`:

```markdown
# 2bd Engine Configuration

## Vault

vault_path: $VAULT
```

### 6. Report What Was Copied

Count and report:
- Number of Captive notes copied
- Number of Periodic archives copied
- Number of Projects copied
- Number of People files copied
- Whether Directives were found and copied

### 7. Cleanup Instructions

Print instructions for cleaning up the engine repo:

"Migration complete! Your vault is at: `$VAULT`

**Next steps to clean up the engine repo:**

1. Delete personal content from this repo (it's now in your vault):
   ```bash
   rm -rf 00_Brain/Captive/*.md
   rm -rf 00_Brain/Periodic/Daily/*.md 00_Brain/Periodic/Weekly/*.md
   rm -rf 00_Brain/Periodic/Monthly/*.md 00_Brain/Periodic/Quarterly/*.md
   rm -rf 00_Brain/Periodic/Yearly/*.md
   rm -rf 00_Brain/Semantic/* 00_Brain/Synthetic/*
   rm -rf 00_Brain/Systemic/Directives/*.md
   rm -rf 01_Projects/*.md
   rm -rf 02_Areas/People/*.md 02_Areas/Insights/*.md
   rm -rf 04_Archives/*
   ```

2. Remove content directories (they now live only in scaffold/):
   ```bash
   rm -rf 00_Brain 01_Projects 02_Areas 03_Resources 04_Archives
   ```

3. Commit the cleaned engine:
   ```bash
   git add -A
   git commit -m 'Clean engine for public sharing'
   ```

4. Open your vault in Obsidian and verify everything looks correct.

5. Test skills work:
   ```bash
   claude skill run rituals/planning/daily-planning
   ```

**Important:** From now on, always run Claude from this engine directory, not from your vault."

---

## Rollback

If something went wrong, your original files are still here. The migrate action only *copies* files to the vault, it doesn't delete anything from the engine until you manually clean up.
