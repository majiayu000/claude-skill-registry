---
name: vue
description: Builds UIs with Vue 3 including Composition API, reactivity, components, and state management. Use when creating Vue applications, building reactive interfaces, or working with the Vue ecosystem.
---

# Vue 3

The progressive JavaScript framework for building user interfaces.

## Quick Start

**Create project:**
```bash
npm create vue@latest my-app
cd my-app
npm install
npm run dev
```

## Component Basics

### Single-File Component (SFC)

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);

function increment() {
  count.value++;
}
</script>

<template>
  <button @click="increment">Count: {{ count }}</button>
</template>

<style scoped>
button {
  font-weight: bold;
}
</style>
```

## Reactivity

### ref - Primitive Values

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);
const message = ref('Hello');

// Access with .value in script
count.value++;
message.value = 'World';
</script>

<template>
  <!-- Auto-unwrapped in template -->
  <p>{{ count }} - {{ message }}</p>
</template>
```

### reactive - Objects

```vue
<script setup lang="ts">
import { reactive } from 'vue';

const state = reactive({
  count: 0,
  user: {
    name: 'John',
    email: 'john@example.com',
  },
});

// Direct access, no .value
state.count++;
state.user.name = 'Jane';
</script>

<template>
  <p>{{ state.count }} - {{ state.user.name }}</p>
</template>
```

### computed - Derived State

```vue
<script setup lang="ts">
import { ref, computed } from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`;
});

// Writable computed
const fullNameWritable = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value) => {
    const [first, last] = value.split(' ');
    firstName.value = first;
    lastName.value = last;
  },
});
</script>
```

### watch - Side Effects

```vue
<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue';

const count = ref(0);
const message = ref('');

// Watch single source
watch(count, (newVal, oldVal) => {
  console.log(`Count: ${oldVal} -> ${newVal}`);
});

// Watch multiple sources
watch([count, message], ([newCount, newMsg], [oldCount, oldMsg]) => {
  console.log('Changed');
});

// Watch with options
watch(
  count,
  (newVal) => console.log(newVal),
  { immediate: true, deep: true }
);

// Auto-track dependencies
watchEffect(() => {
  console.log(`Count is ${count.value}`);
});
</script>
```

## Props

```vue
<!-- ChildComponent.vue -->
<script setup lang="ts">
interface Props {
  title: string;
  count?: number;
  items?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => [],
});
</script>

<template>
  <h1>{{ props.title }}</h1>
  <p>Count: {{ props.count }}</p>
</template>
```

```vue
<!-- Parent -->
<ChildComponent title="Hello" :count="5" :items="['a', 'b']" />
```

## Events

```vue
<!-- ChildComponent.vue -->
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'update', value: number): void;
  (e: 'delete', id: string): void;
}>();

function handleClick() {
  emit('update', 42);
}
</script>

<template>
  <button @click="handleClick">Update</button>
  <button @click="emit('delete', '123')">Delete</button>
</template>
```

```vue
<!-- Parent -->
<ChildComponent @update="handleUpdate" @delete="handleDelete" />
```

## v-model

### Basic v-model

```vue
<!-- CustomInput.vue -->
<script setup lang="ts">
const model = defineModel<string>();
</script>

<template>
  <input v-model="model" />
</template>
```

```vue
<!-- Parent -->
<CustomInput v-model="message" />
```

### Named v-model

```vue
<!-- UserForm.vue -->
<script setup lang="ts">
const firstName = defineModel<string>('firstName');
const lastName = defineModel<string>('lastName');
</script>

<template>
  <input v-model="firstName" placeholder="First" />
  <input v-model="lastName" placeholder="Last" />
</template>
```

```vue
<!-- Parent -->
<UserForm v-model:firstName="first" v-model:lastName="last" />
```

## Slots

### Default Slot

```vue
<!-- Card.vue -->
<template>
  <div class="card">
    <slot>Default content</slot>
  </div>
</template>
```

```vue
<Card>
  <p>Custom content</p>
</Card>
```

### Named Slots

```vue
<!-- Layout.vue -->
<template>
  <header>
    <slot name="header" />
  </header>
  <main>
    <slot />
  </main>
  <footer>
    <slot name="footer" />
  </footer>
</template>
```

```vue
<Layout>
  <template #header>
    <h1>Title</h1>
  </template>

  <p>Main content</p>

  <template #footer>
    <p>Footer</p>
  </template>
</Layout>
```

### Scoped Slots

```vue
<!-- List.vue -->
<script setup lang="ts">
defineProps<{ items: string[] }>();
</script>

<template>
  <ul>
    <li v-for="(item, index) in items" :key="index">
      <slot :item="item" :index="index" />
    </li>
  </ul>
