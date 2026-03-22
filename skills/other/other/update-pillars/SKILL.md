---
name: update-pillars
description: |
  Sync Pillars between projects - bidirectional copy with smart filtering.
  TRIGGER when: user wants to sync Pillars ("update pillars from X", "sync pillars", "pull pillars from framework", "push pillars to project").
  DO NOT TRIGGER when: user wants to update rules/skills/workflow (use respective update-* skills), or just wants to read Pillar docs.
version: "2.1.0"
allowed-tools: Bash(cp *), Bash(mkdir *), Bash(ls *), Bash(find *), Bash(test *), Bash(cat *), Bash(git *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# Update Pillars - Project Pillar Synchronization

Sync Pillar documentation between projects bidirectionally with profile-aware filtering.

## Overview

This skill synchronizes Pillar documentation (.prot/pillars/) between projects:

**What it does:**
1. Scans source and target projects for Pillars
2. Compares Pillars to detect new/updated content
3. Shows detailed diff preview
4. Syncs Pillars with confirmation
5. Respects project profiles (minimal, node-lambda, react-aws)
6. Reports what was synced

**Why it's needed:**
Framework upgrades require updating Pillar documentation across projects. Manual copying is error-prone and time-consuming. This skill automates the sync with safety checks and profile awareness.

**When to use:**
- Monthly framework upgrades
- Initial project setup
- Cross-project learning (adopting Pillar practices)
- Promoting innovations back to framework

## Workflow

### Step 1: Create Todo List

**Initialize sync tracking** using TaskCreate:

```
Task #1: Validate source and target paths
Task #2: Scan Pillars in both projects (blocked by #1)
Task #3: Compare and detect changes (blocked by #2)
Task #4: Show diff preview (blocked by #3)
Task #5: Execute sync with confirmation (blocked by #4)
Task #6: Report sync results (blocked by #5)
```

After creating tasks, proceed with sync execution.

## Sync Modes

### 1. Pull Pillars (--from)

Pull Pillars from source project to current project:

```bash
/update-pillars --from ~/dev/ai-dev
/update-pillars --from ~/dev/ai-dev --dry-run
/update-pillars --from ~/dev/ai-dev --pillars A,B,K
```

**What happens:**
1. Scan source project: `<source>/.prot/pillars/`
2. Scan current project: `.prot/pillars/`
3. Compare modification times and sizes
4. Detect: NEW, NEWER, SAME, OLDER
5. Show analysis table
6. Confirm and copy updated Pillars

**Profile-aware filtering:**
- Reads `.framework-install` to determine profile
- Only updates Pillars enabled in profile
- Example: `minimal` profile → only A, B, K

### 2. Push Pillars (--to)

Push Pillars from current project to target project:

```bash
/update-pillars --to ~/projects/my-app
/update-pillars --to ~/projects/my-app --dry-run
/update-pillars --to ~/projects/my-app --pillars M,Q
```

**What happens:**
1. Scan current project Pillars
2. Scan target project Pillars
3. Compare and detect changes
4. Show what will be pushed
5. Confirm and copy to target

### 3. Dry Run Mode (--dry-run)

Preview changes without applying:

```bash
/update-pillars --from ~/dev/ai-dev --dry-run
```

**Output:**
- Shows analysis table
- Reports what would be synced
- No confirmation required
- No actual changes made

### 4. Selective Sync (--pillars)

Sync only specific Pillars:

```bash
/update-pillars --from ~/dev/ai-dev --pillars A,M,Q
/update-pillars --to ~/projects/my-app --pillars K,L,R
```

**Pillar selection:**
- Comma-separated list (A-R)
- Only syncs specified Pillars
- Ignores others

## Comparison Logic

**File status detection:**

```
For each Pillar:
1. Check if exists in target
   → NEW if not found
2. Compare modification time
   → NEWER if source newer
   → OLDER if source older
3. Compare file size
   → CONFLICT if same time, different size
   → SAME if identical
```

**Analysis output:**

```
📊 Analysis:
┌─────────────┬────────┬──────────────────┐
│ Pillar      │ Status │ Action           │
├─────────────┼────────┼──────────────────┤
│ pillar-a    │ NEWER  │ Update (250 vs 245 lines) │
│ pillar-b    │ SAME   │ Skip             │
│ pillar-k    │ NEW    │ Add (180 lines)  │
│ pillar-m    │ OLDER  │ Skip (warn)      │
└─────────────┴────────┴──────────────────┘

Summary:
- New Pillars: 1 (K)
- Updated Pillars: 1 (A)
- Unchanged: 1 (B)
- Total to sync: 2 Pillars
```

## Profile Integration

**Profile detection:**

```bash
# Method 1: Read .framework-install
cat .framework-install
# → profile: minimal

# Method 2: Scan installed Pillars
ls .prot/pillars/
# → pillar-a, pillar-b, pillar-k
```

**Profile-based filtering:**

| Profile | Pillars Synced |
|---------|----------------|
| minimal | A, B, K only (3 Pillars) |
| node-lambda | A, B, K, M, Q, R (6 Pillars) |
| react-aws | A, B, K, L, M, Q, R (7 Pillars) |
| custom/none | All Pillars in .prot/pillars/ |

**Example:**
```
Source has: 18 Pillars (A-R)
Current profile: minimal (A, B, K)
→ Only sync: A, B, K
→ Skip: 15 other Pillars
```

## What Gets Synced

```
.prot/pillars/
├── pillar-a/
│   └── *.md              ✅ Synced
├── pillar-b/
│   └── *.md              ✅ Synced
├── pillar-k/
│   └── *.md              ✅ Synced
└── README.md             ✅ Synced (if exists)

.prot/
├── checklists/           ❌ Not synced (project-specific)
└── other files           ❌ Not synced
```

## Usage Examples

### Example 1: Framework Upgrade

**User says:**
> "update pillars from the framework"

**What happens:**
1. Pull from ~/dev/ai-dev (detected from context)
2. Scan both projects
3. Show analysis: 2 Pillars updated
4. Confirm and sync
5. Report: "Updated Pillar A, K"

**Time:** ~30 seconds

### Example 2: Initial Setup

**User says:**
> "push pillars to my new project at ~/projects/new-app"

**What happens:**
1. Scan current project Pillars (7 Pillars)
2. Scan target (empty)
3. Show: 7 NEW Pillars to add
4. Confirm and copy all
5. Report: "Added 7 Pillars"

**Time:** ~45 seconds

### Example 3: Cross-Project Learning

**User says:**
> "pull Pillar M and Q from my other project"

**What happens:**
1. `/update-pillars --from ~/projects/other-project --pillars M,Q`
2. Compare Saga and Idempotency Pillars
3. Show diff
4. Sync if newer
5. Adopt best practices

**Time:** ~30 seconds

## Safety Features

**Pre-flight checks:**
- ✅ Source/target paths exist
- ✅ Source has .prot/pillars/ directory
- ✅ User confirmation before changes
- ✅ Dry-run preview available

**Smart filtering:**
- Profile-aware (respects project configuration)
- Only syncs enabled Pillars
- Clear status for each Pillar

**Error handling:**
- Invalid paths: Clear error message
- No updates needed: Skip gracefully
- Permission issues: Helpful guidance

## Error Handling

### Invalid Source/Target

```
❌ Error: Project not found

Path: ../nonexistent
Expected: ../nonexistent/.prot/pillars/

Please check:
1. Path is correct
2. Project has .prot/pillars/ directory
3. You have read permissions
```

### No Pillars to Update

```
✅ All Pillars are up to date!

No new or updated Pillars found in source.
Current project has all latest versions.
```

### OLDER Source (Warning)

```
⚠️ Warning: Source Pillar is OLDER

Pillar: A
Source: 2026-03-01 (245 lines)
Target: 2026-03-04 (250 lines)

Action: Skip (keeping newer target version)
```

## Best Practices

1. **Always dry-run first for major updates:**
```bash
/update-pillars --from ~/dev/ai-dev --dry-run
/update-pillars --from ~/dev/ai-dev
```

2. **Selective updates for safety:**
```bash
# Update only Pillars you understand
/update-pillars --from ~/dev/ai-dev --pillars A,B,K
```

3. **Framework as source of truth:**
```bash
# In projects: pull from framework
/update-pillars --from ~/dev/ai-dev

# In framework: pull innovations from projects
/update-pillars --from ~/projects/my-app --pillars X
```

4. **Regular framework upgrades:**
```bash
# Monthly routine
/update-pillars --from ~/dev/ai-dev
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
Framework upgrade → Pull Pillars → Update Rules → Update Skills
Project setup → Push Pillars → Configure profile
```

## Task Management

**After each sync step**, update progress:

```
Paths validated → Update Task #1
Pillars scanned → Update Task #2
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
- [ ] Pillars compared successfully
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
- **/update-rules** - Sync technical rules
- **/update-skills** - Sync skills
- **/update-workflow** - Sync workflow docs

---

**Version:** 2.1.0
**Last Updated:** 2026-03-12
**Changelog:**
- v2.1.0 (2026-03-12): Sync pillar documentation between projects
**Pattern:** Tool-Reference (guides sync process)
**Compliance:** ADR-001 Section 4 ✅
