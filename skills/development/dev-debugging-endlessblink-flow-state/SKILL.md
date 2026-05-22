---
name: Comprehensive Debugging
description: Master debugging techniques for Vue.js, Pinia, and cached state issues. Identify reactivity problems, memory leaks, performance bottlenecks, and complex state synchronization issues with systematic troubleshooting approaches.
---

# Comprehensive Debugging

## Instructions

### Debugging Philosophy
Always follow systematic debugging methodology:

1. **Identify the Problem**: Gather specific symptoms and error messages
2. **Isolate the Issue**: Use binary search to narrow down the root cause
3. **Verify the Fix**: Ensure the solution works and doesn't introduce regressions
4. **Document the Solution**: Create reusable debugging patterns

### Vue.js Reactivity Debugging

#### Common Reactivity Issues
- **Direct Property Assignment**: Adding properties to reactive objects without `Vue.set()` or `reactive()`
- **Array Mutation**: Direct index assignment or length modification without proper methods
- **Computed Caching**: Computed properties not updating due to stale dependencies
- **Watch Invalidation**: Watchers not firing due to incorrect configuration

#### Debugging Tools
```typescript
import { watch, watchEffect, computed, ref, reactive } from 'vue'

// Debug reactivity dependencies
const debugReactivity = () => {
  const state = reactive({ count: 0, nested: { value: 0 } })

  // Track what triggers reactivity
  watchEffect(() => {
    console.log('Effect triggered with:', state.count, state.nested.value)
  })

  // Debug computed dependencies
  const doubled = computed(() => {
    console.log('Computed recalculating with:', state.count)
    return state.count * 2
  })

  return { state, doubled }
}

// Component-level debugging hooks
export default {
  setup() {
    // Debug what triggers re-renders
    onRenderTracked((e) => {
      console.log('Render tracked:', e.key, e.type, e.target)
    })

    onRenderTriggered((e) => {
      console.log('Render triggered:', e.key, e.type, e.target)
    })
  }
}
```

### Pinia State Debugging

#### Store State Issues
- **Stale State**: State not updating due to missing reactivity
- **Persistence Conflicts**: LocalStorage hydration overriding current state
- **Action Side Effects**: Actions causing unexpected state mutations
- **Subscription Leaks**: Unmanaged store subscriptions

#### Debugging Patterns
```typescript
import { defineStore } from 'pinia'

export const useDebugStore = defineStore('debug', {
  state: () => ({
    tasks: [],
    selectedTaskId: null,
    lastMutation: null,
    debugMode: true
  }),

  actions: {
    // Add mutation tracking
    addTask(task) {
      if (this.debugMode) {
        console.trace('addTask called with:', task)
        console.log('State before:', JSON.parse(JSON.stringify(this.tasks)))
      }

      this.tasks.push(task)
      this.lastMutation = {
        type: 'addTask',
        timestamp: Date.now(),
        payload: task
      }

      if (this.debugMode) {
        console.log('State after:', JSON.parse(JSON.stringify(this.tasks)))
      }
    },

    // Batch mutations for atomic updates
    updateTasks(updates) {
      this.$patch((state) => {
        updates.forEach(({ id, ...changes }) => {
          const task = state.tasks.find(t => t.id === id)
          if (task) {
            Object.assign(task, changes)
            if (this.debugMode) {
              console.log(`Task ${id} updated:`, changes)
            }
          }
        })
      })
    }
  },

  // Debug getters with caching issues
  getters: {
    completedTasks: (state) => {
      console.log('completedTasks getter recalculating')
      return state.tasks.filter(task => task.completed)
    },

    taskById: (state) => {
      console.log('taskById getter recalculating')
      return (id) => state.tasks.find(task => task.id === id)
    }
  }
})
```

### Cached State Issues

#### Browser Storage Debugging
```typescript
import { useLocalStorage, useSessionStorage } from '@vueuse/core'

const debugStorage = () => {
  const settings = useLocalStorage('app-settings', {
    theme: 'light',
    language: 'en'
  })

  // Monitor storage changes
  window.addEventListener('storage', (e) => {
    console.log('Storage changed:', e.key, e.oldValue, e.newValue)
  })

  // Debug hydration conflicts
  const checkStorageConsistency = () => {
    const raw = localStorage.getItem('app-settings')
    const parsed = JSON.parse(raw)
    console.log('Raw storage:', raw)
    console.log('Parsed storage:', parsed)
    console.log('Current reactive:', settings.value)

    if (JSON.stringify(settings.value) !== JSON.stringify(parsed)) {
      console.warn('Storage inconsistency detected!')
    }
  }

  return { settings, checkStorageConsistency }
}
```

