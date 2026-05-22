---
name: vue-patterns
description: Vue 3 Composition API and scoped style policies. Use when writing Vue components, composables, or using :deep() selector. Do NOT use for React/Next.js code -- use react-patterns instead.
durability: encoded-preference
---

# Vue 3 Patterns

## Component Policies

### Props - Use Type-Only Syntax

```vue
<script setup lang="ts">
const props = defineProps<{
  book: Book
  isActive?: boolean
}>()

// With defaults
const props = withDefaults(defineProps<Props>(), {
  msg: 'hello'
})
</script>
```

### Emits - Use Named Tuple Syntax (Vue 3.3+)

```vue
<script setup lang="ts">
const emit = defineEmits<{
  change: [id: number]
  update: [value: string]
}>()
</script>
```

### Two-Way Binding - Use defineModel

```vue
<script setup lang="ts">
const model = defineModel<string>()
const count = defineModel<number>('count', { default: 0 })
</script>
```

## State Management Policies

### Prefer ref over reactive

**Always use `ref` for single values.** Use `reactive` only for tightly-coupled object hierarchies where `.value` is unwieldy.

### Provide/Inject - Always Use InjectionKey

```typescript
export const UserKey: InjectionKey<UserContext> = Symbol('user')
provide(UserKey, context)
const ctx = inject(UserKey)
```

## Reactivity Policies

### watch vs watchEffect

| Use | When |
|-----|------|
| `watch` | Need old value, explicit sources |
| `watchEffect` | Auto-track dependencies, immediate run |

### Performance - Use shallowRef for Large Objects

```typescript
const largeList = shallowRef<Item[]>([])
// Replace entirely instead of mutation
largeList.value = [...largeList.value, newItem]
```

## Template Policies

### Never Mix v-if with v-for

```vue
<!-- BAD -->
<li v-for="item in items" v-if="item.isActive">

<!-- GOOD: Use computed -->
<li v-for="item in activeItems">
```

### Always Use :key with Unique ID

```vue
<li v-for="item in items" :key="item.id">
```

### Use v-show for Frequent Toggles

`v-show` keeps element in DOM, `v-if` removes it.

## Performance Policies

| Technique | When to Use |
|-----------|-------------|
| `defineAsyncComponent` | Heavy components, code splitting |
| `v-memo` | Expensive list items with stable deps |
| `v-once` | Static content that never changes |
| `shallowRef` | Large arrays/objects |

## Scoped Style Policies

### :deep() Selector - Use with Caution

| Use When | Avoid When |
|----------|------------|
| Styling third-party component internals | Styling your own child components |
| No other customization option available | Component exposes props/slots for customization |
| Scoped override needed without global CSS | You control both parent and child |

**Risks:**
- Breaks component encapsulation
- Fragile: child component refactoring breaks styles
- Hard to trace style origins in large codebases

```vue
<style scoped>
/* Target third-party component internals only */
:deep(.third-party-class) {
  color: var(--custom-color);
}
</style>
```

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| `reactive` for primitives | Use `ref` |
| Mutating props | Emit event to parent |
| v-if + v-for on same element | Use computed filter |
| Missing :key in v-for | Always provide unique key |
| inject without null check | Check `if (!ctx) throw` |
| `:deep()` for own child components | Use props, slots, or CSS variables |
| Nested `:deep()` selectors | Flatten or reconsider component structure |
