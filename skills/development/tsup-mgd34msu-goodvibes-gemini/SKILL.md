---
name: tsup
description: Configures tsup for zero-config TypeScript library bundling with ESM/CJS output, declarations, and esbuild speed. Use when building TypeScript packages, creating dual ESM/CJS libraries, or publishing to npm.
---

# tsup

Zero-config TypeScript bundler powered by esbuild for fast library builds.

## Quick Start

```bash
npm install --save-dev tsup typescript

# Bundle with defaults
npx tsup src/index.ts

# ESM and CJS with declarations
npx tsup src/index.ts --format esm,cjs --dts

# Watch mode
npx tsup src/index.ts --watch
```

## Configuration

### tsup.config.ts

```typescript
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  sourcemap: true,
  clean: true,
  minify: true,
  target: 'es2020',
  outDir: 'dist',
});
```

### Multiple Entry Points

```typescript
export default defineConfig({
  entry: {
    index: 'src/index.ts',
    utils: 'src/utils/index.ts',
    cli: 'src/cli.ts',
  },
  format: ['esm', 'cjs'],
  dts: true,
});
```

### Conditional Config

```typescript
export default defineConfig((options) => ({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  minify: !options.watch,
  sourcemap: options.watch,
  clean: !options.watch,
}));
```

## package.json Setup

### Modern Dual Package

```json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.mts",
        "default": "./dist/index.mjs"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    }
  },
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsup",
    "dev": "tsup --watch",
    "prepublishOnly": "npm run build"
  }
}
```

### CLI Package

```json
{
  "name": "my-cli",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "my-cli": "./dist/cli.js"
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsup src/cli.ts --format esm --target node18"
  }
}
```

## Configuration Options

### Entry

```typescript
export default defineConfig({
  // Single entry
  entry: ['src/index.ts'],

  // Multiple entries
  entry: ['src/index.ts', 'src/cli.ts'],

  // Named entries
  entry: {
    index: 'src/index.ts',
    cli: 'src/cli.ts',
  },

  // Glob patterns
  entry: ['src/**/*.ts'],
});
```

### Output Formats

```typescript
export default defineConfig({
  format: [
    'esm',  // ES modules (.mjs)
    'cjs',  // CommonJS (.cjs)
    'iife', // Browser global
  ],

  // Global name for IIFE
  globalName: 'MyLibrary',
});
```

### TypeScript Declarations

```typescript
export default defineConfig({
  dts: true,

  // Or with options
  dts: {
    resolve: true, // Resolve external types
    entry: 'src/index.ts',
    compilerOptions: {
      strict: true,
    },
  },

  // Only declarations (no JS)
  dts: { only: true },
});
```

### Bundling

```typescript
export default defineConfig({
  // Bundle dependencies (default: false)
  bundle: true,

  // External packages (not bundled)
  external: ['react', 'react-dom', /^@radix-ui/],

  // Don't bundle any dependencies
  noExternal: [],

  // Skip node_modules
  skipNodeModulesBundle: true,
});
```

### Code Splitting

```typescript
export default defineConfig({
  entry: ['src/index.ts', 'src/utils.ts'],
  format: ['esm'],

  // Enable code splitting
  splitting: true,

  // Chunk naming
  chunkNames: '[name]-[hash]',
});
```

### Minification

```typescript
export default defineConfig({
  minify: true,

  // Or use terser for better minification
  minify: 'terser',

  terserOptions: {
    compress: {
      drop_console: true,
    },
  },
});
```

### Target Environment

```typescript
export default defineConfig({
  // Browser targets
  target: ['es2020', 'chrome90', 'firefox88'],

  // Node.js target
  target: 'node18',

  // Platform
  platform: 'browser', // or 'node', 'neutral'
});
```

### Environment Variables

```typescript
export default defineConfig({
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },

  // Replace with env values
  env: {
    API_URL: 'https://api.example.com',
  },
});
```

## Advanced Features

### Shims

```typescript
export default defineConfig({
  // Add shims for ESM/CJS interop
  shims: true,

  // CJS interop for __dirname, require, etc.
  cjsInterop: true,
});
```

### Banner/Footer

```typescript
export default defineConfig({
  banner: {
    js: '/* My Library v1.0.0 */',
    css: '/* Styles */',
  },

  footer: {
    js: '/* End of bundle */',
  },
});
```

### CLI Shebang

```typescript
export default defineConfig({
  entry: ['src/cli.ts'],
  format: ['esm'],

  // Add shebang for CLI
  banner: {
    js: '#!/usr/bin/env node',
  },
});
```

### Inject

```typescript
export default defineConfig({
  // Auto-import React
  inject: ['./react-shim.js'],
});

// react-shim.js
import * as React from 'react';
export { React };
```

### Source Maps

```typescript
export default defineConfig({
  sourcemap: true, // External .map files
  // sourcemap: 'inline', // Inline source maps
});
```

### Watch Mode

```typescript
export default defineConfig({
  watch: ['src/**/*.ts'],

  // Ignore patterns
  ignoreWatch: ['**/*.test.ts', 'node_modules'],

  // Callback on rebuild
  onSuccess: 'node dist/index.js',
});
```

### esbuild Plugins

```typescript
export default defineConfig({
  esbuildPlugins: [
    {
      name: 'my-plugin',
      setup(build) {
        build.onLoad({ filter: /\.txt$/ }, async (args) => {
          return {
            contents: `export default ${JSON.stringify(await fs.readFile(args.path, 'utf8'))}`,
            loader: 'js',
          };
        });
      },
    },
  ],

  // esbuild options
  esbuildOptions(options) {
    options.jsx = 'automatic';
    options.jsxImportSource = 'react';
  },
});
```

### Custom Loaders

```typescript
export default defineConfig({
  loader: {
    '.png': 'file',
    '.svg': 'dataurl',
    '.json': 'json',
  },
});
```

## Common Patterns

### React Library

```typescript
export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  sourcemap: true,
  clean: true,

  // Don't bundle React
  external: ['react', 'react-dom'],

  // JSX
  esbuildOptions(options) {
    options.jsx = 'automatic';
  },
});
```

### Node.js Package

```typescript
export default defineConfig({
  entry: ['src/index.ts'],
  format: ['esm', 'cjs'],
  dts: true,
  target: 'node18',
  platform: 'node',
  clean: true,

  // Don't bundle native modules
  external: ['fsevents'],
});
```

### CLI with Dependencies

```typescript
export default defineConfig({
  entry: ['src/cli.ts'],
  format: ['esm'],
  target: 'node18',
  platform: 'node',

  // Bundle everything for standalone CLI
  noExternal: [/.*/],

  // Shebang
  banner: {
    js: '#!/usr/bin/env node',
  },

  minify: true,
});
```

### Multiple Configs

```typescript
export default defineConfig([
  // Main library
  {
    entry: ['src/index.ts'],
    format: ['esm', 'cjs'],
    dts: true,
  },
  // CLI
  {
    entry: ['src/cli.ts'],
    format: ['esm'],
    banner: { js: '#!/usr/bin/env node' },
  },
]);
```

## CLI Commands

```bash
# Basic build
tsup src/index.ts

# With options
tsup src/index.ts --format esm,cjs --dts --minify

# Watch mode
tsup src/index.ts --watch

# Clean before build
tsup src/index.ts --clean

# Specific outDir
tsup src/index.ts --out-dir lib

# Run command on success
tsup src/index.ts --watch --onSuccess "node dist/index.js"
```

See [references/options.md](references/options.md) for complete option reference.
