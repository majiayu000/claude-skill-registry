---
name: Bun Bundler
description: This skill should be used when the user asks about "bun build", "Bun.build", "bundling with Bun", "code splitting", "tree shaking", "minification", "sourcemaps", "bundle optimization", "esbuild alternative", "building for production", "bundling TypeScript", "bundling for browser", "bundling for Node", or JavaScript/TypeScript bundling with Bun.
version: 1.0.0
---

# Bun Bundler

Bun's bundler is a fast JavaScript/TypeScript bundler built on the same engine as Bun's runtime. It's an esbuild-compatible alternative with native performance.

## Quick Start

### CLI

```bash
# Basic bundle
bun build ./src/index.ts --outdir ./dist

# Production build
bun build ./src/index.ts --outdir ./dist --minify

# Multiple entry points
bun build ./src/index.ts ./src/worker.ts --outdir ./dist
```

### JavaScript API

```typescript
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
});

if (!result.success) {
  console.error("Build failed:", result.logs);
}
```

## Bun.build Options

```typescript
await Bun.build({
  // Entry points (required)
  entrypoints: ["./src/index.ts"],

  // Output directory
  outdir: "./dist",

  // Target environment
  target: "browser",  // "browser" | "bun" | "node"

  // Output format
  format: "esm",  // "esm" | "cjs" | "iife"

  // Minification
  minify: true,  // or { whitespace: true, identifiers: true, syntax: true }

  // Code splitting
  splitting: true,

  // Source maps
  sourcemap: "external",  // "none" | "inline" | "external" | "linked"

  // Naming patterns
  naming: {
    entry: "[dir]/[name].[ext]",
    chunk: "[name]-[hash].[ext]",
    asset: "[name]-[hash].[ext]",
  },

  // Define globals
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },

  // External packages
  external: ["react", "react-dom"],

  // Loaders
  loader: {
    ".svg": "text",
    ".png": "file",
  },

  // Plugins
  plugins: [myPlugin],

  // Root directory
  root: "./src",

  // Public path for assets
  publicPath: "/static/",
});
```

## CLI Flags

```bash
bun build <entrypoints> [flags]
```

| Flag | Description |
|------|-------------|
| `--outdir` | Output directory |
| `--outfile` | Output single file |
| `--target` | `browser`, `bun`, `node` |
| `--format` | `esm`, `cjs`, `iife` |
| `--minify` | Enable minification |
| `--minify-whitespace` | Minify whitespace only |
| `--minify-identifiers` | Minify identifiers only |
| `--minify-syntax` | Minify syntax only |
| `--splitting` | Enable code splitting |
| `--sourcemap` | `none`, `inline`, `external`, `linked` |
| `--external` | Mark packages as external |
| `--define` | Define compile-time constants |
| `--loader` | Custom loaders for extensions |
| `--public-path` | Public path for assets |
| `--root` | Root directory |
| `--entry-naming` | Entry point naming pattern |
| `--chunk-naming` | Chunk naming pattern |
| `--asset-naming` | Asset naming pattern |

## Target Environments

### Browser (default)

```typescript
await Bun.build({
  entrypoints: ["./src/index.ts"],
  target: "browser",
  outdir: "./dist",
});
```

### Bun Runtime

```typescript
await Bun.build({
  entrypoints: ["./src/server.ts"],
  target: "bun",
  outdir: "./dist",
});
```

### Node.js

```typescript
await Bun.build({
  entrypoints: ["./src/server.ts"],
  target: "node",
  outdir: "./dist",
});
```

## Code Splitting

```typescript
await Bun.build({
  entrypoints: ["./src/index.ts", "./src/admin.ts"],
  splitting: true,
  outdir: "./dist",
});
```

Shared dependencies are extracted into separate chunks automatically.

## Loaders

| Loader | Extensions | Output |
|--------|------------|--------|
| `js` | `.js`, `.mjs`, `.cjs` | JavaScript |
| `jsx` | `.jsx` | JavaScript |
| `ts` | `.ts`, `.mts`, `.cts` | JavaScript |
| `tsx` | `.tsx` | JavaScript |
| `json` | `.json` | JavaScript |
| `toml` | `.toml` | JavaScript |
| `text` | - | String export |
| `file` | - | File path export |
| `base64` | - | Base64 string |
| `dataurl` | - | Data URL |
| `css` | `.css` | CSS file |

Custom loaders:

```typescript
await Bun.build({
  entrypoints: ["./src/index.ts"],
  loader: {
    ".svg": "text",
    ".png": "file",
    ".woff2": "file",
  },
});
```

## Plugins

```typescript
const myPlugin = {
  name: "my-plugin",
  setup(build) {
    // Resolve hook
    build.onResolve({ filter: /\.special$/ }, (args) => {
      return { path: args.path, namespace: "special" };
    });

    // Load hook
    build.onLoad({ filter: /.*/, namespace: "special" }, (args) => {
      return {
        contents: `export default "special"`,
        loader: "js",
      };
    });
  },
};

await Bun.build({
  entrypoints: ["./src/index.ts"],
  plugins: [myPlugin],
});
```

## Build Output

```typescript
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
});

// Check success
if (!result.success) {
  for (const log of result.logs) {
    console.error(log);
  }
  process.exit(1);
}

// Access outputs
for (const output of result.outputs) {
  console.log(output.path);   // File path
  console.log(output.kind);   // "entry-point" | "chunk" | "asset"
  console.log(output.hash);   // Content hash
  console.log(output.loader); // Loader used

  // Read content
  const text = await output.text();
}
```

## Common Patterns

### Production Build

```typescript
await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "browser",
  minify: true,
  sourcemap: "external",
  splitting: true,
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
});
```

### Library Build

```typescript
await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "bun",
  format: "esm",
  external: ["*"],  // Externalize all dependencies
  sourcemap: "external",
});
```

### Build Script

```typescript
// build.ts
const result = await Bun.build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  minify: process.env.NODE_ENV === "production",
});

if (!result.success) {
  console.error("Build failed");
  process.exit(1);
}

console.log(`Built ${result.outputs.length} files`);
```

Run: `bun run build.ts`

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Could not resolve` | Missing import | Install package or fix path |
| `No matching export` | Named export missing | Check export name |
| `Unexpected token` | Syntax error | Fix source code |
| `Target not supported` | Invalid target | Use `browser`, `bun`, or `node` |

## When to Load References

Load `references/options.md` when:
- Need complete option reference
- Configuring advanced features

Load `references/plugins.md` when:
- Writing custom plugins
- Understanding plugin API

Load `references/macros.md` when:
- Using compile-time macros
- Build-time code generation
