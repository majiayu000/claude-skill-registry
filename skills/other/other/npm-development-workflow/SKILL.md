---
name: npm-development-workflow
description: |
  CRITICAL workflow for developing and testing NextSpark in dual-mode: monorepo AND npm.
  ALL changes MUST be validated in both environments before publishing.
  Defines the exact methodology, commands, and validation steps.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
version: "1.0"
---

# NPM Development Workflow

## GOLDEN RULE

> **EVERY change to core packages MUST be tested in BOTH modes before publishing.**
> - Monorepo mode: `/repo` (port 5173)
> - npm mode: `/projects/my-app` (port 3000)

---

## Philosophy: Root Cause Analysis

> **NOTHING in core is sacred. Challenge the status quo.**
>
> If you find disconnected systems, incoherent patterns, or code not designed for npm distribution,
> **propose architectural changes**. Quality and professionalism over legacy code preservation.

### The 7-Question Framework

Before fixing ANY issue, ask:

```
1. What is the SYMPTOM? (error message, behavior)
2. What is the IMMEDIATE cause? (the line that fails)
3. What is the ROOT cause? (why does that code exist/fail?)
4. Does this affect monorepo mode? npm mode? Both?
5. Will my fix work in BOTH modes?
6. Is this a DESIGN FLAW in core? (disconnected systems, missing abstraction, wrong assumptions)
7. Should we FIX THE DESIGN instead of patching the symptom?
```

### Questioning Core Design

**When you find a bug, ask yourself:**

| Question | If YES → Action |
|----------|-----------------|
| Are there TWO systems doing the same thing? | **Unify them** - One source of truth |
| Does this code assume monorepo-only execution? | **Redesign for npm** - npm users are priority |
| Is there a "clever" workaround that's fragile? | **Replace with explicit solution** |
| Does fixing this require touching 5+ files? | **The abstraction is wrong** - Refactor first |
| Will this fix break if someone changes X? | **Make it robust** - Don't create time bombs |
| Is there duplicated logic across client/server? | **Create shared module** with proper boundaries |

### Real Example: Entity Registry Issue

**Symptom:** `Entity not found` in API routes (npm mode only)

**Bad approach (patch):**
```typescript
// Just add a try-catch and fallback
try {
  return entityRegistry.get(slug)
} catch {
  return null // Hide the problem
}
```

**Good approach (question the design):**
```
Q: Why does this fail in npm mode?
A: There are TWO registry systems that don't sync.

Q: Why are there two systems?
A: Historical accident - one was added for client, one for server.

Q: Is this a design flaw?
A: YES - violates single source of truth.

SOLUTION: Unify into ONE system with FACADE pattern.
```

**Result:** EntityRegistry became a facade that delegates to the singleton.
Problem solved at the root, not patched.

### Priority Order for Changes

When designing solutions, prioritize in this order:

```
1. npm mode user experience (they can't debug our code)
2. Security (no exposed internals, no unsafe patterns)
3. Performance (bundle size, runtime efficiency)
4. Developer experience (clear errors, good types)
5. Monorepo convenience (last priority - we can work around issues)
```

### Signs of Design Problems to Challenge

| Pattern You Find | What It Indicates | Action |
|------------------|-------------------|--------|
| `require()` in client code | Server/client boundary violation | Restructure module |
| Multiple registries for same data | Accidental complexity | Unify systems |
| Webpack aliases in runtime | Monorepo-only thinking | Use explicit imports |
| "Works in dev, fails in prod" | Missing abstraction | Design for production first |
| Complex initialization order | Implicit dependencies | Make dependencies explicit |
| `if (process.env.NODE_ENV)` everywhere | Missing proper configuration | Create config system |
| Duplicated types across packages | Missing shared types package | Centralize types |
| "Magic" that's hard to trace | Over-engineering | Simplify ruthlessly |

### Common Root Causes in Dual-Mode Systems

| Symptom | Immediate Cause | Root Cause (Question the Design) |
|---------|-----------------|----------------------------------|
| `require is not defined` | Using `require()` in browser | **Design flaw:** Client code has server dependencies |
| `Entity not found` in API | Registry not populated | **Design flaw:** Multiple disconnected registry systems |
| `Module not found` in npm | Webpack alias not resolved | **Design flaw:** Code assumes build-time resolution |
| `Context provider missing` | Component outside provider tree | **Design flaw:** Implicit provider assumptions |
| Hydration mismatch | Server/client render differently | **Design flaw:** Shared state not properly serialized |

### Decision Framework

