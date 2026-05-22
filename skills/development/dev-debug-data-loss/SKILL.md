---
name: Debug Data Loss
description: DEBUG mysteriously disappearing tasks using the taskDisappearanceLogger. Use when tasks vanish without user deletion, data seems to be lost, or you need to track what's modifying the task array. Provides comprehensive logging of all task array operations.
---

# Debug Data Loss

## When to Use This Skill

Activate this skill when:
- Tasks are mysteriously disappearing without user deletion
- Data loss is suspected but can't be reproduced
- You need to track what code paths are modifying `tasks.value`
- Cross-tab sync or undo/redo is suspected of causing data loss

## Task Disappearance Logger

**Location**: `src/utils/taskDisappearanceLogger.ts`

The logger tracks all modifications to the task array and identifies when tasks disappear without explicit user deletion.

### Current Status

The logger is **auto-enabled** on app startup (added for BUG-020 investigation).
- Auto-enable code: `src/main.ts` (lines 74-79)
- Periodic snapshots every 30 seconds when enabled
- Persists logs to localStorage

### Browser Console API

```javascript
// Enable/Disable monitoring
window.taskLogger.enable()
window.taskLogger.disable()

// Check for disappeared tasks (most important!)
window.taskLogger.getDisappearedTasks()

// Get summary of all logging
window.taskLogger.printSummary()

// Search for a specific task in history
window.taskLogger.findTaskInHistory("task title or id")

// Get all logs
window.taskLogger.getLogs()

// Get all snapshots
window.taskLogger.getSnapshots()

// Export logs for analysis
window.taskLogger.exportLogs()

// Clear all history
window.taskLogger.clearHistory()
```

### What Gets Logged

The logger wraps all `tasks.value =` assignments in these files:

| File | Operations Logged |
|------|-------------------|
| `src/stores/tasks.ts` | All task array replacements (12 locations) |
| `src/composables/useCrossTabSync.ts` | Cross-tab delete operations |
| `src/main.ts` | Auto-enable on startup |

### Log Sources

Each log entry includes a `source` field identifying where the change occurred:

| Source | Description |
|--------|-------------|
| `loadFromPouchDB` | Task array loaded from database |
| `localStorage-userBackup-restore` | Restored from user backup |
| `localStorage-importedTasks-restore` | Restored from import |
| `createSampleTasks-initial` | Sample tasks created for new users |
| `error-recovery-*` | Error recovery operations |
| `debugLoadTasksDirectly-*` | Direct debug load operations |
| `undo-restoreTaskState` | Undo operation |
| `undo-emergencyRestore` | Emergency restore after failed undo |
| `crossTabSync-delete` | Cross-tab sync deleted a task |
| `crossTabSync-bulkDelete` | Cross-tab sync bulk delete |
| `deleteTask-*` | User-initiated delete (marked as intentional) |

### Analyzing Disappearances

When a task disappears, the logger records:

```typescript
interface DisappearedTask {
  task: { id, title, status, projectId }
  disappearedAt: number      // Timestamp when it vanished
  lastSeenAt: number         // Timestamp of last snapshot containing it
  lastSeenSource: string     // What operation was happening
  disappearedDuring: string  // What operation caused disappearance
  stackTrace?: string        // JavaScript stack trace
  wasUserDeletion: boolean   // false = suspicious disappearance
}
```

### Debugging Workflow

1. **Enable logging** (auto-enabled for BUG-020):
   ```javascript
   window.taskLogger.enable()
   ```

2. **Use the app normally** - reproduce the issue if possible

3. **Check for disappeared tasks**:
   ```javascript
   const disappeared = window.taskLogger.getDisappearedTasks()
   console.log(disappeared)
   ```

4. **Analyze the source**:
   - Look at `disappearedDuring` to see what operation caused it
   - Check `stackTrace` to see the exact code path
   - Compare `lastSeenSource` vs `disappearedDuring`

5. **Export for detailed analysis**:
   ```javascript
   const logs = window.taskLogger.exportLogs()
   // Copy/paste to a file for analysis
   ```

### Removing Auto-Enable

Once BUG-020 is resolved, remove auto-enable from `src/main.ts`:

```typescript
// DELETE these lines (around lines 74-79):
setTimeout(() => {
  taskDisappearanceLogger.enable()
  console.log('%c[TASK-LOGGER] Auto-enabled for BUG-020 investigation', 'color: #4CAF50; font-weight: bold')
}, 2000)
```

### Related

- **BUG-020**: Tasks randomly disappearing without user deletion
- **TASK-022**: Task Disappearance Logger & Investigation
- **TASK-024**: Review Task Disappearance Logs (scheduled review)
- **Skill**: `dev-fix-task-store` - General task store debugging
