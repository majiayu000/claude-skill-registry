---
name: godot
version: 1.2.0
description: Develop, test, build, and deploy Godot 4.x games. Includes GdUnit4 for GDScript unit tests and PlayGodot for game automation and E2E testing. Supports web/desktop exports, CI/CD pipelines, and deployment to Vercel/GitHub Pages/itch.io.
---

# Godot Skill (Streamlined)

## What This Is For
Use this when working in Godot 4.x projects: playtesting, debugging, writing GDScript, or running tests.

---

## HPV Best Practices (Headed Playability)
- Prefer fewer, batched inputs with 400-800 ms waits, then verify state once.
- Cache key nodes once per session (world root, player, DialogueBox) to avoid repeat lookups.
- Gate actions on state checks (DialogueBox visible, quest flags, markers) to avoid loops.
- Use teleport/runtime eval to reach targets quickly, then interact like a human would.
- In this repo, minigames are typically skipped unless explicitly requested.

---

## MCP Quick Flow (Typical)
1) Start project headed.
2) Inspect runtime scene tree once.
3) Teleport to target.
4) Trigger interaction.
5) Verify with DialogueBox text or flag state.

---

## Headless Logic Checks (HLC)
Run logic tests when you are in an engineering role:

- godot --headless --path . --script tests/run_tests.gd
- godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests

---

## GdUnit4 Quick Start
Basic structure:
- extends GdUnitTestSuite
- use scene_runner for scene tests
- await runner.await_idle_frame() before input

---

## PlayGodot (Optional)
PlayGodot is useful for external automation but requires a custom Godot fork.
Consider it when the project specifically needs E2E automation.

---

## Export/Deploy (Optional)
Reserve this for tasks that explicitly require exporting or deployment.
