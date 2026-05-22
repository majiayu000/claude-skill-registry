# Vite Build Tool Skill

---
progressive_disclosure:
  entry_point:
    summary: "Lightning-fast build tool with instant HMR and ESM-first architecture for modern web development"
    when_to_use:
      - "When building React/Vue/Svelte/Preact applications"
      - "When needing instant HMR (Hot Module Replacement)"
      - "When migrating from webpack/CRA/Parcel"
      - "When setting up TypeScript projects with zero config"
      - "When building component libraries or UI frameworks"
    quick_start:
      - "npm create vite@latest my-app"
      - "Select framework: React/Vue/Svelte/Vanilla"
      - "cd my-app && npm install && npm run dev"
    essential_commands:
      - "vite: Start dev server with instant HMR"
      - "vite build: Production build with Rollup"
      - "vite preview: Preview production build locally"
  token_estimate:
    entry: 75
    full: 4000
---

## Core Concepts

### Why Vite?

**ESM-First Architecture**
- No bundling in development - serves native ESM
- Instant cold server start (no matter project size)
- Lightning-fast HMR that stays fast as app grows
- Rollup-based production builds with optimal code splitting

**Key Advantages**
- **Dev Speed**: 10-100x faster than webpack (no bundling)
- **Zero Config**: TypeScript, JSX, CSS modules out-of-box
- **Framework Agnostic**: React, Vue, Svelte, Preact, Lit
- **Plugin Ecosystem**: Rollup plugins + Vite-specific plugins
- **Modern by Default**: ESM, dynamic imports, top-level await

## Quick Start

### Create New Project

```bash
# Interactive creation
npm create vite@latest

# With template
npm create vite@latest my-app -- --template react-ts
npm create vite@latest my-app -- --template vue
npm create vite@latest my-app -- --template svelte-ts

# Available templates:
# vanilla, vanilla-ts
# react, react-ts, react-swc, react-swc-ts
# vue, vue-ts
# svelte, svelte-ts
# preact, preact-ts
# lit, lit-ts
```

### Essential Commands

```bash
# Development server (instant start)
npm run dev
vite --port 3000 --host 0.0.0.0

# Production build
npm run build
vite build --mode production

# Preview production build
npm run preview
vite preview --port 8080

# Clear cache (dependency pre-bundling)
rm -rf node_modules/.vite
```

## Configuration

### Basic vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],

  // Dev server
  server: {
    port: 3000,
    open: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },

  // Build options
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash-es', 'date-fns']
        }
      }
    }
  },

  // Path aliases
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@utils': '/src/utils'
    }
  }
});
```

### Framework-Specific Configs

**React + TypeScript + SWC**
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [
    react({
      // Enable Fast Refresh
      fastRefresh: true,
      // SWC optimizations
      tsDecorators: true
    })
  ],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },

  build: {
    target: 'es2020',
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('react') || id.includes('react-dom')) {
              return 'react-vendor';
            }
            return 'vendor';
          }
        }
      }
    }
  }
});
```

**Vue 3 + TypeScript**
```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';

export default defineConfig({
  plugins: [
    vue(),
    vueJsx() // For JSX/TSX in Vue
  ],

  resolve: {
    alias: {
      '@': '/src',
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },

  // Vue-specific optimizations
  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia']
  }
});
```

**Svelte + TypeScript**
```typescript
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [
    svelte({
      compilerOptions: {
        dev: process.env.NODE_ENV !== 'production'
      },
      hot: {
        preserveLocalState: true
      }
    })
  ],

  build: {
    target: 'es2020',
    minify: 'esbuild'
  }
});
```

## Environment Variables

### .env Files

```bash
# .env (loaded in all cases)
VITE_APP_TITLE=My App

# .env.local (local overrides, gitignored)
VITE_API_KEY=secret-key

# .env.development
VITE_API_URL=http://localhost:8000

# .env.production
VITE_API_URL=https://api.production.com
```

### Usage in Code

