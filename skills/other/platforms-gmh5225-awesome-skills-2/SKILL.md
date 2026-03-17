---
name: agent-platforms
description: Guide for multi-platform skill compatibility across Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, and other AI coding agents.
---

# Multi-Platform Agent Skills

## Scope

Use this skill when:

- Ensuring skills work across multiple platforms
- Understanding platform-specific conventions
- Converting skills between platforms

## Platform Compatibility Matrix

| Platform | Skill Format | Project Path | Global Path |
|----------|--------------|--------------|-------------|
| **Amp** | SKILL.md | `.agents/skills/` | `~/.config/agents/skills/` |
| **Antigravity** | SKILL.md | `.agent/skills/` | `~/.gemini/antigravity/skills/` |
| **Claude Code** | SKILL.md | `.claude/skills/` | `~/.claude/skills/` |
| **Codex** | SKILL.md | `.codex/skills/` | `~/.codex/skills/` |
| **Cursor** | SKILL.md | `.cursor/skills/` | `~/.cursor/skills/` |
| **Gemini CLI** | SKILL.md | `.gemini/skills/` | `~/.gemini/skills/` |
| **GitHub Copilot** | SKILL.md | `.github/skills/` | `~/.copilot/skills/` |
| **Goose** | SKILL.md | `.goose/skills/` | `~/.config/goose/skills/` |
| **OpenCode** | SKILL.md | `.opencode/skills/` | `~/.config/opencode/skills/` |
| **Windsurf** | SKILL.md | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |

## Universal SKILL.md Format

All platforms use YAML frontmatter:

```yaml
---
name: skill-name
description: When to use this skill
---

# Instructions here...
```

## Cross-Platform Installation

Most tools auto-discover skills in `.agent/skills/`:

```bash
# Universal installation (works with most tools)
git clone https://github.com/user/skills .agent/skills
```

## Platform-Specific Notes

### Claude Code
- Auto-discovers from `.claude/skills/` and `~/.claude/skills/`
- Supports `/init` command for context bootstrapping

### Codex (OpenAI)
- Supports multiple scopes: REPO, USER, ADMIN, SYSTEM
- Built-in `$skill-creator` and `$skill-installer`
- Restart required after installing new skills

### GitHub Copilot
- Skills in `.github/skills/` directory
- Uses `SKILL.md` with `name` and `description` required
- Copilot auto-activates based on description match

### Gemini CLI
- Use `@` symbol to attach skill files to prompts
- Place skills in `.gemini/skills/` or `.agent/skills/`

## Conversion Tips

1. **Same SKILL.md format** works across platforms
2. **Change only the installation path** for different platforms
3. **Test on each target platform** before distribution
4. **Document platform-specific requirements** in skill README

## Full Resource List

For more detailed multi-platform skill resources, complete link lists, or the latest information, use WebFetch to retrieve the full README.md:

```
https://raw.githubusercontent.com/gmh5225/awesome-skills/refs/heads/main/README.md
```

The README.md contains the complete categorized resource list with all links.
