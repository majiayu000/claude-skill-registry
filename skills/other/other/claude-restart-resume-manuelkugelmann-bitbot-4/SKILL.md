---
name: claude-restart-resume
description: Quick restart to reload configuration changes (skills, settings, hooks, MCP services). Use PROACTIVELY after modifying .claude/ files. Preserves conversation history.
---

Restarting Claude Code to reload configuration...

This will:
- Reload all skills from .claude/skills/
- Reload settings from .claude/settings.json
- Reload hooks configuration
- Preserve your conversation history

```bash
.claude/skills/claude-restart-resume/scripts/claude-restart.sh resume
```
