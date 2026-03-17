---
name: mockup-creation
description: Create interactive, production-ready UI mockups and prototypes using NuxtJS 4 (Vue) or Next.js (React), TypeScript, and TailwindCSS v4. Use when building web mockups, prototypes, landing pages, dashboards, admin panels, or interactive UI demonstrations. Trigger when users mention "create mockup", "build prototype", "interactive demo", "UI prototype", "design to code", or need rapid frontend development with modern tooling. Prefer NuxtJS for Vue-based projects; use Next.js when users mention ReactJS.
license: MIT
compatibility: Requires Node.js 20.x or newer
---

# Mockup Creation

Create polished, interactive UI mockups and prototypes using NuxtJS 4 (Vue) or Next.js (React) with TypeScript and TailwindCSS v4.

## Overview

Rapid creation of production-quality mockups with:

**NuxtJS 4 (Vue):**
- **Vue 3 Composition API** with TypeScript
- **Vite** bundler (built-in)
- **Auto-imports** for components and composables
- **Zero-config TypeScript** with auto-generated types
- **File-based routing** from pages/ directory

**Next.js (React):**
- **React 19** with TypeScript v5.1.0+
- **Turbopack** bundler (default, faster than Webpack)
- **App Router** with Server/Client Components
- **Built-in TypeScript** with zero configuration
- **File-based routing** from app/ directory

**Common Features:**
- **TailwindCSS v4** with modern tooling
- **Component-driven architecture**
- **Server-side rendering (SSR)** or static site generation (SSG)
- **Interactive reactivity**
- **Production-ready optimizations**

## Quick Start

### Option A: NuxtJS 4 (Vue-based)

### Option A: NuxtJS 4 (Vue-based)

#### 1. Initialize Project

```bash
# Create NuxtJS 4 project (TypeScript enabled by default)
npx nuxi@latest init my-mockup
cd my-mockup
npm install
```

#### 2. Install and Configure TailwindCSS

**Install TailwindCSS v4 with Vite plugin:**

```bash
npm install -D tailwindcss @tailwindcss/vite
```

**Configure nuxt.config.ts:**

```typescript
// https://nuxt.com/docs/4.x/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  devtools: { enabled: true },
  
  typescript: {
    strict: true,
    typeCheck: true
  },
  
  // Auto-import components and composables
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  
  // App configuration
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'My Mockup',
      meta: [
        { name: 'description', content: 'My mockup description' }
      ],
    }
  },
  
  // Vite configuration with TailwindCSS v4
  vite: {
    plugins: [
      tailwindcss()
    ],
    css: {
      devSourcemap: true
    }
  }
})
```

**Create CSS file and import TailwindCSS (e.g., assets/css/main.css):**

```css
@import "tailwindcss";
```

**Import CSS in app.vue or nuxt.config.ts:**

```typescript
// In nuxt.config.ts, add to the config:
export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],
  // ... rest of config
})
```

#### 3. Start Development

```bash
npm run dev
# Opens http://localhost:3000
```

### Option B: Next.js (React-based)

#### 1. Initialize Project

```bash
# Create Next.js project (uses recommended defaults with TypeScript and TailwindCSS)
npx create-next-app@latest my-mockup --yes
cd my-mockup
```

**Or with custom options:**

```bash
npx create-next-app@latest my-mockup
# Choose: TypeScript: Yes, TailwindCSS: Yes, App Router: Yes
```

#### 2. Verify TailwindCSS v4 Setup

**Next.js includes TailwindCSS by default. To upgrade to v4:**

```bash
npm install -D tailwindcss@next @tailwindcss/postcss@next
```

**Update tailwind.config.ts:**

```typescript
import type { Config } from 'tailwindcss'

export default {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
} satisfies Config
```

**Update postcss.config.mjs:**

