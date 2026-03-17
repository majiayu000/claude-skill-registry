---
name: 50-01-video-based-nhitl-testing
description: Visual verification loop combining Playwright video recording with video-explorer frame extraction for autonomous behavior debugging.
---

# 50.01 Video-Based NHITL Testing

## Problem

E2E tests check **state labels** (e.g., `action === 'Engage'`) but not **actual behaviors** (e.g., projectiles fired, damage dealt). A test can "pass" while the feature is completely broken.

## Solution: Visual Verification Loop

Combine Playwright video recording with video-explorer frame extraction to enable you to visually debug test failures without human involvement.

### Flow

```
1. Run E2E test with video recording enabled
2. Test completes (pass or fail)
3. Extract frames from test-results/*.webm using video-explorer
4. You analyze frames visually:
   - "Frame 00:03: Label shows 'Engage'"
   - "Frame 00:03-00:08: No projectiles visible"
   - "Diagnosis: Engage state set but weapon not firing"
5. Fix the actual issue (not just make test pass)
6. Re-run and verify visually
```

### Configuration

```typescript
// playwright.config.ts
use: {
  video: 'on',  // Record ALL tests, not just failures
}
```

### Video Analysis Commands

```bash
# Overview of test video
videx overview test-results/<test-name>/video.webm 1 480

# Zoom into specific moment
videx range test-results/<test-name>/video.webm 0:03-0:08 --fps=5

# Single frame detail
videx zoom test-results/<test-name>/video.webm 0:05
```

### What to Look For

Adapt this table to your project's visual indicators:

| Behavior | Visual Indicator |
|----------|------------------|
| Action triggered | UI element changes state |
| Animation playing | Sprite/element visible in frames |
| State transition | Labels/overlays change |
| Error state | Error UI appears |

### Benefits

1. **True behavior verification** - see what actually happens, not just state changes
2. **NHITL debugging** - You watch the video, find problems autonomously
3. **Evidence-based fixes** - know exactly what's broken before coding
4. **Regression detection** - visual diff between expected and actual behavior
