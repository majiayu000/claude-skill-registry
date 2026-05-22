---
name: starwards-monorepo
description: npm workspace monorepo workflow for Starwards - build order, module dependencies, watch mode, testing across modules, and avoiding common monorepo pitfalls; core builds first always
version: 2025-11-04
related_skills:
  - starwards-tdd (test patterns for each module)
  - starwards-debugging (debug cross-module issues)
  - starwards-verification (commands verify all modules)
  - using-superpowers (announce skill usage)
---

# Starwards Monorepo Workflow

## Overview

Starwards uses npm workspaces with 4 interdependent modules. Understanding build order, dependencies, and workflow prevents wasted time.

**Core principle:** Core builds first. Others depend on it.

## Monorepo Structure

```
starwards/
├── package.json              # Root workspace config
├── modules/
│   ├── core/                 # Game logic, shared types
│   │   ├── src/             # TypeScript source
│   │   ├── cjs/             # Built CommonJS (gitignored)
│   │   └── package.json     # @starwards/core
│   ├── server/              # Colyseus rooms, game server
│   │   ├── src/
│   │   ├── cjs/             # Built server code
│   │   └── package.json     # @starwards/server
│   ├── browser/             # React UI, PixiJS rendering
│   │   ├── src/
│   │   ├── dist/            # Webpack bundle
│   │   └── package.json     # @starwards/browser
│   ├── node-red/            # Node-RED integration
│   │   ├── src/
│   │   ├── dist/
│   │   └── package.json     # @starwards/node-red
│   └── e2e/                 # Playwright tests
│       └── test/
└── node_modules/            # Shared dependencies (hoisted)
```

## Module Dependencies

```
core (no deps)
  ├─→ server (depends on core)
  ├─→ browser (depends on core)
  ├─→ node-red (depends on core)
  └─→ e2e (depends on all)
```

**Critical:** Core must build before others.

## Build Commands

### From Root Directory

```bash
# Build all modules (correct order)
npm run build
# Runs: core → (server, browser, node-red in parallel)

# Build specific module
npm run build:core
npm run build:browser
npm run build:server
npm run build:node-red

# Clean all build artifacts
npm run clean
# Removes: cjs/, dist/ from all modules

# Fresh build
npm run clean && npm run build
```

### From Module Directory

```bash
# Build just this module
cd modules/core && npm run build
cd modules/browser && npm run build

# Watch mode (rebuild on file change)
cd modules/core && npm run build:watch
```

**When to use:**
- Root commands: CI/CD, fresh builds, building everything
- Module commands: Active development of that module

## Development Workflow (3 Terminals)

### Terminal 1: Core Watch Mode

```bash
cd modules/core && npm run build:watch
```

**Purpose:** Automatically rebuild core when files change

**When running:** Any time you're editing core/ files

**Status:** Keep running in background

**Troubleshooting:**
- Not rebuilding? Check console for errors
- Server not seeing changes? Core build may have failed

### Terminal 2: Webpack Dev Server

```bash
cd modules/browser && npm start
```

**Purpose:** Hot-reload browser UI

**Serves:** http://localhost:3000

**When running:** When developing browser/ UI

**Troubleshooting:**
- Port 3000 taken? `lsof -ti:3000 | xargs kill -9`
- Webpack overlay shows [object Object]? Check browser console (F12)
- Changes not appearing? Check if core watch is running

### Terminal 3: API Server

```bash
node -r ts-node/register/transpile-only modules/server/src/dev.ts
```

**Purpose:** Run game server with Colyseus

**Serves:** http://localhost:8080

**When running:** Always (browser needs API)

