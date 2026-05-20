---
name: playwright-research
description: Analyze UI code changes to plan, create, and maintain Playwright demo videos - change detection, test writing, video recording lifecycle
---

# Playwright Research - Demo Video Lifecycle

Analyze UI code to determine which demo videos need creation or regeneration,
write Playwright demo tests, validate them, and manage the video lifecycle.

## When to Use

- New feature added to UI -- determine if a new demo is needed
- UI code changed -- check if existing demos need regeneration
- Planning demo coverage -- find uncovered workflows
- Writing new demo tests -- analyze UI code for correct selectors
- Managing TODO_VIDEOS.md -- keep video plan current

## Workflow

```
1. ANALYZE  -> Read UI code, compare against TODO_VIDEOS.md
2. DETECT   -> git diff for UI changes, map to affected videos
3. WRITE    -> Create test spec + narration from UI source analysis
4. VALIDATE -> Run test, fix failures, iterate
5. RECORD   -> Use playwright-demo skill
6. NARRATE  -> Add narration, sync, record voiceover
```

## Phase 1: UI Code Analysis

Read these files to inventory current UI:

```
kagenti/ui-v2/src/App.tsx          # Routes
kagenti/ui-v2/src/pages/           # Page components
kagenti/ui-v2/src/components/      # Shared components
kagenti/ui-v2/src/services/        # API layer
```

Compare against `.worktrees/playwright-demos/TODO_VIDEOS.md`.

## Phase 2: Change Detection

```bash
git diff --name-only HEAD~10 -- kagenti/ui-v2/src/
```

File-to-video mapping in `TODO_VIDEOS.md` section 10 identifies affected demos.

When a component changes, check:
1. **Selector changes** -- update test selectors to match new DOM
2. **Layout changes** -- video may look different, mark for regen
3. **New features** -- add new `markStep()` sections
4. **Removed features** -- remove corresponding sections

## Phase 3: Test Writing

### Analyze UI source for selectors

```typescript
// Read the page component to find element identifiers
// PatternFly Button with onClick -> page.getByRole('button', { name: /text/i })
// PatternFly Tab -> page.getByRole('tab', { name: /text/i })
// Link with React Router -> page.locator('a').filter({ hasText: 'text' })
// Aria label -> page.locator('[aria-label="Select namespace"]')
```

### Test requirements

Every test MUST:
- Call `markStep()` OUTSIDE conditional blocks
- Use `expect()` assertions at every section (not silent `.catch()`)
- Use SPA sidebar clicks for Kagenti pages (not `page.goto()`)
- Use `demoClick()` for visible cursor movement
- Write timestamps to `<test-name>-timestamps.json`
- Have 10s final pause

### Assertion pattern

```typescript
// After login
expect(page.url()).not.toContain('/realms/');

// After navigation
await expect(page).toHaveURL(/\/agents/, { timeout: 10000 });

// Before critical interaction
await expect(element).toBeVisible({ timeout: 5000 });

// After content load
expect(cardCount).toBeGreaterThan(0);
```

## Phase 4: Test Validation

```bash
./local_experiments/run-playwright-demo.sh --cluster-suffix <SUFFIX> --test <name> --no-narration
```

If it fails: read UI source, update selectors, re-run. Use `playwright-demo:debug`.

## Phase 5-6: Recording and Narration

Use `playwright-demo` skill for recording and voiceover.

## Architecture: Segments and Timing

```
markStep('section') -> records timestamp
                    -> sync-narration.py generates TTS, measures duration
                    -> if narration > video slot: inject waitForTimeout()
                    -> add-voiceover.py positions audio at timestamp
                    -> audio_segments/<section>.mp3 cached by MD5 hash
```

## File Layout

```
.worktrees/playwright-demos/local_experiments/
├── demo-map.json           # Test name -> output dir mapping
├── e2e/*.spec.ts           # Source test specs (22 tests)
├── narrations/*.txt        # Narration text files
├── demos/                  # Output: nested by category
│   ├── 01-demos/           # Original walkthrough
│   ├── 02-ui-pages/        # UI page demos
│   ├── 03-workflows/       # Multi-page workflow demos
│   ├── 04-observability/   # External app demos
│   └── 05-advanced/        # Advanced feature demos
├── run-playwright-demo.sh  # Main entry script
├── add-voiceover.py        # TTS + FFmpeg compositing
├── sync-narration.py       # Narration timing sync
└── sync-to-gdrive.sh       # Google Drive upload
```

## TODO_VIDEOS.md Status Markers

| Status | Meaning |
|--------|---------|
| `[NEW]` | Needs test + narration |
| `[WIP]` | Test exists, needs iteration |
| `[DONE]` | Test passes, video recorded |
| `[REGEN]` | UI changed, needs re-recording |

## Task Tracking

1. TaskCreate: `playwright-research | <phase> | <scope>`
2. TaskUpdate as work progresses

## Related Skills

- `playwright-demo` -- Record demo videos (Phase 5-6)
- `playwright-demo:debug` -- Debug failing tests (Phase 4)
- `k8s:health` -- Verify platform health before testing
