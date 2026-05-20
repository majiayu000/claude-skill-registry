---
name: vue-best-practices
description: Vue.js 3 best practices guidelines covering Composition API, component design, reactivity patterns, Tailwind CSS utility-first styling, PrimeVue component library integration, and code organization. This skill should be used when writing, reviewing, or refactoring Vue.js code to ensure idiomatic patterns and maintainable code.
license: MIT
---

# Vue.js Best Practices

Comprehensive best practices guide for Vue.js 3 applications. Contains guidelines across multiple categories to ensure idiomatic, maintainable, and scalable Vue.js code, including Tailwind CSS integration patterns for utility-first styling and PrimeVue component library best practices.

## When to Apply

Reference these guidelines when:
- Writing new Vue components or composables
- Implementing features with Composition API
- Reviewing code for Vue.js patterns compliance
- Refactoring existing Vue.js code
- Setting up component architecture
- Working with Nuxt.js applications
- Styling Vue components with Tailwind CSS utility classes
- Creating design systems with Tailwind and Vue
- Using PrimeVue component library
- Customizing PrimeVue components with PassThrough API

## Rule Categories

| Category | Focus | Prefix |
|----------|-------|--------|
| Composition API | Proper use of Composition API patterns | `composition-` |
| Component Design | Component structure and organization | `component-` |
| Reactivity | Reactive state management patterns | `reactive-` |
| Props & Events | Component communication patterns | `props-` |
| Template Patterns | Template syntax best practices | `template-` |
| Code Organization | Project and code structure | `organization-` |
| TypeScript | Type-safe Vue.js patterns | `typescript-` |
| Error Handling | Error boundaries and handling | `error-` |
| Tailwind CSS | Utility-first styling patterns | `tailwind-` |
| PrimeVue | Component library integration patterns | `primevue-` |

## Quick Reference

### 1. Composition API Best Practices

- `composition-script-setup` - Always use `<script setup>` for single-file components
- `composition-ref-vs-reactive` - Use `ref()` for primitives, `reactive()` for objects
- `composition-computed-derived` - Use `computed()` for all derived state
- `composition-watch-side-effects` - Use `watch()`/`watchEffect()` only for side effects
- `composition-composables` - Extract reusable logic into composables
- `composition-lifecycle-order` - Place lifecycle hooks after reactive state declarations
- `composition-avoid-this` - Never use `this` in Composition API

### 2. Component Design

- `component-single-responsibility` - One component, one purpose
- `component-naming-convention` - Use PascalCase for components, kebab-case in templates
- `component-small-focused` - Keep components under 200 lines
- `component-presentational-container` - Separate logic from presentation when beneficial
- `component-slots-flexibility` - Use slots for flexible component composition
- `component-expose-minimal` - Only expose what's necessary via `defineExpose()`

### 3. Reactivity Patterns

- `reactive-const-refs` - Always declare refs with `const`
- `reactive-unwrap-template` - Let Vue unwrap refs in templates (no `.value`)
- `reactive-shallow-large-data` - Use `shallowRef()`/`shallowReactive()` for large non-reactive data
- `reactive-readonly-props` - Use `readonly()` to prevent mutations
- `reactive-toRefs-destructure` - Use `toRefs()` when destructuring reactive objects
- `reactive-avoid-mutation` - Prefer immutable updates for complex state

### 4. Props & Events

- `props-define-types` - Always define prop types with `defineProps<T>()`
- `props-required-explicit` - Be explicit about required vs optional props
- `props-default-values` - Provide sensible defaults with `withDefaults()`
- `props-immutable` - Never mutate props directly
- `props-validation` - Use validator functions for complex prop validation
- `events-define-emits` - Always define emits with `defineEmits<T>()`
- `events-naming` - Use kebab-case for event names in templates
- `events-payload-objects` - Pass objects for events with multiple values

### 5. Template Patterns

- `template-v-if-v-show` - Use `v-if` for conditional rendering, `v-show` for toggling
- `template-v-for-key` - Always use unique, stable `:key` with `v-for`
- `template-v-if-v-for` - Never use `v-if` and `v-for` on the same element
- `template-computed-expressions` - Move complex expressions to computed properties
- `template-event-modifiers` - Use event modifiers (`.prevent`, `.stop`) appropriately
- `template-v-bind-shorthand` - Use shorthand syntax (`:` for `v-bind`, `@` for `v-on`)
- `template-v-model-modifiers` - Use v-model modifiers (`.trim`, `.number`, `.lazy`)

### 6. Code Organization

- `organization-feature-folders` - Organize by feature, not by type
- `organization-composables-folder` - Keep composables in dedicated `composables/` folder
- `organization-barrel-exports` - Use index files for clean imports
- `organization-consistent-naming` - Follow consistent naming conventions
- `organization-colocation` - Colocate related files (component, tests, styles)

### 7. TypeScript Integration

- `typescript-generic-components` - Use generics for reusable typed components
- `typescript-prop-types` - Use TypeScript interfaces for prop definitions
- `typescript-emit-types` - Type emit payloads explicitly
- `typescript-ref-typing` - Specify types for refs when not inferred
- `typescript-template-refs` - Type template refs with `ref<InstanceType<typeof Component> | null>(null)`

### 8. Error Handling

- `error-boundaries` - Use `onErrorCaptured()` for component error boundaries
- `error-async-handling` - Handle errors in async operations explicitly
- `error-provide-fallbacks` - Provide fallback UI for error states
- `error-logging` - Log errors appropriately for debugging

### 9. Tailwind CSS

