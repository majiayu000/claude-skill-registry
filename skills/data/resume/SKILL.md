---
name: resume
description: Resume a paused or backlog increment
argument-hint: [increment-id]
---

# Resume Increment Command

**Usage**: `/sw:resume <increment-id>`

---

## Purpose

Resume a paused or backlog increment when:
- **From Backlog**: Ready to start planned work
- **From Paused**: Blocker resolved (API keys arrived, approval granted)
- **From Paused**: Ready to continue after deprioritization
- **From Paused**: Prerequisite completed (can now proceed)

---

## Behavior

1. **Normalize increment ID**:
   - If ID contains dash (e.g., "0153-feature-name"), extract numeric portion before first dash → "0153"
   - Convert to 4-digit format (e.g., "1" → "0001", "153" → "0153")
   - Both formats work: `/sw:resume 0153` or `/sw:resume 0153-feature-name`
2. **Validates** increment exists and is "paused" or "backlog"
3. **Calculates** pause/backlog duration (days, hours)
4. **Updates** metadata.json:
   - `status`: "paused" or "backlog" → "active"
   - Clears `pausedReason` and `pausedAt` (if paused)
   - Clears `backlogReason` and `backlogAt` (if backlog)
   - Updates `lastActivity` timestamp
4. **Displays** context (duration, last activity)
5. **Suggests** next actions (`/sw:do` to continue/start work)

---

## Examples

### Resume from backlog
```bash
/sw:resume 0032

✅ Increment 0032 activated from backlog
📦 Was in backlog for: 5 days
💡 Reason: Low priority, focus on 0031 first
📋 Start work with: /sw:do
```

### Resume paused work after a few days
```bash
/sw:resume 0006

✅ Increment 0006 resumed
⏱️  Was paused for: 3 days, 4 hours
💡 Last activity: Created translation pipeline
📋 Continue with: /sw:do
```

### Resume paused work after a few hours
```bash
/sw:resume 0007

✅ Increment 0007 resumed
⏱️  Was paused for: 2 hours
📋 Continue with: /sw:do
```

---

## Edge Cases

### Already Active
```bash
/sw:resume 0006

⚠️  Increment 0006 is already active
   No action needed. Continue with: /sw:do
```

### Cannot Resume Completed
```bash
/sw:resume 0005

❌ Cannot resume increment 0005
   Status: completed
   Increment is already complete
```

### Resume Abandoned (Confirmation Required)
```bash
/sw:resume 0008

⚠️  Increment 0008 is abandoned
   Reason: Requirements changed

   Are you sure you want to resume? [y/N]: y

✅ Increment 0008 resumed
⚠️  Note: Was abandoned 5 days ago
💡 Review spec.md to ensure still relevant
📋 Continue with: /sw:do
```

### Increment Not Found
```bash
/sw:resume 9999

❌ Increment not found: 9999
💡 Check paused increments: /sw:status --paused
```

---

## Implementation

This command uses the MetadataManager to update increment status:

```typescript
import { MetadataManager, IncrementStatus } from '../src/core/increment/metadata-manager';

// Read current metadata
const metadata = MetadataManager.read(incrementId);

// Validate can resume
if (metadata.status === IncrementStatus.COMPLETED) {
  throw new Error('Cannot resume completed increment');
}

// Calculate duration based on status
let duration;
if (metadata.status === IncrementStatus.PAUSED && metadata.pausedAt) {
  duration = calculateDuration(metadata.pausedAt, new Date());
  console.log(`Was paused for: ${duration}`);
} else if (metadata.status === IncrementStatus.BACKLOG && metadata.backlogAt) {
  duration = calculateDuration(metadata.backlogAt, new Date());
  console.log(`Was in backlog for: ${duration}`);
}

// Update status to active
MetadataManager.updateStatus(incrementId, IncrementStatus.ACTIVE);

// Display context
console.log(`Last activity: ${getLastActivity(incrementId)}`);
```

---

## Status Flow

```
backlog ──resume──> active (start work)
   │
paused ──resume──> active (continue work)
   │
abandoned ──resume──> active (with confirmation)
```

---

## Related Commands

- `/sw:pause <id>` - Pause active increment
- `/sw:backlog <id>` - Move increment to backlog
- `/sw:status` - Show all increment statuses
- `/sw:status --paused` - Show only paused increments
- `/sw:status --backlog` - Show only backlog increments
- `/sw:do` - Continue/start work after resuming

---

## Best Practices

✅ **Review spec.md first** - Especially after long pauses

✅ **Check for changes** - Dependencies, requirements may have changed

✅ **Update estimates** - If scope changed during pause

✅ **Communicate** - Let team know you're resuming (if collaborative)

❌ **Don't blindly resume** - Re-validate context first

❌ **Don't resume abandoned without review** - Understand why it was abandoned

---

## Automatic Suggestions

When you run `/sw:status`, stale paused/backlog increments trigger suggestions:

```bash
/sw:status

🗂️  Backlog (2):
  📦 0032-feature-a [feature]
     In backlog: 5 days
     Reason: Low priority
     💡 Ready to start? → /sw:resume 0032

⏸️  Paused (2):
  🔄 0006-stripe [feature]
     Paused: 3 days ago
     Reason: Waiting for API keys
     💡 Check if API keys arrived → /sw:resume 0006

  🔄 0007-refactor [refactor]
     Paused: 10 days ago
     Reason: Deprioritized
     ⚠️  STALE! Consider resuming or abandoning
```

---

## Context Recovery

After resuming, the command shows helpful context:

```bash
/sw:resume 0006

✅ Increment 0006 resumed

📊 Status before pause:
   - Progress: 30% (6/20 tasks done)
   - Last completed: T-005 (Create translation pipeline)
   - Paused reason: Waiting for Stripe API keys

💡 Next steps:
   1. Review spec.md (requirements may have changed)
   2. Check dependencies (are API keys available?)
   3. Continue with: /sw:do

📋 Quick commands:
   /sw:do           # Resume work
   /sw:progress     # See detailed progress
   /sw:validate     # Check increment health
```

---

**Command**: `/sw:resume`
**Plugin**: specweave (core)
**Version**: v0.7.0
**Part of**: Increment 0007 - Smart Status Management
