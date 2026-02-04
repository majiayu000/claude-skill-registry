---
name: restore
description: Restore archived increments back to active folder
---

# Restore Increment from Archive

Restore an archived increment back to the main increments folder. Useful when you need to reference, update, or continue work on an old increment.

## Usage

```bash
# Restore specific increment
/sw:restore 0031

# Restore multiple increments
/sw:restore 0001 0002 0003

# List archived increments
/sw:restore --list
```

## Arguments

- `<increment-ids>`: Increment IDs to restore (e.g., "1", "0001", "0031")
- `--list`: List all archived increments without restoring

## Examples

### Example 1: Restore Specific Increment

```bash
/sw:restore 0031
```

**Output**:
```
📦 Restoring increment from archive...

Increment: 0031-external-tool-status-sync
Source: .specweave/increments/_archive/0031-external-tool-status-sync/
Target: .specweave/increments/0031-external-tool-status-sync/

Checking target location...
  ✓ Target location is empty

✅ Restored: 0031-external-tool-status-sync
   Location: .specweave/increments/0031-external-tool-status-sync/

📊 Archive Statistics:
   Active: 33 increments (+ 1 restored)
   Archived: 30 increments (- 1)

Next: /sw:do 0031 (to continue work)
```

### Example 2: List Archived Increments

```bash
/sw:restore --list
```

**Output**:
```
📦 Archived Increments:

.specweave/increments/_archive/
├── 0001-core-framework (152 days old)
├── 0002-plugin-system (148 days old)
├── 0003-auth-service (145 days old)
├── 0004-payment-integration (142 days old)
├── 0005-api-gateway (140 days old)
...
├── 0030-jira-integration (35 days old)
└── 0031-external-tool-status-sync (12 days old)

Total: 31 archived increments

To restore: /sw:restore <increment-id>
```

### Example 3: Restore Multiple Increments

```bash
/sw:restore 0030 0031
```

**Output**:
```
📦 Restoring increments from archive...

Restoring 0030-jira-integration...
  ✅ Restored

Restoring 0031-external-tool-status-sync...
  ✅ Restored

✅ Restored: 2 increments

📊 Archive Statistics:
   Active: 34 increments (+ 2 restored)
   Archived: 29 increments (- 2)
```

## Error Handling

### Increment Not Found in Archive

```
❌ Error: Increment 0031 not found in archive

Archive location: .specweave/increments/_archive/

Available archived increments:
  • 0001-core-framework
  • 0002-plugin-system
  • 0003-auth-service
  ...

Use: /sw:restore --list to see all
```

### Target Location Already Exists

```
❌ Error: Cannot restore 0031 - already exists in active folder

Conflict:
  Archive: .specweave/increments/_archive/0031-external-tool-status-sync/
  Active: .specweave/increments/0031-external-tool-status-sync/

Options:
  1. Delete active version first (if it's a duplicate)
  2. Resolve duplicates: /sw:fix-duplicates
  3. Archive active version: /sw:archive 0031
  4. Rename one version manually

Recommended: /sw:fix-duplicates (auto-resolves conflicts)
```

### Permission Errors

```
❌ Error: Permission denied

Could not move:
  From: .specweave/increments/_archive/0031-external-tool-status-sync/
  To: .specweave/increments/0031-external-tool-status-sync/

Check:
  • File permissions
  • Disk space
  • Files not open in another program
```

## Safety Checks

Before restoring, the system checks:
- ✅ **Increment exists in archive**: Source folder exists
- ✅ **Target location empty**: No conflict in main folder
- ✅ **Valid increment structure**: Has required files (metadata.json)
- ✅ **Disk space available**: Enough space for restored files

## Related Commands

- `/sw:archive <increment-id>` - Archive completed increments
- `/sw:status` - View archive statistics
- `/sw:fix-duplicates` - Auto-resolve duplicate increments
- `/sw:do <increment-id>` - Resume work on restored increment

