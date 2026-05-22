---
name: develop-web-game
description: >-
  Use when building or iterating on an HTML5 Canvas web game and you need a
  reliable develop-test loop: implement a small change, run the bundled
  Playwright test script with action bursts and deterministic time stepping,
  inspect screenshots and render_game_to_text output, review console errors,
  and fix issues before the next iteration. Covers canvas layout, game state
  exposure, progress tracking, and automated visual verification.
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - guide
    - web-game
    - html5-canvas
    - playwright
    - testing
    - game-development
  provenance:
    upstream_source: "develop-web-game"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:54:11Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Develop Web Game

Build HTML5 Canvas games in small steps and validate every change through an automated Playwright test loop: implement, act, pause, observe, adjust.

## Overview

This guide teaches an iterative development workflow for browser-based games rendered on an HTML5 Canvas element. Each cycle follows a tight feedback loop:

1. Pick a single feature or behavior to implement
2. Make the smallest code change that moves the game forward
3. Run the Playwright test script to exercise the change
4. Inspect screenshots and text state output for correctness
5. Review console errors and fix any regressions
6. Repeat until stable

The workflow relies on two integration points the game must expose: `window.render_game_to_text()` for machine-readable state and `window.advanceTime(ms)` for deterministic frame stepping. These let the Playwright script drive the game without flaky timing dependencies.

**What you will learn:**

- Setting up skill paths and verifying Playwright prerequisites
- The implement-test-inspect core development loop
- Canvas layout, visual guidelines, and state exposure patterns
- Deterministic time stepping for reliable automated testing
- Progress tracking across agent handoffs
- Multi-step interaction verification and regression testing

**Prerequisites:**

- Node.js >= 18 with npm/npx on `PATH`
- Playwright (local dependency or global install via `npm install -g @playwright/mcp@latest`)
- An HTML file serving a Canvas-based game on a local dev server

## Learning Path

### Level 1: Project Setup

**Set skill paths once per session:**

```bash
export SKILL_HOME="${SKILL_HOME:-$HOME/.claude/skills/develop-web-game}"
export WEB_GAME_CLIENT="$SKILL_HOME/scripts/web_game_playwright_client.js"
export WEB_GAME_ACTIONS="$SKILL_HOME/references/action_payloads.json"
```

**Verify Playwright availability:**

```bash
command -v npx >/dev/null 2>&1 && echo "npx ready" || echo "install Node.js first"
```

If `npx` is missing, install Node.js and npm. If the project already has a local `playwright` dependency, prefer that over a global install.

**Initialize progress tracking:**

If `progress.md` exists, read it first and confirm the original user prompt is recorded at the top (prefixed with `Original prompt:`). Note any TODOs and suggestions left by a previous agent. If the file is missing, create it:

```markdown
Original prompt: <user's request here>

## Progress
- [ ] Initial setup complete
```

Update `progress.md` after each meaningful chunk of work so another agent can pick up seamlessly.

### Level 2: Core Development Loop

The fundamental cycle is implement-run-inspect-fix:

**Step 1 -- Implement a small change.** Modify the game code to add or adjust a single feature. Keep changes minimal so failures are easy to diagnose.

**Step 2 -- Run the Playwright test script:**

```bash
node "$WEB_GAME_CLIENT" \
  --url http://localhost:5173 \
  --actions-file "$WEB_GAME_ACTIONS" \
  --click-selector "#start-btn" \
  --iterations 3 \
  --pause-ms 250
```

Required flags: `--url` and one of `--actions-file`, `--actions-json`, or `--click`. The script launches Chromium, injects the virtual-time shim, runs action bursts, captures screenshots to `output/web-game/shot-{i}.png`, and writes `state-{i}.json` from `render_game_to_text()`.

**Step 3 -- Inspect screenshots.** Open each `shot-{i}.png` and verify expected visuals. Do not skip this step; screenshots are the source of truth for what the player sees.

**Step 4 -- Inspect text state.** Read `state-{i}.json` and confirm it matches what the screenshot shows. If `render_game_to_text` disagrees with the visual, fix the state function.

**Step 5 -- Check console errors.** If `errors-{i}.json` exists, fix the first new error before continuing. The script halts on the first error iteration.

**Step 6 -- Iterate.** Change one variable at a time (frames, inputs, timing, positions), then repeat steps 2-5 until stable.

### Level 3: Advanced Verification

**Multi-step interaction testing:**

For each important interaction, trace the full causal chain and verify every intermediate state:

- Shooting an enemy: projectile spawns, travels, hits target, target health decreases, at zero health target disappears, score updates
- Collecting a key: key disappears from map, inventory updates, locked door becomes passable, player can enter next area
- Menu navigation: start/pause/resume/restart transitions all function correctly

Exercise all control paths: move, jump, shoot/attack, interact/use, menu select/confirm/cancel, pause/resume, restart, and any special abilities.

**Inline action bursts:**

When `--actions-file` is not flexible enough, pass actions directly:

```bash
node "$WEB_GAME_CLIENT" \
  --url http://localhost:5173 \
  --actions-json '{"steps":[{"buttons":["left_mouse_button"],"frames":2,"mouse_x":120,"mouse_y":80},{"buttons":[],"frames":6},{"buttons":["right"],"frames":8},{"buttons":["space"],"frames":4}]}' \
  --iterations 1
```

