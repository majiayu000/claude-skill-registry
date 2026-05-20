---
name: sync-mcp
description: Sync MCP servers from .mcp.json (source of truth) into Codex user config (~/.codex/config.toml). Claude Code picks up .mcp.json natively so no action needed there.
allowed-tools: Bash(python3 *), Bash(mkdir *), Read
---

# Sync MCP Servers

Run the sync script to install MCP servers from `.mcp.json` into the Codex user config:

```
python3 .claude/skills/sync-mcp/sync.py
```

After running, report which servers were synced and confirm both targets are up to date:
- `.mcp.json` — Claude Code (project-level, already the source file)
- `~/.codex/config.toml` — Codex (user-level, merged by the script)
