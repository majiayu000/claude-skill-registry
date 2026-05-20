---
name: shadcn-vue
description: shadcn-vue for Vue/Nuxt with Reka UI components and Tailwind. Use for accessible UI, Auto Form, data tables, charts, or encountering component imports, dark mode, Reka UI errors.

  Keywords: shadcn-vue, shadcn vue, Reka UI, radix-vue, Vue components, Nuxt components, Tailwind CSS, accessible components, headless ui, Auto Form, Zod validation, TanStack Table, data tables, Unovis charts, dark mode, useColorMode, components.json, bunx shadcn-vue, vueuse, composables, Vue 3, Nuxt 3, TypeScript, accessibility, ARIA, component library, UI components, form builder, schema validation
license: MIT
---

# shadcn-vue Production Stack

**Production-tested**: Vue/Nuxt applications with accessible, customizable components
**Last Updated**: 2025-12-09
**Status**: Production Ready ✅
**Latest Version**: shadcn-vue@latest (Reka UI v2)
**Dependencies**: Tailwind CSS, Reka UI, Vue 3+ or Nuxt 3+

---

## Quick Start (3 Minutes)

### For Vue Projects (Vite)

#### 1. Initialize shadcn-vue

```bash
# Using Bun (recommended)
bunx shadcn-vue@latest init

# Using npm
npx shadcn-vue@latest init
```

**During initialization**:
- Style: `New York` or `Default` (cannot change later!)
- Base color: `Slate` (recommended)
- CSS variables: `Yes` (required for dark mode)

#### 2. Configure TypeScript Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

#### 3. Configure Vite

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite' // Tailwind v4
import path from 'path'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
})
```

#### 4. Add Your First Component

```bash
bunx shadcn-vue@latest add button
# or: npx shadcn-vue@latest add button
```

**See Full Setup**: `templates/quick-setup.ts`

---

### For Nuxt Projects

```bash
# Create project with Tailwind
bun create nuxt-app my-app
cd my-app
bun add -D @nuxtjs/tailwindcss

# Configure Nuxt
# nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss']
})

# Initialize shadcn-vue
bunx shadcn-vue@latest init
# or: npx shadcn-vue@latest init
# or: pnpm dlx shadcn-vue@latest init
```

---

## Component Library (50+ Components)

### Navigation & Layout
- Accordion, Alert Dialog, Avatar, Badge, Breadcrumb, Card, Carousel, Collapsible, Dialog, Drawer, Dropdown Menu, Menu Bar, Navigation Menu, Pagination, Popover, Resizable, Scroll Area, Sheet, Sidebar, Tabs, Toast, Tooltip

### Form Components
- Auto Form, Button, Calendar, Checkbox, Combobox, Command, Context Menu, Date Picker, Form, Input, Input OTP, Label, Number Field, PIN Input, Radio Group, Range Calendar, Select, Slider, Sonner, Switch, Textarea, Toggle, Toggle Group

### Data Display
- Aspect Ratio, Data Table, Skeleton, Stepper, Splitter, Table, Tag Input

### Advanced
- Charts (Unovis), Color Picker, Editable, File Upload, Sortable

**Full Component Reference**: https://shadcn-vue.com/docs/components

---

## Auto Form - Schema-Based Forms

### Installation

```bash
bunx shadcn-vue@latest add auto-form
# or: npx shadcn-vue@latest add auto-form

bun add zod
# or: npm install zod
```

### Basic Usage

```vue
<script setup lang="ts">
import { AutoForm } from '@/components/ui/auto-form'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email'),
  age: z.number().min(18, 'Must be 18 or older'),
  bio: z.string().optional(),
  subscribe: z.boolean().default(false)
})

function onSubmit(values: z.infer<typeof schema>) {
  console.log('Form submitted:', values)
}
</script>

<template>
  <AutoForm :schema="schema" @submit="onSubmit">
    <template #submit>
      <Button type="submit">Submit</Button>
    </template>
  </AutoForm>
