---
name: maintenance
description: Run organism maintenance checks - drift detection, symlink repair, service verification. Use for health checks and maintenance tasks.
triggers:
  - maintenance
  - health check
  - system check
  - drift check
---

# Organism Maintenance

Run maintenance checks and repairs on the Samara organism.

## Quick Check

Run a quick health status:

```bash
~/.claude-mind/bin/sync-organism --check && echo "No drift detected" || echo "Drift detected"
```

## Full Maintenance Checklist

### 1. System Drift Check
```bash
~/.claude-mind/bin/sync-organism --check
```
If drift detected, review and sync:
```bash
~/.claude-mind/bin/sync-organism
```

### 2. Launchd Services
```bash
launchctl list | grep com.claude
```
Expected: 4+ services (wake-adaptive, dream, message-watcher, etc.)

If missing, reload:
```bash
launchctl load ~/Library/LaunchAgents/com.claude.*.plist
```

### 3. Samara.app Status
```bash
pgrep -x Samara && echo "Running" || echo "Not running"
```
If not running:
```bash
open /Applications/Samara.app
```

### 4. FDA Status
```bash
# Check for recent FDA issues
tail -20 ~/.claude-mind/logs/samara.log | grep -i "denied\|permission"
```

### 5. Lock File
```bash
# Check for stale locks
if [ -f ~/.claude-mind/claude.lock ]; then
    cat ~/.claude-mind/claude.lock | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Lock held by: {d.get('task')} (PID: {d.get('pid')})\")"
fi
```

### 6. Symlink Integrity
```bash
# Check critical symlinks
for link in ~/.claude-mind/bin ~/.claude-mind/.claude ~/.claude-mind/instructions; do
    if [ -L "$link" ]; then
        if [ -e "$link" ]; then
            echo "$link -> $(readlink "$link") [OK]"
        else
            echo "$link -> $(readlink "$link") [BROKEN]"
        fi
    fi
done
```

## Repair Commands

### Sync from repo
```bash
~/.claude-mind/bin/sync-organism
```

### Rebuild Samara.app
```bash
~/.claude-mind/bin/update-samara
```

### Clear stale lock
```bash
rm -f ~/.claude-mind/claude.lock
```

### Reload all launchd services
```bash
for f in ~/Library/LaunchAgents/com.claude.*.plist; do
    launchctl unload "$f" 2>/dev/null
    launchctl load "$f"
done
```

## When to Use

- After updating samara-main repo
- After system restart
- When wake cycles seem stuck
- When messages aren't being processed
- After Xcode rebuild of Samara.app
