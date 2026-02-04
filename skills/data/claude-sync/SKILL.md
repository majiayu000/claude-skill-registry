---
name: claude-sync
version: 1.0.0
description: Synchronize Claude Code configuration files to existing codebases. Updates skills, CLAUDE.md, settings, and related configuration from a source template to target repositories. Includes automatic backup and dry-run capabilities.
---

# Claude Sync Skill

Synchronize Claude Code configuration files from a source template to existing codebases. Ensures projects stay up-to-date with the latest skills, configurations, and best practices.

## Triggers

Use this skill when:
- Syncing Claude Code configuration to an existing project
- Updating a codebase with the latest Claude settings
- Ensuring a project has all standard Claude Code files
- Migrating configurations between projects
- Keywords: claude sync, sync configuration, update claude config, sync skills, configuration sync

## Core Mission

Synchronize Claude Code configuration files from a template repository to existing codebases, ensuring every project has:
- Latest Claude Code skills
- Updated CLAUDE.md instructions
- Current settings and configurations
- Automatic backups of existing files

---

## What Gets Synced

| Category | Files/Folders | Description |
|----------|---------------|-------------|
| **Skills** | `.claude/skills/` | All custom Claude Code skills |
| **Settings** | `.claude/settings.json` | Claude Code configuration |
| **Instructions** | `CLAUDE.md` | Project-level Claude instructions |
| **MCP Config** | `.claude/mcp.json` | MCP server configurations |
| **Commands** | `.claude/commands/` | Custom slash commands |
| **Templates** | `.claude/templates/` | Code and document templates |
| **Pre-commit** | `.pre-commit-config.yaml` | Secret detection hooks |
| **Git Attributes** | `.gitattributes` | File handling config |

---

## Workflow

### Step 1: Validate Target Codebase

Before syncing, validate the target:

```bash
# Check if path exists
test -d "<target_path>"

# Check if it's a Git repository
test -d "<target_path>/.git"
```

**Validations:**
1. Path exists and is a directory
2. Path is an initialized Git repository
3. User has write permissions

### Step 2: Gather Information

Collect the following:

```markdown
1. **Source Path** - Template repository with source configurations
   - Must contain .claude/ directory
   - Example: E:\Repos\Templates\claude-code-base

2. **Target Path** - Full path to the codebase to sync
   - Must be an existing Git repository
   - Example: E:\Repos\MyOrg\my-project

3. **Dry Run?** - Preview changes without applying
   - Default: No (apply changes)
   - Recommended for first-time sync

4. **Create Backups?** - Backup existing files
   - Default: Yes
   - Backups stored in .claude-backup/
```

### Step 3: Preview Changes (Dry Run)

If dry run requested, show what would happen:

```markdown
## Dry Run Preview

### Files to Create (New)
- .claude/skills/new-skill/SKILL.md
- .claude/commands/new-command.md

### Files to Update (Overwrite)
- CLAUDE.md
- .claude/settings.json
- .claude/skills/existing-skill/SKILL.md

### Summary
- New files: 5
- Updated files: 12
- Total files: 17
```

### Step 4: Execute Sync

Perform the sync with backups:

```python
import shutil
import os
from datetime import datetime

# Create backup directory
backup_dir = os.path.join(target_path, ".claude-backup", datetime.now().strftime("%Y%m%d_%H%M%S"))
os.makedirs(backup_dir, exist_ok=True)

# For each file to sync
for source_file in sync_files:
    target_file = os.path.join(target_path, source_file)

    # Backup if exists
    if os.path.exists(target_file):
        backup_file = os.path.join(backup_dir, source_file + ".backup")
        os.makedirs(os.path.dirname(backup_file), exist_ok=True)
        shutil.copy2(target_file, backup_file)

    # Copy from source
    shutil.copy2(os.path.join(source_path, source_file), target_file)
```

### Step 5: Post-Sync Customization

After sync, guide user to customize:

1. **Review CLAUDE.md**
   - Add project-specific context
   - Update technology stack references
   - Add custom rules for this codebase

2. **Check for conflicts**
   - Review any customizations that may have been overwritten
   - Restore from backups if needed: `.claude-backup/`

3. **Commit changes**
   ```bash
   git add .claude CLAUDE.md
   git commit -m "chore: sync Claude Code configuration"
   ```

