---
name: playwright-demo
description: Record narrated demo videos of the Kagenti platform using Playwright and OpenAI TTS
---

# Playwright Demo Recording

Record demo videos of the Kagenti platform with AI-generated voiceover narration.

## When to Use

- Creating a demo video of the Kagenti platform for presentations
- Recording a walkthrough of a new feature with voiceover
- Generating reproducible video documentation of platform workflows

## Prerequisites

- HyperShift or Kind cluster with Kagenti deployed
- The `playwright-demos` worktree: `.worktrees/playwright-demos/`
- `ffmpeg` and `ffprobe` installed
- `OPENAI_API_KEY` in `.env` for narration (optional -- video-only without it)

## Quick Start

```bash
cd .worktrees/playwright-demos
```

List available tests:

```bash
./local_experiments/run-playwright-demo.sh --cluster-suffix <SUFFIX>
```

Record video only:

```bash
./local_experiments/run-playwright-demo.sh --cluster-suffix <SUFFIX> --test <name>
```

Record video + narration:

```bash
source .env
```

```bash
./local_experiments/run-playwright-demo.sh --cluster-suffix <SUFFIX> --test <name>
```

## Workflow

### On invocation

1. **Write/review test** using `test:playwright` -- verify markStep segments,
   assertions, selectors, and narration alignment
2. **Run test** to verify it passes: `--no-narration` first
3. **Record** video with voiceover: `source .env` then run
4. **Validate alignment** and iterate on narration text
5. **Fix failures** using `playwright-demo:debug` if needed

### Recording pipeline (with OPENAI_API_KEY)

```
Step 1: Fast run -> measure video slot timing per markStep()
Step 2: Generate TTS per [section], inject waitForTimeout() to match
Step 3: Record narration-synced video -> composite voiceover
```

## Test Review Requirements

Before recording, verify every test meets these criteria:

### Section time slots

- Every `markStep()` call is OUTSIDE conditional blocks
- Each section is 3-15 seconds (split longer ones)
- `markStep()` names match `[section]` in narration file 1:1

### Assertive tests (fail if content missing)

Tests MUST use `expect()` assertions, NOT silent `.catch(() => {})`:

```typescript
// REQUIRED - fails if navigation broken
await expect(page).toHaveURL(/\/agents/, { timeout: 10000 });

// REQUIRED - fails if content missing
await expect(element).toBeVisible({ timeout: 5000 });
expect(count).toBeGreaterThan(0);

// REQUIRED - after login
expect(page.url()).not.toContain('/realms/');
```

Keep `.catch()` ONLY for truly optional elements (VERIFY_PROFILE, hover effects).

### Verification

Run the test without narration first to confirm it passes:

```bash
./local_experiments/run-playwright-demo.sh --cluster-suffix <SUFFIX> --test <name> --no-narration
```

If it fails, fix selectors by reading UI source code. Use `playwright-demo:debug`.

## Directory Structure

```
demos/
├── 01-demos/full-platform-walkthrough/
├── 02-ui-pages/{home-overview,agent-detail,...}/
├── 03-workflows/{agent-chat,multi-namespace,...}/
├── 04-observability/{mlflow-traces,kiali-mesh,...}/
└── 05-advanced/{keycloak-admin,env-vars,...}/
```

Each demo directory contains all artifacts:

```
demos/02-ui-pages/home-overview/
├── home-overview.spec.ts              # Test spec (copy)
├── home-overview.txt                  # Narration text (copy)
├── home-overview-timestamps.json      # Step timings
├── audio_segments/                    # Per-section TTS (cached by MD5)
│   ├── intro.mp3 + intro.hash
│   ├── login.mp3 + login.hash
│   └── ...
├── home-overview_YYYY-MM-DD.webm      # Timestamped raw video
├── home-overview_YYYY-MM-DD_voiceover.mp4
├── home-overview_latest.webm          # Latest (overwritten)
└── home-overview_latest_voiceover.mp4
```

Audio segments are cached by MD5 hash -- only changed narration text
triggers TTS regeneration.

## Creating New Demos

1. Add to `demo-map.json`
2. Create `e2e/<name>.spec.ts` with `markStep()`, `expect()`, `demoClick()`
3. Create `narrations/<name>.txt` with `[section]` markers
4. Run and iterate

See `playwright-research` for analyzing UI code to write selectors.

## Google Drive Sync

```bash
./local_experiments/sync-to-gdrive.sh
```

Shows setup instructions for scoped service account. Then:

```bash
./local_experiments/sync-to-gdrive.sh --sync --latest-only
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Validation IDLE gaps | Add narration text to fill the gap |
| Narration overlaps | --sync pipeline adds extra waits automatically |
| Missing markStep timestamp | Move markStep() outside conditional blocks |
| Auth lost after navigation | Use SPA sidebar clicks, not page.goto() |
| Overlapping audio | Fix markStep() calls, check timestamps file |
| Video in wrong directory | Add test to demo-map.json |

## Task Tracking

1. TaskList -- check existing demo recording tasks
2. TaskCreate: `playwright-demos | <cluster> | <test> | <phase>`
3. TaskUpdate as iterations progress

## Related Skills

- `playwright-demo:debug` -- Debug failing Playwright steps
- `playwright-research` -- Analyze UI code, detect changes, plan videos
- `hypershift:cluster` -- Create/manage test clusters
- `k8s:health` -- Verify platform health before recording
