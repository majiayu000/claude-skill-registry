---
name: web-tooling-vite
description: Vite config, path aliases, vendor chunk splitting, environment-specific builds, Rolldown codeSplitting, Sass modern API, build targets, module preload
---

# Vite Build Tool Patterns

> **Quick Guide:** Vite is the build tool for frontend apps. Keep path aliases in sync between `vite.config.ts` and `tsconfig.json` (or use `resolve.tsconfigPaths` in Vite 8). Use vendor chunk splitting (`manualChunks` in Vite 7, `codeSplitting.groups` in Vite 8). Use `loadEnv()` for environment-specific builds. Vite 8 uses Rolldown by default with `build.rolldownOptions`.
>
> **Current versions:** Vite 8 (stable, March 2026) with Rolldown bundler. Vite 7 (June 2025) still widely deployed.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST keep path aliases in sync between `vite.config.ts` and `tsconfig.json` - mismatches cause import resolution failures)**

**(You MUST use `build.rolldownOptions` in Vite 8+ - `build.rollupOptions` is a deprecated alias)**

**(You MUST use `codeSplitting.groups` for chunk splitting in Vite 8 - object-form `manualChunks` is removed, function-form deprecated)**

**(You MUST use `build.modulePreload.polyfill` instead of deprecated `build.polyfillModulePreload`)**

**(You MUST use Sass modern API (default in Vite 6+) - legacy API is removed in Vite 7+)**

</critical_requirements>

---

**Auto-detection:** Vite, vite.config.ts, vite.config.js, manualChunks, advancedChunks, codeSplitting, loadEnv, rolldownOptions, rollupOptions, modulePreload, resolve.alias, resolve.tsconfigPaths, build.target, baseline-widely-available

**When to use:**

- Configuring Vite build tool for frontend applications
- Setting up path aliases with tsconfig sync
- Vendor chunk splitting for production builds
- Environment-specific build configuration (dev/staging/prod)
- Migrating from Vite 7 (Rollup) to Vite 8 (Rolldown)
- Configuring module preload, build targets, or Sass preprocessing

**When NOT to use:**

- Server-side build processes (Docker builds, CI/CD pipelines)
- Linter or formatter configuration (separate tooling skill)
- TypeScript compiler options (separate tooling skill)

**Key patterns covered:**

- Path aliases with tsconfig sync (and Vite 8 `resolve.tsconfigPaths`)
- Vendor chunk splitting (`manualChunks` for Vite 7, `codeSplitting` for Vite 8)
- Environment-specific builds with `loadEnv` and `define`
- Module preload configuration
- Sass modern API configuration
- Environment API (experimental, primarily for framework authors)
- Build target selection (`baseline-widely-available`)

**Detailed resources:**

- [examples/core.md](examples/core.md) - Full code examples for all patterns
- [reference.md](reference.md) - Quick-lookup tables, migration checklist, external links

---

<philosophy>

## Philosophy

Vite should be **fast, zero-config by default, and environment-aware**. The build tool stays out of your way during development (instant HMR) and optimizes aggressively for production (chunk splitting, minification, tree-shaking).

**When to use this skill:**

- Configuring or optimizing Vite builds
- Setting up path aliases, chunk splitting, or environment configs
- Migrating between Vite major versions (7 to 8)
- Configuring Sass, build targets, or module preload

**When NOT to use:**

- Runtime application code (this is build-time configuration only)
- SSR meta-framework configuration (handled by meta-framework skills)
- CI/CD pipeline configuration

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Path Aliases

Configure path aliases in both `vite.config.ts` and `tsconfig.json` to eliminate deep relative imports. In Vite 8, use `resolve.tsconfigPaths: true` instead of manual `resolve.alias`.

```typescript
// Vite 7: manual resolve.alias
resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
    "@components": path.resolve(__dirname, "./src/components"),
  },
},

// Vite 8: built-in tsconfig path resolution
resolve: {
  tsconfigPaths: true, // reads from tsconfig.json automatically
},
```

**Key point:** `resolve.tsconfigPaths` is disabled by default (performance cost). Enable only if using tsconfig paths. See [examples/core.md](examples/core.md) for complete configs.

---

### Pattern 2: Vendor Chunk Splitting

Split vendor dependencies into separate chunks for better caching. API differs between Vite 7 and 8.

