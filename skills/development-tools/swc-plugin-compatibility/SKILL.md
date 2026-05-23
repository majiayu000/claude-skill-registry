---
name: swc-plugin-compatibility
description: Diagnose and fix Lingui SWC plugin compatibility errors with Next.js, Rspack, or other SWC runtimes. Use when seeing errors like "failed to invoke plugin", "failed to run Wasm plugin transform", "out of bounds memory access", or "LayoutError" during builds with @lingui/swc-plugin.
---

# SWC Plugin Compatibility

If you see errors like these during your build:

```
failed to invoke plugin on 'Some("/app/src/file.ts")'
failed to run Wasm plugin transform
RuntimeError: out of bounds memory access
LayoutError called Result::unwrap()
```

**This is NOT a bug.** You're using an incompatible version of `@lingui/swc-plugin` with your SWC runtime.

## Why This Happens

SWC plugin support is experimental. The plugin API does not follow semantic versioning.

SWC uses Rkyv to transfer the AST between the core and plugins. Both must agree on the exact memory layout of the AST. If the layout changes (e.g., new ECMAScript features), older plugins cannot read the data correctly.

This layout cannot be negotiated at runtime—it must match at compile time.

## How to Fix

### Step 1: Check the Compatibility Table

Go to the [compatibility table](https://github.com/lingui/swc-plugin?tab=readme-ov-file#compatibility) and find the plugin version that matches your runtime.

### Step 2: Use the Plugin Compatibility Site

For precise matching, use https://plugins.swc.rs/:

1. Select your runtime (e.g., `next`)
2. Select your runtime version (e.g., `next@15.0.1`)
3. Find a compatible `@lingui/swc-plugin` version

### Step 3: Pin Your Versions

```json
{
  "devDependencies": {
    "@lingui/swc-plugin": "5.10.0"
  }
}
```

Use an **exact version** (no `^` or `~`) to prevent accidental upgrades.

## Version Compatibility Quick Reference

| Plugin Version | @lingui/core | Notes |
|----------------|--------------|-------|
| `5.*` | `@lingui/core@5.*` | Current |
| `4.*` | `@lingui/core@4.*` | Legacy |

**Important**: `@lingui/swc-plugin` does not need to match other `@lingui/*` package versions exactly. It follows its own versioning scheme.

## Rules to Avoid Build Breakage

1. **Pin an exact plugin version** compatible with your runtime
2. **Don't auto-bump `@lingui/swc-plugin`** — check release notes first
3. **Don't auto-bump your runtime** (Next.js, Rspack, etc.) — runtimes may bump `swc-core` in minor/patch releases
4. **Check compatibility after any upgrade** that touches SWC or the plugin

## Understanding Runtimes

By "runtime" we mean the tool executing SWC: Next.js, Rspack, or `@swc/core`.

Some runtimes (like Next.js) embed SWC directly and don't use `@swc/core` from npm. This means:

- You cannot control `swc-core` version via `package.json`
- Plugin compatibility depends on the runtime's embedded SWC version

## Example: Next.js Configuration

```js
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    swcPlugins: [
      ['@lingui/swc-plugin', {
        // Plugin options
      }],
    ],
  },
};

module.exports = nextConfig;
```

## Example: .swcrc Configuration

```json
{
  "$schema": "https://json.schemastore.org/swcrc",
  "jsc": {
    "experimental": {
      "plugins": [
        ["@lingui/swc-plugin", {}]
      ]
    }
  }
}
```

## What If No Compatible Version Exists?

If your runtime uses a newer `swc-core` that no plugin version supports yet:

1. Check for recent plugin releases
2. Open an issue or PR at https://github.com/lingui/swc-plugin
