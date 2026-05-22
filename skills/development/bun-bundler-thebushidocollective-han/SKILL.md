---
name: jutsu-bun:bun-bundler
description: Use when bundling JavaScript/TypeScript code with Bun's fast bundler. Covers building for different targets, tree-shaking, code splitting, and optimization strategies.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Bun Bundler

Use this skill when bundling JavaScript/TypeScript applications with Bun's built-in bundler, which provides exceptional performance and modern features.

## Key Concepts

### Basic Bundling

Bun can bundle your code for different targets:

```bash
# Bundle for Bun runtime
bun build ./src/index.ts --outdir ./dist

# Bundle for browsers
bun build ./src/index.ts --outdir ./dist --target=browser

# Bundle for Node.js
bun build ./src/index.ts --outdir ./dist --target=node

# Minify output
bun build ./src/index.ts --outdir ./dist --minify
```

### Programmatic API

Use Bun's build API in TypeScript:

```typescript
import { build } from "bun";

await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  target: "bun",
  minify: true,
  sourcemap: "external",
});
```

### Build Targets

Bun supports multiple build targets:

- `bun` - Optimized for Bun runtime (default)
- `browser` - Browser-compatible bundle
- `node` - Node.js-compatible bundle

### Output Formats

Control output format:

```typescript
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  format: "esm", // or "cjs", "iife"
});
```

## Best Practices

### Entry Points Configuration

Define multiple entry points for complex applications:

```typescript
await build({
  entrypoints: [
    "./src/client/index.ts",
    "./src/server/index.ts",
    "./src/worker.ts",
  ],
  outdir: "./dist",
  naming: {
    entry: "[dir]/[name].[ext]",
    chunk: "[name]-[hash].[ext]",
    asset: "assets/[name]-[hash].[ext]",
  },
});
```

### Tree Shaking

Bun automatically tree-shakes unused code:

```typescript
// utils.ts
export function used() {
  return "used";
}

export function unused() {
  return "unused";
}

// index.ts
import { used } from "./utils";

console.log(used()); // Only 'used' function will be bundled
```

### Code Splitting

Split code for better loading performance:

```typescript
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  splitting: true, // Enable code splitting
  target: "browser",
});
```

### Environment Variables

Replace environment variables at build time:

```typescript
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  define: {
    "process.env.API_URL": JSON.stringify("https://api.example.com"),
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
});
```

### External Dependencies

Mark dependencies as external to exclude from bundle:

```typescript
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  external: ["react", "react-dom"], // Don't bundle React
  target: "browser",
});
```

### Source Maps

Generate source maps for debugging:

```typescript
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  sourcemap: "external", // or "inline", "none"
  minify: true,
});
```

## Common Patterns

### Building a Library

```typescript
// build.ts
import { build } from "bun";

// ESM build
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist/esm",
  format: "esm",
  target: "node",
  minify: true,
  sourcemap: "external",
});

// CJS build
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist/cjs",
  format: "cjs",
  target: "node",
  minify: true,
  sourcemap: "external",
});

console.log("Build complete!");
```

### Building a Web Application

```typescript
// build.ts
import { build } from "bun";

await build({
  entrypoints: ["./src/index.tsx"],
  outdir: "./dist",
  target: "browser",
  format: "esm",
  minify: true,
  splitting: true,
  sourcemap: "external",
  publicPath: "/assets/",
  naming: {
    entry: "[dir]/[name].[ext]",
    chunk: "[name]-[hash].[ext]",
    asset: "assets/[name]-[hash].[ext]",
  },
  define: {
    "process.env.NODE_ENV": JSON.stringify("production"),
  },
});
```

### Building Multiple Outputs

```typescript
// build.ts
import { build } from "bun";

const builds = [
  {
    entrypoints: ["./src/index.ts"],
    outdir: "./dist/esm",
    format: "esm" as const,
    target: "browser" as const,
  },
  {
    entrypoints: ["./src/index.ts"],
    outdir: "./dist/cjs",
    format: "cjs" as const,
    target: "node" as const,
  },
  {
    entrypoints: ["./src/index.ts"],
    outdir: "./dist/iife",
    format: "iife" as const,
    target: "browser" as const,
  },
];

for (const config of builds) {
  await build({
    ...config,
    minify: true,
    sourcemap: "external",
  });
}

console.log("All builds complete!");
```

### Build Script with Watching

```typescript
// watch-build.ts
import { watch } from "fs";
import { build } from "bun";

async function buildApp() {
  console.log("Building...");
  await build({
    entrypoints: ["./src/index.ts"],
    outdir: "./dist",
    target: "bun",
  });
  console.log("Build complete!");
}

// Initial build
await buildApp();

// Watch for changes
watch("./src", { recursive: true }, async (event, filename) => {
  console.log(`File changed: ${filename}`);
  await buildApp();
});
```

### Plugin System

Create custom build plugins:

```typescript
import type { BunPlugin } from "bun";

const myPlugin: BunPlugin = {
  name: "my-plugin",
  setup(build) {
    build.onLoad({ filter: /\.custom$/ }, async (args) => {
      const text = await Bun.file(args.path).text();
      return {
        contents: `export default ${JSON.stringify(text)}`,
        loader: "js",
      };
    });
  },
};

await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  plugins: [myPlugin],
});
```

## Anti-Patterns

### Don't Bundle Node Modules for Node Target

```typescript
// Bad - Bundling all dependencies for Node
await build({
  entrypoints: ["./src/server.ts"],
  target: "node",
  // Missing external configuration
});

// Good - Mark dependencies as external
await build({
  entrypoints: ["./src/server.ts"],
  target: "node",
  external: ["express", "mongoose", "*"], // "*" excludes all node_modules
});
```

### Don't Ignore Build Errors

```typescript
// Bad - No error handling
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
});

// Good - Handle build errors
try {
  const result = await build({
    entrypoints: ["./src/index.ts"],
    outdir: "./dist",
  });

  if (!result.success) {
    console.error("Build failed");
    process.exit(1);
  }

  console.log("Build succeeded");
} catch (error) {
  console.error("Build error:", error);
  process.exit(1);
}
```

### Don't Minify Development Builds

```typescript
// Bad - Always minifying
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  minify: true, // Hard to debug in development
});

// Good - Conditional minification
const isDev = Bun.env.NODE_ENV === "development";

await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  minify: !isDev,
  sourcemap: isDev ? "inline" : "external",
});
```

### Don't Over-Split Code

```typescript
// Bad - Excessive code splitting
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  splitting: true,
  target: "bun", // Code splitting not needed for Bun target
});

// Good - Split only when beneficial
await build({
  entrypoints: ["./src/index.ts"],
  outdir: "./dist",
  splitting: true,
  target: "browser", // Beneficial for browsers
});
```

## Related Skills

- **bun-runtime**: Understanding Bun's runtime for target optimization
- **bun-package-manager**: Managing build dependencies
- **bun-testing**: Testing bundled code
