---
name: ai-dev-tools-sync
description: Synchronize and update Claude Code and GitHub Copilot development tool configurations to work similarly. Use when asked to update Claude Code setup, update Copilot setup, sync AI dev tools, add new skills/prompts/agents across both platforms, or ensure Claude and Copilot configurations are aligned. Covers skills, prompts, agents, instructions, workflows, and chat modes.
---

# AI Dev Tools Sync

Synchronize Claude Code and GitHub Copilot configurations to maintain feature parity.

## When to Use

Activate this skill when:
- User asks to update Claude Code or Copilot setup
- User wants to add/modify skills, prompts, agents, or instructions
- User wants both tools to work similarly
- User asks about AI dev tool configuration

## Quick Reference

| Claude Code | GitHub Copilot | Location |
|-------------|----------------|----------|
| SKILL.md | SKILL.md | `.claude/skills/` + `.github/skills/` |
| commands/*.md | prompts/*.prompt.md | `.claude/commands/` + `.github/prompts/` |
| agents/*.md | agents/*.md | `.github/agents/` (shared) |
| workflows/*.md | - | `.claude/workflows/` |
| CLAUDE.md | copilot-instructions.md | Root + `.github/` |
| - | instructions/*.md | `.github/instructions/` (applyTo patterns) |
| - | chatmodes/*.chatmode.md | `.github/chatmodes/` |

## Sync Process

### Step 1: Understand Current Setup

Read these files to understand current configuration:
```
.claude/workflows/orchestration-protocol.md
.claude/workflows/primary-workflow.md
.github/copilot-instructions.md
.github/AGENTS.md
CLAUDE.md
```

### Step 2: Research Latest Features

Search web for:
- "GitHub Copilot features setup 2026"
- "GitHub Copilot custom instructions agents skills prompts"
- "GitHub Copilot agent mode workspace context"

See [references/copilot-features.md](references/copilot-features.md) for feature catalog.

### Step 3: Identify Sync Opportunities

Compare capabilities and identify gaps:
- Skills missing in one platform
- Inconsistent prompt/instruction behavior
- Agent definitions that differ

### Step 4: Implement Changes

For each change:
1. **Skills**: Create in both `.claude/skills/` and `.github/skills/`
2. **Prompts**: Create in both `.claude/commands/` and `.github/prompts/`
3. **Instructions**: Update both `CLAUDE.md` and `.github/copilot-instructions.md`
4. **Agents**: Update `.github/agents/` (shared by both)

## Compatibility Notes

- Copilot reads `.claude/skills/` automatically (backward compatibility)
- Both read `.github/prompts/*.prompt.md`
- Both read `.github/agents/*.md`
- Both read `AGENTS.md` in root or `.github/`
- Both support path-based instruction files via `applyTo` in frontmatter

## References

- [Copilot Features Catalog](references/copilot-features.md)
- [Sync Patterns](references/sync-patterns.md)
