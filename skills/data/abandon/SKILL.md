---
name: abandon
description: 'Usage: /sw:abandon <increment-id> --reason="<reason>"'
---

---
name: abandon
description: Abandon an incomplete increment (requirements changed, obsolete)
argument-hint: [increment-id] --reason="reason"
---

# Abandon Increment Command

**Usage**: `/sw:abandon <increment-id> --reason="<reason>"`

⚠️  **THIS ACTION MOVES THE INCREMENT TO `_archive/` FOLDER**

---

## Purpose

Abandon an increment when:
- **Requirements changed** (feature no longer needed)
- **Approach wrong** (discovered better solution)
- **Superseded** (replaced by different increment)
- **Experiment failed** (spike didn't pan out)

---

## Behavior

1. **Normalize increment ID**:
   - If ID contains dash (e.g., "0153-feature-name"), extract numeric portion before first dash → "0153"
   - Convert to 4-digit format (e.g., "1" → "0001", "153" → "0153")
   - Both formats work: `/sw:abandon 0153` or `/sw:abandon 0153-feature-name`
2. **Validates** increment exists and is NOT "completed"
3. **Prompts** for reason if not provided
4. **Confirmation prompt** ("This is permanent. Continue? [y/N]")
5. **Updates** metadata.json:
   - `status`: → "abandoned"
   - `abandonedReason`: User-provided reason
   - `abandonedAt`: Current timestamp
6. **Moves folder**:
   - From: `.specweave/increments/{id}/`
   - To: `.specweave/increments/_archive/{id}/`
7. **Displays** confirmation with preserved location

---

## Examples

### Abandon with reason
```bash
/sw:abandon 0008 --reason="Requirements changed - feature no longer needed"

⚠️  This will move increment 0008 to _archive/
   Reason: Requirements changed - feature no longer needed

Continue? [y/N]: y

✅ Increment 0008 abandoned
📦 Moved to: .specweave/increments/_archive/0008-old-feature/
📝 Reason: Requirements changed - feature no longer needed
💾 All work preserved for reference

💡 To un-abandon: Manually move back to increments/ folder
```

### Abandon without reason (prompts)
```bash
/sw:abandon 0009

❓ Why are you abandoning this increment?
   1. Requirements changed
   2. Approach was wrong
   3. Superseded by different work
   4. Experiment failed
   5. Other (type reason)

> 1

⚠️  This will move increment 0009 to _archive/
   Reason: Requirements changed

Continue? [y/N]: y

✅ Increment 0009 abandoned
📦 Moved to: .specweave/increments/_archive/0009-experiment/
```

---

## Edge Cases

### Cannot Abandon Completed
```bash
/sw:abandon 0005

❌ Cannot abandon increment 0005
   Status: completed
   Completed increments cannot be abandoned

💡 Increments are done - no need to abandon
```

### Already Abandoned
```bash
/sw:abandon 0008

⚠️  Increment 0008 is already abandoned
   Location: .specweave/increments/_abandoned/0008-old-feature/
   Reason: Requirements changed

No action needed.
```

### Increment Not Found
```bash
/sw:abandon 9999

❌ Increment not found: 9999
💡 Check available increments: /sw:status
```

### Cancel Abandonment
```bash
/sw:abandon 0008 --reason="Not needed"

⚠️  This will move increment 0008 to _archive/
   Reason: Not needed

Continue? [y/N]: n

❌ Abandonment cancelled
   Increment 0008 remains active
```

---

## Implementation

This command uses the MetadataManager and file system operations:

```typescript
import { MetadataManager, IncrementStatus } from '../src/core/increment/metadata-manager';
import * as fs from 'fs-extra';
import * as path from 'path';

// Read current metadata
const metadata = MetadataManager.read(incrementId);

// Validate can abandon
if (metadata.status === IncrementStatus.COMPLETED) {
  throw new Error('Cannot abandon completed increment');
}

// Confirmation prompt
const confirmed = await prompt('Continue? [y/N]');
if (!confirmed) {
  console.log('Abandonment cancelled');
  return;
}

// Update metadata
MetadataManager.updateStatus(incrementId, IncrementStatus.ABANDONED, reason);

// Move to _archive/ folder
const fromPath = path.join('.specweave/increments', incrementId);
const toPath = path.join('.specweave/increments/_archive', incrementId);
fs.moveSync(fromPath, toPath);

console.log(`✅ Moved to: ${toPath}`);
```

---

## Status Flow

```
active ──abandon──> abandoned
   │
paused ──abandon──> abandoned
   │
abandoned (already abandoned - no-op)

completed (CANNOT abandon)
```

---

## _archive/ Folder Structure

```
.specweave/increments/
├── 0023-release-management/      # Active
├── 0024-bidirectional-spec/      # Active
├── 0025-per-project-config/      # Active
├── _archive/                      # All archived/abandoned/old increments
│   ├── 0001-core-framework/       # Completed (archived)
│   ├── 0002-core-enhancements/    # Completed (archived)
│   ├── 0008-old-approach/         # Abandoned
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── metadata.json (status: abandoned)
│   ├── 0009-failed-experiment/    # Abandoned
│   └── 0029-cicd-auto-fix/        # Abandoned
└── _backlog/                       # Future work
```

---

## Un-Abandoning (Manual Process)

To un-abandon an increment:

```bash
# 1. Move back to increments/
mv .specweave/increments/_archive/0008-feature \
   .specweave/increments/0008-feature

# 2. Resume via command
/sw:resume 0008

✅ Increment 0008 resumed
⚠️  Note: Was abandoned 10 days ago
   Reason: Requirements changed
💡 Review spec.md to ensure still relevant
```

---

## Related Commands

- `/sw:pause <id>` - Pause increment (temporary, can resume)
- `/sw:resume <id>` - Resume paused or abandoned increment
- `/sw:status` - Show all increments (including abandoned count)
- `/sw:status --abandoned` - Show only abandoned increments

---

## Best Practices

✅ **Always provide clear reason** - Future you will thank you

✅ **Document learnings** - Add retrospective notes to spec.md before abandoning

✅ **Extract reusable parts** - Move to _backlog/ if salvageable

✅ **Communicate** - Let team know if collaborative

❌ **Don't abandon as procrastination** - Pause if temporarily blocked

❌ **Don't delete** - Abandon moves to _abandoned/, preserves history

---

## Auto-Abandonment (Experiments)

Experiments (--type=experiment) auto-abandon after **14 days** of inactivity:

```bash
# Create experiment
/sw:inc "Try GraphQL" --type=experiment

# ... 15 days pass with no activity ...

# Automatic abandonment
/sw:status

📊 Auto-Abandoned (1):
  🧪 0010-graphql-experiment [experiment]
     Abandoned: automatically (14+ days inactive)
     Created: 15 days ago
     Last activity: 15 days ago

💡 Experiments auto-abandon after 14 days of inactivity
   To prevent: Update lastActivity via /sw:do or manual touch
```

---

## Statistics

View abandonment statistics:

```bash
/sw:status

✅ Completed (4):
  0001-core-framework
  0002-core-enhancements
  0003-model-selection
  0004-plugin-architecture

❌ Abandoned (3):
  0008-old-approach (Requirements changed)
  0009-failed-experiment (Experiment failed)
  0010-superseded (Replaced by 0011)

📊 Summary:
  - Success rate: 57% (4/7 completed)
  - Abandonment rate: 43% (3/7 abandoned)
  - Common reasons: Requirements changed (2), Experiment failed (1)
```

---

## Abandoned Increments as Learning

Abandoned work is valuable!

- **Retrospectives**: What went wrong? Why did requirements change?
- **Patterns**: Are we over-committing? Under-planning?
- **Learnings**: Failed experiments teach us what NOT to do
- **Reference**: Abandoned specs can inform future work

💡 Periodically review `_archive/` folder for insights

---

**Command**: `/sw:abandon`
**Plugin**: specweave (core)
**Version**: v0.7.0
**Part of**: Increment 0007 - Smart Status Management
