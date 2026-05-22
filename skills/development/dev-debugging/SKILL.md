---
name: dev-debugging
description: UNIFIED DEBUGGER - Use when tasks disappear, data is lost, things are broken, or bugs need fixing. Debug Vue.js reactivity, Pinia state, task store CRUD, keyboard shortcuts, canvas positions, drag-drop, cache, memory leaks, and performance. Invoke for "not working", "broken", "fix bug", "debug", "tasks missing", "shortcuts not working", "state not updating".
---

<!-- SKILL CHAINING: After completing debugging work, Claude MUST invoke related skills -->
## Automatic Skill Chaining

**IMPORTANT**: After completing debugging work, automatically invoke these skills:

1. **After fixing a bug** → Use `Skill(qa-testing)` to verify the fix with proper tests
2. **If canvas issues** → Use `Skill(vue-flow-debug)` for specialized Vue Flow debugging
3. **If timer issues** → Use `Skill(dev-fix-timer)` for Pomodoro-specific debugging
4. **If Supabase issues** → Use `Skill(supabase-debugger)` for database/auth debugging

**Example chaining**:
```
User: "Fix the bug where tasks disappear"
1. Claude uses dev-debugging skill (this skill)
2. After fix implemented → Claude invokes: Skill(qa-testing)
3. QA skill runs verification tests
4. Only then claim the fix is complete
```

## When to Defer to Specialized Skills

**IMPORTANT**: This skill handles general debugging. For domain-specific issues, use specialized skills instead:

| Issue Type | Use This Skill Instead |
|------------|------------------------|
| Timer/Pomodoro bugs | `Skill(dev-fix-timer)` |
| Canvas/Vue Flow issues | `Skill(vue-flow-debug)` |
| Supabase/Auth problems | `Skill(supabase-debugger)` |
| Calendar interface bugs | `Skill(calendar-interface-architect)` |
| Port/server conflicts | `Skill(ops-port-manager)` |

**When to use THIS skill (dev-debugging)**:
- General Vue.js reactivity issues
- Pinia state management bugs
- Task store CRUD problems
- Keyboard shortcut failures
- Memory leaks and performance issues
- Cross-cutting bugs that span multiple systems

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

## Canvas Debugging (Integrated from dev-debug-canvas)

### 🚨 CRITICAL Canvas Testing Requirements

#### **ZERO TOLERANCE POLICY**
**NEVER claim canvas fixes work without comprehensive visual testing. Canvas issues are often visual and require actual interaction testing.**

#### **Before Claiming Success - MANDATORY Steps:**
1. **Start Development Server**: `npm run dev` (ensure port 5546 is available)
2. **Reactivate Playwright**: Use Playwright MCP for canvas interaction testing
3. **Open Browser DevTools**: Use Elements and Console panels for debugging
4. **Test Mouse Events**: Verify click, drag, hover interactions work
5. **Test Node Selection**: Verify single and multi-selection work
6. **Test Drag/Drop**: Verify nodes can be dragged and dropped correctly
7. **Test Viewport**: Verify zoom, pan, and viewport transformations work
8. **Test Edge Cases**: Verify boundary conditions and error scenarios

### Canvas Debugging Protocol

#### Common Canvas Issues
- **Mouse Event Failures**: Click, drag, hover events not firing
- **Node Selection Problems**: Single/multi-selection not working
- **Viewport Transform Issues**: Zoom, pan, or coordinate transformations broken
- **Drag/Drop Failures**: Nodes won't move or drop correctly
- **Coordinate System Problems**: Mouse positions don't match node positions