- `tailwind-utility-first` - Apply utility classes directly in templates, avoid custom CSS
- `tailwind-class-order` - Use consistent class ordering (layout → spacing → typography → visual)
- `tailwind-responsive-mobile-first` - Use mobile-first responsive design (`sm:`, `md:`, `lg:`)
- `tailwind-component-extraction` - Extract repeated utility patterns into Vue components
- `tailwind-dynamic-classes` - Use computed properties or helper functions for dynamic classes
- `tailwind-complete-class-strings` - Always use complete class strings, never concatenate
- `tailwind-state-variants` - Use state variants (`hover:`, `focus:`, `active:`) for interactions
- `tailwind-dark-mode` - Use `dark:` prefix for dark mode support
- `tailwind-design-tokens` - Configure design tokens in Tailwind config for consistency
- `tailwind-avoid-apply-overuse` - Limit `@apply` usage; prefer Vue components for abstraction

### 10. PrimeVue

- `primevue-design-tokens` - Use design tokens over CSS overrides for theming
- `primevue-passthrough-api` - Use PassThrough (pt) API for component customization
- `primevue-wrapper-components` - Wrap PrimeVue components for consistent styling across apps
- `primevue-unstyled-mode` - Use unstyled mode with Tailwind for full styling control
- `primevue-global-pt-config` - Define shared PassThrough properties at app level
- `primevue-merge-strategies` - Choose appropriate merge strategies for PT customization
- `primevue-use-passthrough-utility` - Use `usePassThrough` for extending presets
- `primevue-typed-components` - Leverage PrimeVue's TypeScript support for type safety
- `primevue-accessibility` - Maintain WCAG compliance with proper aria attributes
- `primevue-lazy-loading` - Use async components for large PrimeVue imports

## Key Principles

### Composition API Best Practices

The Composition API is the recommended approach for Vue.js 3. Follow these patterns:

- **Always use `<script setup>`**: More concise, better TypeScript inference, and improved performance
- **Organize code by logical concern**: Group related state, computed properties, and functions together
- **Extract reusable logic to composables**: Follow the `use` prefix convention (e.g., `useAuth`, `useFetch`)
- **Keep setup code readable**: Order: props/emits, reactive state, computed, watchers, methods, lifecycle hooks

### Component Design Principles

Well-designed components are the foundation of maintainable Vue applications:

- **Single Responsibility**: Each component should do one thing well
- **Props Down, Events Up**: Follow unidirectional data flow
- **Prefer Composition over Inheritance**: Use composables and slots for code reuse
- **Keep Components Small**: If a component exceeds 200 lines, consider splitting it

### Reactivity Guidelines

Understanding Vue's reactivity system is crucial:

- **ref vs reactive**: Use `ref()` for primitives and values you'll reassign; use `reactive()` for objects you'll mutate
- **Computed for derived state**: Never store derived state in refs; use `computed()` instead
- **Watch for side effects**: Only use `watch()` for side effects like API calls or localStorage
- **Be mindful of reactivity loss**: Don't destructure reactive objects without `toRefs()`

### Props & Events Patterns

Proper component communication ensures maintainable code:

- **Type your props**: Use TypeScript interfaces with `defineProps<T>()`
- **Validate complex props**: Use validator functions for business logic validation
- **Emit typed events**: Use `defineEmits<T>()` for type-safe event handling
- **Use v-model for two-way binding**: Implement `modelValue` prop and `update:modelValue` emit

## Common Patterns

### Script Setup Structure

**Recommended structure for `<script setup>`:**
```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { User } from '@/types'

// 2. Props and Emits
const props = defineProps<{
  userId: string
  initialData?: User
}>()

const emit = defineEmits<{
  submit: [user: User]
  cancel: []
}>()

// 3. Composables
const router = useRouter()
const { user, loading, error } = useUser(props.userId)

// 4. Reactive State
const formData = ref({ name: '', email: '' })
const isEditing = ref(false)

// 5. Computed Properties
const isValid = computed(() => {
  return formData.value.name.length > 0 && formData.value.email.includes('@')
})

// 6. Watchers (for side effects only)
watch(() => props.userId, (newId) => {
  fetchUserData(newId)
})

// 7. Methods
function handleSubmit() {
  if (isValid.value) {
    emit('submit', formData.value)
  }
}

// 8. Lifecycle Hooks
onMounted(() => {
  if (props.initialData) {
    formData.value = { ...props.initialData }
  }
})
</script>
```

### Composable Pattern

**Correct: Well-structured composable**
```typescript
// composables/useUser.ts
import { ref, computed, watch } from 'vue'
import type { Ref } from 'vue'
import type { User } from '@/types'

export function useUser(userId: Ref<string> | string) {
  // State
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  // Computed
  const fullName = computed(() => {
    if (!user.value) return ''
    return `${user.value.firstName} ${user.value.lastName}`
  })

  // Methods
  async function fetchUser(id: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.getUser(id)
      user.value = response.data
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  // Auto-fetch when userId changes (if reactive)
  if (isRef(userId)) {
    watch(userId, (newId) => fetchUser(newId), { immediate: true })
  } else {
    fetchUser(userId)
  }

  // Return
  return {
    user: readonly(user),
    fullName,
    loading: readonly(loading),
    error: readonly(error),
    refresh: () => fetchUser(unref(userId))
  }
}
```

### Props with Defaults

**Correct: Typed props with defaults**
```vue
<script setup lang="ts">
interface Props {
  title: string
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  items?: string[]
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  disabled: false,
  items: () => []  // Use factory function for arrays/objects
})
</script>
```

### Event Handling

**Correct: Typed emits with payloads**
```vue
<script setup lang="ts">
interface FormData {
  name: string
  email: string
}

const emit = defineEmits<{
  submit: [data: FormData]
  cancel: []
  'update:modelValue': [value: string]
}>()

function handleSubmit(data: FormData) {
  emit('submit', data)
}
</script>
```

### v-model Implementation

**Correct: Custom v-model with defineModel (Vue 3.4+)**
```vue
<script setup lang="ts">
const model = defineModel<string>({ required: true })

// Or with default
const modelWithDefault = defineModel<string>({ default: '' })
</script>

<template>
  <input :value="model" @input="model = $event.target.value" />
</template>
```