```typescript
// TypeScript: Define env types
interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string;
  readonly VITE_API_URL: string;
  readonly VITE_API_KEY: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

// Access variables (MUST start with VITE_)
console.log(import.meta.env.VITE_API_URL);
console.log(import.meta.env.MODE); // 'development' or 'production'
console.log(import.meta.env.DEV); // boolean
console.log(import.meta.env.PROD); // boolean
```

### vite-env.d.ts

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string;
  readonly VITE_API_URL: string;
  readonly VITE_API_KEY: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## Plugin Ecosystem

### Official Plugins

```bash
# React
npm install -D @vitejs/plugin-react          # Babel-based
npm install -D @vitejs/plugin-react-swc      # SWC-based (faster)

# Vue
npm install -D @vitejs/plugin-vue
npm install -D @vitejs/plugin-vue-jsx

# Svelte
npm install -D @sveltejs/vite-plugin-svelte

# Legacy browser support
npm install -D @vitejs/plugin-legacy
```

### Essential Community Plugins

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tsconfigPaths from 'vite-tsconfig-paths';
import { VitePWA } from 'vite-plugin-pwa';
import compression from 'vite-plugin-compression';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),

    // TypeScript paths from tsconfig.json
    tsconfigPaths(),

    // PWA support
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'My App',
        short_name: 'App',
        theme_color: '#ffffff'
      }
    }),

    // Gzip/Brotli compression
    compression({
      algorithm: 'brotliCompress',
      ext: '.br'
    }),

    // Bundle size visualization
    visualizer({
      open: true,
      gzipSize: true,
      brotliSize: true
    })
  ]
});
```

## TypeScript Configuration

### tsconfig.json for Vite

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### tsconfig.node.json (for config files)

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

## CSS & Asset Handling

### CSS Modules

```typescript
// Component.module.css
.button {
  background: blue;
  color: white;
}

// Component.tsx
import styles from './Component.module.css';

export function Button() {
  return <button className={styles.button}>Click</button>;
}
```

### PostCSS Configuration

```javascript
// postcss.config.js
export default {
  plugins: {
    'postcss-nesting': {},
    'autoprefixer': {},
    'cssnano': {
      preset: 'default'
    }
  }
};
```

### Sass/SCSS

```bash
npm install -D sass
```

```typescript
// Just import - Vite handles it
import './styles.scss';

// Vite config for global variables
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
});
```

### Static Assets

```typescript
// Import as URL
import imgUrl from './assets/logo.png';
console.log(imgUrl); // '/assets/logo.abc123.png'

// Import as string (raw)
import svgRaw from './icon.svg?raw';
console.log(svgRaw); // '<svg>...</svg>'

// Import as Web Worker
import Worker from './worker?worker';
const worker = new Worker();

// Public directory (not processed)
// public/favicon.ico → /favicon.ico
<img src="/favicon.ico" />
```

## Build Optimization

### Code Splitting

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Manual chunks for better caching
        manualChunks(id) {
          if (id.includes('node_modules')) {
            // Split by package
            if (id.includes('react') || id.includes('react-dom')) {
              return 'react-vendor';
            }
            if (id.includes('@mui')) {
              return 'mui-vendor';
            }
            if (id.includes('lodash')) {
              return 'lodash-vendor';
            }
            return 'vendor';
          }
        },

        // Naming patterns
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]'
      }
    },

    // Chunk size warnings
    chunkSizeWarningLimit: 1000,

    // Minification
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
});
```

### Dependency Pre-bundling

```typescript
export default defineConfig({
  optimizeDeps: {
    // Force include (for dynamic imports)
    include: [
      'react',
      'react-dom',
      'lodash-es'
    ],

    // Force exclude (keep unbundled)
    exclude: [
      'your-local-package'
    ],

    // esbuild options
    esbuildOptions: {
      target: 'es2020',
      define: {
        global: 'globalThis'
      }
    }
  }
});
```

### Library Mode

```typescript
// Build as library/package
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/index.ts'),
      name: 'MyLibrary',
      fileName: (format) => `my-library.${format}.js`,
      formats: ['es', 'cjs', 'umd']
    },

    rollupOptions: {
      // Externalize deps that shouldn't be bundled
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
      }
    }
  }
});
```