#### Canvas Debugging Tools
```typescript
// Canvas coordinate debugging
const debugCanvasCoords = (canvas, event) => {
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top

  console.log('Canvas Debug:')
  console.log('Event client:', event.clientX, event.clientY)
  console.log('Canvas rect:', rect.left, rect.top, rect.width, rect.height)
  console.log('Canvas coords:', x, y)
  console.log('Transformed coords:', canvas.transformPoint(x, y))

  return { x, y }
}

// Mouse event debugging
const debugMouseEvents = (element) => {
  const events = ['mousedown', 'mousemove', 'mouseup', 'click']

  events.forEach(eventType => {
    element.addEventListener(eventType, (e) => {
      console.log(`🖱️ ${eventType}:`, {
        target: e.target,
        button: e.button,
        buttons: e.buttons,
        clientX: e.clientX,
        clientY: e.clientY,
        ctrlKey: e.ctrlKey,
        shiftKey: e.shiftKey
      })
    })
  })
}

// Viewport debugging
const debugViewport = (viewport) => {
  console.log('Viewport Debug:')
  console.log('Zoom:', viewport.zoom)
  console.log('Pan:', viewport.x, viewport.y)
  console.log('Bounds:', viewport.getBounds())
  console.log('Transform matrix:', viewport.getTransform())
}
```

### Task Store Debugging

#### Task CRUD Issues
```typescript
// Debug task store operations
const debugTaskStore = () => {
  const taskStore = useTaskStore()

  // Watch for mutations
  taskStore.$subscribe((mutation, state) => {
    console.group('🔄 Task store mutation')
    console.log('Type:', mutation.type)
    console.log('Tasks count:', state.tasks.length)
    console.groupEnd()
  })

  // Check for duplicate IDs
  const checkDuplicates = () => {
    const ids = taskStore.tasks.map(t => t.id)
    const duplicates = ids.filter((id, i) => ids.indexOf(id) !== i)
    if (duplicates.length) console.error('🚨 Duplicate IDs:', duplicates)
  }

  return { checkDuplicates }
}
```

#### Pinia-Supabase Sync Issues
```typescript
// Diagnose sync problems
const diagnosePiniaSync = async () => {
  const taskStore = useTaskStore()
  console.log('📊 Pinia tasks:', taskStore.tasks.length)

  // Compare with Supabase
  const { data } = await supabase.from('tasks').select('id')
  console.log('💾 Supabase tasks:', data?.length || 0)

  // Find discrepancies
  const piniaIds = new Set(taskStore.tasks.map(t => t.id))
  const dbIds = new Set(data?.map(t => t.id) || [])
  console.log('Missing from Pinia:', [...dbIds].filter(id => !piniaIds.has(id)))
}
```

### Keyboard Shortcut Debugging

#### Event Handler Debug
```typescript
// Debug keyboard events
const debugKeyboard = () => {
  document.addEventListener('keydown', (e) => {
    console.log('⌨️ Key:', {
      key: e.key, code: e.code,
      ctrl: e.ctrlKey, shift: e.shiftKey,
      target: e.target.tagName
    })

    // Check if input has focus (shortcuts may be disabled)
    const isInput = ['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName)
    if (isInput) console.log('📝 Input focused - shortcuts disabled')
  }, true)
}

// Test VueUse magic keys
import { useMagicKeys } from '@vueuse/core'
const keys = useMagicKeys()
watch(keys.ctrl_z, (v) => v && console.log('Ctrl+Z pressed'))
```

#### Event Conflict Detection
```typescript
// Find multiple handlers for same key
const detectConflicts = () => {
  const handlers = []
  const originalAdd = EventTarget.prototype.addEventListener
  EventTarget.prototype.addEventListener = function(type, handler, opts) {
    if (type === 'keydown') handlers.push({ el: this, handler })
    return originalAdd.call(this, type, handler, opts)
  }
  console.log('Active keydown handlers:', handlers.length)
}
```

### Cache Debugging (Integrated from dev-debug-cache)

#### Vue 3 Cache Troubleshooting

**When to Activate:**
- Changes to Vue components are not appearing after refresh
- Hard refresh (Ctrl+R, Ctrl+Shift+R) does not work
- "Disable cache" in DevTools Network tab does not help
- HMR (Hot Module Replacement) appears broken
- The app seems to be serving old/stale code

#### Service Worker Debugging
```typescript
// Check for active service workers
const debugServiceWorkers = async () => {
  if ('serviceWorker' in navigator) {
    const registrations = await navigator.serviceWorker.getRegistrations()

    console.log('Service Workers:', registrations)

    registrations.forEach(registration => {
      console.log('Scope:', registration.scope)
      console.log('Active:', registration.active)
      console.log('Installing:', registration.installing)
      console.log('Waiting:', registration.waiting)
    })

    return registrations
  }
}

// Clear service workers
const clearServiceWorkers = async () => {
  const registrations = await navigator.serviceWorker.getRegistrations()

  for (const registration of registrations) {
    await registration.unregister()
    console.log('Unregistered:', registration.scope)
  }
}
```

