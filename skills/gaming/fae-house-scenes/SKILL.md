---
name: fae-house-scenes
description: Build Fae's house scenes (3D low-poly) consistent with Cloverhollow style lock
compatibility: opencode
---
# Skill: Build Fae’s House Scenes (3D)

## Objective
Create Fae’s house as the player’s starting location, using the same exploration camera and 3D toon style as the overworld.

Minimum required rooms for the vertical slice:
- Bedroom (start)
- Hall or Living room (navigation hub)

### Must-have interactions
- Bed: flavor/rest stub
- Desk or container: starter item pickup (Journal)
- Door(s) to town

## Steps

1) Bedroom scene
- Path: `game/scenes/areas/cloverhollow/interiors/Area_Cloverhollow_FaeHouse_Bedroom.tscn`
- Build a simple low-poly room:
  - floor + walls
  - a bed
  - a desk/container
- Add collisions for walls and large furniture
- Add spawn marker `SPAWN_BEDROOM`

2) Hall/Living scene
- Path: `game/scenes/areas/cloverhollow/interiors/Area_Cloverhollow_FaeHouse_Living.tscn`
- Keep layout navigable with clear exits
- Add at least 2 flavor props
- Add spawn marker `SPAWN_LIVING`

3) Door wiring
- Use Door interactables that call SceneRouter:
  - Bedroom ↔ Living
  - Living → Cloverhollow Town (exterior)

4) Starter item pickup
- Add a Container interactable in Bedroom that grants the Journal item (stub ItemDef ok).
- Set a GameState flag so it cannot be collected twice.

5) Scenario Runner
- Add scenario `tests/scenarios/vertical_slice_house_to_town.json`:
  - start in bedroom
  - collect journal
  - exit to town
  - capture checkpoints

## Verification
- New game starts in Bedroom.
- Journal pickup works once and is persisted.
- Player can reach Town reliably via deterministic spawn markers.
- Scenario passes headlessly and produces artifacts.