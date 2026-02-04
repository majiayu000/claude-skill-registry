---
name: sync-acs
description: Manually synchronize acceptance criteria (AC) checkbox status in spec.md based on task completion
---

# Sync Acceptance Criteria Status

**Purpose**: Manually trigger AC checkbox synchronization to ensure spec.md acceptance criteria accurately reflect task completion status.

**Use When**:
- AC checkboxes in spec.md are out of sync with completed tasks
- After manually completing tasks without running the hook
- To verify AC status before closing an increment
- To resolve conflicts between manual AC edits and task completion

---

## How It Works

1. **Detect Active Increment**
   - Find increment in-progress
   - Check if spec.md and tasks.md exist

2. **Parse Task Completion**
   - Extract all tasks from tasks.md
   - Map AC-IDs to completion status
   - Calculate percentage complete per AC (# complete tasks / # total tasks)

3. **Parse AC Definitions**
   - Extract all ACs from spec.md
   - Track current checkbox state ([ ] or [x])
   - Map line numbers for atomic updates

4. **Intelligent Sync Logic**
   - **100% Complete**: Update [ ] → [x]
   - **< 100% Complete**: Keep [ ] (partial work)
   - **Conflict Detection**: AC is [x] but tasks incomplete → WARN
   - **Orphaned ACs**: AC has no implementing tasks → WARN

5. **Atomic File Update**
   - Update spec.md only if changes needed
   - Preserve manual overrides (conflicts)
   - Log all changes to metadata.json

---

## Usage

```bash
# Auto-detect and sync active increment
/sw:sync-acs

# Sync specific increment
/sw:sync-acs 0039

# Show what would change (dry run)
/sw:sync-acs --dry-run

# Force sync (ignore conflicts)
/sw:sync-acs --force

# Validate only (check for mismatches)
/sw:sync-acs --validate
```

---

## Implementation

The command uses **ACStatusManager** for sophisticated synchronization:

```typescript
import { ACStatusManager } from '../../../../../src/core/increment/ac-status-manager';

const manager = new ACStatusManager(process.cwd());
const result = await manager.syncACStatus(incrementId);

// result.synced: true if sync was performed
// result.updated: string[] - AC-IDs updated to [x]
// result.conflicts: string[] - Conflicts detected
// result.warnings: string[] - Orphaned ACs, missing files
// result.changes: string[] - Human-readable diff
```

### Step 1: Find Active Increment

```bash
# Auto-detect active increment
ACTIVE_INCREMENT=$(ls -t .specweave/increments/ 2>/dev/null | grep -v "_backlog\|_archive" | head -1)

if [[ -z "$ACTIVE_INCREMENT" ]]; then
    echo "❌ No active increment found"
    exit 1
fi

echo "🔄 Syncing AC status for $ACTIVE_INCREMENT..."
```

### Step 2: Call ACStatusManager

```bash
# Use the update-ac-status.js hook script (already integrated)
node plugins/specweave/lib/hooks/update-ac-status.js "$ACTIVE_INCREMENT"
```

Or invoke directly:

```typescript
const result = await manager.syncACStatus(incrementId);
```

### Step 3: Display Results

```bash
# Updated ACs
if [[ -n "${result.updated}" ]]; then
    echo "✅ Updated AC checkboxes:"
    for acId in "${result.updated[@]}"; do
        echo "   $acId → [x]"
    done
fi

# Conflicts
if [[ -n "${result.conflicts}" ]]; then
    echo "⚠️  Conflicts detected:"
    for conflict in "${result.conflicts[@]}"; do
        echo "   $conflict"
    done
fi

# Warnings
if [[ -n "${result.warnings}" ]]; then
    echo "⚠️  Warnings:"
    for warning in "${result.warnings[@]}"; do
        echo "   $warning"
    done
fi
```

---

## Example Scenarios

### Scenario 1: Normal Sync (100% Complete AC)

**Before**:
```markdown
# spec.md
- [ ] AC-US1-01: User can login
- [ ] AC-US1-02: Session persists

# tasks.md
#### T-001: Implement login API
**AC**: AC-US1-01
**Status**: [x] (100% - Completed)

#### T-002: Add session storage
**AC**: AC-US1-01
**Status**: [x] (100% - Completed)
```

**After**:
```markdown
# spec.md
- [x] AC-US1-01: User can login  ✓ UPDATED
- [ ] AC-US1-02: Session persists
```

**Output**:
```
🔄 Syncing AC status for increment 0039...

✅ Updated AC checkboxes:
   AC-US1-01 → [x]

📝 Changes:
   AC-US1-01: [ ] → [x] (2/2 tasks complete - 100%)
```

---

### Scenario 2: Partial Completion (No Update)

**Before**:
```markdown
# spec.md
- [ ] AC-US1-02: Session persists

# tasks.md
#### T-003: Add Redis session store
**AC**: AC-US1-02
**Status**: [x] (100% - Completed)

#### T-004: Test session expiry
**AC**: AC-US1-02
**Status**: [ ] (0% - Not started)
```

**After**:
```markdown
# spec.md
- [ ] AC-US1-02: Session persists  (NO CHANGE - 50% complete)
```

**Output**:
```
🔄 Syncing AC status for increment 0039...

ℹ️  No AC updates needed

📊 Completion Status:
   AC-US1-02: 1/2 tasks complete (50%) - threshold not met
```

---

### Scenario 3: Conflict Detection

**Before**:
```markdown
# spec.md
- [x] AC-US1-03: Data validated (manually checked)

# tasks.md
#### T-005: Add validation rules
**AC**: AC-US1-03
**Status**: [x] (100% - Completed)

#### T-006: Add error handling
**AC**: AC-US1-03
**Status**: [ ] (0% - Not started)
```

**After**:
```markdown
# spec.md
- [x] AC-US1-03: Data validated (PRESERVED - conflict detected)
```

**Output**:
```
🔄 Syncing AC status for increment 0039...

⚠️  Conflicts detected:
   AC-US1-03: Marked [x] but only 1/2 tasks complete (50%)
   → Manual override preserved (no change made)

💡 Tip: Review tasks for AC-US1-03 or uncheck manually if premature
```

---

### Scenario 4: Orphaned AC Warning

**Before**:
```markdown
# spec.md
- [ ] AC-US1-04: Performance optimized
- [ ] AC-US1-05: Security hardened

# tasks.md
#### T-007: Implement caching
**AC**: AC-US1-04
**Status**: [x] (100% - Completed)

(No tasks reference AC-US1-05)
```

**Output**:
```
🔄 Syncing AC status for increment 0039...

✅ Updated AC checkboxes:
   AC-US1-04 → [x]

⚠️  Warnings:
   AC-US1-05: No implementing tasks found (orphaned AC)
   → Add tasks or remove AC from spec.md
```

---

## Integration with Hooks

### Automatic Sync (Post-Task-Completion Hook)

The hook automatically calls `ACStatusManager.syncACStatus()` after every task completion:

```bash
# plugins/specweave/hooks/post-task-completion.sh (lines 232-269)
if [ -n "$CURRENT_INCREMENT" ]; then
    node plugins/specweave/lib/hooks/update-ac-status.js "$CURRENT_INCREMENT"
fi
```

**Disable automatic sync**:
```bash
export SKIP_AC_SYNC=true
# Now hooks won't sync ACs (useful for batch work)
```

---

## Integration with Other Commands

### /sw:validate
```bash
# Validate ACs before closing increment
/sw:sync-acs --validate
# Warns if ACs out of sync
```

### /sw:done
```bash
# Auto-sync ACs before closing
/sw:sync-acs
# Then proceed with increment closure
```

### /sw:progress
```bash
# Show AC completion alongside task progress
/sw:sync-acs --status
# Display: 8/10 ACs complete (80%)
```

---

## Success Criteria

- ✅ Syncs AC checkboxes based on task completion (100% threshold)
- ✅ Detects and preserves manual overrides (conflicts)
- ✅ Warns about orphaned ACs (no implementing tasks)
- ✅ Shows clear diff of changes before/after
- ✅ Atomic file writes (no corruption risk)
- ✅ Integrates with post-task-completion hook
- ✅ Supports dry-run mode
- ✅ Logs all changes to metadata.json

---

**This command ensures acceptance criteria accurately reflect implementation progress!**
