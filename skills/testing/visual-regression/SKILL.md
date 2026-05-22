---
name: visual-regression
description: Screenshot-based regression testing with Playwright. Compares rendered pixels against baseline PNGs. Use when working with stories, *.visual.spec.ts files, or baseline screenshots. Auto-apply when editing files in stories/ or *.visual.spec.ts.
---

# Visual Regression Skill

Orchestrates **screenshot-based regression testing** with Playwright. Compares rendered pixels against baseline PNGs to detect unintended visual changes.

## Specialized Skills

Visual regression has two specialized skills:

| Skill | Purpose | Use When |
|-------|---------|----------|
| `component-screenshot-testing` | React component pixels | Testing UI components, buttons, panels |
| `canvas-filmstrip-testing` | Canvas-rendered matrix progressions | Testing 8-layer filmstrip visualizations |

## Shared Infrastructure

### Directory Structure

```
stories/
  01-bathymetry/
    01-bathymetry.mdx              → MDX story page
    01-bathymetry.visual.spec.ts   → Playwright visual test
    strip-bathymetry-basic.png     → Baseline screenshot (colocated)
  02-energy-field/
  ...
  components/                      → Shared story components
  visual-test-helpers.ts           → Test helper utilities
  App.tsx                          → Story viewer app
```

### Playwright Configuration

```typescript
// playwright.visual.config.js
testDir: './stories',
testMatch: '**/*.visual.spec.ts',
snapshotPathTemplate: 'stories/{testFileDir}/{arg}{ext}',
```

## Commands

```bash
# Verify stories compile (fast, no dev server)
npm run stories:build

# Run visual regression tests
npm run test:visual:headless      # CI/agents
npm run test:visual:headed        # Debugging with browser UI

# Update baselines after intentional changes
npm run test:visual:update:headless
npm run test:visual:update:headed

# Clear test artifacts
npm run reset:visual              # Clear results/reports only
npm run reset:visual:all          # Clear results + colocated baselines

# Start stories dev server for interactive debugging
npm run stories                   # Starts on http://localhost:3001
```

## Interactive Debugging with Chrome DevTools MCP

**IMPORTANT**: Always use the dev server (localhost), NOT `file://` URLs. The `file://` protocol triggers CORS errors.

### Start Dev Server

```bash
npm run stories  # Starts on http://localhost:3001
```

### Launch in Browser

```typescript
mcp__chrome-devtools__new_page({ url: "http://localhost:3001" })

// Navigate to specific page
mcp__chrome-devtools__new_page({ url: "http://localhost:3001/?page=01-bathymetry" })

// With presentation mode and theme
mcp__chrome-devtools__new_page({ url: "http://localhost:3001/?mode=presentation&theme=light" })
```

### Take Snapshots and Screenshots

```typescript
// Get element UIDs
mcp__chrome-devtools__take_snapshot()

// Screenshot specific element
mcp__chrome-devtools__take_screenshot({ uid: "<element-uid>" })

// Reload after changes
mcp__chrome-devtools__navigate_page({ type: "reload" })
```

## Workflow: Data Before Visual

**CRITICAL**: When modifying progression data, verify data first:

1. **Run data tests** - `npx vitest run *Progressions.test.ts`
2. **Verify matrix values** - Check ASCII output shows expected changes
3. **Then update visuals** - Only after data tests pass

```
Wrong: Change coefficient → Update visual → "Looks the same"
Right: Change coefficient → Check matrix → Verify numbers → Update visual
```

## Verifying Stories

After code changes, verify stories still build:

```bash
npm run stories:build
```

This catches broken imports, type errors, missing dependencies.

**Do NOT start dev server** just to verify - use the build.

## Common Issues

### Import Extensions After TS Migration

```typescript
// Wrong
import { foo } from '../state/waveModel.js';

// Correct
import { foo } from '../state/waveModel';
```

### Missing Exports

```typescript
// In *Progressions.ts - ensure strips are exported
export const BATHYMETRY_STRIPS = [BATHYMETRY_STRIP_BASIC];
```

## Related Skills

- **component-screenshot-testing** - React component pixel testing
- **canvas-filmstrip-testing** - Matrix-to-canvas filmstrip testing
- **matrix-data-model-progression-testing** - Data verification before visual
