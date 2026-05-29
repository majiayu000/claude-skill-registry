---
name: debugging-claude-code
description: Troubleshooting guide for Claude Code issues. Use when Claude behaves unexpectedly, tools fail, sessions hang, or you need to diagnose problems. Covers diagnostics, common issues, and recovery procedures.
allowed-tools: ["Read", "Bash"]
---

# Debugging Claude Code

Systematic troubleshooting guide for diagnosing and resolving Claude Code issues.

## Quick Diagnostics

Run these commands first when experiencing issues:

```bash
# Health check - comprehensive system status
claude doctor

# Or in-session
/doctor

# Check Claude Code version
claude --version

# Debug mode - verbose output for all operations
claude --debug

# Environment-level debug logging
ANTHROPIC_LOG=debug claude

# Check registered hooks
claude --print-hooks

# View MCP server status
claude mcp list
```

## Common Issues Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| Tool not working | Permission denied | `/permissions` then allow tool |
| MCP tools missing | Server disconnected | `/mcp` to check status |
| Hook not firing | JSON syntax error | `jq . ~/.claude/settings.json` |
| Skill not loading | Invalid frontmatter | Check YAML syntax |
| Context overflow | Too much data | Use `/compact` or `/clear` |
| Rate limited | Too many requests | Wait 60 seconds |
| API errors | Auth/network issues | Check `~/.claude/.credentials.json` |
| Session stuck | Process hanging | Ctrl+C, restart Claude |
| Slow responses | Network or model load | Check connection, try again |

## Debug Flags and Environment Variables

### Command-Line Flags

| Flag | Purpose |
|------|---------|
| `--debug` | Enable verbose debug output |
| `--print-hooks` | Display all registered hooks |
| `--verbose` | Show more detailed output |
| `--no-cache` | Disable response caching |

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `ANTHROPIC_LOG` | Log level | `debug`, `info`, `warn`, `error` |
| `CLAUDE_CODE_DEBUG` | Additional debugging | `1` or `true` |
| `MCP_TIMEOUT` | MCP connection timeout (ms) | `30000` |
| `MAX_MCP_OUTPUT_TOKENS` | Max MCP output size | `50000` |
| `HTTP_PROXY` | Proxy for network requests | `http://proxy:8080` |
| `HTTPS_PROXY` | HTTPS proxy | `https://proxy:8080` |
| `NO_PROXY` | Skip proxy for hosts | `localhost,127.0.0.1` |

### Combined Debug Session

```bash
# Maximum verbosity
ANTHROPIC_LOG=debug claude --debug 2>&1 | tee ~/claude-debug.log
```

## Log Locations

### By Operating System

| OS | Location |
|----|----------|
| macOS | `~/Library/Logs/Claude Code/` |
| Linux | `~/.local/share/claude-code/logs/` |
| Windows | `%APPDATA%\Claude Code\logs\` |

### Configuration Files

| File | Purpose |
|------|---------|
| `~/.claude/settings.json` | User settings and hooks |
| `~/.claude/.credentials.json` | API credentials |
| `~/.claude/projects.json` | Project-specific settings |
| `.claude/settings.json` | Project settings (committed) |
| `.claude/settings.local.json` | Local project settings |
| `.mcp.json` | MCP server configuration |

### Session Data

| Location | Contents |
|----------|----------|
| `~/.claude/sessions/` | Session transcripts |
| `~/.claude/todos/` | Task lists |
| `~/.claude/memory/` | Persistent memory |

## Diagnostic Commands

### System Health

```bash
# Full health check
claude doctor

# Check component status
claude doctor --component api
claude doctor --component mcp
claude doctor --component hooks
```

**`/doctor` reports (2.1.6+):**
- **Updates section** - Shows auto-update channel and available npm versions (stable/latest)
- **Permission warnings** - Detects unreachable permission rules with fix guidance
- **API connectivity** - Verifies connection to Anthropic API
- **MCP servers** - Lists connected servers and their status
- **Hooks** - Validates hook configurations

### Permission Diagnostics

```bash
# View current permissions
/permissions