```javascript
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

**Update app/globals.css:**

```css
@import "tailwindcss";
```

#### 3. Start Development

```bash
npm run dev
# Opens http://localhost:3000
```

## Workflow

### 1. Define Structure

Identify mockup requirements:

- Layout type (single page, dashboard, multi-page)
- Sections needed (header, hero, features, footer, sidebar)
- Responsive breakpoints (mobile, tablet, desktop)
- Interactive elements (forms, modals, dropdowns)

### 2. Create Component Architecture

**NuxtJS (Vue) auto-imports from:**

```
my-mockup/
├── components/
│   ├── layout/        # Header, Footer, Sidebar (auto-imported)
│   ├── ui/            # Button, Card, Modal, Input (auto-imported)
│   └── sections/      # Hero, Features, Testimonials (auto-imported)
├── pages/             # File-based routing (auto-routed)
├── composables/       # Shared logic (auto-imported)
├── layouts/           # Layout templates (default.vue, dashboard.vue)
└── types/             # TypeScript interfaces
```

**Next.js (React) structure:**

```
my-mockup/
├── app/
│   ├── layout.tsx     # Root layout (required)
│   ├── page.tsx       # Home page
│   ├── dashboard/
│   │   └── page.tsx   # /dashboard route
│   └── globals.css    # TailwindCSS imports
├── components/
│   ├── layout/        # Header, Footer, Sidebar
│   ├── ui/            # Button, Card, Modal, Input
│   └── sections/      # Hero, Features, Testimonials
├── lib/               # Utilities and shared logic
└── types/             # TypeScript interfaces
```

### 3. Build Components

**NuxtJS (Vue) Example: Type-safe Button Component (components/ui/Button.vue)**

```vue
<script setup lang="ts">
// No need to import 'computed' - auto-imported by Nuxt
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

**Usage in pages/index.vue:**

```vue
<template>
  <div>
    <!-- Auto-imported as UiButton from components/ui/Button.vue -->
    <UiButton variant="primary" size="lg">
      Get Started
    </UiButton>
  </div>
</template>
```

**Next.js (React) Example: Type-safe Button Component (components/ui/Button.tsx)**

```typescript
import { ButtonHTMLAttributes } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}

export function Button({ 
  variant = 'primary', 
  size = 'md', 
  children,
  className = '',
  ...props 
}: ButtonProps) {
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
  
  const buttonClasses = `font-semibold rounded-lg transition ${variants[variant]} ${sizes[size]} ${className}`
  
  return (
    <button className={buttonClasses} {...props}>
      {children}
    </button>
  )
}
```

**Usage in app/page.tsx:**

```typescript
import { Button } from '@/components/ui/Button'

export default function Home() {
  return (
    <div>
      <Button variant="primary" size="lg">
        Get Started
      </Button>
    </div>
  )
}
```

### 4. Apply Responsive Design

Use TailwindCSS breakpoints:

- `sm:` (640px), `md:` (768px), `lg:` (1024px), `xl:` (1280px), `2xl:` (1536px)

**NuxtJS (Vue) Responsive Grid Example:**

```vue
<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- Auto-imported as UiCard from components/ui/Card.vue -->
    <UiCard v-for="item in items" :key="item.id" :data="item" />
  </div>
</template>

<script setup lang="ts">
const items = ref([...])
</script>
```

**Next.js (React) Responsive Grid Example:**

```typescript
import { Card } from '@/components/ui/Card'

export default function FeaturesSection() {
  const items = [
    { id: 1, title: 'Feature 1', description: '...' },
    // ...
  ]
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map((item) => (
        <Card key={item.id} data={item} />
      ))}
    </div>
  )
}
```

### 5. Add Interactivity

**NuxtJS (Vue) Composable Pattern (composables/useModal.ts):**

```typescript
// Auto-imported by Nuxt - no need to import 'ref'
export function useModal() {
  const isOpen = ref(false)
  const open = () => { isOpen.value = true }
  const close = () => { isOpen.value = false }
  return { isOpen, open, close }
}
```

**Usage in any Vue component:**

```vue
<script setup lang="ts">
// Auto-imported - no import statement needed
const { isOpen, open, close } = useModal()
</script>
```

