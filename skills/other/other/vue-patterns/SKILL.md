---
name: vue-patterns
description: Vue 3 patterns and best practices for this workout tracker: feature module architecture, createGlobalState() singleton state (not Pinia), defineModel two-way binding, and component gotchas. Use when creating/refactoring components, features, composables, managing shared state, or debugging reactivity issues. Triggers include "add component", "create feature", "refactor", "composable", "v-model", "defineModel", "global state", "createGlobalState", "singleton", "reactive", "two-way binding", "feature structure", "reka-ui", "shadcn-vue".
---

# Vue Patterns

## Feature Module Architecture

**Bulletproof architecture**: Self-contained domain modules. Each feature owns UI components, composables, and business logic.

| Feature | Purpose | Entry Point |
|---------|---------|-------------|
| `workout/` | Active workout state & execution | `composables/useWorkout.ts` |
| `exercises/` | Exercise library CRUD | `composables/useExerciseForm.ts` |
| `templates/` | Workout template management | `composables/useTemplateForm.ts` |
| `benchmarks/` | Benchmark workout tracking | `composables/useBenchmark.ts` |
| `settings/` | App settings & preferences | `composables/useLanguageSettings.ts` |
| `timers/` | Standalone timer UI | `components/TimerCard.vue` |
| `log-past-workout/` | Retroactive workout entry | `composables/usePastWorkout.ts` |

**Structure:**
```
src/features/[feature]/
├── components/      # Feature-specific Vue components
├── composables/     # Feature-specific composables
├── lib/             # Feature utilities
└── state/           # Singleton state (if needed)
```

## Singleton State Pattern

Use `createGlobalState()` from VueUse for shared state (NOT Pinia):

```ts
// src/stores/workoutState.ts
import { createGlobalState } from '@vueuse/core'

export const useWorkoutState = createGlobalState(() => {
  const workout = ref<Workout | null>(null)
  return { workout }
})

// Feature composable provides singleton ref
// src/features/workout/composables/useWorkout.ts
import { getWorkoutRef } from '@/stores/workoutState'

const workout = getWorkoutRef() // Shared singleton ref

export function useWorkout() {
  return {
    workout,           // Ref<Workout> - shared across all components
    selectBlock,
    // ...
  }
}
```

## Two-Way Binding

Always use `defineModel` for v-model:

```ts
// Props with v-model
const open = defineModel<boolean>('open')
const value = defineModel<string>() // default model
```

## Gotchas

### 1. Wrap Destructured Props in Getters for Watchers

```ts
// BAD - breaks reactivity
const { count } = defineProps<{ count: number }>()
watch(count, ...)

// GOOD - wrap in getter
watch(() => count, ...)
```

### 2. shadcn-vue Uses reka-ui (Not Radix)

```vue
<!-- BAD - v-model:checked doesn't exist -->
<Switch v-model:checked="enabled" />

<!-- GOOD - use v-model -->
<Switch v-model="enabled" />
```

Check [reka-ui docs](https://reka-ui.com) for correct API.

## Quick Find

```bash
rg -n "export function use" src/features/workout/composables  # Feature composables
find src/features/workout/components -name "*.vue"            # Feature components
rg -n "kind: '(strength|amrap|emom|tabata|fortime)'" src/     # Block types
```
