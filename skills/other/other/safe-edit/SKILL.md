---
name: safe-edit
description: Automatically backs up files, saves diffs, uses agents/skills, and ensures modular code (<200 lines) before any implementation. Use this skill for ALL code changes to ensure safe, reversible, and clean implementations.
allowed-tools: Read, Write, Edit, Bash, Glob, Task, TodoWrite
---

# Safe Edit Skill

## Overview

Comprehensive workflow automation for safe, reversible, and clean code implementations. This skill ensures every code change follows best practices: automatic backups, diff tracking, agent utilization, and modular architecture enforcement.

## When to Use

**ALWAYS activate this skill before ANY code implementation:**
- Any file modification (create, update, delete)
- Feature implementation
- Bug fixes
- Refactoring
- UI/UX changes
- API changes
- Database schema updates

**User triggers (automatic activation):**
- Any implementation request without explicit backup mention
- "implement", "add", "create", "fix", "update", "change"
- Any code-related task

## Core Workflow

### Phase 1: Pre-Implementation Analysis
```
1. Analyze task complexity and scope
2. Identify affected files and modules
3. Check if agents/skills can help
4. Plan modular architecture (if >200 lines)
5. Create TODO list for tracking
```

### Phase 2: Backup & Safety
```
1. Create timestamped backup in .backups/
2. Generate git diff (save to /tmp/diffs/)
3. Document rollback commands
4. Verify backup integrity
```

### Phase 3: Implementation
```
1. Use appropriate agents/skills
2. Implement in modular chunks (<200 lines)
3. Follow existing patterns
4. Update TODO progress
```

### Phase 4: Verification
```
1. Generate final diff
2. Run type checking (if TypeScript)
3. Test build (if applicable)
4. Document changes
```

## Backup Management

### Directory Structure
```
.backups/
├── YYYY-MM-DD/
│   ├── HH-MM-SS_{filename}.backup
│   └── HH-MM-SS_{filename}.backup
└── ROLLBACK_GUIDE.md

/tmp/diffs/
├── YYYY-MM-DD_HH-MM-SS_{description}.patch
└── latest.patch
```

### Backup Naming Convention
```
Format: {timestamp}_{original_path_with_underscores}.backup

Examples:
2025-10-24_13-45-30_app_pricing_page.tsx.backup
2025-10-24_13-45-30_components_editor_EditorContainer.tsx.backup
```

### Diff Naming Convention
```
Format: YYYY-MM-DD_HH-MM-SS_{feature_description}.patch

Examples:
2025-10-24_13-45-30_add-footer-links.patch
2025-10-24_14-20-15_pricing-policy-update.patch
```

## Automatic Modularization

### When File Exceeds 200 Lines

**Detection:**
- Count lines before implementation
- Predict final size after changes
- Warn if approaching 200 lines

**Action Plan:**
1. Analyze component responsibilities
2. Identify extractable logic
3. Create modular structure
4. Implement in separate files
5. Update imports/exports

**Example Refactoring:**
```
Original: EditorContainer.tsx (450 lines)
↓
Modularized:
- EditorContainer.tsx (180 lines) - Main layout
- hooks/useEditorState.ts (80 lines) - State management
- hooks/useKeyboardShortcuts.ts (60 lines) - Keyboard logic
- actions/ttsActions.ts (70 lines) - TTS operations
- actions/mediaActions.ts (60 lines) - Media operations
```

## Agent & Skill Utilization

### Automatic Agent Selection

**Analysis Tasks:**
- `Explore` - Codebase exploration
- `general-purpose` - Complex analysis

**Implementation Tasks:**
- `frontend-developer` - UI components
- `backend-api-developer` - API endpoints
- `database-architect` - Schema design
- `ux-ui-designer` - Design specs

**Skill Integration:**
- `supabase-manager` - Database operations
- `safe-edit` (this skill) - All implementations

### Decision Matrix

