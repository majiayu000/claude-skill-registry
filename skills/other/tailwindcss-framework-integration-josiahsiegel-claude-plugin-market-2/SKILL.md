---
name: tailwindcss-framework-integration
description: Tailwind CSS integration guide for React, Vue, Next.js, and other frameworks
---

# Tailwind CSS Framework Integration

## React with Vite

### Setup

```bash
# Create React + Vite project
npm create vite@latest my-app -- --template react-ts
cd my-app

# Install Tailwind CSS
npm install -D tailwindcss @tailwindcss/vite
```

### Configuration

```javascript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()]
})
```

```css
/* src/index.css */
@import "tailwindcss";
```

```tsx
// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

### Component Example

```tsx
// src/components/Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

const variants = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
  outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50'
}

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`
        inline-flex items-center justify-center
        font-medium rounded-lg
        transition-colors duration-200
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        disabled:opacity-50 disabled:cursor-not-allowed
        ${variants[variant]}
        ${sizes[size]}
      `}
    >
      {children}
    </button>
  )
}
```

## Next.js

### Setup (App Router)

```bash
# Create Next.js project (Tailwind included by default)
npx create-next-app@latest my-app
cd my-app
```

If adding to existing project:

```bash
npm install -D tailwindcss @tailwindcss/postcss
```

### Configuration

```javascript
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
}
```

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.6 0.2 250);
}
```

```tsx
// app/layout.tsx
import './globals.css'

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-white dark:bg-gray-900">{children}</body>
    </html>
  )
}
```

### Server Components

Tailwind works seamlessly with React Server Components:

```tsx
// app/page.tsx (Server Component)
export default function Home() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
        Welcome
      </h1>
      <p className="mt-4 text-gray-600 dark:text-gray-300">
        Server-rendered with Tailwind
      </p>
    </main>
  )
}
```

### Dark Mode with next-themes

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
'use client'

import { ThemeProvider } from 'next-themes'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
}
```

```tsx
// app/layout.tsx
import { Providers } from './providers'
import './globals.css'

export default function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

```css
/* globals.css - Add dark mode variant */
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
```

## Vue 3

### Setup with Vite

```bash
npm create vue@latest my-app
cd my-app

npm install -D tailwindcss @tailwindcss/vite
```

### Configuration

```javascript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()]
})
```

```css
/* src/assets/main.css */
@import "tailwindcss";
```

```typescript
// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'

createApp(App).mount('#app')
```

### Component Example

```vue
<!-- src/components/Button.vue -->
<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary'
}>()
</script>

<template>
  <button
    class="px-4 py-2 rounded-lg font-medium transition-colors"
    :class="{
      'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
      'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary'
    }"
  >
    <slot />
  </button>
</template>
```

### Scoped Styles with @reference

```vue
<template>
  <h1>Hello world!</h1>
</template>

<style scoped>
/* Reference global Tailwind definitions */
@reference "../../assets/main.css";

h1 {
  @apply text-2xl font-bold text-blue-600;
}
</style>
```

### Alternative: CSS Variables

```vue
<template>
  <h1>Hello world!</h1>
</template>

<style scoped>
h1 {
  /* Use CSS variables directly - better performance */
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-blue-600);
}
</style>
```

## Nuxt 3

### Setup

```bash
npx nuxi init my-app
cd my-app

npm install -D tailwindcss @tailwindcss/postcss
```

### Configuration

```javascript
// postcss.config.mjs
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
}
```

```css
/* assets/css/main.css */
@import "tailwindcss";
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  css: ['~/assets/css/main.css']
})
```

## Svelte / SvelteKit

### Setup

```bash
npm create svelte@latest my-app
cd my-app

npm install -D tailwindcss @tailwindcss/vite
```

### Configuration

```javascript
// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [sveltekit(), tailwindcss()]
})
```

```css
/* src/app.css */
@import "tailwindcss";
```

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import '../app.css'
</script>

<slot />
```

### Component Example

```svelte
<!-- src/lib/Button.svelte -->
<script lang="ts">
  export let variant: 'primary' | 'secondary' = 'primary'
</script>

<button
  class="px-4 py-2 rounded-lg font-medium transition-colors
    {variant === 'primary' ? 'bg-blue-600 text-white hover:bg-blue-700' : ''}
    {variant === 'secondary' ? 'bg-gray-200 text-gray-900 hover:bg-gray-300' : ''}"
>
  <slot />
</button>
```

## Astro

### Setup

```bash
npm create astro@latest my-app
cd my-app

npx astro add tailwind
```

### Manual Setup

```bash
npm install -D tailwindcss @tailwindcss/vite
```

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  vite: {
    plugins: [tailwindcss()]
  }
})
```

```css
/* src/styles/global.css */
@import "tailwindcss";
```

```astro
<!-- src/layouts/Layout.astro -->
---
import '../styles/global.css'
---
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>My Site</title>
  </head>
  <body class="bg-white dark:bg-gray-900">
    <slot />
  </body>
</html>
```

## Remix

### Setup

```bash
npx create-remix@latest my-app
cd my-app

npm install -D tailwindcss @tailwindcss/vite
```

### Configuration

```javascript
// vite.config.ts
import { vitePlugin as remix } from '@remix-run/dev'
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [remix(), tailwindcss()]
})
```

```css
/* app/tailwind.css */
@import "tailwindcss";
```

```tsx
// app/root.tsx
import stylesheet from './tailwind.css?url'
import { Links } from '@remix-run/react'

export const links = () => [
  { rel: 'stylesheet', href: stylesheet }
]

export default function App() {
  return (
    <html>
      <head>
        <Links />
      </head>
      <body className="bg-white dark:bg-gray-900">
        <Outlet />
      </body>
    </html>
  )
}
```

## Best Practices for All Frameworks

### 1. Use the Prettier Plugin

```bash
npm install -D prettier prettier-plugin-tailwindcss
```

```json
// .prettierrc
{
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### 2. Install VS Code Extension

```bash
code --install-extension bradlc.vscode-tailwindcss
```

### 3. Create Reusable Components

Don't repeat long class strings—extract components:

```tsx
// Instead of repeating this everywhere:
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">

// Create a component:
<Button variant="primary">Click me</Button>
```

### 4. Use clsx or tailwind-merge for Conditional Classes

```bash
npm install clsx tailwind-merge
```

```tsx
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
<div className={cn(
  "base-class",
  isActive && "active-class",
  disabled && "opacity-50"
)} />
```

### 5. Configure Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"]
    }
  }
}
```

```tsx
import { Button } from '@/components/Button'
```