#### Memory Leak Detection
```typescript
const detectMemoryLeaks = () => {
  const componentInstances = new WeakSet()
  const subscriptions = new Set()

  const trackComponent = (component) => {
    componentInstances.add(component)
    console.log('Component tracked:', component.$options.name)
  }

  const trackSubscription = (unsubscribe) => {
    subscriptions.add(unsubscribe)

    // Auto-cleanup after component unmounts
    onUnmounted(() => {
      if (subscriptions.has(unsubscribe)) {
        unsubscribe()
        subscriptions.delete(unsubscribe)
        console.log('Subscription cleaned up')
      }
    })
  }

  // Monitor for memory leaks
  setInterval(() => {
    console.log('Active subscriptions:', subscriptions.size)
    console.log('Tracked components:', componentInstances.size || 0)
  }, 10000)

  return { trackComponent, trackSubscription }
}
```

### Performance Debugging

#### Component Performance
```vue
<template>
  <div>
    <!-- Use v-memo for expensive rendering -->
    <ExpensiveComponent
      v-for="item in items"
      :key="item.id"
      v-memo="[item.id, item.lastModified]"
      :data="item"
    />
  </div>
</template>

<script setup>
import { ref, computed, shallowRef } from 'vue'

// Performance monitoring
const renderCount = ref(0)
const lastRenderTime = ref(Date.now())

// Use shallowRef for large arrays
const items = shallowRef([])

// Optimize computed properties
const expensiveComputed = computed(() => {
  renderCount.value++
  lastRenderTime.value = Date.now()

  console.log(`Computed recalculated (${renderCount.value} times)`)

  return items.value
    .filter(item => item.active)
    .map(item => processItem(item))
})

// Debug performance
onMounted(() => {
  const observer = new PerformanceObserver((list) => {
    list.getEntries().forEach((entry) => {
      if (entry.entryType === 'measure') {
        console.log(`Performance: ${entry.name} took ${entry.duration}ms`)
      }
    })
  })

  observer.observe({ entryTypes: ['measure'] })

  // Measure render performance
  performance.mark('render-start')
  nextTick(() => {
    performance.mark('render-end')
    performance.measure('render-time', 'render-start', 'render-end')
  })
})
</script>
```

### Canvas Debugging

#### Canvas State Issues
```typescript
const debugCanvas = () => {
  const canvasState = reactive({
    nodes: [],
    selectedNodes: [],
    viewport: { x: 0, y: 0, zoom: 1 },
    isDragging: false
  })

  // Debug canvas mutations
  const debugCanvasMutation = (action, data) => {
    console.group(`Canvas ${action}`)
    console.log('State before:', JSON.parse(JSON.stringify(canvasState)))
    console.log('Mutation data:', data)

    action(canvasState, data)

    console.log('State after:', JSON.parse(JSON.stringify(canvasState)))
    console.groupEnd()
  }

  // Debug selection issues
  const debugSelection = (nodeIds) => {
    console.log('Selecting nodes:', nodeIds)
    console.log('Current selection:', canvasState.selectedNodes)
    console.log('Available nodes:', canvasState.nodes.map(n => n.id))

    const invalidIds = nodeIds.filter(id =>
      !canvasState.nodes.some(n => n.id === id)
    )

    if (invalidIds.length > 0) {
      console.warn('Invalid node IDs in selection:', invalidIds)
    }
  }

  return { canvasState, debugCanvasMutation, debugSelection }
}
```

### Async Operation Debugging

#### Promise and Timer Debugging
```typescript
const debugAsync = () => {
  const activePromises = new Set()
  const activeTimers = new Set()

  const debugPromise = (promise, description) => {
    activePromises.add(promise)
    console.log(`Promise started: ${description}`)

    promise
      .then(result => {
        console.log(`Promise resolved: ${description}`, result)
        activePromises.delete(promise)
      })
      .catch(error => {
        console.error(`Promise rejected: ${description}`, error)
        activePromises.delete(promise)
      })

    return promise
  }

  const debugTimer = (callback, delay, description) => {
    const timerId = setTimeout(() => {
      console.log(`Timer fired: ${description}`)
      callback()
      activeTimers.delete(timerId)
    }, delay)

    activeTimers.add(timerId)
    console.log(`Timer set: ${description} (${delay}ms)`)

    return timerId
  }

  // Check for leaks
  setInterval(() => {
    console.log('Active promises:', activePromises.size)
    console.log('Active timers:', activeTimers.size)

    if (activePromises.size > 10) {
      console.warn('Possible promise leak detected!')
    }

    if (activeTimers.size > 5) {
      console.warn('Possible timer leak detected!')
    }
  }, 5000)

  return { debugPromise, debugTimer }
}
```