**Troubleshooting:**
- Server crashes? Check if core is built
- Changes not appearing? Restart this terminal (server doesn't auto-reload)

### Workflow Summary

1. Start Terminal 1 (core watch)
2. Start Terminal 2 (webpack dev server)
3. Start Terminal 3 (API server)
4. Edit code
5. Browser auto-reloads (Terminal 2 hot-reload)
6. Core changes → rebuild (Terminal 1 watches)
7. Server changes → manually restart Terminal 3

## Testing in Monorepo

### All Tests

```bash
# From root: Run all module tests
npm test
# Runs: core tests, server tests, node-red tests

# Specific module
npm test -- --projects=core
npm test -- --projects=server
npm test -- --projects=node-red

# Specific file
npm test -- modules/core/test/shield.spec.ts
```

### E2E Tests

```bash
# E2E tests require ALL modules built
npm run build        # Build everything first
npm run test:e2e     # Then run E2E

# Update snapshots
npm run test:e2e -- --update-snapshots
```

**Why build first:** E2E tests start real server, which needs built modules.

### Watch Mode During Development

```bash
# Watch all tests
npm test -- --watch

# Watch specific module
cd modules/core && npm test -- --watch
```

**Tip:** Run in 4th terminal while developing.

## Common Workflows

### Adding New Core Feature

```bash
# 1. Ensure core watch running
cd modules/core && npm run build:watch  # Terminal 1

# 2. Write test (TDD)
# modules/core/test/shield.spec.ts

# 3. Run test (should fail RED)
npm test -- modules/core/test/shield.spec.ts

# 4. Implement feature
# modules/core/src/ship/shield.ts
# (watch rebuilds automatically)

# 5. Test passes GREEN
npm test -- modules/core/test/shield.spec.ts

# 6. Verify dependents still work
npm test                # All tests
npm run test:e2e        # E2E tests
```

### Adding New UI Widget

```bash
# 1. Ensure everything running
# Terminal 1: core watch
# Terminal 2: webpack dev server
# Terminal 3: API server

# 2. Write E2E test (TDD)
# modules/e2e/test/shield-widget.spec.ts
npm run test:e2e -- shield-widget.spec.ts  # Fails RED

# 3. Create widget
# modules/browser/src/widgets/shield.ts
# (webpack hot-reloads automatically)

# 4. Test passes GREEN
npm run test:e2e -- shield-widget.spec.ts

# 5. Verify
npm run test:e2e       # All E2E
```

### Adding New Server Feature

```bash
# 1. Core watch running (Terminal 1)
# 2. Write test
# modules/server/test/shield-command.spec.ts
npm test -- modules/server/test/shield-command.spec.ts  # RED

# 3. Implement
# modules/server/src/ship/room.ts
npm run build:server

# 4. Restart server (Terminal 3)
# Ctrl+C, then re-run command

# 5. Test passes GREEN
npm test -- modules/server/test/shield-command.spec.ts

# 6. Verify E2E
npm run test:e2e
```

## Build Order & Dependencies

**Automatic (from root):**
```bash
npm run build
# 1. Build core first (required)
# 2. Build server, browser, node-red in parallel
```

**Manual (module by module):**
```bash
# CORRECT order
npm run build:core       # 1st
npm run build:server     # 2nd (can run parallel with browser)
npm run build:browser    # 2nd (can run parallel with server)
npm run build:node-red   # 2nd (can run parallel with others)

# WRONG order
npm run build:browser  # FAILS - core not built yet
npm run build:core     # Too late
```

## Path Aliases

All modules can import core using `@starwards/core`:

```typescript
// In server, browser, or node-red:
import { ShipState } from '@starwards/core';
```

**Configured in:**
- `tsconfig.json` (TypeScript)
- `jest.config.js` (Jest tests)
- `webpack.common.js` (Browser webpack)

**Maps to:**
- Development: `modules/core/src`
- Production: `modules/core/cjs`

## Common Pitfalls

### Pitfall 1: Core Not Built

**Symptom:**
```
Error: Cannot find module '@starwards/core'
```

**Solution:**
```bash
npm run build:core
# Or start watch mode: cd modules/core && npm run build:watch
```

### Pitfall 2: Server Not Restarted

**Symptom:** Server code changes not appearing

**Solution:** Server doesn't auto-reload. Restart Terminal 3:
```bash
Ctrl+C
node -r ts-node/register/transpile-only modules/server/src/dev.ts
```

### Pitfall 3: Webpack Not Running

**Symptom:** Browser changes not appearing

**Solution:** Start Terminal 2:
```bash
cd modules/browser && npm start
```

### Pitfall 4: Build Artifacts Stale

**Symptom:** Weird errors, imports failing, tests failing randomly

**Solution:** Fresh build:
```bash
npm run clean
npm ci            # Fresh dependencies
npm run build
```

### Pitfall 5: Wrong Directory for npm test

**Symptom:** Tests not found

**Solution:** Run from root, not module:
```bash
# CORRECT
npm test

# WRONG
cd modules/core && npm test  # Works but limits to core only
```

### Pitfall 6: E2E Without Build

**Symptom:** E2E tests fail, server doesn't start

**Solution:**
```bash
npm run build      # Build all first
npm run test:e2e   # Then E2E
```

### Pitfall 7: Dependency Version Mismatch

**Symptom:** "Multiple versions of package X"

**Solution:**
```bash
npm ci            # Use exact versions from package-lock.json
npm dedupe        # Deduplicate dependencies
```

## CI/CD Monorepo Considerations

**GitHub Actions workflow:**

```yaml
- run: npm ci                  # Install all workspaces
- run: npm run test:types      # Type check all modules
- run: npm run test:format     # Format check all modules
- run: npm run build           # Build all modules (correct order)
- run: npm test                # Test all modules
- run: npm run test:e2e        # E2E tests (after build)
```

**Order matters:** Build must complete before E2E.

## Debugging Monorepo Issues

### Check Build Status

```bash
# Verify all modules built
ls modules/core/cjs          # Should exist
ls modules/browser/dist      # Should exist
ls modules/server/cjs        # Should exist
```

### Check Dependencies

```bash
# List workspace dependencies
npm ls @starwards/core      # Who depends on core?

# Check if hoisted correctly
ls node_modules/@starwards  # Should see symlinks
```

### Fresh Start

```bash
# Nuclear option - full reset
npm run clean               # Remove build artifacts
rm -rf node_modules         # Remove dependencies
rm package-lock.json        # Remove lockfile
npm install                 # Fresh install
npm run build               # Fresh build
```

**Use when:** Everything is broken, nothing makes sense.

## Integration with Other Skills

- **starwards-tdd** - Test patterns for each module type
- **starwards-verification** - Commands verify all modules
- **starwards-debugging** - Debug issues across module boundaries

## Quick Reference

| Action | Command |
|--------|---------|
| Build all | `npm run build` |
| Build core only | `npm run build:core` |
| Core watch | `cd modules/core && npm run build:watch` |
| Test all | `npm test` |
| Test core only | `npm test -- --projects=core` |
| Clean all | `npm run clean` |
| Fresh build | `npm run clean && npm ci && npm run build` |
| Dev workflow | 3 terminals: core watch, webpack, server |

## The Bottom Line

**Remember:**
1. Core builds first, always
2. Watch mode saves time (Terminal 1)
3. Server needs manual restart (Terminal 3)
4. Browser hot-reloads (Terminal 2)
5. Run tests from root
6. Build before E2E
7. When in doubt: fresh build
