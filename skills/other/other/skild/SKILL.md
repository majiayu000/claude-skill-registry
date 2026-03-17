---
name: skild
description: Skill package manager for AI Agents — install, manage, and publish Agent Skills.
version: 0.2.9
author: Peiiii
license: MIT
tags:
  - cli
  - package-manager
  - skills
---

# skild

**skild** is the package manager for Agent Skills — like npm, but for AI agents.

## When to Use

Use this skill when:
- Installing new capabilities for AI agents
- Managing installed Skills (list, update, uninstall)
- Publishing Skills to share with the community
- Searching or discovering new Skills

## Agent Search & Discovery (Skild Index)

When an agent needs to find Skills from the Skild index (registry + linked + auto catalog), use the Registry API:

```bash
# Unified discovery (registry + linked skills)
curl "https://registry.skild.sh/discover?q=<query>&limit=20"

# Resolve a short alias (optional)
curl "https://registry.skild.sh/resolve?alias=<alias>"
```

**Notes:**
- Prefer `alias` if present; it provides the shortest install command.
- Use the returned `install` string directly (quotes may appear when a `#ref` is required).
- If you need to browse linked items only:
  - `https://registry.skild.sh/linked-items?limit=20`
- CLI `skild search` uses the same unified index.

## Agent Workflow (Recommended)

1) Search via `/discover` and shortlist results by description/tags.  
2) Confirm with the user and pick the best match.  
3) Install using the provided `install` command (or alias).  
4) Manage using `skild list / info / update / uninstall / sync`.

## Prerequisites

Node.js ≥18 is required.

```bash
npm install -g skild
```

## Core Commands

### Install a Skill

```bash
# From GitHub (shorthand)
skild install owner/repo/path/to/skill

# From registry
skild install @publisher/skill-name

# From local directory
skild install ./my-skill
```

### List Installed Skills

```bash
skild list
```

Output groups Skills by type: Skillsets, Skills, Dependencies.

### Manage Skills

```bash
skild info <skill>       # Show details
skild update <skill>     # Update to latest
skild uninstall <skill>  # Remove
skild validate <path>    # Validate structure
```

### Search Registry

```bash
skild search <query>
```

Browse online: [hub.skild.sh](https://hub.skild.sh)

## Target Platforms

| Platform | Option | Global Path |
|----------|--------|-------------|
| Claude | `-t claude` (default) | `~/.claude/skills` |
| Codex | `-t codex` | `~/.codex/skills` |
| Copilot | `-t copilot` | `~/.github/skills` |
| Antigravity | `-t antigravity` | `~/.gemini/antigravity/skills` |
| OpenCode | `-t opencode` | `~/.config/opencode/skill` |
| Cursor | `-t cursor` | `~/.cursor/skills` |
| Windsurf | `-t windsurf` | `~/.windsurf/skills` |
| Agents | `-t agents` | `~/.agents/skills` |

```bash
# Example: Install to Antigravity
skild install @publisher/skill -t antigravity

# Project-level installation
skild install @publisher/skill --local
```

## Skillsets

Skillsets bundle multiple Skills for one-command installation:

```bash
skild install @skild/data-analyst-pack
# Installs: csv, pandas, sql-helper...
```

## Publishing Skills

```bash
# 1. Create account
skild signup

# 2. Login
skild login

# 3. Publish
skild publish --dir ./my-skill
```

## Push to Git Repos (Registry-free)

Use `skild push` to sync a Skill into a Git repository and push changes.

```bash
# Push to GitHub by owner/repo
skild push owner/repo --dir ./my-skill

# Set a default repo (omit <repo> afterwards)
skild config set push.defaultRepo owner/repo
skild push --dir ./my-skill

# Push to a local repo path
skild push ~/work/skills-repo --local --dir ./my-skill

# Push to a specific subdirectory
skild push owner/repo --dir ./my-skill --path skills/my-skill

# Push to a branch (or append #branch to the repo)
skild push owner/repo#dev --dir ./my-skill
```

**Notes:**
- The target path defaults to `skills/<skill-name>` derived from `SKILL.md`.
- Target path cannot be the repo root.
- The command clones, commits, and pushes to the remote branch.
- For `owner/repo`, skild tries SSH first and falls back to HTTPS if SSH auth fails.
- `skild push <repo>` always overrides the default repo.
- You can also set `SKILD_DEFAULT_PUSH_REPO` to override the default repo per shell.

## Command Reference

For the complete command reference with all options, see [commands.md](./commands.md).

## Skillsets

For detailed Skillsets guide (bundles of Skills), see [skillsets.md](./skillsets.md).

## Troubleshooting

For common issues and solutions, see [troubleshooting.md](./troubleshooting.md).

## More Info

- Website: [skild.sh](https://skild.sh)
- Hub: [hub.skild.sh](https://hub.skild.sh)
- Documentation: [GitHub](https://github.com/Peiiii/skild/tree/main/docs)
