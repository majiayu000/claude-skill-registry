---
name: baseproject-update
description: Update an existing BaseProject installation by syncing skills, docs, and AGENT.md from the latest upstream. Use when you want to pull the newest BaseProject templates, skills, and guides into your project.
---

# BaseProject Update Skill

## When to Activate

Activate this skill when:
- Updating an existing BaseProject installation to latest
- Syncing skills or AgentUsage docs with upstream
- User says "update baseproject", "sync baseproject", or invokes `/baseproject-update`
- Refreshing project templates after upstream changes

## Prerequisites

- Project already has BaseProject installed (`.claude/skills/` and/or `AgentUsage/` exist)
- Git repository is clean (commit or stash changes first)

## Update Workflow

Execute these steps in order:

### Step 1: Verify Current State
```bash
# Confirm BaseProject is installed
ls .claude/skills/ AgentUsage/ AGENT.md 2>/dev/null

# Ensure git is clean
git status --porcelain
```

If git is dirty, warn the user and ask them to commit or stash first.

### Step 2: Clone Latest BaseProject
```bash
git clone --depth 1 https://github.com/AutumnsGrove/BaseProject.git /tmp/bp-update
```

### Step 3: Create Backup
```bash
BACKUP_DIR=".baseproject-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r .claude/skills/ "$BACKUP_DIR/skills-backup/" 2>/dev/null
cp -r AgentUsage/ "$BACKUP_DIR/AgentUsage-backup/" 2>/dev/null
cp AGENT.md "$BACKUP_DIR/AGENT.md.backup" 2>/dev/null
```

### Step 4: Sync Skills
Compare `.claude/skills/` with `/tmp/bp-update/.claude/skills/`:
- **Add** new skill directories that don't exist locally
- **Update** existing skills where upstream content has changed
- **Preserve** unchanged skills (skip if identical)
- Report: added, updated, unchanged counts

### Step 5: Sync AgentUsage Docs
Compare `AgentUsage/` with `/tmp/bp-update/AgentUsage/`:
- **Add** new files/directories from upstream
- **Update** existing files where upstream content has changed
- **Preserve** custom files that only exist locally (user additions)
- **Preserve** unchanged files (skip if identical)
- Report: added, updated, unchanged, custom-preserved counts

### Step 6: Merge .gitignore
```bash
# Add any new entries from upstream that aren't already present
# Never remove existing entries
```

### Step 7: Update AGENT.md
Intelligently merge AGENT.md:
- **Preserve** all project-specific content (purpose, tech stack, architecture, custom sections)
- **Update** BaseProject template sections (skills list, workflow references, tool instructions)
- **Add** any new template sections from upstream
- Use content analysis to distinguish template boilerplate from custom project content

### Step 8: Cleanup
```bash
rm -rf /tmp/bp-update
```

### Step 9: Commit
```bash
git add .claude/skills/ AgentUsage/ .gitignore AGENT.md
git commit -m "chore: sync BaseProject skills, docs, and agent config"
```

### Step 10: Display Summary
Show:
- Skills: added/updated/unchanged with full list of available skills
- AgentUsage: added/updated/unchanged/custom-preserved
- .gitignore: entries added (if any)
- AGENT.md: sections updated (if any)
- Backup location

## What Gets Updated

| Target | Action |
|--------|--------|
| `.claude/skills/` | Sync all skills from upstream |
| `AgentUsage/` | Sync docs, preserve custom files |
| `.gitignore` | Merge new entries |
| `AGENT.md` | Merge template sections, preserve custom content |

## What Is NOT Touched

- `README.md` - Your project README
- `TODOS.md` - Your task tracking reference (points to GitHub Issues)
- `secrets.json` / `secrets_template.json` - Your secrets
- `pyproject.toml` / `package.json` / `go.mod` - Language configs
- `src/` / `tests/` - Your source code
- Git hooks - Not installed or modified
- House agents - Not installed or modified

## Troubleshooting

### Clone fails
```bash
# If GitHub is unreachable, try with a local copy:
# cp -r /path/to/local/BaseProject /tmp/bp-update
```

### Merge conflicts in AGENT.md
If AGENT.md structure is too different to merge cleanly:
1. Keep the user's version
2. Append new sections at the end with a marker comment
3. Let the user reorganize manually

### Backup recovery
```bash
# Restore from backup if something went wrong
cp -r .baseproject-backup-*/skills-backup/ .claude/skills/
cp -r .baseproject-backup-*/AgentUsage-backup/ AgentUsage/
cp .baseproject-backup-*/AGENT.md.backup AGENT.md
```
