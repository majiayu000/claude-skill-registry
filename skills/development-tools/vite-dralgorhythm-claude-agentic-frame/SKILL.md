---
name: vite
description: Vite 7.x build tool patterns. Use when configuring build setup, development server, environment variables, asset handling, or optimizing production builds for React applications.
---

# Vite

> **Platform:** Web only. Mobile demos use Expo with Metro bundler. See the **expo-sdk** skill.

## Overview

Build tool and development server patterns for Vite 7.x. Provides instant server start, lightning-fast HMR, optimized production builds, and extensive plugin ecosystem with first-class TypeScript support.

**Install**: `pnpm add -D vite`

## Workflows

**Initial setup:**
1. [ ] Create `vite.config.ts` with TypeScript types
2. [ ] Install React plugin: `pnpm add -D @vitejs/plugin-react`
3. [ ] Configure path aliases for clean imports
4. [ ] Set up environment variables with `.env` files
5. [ ] Test dev server: `pnpm vite`

**Production optimization:**
1. [ ] Configure build output directory and asset handling
2. [ ] Set up code splitting and chunk optimization
3. [ ] Enable build compression (gzip/brotli)
4. [ ] Configure minification options
5. [ ] Run production build: `pnpm vite build`
6. [ ] Preview build locally: `pnpm vite preview`

## Basic Configuration

### Minimal vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true
  },
  build: {
    outDir: 'dist'
  }
});
```

### TypeScript-Aware Config

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'node:path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@types': path.resolve(__dirname, './src/types')
    }
  }
});
```

**Update tsconfig.json paths to match:**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@utils/*": ["./src/utils/*"],
      "@types/*": ["./src/types/*"]
    }
  }
}
```

## React Plugin Setup

### Basic React Plugin

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react({
      // Babel plugins for React (optional)
      babel: {
        plugins: [
          // Add custom babel plugins here
        ]
      }
    })
  ]
});
```

**Note**: Fast Refresh is enabled by default in `@vitejs/plugin-react`. No configuration needed.

### React with SWC (Faster Alternative)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

export default defineConfig({
  plugins: [
    react({
      // SWC plugins
      plugins: [
        // Add SWC plugins here
      ]
    })
  ]
});
```

## Environment Variables

### .env File Structure

```bash
# .env - Base config (committed)
VITE_APP_NAME=Demo Harness
VITE_API_VERSION=v1

# .env.local - Local overrides (gitignored)
VITE_API_URL=http://localhost:3000

# .env.development - Dev defaults
VITE_DEBUG=true
VITE_API_URL=http://dev.example.com

# .env.production - Production defaults
VITE_DEBUG=false
VITE_API_URL=https://api.example.com
```

**CRITICAL**: All env vars must start with `VITE_` to be exposed to client code.

### Using Environment Variables

```typescript
// ✅ Accessing env vars in code
const apiUrl = import.meta.env.VITE_API_URL;
const isDev = import.meta.env.DEV;
const isProd = import.meta.env.PROD;
const mode = import.meta.env.MODE; // 'development' | 'production'

// Type-safe env vars
interface ImportMetaEnv {
  readonly VITE_APP_NAME: string;
  readonly VITE_API_URL: string;
  readonly VITE_API_VERSION: string;
  readonly VITE_DEBUG: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

// ❌ NEVER commit secrets to .env files
// Use .env.local for API keys and credentials
```

### Configuring Environment Variables

```typescript
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  // Load env file based on mode
  const env = loadEnv(mode, process.cwd(), '');

  return {
    define: {
      // Expose non-VITE_ prefixed vars
      __APP_VERSION__: JSON.stringify(env.npm_package_version)
    },
    server: {
      port: Number(env.PORT) || 5173
    }
  };
});
```

## Development Server

### Basic Server Configuration

```typescript
export default defineConfig({
  server: {
    port: 5173,
    strictPort: true, // Exit if port is already in use
    open: true, // Open browser on server start
    cors: true, // Enable CORS

    // Hot Module Replacement
    hmr: {
      overlay: true // Show error overlay
    },

    // File watching
    watch: {
      // Ignore dotfiles
      ignored: ['**/.*']
    }
  }
});
```

### Proxy Configuration for API

```typescript
export default defineConfig({
  server: {
    proxy: {
      // Proxy API requests to backend
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },

      // WebSocket proxy
      '/ws': {
        target: 'ws://localhost:3000',
        ws: true
      },

      // Multiple backends
      '/v1': {
        target: 'http://localhost:3001',
        changeOrigin: true
      },
      '/v2': {
        target: 'http://localhost:3002',
        changeOrigin: true
      }
    }
  }
});
```

### HTTPS Development Server

```typescript
import { defineConfig } from 'vite';
import fs from 'node:fs';

