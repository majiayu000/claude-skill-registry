---
name: Debug Vue Reactivity
description: DEBUG when Vue components won't update, computed properties are stale, or watchers not firing. Fix reactivity issues with ref(), reactive(), Pinia stores, and component state. Use when UI is not updating despite state changes.
keywords: vue, reactivity, ref, reactive, computed, watch, components
category: debug
triggers: components won't update, reactivity issues, computed not working, watcher not firing
---

🔧 **SKILL ACTIVATED: Debug Vue Reactivity**

*This skill was activated because you mentioned reactivity issues, components not updating, or Vue state problems.*

## Instructions

### Reactivity Debugging Protocol
When Vue components don't update or state seems broken, follow this systematic approach:

#### 1. Check Reactive References
- **Always use `.value`** for `ref()` in setup()
- **Never destructure reactive objects** (breaks reactivity)
- **Use `storeToRefs()`** for Pinia store destructuring
- **Use `reactive()`** for objects, not `ref()`

#### 2. Computed Properties
- **Check dependencies** - computed should only track what it uses
- **Debug stale computed** - add console.log to see when it recalculates
- **Use `watchEffect()`** for automatic dependency tracking

#### 3. Watcher Configuration
- **Use `{ deep: true }`** for nested object changes
- **Use `{ immediate: true }`** to run watcher immediately
- **Check `flush: 'post'`** for timing issues

## Quick Debug Patterns

### Reactivity Checker
```typescript
const debugReactivity = (ref, name) => {
  console.log(`${name} initial:`, ref.value)

  const stopWatcher = watch(ref, (newVal, oldVal) => {
    console.log(`${name} changed:`, oldVal, '→', newVal)
  }, { immediate: true })

  return stopWatcher
}
```

### Component Update Tracker
```typescript
export default {
  setup() {
    onRenderTracked((e) => {
      console.log('Render tracked:', e.key, e.type)
    })

    onRenderTriggered((e) => {
      console.log('Render triggered:', e.key, e.type)
    })
  }
}
```

## 🎯 Activation Triggers
This skill activates when you mention:
- "components won't update"
- "reactivity issues"
- "computed not working"
- "watcher not firing"
- "UI not updating"
- "state seems broken"
- "Vue reactivity problems"

## 🔗 Related Skills
- **Fix Pinia State**: If this is a store synchronization issue
- **Optimize Performance**: If this is a performance-related reactivity problem

## 📊 Usage Context
<!-- SKILL: dev-debug-reactivity -->
*Skill usage will be tracked for analytics and improvement purposes*

This skill provides systematic debugging approaches for Vue.js reactivity issues in the PomoFlow application.