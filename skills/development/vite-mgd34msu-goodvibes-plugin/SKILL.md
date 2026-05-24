---
name: vite
description: Builds web applications with Vite including dev server, production builds, plugins, and configuration. Use when scaffolding projects, configuring build tools, optimizing bundles, or setting up development environments.
---

# Vite

Next-generation frontend build tool with instant dev server and optimized production builds.

## Quick Start

**Create project:**
```bash
npm create vite@latest my-app
cd my-app
npm install
npm run dev
```

**Templates:**
```bash
npm create vite@latest my-app -- --template react
npm create vite@latest my-app -- --template react-ts
npm create vite@latest my-app -- --template vue
npm create vite@latest my-app -- --template vue-ts
npm create vite@latest my-app -- --template svelte
npm create vite@latest my-app -- --template svelte-ts
```

## Configuration

### Basic Config

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

### Full Configuration

```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig(({ command, mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],

    // Path aliases
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@components': path.resolve(__dirname, './src/components'),
        '@lib': path.resolve(__dirname, './src/lib'),
      },
    },

    // Dev server
    server: {
      port: 3000,
      host: true, // Listen on all addresses
      open: true,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
      },
    },

    // Build options
    build: {
      outDir: 'dist',
      sourcemap: mode === 'development',
      minify: 'terser',
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            utils: ['lodash', 'date-fns'],
          },
        },
      },
    },

    // Preview server (for built app)
    preview: {
      port: 4173,
    },

    // Define global constants
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },

    // CSS options
    css: {
      modules: {
        localsConvention: 'camelCaseOnly',
      },
      preprocessorOptions: {
        scss: {
          additionalData: `@import "@/styles/variables.scss";`,
        },
      },
    },
  };
});
```

## Environment Variables

### Env Files

```bash
.env                # Loaded in all cases
.env.local          # Loaded in all cases, ignored by git
.env.[mode]         # Only loaded in specified mode
.env.[mode].local   # Only loaded in specified mode, ignored by git
```

### Define Variables

```bash
# .env
VITE_API_URL=https://api.example.com
VITE_APP_TITLE=My App

# Not exposed to client (no VITE_ prefix)
DATABASE_URL=postgres://...
```

### Access Variables

```typescript
// In client code
console.log(import.meta.env.VITE_API_URL);
console.log(import.meta.env.VITE_APP_TITLE);

// Built-in variables
console.log(import.meta.env.MODE);       // 'development' | 'production'
console.log(import.meta.env.BASE_URL);   // Base URL
console.log(import.meta.env.PROD);       // boolean
console.log(import.meta.env.DEV);        // boolean
```

### TypeScript Types

```typescript
// env.d.ts
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

### React

```typescript
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react({
      // Enable React Refresh
      fastRefresh: true,
      // Use automatic JSX runtime
      jsxRuntime: 'automatic',
    }),
  ],
});
```

### React SWC (Faster)

```bash
npm install -D @vitejs/plugin-react-swc
```

```typescript
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [react()],
});
```

### SVG as Components

```bash
npm install -D vite-plugin-svgr
```

```typescript
import svgr from 'vite-plugin-svgr';

export default defineConfig({
  plugins: [react(), svgr()],
});
```

```tsx
import Logo from './logo.svg?react';

function App() {
  return <Logo className="logo" />;
}
```

### PWA

```bash
npm install -D vite-plugin-pwa
```

```typescript
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'My App',
        short_name: 'App',
        theme_color: '#ffffff',
        icons: [
          {
            src: '/icon-192.png',
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: '/icon-512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
    }),
  ],
});
```

### Compression

```bash
npm install -D vite-plugin-compression
```

```typescript
import viteCompression from 'vite-plugin-compression';

export default defineConfig({
  plugins: [
    react(),
    viteCompression({
      algorithm: 'gzip',
      ext: '.gz',
    }),
    viteCompression({
      algorithm: 'brotliCompress',
      ext: '.br',
    }),
  ],
});
```

## CSS

### CSS Modules

```css
/* Button.module.css */
.button {
  background: blue;
  color: white;
}
```

```tsx
import styles from './Button.module.css';

function Button() {
  return <button className={styles.button}>Click</button>;
}
```

### PostCSS

```javascript
// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### Sass/SCSS

```bash
npm install -D sass
```

```typescript
// vite.config.ts
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`,
      },
    },
  },
});
```

## Static Assets

### Import Assets

```typescript
// Import as URL
import imgUrl from './img.png';

// Import as string (inline)
import imgData from './img.png?inline';

// Import as raw string
import shaderCode from './shader.glsl?raw';
```

### Public Directory

Files in `public/` are served at root and copied as-is to build output.

```html
<!-- Access public/favicon.ico -->
<link rel="icon" href="/favicon.ico" />
```

## Build Optimization

### Code Splitting

```typescript
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
```

### Manual Chunks

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Split vendor code
          react: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
    },
  },
});
```

### Chunk Size Warnings

```typescript
export default defineConfig({
  build: {
    chunkSizeWarningLimit: 500, // KB
  },
});
```

### Analyze Bundle

```bash
npm install -D rollup-plugin-visualizer
```

```typescript
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({
      open: true,
      gzipSize: true,
    }),
  ],
});
```

## Library Mode

```typescript
// vite.config.ts (for building a library)
import { defineConfig } from 'vite';
import { resolve } from 'path';
import dts from 'vite-plugin-dts';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLib',
      fileName: 'my-lib',
      formats: ['es', 'cjs', 'umd'],
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
  plugins: [dts()],
});
```

## Testing

### Vitest Integration

```bash
npm install -D vitest
```

```typescript
// vite.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
});
```

## Commands

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  }
}
```

### Build for Different Modes

```bash
vite build --mode staging
vite build --mode production
```

## Best Practices

1. **Use path aliases** - Cleaner imports
2. **Split vendor chunks** - Better caching
3. **Lazy load routes** - Smaller initial bundle
4. **Enable source maps in dev** - Easier debugging
5. **Use SWC for React** - Faster builds

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing VITE_ prefix | Prefix env vars with VITE_ |
| Wrong import.meta usage | Use import.meta.env |
| Large chunks | Add manualChunks |
| Slow builds | Use @vitejs/plugin-react-swc |
| Missing types | Add env.d.ts |

## Reference Files

- [references/plugins.md](references/plugins.md) - Plugin ecosystem
- [references/optimization.md](references/optimization.md) - Build optimization
- [references/ssr.md](references/ssr.md) - Server-side rendering
