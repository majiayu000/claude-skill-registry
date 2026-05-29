---
name: personal-vite-jsx-caching-fix
description: 'Troubleshoot Vite JSX parsing errors caused by stale compiled files in src directories'
---

# Vite JSX Caching Fix

Troubleshooting guide for "Failed to parse source for import analysis because the content contains invalid JS syntax" errors in Vite projects.

## Problem Description

This error occurs when compiled `.js`, `.d.ts`, and `.map` files accumulate in `src/` directories. Vite picks up these stale compiled files instead of the fresh TypeScript sources, leading to JSX parsing failures.

**Error message:**

```
[plugin:vite:import-analysis] Failed to parse source for import analysis because the content contains invalid JS syntax. If you are using JSX, make sure to name the file with the .jsx or .tsx extension.
```

## When This Occurs

- After linters or build tools accidentally compile files into `src/` instead of `dist/`
- After IDE plugins auto-compile TypeScript
- After incorrect tsconfig `outDir` settings
- After running `tsc` from wrong directory

## Identifying the Problem

Search for compiled files in src directories:

```bash
# Count compiled files in src directories
find packages/*/src -name "*.js" -o -name "*.js.map" -o -name "*.d.ts" -o -name "*.d.ts.map" 2>/dev/null | wc -l

# List all compiled files
find packages/*/src \( -name "*.js" -o -name "*.js.map" -o -name "*.d.ts" -o -name "*.d.ts.map" \) -type f

# Check specific package
find packages/dashboard-frontend/src -name "*.js" 2>/dev/null
```

## Complete Cleanup Procedure

### Step 1: Stop dev server

```bash
./run.sh dev stop
```

### Step 2: Remove compiled files from ALL src directories

```bash
find packages/*/src \( -name "*.js" -o -name "*.js.map" -o -name "*.d.ts" -o -name "*.d.ts.map" \) -type f -delete
```

### Step 3: Clear Vite cache

```bash
rm -rf node_modules/.vite packages/*/node_modules/.vite
```

### Step 4: Clear Turbo cache (optional but recommended)

```bash
rm -rf .turbo packages/*/.turbo
```

### Step 5: Reinstall dependencies (if issues persist)

```bash
pnpm install --force
```

## Verification Steps

1. Confirm no compiled files remain:

```bash
find packages/*/src -name "*.js" 2>/dev/null | wc -l  # Should be 0
```

2. Test module import speed (should be < 1 second):

```bash
cd packages/dashboard && node --import tsx -e "
console.time('import');
import('./src/server/index.js').then(() => console.timeEnd('import'));
"
```

3. Start dev server and verify it starts within 30 seconds:

```bash
./run.sh dev
```

## Prevention Strategies

### 1. Add to .gitignore

Ensure these patterns are in your root `.gitignore`:

```gitignore
# Compiled output in src directories (should never happen)
packages/*/src/**/*.js
packages/*/src/**/*.js.map
packages/*/src/**/*.d.ts
packages/*/src/**/*.d.ts.map
!packages/*/src/**/*.config.js
```

### 2. Verify tsconfig.json

Each package's `tsconfig.json` should have:

```json
{
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### 3. Pre-commit hook check

Add a check to your pre-commit hook:

```bash
# Fail if compiled files exist in src/
if find packages/*/src -name "*.js" -o -name "*.d.ts" 2>/dev/null | grep -q .; then
  echo "ERROR: Compiled files found in src directories!"
  exit 1
fi
```

## Orphaned Processes (Dashboard Running but Not Responding)

Sometimes after cleanup, the dashboard process shows as "running" but the API is unreachable (connection refused on port 4098). The logs show successful startup but nothing is actually listening.

### Symptoms

- `./run.sh dev status` shows Dashboard API as "running" but endpoint as "unhealthy"
- `curl http://localhost:4098/api/health` returns connection refused
- `lsof -i :4098` shows nothing listening
- Logs show "Dashboard running" and "Dashboard started successfully"

### Diagnosis

```bash
# Check if process is running but not bound to port
ps aux | grep "dashboard\|4098" | grep -v grep

# Check if anything is listening on the port
lsof -i :4098

# Check for multiple dashboard processes (indicates orphans)
pgrep -f "tsx.*src/main.ts" | wc -l  # Should be 1, not more
```

### Root Causes

1. **tsx watch mode not exiting cleanly** - The `tsx watch` command spawns child processes that may not receive SIGTERM properly when the parent is killed
2. **Crypto mismatch** causing the server to crash after logging startup (see `personal-crypto-secrets-management` skill)
3. **Multiple dev sessions** - Starting `./run.sh dev` in multiple terminals without stopping the first
4. **Interrupted stop** - Pressing Ctrl+C during `./run.sh dev stop` before cleanup completes

### How `dev stop` Works

The `./run.sh dev stop` command has built-in cleanup:

1. Kills registered PIDs from `.dev-pids/` directory
2. Kills child processes recursively
3. Searches for orphaned tsx processes matching known patterns
4. Checks ports and kills any process still holding them

However, manual intervention is needed when:

- tsx processes were started outside of `run.sh`
- The PID files were deleted but processes remained
- Node processes are in a defunct/zombie state

### Detecting a Failed Stop

After running `./run.sh dev stop`, verify cleanup succeeded:

```bash
# Should show "All instance 0 ports are free"
./run.sh dev stop

# Verify no tsx dashboard processes remain
pgrep -f "tsx.*dashboard" && echo "ORPHANS FOUND" || echo "Clean"

# Verify ports are free
lsof -i :4098 -i :5173 -i :4097 -i :4099 | grep LISTEN && echo "PORTS IN USE" || echo "Ports free"
```

### Recovery

**Step 1: Try clean stop first**

```bash
./run.sh dev stop
```

**Step 2: Check if stop was successful**

```bash
# Count remaining tsx processes (should be 0)
pgrep -f "tsx.*src/main.ts" | wc -l
```

**Step 3: If orphans remain, kill them**

```bash
# Kill tsx processes related to dashboard
pkill -f "tsx.*src/main.ts"

# Kill any process on dashboard port
lsof -ti :4098 | xargs kill -9 2>/dev/null

# Nuclear option: kill all tsx watch processes
pkill -f "tsx.*watch"
```

**Step 4: Wait for processes to exit** (important!)

```bash
# Give processes time to clean up
sleep 2

# Verify they're gone
pgrep -f "tsx.*src/main.ts" || echo "All tsx processes terminated"
```

**Step 5: Restart cleanly**

```bash
./run.sh dev
```

### If the problem persists

Check for crypto/secrets errors in the logs:

```bash
grep -i "error\|crypto\|decrypt" logs/instance-0/dashboard-dev.log | tail -20
```

If you see "Unsupported state or unable to authenticate data", the secrets encryption key has changed. See the `personal-crypto-secrets-management` skill.

## Related Issues

- **Slow dashboard startup**: If the dashboard takes 60+ seconds to start, check if heavy SDKs like `oci-sdk` are being imported at module level. Use dynamic `import()` for lazy-loading.

- **Module resolution errors**: After cleanup, you may need to rebuild dependent packages:

```bash
pnpm run build
```

- **502 Bad Gateway after restart**: Often caused by orphaned processes or crypto key mismatch. Follow the orphaned processes recovery steps above.
