---
name: rollup
description: Configures Rollup for ES module bundling with plugins, tree shaking, and multiple output formats. Use when building JavaScript libraries, creating optimized bundles, or publishing npm packages.
---

# Rollup

Next-generation ES module bundler optimized for libraries and tree shaking.

## Quick Start

```bash
npm install --save-dev rollup

# Simple bundle
npx rollup src/index.js --file dist/bundle.js --format esm

# With config
npx rollup -c
```

## Configuration

### rollup.config.js

```javascript
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import typescript from '@rollup/plugin-typescript';
import terser from '@rollup/plugin-terser';

export default {
  input: 'src/index.ts',

  output: [
    {
      file: 'dist/bundle.esm.js',
      format: 'esm',
      sourcemap: true,
    },
    {
      file: 'dist/bundle.cjs.js',
      format: 'cjs',
      sourcemap: true,
    },
    {
      file: 'dist/bundle.umd.js',
      format: 'umd',
      name: 'MyLibrary',
      sourcemap: true,
    },
  ],

  plugins: [
    resolve(),
    commonjs(),
    typescript({ tsconfig: './tsconfig.json' }),
    terser(),
  ],

  external: ['react', 'react-dom'],
};
```

### Multiple Entry Points

```javascript
export default {
  input: {
    main: 'src/index.ts',
    utils: 'src/utils/index.ts',
    hooks: 'src/hooks/index.ts',
  },

  output: {
    dir: 'dist',
    format: 'esm',
    entryFileNames: '[name].js',
    chunkFileNames: 'chunks/[name]-[hash].js',
  },
};
```

## Output Formats

### ESM (ES Modules)

```javascript
output: {
  file: 'dist/bundle.mjs',
  format: 'es', // or 'esm'
}
```

### CommonJS

```javascript
output: {
  file: 'dist/bundle.cjs',
  format: 'cjs',
  exports: 'auto', // 'default', 'named', 'none', 'auto'
}
```

### UMD (Universal)

```javascript
output: {
  file: 'dist/bundle.umd.js',
  format: 'umd',
  name: 'MyLibrary', // Global variable name
  globals: {
    react: 'React',
    'react-dom': 'ReactDOM',
  },
}
```

### IIFE (Browser)

```javascript
output: {
  file: 'dist/bundle.js',
  format: 'iife',
  name: 'MyLibrary',
}
```

## Essential Plugins

### Install Core Plugins

```bash
npm install --save-dev @rollup/plugin-node-resolve @rollup/plugin-commonjs @rollup/plugin-typescript @rollup/plugin-terser @rollup/plugin-json
```

### Node Resolve

Resolve node_modules imports:

```javascript
import resolve from '@rollup/plugin-node-resolve';

plugins: [
  resolve({
    browser: true, // Prefer browser field
    preferBuiltins: false, // Don't prefer Node.js builtins
    extensions: ['.js', '.ts', '.tsx'],
  }),
]
```

### CommonJS

Convert CommonJS to ESM:

```javascript
import commonjs from '@rollup/plugin-commonjs';

plugins: [
  commonjs({
    include: /node_modules/,
    requireReturnsDefault: 'auto',
  }),
]
```

### TypeScript

```javascript
import typescript from '@rollup/plugin-typescript';

plugins: [
  typescript({
    tsconfig: './tsconfig.json',
    declaration: true,
    declarationDir: 'dist/types',
  }),
]
```

### Terser (Minification)

```javascript
import terser from '@rollup/plugin-terser';

plugins: [
  terser({
    compress: {
      drop_console: true,
    },
    format: {
      comments: false,
    },
  }),
]
```

### JSON

```javascript
import json from '@rollup/plugin-json';

plugins: [json()]
```

### Replace

```javascript
import replace from '@rollup/plugin-replace';

plugins: [
  replace({
    preventAssignment: true,
    'process.env.NODE_ENV': JSON.stringify('production'),
  }),
]
```

## Library Build Pattern

### package.json

