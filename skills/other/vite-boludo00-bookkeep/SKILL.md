---
name: vite
description: |
  Configures Vite build tool, HMR, and SWC transpilation for React development.
  Use when: modifying vite.config.ts, adding path aliases, configuring build output,
  optimizing bundle splitting, setting up environment variables, or debugging HMR issues.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_console_messages, mcp__plugin_playwright_playwright__browser_network_requests
---

# Vite Skill

Bookkeep uses Vite 5.x with @vitejs/plugin-react-swc for fast HMR and transpilation. The frontend builds to `dist/` and is served by the FastAPI backend in production. SWC replaces Babel for significantly faster development builds.

## Quick Start

### Development Server

```bash
npm run dev          # Starts on port 8080
npm run build        # Production build to dist/
npm run preview      # Preview production build locally
```

### Current Configuration

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

export default defineConfig(({ mode }) => ({
  server: {
    host: "::",           // Listen on all interfaces
    port: 8080,
  },
  plugins: [react()],     // SWC for fast transpilation
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: "dist",
  },
}));
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Path alias | Import from `@/` | `import { Button } from '@/components/ui/button'` |
| Environment vars | `VITE_` prefix required | `import.meta.env.VITE_API_URL` |
| Code splitting | `React.lazy()` + dynamic import | `lazy(() => import("@/pages/Settings"))` |
| Production mode | `import.meta.env.PROD` | Conditional API base URL |

## Environment Variables

```typescript
// src/lib/api.ts - Environment-aware API URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.PROD ? '' : 'http://localhost:8000');
```

| Variable | Purpose |
|----------|---------|
| `VITE_API_URL` | Override API base URL (dev only) |
| `VITE_APP_VERSION` | Build version (set in Docker build) |

## Code Splitting Pattern

All pages except Login and NotFound are lazy-loaded:

```typescript
// src/App.tsx
import { Suspense, lazy } from "react";

// Static imports for critical path
import Login from "@/pages/Login";
import NotFound from "@/pages/NotFound";

// Lazy-load everything else
const Settings = lazy(() => import("@/pages/Settings"));
const BookDetails = lazy(() => import("@/pages/BookDetails"));

// Wrap routes in Suspense
<Suspense fallback={<PageLoader />}>
  <Routes>
    <Route path="/settings" element={<Settings />} />
  </Routes>
</Suspense>
```

## See Also

- [config](references/config.md) - Vite configuration patterns
- [environment](references/environment.md) - Environment variable handling
- [build](references/build.md) - Production build optimization
- [hmr](references/hmr.md) - HMR debugging and patterns

## Related Skills

- See the **react** skill for component patterns and lazy loading
- See the **typescript** skill for path alias TypeScript configuration
- See the **tailwind** skill for PostCSS integration