## Migration Guides

### From Create React App (CRA)

```bash
# 1. Remove CRA
npm uninstall react-scripts

# 2. Install Vite
npm install -D vite @vitejs/plugin-react

# 3. Update package.json scripts
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

```typescript
// 4. Create vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  },
  build: {
    outDir: 'build' // CRA uses 'build'
  }
});
```

```html
<!-- 5. Update index.html (move to root, remove %PUBLIC_URL%) -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

```typescript
// 6. Update environment variables
// CRA: REACT_APP_API_URL
// Vite: VITE_API_URL

// Before (CRA)
process.env.REACT_APP_API_URL

// After (Vite)
import.meta.env.VITE_API_URL
```

### From Webpack

```typescript
// webpack.config.js → vite.config.ts

// Webpack concepts → Vite equivalents:
// - entry → index.html + <script src="main.tsx">
// - output.path → build.outDir
// - resolve.alias → resolve.alias (same!)
// - module.rules → plugins (for file types)
// - optimization.splitChunks → build.rollupOptions.output.manualChunks
// - DefinePlugin → define config option
// - devServer → server config
```

## SSR (Server-Side Rendering)

### Basic SSR Setup

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    // SSR build
    ssr: true,
    outDir: 'dist/server'
  }
});
```

```typescript
// server.ts (Express + Vite SSR)
import express from 'express';
import { createServer as createViteServer } from 'vite';

async function createServer() {
  const app = express();

  const vite = await createViteServer({
    server: { middlewareMode: true },
    appType: 'custom'
  });

  app.use(vite.middlewares);

  app.use('*', async (req, res) => {
    const url = req.originalUrl;

    try {
      // Load template
      let template = await vite.transformIndexHtml(
        url,
        fs.readFileSync('index.html', 'utf-8')
      );

      // Load SSR entry
      const { render } = await vite.ssrLoadModule('/src/entry-server.tsx');

      // Render app
      const appHtml = await render(url);

      // Inject into template
      const html = template.replace(`<!--ssr-outlet-->`, appHtml);

      res.status(200).set({ 'Content-Type': 'text/html' }).end(html);
    } catch (e) {
      vite.ssrFixStacktrace(e);
      res.status(500).end(e.stack);
    }
  });

  app.listen(3000);
}

createServer();
```

## Performance Best Practices

### Dev Server Optimization

```typescript
export default defineConfig({
  server: {
    // Faster dependency resolution
    fs: {
      strict: false,
      allow: ['..']
    },

    // WebSocket connection
    hmr: {
      overlay: true,
      clientPort: 3000
    }
  },

  // Faster pre-bundling
  optimizeDeps: {
    force: false, // Only rebuild on deps change
    include: ['large-dependencies']
  },

  // Faster transforms
  esbuild: {
    logOverride: { 'this-is-undefined-in-esm': 'silent' }
  }
});
```

### Build Performance

```typescript
export default defineConfig({
  build: {
    // Faster builds (esbuild vs terser)
    minify: 'esbuild',

    // Disable source maps in production
    sourcemap: false,

    // Target modern browsers only
    target: 'es2020',

    // Reduce rollup overhead
    rollupOptions: {
      cache: true
    },

    // Report compressed size (slower but informative)
    reportCompressedSize: false
  }
});
```

### Smart Code Splitting

```typescript
// Dynamic imports for route-based splitting
const Home = lazy(() => import('./pages/Home'));
const About = lazy(() => import('./pages/About'));

// Component-level splitting
const HeavyChart = lazy(() => import('./components/HeavyChart'));

// Conditional loading
const AdminPanel = lazy(() =>
  import(/* @vite-ignore */ './admin/Panel')
);
```

## Debugging

### Common Issues

**Issue: Module not found**
```bash
# Clear dependency cache
rm -rf node_modules/.vite
npm install
```

**Issue: HMR not working**
```typescript
// Check vite.config.ts
export default defineConfig({
  server: {
    hmr: {
      overlay: true
    },
    watch: {
      usePolling: true // For Docker/WSL
    }
  }
});
```

**Issue: Build errors but dev works**
```bash
# Check for:
# - TypeScript errors (tsc --noEmit)
# - Import paths (case sensitivity)
# - Missing dependencies in package.json
```

### Debug Mode

```bash
# Verbose logging
DEBUG=vite:* vite

