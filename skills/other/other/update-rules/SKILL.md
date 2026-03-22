---
name: update-rules
description: |
  Sync technical rules between projects - bidirectional copy with category filtering.
  TRIGGER when: user wants to sync rules ("update rules from X", "sync rules", "pull rules from framework", "push rules to project").
  DO NOT TRIGGER when: user wants to update pillars/skills/workflow (use respective update-* skills), or just wants to read rule docs.
version: "2.1.0"
allowed-tools: Bash(cp *), Bash(mkdir *), Bash(ls *), Bash(find *), Bash(test *), Bash(cat *), Bash(git *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# Update Rules - Technical Rules Synchronization

Sync technical rule documentation between projects bidirectionally with **profile-aware filtering** (v2.2.0+).

## Overview

This skill synchronizes technical rules (.claude/rules/) between projects:

**What it does:**
1. Scans source and target projects for rules
2. **Filters by profile** - syncs only rules relevant to tech stack (recommended)
3. Compares rules to detect new/updated content
4. Shows detailed diff preview with filter summary
5. Syncs rules with confirmation
6. Validates profile compliance
7. Reports what was synced

**Why it's needed:**
Framework rule updates need to propagate across projects with **precision**. Category-based sync causes 30-50% rule bloat (e.g., Tauri rules in web apps). Profile-aware filtering ensures **zero incorrect rules** by syncing only what's relevant to each project's tech stack.

**When to use:**
- Monthly framework upgrades
- Propagating best practices
- Cross-project learning
- Initial project setup

## Workflow

### Step 1: Create Todo List

**Initialize sync tracking** using TaskCreate:

```
Task #1: Validate source and target paths
Task #2: Scan rules in both projects (blocked by #1)
Task #3: Compare rules by category (blocked by #2)
Task #4: Show diff preview (blocked by #3)
Task #5: Execute sync with confirmation (blocked by #4)
Task #6: Report sync results (blocked by #5)
```

After creating tasks, proceed with sync execution.

## Rule Categories

```
.claude/rules/
├── core/                    # Workflow, naming, debugging (7 rules)
├── architecture/            # Clean architecture, layers (7 rules)
├── languages/               # TypeScript, Python, Go (3 rules)
├── frontend/                # React, state management (6 rules)
├── backend/                 # Lambda, API design (5 rules)
├── infrastructure/          # AWS CDK, secrets (10 rules)
└── development/             # Performance, security (2 rules)
```

## Sync Modes

### 1. Pull Rules (--from)

Pull rules from source project to current project:

```bash
/update-rules --from ~/dev/ai-dev
/update-rules --from ~/dev/ai-dev --dry-run
/update-rules --from ~/dev/ai-dev --categories core,architecture
```

**What happens:**
1. Scan source: `<source>/.claude/rules/`
2. Scan current: `.claude/rules/`
3. Compare by category
4. Detect: NEW, NEWER, SAME, OLDER
5. Show analysis table
6. Confirm and copy updated rules

### 2. Push Rules (--to)

Push rules from current project to target project:

```bash
/update-rules --to ~/projects/my-app
/update-rules --to ~/projects/my-app --dry-run
/update-rules --to ~/projects/my-app --categories backend,infrastructure
```

**What happens:**
1. Scan current project rules
2. Scan target project rules
3. Compare by category
4. Show what will be pushed
5. Confirm and copy to target

### 3. Dry Run Mode (--dry-run)

Preview changes without applying:

```bash
/update-rules --from ~/dev/ai-dev --dry-run
```

**Output:**
- Shows analysis table by category
- Reports what would be synced
- No confirmation required
- No actual changes made

### 4. Profile-Based Sync (--profile) - RECOMMENDED

**New in v2.2.0**: Sync rules based on project profile with precise filtering.

Sync only rules relevant to project's tech stack:

```bash
/update-rules --from ~/dev/ai-dev --to ~/dev/u-safe --profile tauri
/update-rules --from ~/dev/ai-dev --to ~/dev/buffer --profile nextjs-aws
/update-rules --from ~/dev/ai-dev --profile tauri-aws  # Auto-detects target from pwd
```

**How it works:**
1. Reads profile definition from `framework/profiles/<profile>.json`
2. Applies `rules.include` whitelist (exact rules needed)
3. Applies `rules.exclude` patterns (rules to skip)
4. Syncs ONLY relevant rules for that tech stack

**Benefits:**
- ✅ Precise rule sets (zero bloat)
- ✅ No incorrect rules (e.g., no Tauri in web apps, no AWS in desktop apps)
- ✅ Profile compliance validation
- ✅ Better Claude Code context management

**Supported Profiles:**
- `tauri` - Desktop apps (Tauri + React): 23 rules
- `tauri-aws` - Desktop + cloud backend: TBD rules
- `nextjs-aws` - Full-stack web (Next.js + AWS): 30 rules

**Example Results (from Issue #162):**

```
Before:
  u-safe (tauri): 46 rules (bloated with AWS/Lambda rules)
  buffer (nextjs-aws): 43 rules (bloated with Tauri rules)

After:
  u-safe (tauri): 23 rules ✅ (50% reduction)
  buffer (nextjs-aws): 30 rules ✅ (30% reduction)

Impact: 100% profile compliance, zero incorrect rules
```

**Profile Definition Example** (`framework/profiles/tauri.json`):
```json
{
  "name": "tauri",
  "pillars": ["A", "B", "K", "L"],
  "rules": {
    "include": [
      // Core (7 rules)
      "workflow", "naming", "debugging", "docs",
      "memory-management", "memory-protection", "planning-context",

      // Architecture (6 rules)
      "clean-architecture", "dependency-rule", "service-layer",
      "headless", "adapters", "identity",

      // Languages (3 rules)
      "typescript-esm", "typescript-strict", "typescript-nominal-types",

      // Frontend (4 rules)
      "design-system", "zustand-hooks", "views", "css",

      // Infrastructure - Tauri specific (3 rules)
      "tauri-stack", "tauri-ipc", "tauri-security"
    ],
    "exclude": [
      "backend/lambda-*.md",      // No serverless in desktop
      "infrastructure/aws-*.md",  // No AWS in desktop
      "infrastructure/cdk-*.md"   // No CDK in desktop
    ]
  }
}
```

**Comparison with Category Filtering:**

| Approach | nextjs-aws Example | Result |
|----------|-------------------|--------|
| `--categories` | Syncs ALL rules in specified categories | 43 rules (30% bloat) |
| `--profile` | Syncs ONLY rules in profile's include list | 30 rules (100% precise) |

**Migration from --categories:**

```bash
# Old way (category-based) - causes bloat
/update-rules --to ~/dev/buffer --categories core,architecture,frontend,backend,infrastructure
# Result: 43 rules (includes irrelevant Tauri rules)

# New way (profile-based) - precise
/update-rules --to ~/dev/buffer --profile nextjs-aws
# Result: 30 rules (only relevant rules)
```

**Troubleshooting:**

```bash
# Check current rule count
find .claude/rules -name "*.md" | wc -l

# Check expected count for profile
cat ~/dev/ai-dev/framework/profiles/nextjs-aws.json | jq '.rules.include | length'

# If mismatch, re-sync with profile
cd ~/dev/ai-dev
/update-rules --to ~/dev/your-project --profile <profile>
```

### 5. Category Filter (--categories) - LEGACY

**Deprecated**: Use `--profile` instead for precise filtering.

Sync rules by category (coarse-grained):

```bash
/update-rules --from ~/dev/ai-dev --categories core,architecture,languages
/update-rules --to ~/projects/my-app --categories frontend,backend
```

**Available categories:**
- `core` - Workflow, naming, debugging, docs
- `architecture` - Clean architecture, layers, dependencies
- `languages` - TypeScript, Python, Go
- `frontend` - React, state, design system
- `backend` - Lambda, saga, API design
- `infrastructure` - AWS CDK, secrets, monitoring
- `development` - Performance, security

**Why deprecated:**
- ❌ Too coarse-grained (syncs ALL rules in category)
- ❌ Causes rule bloat (30-50% extra rules)
- ❌ Can't exclude specific files within category
- ✅ Use `--profile` instead for precise control

### 6. Smart Filter (--filter-config)

Apply intelligent filtering based on tech stack configuration:

```bash
# Used by /update-framework meta-skill
/update-rules --from ~/dev/ai-dev --filter-config <target>/.claude/framework-config.json
```

**What it does:**
1. Reads filter config from `.claude/framework-config.json`
2. Applies include/exclude patterns based on tech stack
3. Filters by categories, specific files, and glob patterns
4. Shows filter summary in analysis

**Filter Configuration Format:**

```json
{
  "filterConfig": {
    "rules": {
      "include_categories": ["core", "architecture", "frontend", "languages"],
      "include_files": ["infrastructure/tauri-stack.md"],
      "exclude_patterns": [
        "backend/lambda-*.md",
        "infrastructure/aws-*.md",
        "infrastructure/cdk-*.md"
      ]
    }
  }
}
```

**Filter Logic:**

```
For each rule file:
1. Check if category in include_categories
   → Skip if not included
2. Check if file matches include_files
   → Include if matched
3. Check if file matches exclude_patterns
   → Exclude if matched (takes precedence)
4. Apply normal NEW/NEWER/SAME logic
```

**Example - Tauri Project:**

Without filter: 43 rules synced
With filter: ~25 rules synced (excludes AWS/Lambda rules)

```
📋 Smart Filter Active (Tauri + React + No Cloud)
⏭️  Excluding: backend/lambda-* (3 files)
⏭️  Excluding: infrastructure/aws-* (5 files)
⏭️  Excluding: infrastructure/cdk-* (3 files)
✅ Including: infrastructure/tauri-stack.md

Result: 25 rules synced (18 excluded as not relevant)
```

**Note:** Typically called by `/update-framework` meta-skill, not directly by users.

## Comparison Logic

**File status detection:**

```
For each rule file:
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
📊 Analysis by category:
┌────────────────┬─────┬─────┬──────┐
│ Category       │ New │ Upd │ Same │
├────────────────┼─────┼─────┼──────┤
│ core           │  0  │  1  │   6  │
│ architecture   │  0  │  2  │   5  │
│ languages      │  1  │  0  │   2  │
│ frontend       │  1  │  1  │   4  │
│ backend        │  2  │  0  │   3  │
│ infrastructure │  0  │  1  │   9  │
│ development    │  0  │  0  │   2  │
└────────────────┴─────┴─────┴──────┘

Summary:
- New rules: 4
- Updated rules: 5
- Unchanged: 33
- Total to sync: 9 rules
```

## What Gets Synced

```
.claude/rules/
├── core/
│   ├── workflow.md           ✅ Synced
│   ├── naming.md             ✅ Synced
│   └── ...                   ✅ Synced
├── architecture/
│   └── ...                   ✅ Synced
├── languages/
│   └── ...                   ✅ Synced
├── frontend/
│   └── ...                   ✅ Synced
├── backend/
│   └── ...                   ✅ Synced
├── infrastructure/
│   └── ...                   ✅ Synced
└── development/
    └── ...                   ✅ Synced

.claude/
├── settings.json             ❌ Not synced (project-specific)
├── MEMORY.md                 ❌ Not synced (project-specific)
└── plans/                    ❌ Not synced (project-specific)
```

## Usage Examples

### Example 1: Profile-Based Sync (Recommended)

**User says:**
> "update rules from framework for my tauri project"

**What happens:**
1. Detect profile from `.framework-install` → `tauri`
2. Load `framework/profiles/tauri.json` → 23 rules in include list
3. Scan and filter: exclude AWS/Lambda/CDK rules
4. Show: 23 rules to sync (with filter summary)
5. Confirm and sync
6. Report: "Synced 23 rules (tauri profile, 100% compliance)"

**Before/After:**
- Before: 46 rules (bloated with AWS rules)
- After: 23 rules (precise, zero bloat)
- Reduction: 50%

**Time:** ~25 seconds

### Example 2: Framework Upgrade with Profile

**User says:**
> "update rules from the framework"

**What happens:**
1. Auto-detect profile from `.framework-install`
2. Apply profile filtering
3. Show: 5 rules to update (only relevant ones)
4. Confirm and sync
5. Report: "Updated 5 rules (nextjs-aws profile)"

**Time:** ~20 seconds

### Example 3: Category-Based Update (Legacy - Not Recommended)

**User says:**
> "pull only frontend and React rules from the framework"

**What happens:**
1. `/update-rules --from ~/dev/ai-dev --categories frontend,languages`
2. Scan frontend/ and languages/ categories
3. Show: 3 rules to update
4. Sync specific categories
5. Report: "Updated 3 frontend/language rules"

**⚠️ Warning:** This syncs ALL rules in categories, causing bloat. Use `--profile` instead.

**Time:** ~20 seconds

## Safety Features

**Pre-flight checks:**
- ✅ Source/target paths exist
- ✅ Source has .claude/rules/ directory
- ✅ User confirmation before changes
- ✅ Dry-run preview available

**Smart filtering:**
- Profile-aware filtering (whitelist-based)
- Only syncs rules relevant to tech stack
- Excludes incorrect rules (e.g., no AWS in desktop apps)
- Clear status for each rule

**Backup strategy:**
```bash
# Before overwrite
.claude/rules/core/workflow.md
→ .claude/rules/core/workflow.md.backup-20260306
```

## Error Handling

### Invalid Source/Target

```
❌ Error: Project not found

Path: ../nonexistent
Expected: ../nonexistent/.claude/rules/

Please check:
1. Path is correct
2. Project has .claude/rules/ directory
3. You have read permissions
```

### No Rules to Update

```
✅ All rules are up to date!

No new or updated rules found in source.
Current project has all latest versions.
```

### Invalid Category

```
❌ Error: Unknown category: invalid-category

Valid categories:
- core
- architecture
- languages
- frontend
- backend
- infrastructure
- development
```

## Best Practices

1. **Use profile-based sync (recommended):**
```bash
# Auto-detects profile from .framework-install
/update-rules --from ~/dev/ai-dev --to ~/dev/u-safe --profile tauri

# Ensures zero incorrect rules
/update-rules --from ~/dev/ai-dev --to ~/dev/buffer --profile nextjs-aws
```

2. **Always dry-run first:**
```bash
/update-rules --from ~/dev/ai-dev --dry-run
/update-rules --from ~/dev/ai-dev
```

3. **Framework as source of truth:**
```bash
# In projects: pull from framework with profile
/update-rules --from ~/dev/ai-dev --profile tauri

# In framework: test profile filtering
/update-rules --to ~/dev/test-project --profile nextjs-aws --dry-run
```

4. **Regular updates:**
```bash
# Weekly/monthly routine (profile auto-detected)
/update-rules --from ~/dev/ai-dev
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
Framework upgrade → Pull Rules → Apply best practices
Project setup → Push Rules → Share knowledge
```

## Task Management

**After each sync step**, update progress:

```
Paths validated → Update Task #1
Rules scanned → Update Task #2
Rules compared by profile → Update Task #3
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
- [ ] Rules compared by profile (or category if legacy mode)
- [ ] User confirmed changes
- [ ] Files copied correctly
- [ ] Sync summary displayed with filter info
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
- **/update-skills** - Sync skills
- **/update-workflow** - Sync workflow docs

---

**Version:** 2.1.0
**Last Updated:** 2026-03-12
**Changelog:**
- v2.1.0 (2026-03-12): Sync technical rules between projects with profile-aware filtering
**Pattern:** Tool-Reference (guides sync process)
**Compliance:** ADR-001 Section 4 ✅
