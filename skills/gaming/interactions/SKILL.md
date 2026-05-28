---
name: interactions
description: Add 3D interactable protocol, detection, and item interactions
compatibility: opencode
---
# Skill: Interactables (3D)

## Objective
Provide a consistent interaction system for:
- NPC conversations
- signs/plaques
- containers that give items once

## Recommended pattern
- Player owns an `InteractionDetector` (`Area3D`) that tracks nearby interactables.
- Interactables join group: `interactable`
- Interactables implement an API (interface-by-convention):
  - `get_prompt() -> String`
  - `interact(actor: Node) -> void`

## Steps
1) Create a reusable base script
- `game/scripts/exploration/interactable.gd` (`class_name Interactable`)

2) Create interactable scenes
- `game/scenes/actors/NPC.tscn`
- `game/scenes/props/Sign.tscn`
- `game/scenes/props/Container.tscn`

3) Player selection
- On `interact` action:
  - select nearest interactable in range
  - call `interact(self)`

## Verification
- NPC: shows dialogue and closes cleanly.
- Sign: shows text and closes cleanly.
- Container: adds item and becomes empty after first open.
