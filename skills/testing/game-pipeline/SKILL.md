---
name: game-pipeline
description: "Game lifecycle orchestrator: scaffold, assets, audio, QA, deploy."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Edit
  - Task
routing:
  triggers:
    - make game
    - game pipeline
    - game audio
    - add audio game
    - game testing
    - game qa
    - playtest
    - deploy game
    - ship game
    - promo video
    - record gameplay
    - game polish
    - add juice
    - screen shake
    - capacitor ios
  pairs_with:
    - threejs-builder
    - phaser-gamedev
    - game-asset-generator
  complexity: Complex
  category: game-development
---

# Game Pipeline Skill

## Overview

This skill orchestrates the full game development lifecycle: SCAFFOLD → ASSETS → DESIGN → AUDIO → QA → DEPLOY. Each phase can be entered independently — you do not need to start from SCAFFOLD. The orchestrator never writes game code directly; it delegates each phase to the appropriate engine-specific skill or domain reference.

**Scope**: Use for any browser-based game (Three.js, Phaser, or vanilla canvas), cross-cutting concerns that span engines (audio, QA, promo, deploy), and iOS export via Capacitor. Skip Unity/Godot/native engines, non-game web apps, and server-side logic.

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| `references/game-audio.md` | `game-audio.md` | AUDIO |
| `references/game-qa.md` | `game-qa.md` | QA |
| `references/game-designer.md` | `game-designer.md` | DESIGN |
| `references/promo-video.md` | `promo-video.md` | DEPLOY |
| `references/deploy.md` | `deploy.md` | DEPLOY |
| `references/capacitor-ios.md` | `capacitor-ios.md` | DEPLOY |

## Instructions

### Entry Point Detection

**Before executing any phase**, determine which phase applies:

| User request | Entry phase |
|---|---|
| "make a game", "start a game", "new game" | SCAFFOLD |
| "generate assets", "add sprites", "need art" | ASSETS |
| "add juice", "game feels flat", "particles", "screen shake" | DESIGN |
| "add audio", "background music", "sound effects" | AUDIO |
| "test my game", "visual regression", "playwright", "game qa" | QA |
| "deploy", "ship", "publish", "github pages", "promo video", "ios" | DEPLOY |

If the entry phase is not SCAFFOLD, skip to that phase. Phases are independently re-enterable.

---

### Phase 1: SCAFFOLD

**Goal**: Initialize the project and delegate engine-specific setup.

**Step 1: Detect engine**

| Signal | Engine | Delegate to |
|---|---|---|
| `import * as THREE`, three.js in package.json | Three.js | `threejs-builder` skill |
| `new Phaser.Game()`, phaser in package.json | Phaser | `phaser-gamedev` skill |
| No engine signal | Ask user before proceeding | — |

**Step 2: Initialize project structure**

```
game/
├── index.html
├── src/
│   └── main.js
├── assets/
│   └── assets_index.json   # Asset manifest (required for Capacitor iOS)
└── dist/                   # Build output
```

`assets_index.json` format:
```json
{
  "version": "1.0",
  "assets": {
    "player": "assets/player.png",
    "bgm": "assets/music.ogg"
  }
}
```

**Step 3: Wire EventBus**

Every game needs an EventBus before any feature — it is the integration contract that lets audio, effects, and analytics attach without touching game logic:

```javascript
// src/EventBus.js
export const EventBus = new EventTarget();
export const emit = (name, detail = {}) =>
  EventBus.dispatchEvent(new CustomEvent(name, { detail }));
export const on = (name, fn) =>
  EventBus.addEventListener(name, (e) => fn(e.detail));
```

Pre-wire these event names so downstream phases attach immediately:
`ENEMY_HIT`, `PLAYER_DEATH`, `LEVEL_UP`, `GAME_OVER`, `SCORE_CHANGE`, `SPECTACLE_*`

**Gate**: Engine chosen, project structure created, EventBus wired.

---

### Phase 2: ASSETS

**Goal**: Source or generate game assets and register them in the asset manifest.

**Step 1: Audit what exists**

```bash
ls assets/
cat assets/assets_index.json
```

**Step 2: Delegate to game-asset-generator**

Dispatch a subagent with: asset list, art style, output format (PNG spritesheet for Phaser, GLB for Three.js), target path `assets/`.

**Step 3: Update asset manifest**

After generation, update `assets/assets_index.json`. This manifest is read by both the web game and the Capacitor iOS wrapper — use relative paths only.

**Gate**: All assets generated, manifest updated, assets load in-game without errors.

---

### Phase 3: DESIGN

**Goal**: Add visual polish and "juice" — effects that make a game feel great.

**Load reference**: Read `references/game-designer.md` for patterns.

**Key principle**: Design polish wires to the EventBus, not to game logic. Effects can be added, removed, or swapped without touching gameplay code.

**Core effects**:

| Effect | Trigger event | Impact |
|---|---|---|
| Screen shake | `ENEMY_HIT`, `EXPLOSION` | Impact weight |
| Hit freeze frame | `ENEMY_HIT` (big) | Dramatic pause |
| Particle burst | `ENEMY_HIT`, `GAME_OVER` | Visual feedback |
| Floating score text | `SCORE_CHANGE` | Progress reward |
| Combo text | `COMBO_REACHED` | Achievement surge |

**Opening moment rule**: The first 3 seconds must hook the player — immediate visual spectacle, never a loading screen or empty scene.

**Gate**: At least 3 juice effects wired to EventBus events. Opening moment is compelling. No effects hardcoded into gameplay logic.

---

### Phase 4: AUDIO

**Goal**: Add background music and sound effects using Web Audio API.

