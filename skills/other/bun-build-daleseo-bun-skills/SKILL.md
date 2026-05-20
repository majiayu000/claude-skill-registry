---
name: bun-build
description: Create optimized production bundles with Bun's native bundler. Use when building applications for production, optimizing bundle sizes, setting up multi-environment builds, or replacing webpack/esbuild/rollup.
compatibility: Requires Bun 1.0+
allowed-tools: ["Bash", "Write", "Read"]
metadata:
  author: dale
  category: bun-runtime
  tags: [bun, build, bundler, production, optimization]
---

# Bun Production Build Configuration

Set up production builds using Bun's native bundler - fast, optimized bundle creation without webpack or esbuild.

## Quick Reference

For detailed patterns, see:
- **Build Targets**: [targets.md](references/targets.md) - Browser, Node.js, library, CLI configurations
- **Optimization**: [optimization.md](references/optimization.md) - Tree shaking, code splitting, analysis
- **Plugins**: [plugins.md](references/plugins.md) - Custom loaders and transformations

## Core Workflow

### 1. Check Prerequisites

```bash
# Verify Bun installation
bun --version

# Check project structure
ls -la package.json src/
```

### 2. Determine Build Requirements

Ask the user about their build needs:

- **Application Type**: Frontend SPA, Node.js backend, CLI tool, or library
- **Target Platform**: Browser, Node.js, Bun runtime, or Cloudflare Workers
- **Output Format**: ESM (modern), CommonJS (legacy), or both

### 3. Create Basic Build Script

Create `build.ts` in project root:

```typescript
#!/usr/bin/env bun

const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser', // or 'node', 'bun'
  format: 'esm', // or 'cjs', 'iife'
  minify: true,
  splitting: true,
  sourcemap: 'external',
});

if (!result.success) {
  console.error('Build failed');
  for (const message of result.logs) {
    console.error(message);
  }
  process.exit(1);
}

console.log('✅ Build successful');
console.log(`📦 ${result.outputs.length} files generated`);

// Show bundle sizes
for (const output of result.outputs) {
  const size = (output.size / 1024).toFixed(2);
  console.log(`  ${output.path} - ${size} KB`);
}
```

### 4. Configure for Target Platform

**For Browser/Frontend:**

```typescript
await Bun.build({
  entrypoints: ['./src/index.tsx'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  minify: true,
  splitting: true,
  define: {
    'process.env.NODE_ENV': '"production"',
  },
  loader: {
    '.png': 'file',
    '.svg': 'dataurl',
    '.css': 'css',
  },
});
```

**For Node.js Backend:**

```typescript
await Bun.build({
  entrypoints: ['./src/server.ts'],
  outdir: './dist',
  target: 'node',
  format: 'esm',
  minify: true,
  external: ['*'], // Don't bundle node_modules
});
```

**For libraries, CLI tools, and other targets**, see [targets.md](references/targets.md).

### 5. Add Production Optimizations

```typescript
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',

  // Maximum minification
  minify: {
    whitespace: true,
    identifiers: true,
    syntax: true,
  },

  // Code splitting for optimal caching
  splitting: true,

  // Content hashing for cache busting
  naming: {
    entry: '[dir]/[name].[hash].[ext]',
    chunk: 'chunks/[name].[hash].[ext]',
    asset: 'assets/[name].[hash].[ext]',
  },

  // Source maps for debugging
  sourcemap: 'external',
});
```

For advanced optimizations (tree shaking, bundle analysis, size limits), see [optimization.md](references/optimization.md).

### 6. Environment-Specific Builds

Create `build-env.ts`:

```typescript
#!/usr/bin/env bun

const env = process.env.NODE_ENV || 'development';

const configs = {
  development: {
    minify: false,
    sourcemap: 'inline',
    define: {
      'process.env.NODE_ENV': '"development"',
      'process.env.API_URL': '"http://localhost:3000"',
    },
  },
  production: {
    minify: true,
    sourcemap: 'external',
    define: {
      'process.env.NODE_ENV': '"production"',
      'process.env.API_URL': '"https://api.example.com"',
    },
  },
};

const config = configs[env as keyof typeof configs];

const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  splitting: true,
  ...config,
});

if (!result.success) {
  console.error('❌ Build failed');
  process.exit(1);
}

console.log(`✅ ${env} build successful`);
```