**Next.js (React) Custom Hook Pattern (lib/hooks/useModal.ts):**

```typescript
import { useState } from 'react'

export function useModal() {
  const [isOpen, setIsOpen] = useState(false)
  const open = () => setIsOpen(true)
  const close = () => setIsOpen(false)
  return { isOpen, open, close }
}
```

**Usage in any React component:**

```typescript
'use client' // Mark as Client Component for interactivity

import { useModal } from '@/lib/hooks/useModal'

export default function MyComponent() {
  const { isOpen, open, close } = useModal()
  
  return (
    <div>
      <button onClick={open}>Open Modal</button>
      {isOpen && <Modal onClose={close} />}
    </div>
  )
}
```

### 6. Build for Production

**NuxtJS:**

```bash
npm run build      # Build for production (.output/)
npm run preview    # Preview production build
npm run generate   # Generate static site (SSG)
```

**Next.js:**

```bash
npm run build      # Build for production (.next/)
npm run start      # Start production server (SSR)
# For static export (SSG), add to next.config.js:
# output: 'export'
```

## Common Patterns

### Landing Page (NuxtJS)

**Create layout (layouts/default.vue):**

```vue
<template>
  <div class="min-h-screen flex flex-col">
    <LayoutHeader />
    <main class="flex-1">
      <slot />
    </main>
    <LayoutFooter />
  </div>
</template>
```

**Create page (pages/index.vue):**

```vue
<template>
  <div>
    <SectionsHero />
    <SectionsFeatures />
  </div>
</template>
```

### Landing Page (Next.js)

**Create layout (app/layout.tsx):**

```typescript
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
```

**Create page (app/page.tsx):**

```typescript
import { Hero } from '@/components/sections/Hero'
import { Features } from '@/components/sections/Features'

export default function Home() {
  return (
    <div>
      <Hero />
      <Features />
    </div>
  )
}
```

### Dashboard Layout (NuxtJS)

**Create dashboard layout (layouts/dashboard.vue):**

```vue
<template>
  <div class="flex h-screen bg-gray-100">
    <LayoutSidebar class="w-64 bg-white shadow-lg" />
    <div class="flex-1 flex flex-col">
      <LayoutTopBar class="bg-white shadow-sm" />
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
```

**Use in page (pages/dashboard/index.vue):**

```vue
<script setup lang="ts">
definePageMeta({
  layout: 'dashboard'
})
</script>

<template>
  <div>
    <!-- Dashboard content -->
  </div>
</template>
```

### Dashboard Layout (Next.js)

**Create dashboard layout (app/dashboard/layout.tsx):**

```typescript
import { Sidebar } from '@/components/layout/Sidebar'
import { TopBar } from '@/components/layout/TopBar'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar className="w-64 bg-white shadow-lg" />
      <div className="flex-1 flex flex-col">
        <TopBar className="bg-white shadow-sm" />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

**Use in page (app/dashboard/page.tsx):**

```typescript
export default function DashboardPage() {
  return (
    <div>
      {/* Dashboard content */}
    </div>
  )
}
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

- **[Component Library](references/component-library.md)** - Complete reusable Vue components with TypeScript
- **[TailwindCSS v4 Patterns](references/tailwind-patterns.md)** - Advanced styling (works with both frameworks)
- **[NuxtJS Composables](references/composition-api.md)** - State management and auto-imports (Vue-specific)
- **[React Hooks](references/react-hooks.md)** - Custom hooks and state management (React-specific)
- **[Animations](references/animations.md)** - Vue transitions and TailwindCSS animations
- **[Examples](references/examples.md)** - Complete Vue/NuxtJS mockup examples
- **[Deployment](references/deployment.md)** - Build and hosting guides for both frameworks

## Scripts

Helper scripts available in `scripts/` (Bash and PowerShell versions):

**create-component.sh / .ps1** - Generate components with TypeScript boilerplate

