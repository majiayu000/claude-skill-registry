---
name: fix
description: Debugs and fixes issues systematically. Use when something is broken, throwing errors, or behaving unexpectedly.
user-invocable: true
triggers:
  - fix
  - debug
  - broken
  - error
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
model: opus
argument-hint: "[error or file]"
---

# Fix Workflow

## On "fix" or "debug"

### Step 1: Identify the Problem
```
question: "What's the issue?"
options:
  - { label: "Build error", description: "npm run build fails" }
  - { label: "Runtime error", description: "App crashes or throws" }
  - { label: "UI bug", description: "Something looks wrong" }
  - { label: "I'll describe it", description: "Custom issue" }
```

### Step 2: Gather Context

**Build error:**
```bash
npm run build 2>&1
# Capture and parse error output
```

**Runtime error:**
```bash
# Check browser console
agent-browser run --task "Go to localhost:3000, open dev console, report any errors"
# Or check server logs
npm run dev 2>&1 | tail -50
```

**UI bug:**
```bash
# Take screenshot
agent-browser run --task "Go to localhost:3000/[page], screenshot the issue"
# Inspect element
agent-browser run --task "Inspect [element], report CSS and structure"
```

### Step 3: Analyze Root Cause

Common patterns:
| Error Type | Likely Cause |
|------------|--------------|
| `Cannot find module` | Missing import or package |
| `Type 'X' is not assignable` | TypeScript mismatch |
| `undefined is not a function` | Null/undefined access |
| `Hydration mismatch` | Server/client render diff |
| `CORS error` | API endpoint config |
| `401 Unauthorized` | Auth token issue |

### Step 4: Fix

1. Make the minimal change needed
2. Don't refactor unrelated code
3. Don't add "improvements"
4. Test the fix immediately

### Step 5: Verify
```bash
npm run build
# If passes, test the specific feature
```

If build or feature test fails, return to Step 4 with updated error info. Maximum 3 fix attempts — if still failing after 3 tries, report the remaining issue and stop.

### Step 6: Document
```
Append to progress.txt:
"## [DATE]: Fixed [issue]
- Root cause: [explanation]
- Solution: [what was changed]
- Files: [list of modified files]"
```

## Quick Fix Commands

| Say | Action |
|-----|--------|
| `fix build` | Run build, auto-fix errors |
| `fix types` | Fix TypeScript errors only |
| `fix [file]` | Focus on specific file |

## Common Auto-Fixes

**Missing import:**
```typescript
// Add at top of file
import { Thing } from './path'
```

**Null safety:**
```typescript
// Before
obj.property
// After
obj?.property
```

**Type assertion:**
```typescript
// When type is known but TS doesn't infer
(value as ExpectedType)
```

## When to Stop

STOP and ask user if:
- Fix requires architectural change
- Multiple valid approaches exist
- Fix might break other features
- Root cause is unclear after 3 attempts