#### Vite Cache Issues
```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install

# Restart dev server
npm run dev
```

---

## Production & CDN Debugging

### When to Use This Section
- App works locally but fails in production
- Chromium browsers fail, Firefox works
- `curl` shows correct response but browser fails
- MIME type errors in browser console
- Stale assets after deployment

### Cloudflare Cache MIME Type Issue (CRITICAL)

**Symptom**: Chromium browsers show MIME type errors for CSS/JS, but `curl` returns correct content-type.

**Root Cause**: Cloudflare caches by URL only. Chromium's preload scanner sends `Accept: text/html`, and Cloudflare serves cached HTML instead of CSS/JS.

**Quick Diagnostic**:
```bash
# Check if Vary header is present (MUST include "Accept")
curl -sI "https://in-theflow.com/assets/index.css" | grep -iE "vary|content-type"

# Expected:
# content-type: text/css; charset=utf-8
# vary: Accept-Encoding, Accept
```

**Fix**:
```bash
# Add to Caddyfile on VPS:
@static path /assets/*
header @static Vary "Accept-Encoding, Accept"
```

**Full Documentation**: `docs/sop/SOP-032-cloudflare-cache-mime-prevention.md`

### Cloudflare Debug Commands

```bash
# Check cache status
curl -sI https://example.com/path | grep cf-cache-status
# HIT = edge cache, MISS = origin, DYNAMIC = not cached

# Check response headers
curl -sI https://example.com/assets/app.css | grep -iE "content-type|cache-control|vary"

# Bypass Cloudflare (test origin directly)
curl -sI --resolve "example.com:443:YOUR_VPS_IP" https://example.com/path
```

### VPS/Caddy Debug Commands

```bash
# Check Caddy status
ssh root@VPS "systemctl status caddy"

# View Caddy logs
ssh root@VPS "journalctl -u caddy -f"

# Validate Caddy config
ssh root@VPS "caddy validate --config /etc/caddy/Caddyfile"

# Reload Caddy
ssh root@VPS "systemctl reload caddy"
```

### Browser-Specific Issues

| Works | Fails | Likely Cause |
|-------|-------|--------------|
| Firefox | Chrome/Brave | Cloudflare cache + preload scanner |
| curl | All browsers | Service Worker cache |
| Incognito | Normal mode | Browser cache |
| VPN | Local | Regional CDN issue |

### Quick Fix Script

```bash
# Emergency fix for Cloudflare MIME issue
./scripts/fix-cloudflare-cache.sh

# Then purge Cloudflare cache:
# Dashboard → Caching → Purge Everything
```

**Full Reference**: `.claude/skills/🐛 dev-debugging/references/production-cdn-debugging.md`

---

This comprehensive debugging skill provides systematic approaches to identify and resolve complex state management, reactivity, performance, canvas interactions, cache issues, and production/CDN problems in Vue.js applications with Pinia stores.

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

---

## Tauri/Linux Desktop Icon Troubleshooting

### When Icons Don't Update After Build

If you rebuild a Tauri app with new icons but the old icons still appear in the taskbar/window title bar, follow this troubleshooting guide.

#### Common Causes
1. **Conflicting .desktop files** - User-local file takes precedence over system file
2. **KDE icon cache** - Cached icons not refreshed
3. **StartupWMClass mismatch** - Desktop file doesn't match app's WM_CLASS
4. **Old binary still running** - System using old installed version

#### Diagnostic Commands
```bash
# 1. Find all .desktop files for your app
find /usr/share/applications ~/.local/share/applications -iname "*flowstate*" -o -iname "*flow-state*" 2>/dev/null

# 2. Check WM_CLASS of running app (click on app window when prompted)
xprop WM_CLASS

# 3. View .desktop file contents
cat /usr/share/applications/FlowState.desktop
cat ~/.local/share/applications/flowstate.desktop

# 4. Check installed icon locations
ls -la /usr/share/icons/hicolor/*/apps/flow-state.png
```

