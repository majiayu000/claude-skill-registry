---
name: samara
description: Debug, check, or restart Samara.app - the message broker. Use when messages aren't being detected, Samara crashed, need to view logs, check Full Disk Access, or restart the app. Trigger words: samara, messages not working, restart, logs, FDA, broker.
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "/Users/claude/Developer/samara-main/.claude/hooks/block-deriveddata-copy.sh"
          timeout: 5
---

# Samara Debug and Control

Diagnose and manage Samara.app, the message broker that connects iMessage to Claude.

## Quick Actions

### Check if Running
```bash
launchctl list co.organelle.Samara 2>/dev/null | grep -E "PID|Label"
ps aux | grep -i [S]amara
```

### View Recent Logs
```bash
# Samara's own logs
tail -50 ~/.claude-mind/system/logs/samara.log 2>/dev/null

# System logs for Samara
log show --predicate 'process == "Samara"' --last 5m 2>/dev/null | tail -30
```

### Restart Samara
```bash
# Kill if running
pkill -f Samara

# Wait a moment
sleep 2

# Relaunch
open /Applications/Samara.app
```

**Tip:** This sequence is a good candidate for the Bash subagent (Task tool with `subagent_type=Bash`) to avoid polluting context with intermediate steps.

### Check Full Disk Access
```bash
# This will work if FDA is granted
ls ~/Library/Messages/chat.db && echo "FDA: OK" || echo "FDA: MISSING"

# Check code signature (Team ID must be stable)
codesign -d -r- /Applications/Samara.app 2>&1 | head -5
```

## Common Issues

### Messages Not Being Detected
1. Check Samara is running
2. Check FDA is intact
3. Check chat.db is readable
4. Look for errors in logs

### Samara Crashed
1. Check system logs for crash reason
2. Restart with `open /Applications/Samara.app`
3. If repeated crashes, may need rebuild

### FDA Revoked After Update
This happens if Team ID changed during rebuild:
```bash
# Check current signature - MUST show G4XVD3J52J
codesign -d -r- /Applications/Samara.app 2>&1 | grep "subject.OU"

# If shows 7V9XLQ8YNQ or any other team: WRONG CERTIFICATE USED
# Must rebuild properly and re-grant FDA
```

### Rebuild Samara

> **CRITICAL**: ONLY use the update-samara script. NEVER copy from DerivedData.
>
> A Claude instance previously broke FDA by copying a Debug build from
> `~/Library/Developer/Xcode/DerivedData/`. This used automatic signing
> which picked the WRONG certificate and revoked all permissions.

**The ONLY correct way to rebuild:**
```bash
~/.claude-mind/system/bin/update-samara
```

**FORBIDDEN (will break FDA):**
- `cp -R ~/Library/Developer/Xcode/DerivedData/.../Samara.app /Applications/`
- `xcodebuild -configuration Debug` for deployment
- Any manual copy of Samara.app to /Applications

**Verify after rebuild:**
```bash
codesign -d -r- /Applications/Samara.app 2>&1 | grep "subject.OU"
# Must show: G4XVD3J52J
# If shows: 7V9XLQ8YNQ - WRONG! FDA will be revoked
```

## Diagnostic Report

When troubleshooting, gather:
1. Is Samara running?
2. FDA status
3. Recent log errors
4. Last successful message detection
5. Code signature validity

Present findings clearly with recommended actions.

## Related Skills

For specific issues, use these specialized skills:

- `/diagnose-leaks` — Debug thinking traces or session IDs leaking into messages
- `/debug-session` — Debug session management, batching, and task routing
- `/status` — Quick system health check