### Step 6: Provide Summary

Output a summary of the sync:

```markdown
# Claude Sync Complete!

## Sync Details

| Metric | Count |
|--------|-------|
| **Files Synced** | 150 |
| **New Files** | 45 |
| **Updated Files** | 105 |
| **Backups Created** | 105 |

## Target Codebase

- **Path:** E:\Repos\MyOrg\my-project
- **Backups:** E:\Repos\MyOrg\my-project\.claude-backup

## What Was Synced

- 80+ Claude Code skills
- CLAUDE.md instructions
- Settings and MCP configuration
- Custom commands
- Pre-commit configuration

## Next Steps

1. Review `CLAUDE.md` and add project context
2. Check `.claude-backup/` for any files you need to restore
3. Commit: `git add .claude CLAUDE.md && git commit -m "chore: sync Claude config"`
```

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Path doesn't exist | Ask for correct path |
| Not a Git repository | Ask to initialize with `git init` or choose different path |
| Permission denied | Check write permissions |
| Source path not found | Verify source template location |
| Backup failed | Check disk space, try without backup |

---

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| Source Path | Path to source configuration | Required |
| Target Path | Path to target codebase | Required |
| Dry Run | Preview changes only | False |
| No Backup | Skip creating backups | False |
| Force | Skip confirmation prompts | False |

---

## Backup & Recovery

### Backup Location

```
<target_path>/.claude-backup/
├── 20260122_143052/
│   ├── CLAUDE.md.backup
│   ├── .claude/
│   │   ├── settings.json.backup
│   │   ├── skills/
│   │   │   └── my-custom-skill/
│   │   │       └── SKILL.md.backup
│   │   └── ...
│   └── ...
└── ...
```

### Restore a File

```bash
# Find backups
find <target>/.claude-backup -name "*.backup"

# Restore a specific file
cp "<backup_file>" "<original_location>"
```

### Clean Up Backups

```bash
# Remove old backups (optional)
rm -rf <target>/.claude-backup
```

---

## Example Session

```
User: Sync Claude configuration to my project

Claude: I'll help you sync Claude Code configuration files.

Q1: What is the path to the source template?
> E:\Repos\Templates\claude-code-base

Q2: What is the path to the target codebase?
> E:\Repos\MyOrg\customer-api

Q3: Would you like to preview changes first (dry run)?
> Yes

Checking prerequisites... Done
Validating source path... Done
Validating target path... Done
Target is a Git repository... Done

## Dry Run Preview

Would create: .claude/skills/new-skill/SKILL.md
Would update: CLAUDE.md
... (more files)

Summary:
   Would sync: 150 files
   New files: 45
   Would update: 105

Q4: Apply these changes?
> Yes

Syncing files... Done
Creating backups... Done

Claude Sync Complete!

- Path: E:\Repos\MyOrg\customer-api
- Backups: E:\Repos\MyOrg\customer-api\.claude-backup

Next steps:
1. Review CLAUDE.md
2. Commit: git add .claude CLAUDE.md && git commit -m "chore: sync Claude config"
```

---

## Selective Sync

For partial syncs, you can specify categories:

```markdown
## Sync Options

- [ ] All (default)
- [ ] Skills only
- [ ] Settings only
- [ ] CLAUDE.md only
- [ ] Commands only
- [ ] Custom selection
```

### Skills Only

```bash
# Sync only the skills directory
rsync -av --backup --suffix=.backup \
  "<source>/.claude/skills/" \
  "<target>/.claude/skills/"
```

### CLAUDE.md Only

```bash
# Sync only CLAUDE.md
cp "<source>/CLAUDE.md" "<target>/CLAUDE.md"
```

---

## Best Practices

1. **Always backup first**: Enable backups on first sync
2. **Dry run first**: Preview changes before applying
3. **Review CLAUDE.md**: Add project-specific context after sync
4. **Commit promptly**: Commit synced changes before making modifications
5. **Regular syncs**: Schedule periodic syncs to stay current
6. **Check for conflicts**: Some skills may need project customization

---

## Related Skills

- [project-wizard](../project-wizard/SKILL.md) - For creating new projects
- [archon-workflow](../archon-workflow/SKILL.md) - For task management
- [git-workflow](../git-workflow/SKILL.md) - For Git operations