export default defineConfig({
  server: {
    https: {
      key: fs.readFileSync('./.cert/key.pem'),
      cert: fs.readFileSync('./.cert/cert.pem')
    }
  }
});
```

## Build Optimization

### Code Splitting and Chunking

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Manual chunk splitting
        manualChunks: {
          // Vendor chunks
          'react-vendor': ['react', 'react-dom'],
          'router-vendor': ['react-router-dom'],
          'animation-vendor': ['framer-motion'],

          // Feature-based chunks
          'dashboard': ['./src/components/views/DashboardView.tsx'],
          'reports': ['./src/components/views/ReportsView.tsx']
        },

        // Asset file naming
        assetFileNames: 'assets/[name]-[hash][extname]',
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js'
      }
    },

    // Chunk size warnings
    chunkSizeWarningLimit: 500, // KB

    // Minification
    minify: 'esbuild', // 'terser' | 'esbuild'

    // Source maps
    sourcemap: true, // or 'inline' | 'hidden'

    // Target browsers
    target: 'esnext', // or 'es2015', 'es2020', etc.

    // CSS code splitting
    cssCodeSplit: true
  }
});
```

### Advanced Chunking Strategy

```typescript
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          // All node_modules in vendor chunk
          if (id.includes('node_modules')) {
            // Split large vendors
            if (id.includes('framer-motion')) {
              return 'vendor-animation';
            }
            if (id.includes('react') || id.includes('react-dom')) {
              return 'vendor-react';
            }
            return 'vendor';
          }

          // Component-based splitting
          if (id.includes('/components/views/')) {
            const viewName = id.split('/components/views/')[1].split('.')[0];
            return `view-${viewName.toLowerCase()}`;
          }
        }
      }
    }
  }
});
```

### Compression and Minification

```typescript
import { defineConfig } from 'vite';
import { compression } from 'vite-plugin-compression2';

// Install: pnpm add -D vite-plugin-compression2
export default defineConfig({
  plugins: [
    // Gzip compression
    compression({
      algorithm: 'gzip',
      include: /\.(js|css|html|svg)$/
    }),

    // Brotli compression
    compression({
      algorithm: 'brotliCompress',
      include: /\.(js|css|html|svg)$/
    })
  ],

  build: {
    // esbuild is faster, terser produces smaller output
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
        drop_debugger: true
      }
    }
  }
});
```

## CSS and Styling

### PostCSS and Tailwind Integration

```typescript
// vite.config.ts
export default defineConfig({
  css: {
    postcss: './postcss.config.js',

    // CSS modules configuration
    modules: {
      localsConvention: 'camelCase',
      scopeBehaviour: 'local'
    },

    // Preprocessor options
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
});
```

```javascript
// postcss.config.js
export default {
  plugins: {
    'tailwindcss': {},
    'autoprefixer': {}
  }
};
```

### CSS Code Splitting

```typescript
export default defineConfig({
  build: {
    cssCodeSplit: true, // Split CSS per chunk

    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          // Organize CSS files
          if (assetInfo.name?.endsWith('.css')) {
            return 'css/[name]-[hash][extname]';
          }
          return 'assets/[name]-[hash][extname]';
        }
      }
    }
  }
});
```

## Static Assets

### Asset Handling Patterns

```typescript
// Importing assets (returns URL string)
import logo from './assets/logo.png';
import styles from './styles.module.css';

// Explicit URL imports
import assetUrl from './asset.png?url';

// Raw content import
import rawSvg from './icon.svg?raw';

// Worker import
import Worker from './worker?worker';

// JSON import
import data from './data.json';
```

### Public Directory

```
/public
  /images
    logo.svg
  /fonts
    custom-font.woff2
  favicon.ico
```

```typescript
// Public assets are served at root and NOT processed
// Reference with absolute path
<img src="/images/logo.svg" alt="Logo" />

// ❌ Don't import from public
// import logo from '/public/images/logo.svg'; // Wrong!

// ✅ Import from src/assets for processing
import logo from '@/assets/logo.svg'; // Correct
```

### Asset Configuration

```typescript
export default defineConfig({
  // Public base path
  base: '/', // or '/my-app/' for subdirectory hosting

  publicDir: 'public', // Default

  build: {
    assetsDir: 'assets', // Output directory for assets
    assetsInlineLimit: 4096, // Inline assets < 4kb as base64

    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.');
          const ext = info[info.length - 1];

          // Organize by file type
          if (/png|jpe?g|svg|gif|webp|ico/i.test(ext)) {
            return 'images/[name]-[hash][extname]';
          }
          if (/woff2?|ttf|otf|eot/i.test(ext)) {
            return 'fonts/[name]-[hash][extname]';
          }
          return 'assets/[name]-[hash][extname]';
        }
      }
    }
  }
});
```

## Preview Mode

### Preview Production Build

```typescript
export default defineConfig({
  preview: {
    port: 4173,
    strictPort: true,
    open: true,

    // Proxy config (same as dev server)
    proxy: {
      '/api': 'http://localhost:3000'
    },

    // CORS
    cors: true,

    // Headers
    headers: {
      'Cache-Control': 'public, max-age=31536000'
    }
  }
});
```

