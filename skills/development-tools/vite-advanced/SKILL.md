---
name: vite-advanced
description: Advanced Vite 7+ patterns including Environment API, plugin development, SSR configuration, library mode, and build optimization. Use when customizing build pipelines, creating plugins, or configuring multi-environment builds.
context: fork
agent: frontend-ui-developer
version: 1.0.0
tags: [vite, build, bundler, plugins, ssr, library-mode, environment-api, optimization]
user-invocable: false
---

# Vite Advanced Patterns

Advanced configuration for Vite 7+ including Environment API.

## Vite 7 Environment API (Key 2026 Feature)

Multi-environment support is now first-class:

```typescript
import { defineConfig } from 'vite'

export default defineConfig({
  environments: {
    // Browser client
    client: {
      build: {
        outDir: 'dist/client',
        manifest: true,
      },
    },
    // Node.js SSR
    ssr: {
      build: {
        outDir: 'dist/server',
        target: 'node20',
      },
    },
    // Edge runtime (Cloudflare, etc.)
    edge: {
      resolve: {
        noExternal: true,
        conditions: ['edge', 'worker'],
      },
      build: {
        outDir: 'dist/edge',
      },
    },
  },
})
```

**Key Changes:**
- Environments have their own module graph
- Plugins access `this.environment` in hooks
- `createBuilder` API for coordinated builds
- Node.js 20.19+ or 22.12+ required

## Plugin Development

Basic plugin structure:

```typescript
export function myPlugin(): Plugin {
  return {
    name: 'my-plugin',

    // Called once when config is resolved
    configResolved(config) {
      // Access resolved config
    },

    // Transform individual modules
    transform(code, id) {
      // this.environment available in Vite 7+
      if (id.endsWith('.special')) {
        return { code: transformCode(code) }
      }
    },

    // Virtual modules
    resolveId(id) {
      if (id === 'virtual:my-module') {
        return '\0virtual:my-module'
      }
    },
    load(id) {
      if (id === '\0virtual:my-module') {
        return 'export const value = "generated"'
      }
    },
  }
}
```

## SSR Configuration

Development (middleware mode):

```typescript
import { createServer } from 'vite'

const vite = await createServer({
  server: { middlewareMode: true },
  appType: 'custom',
})

app.use('*', async (req, res) => {
  const url = req.originalUrl
  let template = fs.readFileSync('index.html', 'utf-8')
  template = await vite.transformIndexHtml(url, template)

  const { render } = await vite.ssrLoadModule('/src/entry-server.tsx')
  const html = template.replace('<!--outlet-->', await render(url))

  res.send(html)
})
```

Production build scripts:

```json
{
  "scripts": {
    "build:client": "vite build --outDir dist/client",
    "build:server": "vite build --outDir dist/server --ssr src/entry-server.tsx"
  }
}
```

## Build Optimization

```typescript
export default defineConfig({
  build: {
    target: 'baseline-widely-available', // Vite 7 default
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
  },
})
```

## Quick Reference

| Feature | Vite 7 Status |
|---------|---------------|
| Environment API | Stable |
| ESM-only distribution | Default |
| Node.js requirement | 20.19+ or 22.12+ |
| `buildApp` hook | New for plugins |
| `createBuilder` | Multi-env builds |

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Multi-env builds | Use Vite 7 Environment API |
| Plugin scope | Use `this.environment` for env-aware plugins |
| SSR | Middleware mode for dev, separate builds for prod |
| Chunks | Manual chunks for vendor/router separation |

## Related Skills

- `biome-linting` - Fast linting alongside Vite
- `react-server-components-framework` - SSR integration
- `edge-computing-patterns` - Edge environment builds

## References

- [Environment API](references/environment-api.md) - Multi-environment builds
- [Plugin Development](references/plugin-development.md) - Plugin hooks
- [SSR Configuration](references/ssr-configuration.md) - SSR setup
- [Library Mode](references/library-mode.md) - Building packages
- [Chunk Optimization](references/chunk-optimization.md) - Build optimization