**Headed mode for debugging:**

When headless screenshots look wrong (e.g., blank canvas from WebGL capture issues), switch to headed mode:

```bash
node "$WEB_GAME_CLIENT" \
  --url http://localhost:5173 \
  --actions-file "$WEB_GAME_ACTIONS" \
  --headless false
```

**Reset between scenarios:**

When testing distinct features, avoid cross-test state contamination. Reload the page or restart the dev server between unrelated test runs.

## Best Practices

### Do

- Expose `window.render_game_to_text()` returning concise JSON with mode, player position/velocity, active entities, score, and state flags
- Expose `window.advanceTime(ms)` wired into the game update loop for deterministic frame stepping
- Use a single Canvas element centered in the viewport
- Draw backgrounds on the canvas itself, not via CSS
- Keep on-screen text minimal; show controls on a start/menu screen
- Include coordinate system documentation in `render_game_to_text` output (origin, axis directions)
- Capture gameplay screenshots beyond the start screen covering all new features
- Update `progress.md` with TODOs and findings after each work session

### Avoid

- Inventing a new test client; always use `$WEB_GAME_CLIENT` unless explicitly required
- Relying on wall-clock timing in tests; always use the `advanceTime` hook
- Making large multi-feature changes between test runs
- Skipping screenshot inspection; treating generated screenshots as the source of truth
- Overlaying dense text on the game canvas during play
- Using overly dark scenes that obscure interactive elements
- Leaving `progress.md` without updating it at session end

## Common Questions

### Q: The canvas screenshot is blank or transparent?

**A**: This usually means the canvas content was not captured correctly in headless mode. The script tries three capture methods: `canvas.toDataURL()`, Playwright element screenshot, and viewport clip. If all fail, rerun with `--headless false` to rule out WebGL/SwiftShader issues. Ensure the canvas has rendered at least one frame before capture.

### Q: Tests are flaky with inconsistent state between runs?

**A**: Make sure `window.advanceTime(ms)` is connected to your game loop. Without deterministic time stepping, `requestAnimationFrame` timing varies between runs. The virtual-time shim intercepts `setTimeout`, `setInterval`, and `requestAnimationFrame` but the game loop must use `advanceTime` when available.

### Q: How do I test keyboard and mouse input combinations?

**A**: Define action steps with multiple buttons and frame counts. Each step presses the listed buttons, advances the specified number of frames via `advanceTime`, then releases:

```json
{
  "steps": [
    { "buttons": ["left", "space"], "frames": 4 },
    { "buttons": [], "frames": 10 },
    { "buttons": ["right"], "frames": 8 }
  ]
}
```

Mouse actions use `left_mouse_button` or `right_mouse_button` with `mouse_x`/`mouse_y` coordinates relative to the canvas.

### Q: Can I run this without a local dev server?

**A**: You need an HTTP URL. Start a local server with `npx serve .` or `python3 -m http.server 5173` and point `--url` to it.

## Examples

### Example 1: Add a Jump Mechanic

```
User: Add jumping to the player character
Assistant:
  1. Adds velocity_y and gravity to player state
  2. Wires Space key to set velocity_y = -12
  3. Updates render_game_to_text to include velocity_y
  4. Runs: node "$WEB_GAME_CLIENT" --url http://localhost:5173 \
       --actions-json '{"steps":[{"buttons":["space"],"frames":4},{"buttons":[],"frames":20}]}' \
       --iterations 1
  5. Opens shot-0.png -- player is mid-air, ground visible below
  6. Reads state-0.json -- velocity_y is negative (ascending)
  7. No errors-0.json -- clean run
  Result: Jump mechanic working, player returns to ground after 20 frames
```

### Example 2: Debug a Collision Bug

```
User: Enemies pass through walls on the right side
Assistant:
  1. Reads render_game_to_text output showing enemy x > wall_x
  2. Finds boundary check uses < instead of <=
  3. Fixes: if (enemy.x + enemy.r >= wall.x) enemy.vx *= -1
  4. Runs test script with enemies moving right for 30 frames
  5. Opens screenshots -- enemies now bounce off right wall
  6. Verifies state JSON shows enemy.x stays within bounds
  7. Tests left wall too (regression check) -- still works
  Result: Collision fixed for both walls, no regressions
```

## Guardrails

- Always run `$WEB_GAME_CLIENT` after each meaningful change; do not skip the test step
- Always visually inspect screenshots; do not assume correctness from state JSON alone
- Fix the first console error before continuing to the next feature
- Keep `progress.md` updated so handoffs between agents are seamless
- Do not switch from the bundled Playwright client to `@playwright/test` unless explicitly asked
- Change one variable at a time when debugging; large changes make failures hard to isolate
- Prefer a single canvas with `render_game_to_text` and `advanceTime` integration points
- Use `--screenshot-dir` to organize output per test scenario when running multiple test suites

## References

Load these on demand when deeper detail is needed:

- **Game architecture patterns**: `references/game-architecture.md` -- Canvas setup, render_game_to_text implementation, advanceTime hook, fullscreen toggle
- **Playwright test patterns**: `references/playwright-testing.md` -- test script flags, action payload format, virtual-time shim internals, capture methods
