---
name: Optimize Performance
description: OPTIMIZE slow Vue applications, fix memory leaks, and improve render performance. Reduce unnecessary re-renders, optimize computed properties, and fix expensive operations. Use when application feels slow, memory usage grows, or animations lag.
---

# Optimize Performance

## Instructions

### Performance Optimization Protocol
When Vue applications are slow or memory usage is high, systematically optimize:

#### 1. Render Performance Issues
- **Identify expensive components** using Vue DevTools performance tab
- **Add `v-memo`** for heavy components that don't need frequent updates
- **Use `shallowRef`** for large arrays/objects that don't need deep reactivity
- **Optimize computed properties** to avoid unnecessary recalculations

#### 2. Memory Leak Detection
- **Check for unmanaged event listeners** in onUnmounted()
- **Cleanup store subscriptions** and async operations
- **Debug timer/interval cleanup**
- **Monitor component reference cycles**

#### 3. Bundle Size Optimization
- **Lazy load components** and routes
- **Tree shake unused imports**
- **Optimize asset loading** with code splitting

## Quick Performance Fixes

### Component Memoization
```vue
<template>
  <!-- Memoize expensive components -->
  <ExpensiveComponent
    v-for="item in items"
    :key="item.id"
    v-memo="[item.id, item.lastModified]"
    :data="item"
  />
</template>

<script setup>
import { shallowRef } from 'vue'

// Use shallowRef for large data structures
const items = shallowRef([])
</script>
```

### Computed Property Optimization
```typescript
// ❌ BAD: Expensive recalculation
const expensiveComputed = computed(() => {
  return heavyCalculation(props.data)
})

// ✅ GOOD: Memoize with caching
const expensiveComputed = computed(() => {
  if (!dataCache.has(props.data.id)) {
    dataCache.set(props.data.id, heavyCalculation(props.data))
  }
  return dataCache.get(props.data.id)
})
```

### Memory Leak Detection
```typescript
const memoryTracker = {
  components: new Set(),
  subscriptions: new Set(),

  track(component, name) {
    this.components.add({ component, name, createdAt: Date.now() })

    onUnmounted(() => {
      this.components.delete(component)
      console.log(`✅ Component cleaned up: ${name}`)
    })
  },

  checkLeaks() {
    const now = Date.now()
    const leaked = Array.from(this.components).filter(c =>
      now - c.createdAt > 30000 // Older than 30 seconds
    )

    if (leaked.length > 0) {
      console.warn('🚨 Potential memory leaks:', leaked)
    }
  }
}
```

This skill activates when you mention performance issues, slow applications, memory leaks, or optimization needs.