---
name: dev-fix-task-store
description: MASTER Pinia task store debugging covering synchronization, CRUD operations, state persistence, IndexedDB conflicts, advanced state management, and complex store architecture. Fix when tasks don't save, disappear unexpectedly, don't update in UI, backup systems read wrong data, store actions fail, or advanced performance issues occur. CRITICAL: All store fixes MUST be tested with Playwright before claiming success.
---

# Fix Task Store Issues

## Instructions

### Task Store Debugging Protocol
When task operations don't work correctly, systematically debug:

#### 1. Task CRUD Operations
- **Check task creation** - verify tasks are added to store correctly
- **Debug task updates** - ensure changes persist and reactivity works
- **Verify task deletion** - confirm removal from store and UI
- **Check for duplicate task IDs** or data corruption

#### 2. Store Reactivity Issues
- **Verify store subscription** in components
- **Check for direct state mutation** vs action usage
- **Debug task list reactivity** and computed properties
- **Ensure proper store instance sharing**

#### 3. Persistence Problems
- **Check localStorage/sessionStorage** integration
- **Debug data serialization/deserialization**
- **Verify data integrity** across browser sessions
- **Check for storage quota exceeded** errors

#### 4. Pinia Store Architecture (Integrated from dev-fix-pinia)
- **Verify store instance is shared** across components
- **Check for multiple store instances** being created
- **Use `$patch()`** for multiple state updates
- **Never assign directly to `$state`** (breaks reactivity)
- **Clean up subscriptions** on component unmount
- **Use Vue DevTools** to inspect state mutations

## Common Pinia Issues & Solutions (Integrated)

### State Not Updating
```typescript
// ❌ BAD: Direct assignment breaks reactivity
store.$state = newState

// ✅ GOOD: Use patch for updates
store.$patch(newState)

// ✅ GOOD: Use action for complex updates
store.updateTasks(newTasks)
```

### Store Instance Problems
```typescript
// ❌ BAD: Creating multiple instances
const store1 = useTaskStore()
const store2 = useTaskStore() // Different instance!

// ✅ GOOD: Shared instance
const store = useTaskStore() // Same across components
```

### Subscription Cleanup
```typescript
// ✅ GOOD: Auto-cleanup subscription
const unsubscribe = store.$subscribe((mutation, state) => {
  // Handle state changes
}, { detached: false }) // Auto cleanup on unmount

// ✅ GOOD: Manual cleanup in onUnmounted
onUnmounted(() => {
  unsubscribe()
})
```

## Common Task Store Issues & Solutions

### Tasks Not Appearing in UI
```typescript
// ❌ BAD: Direct state mutation
const addTaskBad = (task) => {
  tasks.push(task) // Won't trigger reactivity
}

// ✅ GOOD: Using Pinia action
const addTask = (taskData) => {
  const task = {
    id: generateId(),
    ...taskData,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }

  this.tasks.push(task)
  this.saveToStorage() // If using persistence

  console.log('✅ Task added:', task)
  return task
}
```

### Store State Debugging
```typescript
const debugTaskStore = () => {
  // Watch store mutations
  taskStore.$subscribe((mutation, state) => {
    console.group('🔄 Task store mutation')
    console.log('Type:', mutation.type)
    console.log('Payload:', mutation.payload)
    console.log('Tasks count:', state.tasks.length)
    console.log('Recent tasks:', state.tasks.slice(-3))
    console.groupEnd()
  })

  // Debug specific operations
  const originalAddTask = taskStore.addTask
  taskStore.addTask = function(...args) {
    console.log('➕ Adding task:', args[0])
    const result = originalAddTask.apply(this, args)
    console.log('✅ Task added result:', result)
    return result
  }
}
```

### Persistence Issues
```typescript
const debugTaskPersistence = () => {
  const checkStorageConsistency = () => {
    try {
      const stored = localStorage.getItem('pomo-tasks')
      const current = JSON.stringify(taskStore.tasks)

      if (stored !== current) {
        console.warn('Storage inconsistency detected:', {
          storedCount: stored ? JSON.parse(stored).length : 0,
          currentCount: taskStore.tasks.length
        })
      }
    } catch (error) {
      console.error('Storage check failed:', error)
    }
  }

  // Monitor storage changes across tabs
  window.addEventListener('storage', (e) => {
    if (e.key === 'pomo-tasks') {
      console.log('🔄 Tasks updated in another tab')
      // Reload store from storage
      taskStore.loadFromStorage()
    }
  })

  return { checkStorageConsistency }
}
```

### Task ID Conflicts
```typescript
const debugTaskIds = () => {
  const checkForDuplicates = () => {
    const taskIds = taskStore.tasks.map(t => t.id)
    const duplicates = taskIds.filter((id, index) => taskIds.indexOf(id) !== index)

    if (duplicates.length > 0) {
      console.error('🚨 Duplicate task IDs found:', duplicates)

      // Fix duplicates by regenerating IDs
      duplicates.forEach(duplicateId => {
        const task = taskStore.tasks.find(t => t.id === duplicateId)
        if (task) {
          taskStore.updateTask(duplicateId, {
            id: generateId(),
            updatedAt: new Date().toISOString()
          })
        }
      })
    }

    return duplicates
  }

  // Verify ID uniqueness
  const verifyIdUniqueness = (taskId) => {
    const isUnique = !taskStore.tasks.some(t => t.id === taskId)
    console.log(`🔍 Task ID ${taskId} unique:`, isUnique)
    return isUnique
  }

  return { checkForDuplicates, verifyIdUniqueness }
}
```

