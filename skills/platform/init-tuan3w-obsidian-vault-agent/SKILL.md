---
name: init
description: Initialize an Obsidian vault with the agent-ready Zettelkasten system — creates directory structure, templates, CLAUDE.md, MCP config, and hooks
allowed-tools: Bash
---

# /init — Scaffold an Agent-Ready Obsidian Vault

Run the init script to scaffold a complete vault in the current directory:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/init-vault.sh"
```

If CLAUDE.md already exists and the user wants to overwrite:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/init-vault.sh" --force
```

The script handles everything: directories, templates, CLAUDE.md, .mcp.json, hooks, .gitignore, example notes, and git init.

After the script completes, tell the user:

```
Vault initialized! Next steps:

1. Open this folder in Obsidian
2. Install recommended community plugins:
   - Dataview (recommended — powers Spaces dashboards)
   - Obsidian Linter (recommended — auto-formatting)

3. In Obsidian Settings → Core Plugins → Templates:
   - Set "Template folder location" to "templates"

4. Start using the vault:
   - /process  — Process a source note (try the example post!)
   - /recall   — Review session with spaced repetition
   - /synthesize — Cross-domain synthesis
   - /research — Research a new topic
   - /youtube  — Create notes from a YouTube video
```

$ARGUMENTS