# Check what tools are allowed
/permissions --tools

# Check file access patterns
/permissions --files
```

### Hook Diagnostics

```bash
# List all registered hooks
claude --print-hooks

# View hooks in interactive mode
/hooks

# Validate hook JSON
jq . ~/.claude/settings.json
jq . .claude/settings.json
```

### MCP Diagnostics

```bash
# List configured servers
claude mcp list

# Get server details
claude mcp get <server-name>

# Check connection in session
/mcp
```

## Diagnostic Decision Tree

### Is Claude starting?

```
Claude won't start
    |
    +-- Check: claude --version
    |   |
    |   +-- Works --> Config issue, check ~/.claude/
    |   +-- Fails --> Installation issue, reinstall
    |
    +-- Check: ANTHROPIC_LOG=debug claude
        |
        +-- Auth error --> Check credentials
        +-- Network error --> Check connectivity
        +-- Other --> See COMMON-ISSUES.md
```

### Are tools working?

```
Tool not working
    |
    +-- Check: /permissions
    |   |
    |   +-- Denied --> Allow tool
    |   +-- Allowed --> Continue
    |
    +-- Check: --debug output
    |   |
    |   +-- Tool called --> Check tool-specific logs
    |   +-- Not called --> Check permissions/syntax
    |
    +-- MCP tool?
        |
        +-- Yes --> /mcp, check server status
        +-- No --> See COMMON-ISSUES.md
```

### Are hooks working?

```
Hook not firing
    |
    +-- Check: /hooks
    |   |
    |   +-- Listed --> Matcher issue or script issue
    |   +-- Not listed --> JSON syntax error
    |
    +-- Validate JSON: jq . settings.json
    |   |
    |   +-- Valid --> Check matcher pattern
    |   +-- Invalid --> Fix JSON syntax
    |
    +-- Test script: echo '{}' | ./hook.sh
        |
        +-- Works --> Matcher doesn't match
        +-- Fails --> Script error
```

## Built-in Diagnostic Commands

| Command | Purpose |
|---------|---------|
| `/hooks` | View registered hooks |
| `/mcp` | MCP server status |
| `/permissions` | Permission settings |
| `/memory` | Memory bank status |
| `/status` | Session status |
| `/bug` | Report a bug |
| `/doctor` | Run health checks |

## Verbose Mode

Toggle verbose mode during a session:

- **Keyboard shortcut**: `Ctrl+O` (in terminal)
- **Shows**: Hook execution, tool calls, API responses

## Quick Fixes

### Permission Issues

```bash
# Allow all file operations in project
/permissions --allow "Write,Edit,Read" --scope project

# Allow specific MCP server
/permissions --allow "mcp__servername__*"
```

### Clear Issues

```bash
# Clear conversation context
/clear

# Compact context (keep important parts)
/compact

# Reset session
/reset
```

### Configuration Reset

```bash
# Back up and reset settings
cp ~/.claude/settings.json ~/.claude/settings.json.bak
rm ~/.claude/settings.json

# Reset just hooks
jq 'del(.hooks)' ~/.claude/settings.json > tmp && mv tmp ~/.claude/settings.json
```

## Reference Files

| File | Contents |
|------|----------|
| [DIAGNOSTICS.md](./DIAGNOSTICS.md) | Detailed diagnostic techniques |
| [COMMON-ISSUES.md](./COMMON-ISSUES.md) | Common problems and solutions |
| [RECOVERY.md](./RECOVERY.md) | Recovery procedures |

## When to Escalate

Use `/bug` to report issues when:

- `claude doctor` shows failures
- Reproducible crashes
- API errors persist after credential refresh
- Behavior contradicts documentation

Include in bug reports:
- Claude Code version (`claude --version`)
- OS and version
- Debug output (`claude --debug`)
- Steps to reproduce
