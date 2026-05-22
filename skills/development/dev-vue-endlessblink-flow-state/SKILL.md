---
name: Create Vue Components
description: CREATE Vue 3 components with Composition API and TypeScript. Build reactive components, handle props/events, implement lifecycle hooks, and integrate with Vue Router. Use when building new UI components or fixing component bugs.
---

# Vue.js Development

## Instructions

### Component Creation Pattern
Always use this structure for Vue 3 components in this project:

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/tasks'

// Props interface
interface Props {
  taskId?: string
  readonly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
})

const emit = defineEmits<{
  update: [task: Task]
  delete: [id: string]
}>()

// Store integration
const taskStore = useTaskStore()

// Computed properties
const filteredTasks = computed(() =>
  taskStore.tasks.filter(task => task.status === 'active')
)

// Methods
const handleUpdate = (task: Task) => {
  emit('update', task)
}

// Lifecycle
onMounted(() => {
  taskStore.loadTasks()
})
</script>

<template>
  <div class="component-container">
    <!-- Component content -->
  </div>
</template>

<style scoped>
.component-container {
  background: var(--color-surface);
  padding: var(--spacing-md);
}
</style>
```

### Key Requirements
- Always use `<script setup lang="ts">`
- Use design tokens: `var(--color-*)`, `var(--spacing-*)`
- Include proper TypeScript interfaces
- Use Pinia stores for state management
- Follow import organization: Vue → Stores → Components → Composables

### Common Patterns
- Event handling with proper modifiers
- Reactive data with `ref()` and `reactive()`
- Lazy loading for async components
- Proper cleanup in `onUnmounted()`

This skill ensures consistent Vue 3 development patterns across the productivity application.