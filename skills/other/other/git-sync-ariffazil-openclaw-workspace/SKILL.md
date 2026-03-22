---
name: git-sync
description: Git operations on VPS repos — status, commit, push, pull, diff, branch management
user-invocable: true
---

# Git Sync — arifOS_bot

Triggers: "git", "git sync", "commit", "push", "pull", "diff", "branch",
          "git status", "sync repo", "backup workspace", "gitclaw"

---

## Repos on This VPS

| Alias | Path | Remote | Push Protocol |
|-------|------|--------|--------------|
| `arifos` | `/mnt/arifos` | github.com/ariffazil/arifOS | HTTPS + GH_TOKEN |
| `workspace` | `~/.openclaw/workspace` | github.com/ariffazil/openclaw-workspace | HTTPS + GH_TOKEN |
| `apex` | `/mnt/apex` | github.com/ariffazil/APEX-THEORY | HTTPS + GH_TOKEN |

---

## Daily Status Check

```bash
# arifOS repo
git -C /mnt/arifos status --short
git -C /mnt/arifos log --oneline -5

# Workspace
git -C ~/.openclaw/workspace status --short
git -C ~/.openclaw/workspace log --oneline -3
```

## Commit + Push to arifOS

```bash
# 1. See what changed
git -C /mnt/arifos diff --stat

# 2. Stage specific files (never stage .env or secrets)
git -C /mnt/arifos add core/ aaa_mcp/ aclip_cai/ tests/

# 3. Commit
git -C /mnt/arifos commit -m "feat/fix/docs: description

Co-authored-by: arifOS_bot <arifos_bot@arif-fazil.com>"

# 4. Push via HTTPS with GH_TOKEN
git -C /mnt/arifos remote set-url origin "https://${GH_TOKEN}@github.com/ariffazil/arifOS.git"
git -C /mnt/arifos push origin main
git -C /mnt/arifos remote set-url origin "https://github.com/ariffazil/arifOS.git"
```

## Pull Latest (sync from remote)

```bash
# arifOS — rebase style (clean history)
git -C /mnt/arifos fetch origin
git -C /mnt/arifos pull --rebase origin main

# Workspace
git -C ~/.openclaw/workspace pull --rebase origin main

# Both at once
for REPO in /mnt/arifos /mnt/apex; do
  echo "=== Syncing $REPO ==="
  git -C "$REPO" pull --rebase origin main 2>&1 || echo "FAILED: $REPO"
done
```

## Workspace Backup (manual trigger)

```bash
# Full backup to GitHub (same as nightly cron)
bash ~/.openclaw/workspace/scripts/backup-to-github.sh

# Quick backup — just workspace docs + skills
cd ~/.openclaw/workspace
git add SPEC.md AGENTS.md DR_RUNBOOK.md skills/ memory/
git commit -m "chore: manual workspace sync $(date -u +%Y-%m-%dT%H:%M:%SZ)"
git remote set-url origin "https://${GH_TOKEN}@github.com/ariffazil/openclaw-workspace.git"
git push origin main
git remote set-url origin "https://github.com/ariffazil/openclaw-workspace.git"
```

## Branch Management

```bash
# Create feature branch
git -C /mnt/arifos checkout -b feature/my-feature

# List branches
git -C /mnt/arifos branch -a

# Switch branch
git -C /mnt/arifos checkout main

# Delete merged branch (F1: safe, branch exists on remote)
git -C /mnt/arifos branch -d feature/my-feature

# 888_HOLD: Force delete unmerged branch
# git branch -D → requires F13 confirmation
```

## Diff & History

```bash
# What changed since last commit
git -C /mnt/arifos diff HEAD

# What's staged
git -C /mnt/arifos diff --cached

# Recent history (pretty)
git -C /mnt/arifos log --oneline --graph --decorate -10

# Who changed a file
git -C /mnt/arifos log --follow --oneline -- aaa_mcp/server.py

# Compare with remote
git -C /mnt/arifos fetch origin
git -C /mnt/arifos log --oneline HEAD..origin/main
```

## Conflict Resolution

```bash
# Check merge conflicts
git -C /mnt/arifos status | grep "both modified"

# Accept incoming (remote wins) — use with care
git -C /mnt/arifos checkout --theirs <file>
git -C /mnt/arifos add <file>

# Accept local (our wins)
git -C /mnt/arifos checkout --ours <file>
git -C /mnt/arifos add <file>

# Abort rebase if wrong
git -C /mnt/arifos rebase --abort
```

## VAULT999 Special Handling

```bash
# vault999.jsonl is force-tracked — use -f to add
git -C /mnt/arifos add -f VAULT999/vault999.jsonl
git -C /mnt/arifos commit -m "vault: seal $(date +%Y%m%d)"
```

## Safe Defaults (F1/F11)

- Always `git pull --rebase` before push (avoids diverged history)
- Never `git push --force` to `main` → 888_HOLD
- Never `git reset --hard` with uncommitted changes → 888_HOLD
- Never commit `.env`, `openclaw.json`, model weights, `*.safetensors`
- Safe.directory for `/mnt/arifos` is set: `git config --global --add safe.directory /mnt/arifos`

*arifOS_bot — git-sync skill*
