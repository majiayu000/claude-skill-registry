---
name: bun
description: Configures Bun as an all-in-one JavaScript runtime, bundler, package manager, and test runner with native TypeScript support. Use when building fast applications, bundling for production, or replacing Node.js tooling.
---

# Bun

All-in-one JavaScript runtime, bundler, package manager, and test runner written in Zig.

## Quick Start

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Or with npm
npm install -g bun

# Run TypeScript directly
bun run src/index.ts

# Install packages
bun install

# Bundle for production
bun build src/index.ts --outdir=dist
```

## Runtime

### Running Files

```bash
# Run TypeScript/JavaScript
bun run index.ts
bun run index.js
bun run index.jsx
bun run index.tsx

# Run package.json scripts
bun run dev
bun run build

# Shorthand for run
bun dev
bun build
```

### Watch Mode

```bash
# Auto-restart on changes
bun --watch run index.ts

# Hot reload (preserves state)
bun --hot run index.ts
```

### Environment Variables

```bash
# Load .env automatically
bun run index.ts

# Specify env file
bun --env-file=.env.local run index.ts

# No env file
bun --no-env-file run index.ts
```

## Package Manager

### Install Packages

```bash
# Install all dependencies
bun install

# Add package
bun add express
bun add -D typescript

# Add exact version
bun add react@18.2.0

# Global install
bun add -g typescript
```

### Remove/Update

```bash
# Remove package
bun remove lodash

# Update packages
bun update
bun update react
```

### Lock File

```bash
# Generate/update bun.lockb
bun install

# Frozen install (CI)
bun install --frozen-lockfile

# Convert to yarn.lock
bun pm pack
```

## Bundler

### Basic Bundling

```bash
# Bundle for browser
bun build src/index.ts --outdir=dist

# Single file output
bun build src/index.ts --outfile=dist/bundle.js

# Minify
bun build src/index.ts --outdir=dist --minify

# Source maps
bun build src/index.ts --outdir=dist --sourcemap=external
```

### Build API

```typescript
// build.ts
const result = await Bun.build({
  entrypoints: ['./src/index.tsx'],
  outdir: './dist',
  minify: true,
  sourcemap: 'external',
  target: 'browser',
  splitting: true,
  format: 'esm',
});

if (!result.success) {
  console.error('Build failed:', result.logs);
  process.exit(1);
}

console.log('Build complete!', result.outputs);
```

### Bundle Options

```typescript
await Bun.build({
  entrypoints: ['./src/index.ts', './src/worker.ts'],
  outdir: './dist',

  // Target
  target: 'browser', // 'browser' | 'bun' | 'node'

  // Format
  format: 'esm', // 'esm' | 'cjs' | 'iife'

  // Optimization
  minify: {
    whitespace: true,
    identifiers: true,
    syntax: true,
  },
  sourcemap: 'external', // 'none' | 'inline' | 'external' | 'linked'

  // Code splitting
  splitting: true,

  // Naming
  naming: {
    entry: '[dir]/[name].[ext]',
    chunk: 'chunks/[name]-[hash].[ext]',
    asset: 'assets/[name]-[hash].[ext]',
  },

  // Externals
  external: ['react', 'react-dom'],

  // Define
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },

  // Loaders
  loader: {
    '.png': 'file',
    '.svg': 'dataurl',
  },

  // Public path
  publicPath: '/assets/',

  // Plugins
  plugins: [],
});
```

### Plugins

```typescript
const myPlugin = {
  name: 'my-plugin',
  setup(build) {
    // Resolve hook
    build.onResolve({ filter: /^env$/ }, (args) => {
      return { path: args.path, namespace: 'env-ns' };
    });

    // Load hook
    build.onLoad({ filter: /.*/, namespace: 'env-ns' }, () => {
      return {
        contents: `export const API = "${process.env.API_URL}"`,
        loader: 'js',
      };
    });
  },
};

await Bun.build({
  entrypoints: ['./src/index.ts'],
  plugins: [myPlugin],
});
```

## Test Runner

### Running Tests

```bash
# Run all tests
bun test

