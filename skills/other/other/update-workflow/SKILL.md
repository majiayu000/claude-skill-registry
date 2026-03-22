---
name: update-workflow
description: |
  Sync workflow documentation between projects - CLAUDE.md and .claude/workflow/ files.
  TRIGGER when: user wants to sync workflow docs ("update workflow from X", "sync workflow", "pull workflow from framework", "push workflow to project").
  DO NOT TRIGGER when: user wants to update pillars/rules/skills (use respective update-* skills), or just wants to read workflow docs.
version: "2.1.0"
allowed-tools: Bash(cp *), Bash(mkdir *), Bash(ls *), Bash(find *), Bash(test *), Bash(cat *), Bash(git *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# Update Workflow - Workflow Documentation Synchronization

Sync workflow documentation between projects bidirectionally with smart file filtering.

## Overview

This skill synchronizes workflow documentation between projects:

**What it does:**
1. Scans source and target for workflow files
2. Compares CLAUDE.md and .claude/workflow/ contents
3. Shows detailed diff preview
4. Syncs workflow docs with confirmation
5. Smart filtering (excludes project-specific files)
6. Reports what was synced

**Why it's needed:**
Workflow best practices evolve. Framework updates need to propagate, and process improvements should be shared. This skill automates workflow doc sync while protecting project-specific configurations.

**When to use:**
- Monthly framework upgrades
- Process improvement propagation
- Initial project setup
- Cross-project workflow sharing

## Workflow

### Step 1: Create Todo List

**Initialize sync tracking** using TaskCreate:

```
Task #1: Validate source and target paths
Task #2: Scan workflow files (blocked by #1)
Task #3: Compare and detect changes (blocked by #2)
Task #4: Show diff preview (blocked by #3)
Task #5: Execute sync with confirmation (blocked by #4)
Task #6: Report sync results (blocked by #5)
```

After creating tasks, proceed with sync execution.

## What Gets Synced

### ✅ Included Files (Framework Files)

```
Project Root:
├── CLAUDE.md                    ✅ Main project instructions

.claude/:
├── README.md                    ✅ Framework documentation
├── WORKFLOW.md                  ✅ Quick start guide
└── workflow/                    ✅ Planning templates
    ├── MAIN.md
    ├── PLANNING.md
    ├── TIER.md
    └── TEMPLATES.md
```

### ❌ Excluded Files (Project-Specific)

```
.claude/:
├── settings.json                ❌ Project-specific config
├── MEMORY.md                    ❌ Project-specific knowledge
├── plans/                       ❌ Project-specific plans
├── skills/                      ❌ Managed by update-skills
└── rules/                       ❌ Managed by update-rules

.prot/:
└── pillars/                     ❌ Managed by update-pillars
```

## Sync Modes

### 1. Pull Workflow (--from)

Pull workflow docs from source project:

```bash
/update-workflow --from ~/dev/ai-dev
/update-workflow --from ~/dev/ai-dev --dry-run
/update-workflow --from ~/dev/ai-dev --files CLAUDE.md,workflow/
```

**What happens:**
1. Scan source workflow files
2. Scan current workflow files
3. Compare modification times and sizes
4. Detect: NEW, NEWER, SAME, OLDER
5. Show analysis
6. Confirm and copy

### 2. Push Workflow (--to)

Push workflow docs to target project:

```bash
/update-workflow --to ~/projects/my-app
/update-workflow --to ~/projects/my-app --dry-run
/update-workflow --to ~/projects/my-app --files workflow/MAIN.md
```

**What happens:**
1. Scan current workflow files
2. Scan target workflow files
3. Compare and detect changes
4. Show what will be pushed
5. Confirm and copy to target

### 3. Dry Run Mode (--dry-run)

Preview changes without applying:

```bash
/update-workflow --from ~/dev/ai-dev --dry-run
```

**Output:**
- Shows analysis table
- Reports what would be synced
- No confirmation required
- No actual changes made

### 4. File Filter (--files)

Sync only specific files:

```bash
/update-workflow --from ~/dev/ai-dev --files CLAUDE.md,workflow/
/update-workflow --to ~/projects/my-app --files workflow/MAIN.md,workflow/TIER.md
```

**Available patterns:**
- `CLAUDE.md` - Main project instructions
- `README.md` - Framework documentation (.claude/README.md)
- `WORKFLOW.md` - Quick start guide (.claude/WORKFLOW.md)
- `workflow/` - All planning templates (.claude/workflow/*.md)
- `workflow/MAIN.md` - Main workflow guide
- `workflow/PLANNING.md` - Planning template
- `workflow/TIER.md` - Tiering system
- `workflow/TEMPLATES.md` - Template library

## Comparison Logic

**File status detection:**

```
For each workflow file:
1. Check if exists in target
   → NEW if not found
2. Compare modification time
   → NEWER if source newer
   → OLDER if source older
3. Compare file size
   → SAME if identical
```

**Analysis output:**

```
📊 Analysis by location:
┌──────────────────────────┬────────┬──────────────────┐
│ File                     │ Status │ Action           │
├──────────────────────────┼────────┼──────────────────┤
│ CLAUDE.md                │ NEWER  │ Update           │
│ .claude/README.md        │ SAME   │ Skip             │
│ .claude/WORKFLOW.md      │ NEWER  │ Update           │
│ .claude/workflow/MAIN.md │ NEW    │ Add              │
│ .claude/workflow/TIER.md │ SAME   │ Skip             │
└──────────────────────────┴────────┴──────────────────┘

Summary:
- New files: 1
- Updated files: 2
- Unchanged: 2
- Total to update: 3 files
```

## Usage Examples

### Example 1: Framework Upgrade

**User says:**
> "update workflow docs from the framework"

**What happens:**
1. Pull from ~/dev/ai-dev
2. Scan workflow files
3. Show: 3 files to update
4. Confirm and sync
5. Report: "Updated 3 workflow files"

**Time:** ~25 seconds

### Example 2: Selective Update

**User says:**
> "only update CLAUDE.md from the framework"

**What happens:**
1. `/update-workflow --from ~/dev/ai-dev --files CLAUDE.md`
2. Compare only CLAUDE.md
3. Show: NEWER (update needed)
4. Sync CLAUDE.md
5. Report: "Updated CLAUDE.md"

**Time:** ~15 seconds

### Example 3: Share Workflow Templates

**User says:**
> "push workflow templates to my new project"

**What happens:**
1. `/update-workflow --to ~/projects/new-app --files workflow/`
2. Compare all workflow/*.md files
3. Show: 4 NEW files
4. Confirm and push
5. Report: "Pushed 4 workflow templates"

**Time:** ~20 seconds

## Safety Features

**Pre-flight checks:**
- ✅ Source/target paths exist
- ✅ Source has workflow files
- ✅ User confirmation before changes
- ✅ Dry-run preview available

**Smart filtering:**
- Excludes settings.json, MEMORY.md, plans/
- Only syncs framework workflow files
- Protects project-specific configs

**Backup strategy:**
```bash
# Before overwrite
CLAUDE.md → CLAUDE.md.backup-20260306
```

## Error Handling

### Invalid Source/Target

```
❌ Error: Project not found

Path: ../nonexistent
Expected workflow files in: ../nonexistent/

Please check:
1. Path is correct
2. Project has workflow files
3. You have read permissions
```

### No Files to Update

```
✅ All workflow files are up to date!

No new or updated files found in source.
Current project has all latest versions.
```

### Invalid File Pattern

```
❌ Error: Unknown file pattern: invalid.md

Valid patterns:
- CLAUDE.md
- README.md
- WORKFLOW.md
- workflow/ (all workflow templates)
- workflow/MAIN.md
- workflow/PLANNING.md
- workflow/TIER.md
- workflow/TEMPLATES.md
```

## Best Practices

1. **Always dry-run first:**
```bash
/update-workflow --from ~/dev/ai-dev --dry-run
/update-workflow --from ~/dev/ai-dev
```

2. **File-specific updates:**
```bash
# Only update main instructions
/update-workflow --from ~/dev/ai-dev --files CLAUDE.md

# Only update planning templates
/update-workflow --from ~/dev/ai-dev --files workflow/
```

3. **Framework as source of truth:**
```bash
# In projects: pull from framework
/update-workflow --from ~/dev/ai-dev

# In framework: pull innovations from projects
/update-workflow --from ~/projects/my-app
```

4. **Regular updates:**
```bash
# Weekly/monthly routine
/update-workflow --from ~/dev/ai-dev
```

## Integration

**With other update-* skills:**
```bash
# Complete framework update
/update-pillars --from ~/dev/ai-dev   # 1. Pillars
/update-rules --from ~/dev/ai-dev     # 2. Rules
/update-workflow --from ~/dev/ai-dev  # 3. Workflow
/update-skills --from ~/dev/ai-dev    # 4. Skills

# Or use meta-skill
/update-framework --from ~/dev/ai-dev # All-in-one
```

**Common workflow:**
```
Framework upgrade → Pull Workflow → Review changes → Commit
Process improvement → Update workflow → Push to framework
```

## Task Management

**After each sync step**, update progress:

```
Paths validated → Update Task #1
Files scanned → Update Task #2
Changes detected → Update Task #3
Diff shown → Update Task #4
Sync executed → Update Task #5
Results reported → Update Task #6
```

Provides real-time visibility of sync progress.

## Final Verification

**Before declaring sync complete**, verify:

```
- [ ] All 6 sync tasks completed
- [ ] Source and target paths valid
- [ ] Workflow files compared
- [ ] User confirmed changes
- [ ] Files copied correctly
- [ ] Sync summary displayed
```

Missing items indicate incomplete sync.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list for progress tracking
2. **TaskUpdate** during execution - Mark tasks in_progress → completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/update-framework** - Sync entire framework (calls this skill)
- **/update-pillars** - Sync Pillars
- **/update-rules** - Sync rules
- **/update-skills** - Sync skills

---

**Version:** 2.1.0
**Last Updated:** 2026-03-12
**Changelog:**
- v2.1.0 (2026-03-12): Sync workflow documentation between projects
**Pattern:** Tool-Reference (guides sync process)
**Compliance:** ADR-001 Section 4 ✅
