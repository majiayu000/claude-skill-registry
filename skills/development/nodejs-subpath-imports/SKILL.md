---
name: nodejs-subpath-imports
description: Use when debugging subpath import errors (ERR_PACKAGE_IMPORT_NOT_DEFINED, "only allows ./"), configuring package.json imports field, migrating from tsconfig paths, or building cross-platform code with conditions. Covers Node.js spec constraints that ALL bundlers enforce.
---

# Node.js Subpath Imports

## CRITICAL

### Path Restrictions Are Node.js Spec, Not Bundler Limitations

When you see errors about path formats in `imports` field:

| Error pattern       | This is...   | NOT...             |
| ------------------- | ------------ | ------------------ |
| "only allows ./"    | Node.js spec | Metro limitation   |
| "rejects ../ paths" | Node.js spec | Webpack limitation |
| "must be relative"  | Node.js spec | Bundler bug        |

**Every compliant resolver enforces these rules.** See [Spec: Restrictions](#spec-restrictions) below.

---

## Operations

### Debug Subpath Import Errors

1. Check error message for pattern (see CRITICAL table above)
2. Verify targets start with `./` (required for local files)
3. Check for forbidden segments: `..`, `.`, `node_modules`
4. Verify extensions are explicit (no auto-resolution)
5. Check condition order (first match wins)

Common errors:

- `ERR_PACKAGE_PATH_NOT_EXPORTED` → subpath not in exports
- `ERR_PACKAGE_IMPORT_NOT_DEFINED` → key not in imports
- `MODULE_NOT_FOUND` → missing extension or wrong path

### Debug Project Config

1. Check `moduleResolution` in tsconfig (`bundler`, `node16`, `nodenext`)
2. Verify `resolvePackageJsonImports: true` (default with above modes)
3. Check bundler's condition configuration matches your targets
4. Verify `type: "module"` if using ESM

### Migrate from tsconfig Paths

**Before** (compile-time only):

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": { "@utils/*": ["./src/utils/*"] }
  }
}
```

**After** (runtime + compile-time):

```json
// package.json
{
  "imports": {
    "#utils/*": "./src/utils/*.js"
  }
}
```

```json
// tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "resolvePackageJsonImports": true
  }
}
```

Key changes:

- `@` prefix → `#` prefix (required by spec)
- Add explicit `.js` extensions
- Works at runtime without bundler

### Build Cross-Platform Code

See [reference/cross-platform.md](reference/cross-platform.md) for complete guide with:

- Platform abstraction patterns
- External package substitution (unique to `imports`)
- Conditions by runtime (Node, Deno, Bun)
- Conditions by bundler (Webpack, esbuild, Vite, Metro, etc.)

Quick pattern:

```json
{
  "imports": {
    "#platform": {
      "react-native": "./src/platform/native.js",
      "browser": "./src/platform/browser.js",
      "node": "./src/platform/node.js",
      "default": "./src/platform/node.js"
    },
    "#fetch": {
      "node": "node-fetch",
      "default": "./src/fetch-native.js"
    }
  }
}
```

---

## What This Enables

**Runtime aliases** - unlike `tsconfig.json` paths (compile-time only), subpath imports resolve at runtime:

```typescript
import { helper } from "#utils/helper.js"; // Works in Node, Deno, Bun natively
```

**Cross-platform code** - same import, different implementation per environment:

```json
{
  "imports": {
    "#fetch": {
      "node": "node-fetch",
      "browser": "./fetch-browser.js",
      "default": "./fetch-polyfill.js"
    }
  }
}
```

---

## Spec: Syntax

Source: [Node.js Packages - Subpath imports](https://nodejs.org/api/packages.html#subpath-imports)

### Keys Must Start with `#`

```json
{ "imports": { "#dep": "./dep.js", "#internal/*": "./src/internal/*.js" } }
```

> **Future**: Node.js v26+ allows `#/` prefix ([PR #60864](https://github.com/nodejs/node/pull/60864)).

### Targets: Strings, Objects, or Patterns

```json
{
  "imports": {
    "#string": "./path/to/file.js",
    "#object": { "node": "pkg", "default": "./polyfill.js" },
    "#pattern/*": "./src/*.js"
  }
}
```

### Relative Targets Must Start with `./`

```json
{ "imports": { "#good": "./src/file.js", "#bad": "src/file.js" } }
```

External packages (bare specifiers) don't need `./`.

### External Packages Allowed

```json
{
  "imports": {
    "#dep": { "node": "dep-node-native", "default": "./dep-polyfill.js" }
  },
  "dependencies": { "dep-node-native": "^1.0.0" }
}
```

---

## Spec: Resolution Algorithm

Source: [Node.js ESM - Resolution Algorithm](https://nodejs.org/api/esm.html#resolution-algorithm-specification)

1. Import specifier must start with `#`
2. Find matching key in nearest `package.json` `imports` field
3. If value is object → apply condition matching (first match wins)
4. If key contains `*` → perform string substitution on target
5. Resolve resulting path/specifier

### Pattern Substitution

`*` is **literal string replacement**, not glob:

```json
{ "imports": { "#internal/*.js": "./src/internal/*.js" } }
```

```typescript
import z from "#internal/z.js"; // → ./src/internal/z.js
import deep from "#internal/nested/x.js"; // → ./src/internal/nested/x.js
```

---

## Spec: Conditions

Source: [Node.js Packages - Conditional exports](https://nodejs.org/api/packages.html#conditional-exports)

First matching condition wins. Order from most specific to least.

### Built-in Conditions

| Condition     | When Matched               |
| ------------- | -------------------------- |
| `node-addons` | Node.js with native addons |
| `node`        | Any Node.js environment    |
| `import`      | Loaded via `import`        |
| `require`     | Loaded via `require()`     |
| `default`     | Fallback (must be last)    |

### Community Conditions

| Condition                    | When Matched                 |
| ---------------------------- | ---------------------------- |
| `types`                      | TypeScript (should be first) |
| `browser`                    | Web browser                  |
| `react-native`               | React Native                 |
| `react-server`               | React Server Components      |
| `development` / `production` | Build mode                   |

### Nested Conditions

```json
{
  "imports": {
    "#utils": {
      "node": { "import": "./utils-node.mjs", "require": "./utils-node.cjs" },
      "browser": "./utils-browser.js",
      "default": "./utils.mjs"
    }
  }
}
```

---

## Spec: Restrictions

Source: [Node.js Packages - Subpath patterns](https://nodejs.org/api/packages.html#subpath-patterns)

### Forbidden Path Segments

After `./`, these are **disallowed**:

| Segment        | Why            |
| -------------- | -------------- |
| `..`           | Path traversal |
| `.`            | Ambiguous      |
| `node_modules` | Injection      |

### Invalid Examples

```json
{
  "imports": {
    "#bad1": "../outside/file.js",
    "#bad2": "./dist/../dist/file.js",
    "#bad3": "././file.js",
    "#bad4": "./node_modules/pkg/file.js"
  }
}
```

---

## Spec: Scope

Source: [Node.js Packages - Subpath imports](https://nodejs.org/api/packages.html#subpath-imports)

- **Private to package** - only code within the package can use `#` imports
- **Cannot be consumed externally** - `import x from 'pkg/#internal'` is invalid
- **Isolated mappings** - no inheritance between packages

---

## Edge Cases & Gotchas

For full details with sources, see [reference/edge-cases.md](reference/edge-cases.md).

| Gotcha                    | Summary                                        |
| ------------------------- | ---------------------------------------------- |
| PATTERN_KEY_COMPARE       | Longer base index wins, then total length      |
| No extension guessing     | Must use explicit `.js` in CJS and ESM         |
| Arrays as fallbacks       | Only for validation errors, NOT file-not-found |
| Trailing slash (DEP0155)  | Use `#lib/*` pattern instead of `#lib/`        |
| Pattern keys need one `*` | Multiple `*` = exact match only                |
| Exact before patterns     | Non-pattern keys checked first                 |

---

## Tool Support

All major runtimes and bundlers support subpath imports. For versions, conditions config, and examples, see [reference/tool-support.md](reference/tool-support.md).

**Runtimes:** Node.js v14.6+, Deno v1.25+, Bun v1.0+

**Bundlers:** esbuild, Webpack 5+, Rspack, Rollup, Rolldown, Metro v0.82+

**Frameworks:** Vite, Next.js, Astro, Expo

---

## Complete Example

```json
{
  "name": "my-app",
  "type": "module",
  "imports": {
    "#db": "./src/database/index.js",
    "#db/*": "./src/database/*.js",
    "#utils/*": "./src/utils/*.js",
    "#platform": {
      "node": "./src/platform/node.js",
      "browser": "./src/platform/browser.js",
      "react-native": "./src/platform/native.js",
      "default": "./src/platform/node.js"
    }
  }
}
```

```typescript
import { connect } from "#db"; // exact match → ./src/database/index.js
import { query } from "#db/queries.js"; // pattern → ./src/database/queries.js
import platform from "#platform"; // condition-based
```

---

## Monorepo Note

Subpath imports **cannot reference outside the package** - `./` requirement and `..` prohibition are fundamental.

Alternatives for shared code:

1. **Workspace dependencies** - proper package
2. **Symlinks** - link into package
3. **tsconfig paths** - build-time fallback
