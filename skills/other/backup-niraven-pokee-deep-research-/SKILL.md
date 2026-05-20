---
name: backup
version: 1.0.0
description: Automated backup strategies for workspace, credentials, and critical data.
metadata:
  openclaw:
    emoji: 💾
    category: infrastructure
---

# Backup

Automated backup strategies for workspace, credentials, and critical data.

## What to Backup

| Priority | Item | Location | Frequency |
|----------|------|----------|-----------|
| 🔴 Critical | Credentials | `~/.credentials/` | Daily |
| 🔴 Critical | MEMORY.md | Workspace root | Daily |
| 🟡 High | Skill configs | `skills/*/config*` | Weekly |
| 🟡 High | Git repos | Various | On commit |
| 🟢 Medium | Daily memories | `memory/` | Weekly |

## Backup Strategies

### 1. Git-Based (Primary)

```bash
# Daily backup script
cd ~/.openclaw/workspace
git add -A
git commit -m "backup: $(date +%Y-%m-%d-%H:%M)"
git push origin main
```

**Pros:** Version history, free, easy restore
**Cons:** Doesn't handle large binaries well

### 2. Cloud Sync (Secondary)

```bash
# Rsync to cloud storage
rsync -avz ~/.openclaw/workspace/ gdrive:Backups/openclaw/
```

### 3. Local Archive

```bash
# Compressed archive
tar -czf backup-$(date +%Y%m%d).tar.gz ~/.openclaw/workspace/
```

## Automated Backup Job

```json
{
  "name": "daily-workspace-backup",
  "schedule": {"kind": "cron", "expr": "0 2 * * *"},
  "payload": {
    "kind": "agentTurn",
    "message": "Backup workspace: commit all changes, push to remote. Report status."
  },
  "sessionTarget": "isolated"
}
```

## Credential Backup

```bash
# Separate encrypted backup
tar -czf - ~/.credentials/ | gpg -c > credentials-backup-$(date +%Y%m%d).tar.gz.gpg
```

## Restore Procedure

1. **From Git:** `git clone` or `git checkout`
2. **From Archive:** `tar -xzf backup-xxx.tar.gz`
3. **Credentials:** Decrypt GPG backup, extract to `~/.credentials/`

## Backup Verification

Always test backups:

```bash
# Verify git backup
git log --oneline -5

# Verify archive
tar -tzf backup-xxx.tar.gz | head

# Verify credential backup
gpg -d credentials-backup-xxx.tar.gz.gpg | tar -tz | head
```

## Best Practices

1. **3-2-1 Rule:** 3 copies, 2 media types, 1 offsite
2. **Encrypt credentials** — Never plaintext
3. **Test restores** — Monthly verification
4. **Monitor failures** — Alert on backup errors
5. **Document locations** — Know where everything is
