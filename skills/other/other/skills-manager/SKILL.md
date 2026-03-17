---
name: skills-manager
description: Get, List, install, update and uninstall agent skills. Use when user wants to Get, list, install, uninstall and upgrade skills. For install, user should provide a git repo URL.
metadata:
  author: concao
  version: "1.0"
---

# Skills Manager

This skill helps you Get, list, install, uninstall and update agent skills.

## Skill Metadata Format

Skills use YAML frontmatter in `Skill.md` with the following structure:

```yaml
---
name: skill-name              # Required
description: Brief description # Required
license: Apache-2.0           # Optional
metadata:                     # Optional
  author: example-org
  version: "1.0"
---
```

If `version` is not specified, the system uses the file's last modified time as the version identifier.

## Skills Storage Locations

Skills can be stored at two levels:

### 1. Machine-Level Cache (Centralized)

All downloaded skills are cached in: `%USERPROFILE%\.skill\{skill-name}\`

**Cache Structure:**
```
~/.skill/{skill-name}/
├── origin/           # Original files downloaded from remote repo
├── parsed/           # Processed skill files ready for installation
└── metadata.json     # Skill metadata
```

**metadata.json format:**
```json
{
  "name": "skill-name",
  "description": "Skill description",
  "version": "1.0",
  "lastUpdated": "2026-01-15T10:30:00Z",
  "source": {
    "repoUrl": "https://github.com/owner/repo",
    "relativePath": "skills/my-skill",
    "branch": "main"
  }
}
```

### 2. Agent-Level Storage
Skills are installed to agent-specific paths based on scope:

| Scope | Agent | Path |
|-------|-------|------|
| Project | Copilot (default) | `.github\skills\{skill-name}` |
| Project | Claude | `.claude\skills\{skill-name}` |
| Personal | Copilot (default) | `%USERPROFILE%\.copilot\skills\{skill-name}` |
| Personal | Claude | `%USERPROFILE%\.claude\skills\{skill-name}` |

**Default behavior:**
- If user doesn't specify agent preference: use Copilot paths (`.github/skills` or `~/.copilot/skills`)
- If user doesn't specify scope: default to **project scope**

## Instructions

### 1. List Skills

List all installed skills across all scopes.

**Steps:**
1. Scan all skill storage locations (project and personal)
2. Read the `Skill.md` file from each skill folder to extract name and description
3. Display results in a table format

**Script:** [list-skills.ps1](scripts/list-skills.ps1)

---

### 2. Get Skill Details

Get detailed information about a specific skill by name.

**Steps:**
1. Search for the skill in all installed locations
2. Parse the `Skill.md` file to extract name and full description
3. Display skill details including path and files

**Script:** [get-skill.ps1](scripts/get-skill.ps1) `-SkillName "name"`

---

### 3. Install Skills

Install a skill from a git repository URL.

**Steps:**

#### Step 3.1: Parse the Git Repository URL
When the user provides a git repository link, parse it to extract:
- **Repository URL**: The base git repo URL (e.g., `https://github.com/owner/repo`)
- **Relative Path**: The path to the skill folder within the repo (e.g., `skills/my-skill`)
- **Branch** (optional): If specified, use it; otherwise default to `main` or `master`

**Supported URL formats:**
- `https://github.com/owner/repo/tree/branch/path/to/skill`
- `https://github.com/owner/repo/path/to/skill`
- `https://dev.azure.com/org/project/_git/repo?path=/path/to/skill`
- Raw git URL + relative path provided separately

#### Step 3.2: Download to Machine Cache
1. Create cache structure: `~/.skill/{skill-name}/origin/` and `~/.skill/{skill-name}/parsed/`
2. Clone/download files to `origin/` folder
3. Validate skill structure (must contain `Skill.md` or `SKILL.md`)
4. Parse skill metadata and copy processed files to `parsed/` folder
5. Create `metadata.json` with name, description, version (from frontmatter or last modified time), and source info