**Correct: Custom v-model (Vue 3.3 and earlier)**
```vue
<script setup lang="ts">
const props = defineProps<{
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const value = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})
</script>

<template>
  <input v-model="value" />
</template>
```

### Template Ref Typing

**Correct: Typed template refs**
```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MyComponent from './MyComponent.vue'

// DOM element ref
const inputRef = ref<HTMLInputElement | null>(null)

// Component ref
const componentRef = ref<InstanceType<typeof MyComponent> | null>(null)

onMounted(() => {
  inputRef.value?.focus()
  componentRef.value?.someExposedMethod()
})
</script>

<template>
  <input ref="inputRef" />
  <MyComponent ref="componentRef" />
</template>
```

### Provide/Inject with Types

**Correct: Type-safe provide/inject**
```typescript
// types/injection-keys.ts
import type { InjectionKey, Ref } from 'vue'
import type { User } from './user'

export const UserKey: InjectionKey<Ref<User>> = Symbol('user')

// Parent component
import { provide, ref } from 'vue'
import { UserKey } from '@/types/injection-keys'

const user = ref<User>({ id: '1', name: 'John' })
provide(UserKey, user)

// Child component
import { inject } from 'vue'
import { UserKey } from '@/types/injection-keys'

const user = inject(UserKey)
if (!user) {
  throw new Error('User not provided')
}
```

### Error Boundary Component

**Correct: Error boundary with onErrorCaptured**
```vue
<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'

const error = ref<Error | null>(null)

onErrorCaptured((err) => {
  error.value = err
  // Return false to stop error propagation
  return false
})

function reset() {
  error.value = null
}
</script>

<template>
  <div v-if="error" class="error-boundary">
    <p>Something went wrong: {{ error.message }}</p>
    <button @click="reset">Try again</button>
  </div>
  <slot v-else />
</template>
```

### Async Component Loading

**Correct: Async components with loading/error states**
```typescript
import { defineAsyncComponent } from 'vue'

const AsyncDashboard = defineAsyncComponent({
  loader: () => import('./Dashboard.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,  // Show loading after 200ms
  timeout: 10000  // Timeout after 10s
})
```

## Tailwind CSS Best Practices

Vue's component-based architecture pairs naturally with Tailwind's utility-first approach. Follow these patterns for maintainable, consistent styling.

### Utility-First Approach

Apply Tailwind utility classes directly in Vue templates for rapid, consistent styling:

**Correct: Utility classes in template**
```vue
<template>
  <div class="mx-auto max-w-md rounded-xl bg-white p-6 shadow-lg">
    <h2 class="text-xl font-semibold text-gray-900">{{ title }}</h2>
    <p class="mt-2 text-gray-600">{{ description }}</p>
    <button class="mt-4 rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
      {{ buttonText }}
    </button>
  </div>
</template>
```

### Class Ordering Convention

Maintain consistent class ordering for readability. Recommended order:

1. **Layout** - `flex`, `grid`, `block`, `hidden`
2. **Positioning** - `relative`, `absolute`, `fixed`
3. **Box Model** - `w-`, `h-`, `m-`, `p-`
4. **Typography** - `text-`, `font-`, `leading-`
5. **Visual** - `bg-`, `border-`, `rounded-`, `shadow-`
6. **Interactive** - `hover:`, `focus:`, `active:`

Use the official Prettier plugin (`prettier-plugin-tailwindcss`) to automatically sort classes.

### Responsive Design (Mobile-First)

Use Tailwind's responsive prefixes for mobile-first responsive design:

**Correct: Mobile-first responsive layout**
```vue
<template>
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    <article
      v-for="item in items"
      :key="item.id"
      class="p-4 text-sm sm:p-6 sm:text-base lg:text-lg"
    >
      <h3 class="font-medium">{{ item.title }}</h3>
    </article>
  </div>
</template>
```

**Breakpoint Reference:**
- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up
- `2xl:` - 1536px and up

### State Variants

Use state variants for interactive elements:

**Correct: State variants for buttons**
```vue
<template>
  <button
    class="rounded-lg bg-indigo-600 px-4 py-2 font-medium text-white
           transition-colors duration-150
           hover:bg-indigo-700
           focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
           active:bg-indigo-800
           disabled:cursor-not-allowed disabled:opacity-50"
    :disabled="isLoading"
  >
    {{ isLoading ? 'Loading...' : 'Submit' }}
  </button>
</template>
```

### Dark Mode Support

Use the `dark:` prefix for dark mode styles:

**Correct: Dark mode support**
```vue
<template>
  <div class="bg-white dark:bg-gray-900">
    <h1 class="text-gray-900 dark:text-white">{{ title }}</h1>
    <p class="text-gray-600 dark:text-gray-400">{{ content }}</p>
    <div class="border-gray-200 dark:border-gray-700 rounded-lg border p-4">
      <slot />
    </div>
  </div>
</template>
```

### Dynamic Classes with Computed Properties

Use computed properties for conditional class binding:

**Correct: Computed classes for variants**
```vue
<script setup lang="ts">
import { computed } from 'vue'

type ButtonVariant = 'primary' | 'secondary' | 'danger'
type ButtonSize = 'sm' | 'md' | 'lg'

const props = withDefaults(defineProps<{
  variant?: ButtonVariant
  size?: ButtonSize
}>(), {
  variant: 'primary',
  size: 'md'
})

const variantClasses = computed(() => {
  const variants: Record<ButtonVariant, string> = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
  }
  return variants[props.variant]
})

const sizeClasses = computed(() => {
  const sizes: Record<ButtonSize, string> = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }
  return sizes[props.size]
})

const buttonClasses = computed(() => [
  'inline-flex items-center justify-center rounded-md font-medium',
  'transition-colors duration-150',
  'focus:outline-none focus:ring-2 focus:ring-offset-2',
  variantClasses.value,
  sizeClasses.value
])
</script>

<template>
  <button :class="buttonClasses">
    <slot />
  </button>
</template>
```

