---
name: canvas-filmstrip-testing
description: Visual regression for canvas-rendered matrix progressions. Tests filmstrip strips that show how 2D data evolves visually over time. Auto-apply when editing *Progressions.ts strip definitions or stories with filmstrip components.
---

# Canvas Filmstrip Testing Skill

Tests **canvas-rendered filmstrips** that visualize how matrix data (energy fields, foam grids, etc.) evolves over simulated time. Each strip shows multiple frames side-by-side.

This is about **visual rendering** of data progressions. It catches:

- Color scale/gradient changes
- Canvas rendering bugs
- Missing or misaligned frames
- Incorrect visual interpolation

For the underlying data correctness, see `matrix-data-model-progression-testing` first.

## When to Use This

- Verifying canvas-rendered strips match expected appearance
- Testing color scales and gradients
- Debugging visual artifacts in filmstrip rendering
- Validating that progression data renders correctly

## The 8-Layer Visual Pipeline

Each layer tests a specific aspect of the wave physics simulation:

| Layer | Story | Progressions File |
|-------|-------|-------------------|
| 1 | 01-bathymetry | `src/render/bathymetryProgressions.ts` |
| 2 | 02-energy-field | `src/state/energyFieldProgressions.ts` |
| 3 | 03-shoaling | `src/render/shoalingProgressions.ts` |
| 4 | 04-wave-breaking | `src/render/waveBreakingProgressions.ts` |
| 5 | 05-energy-transfer | `src/render/energyTransferProgressions.ts` |
| 6 | 06-foam-grid | `src/render/foamGridProgressions.ts` |
| 7 | 07-foam-dispersion | `src/render/foamDispersionProgressions.ts` |
| 8 | 08-foam-contours | `src/render/foamContoursProgressions.ts` |

## Architecture

```
stories/
  01-bathymetry/
    01-bathymetry.mdx              → MDX story page
    01-bathymetry.visual.spec.ts   → Playwright visual test
    strip-bathymetry-basic.png     → Baseline screenshot (colocated)
    strip-bathymetry-features.png
  02-energy-field/
  ...

src/render/*Progressions.ts        → Progression data + strip definitions
```

## Strip Definition Pattern

Each progression file exports strips for visual testing:

```typescript
// src/render/bathymetryProgressions.ts
export const BATHYMETRY_STRIP_BASIC = {
  testId: 'strip-bathymetry-basic',
  pageId: '01-bathymetry',
  snapshots: PROGRESSION_BATHYMETRY_BASIC.snapshots,
};

export const BATHYMETRY_STRIPS = [
  BATHYMETRY_STRIP_BASIC,
  BATHYMETRY_STRIP_FEATURES,
];
```

## Visual Test Pattern

```typescript
// stories/01-bathymetry/01-bathymetry.visual.spec.ts
import { BATHYMETRY_STRIPS } from '../../src/render/bathymetryProgressions';
import { defineStripVisualTests } from '../visual-test-helpers';

defineStripVisualTests(BATHYMETRY_STRIPS);
```

## Commands

```bash
# Run visual tests
npm run test:visual:headless        # CI/agents
npm run test:visual:headed          # Debugging with browser UI

# Update baselines after intentional changes
npm run test:visual:update:headless
npm run test:visual:update:headed

# Clear test artifacts
npm run reset:visual                # Clear results/reports only
npm run reset:visual:all            # Clear results + colocated baselines

# Start dev server for interactive debugging
npm run stories                     # Starts on http://localhost:3001
```

## Workflow: Data First, Then Visual

**CRITICAL**: Always verify data before visual testing.

```
Wrong workflow:
  Change coefficient → Update visual snapshot → "Looks the same, try higher"

Correct workflow:
  Change coefficient → Run npx vitest run *Progressions.test.ts →
  Verify matrix values changed → Then update visual if needed
```

1. **Verify data with ASCII** - Run `*Progressions.test.ts`
2. **If data correct, update visual** - `npm run test:visual:update:headless`
3. **If data wrong, fix logic first** - Don't touch visuals

## Mapping testId to Source

When a visual test fails:

1. **testId** like `strip-bathymetry-basic` → `BATHYMETRY_STRIP_BASIC` in progressions file
2. **pageId** like `01-bathymetry` → `stories/01-bathymetry/` folder
3. **Pattern**: `strip-{layer}-{variant}` → `*{layer}Progressions.ts`

## Debugging with Chrome DevTools MCP

```typescript
// Start dev server
npm run stories

// Open specific story page
mcp__chrome-devtools__new_page({
  url: "http://localhost:3001/?page=01-bathymetry"
})

// Take snapshot to find strip UIDs
mcp__chrome-devtools__take_snapshot()

// Screenshot the strip element
mcp__chrome-devtools__take_screenshot({ uid: "<strip-uid>" })

// After code changes, reload and compare
mcp__chrome-devtools__navigate_page({ type: "reload" })
mcp__chrome-devtools__take_screenshot({ uid: "<strip-uid>" })
```

## Common Issues

### Visual Differs but Data is Correct

Check:
- Color scale mapping (value → color)
- Canvas context settings (smoothing, etc.)
- Cell sizing/spacing in strip renderer

### Visual Passes but Looks Wrong

The baseline may be incorrect. Manually verify:
1. Start dev server: `npm run stories`
2. Navigate to the story
3. Visually inspect the strip
4. If wrong, update baseline: `npm run test:visual:update:headless`

## Related Skills

- **matrix-data-model-progression-testing** - Verify data correctness first
- **component-screenshot-testing** - For React UI component screenshots
- **visual-regression** - Shared infrastructure and commands
- **visualization-algorithms** - Canvas rendering algorithms