```
Can I use dynamic imports? → NO in most cases (breaks npm mode)
Can I use require()? → ONLY in server-only files with 'import server-only'
Can I use webpack aliases in runtime code? → NO (won't resolve in npm packages)
Should I fix just the error? → NO, trace to root cause first
Should I question if this is a design flaw? → YES, ALWAYS
```

### When to Propose Architectural Changes

**DO propose changes when:**
- The same bug class keeps appearing
- A fix requires "magic" or complex workarounds
- You need to explain "why" something works a certain way
- npm mode requires special handling that monorepo doesn't
- You find yourself adding defensive code for edge cases

**Template for proposing changes:**

```markdown
## Proposed Architectural Change

### Current State
[What exists now and why it's problematic]

### Root Cause
[The design decision that led to this problem]

### Proposed Solution
[New architecture that solves the root cause]

### Migration Path
[How to get from current to proposed]

### Validation
[How to verify in both monorepo and npm modes]
```

---

## Environment Setup

### Directory Structure

```
nextspark/
├── repo/                    # Monorepo (development)
│   ├── packages/
│   │   ├── core/            # @nextsparkjs/core
│   │   ├── cli/             # @nextsparkjs/cli
│   │   └── create-nextspark-app/
│   ├── themes/              # @nextsparkjs/theme-*
│   ├── plugins/             # @nextsparkjs/plugin-*
│   ├── apps/dev/            # Development app
│   └── .packages/           # Packed .tgz files
│
└── projects/
    └── my-app/              # npm mode test project
        ├── .packages/       # Local .tgz files
        └── package.json     # file: references to .packages/
```

### Ports

| Environment | Port | URL |
|-------------|------|-----|
| Monorepo (`repo/`) | 5173 | http://localhost:5173 |
| npm mode (`projects/my-app/`) | 3000 | http://localhost:3000 |

---

## Development Workflow

### Phase 1: Develop in Monorepo

```bash
cd repo

# Make changes to packages/core, packages/cli, themes/, plugins/
# ...

# Start dev server
pnpm dev

# Test at http://localhost:5173
```

### Phase 2: Validate in Monorepo

Before moving to npm mode, verify:

```bash
# 1. TypeScript compiles
pnpm tsc --noEmit

# 2. Build succeeds
pnpm build

# 3. Manual testing checklist:
#    [ ] Server starts without errors
#    [ ] No console errors in browser
#    [ ] API endpoints respond correctly
#    [ ] Dashboard loads entities
#    [ ] CRUD operations work (after login)
```

### Phase 3: Update npm Test Project

```bash
# ONE COMMAND does everything:
pnpm setup:update-local

# This script:
# 1. Builds all packages
# 2. Creates .tgz files in repo/.packages/
# 3. Copies .tgz to my-app/.packages/
# 4. Updates my-app/package.json with file: references
# 5. Cleans .next cache
# 6. Runs pnpm install --force
```

**Options:**
```bash
pnpm setup:update-local                      # Full rebuild + update
pnpm setup:update-local -- --skip-build      # Skip rebuild (faster)
pnpm setup:update-local -- --target ../projects/other-app  # Different target
```

### Phase 4: Validate in npm Mode

```bash
cd ../projects/my-app

# Start dev server
pnpm dev

# Test at http://localhost:3000
```

**CRITICAL Validation Checklist:**
```
[ ] Server starts without errors
[ ] No "require is not defined" errors
[ ] No "Module not found" errors
[ ] API returns correct responses (not "Entity not found")
[ ] Dashboard sidebar shows entities
[ ] CRUD create/edit/delete works
[ ] No hydration mismatches in console
```

### Phase 5: Publish (if both pass)

```bash
cd ../repo

# 1. Increment version
pnpm pkg:version -- patch   # or minor, major, beta

# 2. Package
pnpm pkg:pack

# 3. Publish
pnpm pkg:publish -- --tag latest   # or --tag beta

# 4. Commit
git add .
git commit -m "release: vX.Y.Z - description"
git push
```

---

## Quick Reference Commands

### From `/repo`:

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Start monorepo dev server (port 5173) |
| `pnpm build` | Build monorepo |
| `pnpm setup:update-local` | **Repackage ALL + update my-app** |
| `pnpm setup:update-local -- --skip-build` | Repackage without rebuild |
| `pnpm pkg:version -- patch` | Increment version |
| `pnpm pkg:pack` | Create .tgz files |
| `pnpm pkg:publish -- --tag latest` | Publish to npm |

### From `/projects/my-app`:

| Command | Purpose |
|---------|---------|
| `pnpm dev` | Start npm mode dev server (port 3000) |
| `pnpm build` | Build npm mode project |