**Commands:**
```bash
# Build for production
pnpm vite build

# Preview production build locally
pnpm vite preview

# Preview on specific port
pnpm vite preview --port 8080
```

## Vite 7 Notes

Vite 7.x introduces:
- **Rolldown** - New bundler written in Rust for faster builds (optional)
- Improved TypeScript support
- Better tree-shaking
- Enhanced HMR performance

For demos, the default configuration works well. Advanced bundler options are not typically needed.

## Complete Production Config

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { compression } from 'vite-plugin-compression2';
import path from 'node:path';

export default defineConfig(({ mode }) => {
  const isDev = mode === 'development';

  return {
    plugins: [
      react(),
      // Compression for production (requires vite-plugin-compression2)
      !isDev && compression({ algorithm: 'gzip', include: /\.(js|css|html|svg)$/ }),
      !isDev && compression({ algorithm: 'brotliCompress', include: /\.(js|css|html|svg)$/ })
    ].filter(Boolean),

    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@components': path.resolve(__dirname, './src/components'),
        '@hooks': path.resolve(__dirname, './src/hooks'),
        '@utils': path.resolve(__dirname, './src/utils'),
        '@types': path.resolve(__dirname, './src/types')
      }
    },

    server: {
      port: 5173,
      strictPort: true,
      open: true,
      hmr: {
        overlay: true
      },
      proxy: {
        '/api': {
          target: 'http://localhost:3000',
          changeOrigin: true
        }
      }
    },

    build: {
      outDir: 'dist',
      sourcemap: !isDev,
      minify: isDev ? false : 'terser',
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      },
      rollupOptions: {
        output: {
          manualChunks: {
            'react-vendor': ['react', 'react-dom'],
            'router-vendor': ['react-router-dom'],
            'animation-vendor': ['framer-motion']
          },
          assetFileNames: (assetInfo) => {
            const info = assetInfo.name.split('.');
            const ext = info[info.length - 1];
            if (/png|jpe?g|svg|gif|webp|ico/i.test(ext)) {
              return 'images/[name]-[hash][extname]';
            }
            if (/woff2?|ttf|otf|eot/i.test(ext)) {
              return 'fonts/[name]-[hash][extname]';
            }
            return 'assets/[name]-[hash][extname]';
          },
          chunkFileNames: 'js/[name]-[hash].js',
          entryFileNames: 'js/[name]-[hash].js'
        }
      },
      chunkSizeWarningLimit: 500
    },

    preview: {
      port: 4173,
      strictPort: true,
      open: true
    }
  };
});
```

## Best Practices

- **Use path aliases** for clean imports and avoid ../../../ hell
- **Prefix client env vars** with VITE_ for automatic exposure
- **Split large vendors** into separate chunks for better caching
- **Enable compression** for production builds (gzip + brotli)
- **Use .env.local** for secrets and never commit to git
- **Configure proxy** for API calls to avoid CORS in development
- **Preview builds locally** before deploying to catch issues
- **Organize assets** by type in build output for better CDN caching
- **Enable sourcemaps** in production for debugging (or use 'hidden')
- **Use esbuild** for faster builds, terser for smaller output
- **Set base path** correctly for subdirectory deployments
- **Test HMR** after config changes to ensure Fast Refresh works

## Anti-Patterns

- ❌ Forgetting VITE_ prefix on environment variables
- ❌ Importing from /public directory instead of src/assets
- ❌ Committing .env.local with API keys
- ❌ Not configuring path aliases (causes messy imports)
- ❌ Using terser in development (unnecessary slowdown)
- ❌ Disabling CSS code splitting for large apps
- ❌ Not setting strictPort (silent port conflicts)
- ❌ Ignoring chunk size warnings (impacts load time)
- ❌ Missing tsconfig.json paths when using aliases
- ❌ Hardcoding localhost URLs (use env vars)
- ❌ Not testing preview mode before deployment
- ❌ Placing all vendors in single chunk (defeats caching)
- ❌ Configuring proxy for demos (demos are static, no backend)

## Feedback Loops

**Dev server performance:**
```bash
# Check HMR speed
# Should be < 50ms for most updates
# Chrome DevTools → Network → Filter by "vite"
```

**Build analysis:**
```bash
# Analyze bundle size
pnpm vite build --mode production

# Output shows chunk sizes
# dist/js/vendor-react-abc123.js  142.34 kB
# dist/js/index-def456.js          87.21 kB
```

**Preview testing:**
```bash
# Always preview before deploying
pnpm vite build && pnpm vite preview

# Test:
# - All routes work
# - Assets load correctly
# - API proxy works (if configured)
# - No console errors
```

**Environment validation:**
```typescript
// Add runtime checks for required env vars
if (!import.meta.env.VITE_API_URL) {
  throw new Error('VITE_API_URL is required');
}
```
