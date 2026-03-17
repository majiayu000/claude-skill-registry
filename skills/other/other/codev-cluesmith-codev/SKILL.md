---
name: codev
description: Codev project management CLI quick reference. Use when running codev commands to check correct syntax for init, adopt, update, and doctor.
disable-model-invocation: false
---

# codev - Project Management CLI

## Commands

```bash
codev init [name]          # Create a new codev project
codev init my-app -y       # Non-interactive with defaults
codev adopt                # Add codev to existing project (run from project root)
codev adopt -y             # Skip conflict prompts
codev update               # Update protocols, roles, skills from installed package
codev update --dry-run     # Preview changes without applying
codev update --force       # Force overwrite all framework files
codev doctor               # Check system dependencies
```

## What Each Command Does

### codev init
Creates a new project directory with codev structure: specs/, plans/, reviews/, protocols, CLAUDE.md, AGENTS.md, .claude/skills/, af-config.json, .gitignore.

### codev adopt
Adds codev to the **current directory**. Detects existing CLAUDE.md/AGENTS.md and creates `.codev-new` versions for merge if conflicts exist. Spawns Claude to merge automatically.

### codev update
Updates framework files (protocols, roles, skills) from the installed `@cluesmith/codev` package. **Never touches user data** (specs, plans, reviews). If you've customized a framework file, creates a `.codev-new` version for manual merge.

### codev doctor
Checks that all required dependencies are installed: Node.js (>=18), git (>=2.5), gh (authenticated), and at least one AI CLI (Claude, Gemini, or Codex).

## Common Mistakes

- There is NO `codev tower` command — Tower is managed via `af tower start` / `af tower stop`
- `codev init` creates a **new directory** — use `codev adopt` for existing projects
- `codev update` only updates framework files — it will never overwrite your specs/plans/reviews
- Always run `codev adopt` and `codev update` from the **project root directory**
