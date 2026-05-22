---
name: workers-dev-experience
description: Cloudflare Workers local development with Wrangler, Miniflare, hot reload, debugging. Use for project setup, wrangler.jsonc configuration, or encountering local dev, HMR, binding simulation errors.
---

# Cloudflare Workers Developer Experience

Local development setup with Wrangler, Miniflare, and modern tooling.

## Quick Start

```bash
# Create new project
bunx create-cloudflare@latest my-worker

# Or from scratch
mkdir my-worker && cd my-worker
bun init -y
bun add -d wrangler @cloudflare/workers-types

# Start local development
bunx wrangler dev
```

## Essential wrangler.jsonc

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",

  // Development settings
  "dev": {
    "port": 8787,
    "local_protocol": "http"
  },

  // Environment variables (non-secret)
  "vars": {
    "ENVIRONMENT": "development"
  },

  // Bindings
  "kv_namespaces": [
    { "binding": "KV", "id": "abc123", "preview_id": "def456" }
  ],

  "d1_databases": [
    { "binding": "DB", "database_id": "xyz789", "database_name": "my-db" }
  ],

  "r2_buckets": [
    { "binding": "BUCKET", "bucket_name": "my-bucket" }
  ]
}
```

## Critical Rules

1. **Always use `wrangler dev` for local testing** - Simulates Cloudflare runtime accurately
2. **Set `compatibility_date`** - Controls runtime behavior, update quarterly
3. **Use preview IDs for local dev** - Separate from production bindings
4. **Configure TypeScript properly** - Use `@cloudflare/workers-types`
5. **Enable source maps** - Better error stacks in development

## Top 6 Errors Prevented

| Error | Symptom | Prevention |
|-------|---------|------------|
| Module not found | Import errors on deploy | Set `"moduleResolution": "bundler"` in tsconfig |
| Binding undefined | `env.KV is undefined` locally | Add `preview_id` to KV namespace config |
| HMR not working | Changes not reflecting | Check port conflicts, use `--local` flag |
| D1 schema mismatch | Queries fail locally | Run migrations on local DB |
| Type errors | Missing binding types | Generate types with `wrangler types` |
| CORS issues | Browser blocking requests | Add CORS headers in dev handler |

## Local Development Workflow

```bash
# Start dev server (recommended)
bunx wrangler dev

# With live reload
bunx wrangler dev --live-reload

# Remote mode (use actual Cloudflare services)
bunx wrangler dev --remote

# Specify environment
bunx wrangler dev --env staging

# Custom port
bunx wrangler dev --port 3000
```

## TypeScript Configuration

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types"],
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "deploy:staging": "wrangler deploy --env staging",
    "deploy:production": "wrangler deploy --env production",
    "test": "vitest",
    "test:watch": "vitest --watch",
    "type-check": "tsc --noEmit",
    "lint": "eslint src/",
    "types": "wrangler types",
    "tail": "wrangler tail",
    "db:migrate": "wrangler d1 migrations apply DB",
    "db:studio": "wrangler d1 execute DB --local --command 'SELECT 1'"
  }
}
```

## Debugging

### Console Logging

```typescript
// Development-only logging
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (env.ENVIRONMENT === 'development') {
      console.log('Request:', request.method, request.url);
      console.log('Headers:', Object.fromEntries(request.headers));
    }

    // Handler logic...
  }
};
```

### Using wrangler tail

```bash
# Real-time logs from deployed worker
wrangler tail

# Filter by status
wrangler tail --status error

# Filter by method
wrangler tail --method POST

# JSON format for parsing
wrangler tail --format json
```

### VS Code Debugging

**.vscode/launch.json**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Wrangler Dev",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "bunx",
      "runtimeArgs": ["wrangler", "dev", "--inspector-port", "9229"],
      "skipFiles": ["<node_internals>/**"],
      "sourceMaps": true
    }
  ]
}
```

## When to Load References

Load specific references based on the task:

- **Setting up project?** → Load `references/local-development.md` for complete setup guide
- **Configuring wrangler?** → Load `references/wrangler-config.md` for all configuration options
- **Debugging issues?** → Load `references/debugging-tools.md` for debugging techniques

## Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| `templates/wrangler-config.jsonc` | Complete wrangler config | Starting new project |
| `templates/dev-script.ts` | Development utilities | Adding dev helpers |

## Scripts

| Script | Purpose | Command |
|--------|---------|---------|
| `scripts/dev-setup.sh` | Initialize dev environment | `./dev-setup.sh` |

## Resources

- Wrangler CLI: https://developers.cloudflare.com/workers/wrangler/
- Configuration: https://developers.cloudflare.com/workers/wrangler/configuration/
- Local Development: https://developers.cloudflare.com/workers/testing/local-development/
