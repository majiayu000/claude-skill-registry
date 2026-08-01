---
name: pause
description: 'Usage: /sw:pause <increment-id> --reason="<reason>"'
---

---
name: pause
description: Pause an active increment (blocked by external dependency, deprioritized)
argument-hint: [increment-id] --reason="reason"
---

# Pause Increment Command

**Usage**: `/sw:pause <increment-id> --reason="<reason>"`

---

## Purpose

Pause an active increment when:
- **Blocked** by external dependency (API keys, approvals, reviews)
- **Waiting** for another increment to complete
- **Deprioritized** (will return to later)
- **Needs discussion** before continuing

---

## Behavior

1. **Normalize increment ID**:
   - If ID contains dash (e.g., "0153-feature-name"), extract numeric portion before first dash → "0153"
   - Convert to 4-digit format (e.g., "1" → "0001", "153" → "0153")
   - Both formats work: `/sw:pause 0153` or `/sw:pause 0153-feature-name`
2. **Validates** increment exists and is "active"
3. **Prompts** for reason if not provided via --reason flag
4. **Updates** metadata.json:
   - `status`: "active" → "paused"
   - `pausedReason`: User-provided reason
   - `pausedAt`: Current timestamp
5. **Displays** confirmation message
6. **Suggests** next actions (`/sw:resume` to continue)

---

## Examples

### Pause with reason
```bash
/sw:pause 0006 --reason="Waiting for Stripe API keys"

✅ Increment 0006 paused
📝 Reason: Waiting for Stripe API keys
⏸️  No longer counts toward active limit
💡 Resume with: /sw:resume 0006
```

### Pause without reason (prompts)
```bash
/sw:pause 0006

❓ Why are you pausing this increment?
   1. Blocked by external dependency
   2. Waiting for code review
   3. Deprioritized
   4. Other (type reason)

> 1

✅ Increment 0006 paused
📝 Reason: Blocked by external dependency
💡 Resume with: /sw:resume 0006
```

---

## Edge Cases

### Already Paused
```bash
/sw:pause 0006 --reason="Different reason"

⚠️  Increment 0006 is already paused
   Previous reason: Waiting for Stripe API keys
   New reason: Different reason

Update reason? [Y/n]: y

✅ Reason updated
📝 New reason: Different reason
```

### Cannot Pause Completed
```bash
/sw:pause 0005

❌ Cannot pause increment 0005
   Status: completed
   Completed increments cannot be paused
```

### Cannot Pause Abandoned
```bash
/sw:pause 0008

❌ Cannot pause increment 0008
   Status: abandoned
   Resume it first: /sw:resume 0008
```

### Increment Not Found
```bash
/sw:pause 9999

❌ Increment not found: 9999
💡 Check available increments: /sw:status
```

---

## Implementation

This command uses the MetadataManager to update increment status:

```typescript
import { MetadataManager, IncrementStatus } from '../src/core/increment/metadata-manager';

// Read current metadata
const metadata = MetadataManager.read(incrementId);

// Validate can pause
if (metadata.status !== IncrementStatus.ACTIVE) {
  throw new Error(`Cannot pause increment with status: ${metadata.status}`);
}

// Update status
MetadataManager.updateStatus(incrementId, IncrementStatus.PAUSED, reason);
```

---

## Status Flow

```
active ──pause──> paused
   │
   └──resume──> active
```

---

## Related Commands

- `/resume <id>` - Resume paused increment
- `/abandon <id>` - Abandon increment (permanent)
- `/status` - Show all increment statuses

---

## Best Practices

✅ **Always provide a reason** - Helps future you remember context

✅ **Review paused increments weekly** - Don't let them pile up

✅ **Set calendar reminder** - For external blockers (API keys, approvals)

✅ **Resume or abandon** - After 7+ days paused

❌ **Don't pause as procrastination** - Address scope/motivation issues instead

❌ **Don't pause to start new work** - Finish current work first (focus)

---

## Warning: Stale Paused Increments

Increments paused for **7+ days** trigger warnings in `/sw:status`:

```bash
/sw:status

⏸️  Paused (1):
  🔄 0007-stripe-integration [feature]
     Paused: 10 days ago
     Reason: Waiting for Stripe API keys
     ⚠️  STALE! Review or abandon?

💡 Actions:
   /sw:resume 0007  # If unblocked
   /sw:abandon 0007 # If no longer needed
```

---

**Command**: `/sw:pause`
**Plugin**: specweave (core)
**Version**: v0.7.0
**Part of**: Increment 0007 - Smart Status Management