### Class Variance Authority (CVA) Pattern

For complex component variants, use the CVA pattern with a helper library:

**Correct: CVA-style variant management**
```vue
<script setup lang="ts">
import { computed } from 'vue'
import { cva, type VariantProps } from 'class-variance-authority'

const button = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
  {
    variants: {
      intent: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
        danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500'
      },
      size: {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-4 py-2 text-base',
        lg: 'px-6 py-3 text-lg'
      }
    },
    defaultVariants: {
      intent: 'primary',
      size: 'md'
    }
  }
)

type ButtonProps = VariantProps<typeof button>

const props = defineProps<{
  intent?: ButtonProps['intent']
  size?: ButtonProps['size']
}>()

const classes = computed(() => button({ intent: props.intent, size: props.size }))
</script>

<template>
  <button :class="classes">
    <slot />
  </button>
</template>
```

### Component Extraction for Reusable Patterns

Extract repeated utility patterns into Vue components:

**Correct: Reusable card component**
```vue
<!-- components/BaseCard.vue -->
<script setup lang="ts">
withDefaults(defineProps<{
  padding?: 'none' | 'sm' | 'md' | 'lg'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
}>(), {
  padding: 'md',
  shadow: 'md'
})
</script>

<template>
  <div
    class="rounded-xl bg-white dark:bg-gray-800"
    :class="[
      {
        'p-0': padding === 'none',
        'p-4': padding === 'sm',
        'p-6': padding === 'md',
        'p-8': padding === 'lg'
      },
      {
        'shadow-none': shadow === 'none',
        'shadow-sm': shadow === 'sm',
        'shadow-md': shadow === 'md',
        'shadow-lg': shadow === 'lg'
      }
    ]"
  >
    <slot />
  </div>
</template>
```

### Tailwind Configuration with Design Tokens

Define design tokens in your Tailwind config for consistency:

**Correct: tailwind.config.js with design tokens**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Semantic color tokens
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8'
        },
        surface: {
          light: '#ffffff',
          dark: '#1f2937'
        }
      },
      spacing: {
        // Custom spacing tokens
        '4.5': '1.125rem',
        '18': '4.5rem'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      borderRadius: {
        '4xl': '2rem'
      }
    }
  },
  plugins: []
}
```

### Tailwind CSS v4 Configuration

For Tailwind CSS v4, use the CSS-first configuration approach:

**Correct: Tailwind v4 CSS configuration**
```css
/* main.css */
@import "tailwindcss";

@theme {
  /* Custom colors */
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Custom spacing */
  --spacing-4-5: 1.125rem;
  --spacing-18: 4.5rem;

  /* Custom fonts */
  --font-family-sans: 'Inter', system-ui, sans-serif;
}
```

### Using `cn()` Helper for Conditional Classes

Use a class merging utility for conditional classes:

**Correct: cn() helper with clsx and tailwind-merge**
```typescript
// utils/cn.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Usage in component:**
```vue
<script setup lang="ts">
import { cn } from '@/utils/cn'

const props = defineProps<{
  class?: string
  isActive?: boolean
}>()
</script>

<template>
  <div
    :class="cn(
      'rounded-lg border p-4 transition-colors',
      isActive ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-white',
      props.class
    )"
  >
    <slot />
  </div>
</template>
```

## PrimeVue Best Practices

PrimeVue is a comprehensive Vue UI component library with 90+ components. Follow these patterns for effective integration and customization.

### Installation & Setup

**Correct: PrimeVue v4 setup with Vue 3**
```typescript
// main.ts
import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import App from './App.vue'

const app = createApp(App)

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: '.dark-mode'
    }
  }
})

app.mount('#app')
```

**Correct: Component registration (tree-shakeable)**
```typescript
// main.ts - Register only components you use
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

app.component('Button', Button)
app.component('DataTable', DataTable)
app.component('Column', Column)
```

### PassThrough (PT) API

The PassThrough API allows customization of internal DOM elements without modifying component source:

**Correct: Component-level PassThrough**
```vue
<script setup lang="ts">
import Panel from 'primevue/panel'
</script>

<template>
  <Panel
    header="User Profile"
    toggleable
    :pt="{
      header: {
        class: 'bg-primary-100 dark:bg-primary-900'
      },
      content: {
        class: 'p-6'
      },
      title: {
        class: 'text-xl font-semibold'
      },
      toggler: {
        class: 'hover:bg-primary-200 dark:hover:bg-primary-800 rounded-full'
      }
    }"
  >
    <p>Panel content here</p>
  </Panel>
</template>
```

**Correct: Dynamic PassThrough with state**
```vue
<script setup lang="ts">
import Panel from 'primevue/panel'
</script>

<template>
  <Panel
    header="Collapsible Panel"
    toggleable
    :pt="{
      header: (options) => ({
        class: [
          'transition-colors duration-200',
          {
            'bg-primary-500 text-white': options.state.d_collapsed,
            'bg-surface-100 dark:bg-surface-800': !options.state.d_collapsed
          }
        ]
      })
    }"
  >
    <p>Content changes header style when collapsed</p>
  </Panel>
</template>
```

### Global PassThrough Configuration

Define shared styles at the application level:

**Correct: Global PT configuration**
```typescript
// main.ts
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'

app.use(PrimeVue, {
  theme: {
    preset: Aura
  },
  pt: {
    // All buttons get consistent styling
    button: {
      root: {
        class: 'rounded-lg font-medium transition-all duration-200'
      }
    },
    // All inputs get consistent styling
    inputtext: {
      root: {
        class: 'rounded-lg border-2 focus:ring-2 focus:ring-primary-500'
      }
    },
    // All panels share styling
    panel: {
      header: {
        class: 'bg-surface-50 dark:bg-surface-900'
      }
    },
    // Global CSS injection
    global: {
      css: `
        .p-component {
          font-family: 'Inter', sans-serif;
        }
      `
    }
  }
})
```

