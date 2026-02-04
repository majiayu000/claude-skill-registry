---
name: compact
description: Manually trigger context save when auto-compact fails in VSCode/Cursor extensions. Use when context is high and you need to preserve state before starting fresh.
triggers:
  - /compact
  - context full
  - save context
  - preserve state
allowed-tools: Bash,Read
---

# Manual Context Save (Compact Workaround)

## Why This Exists

VSCode and Cursor extensions have limited hook support (GitHub issue #15021).
The `PreCompact` hook may not trigger automatically, leading to lost context.
This skill provides manual control to save state before context overflow.

## When to Use

- Context warning shows 80%+ usage
- Working in VSCode or Cursor extension
- Before starting a new conversation
- When auto-compact doesn't seem to work

## Execution Steps

### Step 1: Detect Environment

```bash
# Check current environment
source ~/.claude/hooks/detect-environment.sh 2>/dev/null && print_env_info || echo "Environment detection unavailable"
```

### Step 2: Get Current Session ID

The session ID is needed to save context properly:

```bash
# Try to get session ID from state
SESSION_ID=$(cat ~/.ralph/state/current-session 2>/dev/null || echo "manual-$(date +%Y%m%d-%H%M%S)")
echo "Session: $SESSION_ID"
```

### Step 3: Extract and Save Context

```bash
# Run the pre-compact hook manually
export SESSION_ID="${SESSION_ID:-manual-$(date +%Y%m%d-%H%M%S)}"

# Create input JSON for the hook
echo "{\"hook_event_name\":\"PreCompact\",\"session_id\":\"$SESSION_ID\",\"transcript_path\":\"\"}" | \
    ~/.claude/hooks/pre-compact-handoff.sh

echo ""
echo "✅ Context saved to:"
echo "   Ledger: ~/.ralph/ledgers/CONTINUITY_RALPH-$SESSION_ID.md"
echo "   Handoff: ~/.ralph/handoffs/$SESSION_ID/"
```

### Step 4: Verify Save

```bash
# Show the saved ledger
echo "=== SAVED LEDGER ==="
head -30 ~/.ralph/ledgers/CONTINUITY_RALPH-$SESSION_ID.md 2>/dev/null || echo "Ledger not found"
```

## Alternative: Use Ralph CLI

If the above doesn't work, use the Ralph CLI directly:

```bash
ralph compact
```

This wrapper command handles all the complexity automatically.

## Post-Compact Actions

After saving context:

1. **Start fresh**: Use `/clear` or start a new conversation
2. **Restore context**: The `SessionStart` hook will auto-load the saved ledger
3. **Verify restoration**: Check that your objective is loaded

## Recovery

If context was lost without saving:

```bash
# List recent ledgers
ralph ledger list

# Load a specific ledger
ralph ledger load <session-id>

# Search handoffs
ralph handoff search "keyword"
```

## Troubleshooting

### Hook not found
```bash
# Verify hooks exist
ls -la ~/.claude/hooks/pre-compact-handoff.sh
ls -la ~/.claude/hooks/detect-environment.sh

# If missing, sync from repo
ralph sync-global
```

### Permission denied
```bash
# Make hooks executable
chmod +x ~/.claude/hooks/*.sh
chmod +x ~/.claude/scripts/*.py
```

### Context extractor fails
```bash
# Test context extractor directly
python3 ~/.claude/scripts/context-extractor.py --project . --pretty
```
