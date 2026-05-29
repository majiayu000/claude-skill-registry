---
name: capability
description: Check if a specific action is possible and what might be blocking it. Use when asking if you can do something, checking permissions, verifying a capability exists, or troubleshooting why something isn't working. Trigger words: can I, capability, able to, permission, possible, how do I.
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Capability Check

Verify if a specific action is possible and diagnose any blockers.

## Capability Inventory

Full capabilities documentation: `~/.claude-mind/self/inventory.md`

### Access Patterns

```bash
# Read full inventory (comprehensive reference)
cat ~/.claude-mind/self/inventory.md

# Search for specific capability
grep -ni "search term" ~/.claude-mind/self/inventory.md

# List all sections
grep "^## " ~/.claude-mind/self/inventory.md
```

## Quick Capability Matrix

| Capability | Method | Requires |
|------------|--------|----------|
| Send iMessage | AppleScript via Samara | Samara running, Automation permission |
| Send image | `send-image` script | Pictures folder workaround |
| Read calendar | AppleScript | Calendar permission |
| Write calendar | AppleScript | Calendar permission |
| Read contacts | AppleScript | Contacts permission |
| Read/write notes | AppleScript | Notes permission (legacy) |
| Shared workspace notes | Filesystem | `~/.claude-mind/shared/` (preferred) |
| Send email | AppleScript | Mail permission |
| Post to Bluesky | `bluesky-post` script | Credentials in config |
| Browse web | Playwright MCP | MCP server running |
| Take screenshot | `screenshot` script | Screen recording permission |
| Read Messages DB | Direct file access | Full Disk Access |
| Run shell commands | Bash | Always available |
| Read/write files | Direct | Always available |

## Checking Specific Capabilities

### Messaging
```bash
launchctl list co.organelle.Samara 2>/dev/null | grep -q 'PID' && echo "Samara: OK" || echo "Samara: Not running"
~/.claude-mind/system/bin/message "test" --dry-run 2>/dev/null
```

### Calendar
```bash
osascript -e 'tell application "Calendar" to get name of calendars' 2>&1
```

### Contacts
```bash
osascript -e 'tell application "Contacts" to get name of first person' 2>&1
```

### Shared Workspace (Preferred)
```bash
ls ~/.claude-mind/shared 2>/dev/null
```

### Notes (Legacy)
```bash
osascript -e 'tell application "Notes" to get name of first note' 2>&1
```

### Mail
```bash
osascript -e 'tell application "Mail" to get name of first account' 2>&1
```

### Bluesky
```bash
grep -q "bluesky" ~/.claude-mind/system/config.json && echo "Bluesky: Configured" || echo "Bluesky: Not configured"
```

### Full Disk Access
```bash
ls ~/Library/Messages/chat.db 2>/dev/null && echo "FDA: OK" || echo "FDA: Missing"
```

## Troubleshooting Flow

1. **Identify the capability**: What action is being attempted?

2. **Check prerequisites**:
   - Is the required app/service running?
   - Are permissions granted?
   - Is configuration present?

3. **Test minimally**: Run simplest possible version of the action

4. **Check logs**: Look for error messages
```bash
log show --predicate 'process == "osascript"' --last 2m
```

5. **Report findings**: What works, what doesn't, what to fix

## Common Blockers

- **"Not authorized to send Apple events"**: Missing Automation permission
- **"Operation not permitted"**: Missing FDA or specific permission
- **"Application isn't running"**: Need to launch the app first
- **"No such file"**: Script or config missing