```typescript
// Vite 7: manualChunks (object form)
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        "vendor": ["react", "react-dom"],
      },
    },
  },
},

// Vite 8: codeSplitting.groups (regex-based)
build: {
  rolldownOptions: {
    output: {
      codeSplitting: {
        groups: [
          { name: "vendor", test: /[\\/]node_modules[\\/]react(-dom)?[\\/]/ },
        ],
      },
    },
  },
},
```

**Key point:** In Vite 8, object-form `manualChunks` is removed and function-form is deprecated. Rolldown generates a `runtime.js` chunk alongside code-split groups. See [examples/core.md](examples/core.md) for full examples.

---

### Pattern 3: Environment-Specific Builds

Use `loadEnv()` for environment-aware configuration and `define` for build-time constants.

```typescript
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },
    build: {
      sourcemap: mode === "development",
      minify: mode === "production",
    },
  };
});
```

**Key point:** The third argument to `loadEnv()` (`""`) loads all env vars, not just `VITE_`-prefixed ones. Use `--mode` flag for environment selection. See [examples/core.md](examples/core.md) for full config with scripts.

---

### Pattern 4: Module Preload Configuration

```typescript
build: {
  modulePreload: {
    polyfill: false, // disable for modern-only targets
    resolveDependencies: (filename, deps, { hostId, hostType }) => {
      return deps.filter((dep) => !dep.includes("large-vendor"));
    },
  },
},
```

**Key point:** `build.polyfillModulePreload` is deprecated. Use `build.modulePreload.polyfill` (current API since Vite 6).

---

### Pattern 5: Sass Configuration (Vite 6+)

```typescript
css: {
  preprocessorOptions: {
    scss: {
      // modern API is the default in Vite 6+ — no need to specify
      additionalData: `@use "@/styles/variables" as *;`,
    },
  },
},
```

**Key point:** Legacy API (`api: 'legacy'`) is removed in Vite 7+. Migrate `@import` to `@use`/`@forward` with namespaced access (`variables.$color-primary`).

---

### Pattern 6: Environment API (Experimental)

> Primarily for framework authors. Remains in RC phase as of Vite 8. Most apps do not need this.

```typescript
environments: {
  client: { build: { outDir: "dist/client" } },
  ssr: { build: { outDir: "dist/server", ssr: true } },
},
```

See [examples/core.md](examples/core.md) for full multi-environment config.

---

### Pattern 7: Dev Server Proxy

```typescript
const DEV_SERVER_PORT = 3000;
const API_PROXY_TARGET = "http://localhost:8000";

server: {
  port: DEV_SERVER_PORT,
  proxy: {
    "/api": { target: API_PROXY_TARGET, changeOrigin: true },
  },
},
```

</patterns>

---

<decision_framework>

## Decision Framework

### Vite Version Selection

```
Which Vite version?
├─ New project (March 2026+)?
│   └─ Vite 8 (Rolldown bundler, fastest builds) ✓
├─ Existing Vite 7 project?
│   ├─ Build performance is a bottleneck?
│   │   └─ YES → Migrate to Vite 8 (10-30x faster)
│   └─ NO → Stay on Vite 7 (stable, no migration needed)
└─ Existing Vite 6 project?
    └─ Plan upgrade to Vite 7 first, then Vite 8
```

### Chunk Splitting Strategy

```
How to split chunks?
├─ Vite 8 (Rolldown)?
│   ├─ Simple vendor separation?
│   │   └─ codeSplitting.groups with regex patterns ✓
│   └─ Complex splitting (size limits, shared modules)?
│       └─ codeSplitting with maxSize/minSize/minShareCount
├─ Vite 7 (Rollup)?
│   ├─ Simple vendor separation?
│   │   └─ manualChunks object form ✓
│   └─ Complex splitting logic?
│       └─ manualChunks function form
└─ Vite 7 with rolldown-vite (experimental)?
    └─ advancedChunks.groups (renamed to codeSplitting in Vite 8)
```

### Path Alias Strategy

```
How to configure path aliases?
├─ Vite 8?
│   ├─ All aliases match tsconfig paths?
│   │   └─ Use resolve.tsconfigPaths: true ✓
│   └─ Need aliases beyond tsconfig paths?
│       └─ Use resolve.alias (manual configuration)
├─ Vite 7 or earlier?
│   └─ Use resolve.alias + sync with tsconfig.json manually ✓
└─ Any version?
    └─ ALWAYS keep tsconfig paths in sync with Vite aliases
```

