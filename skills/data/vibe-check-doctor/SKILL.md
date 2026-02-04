---
name: vibe-check-doctor
description: Troubleshoot and diagnose vibe-check setup. Use when user says "check my vibe-check setup", "troubleshoot vibe-check", "is vibe-check working", "vibe-check doctor", or asks about vibe-check configuration issues.
---

# Vibe-Check Troubleshooting & Diagnosis

**Purpose:** Help users diagnose and fix vibe-check configuration and operational issues

---

## When to Use This Skill

Invoke this troubleshooting flow when the user:
- Asks "is vibe-check working?"
- Says "check my vibe-check setup"
- Requests "troubleshoot vibe-check"
- Reports issues like "vibe-check isn't recording" or "stats aren't showing up"
- Asks about vibe-check configuration

---

## Diagnostic Steps

### 1. Get Current Status

First, run the status command to understand the current state:

```bash
vibe-check status
```

This will show:
- **Service status**: Is vibe-check running?
- **Database location and size**: Where is data stored?
- **Log file location**: Where to find error messages
- **Local backup status**: Is it processing conversations?
- **Remote sync status**: Is it syncing to the server (if enabled)?
- **Claude integration**: Are MCP and skills installed?

### 2. Read Configuration

Check the configuration file (location shown in status output, typically `~/.vibe-check/config.json`):

```bash
cat ~/.vibe-check/config.json
```

Key things to verify:
- **monitor.conversation_dir**: Should be `~/.claude/projects` (where Claude Code stores conversations)
- **sqlite.enabled**: Should be `true` for local storage
- **sqlite.database_path**: Should be `~/.vibe-check/vibe_check.db`
- **api.enabled**: Whether remote sync is enabled (optional)

### 3. Check for Common Issues

Based on the status output, diagnose common problems:

#### Issue: "Not running"
- **Solution**: Start it with `vibe-check start`
- Check if it stays running or crashes immediately
- If crashes, check logs: `vibe-check logs`

#### Issue: "Database not created yet"
- **Cause**: Service hasn't started or no conversations have been captured
- **Solution**:
  1. Start the service: `vibe-check start`
  2. Use Claude Code to create a conversation
  3. Check status again: `vibe-check status`

#### Issue: "0 events in database"
- **Cause**: Monitor is running but not capturing conversations
- **Check**:
  - Is `conversation_dir` pointing to the right location?
  - Are there `.jsonl` files in `~/.claude/projects/`?
  - Check logs for errors: `vibe-check logs`

#### Issue: "MCP: ❌ Not installed"
- **Cause**: MCP plugin not installed (limits Claude integration)
- **Solution**: Run the plugin installer:
  ```bash
  ./scripts/install-plugin.sh
  ```

#### Issue: "Skills: ⚠️  X/7 installed"
- **Cause**: Some skills are missing
- **Solution**: Run the plugin installer:
  ```bash
  ./scripts/install-plugin.sh
  ```

#### Issue: "Remote sync pending"
- **Cause**: API sync is enabled but events aren't uploading
- **Check**:
  - Is the API endpoint reachable?
  - Is the API key valid? Run `vibe-check auth status`
  - Check logs for API errors: `vibe-check logs`

### 4. Review Documentation (If Needed)

For deeper understanding of the codebase, review the project documentation:

```bash
cat /Users/wanderingstan/Developer/vibe-check/CLAUDE.md
```

This contains:
- Project structure
- Database schema
- Key components
- Common patterns

---

## Response Format

When helping troubleshoot, follow this flow:

1. **Run status check** - Execute `vibe-check status` and analyze output
2. **Identify issues** - Point out what's wrong based on status
3. **Provide solutions** - Give specific commands to fix issues
4. **Verify fixes** - After user applies fixes, check status again
5. **Explain configuration** - If everything is working, explain current setup

### Example Response

```
Let me check your vibe-check setup.

[Runs vibe-check status]

I see a few issues:

1. ❌ Service is not running
   Fix: Run `vibe-check start`

2. ⚠️  Only 5/7 skills are installed
   Fix: Run `./scripts/install-plugin.sh` to install missing skills

3. ⚠️  Remote sync is enabled but no API key is set
   Fix: Run `vibe-check auth login` to authenticate

Would you like me to help you fix these issues?
```

---

## Advanced Troubleshooting

### Check Logs for Errors

If the issue isn't obvious from status:

```bash
vibe-check logs -n 100
```

Look for:
- Python exceptions or tracebacks
- File permission errors
- Database lock errors
- API connection failures

### Verify Database Integrity

If database exists but seems corrupted:

```bash
sqlite3 ~/.vibe-check/vibe_check.db "PRAGMA integrity_check;"
```

### Check File Permissions

Ensure vibe-check can read conversation files:

```bash
ls -la ~/.claude/projects/*.jsonl | head -5
```

Files should be readable by the current user.

---

## What NOT to Do

- Don't suggest deleting the database unless absolutely necessary (user will lose all history)
- Don't modify config manually unless user confirms - always explain changes first
- Don't assume the issue - always check status first

---

## Related Commands

- `vibe-check start` - Start the monitor
- `vibe-check stop` - Stop the monitor
- `vibe-check restart` - Restart the monitor
- `vibe-check logs` - View logs
- `vibe-check auth login` - Authenticate for remote sync
- `./scripts/install-plugin.sh` - Install/update MCP and skills
