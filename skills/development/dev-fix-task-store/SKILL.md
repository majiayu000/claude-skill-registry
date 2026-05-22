---
name: Fix Task Store Issues
description: DEBUG task store synchronization, task creation/deletion bugs, and state persistence problems. Fix when tasks don't save, disappear unexpectedly, or don't update in UI. Use for Pinia task store, task CRUD operations, and data persistence.
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

This skill activates when you mention task store issues, CRUD operations not working, data persistence problems, or task synchronization bugs.