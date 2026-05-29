---
name: scenario-runner-capture
description: Implement deterministic Scenario Runner + capture outputs for agents
compatibility: opencode
---
# Skill: Scenario Runner + Capture

## Objective
Allow agents to validate gameplay and visuals without controlling the OS window.

## Steps

1) Implement a Scenario Runner autoload
- `game/autoload/ScenarioRunner.gd`
- Parse CLI args after `--`:
  - `--scenario <id>`
  - `--capture_dir <dir>`
  - `--seed <int>`
  - `--quit_after_frames <int>`

2) Define scenario scripts
- Store scenarios under `tests/scenarios/` (JSON)
- Actions should include:
  - wait_frames
  - move_to
  - interact_nearest
  - trigger_encounter
  - select_battle_command

3) Capture outputs
- Always write a `trace.json` of executed actions + timings
- Primary: use deterministic movie capture mode in Godot CLI (Movie Maker)
- Secondary: checkpoint screenshots if stable

4) CI scripts
- Implement `tools/ci/run-scenario.sh <scenario_id>`

## Verification
- Scenario runs headlessly
- Artifacts appear in `captures/` or specified capture dir
- Runs are deterministic across repeated runs on the same machine