# Specific debug scopes
DEBUG=vite:deps vite
DEBUG=vite:hmr vite
DEBUG=vite:config vite
```

## Advanced Patterns

### Multi-page App

```typescript
import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        admin: resolve(__dirname, 'admin/index.html'),
        docs: resolve(__dirname, 'docs/index.html')
      }
    }
  }
});
```

### Custom Plugin

```typescript
import { Plugin } from 'vite';

export function myPlugin(): Plugin {
  return {
    name: 'my-plugin',

    // Transform code
    transform(code, id) {
      if (id.endsWith('.custom')) {
        return {
          code: transformCode(code),
          map: null
        };
      }
    },

    // Handle HMR
    handleHotUpdate({ file, server }) {
      if (file.endsWith('.custom')) {
        server.ws.send({
          type: 'custom',
          event: 'update'
        });
      }
    },

    // Modify config
    config(config, env) {
      return {
        define: {
          __BUILD_TIME__: JSON.stringify(new Date().toISOString())
        }
      };
    }
  };
}
```

### Monorepo Support

```typescript
// packages/app/vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  resolve: {
    alias: {
      '@shared': '../../packages/shared/src'
    }
  },

  optimizeDeps: {
    include: [
      '@workspace/shared' // Pre-bundle workspace deps
    ]
  },

  server: {
    fs: {
      allow: ['../..'] // Allow serving from monorepo root
    }
  }
});
```

## Integration Examples

### Vite + React + TypeScript + Tailwind

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```typescript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### Vite + Testing (Vitest)

```bash
npm install -D vitest @testing-library/react jsdom
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html']
    }
  }
});
```

## Quick Reference

### Essential Configuration Options

```typescript
export default defineConfig({
  // Base public path
  base: '/my-app/',

  // Modes: 'development' | 'production'
  mode: 'production',

  // Define global constants
  define: {
    __APP_VERSION__: JSON.stringify('1.0.0')
  },

  // Public directory
  publicDir: 'public',

  // Cache directory
  cacheDir: 'node_modules/.vite',

  // Log level
  logLevel: 'info' // 'info' | 'warn' | 'error' | 'silent'
});
```

### Common Plugin Combinations

```typescript
// React + TypeScript + PWA + Analytics
import react from '@vitejs/plugin-react-swc';
import { VitePWA } from 'vite-plugin-pwa';
import tsconfigPaths from 'vite-tsconfig-paths';

export default defineConfig({
  plugins: [
    react(),
    tsconfigPaths(),
    VitePWA({
      registerType: 'autoUpdate'
    })
  ]
});
```

## Related Skills

When using Vite, consider these complementary skills (available in the skill library):

- **React**: React framework integration - use Vite's optimized React plugin for fast development
- **Vue**: Vue framework integration - leverage Vite's native Vue support and SFC compilation
- **Svelte**: Svelte framework integration - combine Svelte's compile-time optimizations with Vite's speed
- **TypeScript**: TypeScript configuration - configure TypeScript with Vite for type-safe development
- **Vitest**: Testing with Vite - use Vitest for lightning-fast unit testing with Vite's transform pipeline

## Resources

**Official Documentation**
- Vite Guide: https://vitejs.dev/guide/
- Config Reference: https://vitejs.dev/config/
- Plugin API: https://vitejs.dev/guide/api-plugin.html

**Community**
- Awesome Vite: https://github.com/vitejs/awesome-vite
- Vite Rollup Plugins: https://vite-rollup-plugins.patak.dev/

**Migration Tools**
- CRA to Vite: https://github.com/vitejs/vite/discussions/3802
- Webpack to Vite: https://github.com/originjs/webpack-to-vite