### Component Store Integration
```typescript
const debugComponentStoreIntegration = () => {
  // Check if components are using the store correctly
  const checkStoreUsage = (componentName) => {
    console.group(`🔍 Checking ${componentName} store usage`)

    // Check for proper store instance
    const store = useTaskStore()
    console.log('Store instance:', !!store)

    // Check for reactive usage
    const { tasks, projects } = storeToRefs(store)
    console.log('Reactive refs:', {
      tasks: !!tasks,
      projects: !!projects,
      tasksLength: tasks.value.length
    })

    console.groupEnd()
  }

  return { checkStoreUsage }
}
```

## Advanced Sync Debugging (Integrated from dev-fix-task-sync)

### 🎯 Synchronization Failure Detection

You're experiencing the classic Pinia-IndexedDB synchronization failure when:
- **UI shows**: Current tasks (e.g., 4 tasks)
- **Pinia store has**: Empty or stale data (e.g., 0 tasks)
- **IndexedDB has**: Old data (e.g., 22 tasks)
- **Backup system reads**: From IndexedDB (getting wrong data)

The backup system works correctly but reads from wrong data source because Pinia isn't syncing with IndexedDB.

### Sync Diagnostic Protocol
```javascript
// Check data consistency across all layers
async function diagnosePiniaIndexedDBSync() {
  console.group('🔍 Pinia-IndexedDB Sync Diagnosis')

  // 1. Check Pinia store state
  const taskStore = useTaskStore()
  console.log('📊 Pinia Store:')
  console.log('  Tasks count:', taskStore.tasks.length)
  console.log('  Tasks:', taskStore.tasks.map(t => ({ id: t.id, title: t.title })))

  // 2. Check IndexedDB directly
  try {
    const db = await idb.openDB('flow-state-tasks', 1)
    const allTasks = await db.getAll('tasks')
    console.log('💾 IndexedDB:')
    console.log('  Tasks count:', allTasks.length)
    console.log('  Tasks:', allTasks.map(t => ({ id: t.id, title: t.title })))

    // 3. Compare data
    const piniaIds = new Set(taskStore.tasks.map(t => t.id))
    const idbIds = new Set(allTasks.map(t => t.id))

    console.log('🔄 Sync Analysis:')
    console.log('  Missing from Pinia:', Array.from(idbIds).filter(id => !piniaIds.has(id)))
    console.log('  Extra in Pinia:', Array.from(piniaIds).filter(id => !idbIds.has(id)))

    await db.close()
  } catch (error) {
    console.error('❌ IndexedDB access failed:', error)
  }

  console.groupEnd()
}
```

### Sync Resolution Strategies

#### Force Store Resync
```typescript
const forceStoreResync = async () => {
  const taskStore = useTaskStore()

  // Clear current store state
  taskStore.$reset()

  // Force reload from IndexedDB
  await taskStore.loadTasks()

  // Verify sync worked
  console.log('Resync complete. Tasks:', taskStore.tasks.length)
}
```

## Advanced State Management (Integrated from dev-pinia-state)

### Complex Store Architecture Analysis

#### Store Performance Optimization
```typescript
// Performance monitoring for stores
const createStoreMonitor = () => {
  const metrics = {
    mutations: 0,
    subscriptions: 0,
    lastMutation: null,
    slowMutations: []
  }

  return {
    trackMutation(action, duration) {
      metrics.mutations++
      metrics.lastMutation = { action, duration }

      if (duration > 100) {
        metrics.slowMutations.push({ action, duration, timestamp: Date.now() })
      }
    },

    getMetrics() {
      return { ...metrics }
    }
  }
}
```

#### Advanced Persistence Patterns
```typescript
// Conflict resolution for persistence
const createPersistenceLayer = () => {
  return {
    async saveWithConflictResolution(key, data) {
      try {
        const existing = await localStorage.getItem(key)

        if (existing) {
          const existingData = JSON.parse(existing)

          // Merge strategies
          const merged = {
            ...existingData,
            ...data,
            lastModified: Date.now(),
            version: (existingData.version || 0) + 1
          }

          await localStorage.setItem(key, JSON.stringify(merged))
          return merged
        }

        // No conflict, just save
        await localStorage.setItem(key, JSON.stringify({
          ...data,
          lastModified: Date.now(),
          version: 1
        }))

      } catch (error) {
        console.error('Persistence conflict resolution failed:', error)
        throw error
      }
    }
  }
}
```

#### Memory Leak Prevention
```typescript
// Subscription cleanup utilities
const createSubscriptionManager = () => {
  const subscriptions = new Set()

  return {
    add(subscription) {
      subscriptions.add(subscription)
      return subscription
    },

    cleanup() {
      subscriptions.forEach(sub => {
        if (typeof sub === 'function') {
          sub()
        } else if (sub && typeof sub.unsubscribe === 'function') {
          sub.unsubscribe()
        }
      })
      subscriptions.clear()
    },

    count() {
      return subscriptions.size
    }
  }
}
```

---

This comprehensive skill activates when you mention task store issues, CRUD operations not working, data persistence problems, synchronization failures, or advanced Pinia state management challenges.

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
