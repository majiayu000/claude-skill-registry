---
name: claude-code-plugin-development
description: This skill should be used when the user asks to "create a plugin", "build a plugin", "write a plugin", or wants to bundle agents, hooks, commands, skills, or MCP servers into a distributable Claude Code plugin.
---

# Claude Code Plugin Development

Create distributable plugins that bundle commands, agents, skills, hooks, MCP servers, and LSP servers.

**Official docs:** https://code.claude.com/docs/en/plugins-reference

## Quick Reference

You MUST read these references for detailed schemas and examples:

- [Plugin Manifest](./references/plugin-manifest.md) - Complete plugin.json schema
- [Plugin Components](./references/plugin-components.md) - Commands, agents, skills, hooks, MCP, LSP
- [CLI Commands](./references/cli-commands.md) - Install, uninstall, enable, disable, update
- [Debugging](./references/debugging.md) - Common issues and troubleshooting

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required manifest
├── commands/                 # Slash commands (.md files)
├── agents/                   # Subagents (.md files)
├── skills/                   # Skills (subdirs with SKILL.md)
├── hooks/
│   └── hooks.json           # Hook configuration
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
└── scripts/                 # Hook and utility scripts
```

**Important:** Components go at plugin root, NOT inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

## Minimal plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief plugin description"
}
```

## Installation Scopes

| Scope | Location | Use case |
|-------|----------|----------|
| user | `~/.claude/settings.json` | Personal plugins (default) |
| project | `.claude/settings.json` | Team plugins via version control |
| local | `.claude/settings.local.json` | Project-specific, gitignored |
| managed | `managed-settings.json` | Read-only managed plugins |

## Environment Variables

Use `${CLAUDE_PLUGIN_ROOT}` for paths in hooks and MCP configs:

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
}
```

## Plugin Components Summary

| Component | Location | Format |
|-----------|----------|--------|
| Commands | `commands/` | Markdown with frontmatter |
| Agents | `agents/` | Markdown with frontmatter |
| Skills | `skills/*/SKILL.md` | Directories with SKILL.md |
| Hooks | `hooks/hooks.json` | JSON configuration |
| MCP servers | `.mcp.json` | MCP server config |
| LSP servers | `.lsp.json` | Language server config |

## CLI Quick Reference

```bash
# Install
claude plugin install <plugin>@<marketplace> --scope user

# Manage
claude plugin enable <plugin>
claude plugin disable <plugin>
claude plugin update <plugin>
claude plugin uninstall <plugin>

# Debug
claude --debug
```

## Permissions

**Problem:** Using `!` backticks to run plugin scripts fails with permission error:

```
Error: Bash command permission check failed for pattern
"!`${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh 2>&1 || true`":
This Bash command contains multiple operations.
```

**Cause:** `!` backticks have their own permission model separate from `allowed-tools`. Complex commands or scripts fail.

**Solution:** Use the Bash tool instead of `!` backticks for scripts:

```yaml
---
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh:*)
---

Run the script:
    ```bash
    ${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh
    ```
```

Simple git commands still work with `!` backticks: `!`git branch --show-current``

## Common Issues

**Plugin installed but commands don't appear?**

The plugin may be disabled. Check `~/.claude/settings.json`:

```json
"enabledPlugins": {
  "my-plugin@my-marketplace": false  // ← Disabled!
}
```

Fix with: `claude plugin enable my-plugin@my-marketplace` then restart Claude Code.

**Local changes not picked up?**

Use `claude plugin update <plugin>` or do a full reinstall:

```bash
claude plugin marketplace remove my-marketplace
claude plugin marketplace add ./
claude plugin install my-plugin@my-marketplace
```

## Important

After creating or modifying plugins, inform the user:

> **Plugin changes take effect immediately** after installation. Use `claude --debug` to verify plugin loading.

## Checklist

Before finalizing a plugin:

- [ ] `plugin.json` has name, version, description
- [ ] Components at plugin root (not in `.claude-plugin/`)
- [ ] All paths use `${CLAUDE_PLUGIN_ROOT}` variable
- [ ] Scripts are executable (`chmod +x`)
- [ ] Test with `claude --debug` to verify loading
