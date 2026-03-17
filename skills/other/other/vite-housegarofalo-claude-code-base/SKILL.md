---
name: vite
description: Build modern frontend applications with Vite. Covers project setup, plugins, configuration, environment variables, and build optimization. Use for React, Vue, Svelte development with fast HMR and optimized production builds.
---

# Vite Build Tool

Next-generation frontend tooling with instant server start and lightning-fast HMR.

## Instructions

1. **Use native ESM** - Vite serves ES modules directly in development
2. **Leverage HMR** - Hot module replacement works out of the box
3. **Configure plugins** - Extend Vite with official and community plugins
4. **Optimize builds** - Use Rollup under the hood for production
5. **Manage env vars** - Use VITE_ prefix for client-exposed variables

## Project Setup

### Create New Project

```bash
# Create with template
npm create vite@latest my-app -- --template react-ts
npm create vite@latest my-app -- --template vue-ts
npm create vite@latest my-app -- --template svelte-ts

# Available templates:
# vanilla, vanilla-ts
# vue, vue-ts
# react, react-ts, react-swc, react-swc-ts
# preact, preact-ts
# lit, lit-ts
# svelte, svelte-ts
# solid, solid-ts
# qwik, qwik-ts

cd my-app
npm install
npm run dev
```

### Project Structure

```
my-app/
├── public/
│   └── favicon.svg
├── src/
│   ├── assets/
│   ├── components/
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## Configuration

### Basic Configuration

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },

  server: {
    port: 3000,
    open: true,
    cors: true,
  },

  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

### TypeScript Path Aliases

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

## Environment Variables

### Setup

```bash
# .env
VITE_API_URL=http://localhost:4000
VITE_APP_TITLE=My App

# .env.development
VITE_API_URL=http://localhost:4000

# .env.production
VITE_API_URL=https://api.example.com

# .env.local (gitignored)
VITE_SECRET_KEY=your-secret
```

### Usage

```tsx
// Access in code
const apiUrl = import.meta.env.VITE_API_URL;
const title = import.meta.env.VITE_APP_TITLE;
const isDev = import.meta.env.DEV;
const isProd = import.meta.env.PROD;
const mode = import.meta.env.MODE;

// TypeScript types
// vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## Plugins

### Common Plugins

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';
import { VitePWA } from 'vite-plugin-pwa';
import svgr from 'vite-plugin-svgr';

export default defineConfig({
  plugins: [
    react(),

    // SVG as React components
    svgr({
      svgrOptions: {
        icon: true,
      },
    }),

    // Bundle analyzer
    visualizer({
      open: true,
      gzipSize: true,
    }),

    // PWA support
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'robots.txt'],
      manifest: {
        name: 'My App',
        short_name: 'App',
        theme_color: '#ffffff',
      },
    }),
  ],
});
```

### React with SWC (Faster)

```ts
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [react()],
});
```

## Proxy Configuration

```ts
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      // String shorthand
      '/foo': 'http://localhost:4567',

      // Object options
      '/api': {
        target: 'http://localhost:4000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },

      // WebSocket
      '/ws': {
        target: 'ws://localhost:4000',
        ws: true,
      },
    },
  },
});
```

## Build Optimization

### Code Splitting

```ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor splitting
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          query: ['@tanstack/react-query'],
        },
      },
    },
  },
});

// Or with function
output: {
  manualChunks(id) {
    if (id.includes('node_modules')) {
      return 'vendor';
    }
  },
}
```

### Dynamic Imports

```tsx
// Route-level code splitting
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Asset Handling

```ts
export default defineConfig({
  build: {
    assetsInlineLimit: 4096, // 4kb - inline smaller assets
    chunkSizeWarningLimit: 500, // kb
  },
});
```

## CSS Configuration

### PostCSS with Tailwind

```ts
// vite.config.ts - PostCSS is auto-detected
// Just create postcss.config.js

// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### CSS Modules

```tsx
// Automatically enabled for .module.css files
import styles from './Button.module.css';

function Button() {
  return <button className={styles.button}>Click</button>;
}
```

### Global CSS

```tsx
// main.tsx
import './styles/globals.css';
```

## Testing Setup

### Vitest Configuration

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
    coverage: {
      reporter: ['text', 'json', 'html'],
    },
  },
});
```

```ts
// src/test/setup.ts
import '@testing-library/jest-dom';
```

## Library Mode

```ts
// vite.config.ts for building a library
import { defineConfig } from 'vite';
import { resolve } from 'path';
import react from '@vitejs/plugin-react';
import dts from 'vite-plugin-dts';

export default defineConfig({
  plugins: [
    react(),
    dts({ include: ['src'] }),
  ],
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLib',
      fileName: 'my-lib',
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
});
```

## Common Commands

```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npx tsc --noEmit

# Lint
npm run lint
```

## Best Practices

| Practice | Recommendation |
|----------|----------------|
| **Env vars** | Always use VITE_ prefix for client vars |
| **Aliases** | Configure both vite.config.ts and tsconfig.json |
| **Code splitting** | Lazy load routes and heavy components |
| **Assets** | Put static assets in public/, imports in src/assets/ |
| **Plugins** | Use official plugins when available |
| **Proxy** | Use dev server proxy for API calls |

## When to Use

- React, Vue, Svelte applications
- Projects needing fast HMR
- Modern browser-targeted builds
- Component library development
- Any frontend project with ES modules

## Notes

- 10-100x faster than Webpack in development
- Uses esbuild for dependency pre-bundling
- Rollup for production builds
- First-class TypeScript support
- Works with any framework via plugins
