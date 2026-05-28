---
name: scene-transitions
description: Implement 3D scene routing, fades, and spawn points
compatibility: opencode
---
# Skill: Scene Transitions + Spawn Points (3D)

## Objective
Implement transitions between discrete area scenes with deterministic spawn placement.

## Steps

1) Define spawn points in each area scene
- Add a `SpawnPoints` `Node3D`.
- Add `Marker3D` children named by spawn id (e.g., `FrontDoor`, `BedroomDoor`).

2) Implement `SceneRouter` autoload
Responsibilities:
- `goto(scene_path: String, spawn_id: String)`
- fade out -> change scene -> position player at spawn -> fade in
- preserve `GameState` across scenes

3) Implement a reusable `Door` node/scene
- `Area3D` with exported fields:
  - target scene path
  - target spawn id
- On interact, call `SceneRouter.goto(...)`.

## Verification
- Entering a door reliably changes scenes.
- Player appears at the correct spawn marker every time.
- Inventory/flags persist across transitions.
