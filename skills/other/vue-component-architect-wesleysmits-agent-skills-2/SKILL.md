---
name: scaffolding-vue-components
description: Scaffolds Vue/Nuxt components with Composition API, CSS modules, Vitest tests, and Storybook stories. Use when the user asks to create a Vue component, generate component boilerplate, or mentions Vue 3 architecture.
---

# Vue Component Architect

## When to use this skill

- User asks to create a new Vue component
- User wants component scaffolding with tests and stories
- User mentions Nuxt component creation
- User asks for TypeScript props definitions
- User wants CSS modules or scoped styles setup

## Workflow

- [ ] Determine component name and location
- [ ] Detect project conventions (Nuxt vs Vue, styling approach)
- [ ] Generate component file with Composition API
- [ ] Create CSS module or scoped styles
- [ ] Generate Vitest test file
- [ ] Create Storybook story
- [ ] Export from index if barrel pattern used

## Instructions

### Step 1: Determine Component Details

Gather from user:

- Component name (PascalCase)
- Location: `src/components/`, `components/`, or feature folder
- Type: presentational, container, layout, or page component

Derive file paths:

```
src/components/Button/
├── Button.vue
├── Button.test.ts
├── Button.stories.ts
└── index.ts
```

### Step 2: Detect Project Conventions

**Vue vs Nuxt:**

```bash
ls nuxt.config.* 2>/dev/null && echo "Nuxt project"
ls vite.config.* vue.config.* 2>/dev/null && echo "Vue project"
```

**Styling approach:**

```bash
grep -l "module.css\|module.scss" src/**/*.vue 2>/dev/null | head -1 && echo "CSS Modules"
grep -l "<style scoped" src/**/*.vue 2>/dev/null | head -1 && echo "Scoped styles"
npm ls tailwindcss 2>/dev/null && echo "Tailwind CSS"
```

**State management:**

```bash
npm ls pinia vuex 2>/dev/null
```

**Test framework:**

```bash
npm ls vitest @vue/test-utils 2>/dev/null
```

### Step 3: Generate Component File

Use the standard Composition API structure:

- `<script setup lang="ts">` with typed props and emits
- `withDefaults(defineProps<Props>(), { ... })` for defaults
- `defineEmits<{ event: [payload] }>()` for typed events
- `<style module>` with design tokens

[See component-templates.md](examples/component-templates.md) for full templates including:

- Standard component with variants
- Component with composables
- Pinia store integration

### Step 4: Generate Test File

Use Vitest with Vue Test Utils:

```typescript
import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import ComponentName from "./ComponentName.vue";

describe("ComponentName", () => {
  it("renders slot content", () => {
    const wrapper = mount(ComponentName, {
      slots: { default: "Hello" },
    });
    expect(wrapper.text()).toContain("Hello");
  });

  it("emits click when not disabled", async () => {
    const wrapper = mount(ComponentName);
    await wrapper.trigger("click");
    expect(wrapper.emitted("click")).toHaveLength(1);
  });
});
```

[See testing.md](examples/testing.md) for more patterns including Pinia testing and async components.

### Step 5: Create Storybook Story

Use CSF3 format for Storybook 7+:

```typescript
import type { Meta, StoryObj } from "@storybook/vue3";
import ComponentName from "./ComponentName.vue";

const meta: Meta<typeof ComponentName> = {
  title: "Components/ComponentName",
  component: ComponentName,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary"] },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { label: "Primary Button", variant: "primary" },
};
```

[See storybook.md](examples/storybook.md) for slot stories, decorators, and interactions.

### Step 6: Create Barrel Export

**index.ts:**

```typescript
export { default as ComponentName } from "./ComponentName.vue";
```

## Common Patterns

**v-model support (Vue 3.4+):**

```vue
<script setup lang="ts">
  const modelValue = defineModel<string>({ default: "" });
</script>
```

**Expose methods:**

```vue
<script setup lang="ts">
  const focus = () => inputRef.value?.focus();
  defineExpose({ focus });
</script>
```

**Provide/Inject:**

```typescript
// Parent
provide("state", reactive({ active: 0 }));

// Child
const state = inject<{ active: number }>("state");
```

[See advanced-patterns.md](examples/advanced-patterns.md) for compound components, generics, and Nuxt patterns.

## Validation

Before completing:

- [ ] Component renders without errors
- [ ] TypeScript has no errors
- [ ] Props interface uses defineProps with types
- [ ] Emits are properly typed
- [ ] Tests pass
- [ ] Story renders in Storybook

## Error Handling

- **Module not found**: Check import paths and file extensions (`.vue`).
- **CSS module not applying**: Ensure using `$style` in template and `<style module>`.
- **Test setup missing**: Install `@vue/test-utils` and configure Vitest for Vue.
- **Storybook not rendering**: Check `.storybook/main.js` uses `@storybook/vue3`.
- **Pinia not available in tests**: Call `setActivePinia(createPinia())` in beforeEach.
- **Unsure about conventions**: Check existing components in project for patterns.

## Resources

- [Vue 3 Documentation](https://vuejs.org/guide/introduction.html)
- [Vue Test Utils](https://test-utils.vuejs.org/)
- [Storybook for Vue](https://storybook.js.org/docs/vue/get-started/introduction)
- [Pinia Documentation](https://pinia.vuejs.org/)

## Examples

- [Component Templates](examples/component-templates.md) — Full component code examples
- [Testing](examples/testing.md) — Vitest patterns and Pinia testing
- [Storybook](examples/storybook.md) — Story formats and interactions
- [Advanced Patterns](examples/advanced-patterns.md) — Generics, Suspense, Nuxt
