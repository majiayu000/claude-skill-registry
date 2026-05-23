---
name: vite
description: "Vite build tool and dev server for fast modern web development. Configuration, plugins, optimization, HMR. Trigger: When configuring Vite build tool, setting up dev server, or optimizing build performance."
skills:
  - conventions
dependencies:
  vite: ">=5.0.0 <6.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Vite Skill

## Overview

Fast build tool and development server with native ES modules and hot module replacement.

## Objective

Configure and optimize Vite for modern web development with fast builds and excellent developer experience.

---

## When to Use

Use this skill when:

- Setting up Vite build tool for modern web apps
- Configuring dev server with HMR
- Optimizing build performance and bundle size
- Using Vite plugins (React, Vue, etc.)
- Configuring environment variables

Don't use this skill for:

- Webpack-specific configuration (use webpack skill)
- Legacy build setups

---

## Critical Patterns

### ✅ REQUIRED: Use defineConfig

```typescript
// ✅ CORRECT: Type-safe config
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});

// ❌ WRONG: Plain object (no type safety)
export default {
  plugins: [react()],
};
```

### ✅ REQUIRED: Environment Variables with VITE\_ Prefix

```typescript
// ✅ CORRECT: VITE_ prefix
// .env
VITE_API_URL=https://api.example.com

// Access in code
const apiUrl = import.meta.env.VITE_API_URL;

// ❌ WRONG: No prefix (won't be exposed)
API_URL=https://api.example.com // Not accessible
```

### ✅ REQUIRED: Use Plugins for Framework Support

```typescript
// ✅ CORRECT: Framework plugin
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
});
```

---

## Conventions

Refer to conventions for:

- Project structure

### Vite Specific

- Configure vite.config for project needs
- Use environment variables with VITE\_ prefix
- Optimize build output
- Configure plugins properly
- Use static asset handling

---

## Decision Tree

**React project?** → Install and use `@vitejs/plugin-react`.

**Vue project?** → Use `@vitejs/plugin-vue`.

**Need path aliases?** → Configure `resolve.alias` in vite.config.

**Custom dev server port?** → Set `server.port`.

**Proxy API calls?** → Configure `server.proxy` to avoid CORS.

**Slow build?** → Check bundle size, use dynamic imports, optimize dependencies.

**Environment-specific config?** → Use `mode` parameter or separate config files.

---

## Example

vite.config.ts:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
  build: {
    outDir: "dist",
    sourcemap: true,
  },
});
```

---

## Edge Cases

**CommonJS dependencies:** Some packages may not work with ES modules. Use `optimizeDeps.include` to pre-bundle them.

**Global variables:** Use `define` option to replace global constants at build time.

**Static assets:** Assets in `public/` are copied as-is. Assets imported in code are processed and hashed.

**Build base path:** Set `base` option for deploying to subdirectory (e.g., GitHub Pages).

**CSS code splitting:** Vite automatically splits CSS. Use `build.cssCodeSplit: false` to combine into one file.

---

## References

- https://vitejs.dev/guide/
- https://vitejs.dev/config/
