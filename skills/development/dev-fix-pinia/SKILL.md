---
name: Fix Pinia State Bugs
description: DEBUG Pinia store state not updating, persistence conflicts, and store synchronization issues. Fix when store actions don't work, state gets stale, or localStorage hydration problems occur. Use when Pinia stores behave unexpectedly.
keywords: pinia, store, state, persistence, actions, subscriptions
category: fix
triggers: store not updating, pinia state issues, state not syncing, store actions not working
---

⚡ **SKILL ACTIVATED: Fix Pinia State Bugs**

*This skill was activated because you mentioned Pinia store issues, state synchronization problems, or persistence conflicts.*

## Instructions

### Pinia Debugging Protocol
When Pinia stores aren't working correctly, systematically check:

#### 1. Store Instance Issues
- **Verify store instance is shared** across components
- **Check for multiple store instances** being created
- **Ensure actions are called on correct store instance**
- **Verify store initialization timing**

#### 2. State Mutation Problems
- **Use `$patch()`** for multiple state updates
- **Never assign directly to `$state`** (breaks reactivity)
- **Check for persistence plugin conflicts**
- **Verify SSR hydration doesn't overwrite client state**

#### 3. Subscription Management
- **Cleanup subscriptions** on component unmount
- **Use `{ detached: false }`** for auto-cleanup
- **Debug `$subscribe()` callbacks** not firing
- **Check for memory leaks in store watchers**

## Common Issues & Solutions

### State Not Updating
```typescript
// ❌ BAD: Direct assignment breaks reactivity
store.$state = newState

// ✅ GOOD: Use patch for updates
store.$patch(newState)

// ✅ BETTER: Use action for complex updates
store.updateMultipleItems(updates)
```

### Store Subscription Debugging
```typescript
const debugStore = (store, name) => {
  console.log(`🏪 ${name} initial state:`, JSON.parse(JSON.stringify(store.$state)))

  const unsubscribe = store.$subscribe((mutation, state) => {
    console.group(`🔄 ${name} mutation`)
    console.log('Type:', mutation.type)
    console.log('Payload:', mutation.payload)
    console.log('State:', JSON.parse(JSON.stringify(state)))
    console.groupEnd()
  })

  return unsubscribe
}
```

### Persistence Conflicts
```typescript
// Debug localStorage hydration conflicts
const debugStorage = (store, storageKey) => {
  const stored = localStorage.getItem(storageKey)
  const current = JSON.stringify(store.$state)

  if (stored !== current) {
    console.warn('Storage conflict detected:', {
      stored: JSON.parse(stored || '{}'),
      current: store.$state
    })
  }
}
```

## 🎯 Activation Triggers
This skill activates when you mention:
- "store not updating"
- "pinia state issues"
- "state not syncing"
- "store actions not working"
- "persistence problems"
- "localStorage hydration"
- "store synchronization bugs"

## 🔗 Related Skills
- **Debug Vue Reactivity**: If this is a component reactivity issue
- **Fix Task Store**: If this is specifically about task store problems

## 📊 Usage Context
<!-- SKILL: fix-pinia-state -->
*Skill usage will be tracked for analytics and improvement purposes*

This skill provides comprehensive solutions for Pinia store debugging and state management issues in PomoFlow.