### Build Target Selection

```
Choosing build.target?
├─ Supporting legacy browsers (< Safari 16)?
│   └─ Use @vitejs/plugin-legacy
├─ Modern browsers only?
│   ├─ Smallest possible bundle?
│   │   └─ 'esnext'
│   └─ Otherwise → 'baseline-widely-available' (default) ✓
└─ Specific browser requirements?
    └─ Use explicit array: ['chrome111', 'safari16.4']
```

See [reference.md](reference.md) for quick-lookup tables and migration checklist.

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- ❌ Using `build.rollupOptions` in Vite 8 (deprecated alias for `build.rolldownOptions` - may warn)
- ❌ Using object-form `manualChunks` in Vite 8 (removed; use `codeSplitting.groups`)
- ❌ Using deprecated `build.polyfillModulePreload` (use `build.modulePreload.polyfill`)
- ❌ Using deprecated `splitVendorChunkPlugin` (removed in Vite 7+)
- ❌ Using `target: 'modules'` (removed in Vite 7; use `'baseline-widely-available'`)
- ❌ Using Sass legacy API `api: 'legacy'` (removed in Vite 7+)
- ❌ Path aliases in `vite.config.ts` but not `tsconfig.json` (or vice versa)

**Medium Priority Issues:**

- ⚠️ No vendor chunk splitting in production builds (large initial bundles)
- ⚠️ Same build config for all environments (slow dev builds, exposed source maps in prod)
- ⚠️ Hardcoded API URLs instead of environment variables
- ⚠️ Using Environment API in production apps (still RC phase)
- ⚠️ Function-form `manualChunks` in Vite 8 (deprecated, migrate to `codeSplitting`)

**Common Mistakes:**

- Forgetting to sync tsconfig paths with Vite resolve.alias (build works, IDE fails or vice versa)
- Committing `.env` files with secrets (use `.env.local`, add to `.gitignore`)
- Setting `minify: true` in development mode (slows rebuilds significantly)
- Always generating sourcemaps in production (exposes source code)

**Gotchas & Edge Cases:**

- **Vite 8**: `build.rollupOptions` is a deprecated alias for `build.rolldownOptions` - works but will warn
- **Vite 8**: Rolldown generates a `runtime.js` chunk when using `codeSplitting.groups`
- **Vite 8**: Default browser targets: Chrome 111+, Edge 111+, Firefox 114+, Safari 16.4+
- **Vite 8**: `resolve.tsconfigPaths` disabled by default due to performance cost
- **Vite 8**: Install size ~15MB larger than Vite 7 (lightningcss + Rolldown)
- **Vite 8**: `build.commonjsOptions` is a no-op (Rolldown handles CJS natively)
- **Vite 8**: CSS minification uses Lightning CSS, JS minification uses Oxc (both replaced esbuild)
- **Vite 8**: `esbuild` config option is deprecated - auto-converts to `oxc`, but not all options are supported (no property mangling, no `supported` option)
- **Vite 7**: Node.js 18 dropped - requires Node.js 20.19+ or 22.12+
- **Vite 7**: Sass legacy API completely removed
- **Vite 7**: `splitVendorChunkPlugin` removed
- **Vite 7**: Default target changed from `'modules'` to `'baseline-widely-available'`
- **Rolldown**: `advancedChunks` renamed to `codeSplitting` in Vite 8
- **Rolldown**: `codeSplitting.maxSize` is a target, not a strict limit
- **Rolldown**: `includeDependenciesRecursively` defaults to true - may pull in more than expected
- `.env` files are loaded based on `--mode` flag, not `NODE_ENV`
- `loadEnv()` third argument (`""`) loads all env vars, not just `VITE_`-prefixed ones

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST keep path aliases in sync between `vite.config.ts` and `tsconfig.json` - mismatches cause import resolution failures)**

**(You MUST use `build.rolldownOptions` in Vite 8+ - `build.rollupOptions` is a deprecated alias)**

**(You MUST use `codeSplitting.groups` for chunk splitting in Vite 8 - object-form `manualChunks` is removed, function-form deprecated)**

**(You MUST use `build.modulePreload.polyfill` instead of deprecated `build.polyfillModulePreload`)**

**(You MUST use Sass modern API (default in Vite 6+) - legacy API is removed in Vite 7+)**

**Failure to follow these rules will cause build failures, broken imports, or deprecated API warnings.**

</critical_reminders>
