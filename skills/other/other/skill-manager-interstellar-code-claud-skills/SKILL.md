---
name: skill-manager
description: Native Python-based skill management for enabling/disabling skills, configuring permissions, and managing settings.local.json
version: 1.0.0
author: Generic Claude Code Framework
tags: [skill-management, permissions, configuration, settings, productivity, native-script]
auto-activate: false
---

# Skill Manager

**Native Python-based skill management for Claude Code - Zero token overhead!**

## 🎯 Purpose

This skill provides a **native Python script** that handles skill discovery, enabling/disabling, and permission management WITHOUT requiring LLM parsing. This saves 90% tokens compared to LLM-based skill management.

**Token Savings:**
- LLM-based approach: ~800-1000 tokens (reading 6+ skill files)
- This skill: ~50-100 tokens (single script execution)
- **Savings: 750-900 tokens per operation (90%)**

## 🔧 **BASH COMMAND ATTRIBUTION PATTERN**

**CRITICAL: Before executing EACH python/bash command, MUST output:**
```
🔧 [skill-manager] Running: <command>
```

**Examples:**
```
🔧 [skill-manager] Running: python .claude/skills/skill-manager/scripts/skill-manager.py discover
🔧 [skill-manager] Running: python .claude/skills/skill-manager/scripts/skill-manager.py enable cli-modern-tools
🔧 [skill-manager] Running: python .claude/skills/skill-manager/scripts/skill-manager.py toggle-feature cli-modern-tools eza
🔧 [skill-manager] Running: bash .claude/skills/colored-output/color.sh success "" "Configuration updated"
```

**Why:** This pattern helps users identify which skill is executing which command, improving transparency and debugging.

---

## 📋 Available Commands

### Discover & List Skills

```bash
# Discover all skills (formatted output)
python .claude/skills/skill-manager/scripts/skill-manager.py discover

# List all skills
python .claude/skills/skill-manager/scripts/skill-manager.py list

# List only enabled skills
python .claude/skills/skill-manager/scripts/skill-manager.py list --filter enabled

# List only disabled skills
python .claude/skills/skill-manager/scripts/skill-manager.py list --filter disabled

# Output as JSON (for Claude to parse)
python .claude/skills/skill-manager/scripts/skill-manager.py json
```

### Enable/Disable Skills

```bash
# Enable a skill
python .claude/skills/skill-manager/scripts/skill-manager.py enable colored-output

# Disable a skill
python .claude/skills/skill-manager/scripts/skill-manager.py disable time-helper
```

### View Skill Details

```bash
# Show detailed info about a skill
python .claude/skills/skill-manager/scripts/skill-manager.py status changelog-manager
```

### Export Configuration

```bash
# Export current configuration as JSON
python .claude/skills/skill-manager/scripts/skill-manager.py export
```

---

## 🎨 VISUAL OUTPUT FORMATTING

**Use colored-output skill for headers and results only (2 calls max):**

```bash
# START: Header only
bash .claude/skills/colored-output/color.sh skill-header "skill-manager" "Managing skills..."

# MIDDLE: Run Python script (produces formatted output)
python .claude/skills/skill-manager/scripts/skill-manager.py list

# END: Result only (if needed)
bash .claude/skills/colored-output/color.sh success "" "Configuration updated!"
```

---

## 🚀 Usage Workflow

### When User Invokes: `/cs-skill-management`

**Step 1: Run discovery script**

```bash
python .claude/skills/skill-manager/scripts/skill-manager.py json
```

**Output (JSON):**
```json
[
  {
    "skill_name": "changelog-manager",
    "name": "changelog-manager",
    "description": "Update project changelog...",
    "version": "2.8.0",
    "author": "Claude Code",
    "tags": ["changelog", "versioning"],
    "auto_activate": true,
    "enabled": true,
    "permissions": [
      "Skill(changelog-manager)",
      "Bash(python scripts/generate_docs.py:*)"
    ]
  },
  ...
]
```

**Step 2: Parse JSON and present interactive menu**

Claude receives the JSON, parses it instantly (no file reads needed!), and displays:

```
⚙️  Skill Management - Interactive Mode
========================================

Available Skills: 7 total
├─ Enabled: 4 skills
├─ Not Configured: 3 skills
└─ Categories: Release, CLI, Documentation, Time, Output, Development

1. View All Skills (7)
2. View Enabled Skills (4)
3. View Not Configured Skills (3)
4. Browse by Category
5. Search for Skill

🔧 Quick Actions:
6. Enable a Skill
7. Disable a Skill
8. Configure Skill Permissions
9. View Skill Details

Enter choice (1-9) or 'q' to quit:
```

**Step 3: Execute user choice**

If user chooses "6. Enable a Skill":

```bash
# User selects: colored-output
python .claude/skills/skill-manager/scripts/skill-manager.py enable colored-output
```

**Output:**
```
✅ Enabled: colored-output
```

Settings.local.json is automatically updated!

---

## 🔧 Quick Actions (Argument-Based)

Users can also call the slash command with arguments for instant actions:

```bash
# Quick enable
/cs-skill-management enable colored-output

# Quick disable
/cs-skill-management disable time-helper

# Quick status
/cs-skill-management status changelog-manager

# Quick list
/cs-skill-management list enabled
```

**Implementation:**

