---
name: vite-config
description: Vite configuration patterns for React monorepo builds. Use when configuring builds, fixing bundling issues, or optimizing output.
license: MIT
---

# Vite Configuration

## When to Use

Activate when:

- Configuring new package builds
- Fixing "multiple React instances" errors
- Optimizing bundle size
- Adding code splitting
- Debugging build issues

## Project Vite Configs

| Package           | Config         | Plugin                     |
| ----------------- | -------------- | -------------------------- |
| webgl             | vite.config.js | react-swc                  |
| chat              | vite.config.js | react-swc                  |
| header-auth-links | vite.config.js | react-swc                  |
| testing           | vite.config.js | react-swc ✅ (best config) |
| website           | vite.config.js | react (standard)           |

## Standard Config Template

Use this for all packages:

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';
import { fileURLToPath } from 'url';
import pkg from './package.json';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '../..');

export default defineConfig({
  plugins: [react()],

  base: './',

  resolve: {
    alias: {
      // Force single React instance
      react: path.resolve(rootDir, 'node_modules/react'),
      'react-dom': path.resolve(rootDir, 'node_modules/react-dom'),
      'react/jsx-runtime': path.resolve(rootDir, 'node_modules/react/jsx-runtime'),
      'react/jsx-dev-runtime': path.resolve(rootDir, 'node_modules/react/jsx-dev-runtime'),
      // Shared package alias
      '@disruptive-spaces/shared': path.resolve(rootDir, 'packages/shared'),
    },
    dedupe: ['react', 'react-dom', 'framer-motion', '@chakra-ui/react', '@emotion/react'],
  },

  optimizeDeps: {
    include: ['react', 'react-dom', 'react/jsx-runtime'],
    force: true,
  },

  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      output: {
        entryFileNames: `assets/main.v${pkg.version}.js`,
        chunkFileNames: `assets/[name].v${pkg.version}.js`,
        assetFileNames: `assets/[name].v${pkg.version}.[ext]`,
      },
    },
  },
});
```

## React Deduplication (Critical)

### Why It's Needed

Without deduplication:

- Each package bundles its own React
- Hooks fail with "Invalid hook call"
- Context doesn't work across package boundaries
- `useState`, `useEffect` break silently

### Full Solution

```javascript
resolve: {
  alias: {
    // All React paths point to root node_modules
    'react': path.resolve(rootDir, 'node_modules/react'),
    'react-dom': path.resolve(rootDir, 'node_modules/react-dom'),
    'react/jsx-runtime': path.resolve(rootDir, 'node_modules/react/jsx-runtime'),
    'react/jsx-dev-runtime': path.resolve(rootDir, 'node_modules/react/jsx-dev-runtime'),
  },
  dedupe: ['react', 'react-dom', 'framer-motion', '@chakra-ui/react'],
},

optimizeDeps: {
  include: ['react', 'react-dom', 'react/jsx-runtime'],
  force: true,  // Rebuild on every dev start
},
```

## Code Splitting

```javascript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        // Vendor chunks
        'vendor-react': ['react', 'react-dom'],
        'vendor-chakra': ['@chakra-ui/react', '@emotion/react', 'framer-motion'],
        'vendor-agora': ['agora-rtc-sdk-ng', 'agora-rtc-react'],
        'vendor-firebase': ['firebase/app', 'firebase/firestore', 'firebase/auth'],
      },
    },
  },
},
```

## Library Mode (for shared packages)

```javascript
// packages/shared/vite.config.js
export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'index.js'),
      name: 'DisruptiveShared',
      formats: ['es', 'cjs'],
      fileName: (format) => `index.${format}.js`,
    },
    rollupOptions: {
      external: ['react', 'react-dom', 'firebase'],
    },
  },
});
```

## Environment Variables

```javascript
// vite.config.js
export default defineConfig({
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
  },

  envPrefix: ['VITE_', 'REACT_APP_'], // Expose these to client
});
```

Access in code:

```javascript
const apiKey = import.meta.env.VITE_API_KEY;
```

## Plugin: React SWC vs Babel

| Feature        | react-swc   | react (Babel)              |
| -------------- | ----------- | -------------------------- |
| Speed          | ~20x faster | Slower                     |
| Config         | Minimal     | Extensive                  |
| Plugins        | Limited     | Full Babel ecosystem       |
| Recommendation | ✅ Use this | Only if need Babel plugins |

```javascript
// Prefer this
import react from '@vitejs/plugin-react-swc';

// Only use if you need Babel plugins
import react from '@vitejs/plugin-react';
```

## Debugging Builds

```bash
# Analyze bundle
pnpm add -D rollup-plugin-visualizer

# In vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';

plugins: [
  react(),
  visualizer({ open: true }),
],
```

## Common Issues

| Issue          | Cause             | Fix                           |
| -------------- | ----------------- | ----------------------------- |
| Multiple React | Missing dedupe    | Add resolve.alias + dedupe    |
| Hooks error    | React not deduped | Check alias paths are correct |
| Missing styles | CSS not extracted | Add `cssCodeSplit: true`      |
| Large bundle   | No code splitting | Add `manualChunks`            |
| Slow HMR       | Large deps        | Add to `optimizeDeps.include` |

## Files to Update

When applying this config:

1. `packages/webgl/vite.config.js`
2. `packages/chat/vite.config.js`
3. `packages/header-auth-links/vite.config.js`
4. `packages/website/vite.config.js`

(testing package already has the best config - use as reference)

## Related Skills

- `monorepo-deps` - Dependency management
- `frontend-development` - React patterns