</template>
```

```vue
<List :items="['a', 'b', 'c']">
  <template #default="{ item, index }">
    {{ index }}: {{ item }}
  </template>
</List>
```

## Lifecycle Hooks

```vue
<script setup lang="ts">
import {
  onMounted,
  onUpdated,
  onUnmounted,
  onBeforeMount,
  onBeforeUpdate,
  onBeforeUnmount,
} from 'vue';

onBeforeMount(() => {
  console.log('Before mount');
});

onMounted(() => {
  console.log('Mounted - DOM available');
});

onBeforeUpdate(() => {
  console.log('Before update');
});

onUpdated(() => {
  console.log('Updated');
});

onBeforeUnmount(() => {
  console.log('Before unmount');
});

onUnmounted(() => {
  console.log('Unmounted - cleanup');
});
</script>
```

## Template Refs

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';

const inputRef = ref<HTMLInputElement | null>(null);

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<template>
  <input ref="inputRef" />
</template>
```

## Provide / Inject

```vue
<!-- Parent.vue -->
<script setup lang="ts">
import { provide, ref } from 'vue';

const theme = ref('dark');
const updateTheme = (newTheme: string) => {
  theme.value = newTheme;
};

provide('theme', { theme, updateTheme });
</script>
```

```vue
<!-- DeepChild.vue -->
<script setup lang="ts">
import { inject } from 'vue';

const { theme, updateTheme } = inject('theme', {
  theme: ref('light'),
  updateTheme: () => {},
});
</script>

<template>
  <p>Theme: {{ theme }}</p>
  <button @click="updateTheme('light')">Light</button>
</template>
```

## Composables

```typescript
// composables/useMouse.ts
import { ref, onMounted, onUnmounted } from 'vue';

export function useMouse() {
  const x = ref(0);
  const y = ref(0);

  function update(event: MouseEvent) {
    x.value = event.pageX;
    y.value = event.pageY;
  }

  onMounted(() => {
    window.addEventListener('mousemove', update);
  });

  onUnmounted(() => {
    window.removeEventListener('mousemove', update);
  });

  return { x, y };
}
```

```vue
<script setup lang="ts">
import { useMouse } from '@/composables/useMouse';

const { x, y } = useMouse();
</script>

<template>
  <p>Mouse: {{ x }}, {{ y }}</p>
</template>
```

### Async Composable

```typescript
// composables/useFetch.ts
import { ref, watchEffect, toValue, type Ref } from 'vue';

export function useFetch<T>(url: Ref<string> | string) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(true);

  watchEffect(async () => {
    data.value = null;
    error.value = null;
    loading.value = true;

    try {
      const response = await fetch(toValue(url));
      data.value = await response.json();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  });

  return { data, error, loading };
}
```

## Directives

### Built-in Directives

```vue
<template>
  <!-- Conditional -->
  <p v-if="show">Visible</p>
  <p v-else-if="other">Other</p>
  <p v-else>Hidden</p>

  <p v-show="show">Toggle visibility</p>

  <!-- Loop -->
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>

  <!-- Binding -->
  <img :src="imageUrl" :alt="imageAlt" />
  <div :class="{ active: isActive, disabled }" />
  <div :style="{ color: textColor, fontSize: '16px' }" />

  <!-- Events -->
  <button @click="handleClick">Click</button>
  <input @keyup.enter="submit" />
  <form @submit.prevent="handleSubmit" />

  <!-- Two-way binding -->
  <input v-model="text" />
  <input v-model.trim="text" />
  <input v-model.number="age" type="number" />
</template>
```

### Custom Directive

```typescript
// directives/vFocus.ts
import type { Directive } from 'vue';

export const vFocus: Directive = {
  mounted(el) {
    el.focus();
  },
};
```

```vue
<script setup lang="ts">
import { vFocus } from '@/directives/vFocus';
</script>

<template>
  <input v-focus />
</template>
```

## Transition

```vue
<template>
  <Transition name="fade">
    <p v-if="show">Hello</p>
  </Transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

## Best Practices

1. **Use Composition API** - Better TypeScript support, logic reuse
2. **Extract composables** - Reusable stateful logic
3. **Type props and emits** - Full type safety
4. **Use defineModel** - Simpler v-model implementation
5. **Prefer ref over reactive** - More explicit, fewer gotchas

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting .value | Use .value in script, auto-unwrap in template |
| Destructuring reactive | Use toRefs() to keep reactivity |
| Wrong ref type | ref for primitives, reactive for objects |
| Missing key in v-for | Always provide unique :key |
| Mutating props | Emit events to parent |

## Reference Files

- [references/composition-api.md](references/composition-api.md) - Full API reference
- [references/reactivity.md](references/reactivity.md) - Reactivity deep dive
- [references/typescript.md](references/typescript.md) - TypeScript patterns