**Load reference**: Read `references/game-audio.md` for patterns.

**Key constraint**: Create `AudioContext` only on first user interaction — browser autoplay policy silently blocks contexts created before a gesture.

**AudioManager pattern**:
```javascript
// src/AudioManager.js
let ctx = null;
export function getCtx() {
  if (!ctx) ctx = new AudioContext();
  return ctx;
}
```

**AudioBridge — wire to EventBus**:
```javascript
import { on } from './EventBus.js';
import { getCtx } from './AudioManager.js';

on('ENEMY_HIT', () => playSFX('hit'));
on('LEVEL_UP',  () => { stopBGM(); startBGM('level2'); });
on('GAME_OVER', () => playSFX('gameover'));
```

**Volume hierarchy**: master gain → category gains (music, sfx, ambient) → individual sources. Never set volume directly on sources.

**Gate**: AudioContext created on user interaction only. BGM plays. At least 2 SFX events wired. Volume controls work.

---

### Phase 5: QA

**Goal**: Automated testing via Playwright with visual regression and canvas test seams.

**Load reference**: Read `references/game-qa.md` for patterns.

**Scripts** (run from project root):
```bash
python3 skills/game/game-pipeline/scripts/imgdiff.py baseline.png current.png
python3 skills/game/game-pipeline/scripts/with_server.py "npx playwright test"
```

**Test seam** — inject into game bootstrap:
```javascript
const TEST_MODE = new URLSearchParams(location.search).get('test') === '1';
const SEED = parseInt(new URLSearchParams(location.search).get('seed') || '0');
if (TEST_MODE) window.__TEST__ = { seed: SEED, state: null };
```

**Visual regression workflow**:
1. Take baseline: `npx playwright screenshot --save-as baseline.png`
2. Make change
3. Diff: `python3 skills/game/game-pipeline/scripts/imgdiff.py baseline.png current.png`
4. RMS > 5.0 means investigate the diff image

**Gate**: At least 1 Playwright test passes. Visual baseline captured. Canvas test seam exists.

---

### Phase 6: DEPLOY

**Goal**: Ship the game to a live URL.

**Load reference**: Read `references/deploy.md`. Load `references/capacitor-ios.md` if iOS export needed.
Load `references/promo-video.md` if recording gameplay for social.

**Pre-deploy checklist** (mandatory before any deploy):
```bash
npm run build
ls dist/
grep -r "localhost" dist/ && echo "FAIL: localhost refs" || echo "OK"
grep -r 'src="/' dist/ && echo "WARN: absolute paths" || echo "OK"
```

**Deploy targets**:

| Target | Command | Notes |
|---|---|---|
| GitHub Pages | `npx gh-pages -d dist` | Public repo or GitHub Pro |
| Vercel | `vercel --prod` | Best for preview URLs |
| Static host | Upload `dist/` | Works anywhere |
| iOS (Capacitor) | See `capacitor-ios.md` | Requires Xcode |

**Gate**: Build succeeds. Deploy URL live. Game loads. No console errors.

---

## Error Handling

### Error: AudioContext Blocked
**Cause**: `AudioContext` created outside a user gesture handler
**Fix**: Use the `getCtx()` lazy-init pattern from `game-audio.md`. First call must happen inside click/keydown handler.

### Error: Playwright Can't Interact With Canvas
**Cause**: No test seams, non-deterministic state, or missing readiness signal
**Fix**: Add `window.__TEST__` with `?test=1&seed=42`. Wait for `game.events.once('ready')` before asserting. Use `render_game_to_text()` to expose state as text.

### Error: imgdiff.py FAIL With Unexpected Diff
**Cause**: Font rendering or anti-aliasing differences between platforms
**Fix**: `python3 skills/game/game-pipeline/scripts/imgdiff.py a.png b.png --tolerance 10.0`. If still failing, retake baseline on the same platform.

### Error: Capacitor iOS Build Fails
**Cause**: Absolute paths in `dist/`, missing `webDir` config, or CocoaPods conflict
**Fix**: All asset paths must be relative. Check `capacitor.config.ts` has `webDir: 'dist'`. Capacitor 5+ uses SPM — run `npx cap sync`, not `pod install`. See `capacitor-ios.md`.

### Error: Assets Missing After Deploy
**Cause**: Absolute asset paths (`/assets/player.png` instead of `assets/player.png`)
**Fix**: `grep -r '"/assets/' dist/`. Fix paths in build config or source — use relative paths everywhere.

### Error: Promo Video Looks Choppy
**Cause**: Screenshot rate too slow or FFmpeg framerate mismatch
**Fix**: Use CDP screencast instead of screenshot loop. Set game speed to 0.5 before recording, encode with `-r 50` in FFmpeg. See `promo-video.md`.

---

## References

| Reference | Phase | Content |
|---|---|---|
| `references/game-audio.md` | AUDIO | Web Audio API: AudioManager, BGM sequencer, SFX pool, AudioBridge, volume hierarchy |
| `references/game-qa.md` | QA | Playwright: visual regression, canvas seams, deterministic mode, imgdiff patterns |
| `references/game-designer.md` | DESIGN | Juice: particles, screen shake, hit freeze, combo text, spectacle events |
| `references/promo-video.md` | DEPLOY | Slow-mo trick, Playwright recording, FFmpeg assembly, mobile portrait format |
| `references/deploy.md` | DEPLOY | GitHub Pages, Vercel, static hosting, pre-deploy checklist |
| `references/capacitor-ios.md` | DEPLOY | Capacitor 5+ iOS: SPM setup, asset contracts, touch controls, debugging |
