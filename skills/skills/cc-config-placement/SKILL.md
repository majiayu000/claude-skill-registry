---
name: cc-config-placement
description: Use when adding rules, commands, or skills to dotfiles - decides global vs project-local placement
---

# CC Config Placement

Decide whether Claude Code config belongs in global (`claude/`) or project-local (`.claude/`).

## The Two Levels

| Path | Symlink Direction | Scope |
|------|-------------------|-------|
| `dotfiles/claude/` | `~/.claude/*` symlinks point here | All projects (global) |
| `dotfiles/.claude/` | Not symlinked | Dotfiles repo only |

## Symlink Structure

`~/.claude/` contains symlinks pointing **into** `dotfiles/claude/`:

```
~/.claude/
├── CLAUDE.md      → dotfiles/claude/CLAUDE.md
├── commands/      → dotfiles/claude/commands/
├── rules/         → dotfiles/claude/rules/
├── scripts/       → dotfiles/claude/scripts/
├── skills/        → dotfiles/claude/skills/
└── settings.json  (real file, NOT symlinked)
```

**Exception:** `settings.json` - the real file lives at `~/.claude/settings.json`. For version control visibility, `dotfiles/claude/settings.json` symlinks TO it (reverse direction).

## Decision Guide

**Global (`dotfiles/claude/`):**
- Communication preferences, work style
- Commit format, API rules
- Skills/commands useful across all projects
- Settings changes → edit `~/.claude/settings.json` directly

**Project-local (`dotfiles/.claude/`):**
- Dotfiles-specific conventions
- Commands like `/audit`
- Rules scoped to specific dotfiles

## When Ambiguous

Ask: "Should this apply globally (all projects) or just to dotfiles?"

Ambiguous examples:
- "Add a rule about X" → which level?
- "Create a command for Y" → global or local?
- "Remember that I prefer Z" → sounds global, confirm

## File Structure

```
dotfiles/
├── claude/                    ← ~/.claude/* symlinks point here (GLOBAL)
│   ├── CLAUDE.md
│   ├── commands/
│   ├── rules/
│   ├── scripts/
│   ├── skills/
│   └── settings.json          → ~/.claude/settings.json (reverse symlink)
│
└── .claude/                   ← PROJECT-LOCAL (dotfiles repo only)
    ├── CLAUDE.md
    ├── settings.json
    ├── settings.local.json
    ├── skills/
    └── rules/
```
