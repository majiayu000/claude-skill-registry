---
name: superdisco-moai-sync
description: Superdisco MoAI fork management - track customizations, sync upstream updates while preserving your changes
version: 1.0.0
tier: 3
author: Superdisco Agents
prefix: superdisco-
scripts:
  - scripts/check_version.py
  - scripts/check_agents.py
color: yellow
---

# Superdisco MoAI Sync Skill

## Purpose

Manage MoAI-ADK fork (`superdisco-agents/moai-adk`) with automatic customization tracking and upstream synchronization.

## Project Structure

```
/Users/rdmtv/Documents/claydev-local/projects-v2/moai-ir-deck/
├── .claude/                    # Claude Code configuration
│   ├── agents/moai/           # Custom & modified agents
│   ├── skills/                # Skills including this one
│   │   └── superdisco-moai-sync/  # THIS SKILL
│   └── commands/moai/         # Commands
├── .moai/                     # MoAI configuration
│   ├── config/config.json     # Project config (version here)
│   ├── customizations/        # MANIFEST & changelog
│   └── scripts/               # Utility scripts
├── moai-adk/                  # Local MoAI-ADK repository
│   └── src/moai_adk/templates/  # Template source
├── CLAUDE.md                  # Alfred execution directives
└── CLAUDE.local.md            # Local-only configuration
```

## Git Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              SUPERDISCO FORK WORKFLOW                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [upstream: modu-ai/moai-adk]                              │
│         │                                                   │
│         │ git fetch upstream                               │
│         ▼                                                   │
│  [Local moai-adk/]  ◄────── git merge (selective)          │
│         │                                                   │
│         │ git push origin                                  │
│         ▼                                                   │
│  [origin: superdisco-agents/moai-adk]                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Protected Files (Never Overwrite)

These files are tracked as customizations and protected during upstream sync:

### Custom Agents (superdisco prefix)
- `src/moai_adk/templates/.claude/agents/moai/builder-workflow-designer.md` (NEW)
- `src/moai_adk/templates/.claude/agents/moai/builder-reverse-engineer.md` (NEW)

### Modified Agents (TOON v4.0 integration)
- `src/moai_adk/templates/.claude/agents/moai/builder-workflow.md`
- `src/moai_adk/templates/.claude/agents/moai/builder-agent.md`
- `src/moai_adk/templates/.claude/agents/moai/builder-command.md`
- `src/moai_adk/templates/.claude/agents/moai/builder-skill.md`

### Custom Skills
- `src/moai_adk/templates/.claude/skills/moai-library-toon/`
- `.claude/skills/superdisco-moai-sync/` (this skill)

### Local-Only Files
- `CLAUDE.local.md`
- `.moai/config/config.json`
- `.claude/commands/moai/99-release.md`

## Commands

### Check Version Status
```bash
uv run .claude/skills/superdisco-moai-sync/scripts/check_version.py
```

### Check Agent & Skill Colors
```bash
uv run .claude/skills/superdisco-moai-sync/scripts/check_agents.py          # Human-readable table
uv run .claude/skills/superdisco-moai-sync/scripts/check_agents.py --json   # JSON output
uv run .claude/skills/superdisco-moai-sync/scripts/check_agents.py --verbose # Detailed output
```

### Track Customizations
```bash
uv run .claude/skills/superdisco-moai-sync/scripts/track_changes.py
```

### Sync Upstream
```bash
uv run .claude/skills/superdisco-moai-sync/scripts/sync_upstream.py --preview
uv run .claude/skills/superdisco-moai-sync/scripts/sync_upstream.py --apply
```

### Push to Fork
```bash
uv run .claude/skills/superdisco-moai-sync/scripts/push_fork.py --message "feat: description"
```

### Add Color Properties
```bash
# Preview changes without applying
uv run .claude/skills/superdisco-moai-sync/scripts/add_colors.py --dry-run

# Apply color updates
uv run .claude/skills/superdisco-moai-sync/scripts/add_colors.py --apply

# Process only agents or skills
uv run .claude/skills/superdisco-moai-sync/scripts/add_colors.py --agents
uv run .claude/skills/superdisco-moai-sync/scripts/add_colors.py --skills
```

**Color Scheme**:
- **Red**: Official MoAI (expert-*, manager-*, mcp-*, ai-*, builder-agent/skill/command, moai-*)
- **Yellow**: Custom Superdisco (builder-workflow-designer, builder-workflow, builder-reverse-engineer, superdisco-*)
- **Blue**: Claude Code default

### Validate Color Consistency (Planned)
```bash
# Meta checker to validate all agents have correct colors
uv run .claude/skills/superdisco-moai-sync/scripts/check_agents.py
```

## Modules

- `modules/customization-tracker.md` - Track all customizations
- `modules/upstream-sync.md` - Sync with modu-ai/moai-adk
- `modules/fork-workflow.md` - Git fork operations
- `modules/conflict-resolver.md` - Handle merge conflicts

## Integration with Agents

This skill is auto-loaded by:
- `manager-git` - For Git operations
- `builder-*` - For customization tracking

## Version History

| Version | Upstream | Date | Notes |
|---------|----------|------|-------|
| 1.0.0 | v0.31.2 | 2025-12-01 | Initial release |
