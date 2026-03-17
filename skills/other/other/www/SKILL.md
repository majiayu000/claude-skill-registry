---
name: www
description: Worker Watcher - Check and manage MCP worker status (diagnostics and auto-restart). Use when user types 'www' or when MCP worker issues occur.
model: haiku
---

# WWW - Worker Watcher (MCP Plugin Management)

## Purpose
Quick diagnostics and management of the claude-mem worker service. Checks status, verifies health, and provides auto-fix recommendations.

## When to Use
- User explicitly types `www`
- Debugging MCP plugin issues
- Before git operations (worker handles save-hooks)
- After system restart
- Worker errors in logs

## Steps

### 1. Use WWW Script (Uses Gemini Flash for log analysis only)

This skill now uses `scripts/www_worker.py` which:
- Checks worker status automatically (no LLM)
- Verifies health endpoints (no LLM)
- Gets recent logs (no LLM)
- Uses Gemini Flash ONLY for log analysis
- Saves ~80% of LLM costs

### 2. Execute Script

**Basic diagnostics:**
```bash
python3 scripts/www_worker.py
```

**With auto-restart:**
```bash
python3 scripts/www_worker.py --restart
```

The script will:
1. Check worker status (running/stopped, PID, port, uptime)
2. Verify health endpoint if running
3. Check port binding
4. Analyze recent logs with Gemini Flash (or simple analysis if unavailable)
5. Recommend action
6. Auto-restart if requested and recommended

### 3. Report Format

The script produces a complete diagnostic report:
```
# 🔧 MCP Worker Status - [Time GMT+7]

## Worker Service
**Status**: [Running ✅ / Stopped ❌]
**PID**: [number]
**Port**: [number]
**Uptime**: [duration]

## Health Check
**HTTP Health**: [healthy ✅ / unhealthy ❌ / unreachable ❌]
**Port Binding**: [correct ✅ / conflict ❌]

## Recent Activity
[Last 5-10 lines from logs]

## Issues Detected
[If any: list specific issues]
[If none: "✅ No issues detected"]

## Recommendation
[no action needed / restart recommended / see troubleshooting]
```

### 5. Auto-Fix (if needed)

**If worker is down or unhealthy:**
```
⚠️ Worker is not healthy. Would you like me to restart it?

Command: bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js restart
```

**If user approves:**
```bash
# Restart worker
bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js restart

# Wait 2 seconds
sleep 2

# Verify restart
bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js status
curl -s http://127.0.0.1:37777/api/health
```

**Report result:**
```
✅ Worker restarted successfully!

**New Status**: Running
**PID**: [new-pid]
**Health**: Healthy
```

## Common Issues & Fixes

### Issue 1: Worker Not Running
**Symptom**: Status shows "not running"
**Fix**:
```bash
bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js start
```

### Issue 2: Port Conflict
**Symptom**: "address already in use"
**Diagnosis**:
```bash
lsof -i :37777
```
**Fix**:
```bash
# Kill conflicting process
lsof -ti :37777 | xargs kill -9
# Or change port in ~/.claude-mem/settings.json
```

### Issue 3: Bun Not Found
**Symptom**: "bun: command not found"
**Fix**:
```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash
# Add to PATH
echo 'export PATH="$HOME/.bun/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Issue 4: Stale PID File
**Symptom**: Status shows running but no process exists
**Fix**:
```bash
rm ~/.claude-mem/worker.pid
bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js start
```

## Aliases (Recommended)

Suggest these aliases to user:
```bash
# Add to ~/.zshrc or ~/.bashrc
alias cm-status='bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js status'
alias cm-start='bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js start'
alias cm-restart='bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js restart'
alias cm-stop='bun ~/.claude/plugins/marketplaces/thedotmack/plugin/scripts/worker-cli.js stop'
alias cm-logs='tail -f ~/.claude-mem/logs/worker-$(date +%Y-%m-%d).log'
```

## Important Notes

### Prerequisites
- **Bun required**: Worker needs Bun runtime (not Node.js)
- **Port 37777**: Default port (configurable in settings)
- **File locations**: All files in `~/.claude-mem/`

### File Locations
- PID file: `~/.claude-mem/worker.pid`
- Logs: `~/.claude-mem/logs/worker-YYYY-MM-DD.log`
- Settings: `~/.claude-mem/settings.json` (optional)
- Database: `~/.claude-mem/claude-mem.db`

### Before Git Operations
Always check worker before commits:
```bash
# Quick check
cm-status

# Auto-restart if down
cm-status || cm-restart
```

Worker handles save-hooks during git commits.

## Troubleshooting Reference

For detailed troubleshooting, refer to CLAUDE.md section:
- "MCP Plugin Management"
- "Troubleshooting > MCP Worker Issues"

Common fixes:
1. **Quick fix**: Restart worker
2. **Bun missing**: Install Bun
3. **Port conflict**: Kill conflicting process
4. **Stale PID**: Delete PID file
5. **Nuclear option**: Clean reinstall

## Success Criteria
- ✅ Worker status checked
- ✅ Health verified
- ✅ Logs reviewed
- ✅ Issues identified (if any)
- ✅ Recommendations provided
- ✅ Auto-fix offered (if needed)
- ✅ User informed clearly

## Performance Notes
- **Fast**: Haiku model for quick diagnostics
- **Response time**: < 5 seconds
- **Automatic**: Can detect issues proactively
- **Safe**: Only suggests fixes, requires user approval
