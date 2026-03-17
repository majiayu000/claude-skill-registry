---
name: mcp-recovery
description: Autonomous MCP and Godot recovery procedures. Use when MCP tools are unresponsive, port 9080 is not listening, or multiple Godot instances are causing conflicts.
---

# MCP Recovery Skill

Autonomous recovery procedures for Godot MCP connection issues.

## When to Use This Skill

Use when:
- MCP commands timeout or return "Connection refused"
- Port 9080 is not listening
- Multiple Godot processes are running
- MCP CLI is unresponsive
- Health check returns "degraded" or "down"

## Recovery Levels

### Level 1: Light Recovery
**Use for:** Transient MCP issues, single command failures

**Actions:**
1. Test MCP CLI connection
2. Restart MCP CLI if needed
3. Verify port 9080

**Commands:**
```bash
# Test connection
npx -y godot-mcp-cli@latest get_project_info

# If timeout, restart MCP CLI (no action needed - CLI is stateless)
```

### Level 2: Medium Recovery
**Use for:** Port 9080 not listening, MCP not responding

**Actions:**
1. Check for duplicate Godot processes
2. Kill duplicate Godot instances
3. Restart MCP server via Godot

**Commands:**
```bash
# Check for duplicates
tasklist | findstr /i "Godot"

# If more than 1 Godot process, kill extras
Stop-Process -Name "Godot*" -Force

# Restart Godot with MCP
powershell -File .claude/skills/godot-mcp-dap-start/scripts/ensure_godot_mcp.ps1
```

### Level 3: Heavy Recovery
**Use for:** Complete MCP failure, corrupted state

**Actions:**
1. Kill all Godot processes
2. Wait 2 seconds for cleanup
3. Start fresh Godot instance
4. Wait for MCP port 9080
5. Verify MCP handshake

**Commands:**
```bash
# Full restart using recovery script
powershell -ExecutionPolicy Bypass -File .claude/skills/mcp-recovery/scripts/recover.ps1
```

## Quick Reference

| Symptom | Recovery Level | Command |
|---------|---------------|---------|
| Single command timeout | Light | Retry command |
| "Connection refused" | Medium | Kill duplicate Godot processes |
| Port 9080 not listening | Medium | Restart Godot with MCP |
| Multiple Godot processes | Medium | `Stop-Process -Name "Godot*" -Force` |
| Complete MCP failure | Heavy | `powershell -File .claude/skills/mcp-recovery/scripts/recover.ps1` |

## Health Check

Before attempting recovery, run health check:
```bash
powershell -ExecutionPolicy Bypass -File scripts/mcp-health-check.ps1
```

Or for JSON output (parsing):
```bash
powershell -ExecutionPolicy Bypass -File scripts/mcp-health-check.ps1 -JSON
```

## Escalation

**Ask user for help if:**
- Recovery script fails multiple times
- Godot fails to start after heavy recovery
- MCP addon fails to load (check Godot console for errors)
- Port 9080 never becomes available
- You don't understand the error message

## Integration with Other Skills

- **godot-mcp-dap-start**: Use for starting Godot with MCP
- **playtesting**: Run health check before HPV sessions
- **minimax-mcp**: Separate MCP server, not affected by Godot MCP issues

## Notes

- MCP CLI (`npx -y godot-mcp-cli@latest`) is stateless - no need to restart it
- Godot MCP server runs inside Godot editor on port 9080
- Multiple Godot instances cause port conflicts - only one can bind port 9080
- The recovery script automates the full recovery process
