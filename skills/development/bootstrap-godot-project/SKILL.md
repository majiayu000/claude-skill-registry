---
name: bootstrap-godot-project
description: Bootstrap Godot 4.5 project scaffolding for iOS-first 2.5D JRPG
compatibility: opencode
---
# Skill: Bootstrap Godot Project (Godot 4.5, iOS-first)

## Objective
Create a Godot **4.5** project that is:
- iOS landscape-first
- friendly to headless automation
- organized under `res://game/...`

## Steps

1) Create the project
- Create a new Godot project at the repo root so `project.godot` is at `./project.godot`.

2) Configure display
- Landscape-only orientation (iOS).
- Use UI anchors and scaling; do not hardcode a tiny internal resolution.
- Provide a single reference layout resolution (1920x1080) for UI mockups.

3) Define InputMap actions
Required:
- `move`
- `interact`
- `menu`
- `cancel`

Suggested bindings for desktop testing:
- Movement: WASD + arrows
- Interact: Enter/Space
- Cancel: Esc
- Menu: Tab

4) Add autoload singletons
- `GameState.gd`
- `SceneRouter.gd`
- `ScenarioRunner.gd` (can be no-op at first)

5) Create bootstrap scenes
- `game/bootstrap/Main.tscn`
  - loads initial scene
  - owns fade layer (or delegates to SceneRouter)

## Verification checklist
- `godot --path .` launches without errors.
- `godot --headless --path . --quit` returns success.
- Input actions exist and are spelled consistently.