### Error Boundary Debugging

#### Global Error Handling
```typescript
const setupErrorHandling = () => {
  // Vue error handler
  app.config.errorHandler = (err, instance, info) => {
    console.group('Vue Error')
    console.error('Error:', err)
    console.error('Component:', instance?.$options.name)
    console.error('Info:', info)
    console.error('Props:', instance?.$props)
    console.error('State:', instance?.$data)
    console.groupEnd()

    // Send to error tracking service
    errorTracking.captureException(err, {
      tags: { component: instance?.$options.name },
      extra: { info, props: instance?.$props }
    })
  }

  // Unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)

    // Prevent default browser behavior
    event.preventDefault()
  })

  // Global error tracking
  window.addEventListener('error', (event) => {
    console.error('Global error:', event.error)
  })
}
```

### Network Debugging

#### API Request Debugging
```typescript
const debugNetwork = () => {
  const originalFetch = window.fetch

  window.fetch = async (...args) => {
    const [url, options = {}] = args
    const requestId = Math.random().toString(36).substr(2, 9)

    console.group(`🌐 Request ${requestId}: ${options.method || 'GET'} ${url}`)
    console.log('Request:', options)

    const startTime = performance.now()

    try {
      const response = await originalFetch(...args)
      const duration = performance.now() - startTime

      console.log(`✅ Response ${requestId}: ${response.status} (${duration.toFixed(2)}ms)`)
      console.log('Headers:', Object.fromEntries(response.headers.entries()))

      // Clone response to avoid consuming it
      const clonedResponse = response.clone()
      const data = await clonedResponse.json().catch(() => clonedResponse.text())
      console.log('Data:', data)

      console.groupEnd()
      return response
    } catch (error) {
      const duration = performance.now() - startTime
      console.error(`❌ Error ${requestId}: ${error.message} (${duration.toFixed(2)}ms)`)
      console.groupEnd()
      throw error
    }
  }
}
```

### Debugging Utilities

#### State Snapshot
```typescript
const createDebugger = () => {
  const snapshots = []
  const maxSnapshots = 10

  const takeSnapshot = (label, data) => {
    const snapshot = {
      label,
      timestamp: Date.now(),
      data: JSON.parse(JSON.stringify(data)),
      stackTrace: new Error().stack
    }

    snapshots.push(snapshot)

    if (snapshots.length > maxSnapshots) {
      snapshots.shift()
    }

    console.log(`📸 Snapshot: ${label}`, snapshot)
  }

  const compareSnapshots = (index1, index2) => {
    const snap1 = snapshots[index1]
    const snap2 = snapshots[index2]

    const diff = findDiff(snap1.data, snap2.data)
    console.log(`🔍 Comparing snapshots: ${snap1.label} vs ${snap2.label}`)
    console.log('Differences:', diff)
  }

  const findDiff = (obj1, obj2) => {
    // Simple diff implementation
    const diffs = []

    const keys = new Set([...Object.keys(obj1), ...Object.keys(obj2)])

    for (const key of keys) {
      if (JSON.stringify(obj1[key]) !== JSON.stringify(obj2[key])) {
        diffs.push({
          key,
          oldValue: obj1[key],
          newValue: obj2[key]
        })
      }
    }

    return diffs
  }

  return { takeSnapshot, compareSnapshots, snapshots }
}
```

### Usage Examples

#### Quick Debug Patterns
```typescript
// Quick reactivity check
const checkReactivity = (obj, property) => {
  const value = obj[property]
  obj[property] = value
  console.log('Reactivity check:', obj[property] === value)
}

// Performance measurement
const measurePerformance = (fn, label) => {
  const start = performance.now()
  const result = fn()
  const end = performance.now()
  console.log(`⏱️ ${label}: ${(end - start).toFixed(2)}ms`)
  return result
}

// Debug store mutations
const debugStoreMutations = (store) => {
  store.$subscribe((mutation, state) => {
    console.group(`🔄 Store Mutation: ${mutation.type}`)
    console.log('Payload:', mutation.payload)
    console.log('New state:', state)
    console.groupEnd()
  })
}
```

This comprehensive debugging skill provides systematic approaches to identify and resolve complex state management, reactivity, and performance issues in Vue.js applications with Pinia stores.