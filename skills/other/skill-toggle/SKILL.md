---
name: skill-toggle
description: Enable, disable, and manage Claude Code skills. Use when the user asks to enable/disable/toggle/manage skills, check skill status, list skills, manage skill collections, or clean up the skills directory.
user-invocable: true
allowed-tools: Bash
---

# Skill Toggle

Manage personal skills and plugin skills from one CLI.

## Usage

```bash
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py <command> [args]
```

## Commands

| Command | Action |
|---------|--------|
| `list` | Show all skills with status (enabled/disabled), source, description |
| `list --enabled` | Only enabled skills |
| `list --disabled` | Only disabled skills |
| `list --plugins` | Only plugin skills |
| `disable <name> [name...]` | Disable one or more skills (personal: moves to `disabled/`, plugin: flips settings.json) |
| `enable <name> [name...]` | Enable one or more skills (reverse of disable) |
| `status <name>` | Show details for a specific skill |
| `search <query>` | Fuzzy match across all skill names and descriptions |
| `clean` | Move orphan directories (no SKILL.md), zip files, and stale `.sh` scripts to `disabled/orphans/` |
| `collection list` | Show all collections with skill/plugin counts |
| `collection create <name> <skills...>` | Define a new collection from explicit skill list |
| `collection save <name>` | Snapshot all currently-enabled skills as a collection |
| `collection show <name>` | List skills in a collection with current enabled/disabled status |
| `collection on <name>` | Enable all skills in the collection |
| `collection off <name>` | Disable all skills in the collection |
| `collection delete <name>` | Remove a collection definition |
| `collection add <name> <skills...>` | Add skills to existing collection |
| `collection remove <name> <skills...>` | Remove skills from existing collection |

## How It Works

**Personal skills**: Moved between `~/.claude/skills/<name>/` (enabled) and `~/.claude/skills/disabled/<name>/` (disabled). The `disabled/INDEX.md` is auto-regenerated after every operation.

**Plugin skills**: The `enabledPlugins` object in `~/.claude/settings.json` is toggled. Accepts both plugin names (`compound-engineering`) and namespaced skill names (`compound-engineering:deepen-plan`)—the skill suffix is stripped and the entire plugin is toggled either way.

**Collections**: Named groups of skills stored as JSON in `~/.claude/skills/skill-toggle/collections/`. Each collection lists personal skills and/or plugins that can be toggled as a unit. `collection on research` enables everything in the `research` collection; `collection off research` disables them. Collections are additive—turning one on only enables its skills, it doesn't disable anything outside the collection. Use `collection save` to snapshot your current enabled set.

## Examples

```bash
# Disable two personal skills
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py disable smolvlm llama-cpp

# Enable a previously disabled skill
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py enable webflow-migrate

# Disable a plugin (all its skills go with it)
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py disable agent-evaluation

# List only what's currently disabled
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py list --disabled

# Clean orphan dirs and zip files
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py clean

# Create a named collection of skills
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py collection create research academic-research ancient-near-east-research rlama exa-search linear-a-decipherment

# Snapshot all currently-enabled skills as a collection
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py collection save baseline

# Disable all skills in a collection at once
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py collection off research

# Re-enable a collection
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py collection on research

# Show what's in a collection with current status
python3 ~/.claude/skills/skill-toggle/scripts/skill_toggle.py collection show research
```