### usePassThrough Utility

Extend existing presets with custom modifications:

**Correct: Extending Tailwind preset**
```typescript
// presets/custom-tailwind.ts
import { usePassThrough } from 'primevue/passthrough'
import Tailwind from 'primevue/passthrough/tailwind'

export const CustomTailwind = usePassThrough(
  Tailwind,
  {
    panel: {
      header: {
        class: ['bg-gradient-to-r from-primary-500 to-primary-600']
      },
      title: {
        class: ['text-white font-bold']
      }
    },
    button: {
      root: {
        class: ['shadow-lg hover:shadow-xl transition-shadow']
      }
    }
  },
  {
    mergeSections: true,  // Keep original sections
    mergeProps: false     // Replace props (don't merge arrays)
  }
)
```

**Merge Strategy Reference:**

| mergeSections | mergeProps | Behavior |
|---------------|------------|----------|
| `true` | `false` | Custom value replaces original (default) |
| `true` | `true` | Custom values merge with original |
| `false` | `true` | Only custom sections included |
| `false` | `false` | Minimal - only custom sections, no merging |

### Unstyled Mode with Tailwind

Use unstyled PrimeVue components with full Tailwind control:

**Correct: Unstyled mode configuration**
```typescript
// main.ts
import PrimeVue from 'primevue/config'

app.use(PrimeVue, {
  unstyled: true  // Remove all default styles
})
```

**Correct: Custom styled button with unstyled mode**
```vue
<script setup lang="ts">
import Button from 'primevue/button'
</script>

<template>
  <Button
    label="Submit"
    :pt="{
      root: {
        class: [
          'inline-flex items-center justify-center',
          'px-4 py-2 rounded-lg font-medium',
          'bg-primary-600 text-white',
          'hover:bg-primary-700 active:bg-primary-800',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
          'transition-colors duration-150',
          'disabled:opacity-50 disabled:cursor-not-allowed'
        ]
      },
      label: {
        class: 'font-medium'
      },
      icon: {
        class: 'mr-2'
      }
    }"
    :ptOptions="{ mergeSections: false, mergeProps: false }"
  />
</template>
```

### Wrapper Components Pattern

Create reusable wrapper components for consistent styling:

**Correct: Button wrapper component**
```vue
<!-- components/ui/AppButton.vue -->
<script setup lang="ts">
import Button from 'primevue/button'

type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'ghost'
type ButtonSize = 'sm' | 'md' | 'lg'

const props = withDefaults(defineProps<{
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
}>(), {
  variant: 'primary',
  size: 'md',
  loading: false
})

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
  secondary: 'bg-surface-200 text-surface-900 hover:bg-surface-300 focus:ring-surface-500',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  ghost: 'bg-transparent text-primary-600 hover:bg-primary-50 focus:ring-primary-500'
}

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
}
</script>

<template>
  <Button
    v-bind="$attrs"
    :loading="loading"
    :pt="{
      root: {
        class: [
          'inline-flex items-center justify-center rounded-lg font-medium',
          'transition-all duration-200',
          'focus:outline-none focus:ring-2 focus:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          variantClasses[variant],
          sizeClasses[size]
        ]
      }
    }"
    :ptOptions="{ mergeSections: false, mergeProps: false }"
  >
    <slot />
  </Button>
</template>

<script lang="ts">
export default {
  inheritAttrs: false
}
</script>
```

**Usage:**
```vue
<template>
  <AppButton variant="primary" size="lg" @click="handleSubmit">
    Submit Form
  </AppButton>
  <AppButton variant="ghost" size="sm">
    Cancel
  </AppButton>
</template>
```

### DataTable Best Practices

**Correct: Typed DataTable with Composition API**
```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

interface User {
  id: number
  name: string
  email: string
  role: string
  status: 'active' | 'inactive'
}

const users = ref<User[]>([])
const loading = ref(true)
const selectedUsers = ref<User[]>([])

// Pagination
const first = ref(0)
const rows = ref(10)

// Sorting
const sortField = ref<string>('name')
const sortOrder = ref<1 | -1>(1)

onMounted(async () => {
  loading.value = true
  try {
    users.value = await fetchUsers()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <DataTable
    v-model:selection="selectedUsers"
    :value="users"
    :loading="loading"
    :paginator="true"
    :rows="rows"
    :first="first"
    :sortField="sortField"
    :sortOrder="sortOrder"
    dataKey="id"
    stripedRows
    removableSort
    @page="(e) => first = e.first"
    @sort="(e) => { sortField = e.sortField; sortOrder = e.sortOrder }"
  >
    <Column selectionMode="multiple" headerStyle="width: 3rem" />
    <Column field="name" header="Name" sortable />
    <Column field="email" header="Email" sortable />
    <Column field="role" header="Role" sortable />
    <Column field="status" header="Status">
      <template #body="{ data }">
        <span
          :class="[
            'px-2 py-1 rounded-full text-xs font-medium',
            data.status === 'active'
              ? 'bg-green-100 text-green-800'
              : 'bg-red-100 text-red-800'
          ]"
        >
          {{ data.status }}
        </span>
      </template>
    </Column>
  </DataTable>
</template>
```

### Form Components Pattern

