---
name: project-initialization
description: Initialize a project with AI agent rules and documentation. Use when setting up a new repository for AI agent collaboration.
---

# Project Initialization

Improve the results of running the `/init` command to create AI agent rules.

## When to Use This Skill

Use this skill when:
- Setting up a new repository for AI agent collaboration
- Neither `CLAUDE.md` nor `AGENTS.md` exists
- The `/init` command has been run but needs improvement
- You want AI agent rules to be discoverable by multiple agents

## Goal

The `/init` command creates `CLAUDE.md`, but this is only useful for Claude Code.
This skill ensures the same file contents are discoverable and readable by
multiple AI agents looking in different places.

This follows the standard documented at: https://agent-rules.org/

## Process

Perform the following steps:

1. **Check existing files**: Verify if `CLAUDE.md` and/or `AGENTS.md` exist

2. **Handle new project**: If neither file exists, first run Claude's `/init` process to generate initial content

3. **Rename if needed**: If `CLAUDE.md` exists, rename it to `AGENTS.md`

4. **Create symlinks**: Generate symlinks so different agents can find the rules:
   - `CLAUDE.md` → points to `AGENTS.md`
   - `AGENT.md` → points to `AGENTS.md` (for agents that look for this filename)

5. **Verify**: Confirm the symlinks work by checking file accessibility

## Context

- Existing files: `ls CLAUDE.md AGENTS.md`

## Example Commands

```bash
# Check existing files
ls -la CLAUDE.md AGENTS.md

# Rename if needed
mv CLAUDE.md AGENTS.md

# Create symlinks
ln -s AGENTS.md CLAUDE.md
ln -s AGENTS.md AGENT.md

# Verify
cat CLAUDE.md
cat AGENT.md
```

## Result

After this process:
- `AGENTS.md` contains the authoritative AI agent rules
- `CLAUDE.md` is a symlink to `AGENTS.md`
- `AGENT.md` is a symlink to `AGENTS.md`
- Multiple AI agents can discover and read the same rules