## Implementation

```typescript
import { Task } from '@claude/types';

const task = new Task('restore-increment', 'Restore increment from archive');

task.run(async () => {
  const { IncrementArchiver } = await import('../../../dist/src/core/increment/increment-archiver.js');
  const archiver = new IncrementArchiver(process.cwd());

  // Parse arguments
  const args = process.argv.slice(2);

  // List mode
  if (args.includes('--list')) {
    const archived = await archiver.listArchived();
    console.log('\n📦 Archived Increments:\n');

    if (archived.length === 0) {
      console.log('No archived increments found.');
      return;
    }

    console.log('.specweave/increments/_archive/');
    archived.forEach(inc => {
      console.log(`├── ${inc}`);
    });
    console.log(`\nTotal: ${archived.length} archived increments`);
    console.log('\nTo restore: /sw:restore <increment-id>');
    return;
  }

  // Restore mode
  const incrementIds = args.filter(arg => !arg.startsWith('--'));

  if (incrementIds.length === 0) {
    console.error('❌ Error: No increment IDs provided');
    console.log('\nUsage:');
    console.log('  /sw:restore <increment-id>');
    console.log('  /sw:restore --list');
    return;
  }

  // Restore each increment
  let restored = 0;
  let errors = 0;

  for (const id of incrementIds) {
    try {
      // Normalize ID to 4-digit format
      const normalizedId = id.padStart(4, '0');

      // Find archived increment
      const archived = await archiver.listArchived();
      const match = archived.find(inc => inc.startsWith(normalizedId));

      if (!match) {
        console.error(`❌ Increment ${normalizedId} not found in archive`);
        errors++;
        continue;
      }

      // Restore increment
      await archiver.restore(match);
      console.log(`✅ Restored: ${match}`);
      restored++;
    } catch (error) {
      console.error(`❌ Failed to restore ${id}: ${error.message}`);
      errors++;
    }
  }

  // Show statistics
  if (restored > 0 || errors > 0) {
    console.log('\n📊 Restore Summary:');
    if (restored > 0) {
      console.log(`   ✅ Restored: ${restored} increment${restored > 1 ? 's' : ''}`);
    }
    if (errors > 0) {
      console.log(`   ❌ Errors: ${errors} increment${errors > 1 ? 's' : ''}`);
    }

    // Show updated stats
    const stats = await archiver.getStats();
    console.log('\n📊 Archive Statistics:');
    console.log(`   Active: ${stats.active} increments`);
    console.log(`   Archived: ${stats.archived} increments`);
  }
});

export default task;
```

## Important Notes

### Archive is Not Deletion

**Archives are preserved history**, not deleted work. You can restore anytime:
- ✅ Full increment structure preserved
- ✅ All files, reports, and metadata intact
- ✅ Git history preserved (if committed)
- ✅ External tool links preserved in metadata

### When to Restore

Common scenarios for restoring from archive:
- 🔍 **Reference old implementation** - Check how something was done
- 🔄 **Resume abandoned work** - Pick up where you left off
- 🐛 **Bug investigation** - Review completed increment for context
- 📝 **Documentation** - Update reports or completion summaries
- 🔗 **External sync recovery** - Re-sync to GitHub/JIRA if needed

### After Restoring

Once restored, the increment is back in the active folder:
- ✅ Shows up in `/sw:status`
- ✅ Can be resumed with `/sw:do`
- ✅ Can be re-archived with `/sw:archive`
- ✅ Included in increment counts and WIP limits

---

**Best Practice**: Keep archives clean by only restoring when needed, then re-archiving when done.

**Recommended Workflow**:
```bash
# 1. List archived increments
/sw:restore --list

# 2. Restore specific increment
/sw:restore 0031

# 3. Review or update the increment
cat .specweave/increments/0031-external-tool-status-sync/spec.md

# 4. Re-archive when done
/sw:archive 0031
```