**Correct: Form with validation using PrimeVue**
```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'
import Message from 'primevue/message'

interface FormData {
  email: string
  password: string
  role: string | null
}

const formData = ref<FormData>({
  email: '',
  password: '',
  role: null
})

const errors = ref<Partial<Record<keyof FormData, string>>>({})
const submitted = ref(false)

const roles = [
  { label: 'Admin', value: 'admin' },
  { label: 'User', value: 'user' },
  { label: 'Guest', value: 'guest' }
]

const isValid = computed(() => {
  return Object.keys(errors.value).length === 0
})

function validate(): boolean {
  errors.value = {}

  if (!formData.value.email) {
    errors.value.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
    errors.value.email = 'Invalid email format'
  }

  if (!formData.value.password) {
    errors.value.password = 'Password is required'
  } else if (formData.value.password.length < 8) {
    errors.value.password = 'Password must be at least 8 characters'
  }

  if (!formData.value.role) {
    errors.value.role = 'Role is required'
  }

  return Object.keys(errors.value).length === 0
}

function handleSubmit() {
  submitted.value = true
  if (validate()) {
    // Submit form
    console.log('Form submitted:', formData.value)
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="space-y-4">
    <div class="flex flex-col gap-2">
      <label for="email" class="font-medium">Email</label>
      <InputText
        id="email"
        v-model="formData.email"
        :class="{ 'p-invalid': errors.email }"
        aria-describedby="email-error"
      />
      <Message v-if="errors.email" severity="error" :closable="false">
        {{ errors.email }}
      </Message>
    </div>

    <div class="flex flex-col gap-2">
      <label for="password" class="font-medium">Password</label>
      <Password
        id="password"
        v-model="formData.password"
        :class="{ 'p-invalid': errors.password }"
        toggleMask
        :feedback="false"
        aria-describedby="password-error"
      />
      <Message v-if="errors.password" severity="error" :closable="false">
        {{ errors.password }}
      </Message>
    </div>

    <div class="flex flex-col gap-2">
      <label for="role" class="font-medium">Role</label>
      <Dropdown
        id="role"
        v-model="formData.role"
        :options="roles"
        optionLabel="label"
        optionValue="value"
        placeholder="Select a role"
        :class="{ 'p-invalid': errors.role }"
        aria-describedby="role-error"
      />
      <Message v-if="errors.role" severity="error" :closable="false">
        {{ errors.role }}
      </Message>
    </div>

    <Button type="submit" label="Submit" class="w-full" />
  </form>
</template>
```

### Dialog & Overlay Patterns

**Correct: Confirmation dialog with composable**
```typescript
// composables/useConfirmDialog.ts
import { useConfirm } from 'primevue/useconfirm'

export function useConfirmDialog() {
  const confirm = useConfirm()

  function confirmDelete(
    message: string,
    onAccept: () => void,
    onReject?: () => void
  ) {
    confirm.require({
      message,
      header: 'Confirm Delete',
      icon: 'pi pi-exclamation-triangle',
      rejectClass: 'p-button-secondary p-button-outlined',
      acceptClass: 'p-button-danger',
      rejectLabel: 'Cancel',
      acceptLabel: 'Delete',
      accept: onAccept,
      reject: onReject
    })
  }

  function confirmAction(options: {
    message: string
    header: string
    onAccept: () => void
    onReject?: () => void
  }) {
    confirm.require({
      message: options.message,
      header: options.header,
      icon: 'pi pi-info-circle',
      rejectClass: 'p-button-secondary p-button-outlined',
      acceptClass: 'p-button-primary',
      accept: options.onAccept,
      reject: options.onReject
    })
  }

  return {
    confirmDelete,
    confirmAction
  }
}
```

**Usage:**
```vue
<script setup lang="ts">
import { useConfirmDialog } from '@/composables/useConfirmDialog'
import ConfirmDialog from 'primevue/confirmdialog'

const { confirmDelete } = useConfirmDialog()

function handleDelete(item: Item) {
  confirmDelete(
    `Are you sure you want to delete "${item.name}"?`,
    () => deleteItem(item.id)
  )
}
</script>

<template>
  <ConfirmDialog />
  <Button label="Delete" severity="danger" @click="handleDelete(item)" />
</template>
```

### Toast Notifications

**Correct: Toast service with composable**
```typescript
// composables/useNotifications.ts
import { useToast } from 'primevue/usetoast'

export function useNotifications() {
  const toast = useToast()

  function success(summary: string, detail?: string) {
    toast.add({
      severity: 'success',
      summary,
      detail,
      life: 3000
    })
  }

  function error(summary: string, detail?: string) {
    toast.add({
      severity: 'error',
      summary,
      detail,
      life: 5000
    })
  }

  function warn(summary: string, detail?: string) {
    toast.add({
      severity: 'warn',
      summary,
      detail,
      life: 4000
    })
  }

  function info(summary: string, detail?: string) {
    toast.add({
      severity: 'info',
      summary,
      detail,
      life: 3000
    })
  }

  return { success, error, warn, info }
}
```

### Accessibility Best Practices

PrimeVue components are WCAG 2.0 compliant. Ensure proper usage:

**Correct: Accessible form fields**
```vue
<template>
  <div class="flex flex-col gap-2">
    <label :for="id" class="font-medium">
      {{ label }}
      <span v-if="required" class="text-red-500" aria-hidden="true">*</span>
    </label>
    <InputText
      :id="id"
      v-model="modelValue"
      :aria-required="required"
      :aria-invalid="!!error"
      :aria-describedby="error ? `${id}-error` : undefined"
    />
    <small
      v-if="error"
      :id="`${id}-error`"
      class="text-red-500"
      role="alert"
    >
      {{ error }}
    </small>
  </div>
</template>
```

### Lazy Loading Components

**Correct: Async component loading for large PrimeVue components**
```typescript
// components/lazy/index.ts
import { defineAsyncComponent } from 'vue'

export const LazyDataTable = defineAsyncComponent({
  loader: () => import('primevue/datatable'),
  loadingComponent: () => import('@/components/ui/TableSkeleton.vue'),
  delay: 200
})

export const LazyEditor = defineAsyncComponent({
  loader: () => import('primevue/editor'),
  loadingComponent: () => import('@/components/ui/EditorSkeleton.vue'),
  delay: 200
})

export const LazyChart = defineAsyncComponent({
  loader: () => import('primevue/chart'),
  loadingComponent: () => import('@/components/ui/ChartSkeleton.vue'),
  delay: 200
})
```