</template>
```

**Supported Field Types**: string, number, boolean, date, enum, array, object

---

## Data Tables with TanStack Table

### Installation

```bash
bunx shadcn-vue@latest add data-table
# or: npx shadcn-vue@latest add data-table

bun add @tanstack/vue-table
# or: npm install @tanstack/vue-table
```

### Basic Setup

```vue
<script setup lang="ts">
import { DataTable } from '@/components/ui/data-table'
import { h } from 'vue'

const columns = [
  {
    accessorKey: 'id',
    header: 'ID',
  },
  {
    accessorKey: 'name',
    header: 'Name',
  },
  {
    accessorKey: 'email',
    header: 'Email',
  }
]

const data = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
]
</script>

<template>
  <DataTable :columns="columns" :data="data" />
</template>
```

**Features**: Sorting, filtering, pagination, row selection, column visibility, expandable rows

---

## Dark Mode Implementation

### Installation

```bash
bun add @vueuse/core
# or: npm install @vueuse/core
```

### Setup Theme Provider

```vue
<!-- components/ThemeProvider.vue -->
<script setup lang="ts">
import { useColorMode } from '@vueuse/core'

const mode = useColorMode()
</script>

<template>
  <div :class="mode">
    <slot />
  </div>
</template>
```

### Use in Components

```vue
<script setup>
import { useColorMode } from '@vueuse/core'

const mode = useColorMode()

function toggleTheme() {
  mode.value = mode.value === 'dark' ? 'light' : 'dark'
}
</script>

<template>
  <Button @click="toggleTheme">
    {{ mode === 'dark' ? '🌙' : '☀️' }}
  </Button>
</template>
```

---

## Critical Rules

### Always Do

✅ **Run `init` before adding components**
- Creates required configuration and utilities
- Sets up path aliases

✅ **Use CSS variables for theming** (`cssVariables: true`)
- Enables dark mode support
- Flexible theme customization

✅ **Configure TypeScript path aliases**
- Required for component imports
- Must match `components.json` aliases

✅ **Keep components.json in version control**
- Team members need same configuration
- Documents project setup

✅ **Use Bun for faster installs** (recommended)
- 10-20x faster than npm

### Never Do

❌ **Don't change `style` after initialization**
- Requires complete reinstall
- Reinitialize in new directory instead

❌ **Don't mix Radix Vue and Reka UI v2**
- Incompatible component APIs
- Use one or the other

❌ **Don't skip TypeScript configuration**
- Component imports will fail
- IDE autocomplete won't work

❌ **Don't use without Tailwind CSS**
- Components are styled with Tailwind
- Won't render correctly

---

## Top 7 Critical Issues

### Issue #1: Missing TypeScript Path Aliases

**Error**: `Cannot find module '@/components/ui/button'`

**Solution**:
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

### Issue #2: Tailwind CSS Not Configured

**Error**: Components render without styles

**Solution**:
```css
/* src/assets/index.css */
@import "tailwindcss";
```

```typescript
// vite.config.ts (Tailwind v4)
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()]
})
```

---

### Issue #3: CSS Variables Not Defined

**Error**: Theme colors not applying, gray/transparent components

**Solution**: Ensure all CSS variables are defined (run `init` command)

---

### Issue #4: Wrong Style Selected

**Error**: Components look different than expected

**Solution**: Choose carefully during `init` (New York or Default) - cannot change later without reinstall

---

### Issue #5: Mixing Radix Vue and Reka UI

**Error**: Type conflicts, duplicate components

**Solution**:
- Use `bunx shadcn-vue@latest` for Reka UI v2
- Use `bunx shadcn-vue@radix` for legacy Radix Vue
- Don't mix both

---

### Issue #6: Monorepo Path Issues

**Error**: Components installed in wrong directory

**Solution**: Use `-c` flag to specify workspace:
```bash
bunx shadcn-vue@latest init -c ./apps/web
bunx shadcn-vue@latest add button -c ./apps/web
```

---

### Issue #7: Component Import Fails After Manual Edit

**Error**: Import paths broken after editing `components.json`

**Solution**: Keep `components.json` and `tsconfig.json` aliases in sync. Test imports after any config changes.

---

**See All 7 Issues**: `references/error-catalog.md`

---

## CLI Commands Reference

### init Command

```bash
# Initialize in current directory
bunx shadcn-vue@latest init
# or: npx shadcn-vue@latest init

