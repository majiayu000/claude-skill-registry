---
name: mockup-creation
description: Create interactive, production-ready UI mockups and prototypes using Vue.js 3, TypeScript, Vite, and TailwindCSS. Use when building web mockups, prototypes, landing pages, dashboards, admin panels, or interactive UI demonstrations. Trigger when users mention "create mockup", "build prototype", "Vue mockup", "interactive demo", "UI prototype", "design to code", or need rapid frontend development with modern tooling.
license: MIT
compatibility: Requires Node.js 20.19+, 22.12+
---

# Mockup Creation

Create polished, interactive UI mockups and prototypes using Vue.js 3 with TypeScript, Vite, and TailwindCSS.

## Overview

Rapid creation of production-quality mockups with:

- **Vue.js 3 Composition API** with TypeScript
- **Vite** for fast development
- **TailwindCSS v4+** with Vite plugin integration
- **Component-driven architecture**
- **Interactive reactivity**

## Quick Start

## 1. Initialize Project

```bash
# Create Vite + Vue + TypeScript project
npm create vite@latest my-mockup -- --template vue-ts
cd my-mockup
npm install
```

### 2. Install and Configure TailwindCSS

**Install TailwindCSS with Vite plugin (v4+):**

```bash
npm install tailwindcss @tailwindcss/vite
```

**Configure vite.config.ts:**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss()
  ]
})
```

**Import in src/style.css:**

```css
@import "tailwindcss";
```

**Import in src/main.ts:**

```typescript
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

createApp(App).mount('#app')
```

### 3. Start Development

```bash
npm run dev
# Opens http://localhost:5173
```

## Workflow

### 1. Define Structure

Identify mockup requirements:

- Layout type (single page, dashboard, multi-page)
- Sections needed (header, hero, features, footer, sidebar)
- Responsive breakpoints (mobile, tablet, desktop)
- Interactive elements (forms, modals, dropdowns)

### 2. Create Component Architecture

Organize by functionality:

```
src/
├── components/
│   ├── layout/        # Header, Footer, Sidebar
│   ├── ui/            # Button, Card, Modal, Input
│   └── sections/      # Hero, Features, Testimonials
├── views/             # Page-level components
├── composables/       # Shared logic (useModal, useForm)
└── types/             # TypeScript interfaces
```

### 3. Build Components

**Example: Type-safe Button Component**

```vue
<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md'
})

const buttonClasses = computed(() => {
  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-600 text-white hover:bg-gray-700',
    outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50'
  }
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  }
  return `font-semibold rounded-lg transition ${variants[props.variant]} ${sizes[props.size]}`
})
</script>

<template>
  <button :class="buttonClasses">
    <slot />
  </button>
</template>
```

### 4. Apply Responsive Design

Use TailwindCSS breakpoints:

- `sm:` (640px), `md:` (768px), `lg:` (1024px), `xl:` (1280px), `2xl:` (1536px)

**Responsive Grid Example:**

```vue
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <Card v-for="item in items" :key="item.id" />
</div>
```

### 5. Add Interactivity

**Composable Pattern:**

```typescript
// composables/useModal.ts
import { ref } from 'vue'

export function useModal() {
  const isOpen = ref(false)
  const open = () => { isOpen.value = true }
  const close = () => { isOpen.value = false }
  return { isOpen, open, close }
}
```

### 6. Build for Production

```bash
npm run build      # Build to dist/
npm run preview    # Preview production build
```

## Common Patterns

### Landing Page

```vue
<template>
  <div class="min-h-screen flex flex-col">
    <Header />
    <main class="flex-1">
      <Hero />
      <Features />
    </main>
    <Footer />
  </div>
</template>
```

### Dashboard Layout

```vue
<template>
  <div class="flex h-screen bg-gray-100">
    <Sidebar class="w-64 bg-white shadow-lg" />
    <div class="flex-1 flex flex-col">
      <TopBar class="bg-white shadow-sm" />
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
    </div>
  </div>
</template>
```

## Design System

### Colors

- Primary: `blue-600`, Secondary: `gray-600`
- Success: `green-600`, Warning: `yellow-600`, Error: `red-600`
- Neutral: `gray-100` to `gray-900`

### Spacing

Use consistent scale: `p-1` (4px), `p-2` (8px), `p-4` (16px), `p-6` (24px), `p-8` (32px)

### Typography

- Headings: `text-4xl`, `text-3xl`, `text-2xl`, `text-xl`
- Body: `text-base` (16px)
- Weights: `font-normal`, `font-medium`, `font-semibold`, `font-bold`

## Advanced Guides

For detailed implementations:

- **[Component Library](references/component-library.md)** - Complete reusable components
- **[TailwindCSS Patterns](references/tailwind-patterns.md)** - Advanced styling
- **[Vue Composition API](references/composition-api.md)** - State management
- **[Animations](references/animations.md)** - Transitions and effects
- **[Examples](references/examples.md)** - Complete mockup examples
- **[Deployment](references/deployment.md)** - Build and hosting

## Scripts

Helper scripts available in `scripts/` (Bash and PowerShell versions):

**create-component.sh / .ps1** - Generate Vue components with TypeScript boilerplate

```bash
# Linux/macOS
./scripts/create-component.sh ComponentName ui

# Windows
.\scripts\create-component.ps1 -ComponentName ComponentName -Type ui
```

**build-deploy.sh / .ps1** - Build and prepare for deployment

```bash
# Linux/macOS
./scripts/build-deploy.sh

# Windows
.\scripts\build-deploy.ps1
```

## Troubleshooting

**TailwindCSS not working:**

- Restart dev server after vite.config.ts changes
- Verify `@import "tailwindcss";` in CSS file
- Check Vite plugin is correctly configured

**TypeScript errors:**

- Install Volar extension (not Vetur)
- Enable "Take Over Mode" in VS Code

**HMR issues:**

```bash
rm -rf node_modules/.vite
npm run dev
```

**Large bundle size:**

- Use dynamic imports: `() => import('./Component.vue')`
- Analyze with: `npm run build -- --mode analyze`

## Best Practices

1. **Component Design**: Small, single-purpose, reusable
2. **TypeScript**: Clear interfaces for props and emits
3. **TailwindCSS**: Prefer utilities over custom CSS
4. **Composables**: Extract shared logic
5. **Responsive**: Mobile-first approach
6. **Performance**: Lazy load routes and large components
7. **Accessibility**: ARIA labels and keyboard navigation