```bash
# Linux/macOS - Vue component
./scripts/create-component.sh ComponentName ui vue

# Linux/macOS - React component
./scripts/create-component.sh ComponentName ui react

# Windows - Vue component
.\scripts\create-component.ps1 -ComponentName ComponentName -Type ui -Framework vue

# Windows - React component
.\scripts\create-component.ps1 -ComponentName ComponentName -Type ui -Framework react
```

**build-deploy.sh / .ps1** - Build and prepare for deployment

```bash
# Linux/macOS
./scripts/build-deploy.sh

# Windows
.\scripts\build-deploy.ps1
```

**NuxtJS CLI commands:**

```bash
npx nuxi add component ComponentName  # Add new component
npx nuxi add page pageName            # Add new page
npx nuxi add layout layoutName        # Add new layout
```

**Next.js CLI commands:**

```bash
# No built-in CLI for components, use scripts above
# Or manually create files in app/ or components/
```

## Troubleshooting

### NuxtJS (Vue)

**TailwindCSS v4 not working:**

- Restart dev server after nuxt.config.ts changes
- Verify `@import "tailwindcss";` in your CSS file
- Ensure `@tailwindcss/vite` plugin is in vite.plugins array
- Check CSS file is imported in nuxt.config.ts or app.vue
- Run `npx nuxi prepare` to regenerate types

**TypeScript errors:**

- Install Volar extension (not Vetur)
- Run `npx nuxi prepare` to generate types
- Restart TypeScript server in VS Code

**Auto-imports not working:**

```bash
rm -rf .nuxt
npx nuxi prepare
npm run dev
```

**HMR issues:**

```bash
rm -rf .nuxt node_modules/.cache
npm run dev
```

**Large bundle size:**

- Use lazy loading: `defineAsyncComponent(() => import('./Component.vue'))`
- Analyze with: `npx nuxi analyze`

### Next.js (React)

**TailwindCSS not working:**

- Check `tailwind.config.ts` has correct content paths
- Verify `@import "tailwindcss";` in app/globals.css
- Restart dev server after config changes
- Clear `.next` folder: `rm -rf .next && npm run dev`

**TypeScript errors:**

- Ensure tsconfig.json is properly configured
- Run `npm run build` to see full type checking
- Restart TypeScript server in VS Code

**Server vs Client Components:**

- Use `'use client'` directive at top of file for interactive components
- Server Components (default) cannot use hooks or event handlers
- Client Components can use useState, useEffect, onClick, etc.

**Build errors:**

```bash
rm -rf .next node_modules/.cache
npm install
npm run build
```

**Large bundle size:**

- Use dynamic imports: `const Component = dynamic(() => import('./Component'))`
- Analyze with: `npm run build` (shows bundle sizes)

## Best Practices

### Common (Both Frameworks)

1. **Component Design**: Small, single-purpose, reusable
2. **TypeScript**: Clear interfaces for props and component APIs
3. **TailwindCSS**: Prefer utilities over custom CSS
4. **Responsive**: Mobile-first approach
5. **Performance**: Use SSR/SSG when appropriate, lazy load large components
6. **Accessibility**: ARIA labels and keyboard navigation
7. **Code Organization**: Group related components, consistent naming

### NuxtJS (Vue) Specific

8. **Composables**: Extract shared logic (auto-imported)
9. **Auto-imports**: Leverage Nuxt's auto-import system for components and composables
10. **File-based Routing**: Use pages/ directory for automatic routing
11. **Layouts**: Create reusable layouts for consistent UI structure
12. **SEO**: Use `useHead()` and `useSeoMeta()` for meta tags

### Next.js (React) Specific

8. **Server Components**: Default to Server Components, use Client Components only when needed
9. **Data Fetching**: Use async Server Components for data fetching
10. **Metadata API**: Use `generateMetadata()` for dynamic SEO tags
11. **Image Optimization**: Use Next.js `<Image>` component for automatic optimization
12. **Route Handlers**: Use route.ts for API endpoints in app/api/
