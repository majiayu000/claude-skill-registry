---
name: configure-permissions
description: |
  Configure Claude Code permissions for work-issue auto mode.
  TRIGGER when: user wants to configure permissions ("configure permissions", "set up auto mode", "enable work-issue auto mode"), after framework sync with --configure-permissions flag, during project initialization.
  DO NOT TRIGGER when: user just wants to read about permissions, asks conceptual questions about auto mode, or wants to modify permissions manually.
version: "2.0.1"
allowed-tools: Bash(python3 *), Read, Write, Glob
disable-model-invocation: false
user-invocable: true
---

# Configure Permissions - Permission Configuration for work-issue Auto Mode

Configure Claude Code permissions to enable seamless work-issue auto mode execution.

## Overview

This skill configures `.claude/settings.json` with required permissions for work-issue auto mode.

**Two modes available:**

1. **Profile-aware mode** (default) - Detects project type and applies appropriate permissions
2. **Template mode** (NEW) - Use pre-defined or custom permission templates

**What it does:**
1. **Reads or creates** `.claude/settings.json`
2. **Detects project profile** (tauri, tauri-aws, nextjs-aws) OR **loads permission template**
3. **Generates permissions** based on profile or template
4. **Merges permissions smartly** without overwriting existing config
5. **Validates structure** to ensure correctness
6. **Reports changes** clearly

**Why it's needed:**
Without pre-configured permissions, work-issue auto mode stops at every bash command to ask for approval, defeating the purpose of automation. This skill pre-configures the required permissions for seamless execution.

**When to use:**
- After `/update-framework` to configure target project
- During project initialization with `init-project.py --configure-permissions`
- When setting up work-issue auto mode for the first time
- After changing project profile
- When you want different permission levels (full, safe, minimal, read-only)

## Arguments

```bash
/configure-permissions [target-path] [options]
```

**Common usage:**
```bash
# Profile-aware mode (default)
/configure-permissions              # Configure current project (auto-detect profile)
/configure-permissions ../u-safe    # Configure target project
/configure-permissions --dry-run    # Preview changes without applying

# Template mode (NEW in v2.0.0)
/configure-permissions --all        # Full automation (everything)
/configure-permissions --safe       # Safe automation (recommended)
/configure-permissions --minimal    # Basic operations only
/configure-permissions --read-only  # No modifications

# Custom templates
/configure-permissions --template=my-custom-template

# Combine with other flags
/configure-permissions --safe --dry-run
/configure-permissions --all ../other-project
```

**Options:**
- `[target-path]` - Optional, defaults to current directory
- `--dry-run` - Preview changes without modifying files
- `--profile <name>` - Override profile detection (tauri, tauri-aws, nextjs-aws)
- `--all` - Use 'all' template (full automation)
- `--safe` - Use 'safe' template (except critical operations) - **recommended**
- `--minimal` - Use 'minimal' template (basic operations)
- `--read-only` - Use 'read-only' template (no modifications)
- `--template <name>` - Use custom template by name

## Workflow

### Step 1: Create Todo List

**Initialize configuration tracking** using TaskCreate:

```
Task #1: Detect project profile
Task #2: Load or create settings.json (blocked by #1)
Task #3: Generate permission templates (blocked by #1)
Task #4: Merge permissions (blocked by #2, #3)
Task #5: Write updated settings (blocked by #4)
Task #6: Validate and report (blocked by #5)
```

After creating tasks, proceed with configuration execution.

## Required Permissions by Profile

### Official Tool Reference

