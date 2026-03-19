---
name: skill-sharing
description: |
  Skillshare CLI reference and sharing workflows. Use when: (1) user says "share",
  "push", "sync skills", "skillshare", (2) managing extras (rules, commands, agents),
  (3) cross-machine sync, (4) team/org sharing setup, (5) hub or audit operations,
  (6) .skillignore configuration, (7) new team member onboarding with skills.
---

## Skill Sharing

Share skills, rules, commands, and agents across machines and teams using **Skillshare** (v0.17+) and a Git repository.

### Two Modes

| Mode | Source Directory | Scope | Shared Via |
|------|-----------------|-------|------------|
| **Global** (`-g`) | `~/.config/skillshare/skills/` | All projects | Git remote (Team Remote) |
| **Project** (`-p`) | `.skillshare/skills/` | This repo only | Committed to repo |

Skills in the **source** are synced to the **target** (`~/.claude/skills/`) where Claude uses them.

### Sharing Tiers

| Tier | Feature | License |
|------|---------|---------|
| **All paid users** | Install, sync, cross-machine push/pull | Solo, Team, Trial |
| **Team/Trial only** | Team Remote, tracked repos, organization features | Team, Trial |

### Primary Interface

**Use the Share page in the Pilot Shell Console dashboard** (`http://localhost:41777/#/share`):

- **Source & Sync card** — Project (first) and Global sections; Sync/Collect buttons appear when out of sync
- **Remote Share card** — configure git remotes, Push/Pull buttons for cross-machine sync
- **Assets grid** — merged view of all global + project skills with scope/type badges
- **Install from URL** — install skills globally or to a project
- **How does this work?** / **CLI Reference** — collapsed help sections

### Extras — First-Class Resource Management (v0.17+)

Extras manage non-skill resources (rules, commands, agents, prompts) with their own CLI command group. Each extra has a name, a source directory, and one or more target directories.

**Directory structure:**

```
~/.config/skillshare/
├── skills/           ← skill source
└── extras/           ← extras source root (new in v0.17)
    ├── rules/        ← synced to ~/.claude/rules
    ├── commands/     ← synced to ~/.claude/commands
    └── agents/       ← synced to ~/.claude/agents
```

**Core commands:**

```bash
# Create a new extra (interactive wizard or CLI flags)
skillshare extras init rules --target ~/.claude/rules --target ~/.cursor/rules
skillshare extras init rules -p --target .claude/rules          # project-scoped

# List extras with sync status per target
skillshare extras list                                           # interactive TUI
skillshare extras list --json -g                                 # JSON output

# Change sync mode for a target
skillshare extras mode rules --mode copy                         # single-target shorthand
skillshare extras mode rules --target ~/.claude/rules --mode copy

# Collect files from a target back into source
skillshare extras collect rules --from ~/.claude/rules
skillshare extras collect rules --from ~/.claude/rules --dry-run

# Remove an extra (source files preserved)
skillshare extras remove rules
```

**Sync modes:**

| Mode | Behavior |
|------|----------|
| `merge` (default) | Per-file symlinks from target to source |
| `copy` | Per-file copies |
| `symlink` | Entire directory symlink |

**Project-mode extras** — extras now work at project level (`-p`), not just global:

```bash
skillshare extras init rules -p --target .claude/rules
skillshare sync -p --all                                         # sync skills + extras
```

**Note:** Pilot-managed rules/commands (installed by the Pilot installer) are tracked via manifest and should NOT be placed in extras. Extras are for user-created assets you want to share across machines.

### Key Concepts

- **Sync**: Distributes assets from source to target. **Must run after every mutation** (`install`, `uninstall`, `update`, `collect`).
- **Collect**: Imports files from a target back into the source directory so they can be pushed/shared.
- **Team Remote**: Git remotes for **global skills only**. Project skills are shared by committing `.skillshare/` to the project repo instead.
- **Hub**: Curated skill catalogs. `skillshare hub add <url>` to subscribe, `skillshare hub index` to build one.
- **Audit**: Security scan on install. `skillshare audit --threshold high` for CI.

### Health Checks & Diagnostics

`skillshare doctor --json` provides machine-readable health checks for CI pipelines:

```bash
skillshare doctor                      # human-readable output
skillshare doctor --json               # structured JSON (CI-friendly)

# CI gate — fail if any errors
skillshare doctor --json | jq -e '.summary.errors == 0'

# Check .skillignore status
skillshare doctor --json | jq '.checks[] | select(.name == "skillignore")'
```

### .skillignore — Hide Skills from Discovery

Place a `.skillignore` at the source root or inside a tracked repo to hide skills from all commands. Uses full gitignore syntax:

```
# ~/.config/skillshare/skills/.skillignore
draft-*          # hide all draft skills
_archived/       # hide entire directory
test-fixture     # hide specific skill

# Negation, character classes, recursive globs also work
!test-important  # keep this one despite draft-* match
**/temp          # ignore temp at any depth
```

### Cross-Machine Sync and Organization Sharing

**Personal remote** — your skills across your machines:

```bash
skillshare init --remote git@github.com:you/my-skills.git  # first machine
skillshare push -m "Add skill"
# On another machine:
skillshare init --remote git@github.com:you/my-skills.git  # auto-pulls
skillshare pull
```

**Tracked repos** — team/org repos:

```bash
skillshare install github.com/my-team/team-skills --track --name team-skills
skillshare update --all && skillshare sync
```

**Centralized skills repo** (`--config local`) — one repo for skills, each developer manages own targets:

```bash
# Creator: set up the shared repo
skillshare init -p --config local --targets claude
git add .skillshare/ && git commit && git push

# Teammate: clone and configure own targets
git clone <repo> && cd <repo>
skillshare init -p                          # auto-detects shared repo mode
skillshare target add projB ~/DEV/projB/.cursor/skills -p
skillshare sync -p
```

**Org sharing pattern** (two-channel, used at scale):

| Channel | What it does | Who uses it |
|---------|-------------|-------------|
| Claude Code plugin marketplace | Auto-distributes to CC users via `extraKnownMarketplaces` in `.claude/settings.json` | All Claude Code users |
| Skillshare | Multi-tool sync (Windsurf/Cursor/Codex), discoverability UI, security audit | Windsurf users, curators |

Both channels read from the same repo — no lock-in, skills are plain markdown files.

**Hub Index** for org-wide discoverability:

```bash
cd ~/my-org/skills-directory
skillshare hub index --audit -o ./skillshare-hub.json
# Commit to repo — GitHub raw URL makes it searchable by anyone
```

### Tool Portability in Skills

Skills are shared with users who may not have Pilot Shell. **Only reference built-in Claude Code tools** in skill content:

| Use This (Built-in) | NOT This (Pilot-specific) |
|---------------------|--------------------------|
| `Grep`, `Glob` | `probe search/extract/query` |
| `Bash` + `npx playwright` | `playwright-cli` |
| `WebFetch`, `WebSearch` | Pilot MCP servers |
| `Bash` + standard CLI | `pilot` CLI, `skillshare` CLI |

If a skill requires a non-standard tool, list it as a prerequisite.

### /create-skill and /setup-rules Integration

`/create-skill` creates skills in `.skillshare/skills/` **if it exists** in the project (runs `skillshare sync -p` afterward). Otherwise falls back to `.claude/skills/`.

`/setup-rules` focuses exclusively on rules and AGENTS.md — it does not create skills.

### When to Use

| Situation | Action |
|-----------|--------|
| User says "share", "push", "sync skills" | Direct to Share page in Console |
| After `/create-skill` captures a new skill | Use Collect to import to source, then push |
| User wants skills on another machine | Set up Team Remote, push from source, pull on target |
| New team member onboarding | `skillshare install -p && skillshare sync -p` |
| Org-wide skill distribution | `skillshare install <url> --track` (Team plan) |
| Share rules/commands across machines | `skillshare extras init rules --target ~/.claude/rules` |
| Check setup health | `skillshare doctor` |

### Non-Interactive Usage (for Claude)

Claude cannot answer interactive prompts. Always use non-interactive flags:

| Action | Flags |
|--------|-------|
| Install without prompts | `--all` or `-s name1,name2` or `--yes` |
| Uninstall without confirmation | `--force` |
| Collect without confirmation | `--force` |
| Override audit block | `--force` or `--skip-audit` |
| Preview changes | `--dry-run` |
| Structured output | `--json` |

### CLI Quick Reference

```bash
# Skills — global
skillshare status -g && skillshare list -g
skillshare sync -g                            # sync skills only
skillshare sync -g --all                      # sync skills + extras
skillshare install <url> -g
skillshare collect -g && skillshare diff -g

# Skills — project
skillshare init -p
skillshare sync -p && skillshare sync -p --all
skillshare install <url> -p

# Extras (v0.17+)
skillshare extras init <name> --target <path> [-p|-g]
skillshare extras list [--json] [-p|-g]
skillshare extras mode <name> --mode merge|copy|symlink
skillshare extras collect <name> --from <path>
skillshare extras remove <name>

# Cross-machine sync (global only)
skillshare init --remote <url>
skillshare push -m "Add skill"
skillshare pull

# Health & discovery
skillshare doctor [--json]
skillshare audit [--threshold high]
skillshare hub add <url>
skillshare hub index --full

# Organization (Team/Trial)
skillshare install <url> --track              # tracked org repo
skillshare update --all                       # update all tracked repos
skillshare check                              # check for available updates
skillshare trash restore <name>               # recover deleted skill (7-day)
```

### Documentation

- [Quick Start](https://skillshare.runkids.cc/docs/learn/with-claude-code)
- [Extras Reference](https://skillshare.runkids.cc/docs/reference/commands/extras)
- [Cross-Machine Sync](https://skillshare.runkids.cc/docs/how-to/sharing/cross-machine-sync)
- [Project Setup](https://skillshare.runkids.cc/docs/how-to/sharing/project-setup)
- [Organization Sharing](https://skillshare.runkids.cc/docs/how-to/sharing/organization-sharing)
- [Full Command Reference](https://skillshare.runkids.cc/docs/reference/commands)