Run with:
```bash
NODE_ENV=production bun run build-env.ts
```

### 7. Update package.json

Add build scripts:

```json
{
  "scripts": {
    "build": "bun run build.ts",
    "build:dev": "NODE_ENV=development bun run build-env.ts",
    "build:prod": "NODE_ENV=production bun run build-env.ts",
    "build:watch": "bun run build.ts --watch",
    "clean": "rm -rf dist"
  }
}
```

**For libraries**, also add:

```json
{
  "type": "module",
  "main": "./dist/cjs/index.js",
  "module": "./dist/esm/index.js",
  "types": "./dist/esm/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js",
      "types": "./dist/esm/index.d.ts"
    }
  },
  "files": ["dist"]
}
```

### 8. Generate Type Declarations (Libraries)

For libraries, generate TypeScript declarations:

```typescript
// build-lib-with-types.ts
import { $ } from 'bun';

// Build JavaScript
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'node',
  format: 'esm',
  minify: true,
});

// Generate type declarations
await $`bunx tsc --declaration --emitDeclarationOnly --outDir dist`;

console.log('✅ Built library with type declarations');
```

## Build Options Reference

### Target

- **`browser`**: For web applications (includes browser globals)
- **`node`**: For Node.js applications (assumes Node.js APIs)
- **`bun`**: For Bun runtime (optimized for Bun-specific features)

### Format

- **`esm`**: ES Modules (modern, tree-shakeable) - Recommended
- **`cjs`**: CommonJS (legacy Node.js)
- **`iife`**: Immediately Invoked Function Expression (browser scripts)

### Minification

```typescript
minify: true                  // Basic minification
minify: {                     // Granular control
  whitespace: true,
  identifiers: true,
  syntax: true,
}
```

### Source Maps

- **`external`**: Separate .map files (production)
- **`inline`**: Inline in bundle (development)
- **`none`**: No source maps

## Verification

After building:

```bash
# 1. Check output directory
ls -lh dist/

# 2. Verify bundle size
du -sh dist/*

# 3. Test bundle
bun run dist/index.js

# 4. Check for errors
echo $?  # Should be 0
```

## Common Build Patterns

**Watch mode for development:**

```typescript
import { watch } from 'fs';

async function build() {
  await Bun.build({
    entrypoints: ['./src/index.ts'],
    outdir: './dist',
    minify: false,
  });
}

await build();

watch('./src', { recursive: true }, async (event, filename) => {
  if (filename?.endsWith('.ts')) {
    console.log(`Rebuilding...`);
    await build();
  }
});
```

**Custom asset loaders:**

```typescript
loader: {
  '.png': 'file',     // Copy file, return path
  '.svg': 'dataurl',  // Inline as data URL
  '.txt': 'text',     // Inline as string
  '.json': 'json',    // Parse and inline
}
```

**For custom plugins and advanced transformations**, see [plugins.md](references/plugins.md).

## Troubleshooting

**Build fails:**
```typescript
if (!result.success) {
  for (const log of result.logs) {
    console.error(log);
  }
}
```

**Bundle too large:**
See [optimization.md](references/optimization.md) for:
- Bundle analysis
- Code splitting
- Tree shaking
- Size limits

**Module not found:**
Check `external` configuration:
```typescript
external: ['*']         // Exclude all node_modules
external: ['react']     // Exclude specific packages
external: []            // Bundle everything
```

## Completion Checklist

- ✅ Build script created
- ✅ Target platform configured
- ✅ Minification enabled
- ✅ Source maps configured
- ✅ Environment-specific builds set up
- ✅ Package.json scripts added
- ✅ Build tested successfully
- ✅ Bundle size verified

## Next Steps

After basic build setup:

1. **Optimization**: Add bundle analysis and size limits
2. **CI/CD**: Automate builds in your pipeline
3. **Type Checking**: Add pre-build type checking
4. **Testing**: Run tests before building
5. **Deployment**: Integrate with bun-deploy for containerization

For detailed implementations, see the reference files linked above.