# Initialize in specific directory (monorepo)
bunx shadcn-vue@latest init -c ./apps/web
# or: npx shadcn-vue@latest init -c ./apps/web
```

### add Command

```bash
# Add single component
bunx shadcn-vue@latest add button
# or: npx shadcn-vue@latest add button

# Add multiple components
bunx shadcn-vue@latest add button card dialog

# Add all components
bunx shadcn-vue@latest add --all
# or: npx shadcn-vue@latest add --all
```

### diff Command

```bash
# Check for component updates
bunx shadcn-vue@latest diff button
# or: npx shadcn-vue@latest diff button
```

---

## Reka UI v2 Migration

shadcn-vue now uses **Reka UI v2** (formerly Radix Vue) as its foundation. All new components use Reka UI primitives.

**Migration:** Existing projects should update to Reka UI v2. See official migration guide: [shadcn-vue.com/docs/changelog#reka-ui](https://shadcn-vue.com/docs/changelog#reka-ui)

---

## Configuration

shadcn-vue uses `components.json` to configure:
- Component paths (`@/components/ui`)
- Utils location (`@/lib/utils`)
- Tailwind config paths
- TypeScript paths

**Full example:** See `templates/components.json` or generate via `bunx shadcn-vue@latest init`

---

## Utils Library

The `@/lib/utils.ts` file provides the `cn()` helper for merging Tailwind classes:
- Combines multiple className strings
- Uses `clsx` + `tailwind-merge` for conflict resolution

**Auto-generated** by `shadcn-vue init` - no manual setup needed.

---

## Bundled Resources

**Templates** (`templates/`):
- `quick-setup.ts` - Complete setup guide for Vue/Nuxt with examples (190 lines)

**References** (`references/`):
- `error-catalog.md` - All 7 documented issues with solutions (267 lines)

---

## When to Load References

Load these references based on the task:

1. **Load `references/error-catalog.md` when:**
   - User encounters "component not found" or import errors
   - Setup commands fail or configuration issues arise
   - Tailwind CSS variables or TypeScript paths broken
   - **Trigger phrases:** "not working", "error", "fails to", "broken"

2. **Load `references/component-examples.md` when:**
   - User asks "how do I implement [component]?"
   - Need copy-paste examples for specific components
   - Building forms, tables, navigation, or data display
   - **Trigger phrases:** "example", "how to use", "implement", "code sample"

3. **Load `references/dark-mode-setup.md` when:**
   - Implementing dark mode / theme switching
   - User mentions Vue 3 + Vite, Nuxt, or Astro setup
   - Need composable patterns for theme management
   - **Trigger phrases:** "dark mode", "theme", "light/dark", "color scheme"

---

## Integration with Other Skills

This skill composes well with:

- **nuxt-v4** → Nuxt framework
- **tailwind-v4-shadcn** → Tailwind v4 with React shadcn/ui
- **react-hook-form-zod** → Form validation patterns (similar to Auto Form)
- **tanstack-query** → Data fetching for tables
- **zustand-state-management** → State management

---

## Resources

**References** (`references/`):
- `component-examples.md` - All 50+ component examples with code
- `dark-mode-setup.md` - Complete dark mode implementation guide
- `error-catalog.md` - Common errors and solutions

**Templates** (`templates/`):
- Component templates available in references/component-examples.md

---

## Additional Resources

**Official Documentation**:
- shadcn-vue Docs: https://shadcn-vue.com
- Reka UI Docs: https://reka-ui.com
- GitHub: https://github.com/radix-vue/shadcn-vue

**Examples**:
- Component Examples: https://shadcn-vue.com/examples
- Starter Templates: https://github.com/radix-vue/shadcn-vue/tree/main/templates

---

**Production Tested**: Vue/Nuxt applications, admin dashboards, content management systems
**Last Updated**: 2025-12-09
**Token Savings**: ~65% (reduces setup + component documentation)