## Anti-Patterns to Avoid

### Don't Mutate Props

**Incorrect:**
```vue
<script setup>
const props = defineProps(['items'])

function addItem(item) {
  props.items.push(item)  // Never mutate props!
}
</script>
```

**Correct:**
```vue
<script setup>
const props = defineProps(['items'])
const emit = defineEmits(['update:items'])

function addItem(item) {
  emit('update:items', [...props.items, item])
}
</script>
```

### Don't Use v-if with v-for

**Incorrect:**
```vue
<template>
  <div v-for="item in items" v-if="item.isActive" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

**Correct:**
```vue
<script setup>
const activeItems = computed(() => items.value.filter(item => item.isActive))
</script>

<template>
  <div v-for="item in activeItems" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

### Don't Store Derived State

**Incorrect:**
```vue
<script setup>
const items = ref([])
const itemCount = ref(0)  // Derived state stored separately

watch(items, () => {
  itemCount.value = items.value.length  // Manually syncing
})
</script>
```

**Correct:**
```vue
<script setup>
const items = ref([])
const itemCount = computed(() => items.value.length)  // Computed property
</script>
```

### Don't Destructure Reactive Objects

**Incorrect:**
```vue
<script setup>
const state = reactive({ count: 0, name: 'Vue' })
const { count, name } = state  // Loses reactivity!
</script>
```

**Correct:**
```vue
<script setup>
const state = reactive({ count: 0, name: 'Vue' })
const { count, name } = toRefs(state)  // Preserves reactivity
</script>
```

### Don't Concatenate Tailwind Class Names

Dynamic class concatenation breaks Tailwind's compiler and classes get purged in production:

**Incorrect:**
```vue
<script setup>
const color = ref('blue')
</script>

<template>
  <!-- Classes will be purged in production! -->
  <div :class="`bg-${color}-500 text-${color}-900`">
    Content
  </div>
</template>
```

**Correct:**
```vue
<script setup>
const color = ref<'blue' | 'green' | 'red'>('blue')

const colorClasses = computed(() => {
  const colors = {
    blue: 'bg-blue-500 text-blue-900',
    green: 'bg-green-500 text-green-900',
    red: 'bg-red-500 text-red-900'
  }
  return colors[color.value]
})
</script>

<template>
  <div :class="colorClasses">
    Content
  </div>
</template>
```

### Don't Overuse @apply

Excessive `@apply` usage defeats the purpose of utility-first CSS:

**Incorrect:**
```css
/* styles.css */
.card {
  @apply mx-auto max-w-md rounded-xl bg-white p-6 shadow-lg;
}

.card-title {
  @apply text-xl font-semibold text-gray-900;
}

.card-description {
  @apply mt-2 text-gray-600;
}

.card-button {
  @apply mt-4 rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700;
}
```

**Correct: Use Vue components instead**
```vue
<!-- components/Card.vue -->
<template>
  <div class="mx-auto max-w-md rounded-xl bg-white p-6 shadow-lg">
    <h2 class="text-xl font-semibold text-gray-900">
      <slot name="title" />
    </h2>
    <p class="mt-2 text-gray-600">
      <slot name="description" />
    </p>
    <div class="mt-4">
      <slot name="actions" />
    </div>
  </div>
</template>
```

### Don't Use Conflicting Utilities

Applying multiple utilities that target the same CSS property causes unpredictable results:

**Incorrect:**
```vue
<template>
  <!-- Both flex and grid target display property -->
  <div class="flex grid">Content</div>

  <!-- Multiple margin utilities conflict -->
  <div class="m-4 mx-6">Content</div>
</template>
```

**Correct:**
```vue
<template>
  <div :class="isGrid ? 'grid' : 'flex'">Content</div>

  <!-- Use specific margin utilities -->
  <div class="mx-6 my-4">Content</div>
</template>
```

### Don't Ignore Accessibility

Always include proper accessibility attributes alongside visual styling:

**Incorrect:**
```vue
<template>
  <button class="rounded bg-blue-600 p-2 text-white">
    <IconX />
  </button>
</template>
```

**Correct:**
```vue
<template>
  <button
    class="rounded bg-blue-600 p-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    aria-label="Close dialog"
  >
    <IconX aria-hidden="true" />
  </button>
</template>
```

### Don't Create Overly Long Class Strings

Break down complex class combinations into logical groups or components:

**Incorrect:**
```vue
<template>
  <div class="mx-auto mt-8 flex max-w-4xl flex-col items-center justify-between gap-4 rounded-xl border border-gray-200 bg-white p-6 shadow-lg transition-all duration-300 hover:border-blue-500 hover:shadow-xl dark:border-gray-700 dark:bg-gray-800 sm:flex-row sm:gap-6 md:p-8 lg:gap-8">
    <!-- 15+ utilities on one element -->
  </div>
</template>
```

**Correct: Extract to component or use computed**
```vue
<script setup>
const containerClasses = [
  // Layout
  'mx-auto max-w-4xl flex flex-col sm:flex-row',
  'items-center justify-between',
  'gap-4 sm:gap-6 lg:gap-8',
  // Spacing
  'mt-8 p-6 md:p-8',
  // Visual
  'rounded-xl border bg-white shadow-lg',
  'border-gray-200 dark:border-gray-700 dark:bg-gray-800',
  // Interactive
  'transition-all duration-300',
  'hover:border-blue-500 hover:shadow-xl'
]
</script>

<template>
  <div :class="containerClasses">
    <slot />
  </div>
</template>
```

### Don't Override PrimeVue Styles with CSS

Using CSS overrides bypasses the design system and causes maintenance issues:

**Incorrect:**
```css
/* styles.css - Avoid this approach */
.p-button {
  background-color: #3b82f6 !important;
  border-radius: 8px !important;
}

.p-datatable .p-datatable-thead > tr > th {
  background: #f3f4f6 !important;
}
```