#### Fix Procedure (KDE Plasma)
```bash
# Step 1: Remove conflicting user .desktop file
rm -f ~/.local/share/applications/flowstate.desktop

# Step 2: Clear ALL icon caches
rm -f ~/.cache/icon-cache.kcache
rm -f ~/.cache/ksvg-elements-*
rm -rf ~/.cache/ksycoca6*

# Step 3: Update desktop database
update-desktop-database ~/.local/share/applications 2>/dev/null

# Step 4: Rebuild KDE system configuration
kbuildsycoca6 --noincremental  # For Plasma 6
# OR
kbuildsycoca5 --noincremental  # For Plasma 5

# Step 5: Kill the app
pkill -f "flow-state"

# Step 6: Restart plasmashell
kquitapp6 plasmashell && kstart plasmashell

# Step 7: Relaunch app
/usr/bin/flow-state &
```

#### If Icons Still Don't Update
1. **Reinstall the .deb package**:
   ```bash
   sudo dpkg -i src-tauri/target/release/bundle/deb/FlowState_*.deb
   ```

2. **Manually copy icons** (requires sudo):
   ```bash
   sudo cp src-tauri/icons/32x32.png /usr/share/icons/hicolor/32x32/apps/flow-state.png
   sudo cp src-tauri/icons/128x128.png /usr/share/icons/hicolor/128x128/apps/flow-state.png
   sudo cp src-tauri/icons/128x128@2x.png /usr/share/icons/hicolor/256x256@2/apps/flow-state.png
   sudo gtk-update-icon-cache -f /usr/share/icons/hicolor/
   ```

3. **Log out and log back in** - Some icon changes only take effect after re-login

#### Key Files Reference
| File | Purpose |
|------|---------|
| `src-tauri/icons/` | Source icons for Tauri build |
| `src-tauri/tauri.conf.json` | Icon configuration (`bundle.icon` array) |
| `/usr/share/applications/FlowState.desktop` | System .desktop file |
| `~/.local/share/applications/` | User .desktop files (take precedence!) |
| `/usr/share/icons/hicolor/*/apps/` | Installed icon locations |
| `~/.cache/icon-cache.kcache` | KDE icon cache |

#### Desktop File Best Practices
```ini
[Desktop Entry]
Name=FlowState
Comment=Productivity app
Exec=flow-state
Icon=flow-state
Terminal=false
Type=Application
Categories=Office;Productivity;
StartupWMClass=flow-state  # MUST match app's WM_CLASS exactly!
```

**Note**: The `StartupWMClass` must match the WM_CLASS reported by `xprop WM_CLASS` when clicking on the app window.

### Creating Transparent Taskbar Icons from Complex SVGs

Professional taskbar icons (like Spotify, Chrome, Telegram) have **transparent backgrounds** - just the icon shape floating, no visible background square. Here's how to convert complex SVGs to proper transparent icons.

#### Why Icons Look Wrong
| Problem | Cause |
|---------|-------|
| Visible dark/black square behind icon | SVG has background rectangle or fill |
| Icon doesn't match other taskbar icons | Background not truly transparent |
| Icon looks muddy/dark | Opaque background blending with panel |

#### The Solution: Flood-Fill Transparency

Use ImageMagick to flood-fill from corners, which removes connected background pixels:

```bash
# Step 1: Render SVG and make background transparent via flood-fill from all 4 corners
magick convert "original.svg" \
  -fuzz 25% -fill none -draw "color 0,0 floodfill" \
  -fuzz 25% -fill none -draw "color WIDTH-1,0 floodfill" \
  -fuzz 25% -fill none -draw "color 0,HEIGHT-1 floodfill" \
  -fuzz 25% -fill none -draw "color WIDTH-1,HEIGHT-1 floodfill" \
  /tmp/transparent.png

# Step 2: Trim transparent areas and resize to 512x512
magick convert /tmp/transparent.png \
  -trim +repage \
  -resize 490x490 \
  -gravity center \
  -background none \
  -extent 512x512 \
  src-tauri/icons/icon.png

# Step 3: Verify corners are transparent (should output 0)
magick convert src-tauri/icons/icon.png -crop 10x10+0+0 +repage -alpha extract -format "%[fx:mean]" info:
```

