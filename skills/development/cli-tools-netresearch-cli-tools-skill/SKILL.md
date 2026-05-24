---
name: cli-tools
description: "Agent Skill: CLI tool management. Use when commands fail with 'command not found', installing tools, or checking project environments. By Netresearch."
---

# CLI Tools Skill

Manage CLI tool installation, environment auditing, and updates.

## Capabilities

1. **Reactive**: Auto-install missing tools on "command not found"
2. **Proactive**: Audit project dependencies and tool versions
3. **Maintenance**: Batch update all managed tools

## Triggers

**Reactive** (auto-install):
```
bash: <tool>: command not found
```

**Proactive** (audit): "check environment", "what's missing", "update tools"

## Workflows

### Missing Tool Resolution

1. Extract tool name from error
2. Lookup in `references/binary_to_tool_map.md` (e.g., `rg` → `ripgrep`)
3. Install: `scripts/install_tool.sh <tool> install`
4. Retry original command

### Environment Audit

```bash
scripts/check_environment.sh audit .
```

## Scripts

| Script | Purpose |
|--------|---------|
| `install_tool.sh` | Install/update/uninstall tools |
| `auto_update.sh` | Batch update package managers |
| `check_environment.sh` | Audit environment |
| `detect_project_type.sh` | Detect project type |

## Catalog (74 tools)

Core CLI, Languages, Package Managers, DevOps, Linters, Security, Git Tools

## References

- `references/binary_to_tool_map.md` - Binary to catalog mapping
- `references/project_type_requirements.md` - Project type requirements

---

> **Contributing:** https://github.com/netresearch/cli-tools-skill