---

## When to Reset my-app from Scratch

Reset the npm test project when:

1. **CLI/wizard changes** - The init process itself changed
2. **Template changes** - Generated files structure changed
3. **After 3-5 consecutive releases** - Accumulated drift
4. **Unexplainable npm-only bugs** - Fresh install isolates issues

### Reset Command

```bash
cd ../projects
rm -rf my-app
npx --yes create-nextspark-app@latest my-app
cd my-app
pnpm nextspark add:theme @nextsparkjs/theme-default
pnpm dev
```

---

## Debugging Dual-Mode Issues

### Issue: Works in monorepo, fails in npm

**Diagnosis:**
```bash
# Check what's different
diff repo/packages/core/src/file.ts projects/my-app/node_modules/@nextsparkjs/core/dist/file.js

# Check if using runtime aliases
grep -r "require.*@nextsparkjs" repo/packages/core/src/

# Check for 'use client' with server code
grep -l "'use client'" repo/packages/core/src/**/*.ts | xargs grep -l "require("
```

**Common fixes:**
1. Move server-only code to files WITHOUT `'use client'`
2. Replace runtime `require()` with build-time imports
3. Use dependency injection instead of dynamic resolution

### Issue: Registry not populated in npm mode

**Root cause:** Multiple registry systems not synchronized

**Pattern to follow:**
```typescript
// API routes MUST initialize registry
import { setEntityRegistry, isRegistryInitialized } from '@nextsparkjs/core/lib/entities/queries'
import { ENTITY_REGISTRY, ENTITY_METADATA } from '@nextsparkjs/registries/entity-registry'

if (!isRegistryInitialized()) {
  setEntityRegistry(ENTITY_REGISTRY, ENTITY_METADATA)
}
```

### Issue: Different behavior between modes

**Diagnosis:**
```bash
# Compare installed versions
cat projects/my-app/node_modules/@nextsparkjs/core/package.json | grep version
cat repo/packages/core/package.json | grep version

# Check if local packages are being used
cat projects/my-app/package.json | grep "file:"
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| Testing only in monorepo | npm mode has different module resolution | ALWAYS test both |
| Using `require()` in client code | Browser doesn't have `require` | Use ES imports or move to server |
| Hardcoding webpack aliases | Aliases don't work in pre-compiled packages | Use explicit paths or dependency injection |
| Fixing symptoms not causes | Creates fragile patches | Trace to root cause first |
| Publishing without npm test | Breaks users' projects | Run full dual-mode validation |
| Skipping `.next` cache clear | Stale modules cause confusion | `setup:update-local` does this automatically |

---

## Validation Checklist (Copy-Paste)

Before ANY publish, verify ALL items:

```markdown
## Pre-Publish Checklist

### Monorepo (port 5173)
- [ ] `pnpm tsc --noEmit` passes
- [ ] `pnpm build` succeeds
- [ ] Server starts without errors
- [ ] API endpoints respond correctly
- [ ] Dashboard loads with entities
- [ ] CRUD operations work

### npm mode (port 3000)
- [ ] `pnpm setup:update-local` completed
- [ ] Server starts without errors
- [ ] No console errors in browser
- [ ] API endpoints respond correctly (not "Entity not found")
- [ ] Dashboard loads with entities
- [ ] CRUD operations work
- [ ] No hydration mismatches

### Ready to publish
- [ ] Both modes validated
- [ ] Version incremented: `pnpm pkg:version -- <type>`
- [ ] Changes committed to git
```

---

## Related Skills

- **`monorepo-architecture`** - Package structure and dependencies
- **`registry-system`** - How registries work
- **`entity-system`** - Entity configuration
- **`create-plugin`** - Plugin creation with correct dependencies

---

## Script Reference

### `update-local.sh`

Location: `repo/scripts/setup/update-local.sh`

```bash
# Usage
./scripts/setup/update-local.sh [options]

# Options
--target <path>    # Target project (default: ../projects/my-app)
--skip-build       # Skip building packages
--skip-install     # Skip pnpm install

# What it does
1. Runs pack.sh --all (build + package)
2. Copies .tgz to target/.packages/
3. Updates package.json with file: references
4. Cleans .next cache
5. Runs pnpm install --force
```

### `pack.sh`

Location: `repo/scripts/packages/pack.sh`

```bash
# Package all
./scripts/packages/pack.sh --all

# Package specific
./scripts/packages/pack.sh --package core --package cli

# Skip rebuild
./scripts/packages/pack.sh --all --skip-build
```