**Key Parameters:**
- `-fuzz 25%` - Tolerance for color matching (increase if background not fully removed)
- `floodfill` - Removes connected pixels of similar color starting from specified point
- `-trim +repage` - Remove transparent borders, reset canvas
- `-background none` - Ensure transparent background when extending

#### Generate Full Icon Set

```bash
# Generate all required sizes
for size in 16 24 32 48 64 128 256; do
  magick convert src-tauri/icons/icon.png -resize ${size}x${size} /tmp/ico/${size}.png
done

# Windows ICO (multi-size)
magick convert /tmp/ico/16.png /tmp/ico/24.png /tmp/ico/32.png /tmp/ico/48.png \
  /tmp/ico/64.png /tmp/ico/128.png /tmp/ico/256.png src-tauri/icons/icon.ico

# macOS ICNS (requires icnsutil: pip install icnsutil)
python3 -c "
import icnsutil
img = icnsutil.IcnsFile()
for size in [16, 32, 128, 256, 512]:
    img.add_media(file=f'/tmp/icns/icon_{size}x{size}.png')
img.write('src-tauri/icons/icon.icns')
"

# Tauri-specific sizes
magick convert src-tauri/icons/icon.png -resize 32x32 src-tauri/icons/32x32.png
magick convert src-tauri/icons/icon.png -resize 128x128 src-tauri/icons/128x128.png
magick convert src-tauri/icons/icon.png -resize 256x256 "src-tauri/icons/128x128@2x.png"
```

#### Full Workflow: SVG → Tauri App → KDE Taskbar

```bash
# 1. Create transparent icon from SVG
SVG_FILE="/path/to/original.svg"
# Get SVG dimensions first
identify "$SVG_FILE"  # Note WIDTH and HEIGHT

magick convert "$SVG_FILE" \
  -fuzz 25% -fill none -draw "color 0,0 floodfill" \
  -fuzz 25% -fill none -draw "color WIDTH-1,0 floodfill" \
  -fuzz 25% -fill none -draw "color 0,HEIGHT-1 floodfill" \
  -fuzz 25% -fill none -draw "color WIDTH-1,HEIGHT-1 floodfill" \
  -trim +repage \
  -resize 490x490 \
  -gravity center \
  -background none \
  -extent 512x512 \
  src-tauri/icons/icon.png

# 2. Generate all icon sizes (run the generate script above)

# 3. Rebuild Tauri app
npm run tauri build

# 4. Reinstall deb to update system icons
sudo dpkg -i src-tauri/target/release/bundle/deb/FlowState_*.deb

# 5. Refresh KDE caches
kbuildsycoca6 --noincremental

# 6. Restart plasmashell (REQUIRED for icon to appear)
kquitapp6 plasmashell && kstart plasmashell
```

#### Adjusting Icon Size Within Frame

To make the icon larger/smaller within the 512x512 frame:

```bash
# Larger icon (less padding) - use 500x500 or 510x510
magick convert /tmp/transparent.png -trim +repage \
  -resize 510x510 -gravity center -background none -extent 512x512 \
  src-tauri/icons/icon.png

# Smaller icon (more padding) - use 450x450 or 400x400
magick convert /tmp/transparent.png -trim +repage \
  -resize 450x450 -gravity center -background none -extent 512x512 \
  src-tauri/icons/icon.png
```

#### Troubleshooting Transparency

```bash
# Check alpha range (should be 0-1, not 1-1)
magick convert icon.png -alpha extract -format "Alpha: %[fx:minima]-%[fx:maxima]" info:

# Check specific corner (should be 0 for transparent)
magick convert icon.png -crop 10x10+0+0 +repage -alpha extract -format "%[fx:mean]" info:

# If alpha is 1-1 (fully opaque), try increasing fuzz:
magick convert original.svg -fuzz 35% -fill none -draw "color 0,0 floodfill" ...
```
