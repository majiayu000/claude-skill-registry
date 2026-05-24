---
name: configure
description: Interactive SkillForge configuration wizard. Use when configuring settings, setting up MCP servers, customizing plugin.
context: inherit
version: 1.0.0
author: SkillForge
tags: [configuration, setup, wizard, customization]
user-invocable: true
---

# SkillForge Configuration

Interactive setup for customizing your SkillForge installation.

## When to Use

- Initial setup of SkillForge
- Customizing skill categories
- Toggling agents on/off
- Configuring hooks
- Enabling MCP integrations

## Quick Start

```bash
/configure
```

## Step 1: Choose Preset

Use AskUserQuestion:

| Preset | Skills | Agents | Hooks | Description |
|--------|--------|--------|-------|-------------|
| **Complete** | 78 | 20 | 92 | Everything |
| **Standard** | 78 | 0 | 92 | Skills, no agents |
| **Lite** | 10 | 0 | 92 | Essential only |
| **Hooks-only** | 0 | 0 | 92 | Just safety |

## Step 2: Customize Skill Categories

Categories available:
- AI/ML (26 skills)
- Backend (15 skills)
- Frontend (8 skills)
- Testing (13 skills)
- Security (7 skills)
- DevOps (4 skills)
- Planning (6 skills)

## Step 3: Customize Agents

**Product Agents (6):**
- market-intelligence
- product-strategist
- requirements-translator
- ux-researcher
- prioritization-analyst
- business-case-builder

**Technical Agents (14):**
- backend-system-architect
- frontend-ui-developer
- database-engineer
- llm-integrator
- workflow-architect
- data-pipeline-engineer
- test-generator
- code-quality-reviewer
- security-auditor
- security-layer-auditor
- debug-investigator
- metrics-architect
- rapid-ui-designer
- system-design-reviewer

## Step 4: Configure Hooks

**Safety Hooks (Always On):**
- git-branch-protection
- file-guard
- redact-secrets

**Toggleable Hooks:**
- Productivity (auto-approve, logging)
- Quality Gates (coverage, patterns)
- Team Coordination (locks, conflicts)
- Notifications (desktop, sound)

## Step 5: Configure MCPs (Optional)

All MCPs disabled by default. Enable selectively:

| MCP | Purpose |
|-----|---------|
| context7 | Library documentation |
| sequential-thinking | Complex reasoning |
| memory | Cross-session persistence |
| playwright | Browser automation |

## Step 6: CC 2.1.7 Settings (New)

Configure CC 2.1.7-specific features:

### Turn Duration Display

```
Enable turn duration in statusline? [y/N]: y
```

Adds to settings.json:
```json
{
  "statusline": {
    "showTurnDuration": true
  }
}
```

### MCP Auto-Deferral Threshold

```
MCP deferral threshold (default 10%): 10
```

Adds to config.json:
```json
{
  "cc217": {
    "mcp_defer_threshold": 0.10,
    "use_effective_window": true
  }
}
```

### Effective Context Window Mode

```
Use effective context window for calculations? [Y/n]: y
```

When enabled:
- Statusline shows `context_window.effective_percentage`
- Compression triggers use effective window
- MCP deferral more accurate


## Step 7: Preview & Save

Save to: `~/.claude/plugins/skillforge/config.json`

```json
{
  "version": "1.0.0",
  "preset": "complete",
  "skills": { "ai_ml": true, "backend": true, ... },
  "agents": { "product": true, "technical": true },
  "hooks": { "safety": true, "productivity": true, ... },
  "mcps": { "context7": false, ... }
}
```


## Related Skills
- doctor: Diagnose configuration issues
## References

- [Presets](references/presets.md)
- [MCP Configuration](references/mcp-config.md)