# Specific file
bun test src/utils.test.ts

# Pattern matching
bun test --test-name-pattern "should handle"

# Watch mode
bun test --watch

# Coverage
bun test --coverage
```

### Writing Tests

```typescript
// math.test.ts
import { describe, test, expect, beforeEach, mock } from 'bun:test';

describe('math', () => {
  test('adds numbers', () => {
    expect(1 + 2).toBe(3);
  });

  test('async operations', async () => {
    const result = await fetchData();
    expect(result).toBeDefined();
  });
});

// Mocking
const mockFn = mock(() => 42);
mockFn();
expect(mockFn).toHaveBeenCalled();

// Spying
import * as module from './module';
const spy = spyOn(module, 'someFunction');
```

### Test Configuration

```typescript
// bunfig.toml
[test]
root = "./tests"
timeout = 5000
preload = ["./setup.ts"]
coverage = true
coverageReporter = ["text", "lcov"]
```

## HTTP Server

### Bun.serve

```typescript
const server = Bun.serve({
  port: 3000,
  hostname: '0.0.0.0',

  fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === '/') {
      return new Response('Hello World!');
    }

    if (url.pathname === '/api/data') {
      return Response.json({ message: 'Hello' });
    }

    return new Response('Not Found', { status: 404 });
  },

  // WebSocket support
  websocket: {
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
    open(ws) {
      console.log('Client connected');
    },
    close(ws) {
      console.log('Client disconnected');
    },
  },
});

console.log(`Server running at http://localhost:${server.port}`);
```

### Static Files

```typescript
Bun.serve({
  port: 3000,

  async fetch(req) {
    const url = new URL(req.url);
    const filePath = `./public${url.pathname}`;

    const file = Bun.file(filePath);
    if (await file.exists()) {
      return new Response(file);
    }

    return new Response('Not Found', { status: 404 });
  },
});
```

## File System

### Reading Files

```typescript
// Read text
const text = await Bun.file('file.txt').text();

// Read JSON
const json = await Bun.file('data.json').json();

// Read ArrayBuffer
const buffer = await Bun.file('image.png').arrayBuffer();

// Check existence
const exists = await Bun.file('file.txt').exists();

// Get file info
const file = Bun.file('file.txt');
console.log(file.size, file.type);
```

### Writing Files

```typescript
// Write text
await Bun.write('output.txt', 'Hello World');

// Write JSON
await Bun.write('data.json', JSON.stringify(data, null, 2));

// Write Buffer
await Bun.write('output.bin', buffer);

// Append
const file = Bun.file('log.txt');
await Bun.write(file, await file.text() + '\nNew line');
```

## Shell Commands

```typescript
import { $ } from 'bun';

// Simple command
await $`echo "Hello World"`;

// With variables
const name = 'World';
await $`echo "Hello ${name}"`;

// Capture output
const result = await $`ls -la`.text();

// Check exit code
const { exitCode } = await $`npm test`.nothrow();

// Pipe commands
await $`cat file.txt | grep "pattern"`;

// Environment variables
await $`API_KEY=${key} node script.js`;
```

## Standalone Executables

```bash
# Compile to single executable
bun build --compile src/cli.ts --outfile my-cli

# Cross-compile
bun build --compile --target=bun-linux-x64 src/cli.ts
bun build --compile --target=bun-darwin-arm64 src/cli.ts
bun build --compile --target=bun-windows-x64 src/cli.ts
```

## Configuration

### bunfig.toml

```toml
# Package manager
[install]
registry = "https://registry.npmjs.org"
scope = { "@company" = "https://private.registry.com" }

# Bundler
[bundle]
entrypoints = ["./src/index.ts"]
outdir = "./dist"
minify = true
sourcemap = "external"

# Test runner
[test]
root = "./tests"
preload = ["./setup.ts"]
timeout = 5000

# Development server
[serve]
port = 3000
```

See [references/api.md](references/api.md) for complete API reference and [references/migration.md](references/migration.md) for Node.js migration guide.