**Script:** [download-skill.ps1](scripts/download-skill.ps1) `-SkillName "name" -RepoUrl "url" -RelativePath "path" [-Branch "branch"]`

#### Step 3.3: Ask User for Installation Scope
**Prompt the user to choose:**

> Where would you like to install this skill?
>
> 1. **Project scope** - Available only in this repository (default)
> 2. **Personal scope** - Available across all your projects
>
> Which scope do you prefer? (1 or 2, default: 1)

#### Step 3.4: Copy to Agent Path
Based on user's choice, copy from `~/.skill/{skill-name}/parsed/` to the appropriate agent path.

**Script:** [install-skill.ps1](scripts/install-skill.ps1) `-SkillName "name" -Scope "project|personal" -Agent "copilot|claude"`

#### Step 3.5: Confirm Installation
**Success message:**
```
✅ Skill "{skill-name}" installed successfully!

📁 Location: {target-path}
📄 Skill file: {target-path}/Skill.md
📦 Version: {version}

To use this skill, simply ask me about topics related to: {skill-description}
```

---

### 4. Upgrade Skills

Update an existing skill to the latest version from its source repository.

**Steps:**

#### Step 4.1: Read Metadata
1. Read `~/.skill/{skill-name}/metadata.json` to get source repo info
2. If metadata not found, prompt user for repo URL

#### Step 4.2: Update Origin Files
1. Pull latest changes to `~/.skill/{skill-name}/origin/`
2. Re-parse skill files to `~/.skill/{skill-name}/parsed/`
3. Update `metadata.json` with new version info

#### Step 4.3: Compare and Update Installed Locations
1. Compare version in cache with installed locations
2. Copy updated files from `parsed/` to all installed locations if newer
3. Remind user to reopen chat for changes to take effect

**Script:** [upgrade-skill.ps1](scripts/upgrade-skill.ps1) `-SkillName "name"`

#### Step 4.4: Confirm Upgrade
**Success message:**
```
✅ Skill "{skill-name}" upgraded successfully!

📦 New Version: {version}
Updated locations:
  - {location-1}
  - {location-2}
```

---

### 5. Uninstall Skills

Remove an installed skill from a specific scope.

**Steps:**

#### Step 5.1: Locate the Skill
1. Search for the skill in all installed locations
2. Display where the skill is installed

#### Step 5.2: Ask User What to Remove
**Prompt the user:**

> The skill "{skill-name}" is installed in the following locations:
> 1. `.github/skills/{skill-name}` (project)
> 2. `~/.copilot/skills/{skill-name}` (personal)
> 3. `~/.skill/{skill-name}` (machine cache)
>
> Which would you like to remove? (1/2/3/all)

#### Step 5.3: Remove the Skill

**Script:** [uninstall-skill.ps1](scripts/uninstall-skill.ps1) `-SkillName "name"`

#### Step 5.4: Confirm Removal
**Success message:**
```
✅ Skill "{skill-name}" uninstalled from {location}.
```

---

## Example Usage

**User request examples:**
- "List all installed skills"
- "Get details about sfi-handler skill"
- "Install the skill from https://github.com/myorg/skills/tree/main/sfi-handler"
- "Install skill from https://github.com/user/repo path: skills/my-skill to personal scope"
- "Upgrade my sfi-handler skill"
- "Uninstall the old-skill from my personal skills"

## Troubleshooting

### Common Issues

1. **Git not installed**: Ensure git is available in PATH
2. **Permission denied**: Run with appropriate permissions
3. **Invalid skill structure**: Skill folder must contain Skill.md or SKILL.md
4. **Network issues**: Check internet connectivity and repository access

### Validation Checklist

- [ ] Repository URL is accessible
- [ ] Skill folder contains Skill.md or SKILL.md
- [ ] Target directory is writable
- [ ] No naming conflicts with existing skills