**Correct: Use design tokens or PassThrough**
```typescript
// main.ts - Use design tokens
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      cssLayer: {
        name: 'primevue',
        order: 'tailwind-base, primevue, tailwind-utilities'
      }
    }
  },
  pt: {
    button: {
      root: { class: 'rounded-lg' }
    }
  }
})
```

### Don't Import Entire PrimeVue Library

Importing everything bloats bundle size:

**Incorrect:**
```typescript
// main.ts - Don't do this
import PrimeVue from 'primevue/config'
import * as PrimeVueComponents from 'primevue'  // Imports everything!

Object.entries(PrimeVueComponents).forEach(([name, component]) => {
  app.component(name, component)
})
```

**Correct: Import only what you need**
```typescript
// main.ts - Tree-shakeable imports
import Button from 'primevue/button'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

app.component('Button', Button)
app.component('DataTable', DataTable)
app.component('Column', Column)
```

### Don't Mix Styled and Unstyled Inconsistently

Mixing modes creates visual inconsistency:

**Incorrect:**
```typescript
// main.ts
app.use(PrimeVue, {
  unstyled: true  // Global unstyled
})

// SomeComponent.vue - Using styled component anyway
<Button label="Click" />  // No styles applied, looks broken
```

**Correct: Choose one approach consistently**
```typescript
// Option 1: Styled mode with PT customization
app.use(PrimeVue, {
  theme: { preset: Aura },
  pt: { /* global customizations */ }
})

// Option 2: Unstyled mode with complete PT styling
app.use(PrimeVue, {
  unstyled: true,
  pt: {
    button: {
      root: { class: 'px-4 py-2 bg-primary-600 text-white rounded-lg' }
    }
    // ... complete styling for all components
  }
})
```

### Don't Ignore Accessibility Attributes

PrimeVue provides accessibility out of the box, don't disable or ignore it:

**Incorrect:**
```vue
<template>
  <!-- Missing aria attributes and label -->
  <Button icon="pi pi-trash" @click="deleteItem" />

  <!-- No error message association -->
  <InputText v-model="email" :class="{ 'p-invalid': hasError }" />
  <span class="error">Invalid email</span>
</template>
```

**Correct: Maintain accessibility**
```vue
<template>
  <Button
    icon="pi pi-trash"
    aria-label="Delete item"
    @click="deleteItem"
  />

  <div class="flex flex-col gap-2">
    <label for="email">Email</label>
    <InputText
      id="email"
      v-model="email"
      :class="{ 'p-invalid': hasError }"
      :aria-invalid="hasError"
      aria-describedby="email-error"
    />
    <small id="email-error" v-if="hasError" class="text-red-500" role="alert">
      Invalid email
    </small>
  </div>
</template>
```

### Don't Hardcode PassThrough in Every Component

Repeating PT configuration across components creates duplication:

**Incorrect:**
```vue
<!-- ComponentA.vue -->
<Button :pt="{ root: { class: 'rounded-lg shadow-md' } }" />

<!-- ComponentB.vue -->
<Button :pt="{ root: { class: 'rounded-lg shadow-md' } }" />

<!-- ComponentC.vue -->
<Button :pt="{ root: { class: 'rounded-lg shadow-md' } }" />
```

**Correct: Use global PT or wrapper components**
```typescript
// main.ts - Global configuration
app.use(PrimeVue, {
  pt: {
    button: {
      root: { class: 'rounded-lg shadow-md' }
    }
  }
})

// Or use wrapper components (see Wrapper Components Pattern above)
```

## Nuxt.js Specific Guidelines

When using Nuxt.js, follow these additional patterns:

- **Auto-imports**: Leverage Nuxt's auto-imports for Vue APIs and composables
- **useFetch/useAsyncData**: Use Nuxt's data fetching composables for SSR-compatible data loading
- **definePageMeta**: Use for page-level metadata and middleware
- **Server routes**: Use `server/api/` for API endpoints
- **Runtime config**: Use `useRuntimeConfig()` for environment variables

## References

### Vue.js
- [Vue.js Documentation](https://vuejs.org)
- [Vue.js Style Guide](https://vuejs.org/style-guide/)
- [Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html)
- [VueUse - Collection of Vue Composition Utilities](https://vueuse.org)
- [Nuxt Documentation](https://nuxt.com)
- [Pinia Documentation](https://pinia.vuejs.org)

### Tailwind CSS
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Styling with Utility Classes](https://tailwindcss.com/docs/styling-with-utility-classes)
- [Tailwind CSS v4 Release](https://tailwindcss.com/blog/tailwindcss-v4)
- [Class Variance Authority (CVA)](https://cva.style/docs)
- [tailwind-merge](https://github.com/dcastil/tailwind-merge)
- [prettier-plugin-tailwindcss](https://github.com/tailwindlabs/prettier-plugin-tailwindcss)
- [Vue School - Tailwind CSS Fundamentals](https://vueschool.io/courses/tailwind-css-fundamentals)

### PrimeVue
- [PrimeVue Documentation](https://primevue.org/)
- [PrimeVue PassThrough API](https://primevue.org/passthrough/)
- [PrimeVue Theming - Styled Mode](https://primevue.org/theming/styled/)
- [PrimeVue GitHub Repository](https://github.com/primefaces/primevue)
- [PrimeVue v4 Component Changes](https://github.com/primefaces/primevue/wiki/v4-Component-Changes)
- [Volt - Tailwind CSS based PrimeVue Components](https://volt.primevue.org/)
- [Deep Dive into PrimeVue PassThrough Props](https://dev.to/cagataycivici/deep-dive-into-primevue-passthrough-props-2im8)
- [Build Your Own Vue UI Library with Unstyled PrimeVue](https://dev.to/cagataycivici/build-your-own-vue-ui-library-with-unstyled-primevue-core-and-tailwind-css-23ll)
- [PrimeIcons](https://primevue.org/icons/)
