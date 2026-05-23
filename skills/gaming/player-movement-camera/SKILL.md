---
name: player-movement-camera
description: Implement 3D exploration movement + fixed 3/4 camera + 8-direction facing
compatibility: opencode
---
# Skill: Player Movement + Camera (Exploration, 3D)

## Objective
Implement exploration movement for a 2.5D JRPG:
- 3D world, sprite characters
- fixed 3/4 overhead camera (no rotation)
- free analog movement with 8-direction facing selection

## Steps

1) Create `game/scenes/actors/Player.tscn`
Suggested node tree:
- `CharacterBody3D` (root)
  - `AnimatedSprite3D` (visual)
  - `CollisionShape3D`
  - `Area3D` (InteractionDetector)

2) Implement `game/scripts/exploration/player.gd`
- Read analog input (`move` vector) and convert to world-space.
- Use `move_and_slide()`.
- Derive facing direction (8-way) from the movement vector.
- Drive the `AnimatedSprite3D` animation based on facing + locomotion.

3) Camera
- Add a fixed `Camera3D` (orthographic recommended) that follows the player.
- Keep camera stable (no per-frame jitter).

Calibration guidance (initial):
- Use the `spec.md` reference resolution (1920×1080) as the composition target.
- Target: humanoid ~160 px tall at 1080p.
- Start with an orthographic camera and tune `Camera3D.size` until the target is met.

4) Test scene
- Create `game/scenes/tests/TestRoom_Movement.tscn` with walls + obstacles.

## Verification
- Player cannot pass through walls.
- Diagonals are not faster than cardinals.
- Facing changes correctly across 8 directions.
- Camera is stable and framing consistent.