```bash
# Claude detects arguments and calls:
python .claude/skills/skill-manager/scripts/skill-manager.py enable colored-output
```

---

## 📊 Script Capabilities

### Discovery
- Scans `.claude/skills/` directory
- Parses YAML frontmatter from skill.md files
- Extracts: name, description, version, author, tags, auto-activate
- Checks enabled status from settings.local.json
- Identifies all permissions related to each skill

### Enable/Disable
- Adds/removes `Skill(skill-name)` from settings.local.json
- Identifies and removes related permissions (e.g., Bash permissions)
- Validates JSON before saving
- Provides clear success/error messages

### Status & Details
- Shows comprehensive skill information
- Lists all permissions
- Shows enabled/disabled status
- Displays tags, version, author

### Export
- Exports full configuration as JSON
- Can be used for backup/restore workflows
- Portable configuration format

---

## 🎯 Integration with /cs-skill-management Command

The slash command `.claude/commands/cs-skill-management.md` should be updated to:

```markdown
**When user invokes `/cs-skill-management [args]`:**

1. **Parse arguments** (if any)
2. **Run Python script** with appropriate action
3. **Display results** to user
4. **Handle interactive menu** (if no arguments)

**Examples:**

- `/cs-skill-management` → Interactive menu
- `/cs-skill-management enable colored-output` → Quick enable
- `/cs-skill-management list enabled` → Quick list
```

---

## ⚡ Token Efficiency

**Before (LLM-based):**
1. Read 7 skill.md files (30 lines each) = ~600 tokens
2. Read settings.local.json = ~50 tokens
3. Parse and format = ~150 tokens
4. **Total: ~800 tokens**

**After (Script-based):**
1. Run Python script = ~30 tokens
2. Parse JSON output = ~20 tokens
3. **Total: ~50 tokens**

**Savings: 750 tokens (94% reduction)**

---

## 🛠️ Implementation Notes

### Auto-Detection of Project Root
The script automatically finds the project root by searching for `.claude/` directory:

```python
current = Path.cwd()
while current != current.parent:
    if (current / '.claude').exists():
        self.project_root = current
        break
    current = current.parent
```

### Cross-Platform Compatibility
- Uses `pathlib.Path` for Windows/Mac/Linux compatibility
- Pure Python (no external dependencies)
- Works with Python 3.6+

### Error Handling
- Validates JSON before saving
- Handles missing files gracefully
- Provides clear error messages
- Safe fallbacks for parsing errors

### YAML Parsing
Simple frontmatter parser (no external deps):
- Extracts YAML between `---` markers
- Parses key: value pairs
- Handles arrays in tags field
- Falls back to defaults on errors

---

## 📝 Customization Points

### Adding New Actions
To add new script actions, modify `skill-manager.py`:

```python
# Add to argument choices
parser.add_argument('action',
                   choices=['discover', 'list', 'enable', 'disable',
                            'status', 'export', 'json', 'YOUR_ACTION'],
                   help='Action to perform')

# Add handler in main()
elif args.action == 'YOUR_ACTION':
    manager.your_custom_method()
```

### Custom Filtering
Add custom skill filters:

```python
def list_skills(self, filter_type: str = 'all') -> None:
    skills = self.discover_skills()

    if filter_type == 'by-tag':
        # Custom tag-based filtering
        skills = [s for s in skills if 'your-tag' in s['tags']]
```

---

## 🔍 Example Output

### Discover Command

```
$ python .claude/skills/skill-manager/scripts/skill-manager.py discover

📋 Skills (7 total)

✅ changelog-manager (v2.8.0)
   Update project changelog with uncommitted changes
   Permissions: 4 configured

✅ cli-modern-tools (v1.0.0)
   Auto-suggest modern CLI tool alternatives
   Permissions: 1 configured

⬜ colored-output (v1.0.0)
   Centralized colored output formatter
   Permissions: 0 configured

...
```

### Status Command

```
$ python .claude/skills/skill-manager/scripts/skill-manager.py status changelog-manager

📊 Skill Details: changelog-manager
============================================================

Basic Info:
  Name: changelog-manager
  Version: 2.8.0
  Description: Update project changelog with uncommitted changes
  Author: Claude Code

Status:
  ✅ Enabled
  Auto-activate: Yes

Permissions (4):
  ✅ Skill(changelog-manager)
  ✅ Bash(python scripts/generate_docs.py:*)
  ✅ Bash(git tag:*)
  ✅ Bash(git commit:*)

Tags:
  changelog, versioning, git, release-management
```

---

## 📦 File Structure

```
.claude/skills/skill-manager/
├── skill.md                    # This file (skill instructions)
├── scripts/
│   └── skill-manager.py        # Native Python script
└── README.md                   # User documentation (optional)
```

---

## 🚀 Future Enhancements

Potential additions:
1. **Interactive TUI** - Use `rich` or `textual` for terminal UI
2. **Skill Templates** - Generate new skills from templates
3. **Dependency Management** - Track skill dependencies
4. **Backup/Restore** - Automatic backup before changes
5. **Import Config** - Import exported configurations
6. **Batch Operations** - Enable/disable multiple skills at once
7. **Search** - Full-text search across skill descriptions

---

## Version History

### v1.0.0
- Initial release
- Native Python implementation
- Skill discovery and parsing
- Enable/disable functionality
- Status and details display
- JSON export
- Cross-platform support
- Zero external dependencies
