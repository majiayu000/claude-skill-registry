---
name: Bun Runtime
description: Use for Bun runtime, bunfig.toml, watch/hot modes, env vars, CLI flags, and module resolution.
version: 1.0.0
---

# Bun Runtime

Bun is a fast all-in-one JavaScript runtime built on JavaScriptCore (Safari's engine). It provides 4x faster startup than Node.js on Linux.

## Quick Start

```bash
# Run a file
bun run index.ts
bun index.ts  # shorthand

# Run with watch mode
bun --watch run index.ts

# Run package.json script
bun run dev

# Run with hot reloading
bun --hot run server.ts
```

## Core CLI Flags

| Flag | Purpose |
|------|---------|
| `--watch` | Restart on file changes |
| `--hot` | Hot module replacement (preserves state) |
| `--smol` | Reduce memory usage (slower GC) |
| `--inspect` | Enable debugger |
| `--preload` | Load modules before execution |
| `--env-file` | Load specific .env file |
| `-e, --eval` | Evaluate code string |

## Running Files

Bun transpiles TypeScript and JSX on-the-fly:

```bash
bun run index.js
bun run index.ts
bun run index.jsx
bun run index.tsx
```

**Important**: Put Bun flags immediately after `bun`:
```bash
bun --watch run dev    # Correct
bun run dev --watch    # Wrong - flag passed to script
```

## Package.json Scripts

```bash
# Run script
bun run dev
bun dev  # shorthand (if no Bun command conflicts)

# List available scripts
bun run

# Run with Bun instead of Node
bun run --bun vite
```

Bun respects lifecycle hooks (`preclean`, `postclean`, etc.).

## Watch Mode vs Hot Reloading

| Mode | Flag | Behavior |
|------|------|----------|
| Watch | `--watch` | Full process restart on changes |
| Hot | `--hot` | Replace modules, preserve state |

```bash
# Watch mode - full restart
bun --watch run server.ts

# Hot reloading - preserves connections/state
bun --hot run server.ts
```

## Environment Variables

Bun automatically loads `.env` files:

```bash
# Loads automatically: .env, .env.local, .env.development
bun run index.ts

# Specify env file
bun --env-file .env.production run index.ts

# Disable auto-loading
# In bunfig.toml: env = false
```

Access in code:
```typescript
const apiKey = process.env.API_KEY;
const bunEnv = Bun.env.NODE_ENV;
```

## Globals Available

| Global | Source | Notes |
|--------|--------|-------|
| `Bun` | Bun | Main API object |
| `Buffer` | Node.js | Binary data |
| `process` | Node.js | Process info |
| `fetch` | Web | HTTP requests |
| `Request/Response` | Web | HTTP types |
| `WebSocket` | Web | WebSocket client |
| `crypto` | Web | Cryptography |
| `console` | Web | Logging |
| `__dirname` | Node.js | Current directory |
| `__filename` | Node.js | Current file |

## Preload Scripts

Load modules before your main script:

```bash
bun --preload ./setup.ts run index.ts
```

Or in `bunfig.toml`:
```toml
preload = ["./setup.ts"]
```

Use cases: polyfills, global setup, instrumentation.

## Stdin Execution

```bash
# Pipe code to Bun
echo "console.log('Hello')" | bun run -

# Redirect file
bun run - < script.js
```

## Workspaces & Monorepos

```bash
# Run script in specific packages
bun run --filter 'pkg-*' build

# Run in all workspaces
bun run --filter '*' test
```

## Debugging

```bash
# Start debugger
bun --inspect run index.ts

# Wait for debugger connection
bun --inspect-wait run index.ts

# Break on first line
bun --inspect-brk run index.ts
```

Connect via Chrome DevTools or VS Code.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module` | Missing dependency | Run `bun install` |
| `Top-level await` | Using await outside async | Wrap in async function or use `.mts` |
| `--watch not working` | Flag in wrong position | Put flag before `run` |

## When to Load References

Load `references/bunfig.md` when:
- Configuring bunfig.toml
- Setting up test configuration
- Configuring package manager behavior
- Setting JSX options

Load `references/cli-flags.md` when:
- Need complete CLI flag reference
- Configuring advanced runtime options
- Setting up debugging

Load `references/module-resolution.md` when:
- Troubleshooting import errors
- Configuring path aliases
- Understanding Bun's resolution algorithm