**Documentation**: [Claude Code Tools Reference](https://code.claude.com/docs/en/tools-reference.md)

**Available tools** (see official docs for complete list):

| Tool | Purpose | Path Pattern Format |
|------|---------|---------------------|
| `Bash` | Terminal commands | Command string (e.g., "git add *") |
| `Read` | Read files | Gitignore-style globs (e.g., "**/*.ts") |
| `Write` | Write new files | Gitignore-style globs |
| `Edit` | Edit existing files | Gitignore-style globs |
| `Glob` | File pattern matching | Gitignore-style globs |
| `Grep` | Search file contents | Gitignore-style globs |
| `NotebookEdit` | Edit Jupyter notebooks | Gitignore-style globs (e.g., "**/*.ipynb") |
| `TaskCreate` | Create tasks | "*" (all) |
| `TaskUpdate` | Update tasks | "*" (all) |
| `TaskGet` | Get task details | "*" (all) |
| `TaskList` | List tasks | "*" (all) |
| `TaskOutput` | Read task output | "*" (all) |
| `TaskStop` | Stop background tasks | "*" (all) |
| `Agent` | Invoke subagents | Agent name (e.g., "Agent(Explore)", "Agent(Plan)") |
| `WebFetch` | Fetch web content | URL pattern (e.g., "https://github.com/*") |
| `WebSearch` | Web search | "*" (all) |
| `Skill` | Invoke skills | Skill name (e.g., "work-issue") |

**Path pattern format** (gitignore specification):
- `*` - Match any characters except `/`
- `**` - Match any characters including `/`
- `**/*.ts` - All TypeScript files recursively
- `.env*` - All files starting with `.env`
- `**/secrets/**` - All files in any `secrets/` directory

**Permission structure:**
```json
{
  "permissions": {
    "toolname": {
      "prompts": ["pattern1", "pattern2"],
      "blocked": ["blocked1", "blocked2"]
    }
  }
}
```

**Note**: Tool names are **lowercase** in settings.json (e.g., `bash`, `read`, `write`), but **PascalCase** in tool references.

### Minimal (all profiles)

**File operation and task management tools:**
```json
{
  "permissions": {
    "read": {
      "prompts": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.json", "**/*.md"],
      "blocked": [".env*", "**/.env*", "**/secrets/**", "**/*secret*", "**/*password*"]
    },
    "write": {
      "prompts": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.json", "**/*.md"],
      "blocked": [".env*", "**/.env*", "**/secrets/**", "**/node_modules/**"]
    },
    "edit": {
      "prompts": ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.json", "**/*.md"],
      "blocked": [".env*", "**/.env*", "**/secrets/**"]
    },
    "glob": {
      "prompts": ["**/*"],
      "blocked": [".env*", "**/.env*", "**/secrets/**"]
    },
    "grep": {
      "prompts": ["**/*"],
      "blocked": [".env*", "**/.env*", "**/secrets/**"]
    },
    "notebookedit": {
      "prompts": ["**/*.ipynb"],
      "blocked": []
    },
    "taskcreate": {"prompts": ["*"], "blocked": []},
    "taskupdate": {"prompts": ["*"], "blocked": []},
    "taskget": {"prompts": ["*"], "blocked": []},
    "tasklist": {"prompts": ["*"], "blocked": []},
    "taskoutput": {"prompts": ["*"], "blocked": []},
    "taskstop": {"prompts": ["*"], "blocked": []},
    "agent": {
      "prompts": ["Agent(Explore)", "Agent(Plan)"],
      "blocked": []
    },
    "webfetch": {
      "prompts": [
        "https://github.com/*",
        "https://docs.rs/*",
        "https://developer.mozilla.org/*",
        "https://stackoverflow.com/*"
      ],
      "blocked": []
    },
    "websearch": {"prompts": ["*"], "blocked": []},
    "bash": {
      "prompts": [
        "git add *", "git commit *", "git push *",
        "git checkout *", "git branch *", "git fetch *",
        "git merge *", "git worktree *",
        "git status *", "git diff *", "git log *",
        "gh issue *", "gh pr *"
      ],
      "blocked": ["git push --force", "git reset --hard", "rm -rf", "sudo *"]
    }
  }
}
```

### Node.js Projects (tauri, tauri-aws, nextjs-aws)

**Additional bash permissions:**
```json
{
  "bash": {
    "prompts": [
      "npm test",
      "npm run lint",
      "npm run build",
      "npm install",
      "npm ci"
    ]
  }
}
```

### Python Projects

**Additional bash permissions:**
```json
{
  "bash": {
    "prompts": [
      "pytest *",
      "python -m pytest *",
      "python -m *"
    ]
  }
}
```

### Rust Projects (Tauri)

**Additional bash permissions:**
```json
{
  "bash": {
    "prompts": [
      "cargo test",
      "cargo build",
      "cargo clippy",
      "cargo run"
    ]
  }
}
```

## Mode Selection: Template vs Profile

### Template Mode (Explicit Control)

Use permission templates for explicit permission levels:

```bash
/configure-permissions --all        # Everything (trusted environments)
/configure-permissions --safe       # Safe automation (recommended)
/configure-permissions --minimal    # Basic operations (learning)
/configure-permissions --read-only  # No writes (exploration)
```

**When to use:**
- Want explicit control over permission level
- Different security requirements
- Multiple projects with same permission needs
- CI/CD or trusted environments (--all)
- Learning or code review (--minimal, --read-only)

**Templates available:**
- `all` - Full automation (grants everything, **zero prompts**)
  - Bash: `["*"]` - All commands allowed
  - File operations: `["*", "**/*"]` - All files in all directories (no folder prompts)
  - Task tools: `["*"]` - All task operations
  - Web tools: `["*"]` - All web operations
  - Skill: `["*"]` - All skill invocations
  - **Use case**: Trusted environments, CI/CD, maximum automation
  - **Note**: No blocked operations - complete trust required
- `safe` - Safe automation (blocks destructive operations)
- `minimal` - Basic operations (git read, tests only)
- `read-only` - No modifications (git read only)
- Custom templates - Create your own in `framework/.claude-template/permission-templates/`

**See:** `framework/.claude-template/permission-templates/README.md` for complete template documentation

### Template: --all (Full Automation)

**The --all template provides complete, unrestricted access with zero permission prompts.**

**What it includes:**

```json
{
  "permissions": {
    "bash": {
      "prompts": ["*"],
      "blocked": []
    },
    "read": {
      "prompts": ["*", "**/*"],
      "blocked": []
    },
    "write": {
      "prompts": ["*", "**/*"],
      "blocked": []
    },
    "edit": {
      "prompts": ["*", "**/*"],
      "blocked": []
    },
    "glob": {
      "prompts": ["*", "**/*"],
      "blocked": []
    },
    "grep": {
      "prompts": ["*", "**/*"],
      "blocked": []
    },
    "notebookedit": {
      "prompts": ["*", "**/*.ipynb"],
      "blocked": []
    },
    "taskcreate": {"prompts": ["*"], "blocked": []},
    "taskupdate": {"prompts": ["*"], "blocked": []},
    "taskget": {"prompts": ["*"], "blocked": []},
    "tasklist": {"prompts": ["*"], "blocked": []},
    "taskoutput": {"prompts": ["*"], "blocked": []},
    "taskstop": {"prompts": ["*"], "blocked": []},
    "agent": {"prompts": ["*"], "blocked": []},
    "webfetch": {"prompts": ["*"], "blocked": []},
    "websearch": {"prompts": ["*"], "blocked": []},
    "skill": {"prompts": ["*"], "blocked": []}
  }
}
```

**Key features:**

1. **Zero folder prompts**: File operations use both `*` and `**/*` patterns
   - `*` - Matches files in current directory
   - `**/*` - Matches files in all subdirectories recursively
   - Result: No permission prompts when accessing new directories

2. **All bash commands**: Includes destructive operations
   - ✅ `git push --force`
   - ✅ `git reset --hard`
   - ✅ `rm -rf`
   - ✅ `sudo *`
   - ⚠️ Complete trust required

3. **All tool operations**: Every Claude Code tool granted full access
   - File operations: Read, Write, Edit, Glob, Grep, NotebookEdit
   - Task management: TaskCreate, TaskUpdate, TaskGet, TaskList, TaskOutput, TaskStop
   - Web access: WebFetch, WebSearch
   - Subagents: Agent (all types)
   - Skills: All skill invocations

**When to use:**
- CI/CD pipelines
- Trusted automation environments
- Internal tooling
- When you want absolutely zero interruptions

**Security warning:**
- Grants unrestricted access to all operations
- No safeguards against destructive commands
- Only use in trusted, isolated environments
- Not recommended for daily development work

**Example:**
```bash
/configure-permissions --all

# After configuration:
# - Edit any file in any folder → No prompt
# - Create new directories → No prompt
# - Run any git command → No prompt
# - Execute any bash command → No prompt
# - Invoke any skill → No prompt
```

### Profile-Aware Mode (Auto-Detection)

Detects project type and applies appropriate permissions:

```bash
/configure-permissions              # Auto-detect profile
/configure-permissions --profile tauri  # Override detection
```

**When to use:**
- Want automatic configuration based on project type
- Framework-managed projects
- Consistent permissions across similar projects

**Detection logic:**
```
1. Check for .framework-install file
   → profile: <name> field

2. If not found, check package.json
   → Node.js project (check for react, next, tauri)

3. If not found, check pyproject.toml
   → Python project

4. Default to tauri profile
```

**Profiles:**
- `tauri` - Desktop app (local): git + gh + npm + Tauri CLI
- `tauri-aws` - Desktop + cloud: tauri + AWS CLI + Lambda permissions
- `nextjs-aws` - Web full-stack: git + gh + npm + Next.js + AWS CLI

### Flag Precedence

**Mutually exclusive** - cannot use both template and profile:

```bash
# ✅ VALID
/configure-permissions --safe
/configure-permissions --profile tauri
/configure-permissions  # Auto-detect profile

# ❌ INVALID
/configure-permissions --safe --profile tauri  # Error: conflicting flags
```

**Priority:**
1. Template flag (`--all`, `--safe`, `--minimal`, `--read-only`, `--template`) → Use template
2. Profile flag (`--profile`) → Use specified profile
3. No flags → Auto-detect profile (default behavior)

## Permission Merging Logic

**Smart merging:**

```python
def merge_permissions(existing, new):
    # 1. Preserve existing allowedPrompts
    existing_prompts = existing.get("allowedPrompts", [])

    # 2. Add new prompts not already present
    for new_prompt in new["allowedPrompts"]:
        if not prompt_exists(existing_prompts, new_prompt):
            existing_prompts.append(new_prompt)

    # 3. Update settings
    existing["allowedPrompts"] = existing_prompts
    return existing

def prompt_exists(prompts, target):
    # Match by tool and prompt pattern
    for p in prompts:
        if p["tool"] == target["tool"] and p["prompt"] == target["prompt"]:
            return True
    return False
```

**Key principles:**
- Never remove existing permissions
- Add only missing permissions
- Preserve all other settings.json fields
- Maintain formatting and structure

## Recovery Using Git

With git version control, you can easily recover previous permission settings without needing automatic backups.

**View changes:**
```bash
# See what changed
git diff .claude/settings.json

# View full git history
git log .claude/settings.json
```

**Restore previous version:**
```bash
# Undo uncommitted changes
git restore .claude/settings.json

# Restore from specific commit
git show <commit-hash>:.claude/settings.json > .claude/settings.json
```

**Why no automatic backup:**
- Git provides complete version history
- Avoids clutter from backup files
- Single source of truth for all changes
- Standard recovery workflow across all skills

## Validation

**After configuration:**

```python
def validate_settings(settings):
    # Required fields
    assert "allowedPrompts" in settings
    assert isinstance(settings["allowedPrompts"], list)

    # Validate each prompt
    for prompt in settings["allowedPrompts"]:
        assert "tool" in prompt
        assert "prompt" in prompt
        assert prompt["tool"] in ["Bash", "Read", "Edit", "Write"]

    # Git operations present (critical for work-issue)
    git_prompts = [p for p in settings["allowedPrompts"] if "git" in p["prompt"]]
    assert len(git_prompts) >= 7  # add, commit, push, checkout, branch, fetch, merge

    return True
```

## Usage Examples

### Example 1: Configure Current Project

**User says:**
> "configure permissions for work-issue auto mode"

**What happens:**
1. Detect profile: nextjs-aws (from .framework-install)
2. Load settings.json (or create if missing)
3. Generate permissions: tools (9) + git (18) + npm (5) = 32 prompts
4. Merge: Add 29 new, preserve 3 existing
5. Write: Updated settings.json
6. Report: "✅ Configured 32 permissions (29 added, 3 existing)"

**Time:** ~8 seconds

### Example 2: Configure Target Project

**User says:**
> "configure permissions for u-safe project"

**What happens:**
1. `/configure-permissions ../u-safe`
2. Detect profile: tauri
3. Generate permissions: tools (9) + git (18) + npm (5) + tauri (2) = 34 prompts
4. Create settings.json (didn't exist)
5. Write: New settings.json with 34 permissions
6. Report: "✅ Created settings.json with 34 permissions"

**Time:** ~10 seconds

### Example 3: Dry Run Preview

**User says:**
> "preview permission changes without applying"

**What happens:**
1. `/configure-permissions --dry-run`
2. Detect profile: nextjs-aws
3. Generate permissions: 18 prompts
4. Compare with existing: 10 existing, 8 to add
5. Show diff:
   ```
   📋 Dry Run - Preview Changes

   Would add 8 permissions:
   + {"tool": "Bash", "prompt": "npm run lint"}
   + {"tool": "Bash", "prompt": "npm run build"}
   + ... (6 more)

   Would preserve 10 existing permissions

   No changes written (dry run mode)
   ```

**Time:** ~5 seconds

## Integration with update-framework

**Called automatically:**

```bash
/update-framework ../target --configure-permissions
```

**Workflow:**
1. update-framework syncs Pillars, Rules, Workflow, Skills
2. Calls configure-permissions skill automatically
3. Shows permission summary in final report

**Example output:**
```
Framework Sync Complete! (36 files updated)

Permissions Configured:
✅ Detected profile: nextjs-aws
✅ Added 12 new permissions
✅ Preserved 3 existing permissions

work-issue auto mode ready!
```

## Integration with init-project

**Called during initialization:**

```bash
python3 scripts/init-project.py --profile=tauri-react --name=my-app --configure-permissions
```

**Workflow:**
1. init-project creates project structure
2. Installs framework files
3. Calls configure-permissions automatically
4. Project ready for work-issue auto mode

**Default behavior:**
- `--configure-permissions` flag optional (defaults to True)
- Can opt-out with `--no-configure-permissions`

## Error Handling

### Invalid Target Path

```
❌ Error: Project not found

Path: ../nonexistent
Expected: ../nonexistent/.claude/

Please check:
1. Path is correct
2. Project has .claude/ directory
3. You have write permissions
```

### Invalid Profile

```
❌ Error: Unknown profile

Profile: invalid-profile
Valid profiles:
- tauri
- tauri-aws
- nextjs-aws

Fix: Use --profile with valid profile name
```

### Permission Denied

```
❌ Error: Cannot write to settings.json

File: .claude/settings.json
Reason: Permission denied

Please check:
1. File is not read-only
2. No other process is locking the file
3. You have write permissions to .claude/
```

### Invalid settings.json

```
❌ Error: Invalid JSON in settings.json

File: .claude/settings.json
Error: Unexpected token at line 15

Options:
1. Fix manually and retry
2. Restore from git: git restore .claude/settings.json
3. View previous version: git show HEAD:.claude/settings.json
```

## Safety Features

**Pre-flight checks:**
- ✅ Target path exists and has .claude/ directory
- ✅ User confirmation before changes (unless in auto mode)
- ✅ Dry-run preview available
- ✅ Git version control for recovery

**Smart merging:**
- Never removes existing permissions
- Only adds missing permissions
- Preserves all other settings fields
- Maintains JSON structure

**Validation:**
- Ensures valid JSON structure
- Validates required fields
- Checks permission format
- Verifies git operations present

## Best Practices

1. **Run after framework installation:**
```bash
# New project
python3 scripts/init-project.py --profile=nextjs-aws --name=my-app --configure-permissions

# Existing project
/update-framework ../target --configure-permissions
```

2. **Use dry-run for preview:**
```bash
/configure-permissions --dry-run
/configure-permissions --dry-run ../target
```

3. **Profile-specific configuration:**
```bash
# Override auto-detection
/configure-permissions --profile=tauri

# Target specific project type
/configure-permissions ../python-api --profile=python-fastapi
```

4. **Verify after configuration:**
```bash
# Check settings.json
cat .claude/settings.json | jq '.allowedPrompts'

# Test work-issue auto mode
/work-issue 123 --auto
```

## Output Examples

### Successful Configuration

```
📋 Configuring permissions for work-issue auto mode

1. Detecting profile...
   ✅ Found profile: nextjs-aws (from .framework-install)

2. Loading settings.json...
   ✅ Found existing settings

3. Generating permission templates...
   ✅ Generated 15 permissions (git: 10, npm: 5)

4. Merging permissions...
   ✅ Added 12 new permissions
   ✅ Preserved 3 existing permissions

5. Writing updated settings...
   ✅ Updated .claude/settings.json

6. Validating configuration...
   ✅ Valid structure
   ✅ All git operations present
   ✅ All npm operations present

✅ Configuration complete!

work-issue auto mode is now ready to run without permission prompts.
```

### Dry Run Output

```
📋 Dry Run - Preview Changes (no files modified)

Profile: nextjs-aws
Target: .claude/settings.json

Would add 8 permissions:
+ {"tool": "Bash", "prompt": "npm run lint"}
+ {"tool": "Bash", "prompt": "npm run build"}
+ {"tool": "Bash", "prompt": "npm test"}
+ {"tool": "Bash", "prompt": "npm install"}
+ {"tool": "Bash", "prompt": "npm ci"}
+ {"tool": "Bash", "prompt": "gh issue *"}
+ {"tool": "Bash", "prompt": "gh pr *"}
+ {"tool": "Bash", "prompt": "git worktree *"}

Would preserve 10 existing permissions

Total permissions after merge: 18

✅ Dry run complete - no changes written
```

## Task Management

**After each configuration step**, update progress:

```
Profile detected → Update Task #1
Settings loaded → Update Task #2
Templates generated → Update Task #3
Permissions merged → Update Task #4
Settings written → Update Task #5
Validation passed → Update Task #6
```

Provides real-time visibility of configuration progress.

## Final Verification

**Before declaring configuration complete**, verify:

```
- [ ] All 6 configuration tasks completed
- [ ] Profile detected or specified
- [ ] settings.json exists
- [ ] All git permissions present
- [ ] Profile-specific permissions added
- [ ] JSON structure validated
- [ ] Configuration summary displayed
```

Missing items indicate incomplete configuration.

**Recovery available via git:**
Use `git restore .claude/settings.json` to undo changes if needed.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list for progress tracking
2. **TaskUpdate** during execution - Mark tasks in_progress → completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/update-framework** - Calls this skill with --configure-permissions flag
- **/work-issue** - Benefits from configured permissions (auto mode)
- **/start-issue** - Uses git/gh permissions for branch creation
- **/finish-issue** - Uses git/gh permissions for PR and merge

---

**Version:** 2.0.1
**Pattern:** Tool-Reference (guides configuration process)
**Compliance:** ADR-001 ✅ | WORKFLOW_PATTERNS.md ✅
**Last Updated:** 2026-03-20
**Changelog:**
- v2.0.1 (2026-03-20): Fixed folder access prompts in --all mode (Issue #271)
  - Added dual wildcard patterns (`*` and `**/*`) to all.json
  - Ensures zero permission prompts for file operations in all directories
- v2.0.0 (2026-03-14): Added permission template support (--all, --safe, --minimal, --read-only, --template)
- v1.0.0: Initial release with profile-aware configuration
