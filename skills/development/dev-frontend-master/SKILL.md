---
name: Frontend Master
description: Master skill for all Frontend Vue 3 development. Covers Components, Pinia, VueUse, Reactivity, CSS, and UI/UX.
triggers:
  - create vue component
  - fix ui issue
  - pinia state management
  - vueuse implementation
  - reactivity debugging
---

# Frontend Master Skill

## 🎯 **Capabilities**
- **Vue 3 Components**: Creation and refactoring (`<script setup>`, TypeScript)
- **State Management**: Pinia stores, actions, and persistence
- **Reactivity**: Debugging `ref`, `reactive`, `computed`, `watch`
- **UI/UX**: Tailwind CSS, Design Tokens, Animations
- **VueUse**: Implementation of browser APIs and utilities

## 🛠️ **Best Practices**

### Component Structure
```vue
<script setup lang="ts">
import { computed } from 'vue'
// Imports...
// Props/Emits...
// Composables...
// Computed...
// Methods...
</script>

<template>
  <!-- Semantic HTML -->
</template>
```

### Pinia Patterns
- Use Setup Stores (`export const useStore = defineStore(...)`)
- Always type state interfaces
- Use `storeToRefs` for destructuring reactive state

### Debugging Reactivity
- Check for lost reactivity on destructuring (use `toRefs`)
- Verify `computed` dependencies
- Ensure deeply nested objects are reactive

## 🧹 **Action Protocol**
1. **Analyze**: Understand the UI/UX requirement or bug.
2. **Plan**: Identify which components/stores are affected.
3. **Implement**: Write clean, typed Vue 3 code.
4. **Verify**: Check for reactivity leaks and console errors.