```json
{
  "name": "my-library",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.cjs",
  "module": "dist/index.mjs",
  "types": "dist/types/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/types/index.d.ts"
    },
    "./utils": {
      "import": "./dist/utils.mjs",
      "require": "./dist/utils.cjs"
    }
  },
  "files": ["dist"],
  "sideEffects": false,
  "scripts": {
    "build": "rollup -c",
    "dev": "rollup -c -w"
  },
  "peerDependencies": {
    "react": ">=18"
  }
}
```

### rollup.config.js for Library

```javascript
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import typescript from '@rollup/plugin-typescript';
import terser from '@rollup/plugin-terser';
import peerDepsExternal from 'rollup-plugin-peer-deps-external';
import { dts } from 'rollup-plugin-dts';

const production = !process.env.ROLLUP_WATCH;

export default [
  // Main bundle
  {
    input: 'src/index.ts',
    output: [
      {
        file: 'dist/index.mjs',
        format: 'esm',
        sourcemap: true,
      },
      {
        file: 'dist/index.cjs',
        format: 'cjs',
        sourcemap: true,
      },
    ],
    plugins: [
      peerDepsExternal(),
      resolve(),
      commonjs(),
      typescript({ tsconfig: './tsconfig.json' }),
      production && terser(),
    ],
  },
  // Type declarations
  {
    input: 'dist/types/index.d.ts',
    output: { file: 'dist/index.d.ts', format: 'es' },
    plugins: [dts()],
  },
];
```

## Code Splitting

### Dynamic Imports

```javascript
// In your code
const module = await import('./heavy-module.js');
```

```javascript
// rollup.config.js
export default {
  input: 'src/index.js',
  output: {
    dir: 'dist',
    format: 'esm',
    chunkFileNames: 'chunks/[name]-[hash].js',
  },
  // Enable code splitting
  preserveEntrySignatures: false,
};
```

### Manual Chunks

```javascript
output: {
  dir: 'dist',
  format: 'esm',
  manualChunks: {
    vendor: ['react', 'react-dom'],
    utils: ['lodash', 'date-fns'],
  },
}

// Or with function
output: {
  manualChunks(id) {
    if (id.includes('node_modules')) {
      return 'vendor';
    }
  },
}
```

## External Dependencies

```javascript
export default {
  input: 'src/index.ts',
  output: { file: 'dist/bundle.js', format: 'esm' },

  // Don't bundle these
  external: [
    'react',
    'react-dom',
    /^@radix-ui/,
    /^lodash/,
  ],
};
```

## Watch Mode

```bash
# Watch for changes
npx rollup -c -w

# With specific config
npx rollup -c rollup.config.dev.js -w
```

```javascript
// rollup.config.js
export default {
  // ...
  watch: {
    include: 'src/**',
    exclude: 'node_modules/**',
    clearScreen: false,
  },
};
```

## Tree Shaking

Tree shaking is automatic for ES modules:

```javascript
// Mark side effects in package.json
{
  "sideEffects": false
}

// Or specify files with side effects
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/polyfills.js"
  ]
}
```

```javascript
// In rollup.config.js
export default {
  treeshake: {
    moduleSideEffects: false,
    propertyReadSideEffects: false,
    tryCatchDeoptimization: false,
  },
};
```

## Source Maps

```javascript
output: {
  file: 'dist/bundle.js',
  format: 'esm',
  sourcemap: true, // Generate .map file
  // sourcemap: 'inline', // Inline source map
  // sourcemap: 'hidden', // Generate but don't reference
}
```

## CLI Options

```bash
# Basic
rollup -c                    # Use rollup.config.js
rollup -c rollup.prod.js     # Specific config
rollup -i src/index.js       # Input file
rollup -o dist/bundle.js     # Output file
rollup -f esm                # Format

# Watching
rollup -c -w                 # Watch mode

# Environment
rollup -c --environment NODE_ENV:production
```

Access in config:

```javascript
export default {
  // process.env.NODE_ENV is available
  plugins: [
    process.env.NODE_ENV === 'production' && terser(),
  ].filter(Boolean),
};
```

See [references/plugins.md](references/plugins.md) for complete plugin catalog and [references/patterns.md](references/patterns.md) for common configuration patterns.
