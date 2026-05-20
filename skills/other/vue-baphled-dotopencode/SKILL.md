---
name: vue
description: Vue.js framework, components, state management, and routing patterns
category: UI Frameworks
---

# Skill: vue

## What I do

I help you build web applications using the Vue.js framework. I focus on component design, state management with Pinia, and routing with Vue Router. I ensure that you follow the latest best practices, including the use of the Composition API and `<script setup>` syntax.

## When to use me

- When you're creating a new Vue component or refactoring an existing one.
- When you're designing the state management for a complex application.
- When you're setting up navigation and guards with Vue Router.
- When you're choosing between different reactivity primitives like `ref()` and `reactive()`.

## Core principles

1. **Composition over inheritance**, use the Composition API to share logic across components rather than relying on mixins.
2. **Predictable state**, use Pinia for centralising application state and ensuring that changes are trackable and consistent.
3. **Reactive data flow**, understand how Vue's reactivity system works to avoid common pitfalls like lost reactivity.
4. **Single-file components**, keep your template, script, and styles together for better maintainability and developer experience.

## Patterns & examples

### Composition API with script setup
The preferred way to write Vue components.
```vue
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubleCount = computed(() => count.value * 2)

function increment() {
    count.value++
}
</script>

<template>
    <button @click="increment">Count is: {{ count }}</button>
</template>
```

### State management with Pinia
Define a store for shared application state.
```javascript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({ name: 'Alice', isLoggedIn: false }),
    actions: {
        login(name) {
            this.name = name
            this.isLoggedIn = true
        }
    }
})
```

### Component communication
Use props for data down and emits for events up.
- **Pattern**, Pass data to child components via props and notify parent components of changes via the `emit` function.

### Navigation guards in Vue Router
Protect routes based on authentication or other conditions.
```javascript
router.beforeEach((to, from) => {
    const auth = useAuthStore()
    if (to.meta.requiresAuth && !auth.isLoggedIn) {
        return { name: 'login' }
    }
})
```

## Anti-patterns to avoid

- ❌ **Options API in new projects**, continuing to use the Options API instead of the more flexible Composition API.
- ❌ **Mutating props directly**, trying to change a prop value within a child component instead of emitting an event.
- ❌ **Over-using reactive()**, using `reactive()` for simple values where `ref()` would be more appropriate and clearer.
- ❌ **Direct DOM manipulation**, using `document.querySelector` instead of Vue's template refs or data binding.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/UI-Frameworks/Vue.md`

## Related skills

- `javascript`, for core language expertise.
- `ui-design`, for designing web interfaces.
- `ux-design`, for creating intuitive user flows.
- `clean-code`, for maintaining a high-quality codebase.
