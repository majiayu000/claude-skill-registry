---
name: copilot-sync
description: Synchronize GitHub Copilot configuration files (agents, prompts, skills, instructions) from github-copilot-base template to existing codebases. Creates backups before overwriting. Use when updating Copilot configuration, syncing Copilot files, or bringing a project up to date. Triggers on sync copilot, update copilot, copilot sync, sync configuration.
---

# Copilot Sync Skill

> Synchronize GitHub Copilot configuration files from the base template to existing codebases.

---

## Triggers

Activate this skill when user mentions:

- "sync copilot", "copilot sync"
- "update copilot files", "update copilot configuration"
- "sync copilot config", "sync configuration"
- "bring project up to date with copilot"
- "#copilot-sync"

---

## Description

The **Copilot Sync** skill synchronizes all Copilot-related files from the `github-copilot-base` template to an existing codebase:

1. **Agents** - All `.github/agents/*.md` files
2. **Prompts** - All `.github/prompts/*.prompt.md` files
3. **Skills** - All `.github/skills/*/` directories
4. **Instructions** - `.github/copilot-instructions.md`
5. **PRP Framework** - `PRPs/` templates
6. **Supporting Docs** - Background workflow, style guides

**Key Features:**

- 💾 Automatic backups before overwriting
- 👁️ Dry-run mode for previewing changes
- ✅ Validation of target repository
- 📊 Detailed sync statistics

---

## Workflow Steps

### 1. Gather Information

Collect the following using `ask_user`:

| Question    | Purpose               | Validation                   |
| ----------- | --------------------- | ---------------------------- |
| Target path | Codebase to sync to   | Must exist, must be Git repo |
| Dry run?    | Preview changes first | Yes/No                       |

### 2. Validate Target

```powershell
# Check path exists
if (-not (Test-Path $TargetPath -PathType Container)) {
    Write-Error "Path does not exist"
}

# Check it's a Git repository
if (-not (Test-Path (Join-Path $TargetPath ".git"))) {
    Write-Error "Not a Git repository"
}
```

### 3. Execute Sync

**Dry Run (Preview):**

```powershell
$TemplateRepo = "E:\Repos\HouseGarofalo\github-copilot-base"
& "$TemplateRepo\scripts\sync-copilot.ps1" -TargetPath $TargetPath -DryRun
```

**Apply Changes:**

```powershell
$TemplateRepo = "E:\Repos\HouseGarofalo\github-copilot-base"
& "$TemplateRepo\scripts\sync-copilot.ps1" -TargetPath $TargetPath
```

**Force (No Prompts):**

```powershell
& "$TemplateRepo\scripts\sync-copilot.ps1" -TargetPath $TargetPath -Force
```

### 4. Post-Sync Guidance

After sync, guide user to:

1. **Review copilot-instructions.md** - Add project-specific context
2. **Check backups** - In `.copilot-backup/` folder
3. **Commit changes**:
   ```powershell
   git add .github PRPs docs
   git commit -m "chore: sync Copilot configuration from github-copilot-base"
   ```

### 5. Output Summary

Provide completion summary with:

- Files synced count
- New files count
- Backups created
- Next steps

---

## What Gets Synced

| Category            | Path                              | Description                      |
| ------------------- | --------------------------------- | -------------------------------- |
| Agents              | `.github/agents/`                 | 44+ custom agents                |
| Prompts             | `.github/prompts/`                | 50+ prompt files                 |
| Skills              | `.github/skills/`                 | 80+ skill definitions            |
| Chat Modes          | `.github/chatmodes/`              | Chat mode configs                |
| Instructions        | `.github/copilot-instructions.md` | Main instructions                |
| Background Workflow | `.github/BACKGROUND_WORKFLOW.md`  | Multi-agent docs                 |
| Copilot Config      | `.github/copilot/`                | Copilot settings                 |
| VS Code Settings    | `.vscode/`                        | Settings, extensions, MCP config |
| Copilot Ignore      | `.copilotignore`                  | Files excluded from Copilot      |
| Git Attributes      | `.gitattributes`                  | Line endings and file handling   |
| Pre-commit Config   | `.pre-commit-config.yaml`         | Secret detection (gitleaks)      |
| Worktree Helper     | `scripts/worktree-helper.ps1`     | Git worktree utilities           |
| PRP Framework       | `PRPs/`                           | Templates & docs                 |
| Style Guide         | `docs/STYLE_GUIDE.md`             | Doc standards                    |

---

## Options

| Option        | Description               | Default  |
| ------------- | ------------------------- | -------- |
| `-TargetPath` | Path to target codebase   | Required |
| `-DryRun`     | Preview only, no changes  | False    |
| `-NoBackup`   | Skip creating backups     | False    |
| `-Force`      | Skip confirmation prompts | False    |

---

## Backup & Recovery

**Backup Location:**

```
<target>\.copilot-backup\
├── .github\
│   ├── copilot-instructions.md.<timestamp>.backup
│   └── agents\*.backup
└── PRPs\*.backup
```

**Restore a File:**

```powershell
Copy-Item "<backup_file>" "<original_path>" -Force
```

---

## Error Handling

| Error              | Resolution                          |
| ------------------ | ----------------------------------- |
| Path doesn't exist | Provide valid path                  |
| Not a Git repo     | Initialize with `git init`          |
| Permission denied  | Check write access                  |
| Backup failed      | Use `-NoBackup` or check disk space |

---

## Prerequisites

- **Git** installed
- **Target** must be an existing Git repository
- **Write access** to target directory

---

## Example

```
User: #copilot-sync E:\Repos\MyOrg\my-project

Copilot: 🔄 Copilot Sync

Validating target... ✅
Target is a Git repository... ✅

Would you like to preview changes first?
> Yes

📋 Dry Run:
   Would sync: 150 files
   New: 45 | Updated: 105

Apply changes?
> Yes

Syncing... ✅
Backing up existing files... ✅

🎉 Sync Complete!
   Files synced: 150
   Backups: .copilot-backup/

Next steps:
1. Review .github/copilot-instructions.md
2. Commit changes
```

---

## Related

- [Copilot Sync Agent](../../agents/copilot-sync.agent.md)
- [Copilot Sync Prompt](../../prompts/copilot-sync.prompt.md)
- [Sync Script](../../../scripts/sync-copilot.ps1)
- [Project Wizard](../project-wizard/SKILL.md) - For new projects
