---
name: setup-harness
description: Copy Claude Code harness into a project directory for version control. Use when user wants to set up the harness or when they say "setup harness", "copy harness", "install harness", or provide a harness path.
title: "Setup Harness"
status: active
---

# Setup Harness Skill

Copies the Claude Code harness into project directories so it becomes part of the Git repository.

## Trigger Patterns

- User says "setup harness"
- User provides a path to claude-code-harness
- User says "copy the harness", "install harness configuration"
- User asks how to use the harness in a new project

## What This Skill Does

Deploys harness files from the source to target project(s) using `deploy-harness.sh`:
1. Syncs `.claude/` directory (excluding runtime files) via rsync
2. Creates runtime directories with `.gitkeep` files
3. Updates `.gitignore` for runtime exclusions
4. Installs git hooks (doc-gardener pre-push)
5. Optionally copies `.mcp.json`

## Why Copy Instead of Symlink?

- **Version Control**: `.claude/` becomes part of your repo
- **Self-Contained**: No external dependencies
- **CI/CD Ready**: Works in pipelines without the source harness
- **Project-Specific**: Customize without affecting other projects

---

## Deployment Script

**All deployment logic is implemented in `deploy-harness.sh`.**

The script lives at `.claude/skills/setup-harness/deploy-harness.sh` and handles the full
deployment lifecycle: source validation, rsync with exclusions, runtime directory creation,
.gitignore updates, git hook installation, and verification.

### Usage

**Deploy to all configured targets:**
```bash
.claude/skills/setup-harness/deploy-harness.sh
```

**Deploy to a specific path:**
```bash
.claude/skills/setup-harness/deploy-harness.sh --target ~/Documents/Windsurf/my-project
```

**Deploy to a named target:**
```bash
.claude/skills/setup-harness/deploy-harness.sh --name my-project
```

**Preview without changes:**
```bash
.claude/skills/setup-harness/deploy-harness.sh --dry-run
```

**List configured targets:**
```bash
.claude/skills/setup-harness/deploy-harness.sh --list
```

**Include .mcp.json:**
```bash
.claude/skills/setup-harness/deploy-harness.sh --target ~/proj --include-mcp
```

### Targets Configuration

Deployment targets are configured in `targets.json` (same directory as this skill).
Edit `targets.json` to add or remove targets. The `~` in paths is expanded at runtime.

---

## Interactive Workflow (When Claude Runs This Skill)

When triggered by a user, Claude should:

### Step 1: Determine Target

If the user specified a path, use it directly. Otherwise, ask:

```
Question: "Where do you want to set up the Claude Code harness?"
Header: "Target Dir"
Options:
1. "All configured targets (Recommended)" - Deploy to all targets in targets.json
2. "Specify path" - Provide a custom directory path

multiSelect: false
```

### Step 2: Handle .mcp.json

```
Question: "How do you want to handle .mcp.json?"
Header: "MCP Config"
Options:
1. "Skip it (Recommended)" - Don't copy .mcp.json (API keys differ per project)
2. "Copy it" - Copy .mcp.json to target (remember to update API keys)

multiSelect: false
```

### Step 3: Run the Script

Based on user choices, construct and run the appropriate command:

```bash
# Example: Deploy to all targets without .mcp.json
.claude/skills/setup-harness/deploy-harness.sh

# Example: Deploy to specific path with .mcp.json
.claude/skills/setup-harness/deploy-harness.sh --target /path/to/project --include-mcp
```

### Step 4: Report Results

The script outputs verification results. Summarize for the user and remind them to:
1. Review `.claude/CLAUDE.md` (harness docs — updated each deploy)
2. Review `.mcp.json` API keys (if copied)
3. Commit the `.claude/` directory to git

---

## What the Script Does (Reference)

The following steps are all handled by `deploy-harness.sh`. They are documented here
for reference only — Claude should NOT execute these manually.

### Source Validation
- Checks harness source exists with `settings.json` and `skills/`
- Warns about stale state/progress files in source

### rsync with Exclusions
Copies `.claude/` while excluding runtime artifacts:
- `/state/*` — Runtime state files
- `/completion-state/` — Session completion tracking
- `/progress/*` — Session progress files
- `/worker-assignments/*` — Worker task assignments
- `/logs/` — Log files
- `*.log`, `.DS_Store`, `__pycache__/`, `*.pyc`, `node_modules/`
- `settings.local.json` — Local overrides

**Important**: `scripts/completion-state/` (CLI tools) ARE copied.
Only the top-level runtime directories are excluded.

### .claude/CLAUDE.md Handling
- `.claude/CLAUDE.md` is harness documentation — ALWAYS overwritten from source
- `CLAUDE.md` at project root is project-specific — NEVER touched

### Runtime Directory Creation
Creates excluded directories with `.gitkeep` so git tracks the structure:
- `state/`, `progress/`, `worker-assignments/`
- `completion-state/` (with subdirs: `default/`, `history/`, `promises/`, `sessions/`)

### .gitignore Updates
Appends Claude Code runtime exclusion entries if not already present.

### Git Hook Installation
Installs doc-gardener pre-push hook via `attractor/cli.py install-hooks`.
Skips gracefully for non-git targets or existing non-symlink hooks.

---

## Files Copied vs Excluded

### Copied (version controlled)
- `settings.json` — Core configuration
- `skills/` — All skill definitions
- `hooks/` — Lifecycle hooks
- `output-styles/` — Agent behavior definitions
- `scripts/` — CLI utilities (includes `scripts/completion-state/`)
- `commands/` — Slash commands
- `schemas/` — JSON schemas
- `tests/` — Hook tests
- `agents/` — Agent configurations
- `documentation/` — Architecture docs
- `validation/` — Validation agent configs
- `learnings/` — Multi-agent coordination guides

### Excluded (runtime, gitignored)
- `state/*` — Directory kept with .gitkeep
- `completion-state/*` — Subdirs created: default/, history/, promises/, sessions/
- `progress/*` — Directory kept with .gitkeep
- `worker-assignments/*` — Directory kept with .gitkeep
- `logs/` — Log files
- `settings.local.json` — Local overrides

---

## Example Interaction

```
User: Setup harness in ~/Documents/Windsurf/new-project

Claude: Running deploy-harness.sh --target ~/Documents/Windsurf/new-project

[Script output with verification results]

Harness deployed successfully. 550 files synced. Next steps:
1. Review .claude/CLAUDE.md
2. Commit .claude/ to git
3. Launch: ccsystem3 | ccorch | launchcc
```

```
User: Deploy harness to all targets

Claude: Running deploy-harness.sh (deploying to all configured targets)

[Script deploys to my-project and my-project]

Both targets updated successfully.
```