| Task Type | Agent/Skill | Why |
|-----------|-------------|-----|
| UI Component | frontend-developer | Design system + implementation |
| API Endpoint | backend-api-developer | Best practices + patterns |
| DB Schema | database-architect | Normalization + indexing |
| Bug Analysis | Explore | Deep analysis + reasoning |
| File Changes | safe-edit (always) | Backup + rollback safety |

## Implementation Rules

### Rule 1: Always Backup First
```bash
# Before ANY file modification
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
backup_dir=".backups/$(date +%Y-%m-%d)"
mkdir -p "$backup_dir"
cp "path/to/file" "$backup_dir/${timestamp}_${file_slug}.backup"
```

### Rule 2: Always Save Diff
```bash
# Before and after changes
mkdir -p "/tmp/diffs"
timestamp=$(date +%Y-%m-%d_%H-%M-%S)
git diff path/to/file > "/tmp/diffs/${timestamp}_${description}.patch"
cp "/tmp/diffs/${timestamp}_${description}.patch" "/tmp/diffs/latest.patch"
```

### Rule 3: Check File Size
```bash
# Before implementation
lines=$(wc -l < "path/to/file")
if [ $lines -gt 200 ]; then
  echo "⚠️ File exceeds 200 lines - planning modularization"
  # Execute modularization strategy
fi
```

### Rule 4: Use Agents When Available
```typescript
// For complex UI work
Task({
  subagent_type: "frontend-developer",
  description: "Implement component",
  prompt: "Detailed requirements..."
})

// For analysis
Task({
  subagent_type: "Explore",
  description: "Analyze codebase",
  prompt: "Find patterns and structure..."
})
```

### Rule 5: Track Progress
```typescript
// Always create TODO list for multi-step tasks
TodoWrite({
  todos: [
    { content: "Backup files", status: "in_progress", activeForm: "Backing up files" },
    { content: "Implement feature", status: "pending", activeForm: "Implementing feature" },
    { content: "Verify changes", status: "pending", activeForm: "Verifying changes" }
  ]
})
```

## Rollback Procedures

### Method 1: Backup Restore
```bash
# Find backup
ls -lt .backups/$(date +%Y-%m-%d)/

# Restore
cp .backups/2025-10-24/13-45-30_app_pricing_page.tsx.backup app/pricing/page.tsx
```

### Method 2: Patch Reversal
```bash
# Apply reverse patch
cd /path/to/your/project
patch -R app/pricing/page.tsx < /tmp/diffs/2025-10-24_13-45-30_feature.patch
```

### Method 3: Git Reset
```bash
# If changes are staged but not committed
git restore app/pricing/page.tsx

# If committed but not pushed
git reset --hard HEAD~1
```

## Automation Checklist

Before ANY implementation, this skill automatically:
- [ ] Creates TODO list for tracking
- [ ] Backs up all affected files to `.backups/YYYY-MM-DD/`
- [ ] Saves pre-change diff to `/tmp/diffs/`
- [ ] Checks file sizes and plans modularization if needed
- [ ] Evaluates if agents/skills can help
- [ ] Implements changes following best practices
- [ ] Saves post-change diff to `/tmp/diffs/`
- [ ] Verifies TypeScript types (if applicable)
- [ ] Tests build (if applicable)
- [ ] Documents rollback commands
- [ ] Reports completion with verification evidence

## Quick Commands

```bash
# View recent backups
ls -lt .backups/$(date +%Y-%m-%d)/

# View recent diffs
ls -lt /tmp/diffs/ | head -10

# Restore from backup
cp .backups/YYYY-MM-DD/HH-MM-SS_file.backup original/path

# Apply reverse diff
patch -R path/to/file < /tmp/diffs/YYYY-MM-DD_HH-MM-SS_desc.patch

# Check file sizes
find . -name "*.tsx" -o -name "*.ts" | xargs wc -l | sort -nr | head -20

# Clean old backups (keep 7 days)
find .backups/ -type f -mtime +7 -delete
```

## Related Files

- `.backups/` - Backup storage
- `/tmp/diffs/` - Diff storage
- `.claude/skills/safe-edit/SKILL.md` - This file
- `.claude/skills/safe-edit/README.md` - User documentation
