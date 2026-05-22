---
name: solidstart-config
description: "SolidStart configuration: app.config.ts with defineConfig, deployment presets (Netlify/Vercel/Cloudflare/etc.), prerendering/SSG, Vite plugins, experimental features."
metadata:
  globs:
    - "app.config.ts"
    - "vite.config.*"
---

# SolidStart Configuration

## app.config.ts

```ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  // Toggle SSR
  ssr: true,
  
  // Solid plugin config
  solid: {
    // Solid plugin options
  },
  
  // File extensions treated as routes
  extensions: ["js", "jsx", "ts", "tsx"],
  
  // Server config (Nitro)
  server: {
    preset: "node", // Deployment preset
    prerender: {
      routes: ["/", "/about"],
      // or crawlLinks: true
    }
  },
  
  // App root and route directories
  appRoot: "./src",
  routeDir: "./routes",
  
  // Middleware path
  middleware: "src/middleware/index.ts",
  
  // Dev overlay
  devOverlay: true,
  
  // Experimental features
  experimental: {
    islands: false
  },
  
  // Vite config
  vite: {
    plugins: []
  }
});
```

## Vite Configuration

Can be object or function for per-router config:

```ts
// Object config
vite: {
  plugins: []
}

// Function config (per router)
vite({ router }) {
  if (router === "server") {
    // Server router config
  } else if (router === "client") {
    // Client router config
  } else if (router === "server-function") {
    // Server function router config
  }
  return { plugins: [] };
}
```

## Deployment Presets

- **Node.js**: `"node"` (default)
- **Netlify**: `"netlify"` or `"netlify_edge"`
- **Vercel**: `"vercel"` or `"vercel_edge"`
- **Cloudflare**: `"cloudflare"`, `"cloudflare_pages"`, or `"cloudflare_module"`
- **AWS**: `"aws_lambda"`
- **Deno**: `"deno_server"` or `"deno_deploy"`

```ts
export default defineConfig({
  server: {
    preset: "netlify_edge"
  }
});
```

### Cloudflare Special Config

```ts
export default defineConfig({
  server: {
    preset: "cloudflare_module",
    rollupConfig: {
      external: ["__STATIC_CONTENT_MANIFEST", "node:async_hooks"]
    }
  }
});

// In wrangler.toml:
// compatibility_flags = [ "nodejs_compat" ]
```

## Static Site Generation (SSG)

### Specific Routes

```ts
export default defineConfig({
  server: {
    prerender: {
      routes: ["/", "/about", "/contact"]
    }
  }
});
```

### All Routes

```ts
export default defineConfig({
  server: {
    prerender: {
      crawlLinks: true // Pre-render all routes
    }
  }
});
```

## Route Preloading

```tsx
export const route = {
  preload: ({ params }) => {
    return getProductQuery(params.id);
  }
} satisfies RouteDefinition;

export default function ProductPage(props: RouteSectionProps) {
  const product = createAsync(() => getProductQuery(props.params.id));
  // Preloaded data in props.data
  return <div>{product()?.name}</div>;
}
```

## Best Practices

1. Configure deployment preset based on hosting platform
2. Use prerendering for static pages (blogs, docs, marketing)
3. Configure Vite plugins per router when needed
4. Use experimental features with caution
5. Set proper appRoot and routeDir if using custom structure

